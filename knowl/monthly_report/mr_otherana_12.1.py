#!/usr/bin/env python3
# -*- encoding:utf-8 -*-
import sys

sys.path.append('/usr/software/knowl')
import PGUtil
import CommUtil
import DBUtil
import psycopg2
import ResultCode
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def getsqlresult(db, sql):
    result = db.execute(sql)
    if (result.code != 0):
        msg = result.msg
        print("msg=WORD_BEGIN" + msg + "WORD_END")
        sys.exit()

    sqlresult = result.msg.fetchall()
    for resulttolist in sqlresult:
        sqlresult[sqlresult.index(resulttolist)] = list(resulttolist)
    return sqlresult


def scnoutalert(pg, targetid, begin_time, end_time):
    ana = ""
    head = ['发生时间', '推进时间(分钟)', '推进原因']
    des = "SCN外部推进告警"
    tipmaxvalue = None
    sqlalert = '''
select begin_time,log_signature ,' ' as reason from log_detail where begin_time between '{0}' and '{1}'
 and target_id='{2}' and upper(log_code)='SCN-00001' limit 10'''.format(begin_time, end_time, targetid)
    scnoutresult = getsqlresult(pg, sqlalert)
    sqltip = '''
select max(metric_value::numeric ) from p_perf_eva_detail where metric_id='2180502' 
and target_id='{0}' and record_time between '{1}' and '{2}' '''.format(targetid, begin_time, end_time)
    tipresult = getsqlresult(pg, sqltip)

    for row in scnoutresult:
        row[2] = row[1].split(',', 1)[1].replace('[', '').replace(']', '')
        row[1] = row[1].split(',', 1)[0].replace('[', '').replace(']', '')
    # print(scnoutresult)

    for row in tipresult:
        tipmaxvalue = row[0]
    if scnoutresult:
        ana += "捕获到SCN较大的推进告警,建议安装db link白名单工具。"
    if tipresult[0][0] is not None:
        if tipmaxvalue > 16000:
            ana += "指标calls to kcmgas出现异常，出现SCN异常增长。"

    sqlresult = CommUtil.createTable(head, scnoutresult, des)
    return ana, sqlresult


def scnheadroom(pg, targetid, begin_time, end_time):
    head = ['上月SCN headroom', '本月SCN headroom', '差异']
    des = "SCN headroom信息"
    sql = '''
select coalesce(lm.error_data,'0') lmd,coalesce(cm.error_data,'0') cmd,
coalesce(cm.error_data::numeric,0)-coalesce(lm.error_data::numeric,0) diff
from 
(select item_desc,case when error_data='' then '0' else error_data end from dc_job_log_detail d where dc_log_id=(
select max(id) from dc_job_log l where target_id='{0}' 
and l.handle_time + interval '1 month' between '{1}' and '{2}') and item_desc='SCN Headroom检查') lm full join
(select item_desc,case when error_data='' then '0' else error_data end from dc_job_log_detail d where dc_log_id=(
select max(id) from dc_job_log l where target_id='{0}' and l.handle_time between '{1}' and '{2}') and item_desc='SCN Headroom检查') cm
on lm.item_desc=cm.item_desc'''.format(targetid, begin_time, end_time)
    scnheadroomresult = getsqlresult(pg, sql)
    sqlresult = CommUtil.createTable(head, scnheadroomresult, des)
    return sqlresult


if __name__ == '__main__':
    dbInfo = eval(sys.argv[1])
    ##pg info
    dbip = dbInfo['pg_ip']
    dbname = dbInfo['pg_dbname']
    username = dbInfo['pg_usr']
    password = dbInfo['pg_pwd']
    pgport = dbInfo['pg_port']
    ##ora info
    usr = dbInfo['ora_usr']
    pwd = dbInfo['ora_pwd']
    host = dbInfo['ora_ip']
    port = dbInfo['ora_port']
    database = dbInfo['ora_sid']

    targetid = dbInfo['targetId']
    begintime = dbInfo['start_time']
    endtime = dbInfo['end_time']
    rpt_id = dbInfo['rptid']

    pg = PGUtil.Postgre(dbip, username, password, pgport, dbname)

    try:
        scnheadroomresult = scnheadroom(pg, targetid, begintime, endtime)
        scnnote, scnalertresult = scnoutalert(pg, targetid, begintime, endtime)
        if scnheadroomresult:
            # print("msg=" + scnheadroomresult)
            sqlsr = '''
begin;
delete from rpt_stat_item where rpt_id='{0}' and rpt_item='SCN headroom' and target_id='{1}';
insert into rpt_stat_item (rpt_id,rpt_item,rpt_value,rpt_value_l,target_id)
select '{0}' rptid,'SCN headroom' rptitem,cmd,lmd,'{1}' target_id
from (
select coalesce(lm.error_data,'0') lmd,coalesce(cm.error_data,'0') cmd,
coalesce(cm.error_data::numeric,0)-coalesce(lm.error_data::numeric,0) diff
from 
(select item_desc,case when error_data='' then '0' else error_data end from dc_job_log_detail d where dc_log_id=(
select max(id) from dc_job_log l where target_id='{1}' 
and l.handle_time + interval '1 month' between '{2}' and '{3}' ) and item_seq=9) lm
full join 
(select item_desc,case when error_data='' then '0' else error_data end from dc_job_log_detail d where dc_log_id=(
select max(id) from dc_job_log l where target_id='{4}' and l.handle_time
	between '{5}' and '{6}' ) and item_seq=9) cm
on lm.item_desc=cm.item_desc
) a;
end;'''.format(rpt_id, targetid, begintime, endtime, targetid, begintime, endtime)
            pg.execute(sqlsr)

        if scnalertresult:
            # print("msg=" + scnalertresult)
            sqlsrt = '''
begin;
delete from rpt_scn_advanced where rpt_id='{0}' and target_id='{1}';
insert into rpt_scn_advanced(rpt_id,target_id,rpt_happen_time,rpt_time,rpt_reason)
select '{0}' rptid,
       '{1}' target_id,
       begin_time, 
       substring(log_signature,2,position('],[' in log_signature)-2)::numeric rptime,
       substring(log_signature,position('],[' in log_signature)+3,length(log_signature)-position('],[' in log_signature)-3) rpt
  from log_detail
 where begin_time between '{2}' and '{3}'
   and target_id='{4}' 
   and upper(log_code) = 'SCN-00001' ;
end;
'''.format(rpt_id, targetid, begintime, endtime, targetid)
            pg.execute(sqlsrt)

        if scnnote:
            # print("SCREEN_BEGIN问题与发现:\\n" + scnnote + "SCREEN_END")
            scnnote = '''问题与发现：
''' + scnnote
            ismf = '''
begin;
delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module='other_scn';

insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'other_scn' rpt_finding_module,
0 rpt_finding_type,'' rpt_sub_id,'' iname,
'SCN分析' rpt_finding_label,
'信息' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
0 rpt_finding_level;
end;
'''.format(rpt_id, targetid, scnnote)
            pg.execute(ismf)

    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

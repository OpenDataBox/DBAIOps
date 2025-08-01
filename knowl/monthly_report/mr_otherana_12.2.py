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


def getrecyclebin(pg, targetid, begin_time, end_time):
    ana = ""
    headsize = ['上月回收站大小(G)', '本月回收站大小(G)', '差异']
    headcnt = ['上月回收站对象数', '本月回收站对象数', '差异']
    des = "回收站分析"
    lm_recyclebincnt = None
    lm_recyclebinsize = None
    cm_recyclebincnt = None
    cm_recyclebinsize = None
    cntdiff = None
    sizediff = None
    sqlrecyclebin = '''
select lm.error_data lm_addinfo,cm.error_data cm_addinfo from 
(select item_desc,error_data from dc_job_log_detail d where dc_log_id=(
select max(id) from dc_job_log l where target_id='{0}' 
and l.handle_time + interval '1 month' between '{1}' and '{2}') and item_desc='回收站空间使用检查') lm
full join
(select item_desc,error_data from dc_job_log_detail d where dc_log_id=(
select max(id) from dc_job_log l where target_id='{0}' and l.handle_time between '{1}' and '{2}') and item_desc='回收站空间使用检查') cm
on lm.item_desc=cm.item_desc'''.format(targetid, begin_time, end_time)

    cyclebinresult = getsqlresult(pg, sqlrecyclebin)
    # print(cyclebinresult)

    for row in cyclebinresult:
        if row[0] is not None:
            lm_recyclebincnt = int(row[0].split(';')[0].split(':')[1])
            lm_recyclebinsize = float(row[0].split(';')[1].split(':')[1][:-2])
        if row[1] is not None:
            cm_recyclebincnt = int(row[1].split(';')[0].split(':')[1])
            cm_recyclebinsize = float(row[1].split(';')[1].split(':')[1][:-2])

    if cm_recyclebinsize is not None:
        if cm_recyclebinsize >= 1:
            ana += "回收站大小超过1G,请定期清理回收站空间。"
    if cm_recyclebincnt is not None:
        if cm_recyclebincnt >= 1000:
            ana += "回收站对象数超过1000,请定期清理回收站空间。"

    if cm_recyclebincnt is None:
        cm_recyclebincnt = "无本月数据"
    if lm_recyclebincnt is None:
        lm_recyclebincnt = "无上月数据"
    if cm_recyclebinsize is None:
        cm_recyclebinsize = "无本月数据"
    if lm_recyclebinsize is None:
        lm_recyclebinsize = "无上月数据"
    if cm_recyclebincnt == "无本月数据" or lm_recyclebincnt == "无上月数据":
        cntdiff = ''
    else:
        cntdiff = cm_recyclebincnt - lm_recyclebincnt
    if cm_recyclebinsize == "无本月数据" or lm_recyclebinsize == "无上月数据":
        sizediff = ''
    else:
        sizediff = cm_recyclebinsize - cm_recyclebinsize
    sqlcnt = "select '{0}','{1}','{2}'".format(lm_recyclebincnt, cm_recyclebincnt, cntdiff)
    # print(sqlcnt)
    sqlsize = "select '{0}','{1}','{2}'".format(lm_recyclebinsize, cm_recyclebinsize, sizediff)
    sqlcntresult = getsqlresult(pg, sqlcnt)
    sqlsizeresult = getsqlresult(pg, sqlsize)

    cntresult = CommUtil.createTable(headcnt, sqlcntresult, des)
    sizeresult = CommUtil.createTable(headsize, sqlsizeresult, des)

    return cntresult, sizeresult, ana


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
        cntresult, sizeresult, cyclebinnote = getrecyclebin(pg, targetid, begintime, endtime)
        if cntresult:
            # print("msg=" + cntresult)
            sqlcs = '''
begin;
delete from rpt_stat_item where rpt_id='{6}' and rpt_item='回收站对象数' and target_id='{0}';
insert into rpt_stat_item (rpt_id,rpt_item,rpt_value,rpt_value_l,target_id)
with a as (
select lm.error_data lmd,cm.error_data cmd from 
(select item_desc,error_data from dc_job_log_detail d where dc_log_id=(
select max(id) from dc_job_log l where target_id='{0}' 
and l.handle_time + interval '1 month' between '{1}' and '{2}') 
and item_desc='回收站空间使用检查') lm
full join
(select item_desc,error_data from dc_job_log_detail d where dc_log_id=(
select max(id) from dc_job_log l where target_id='{3}' and l.handle_time 
	between '{4}' and '{5}') and item_desc='回收站空间使用检查') cm
on lm.item_desc=cm.item_desc
),b as (
select
coalesce(split_part(split_part(cmd,';',1),':',2),'0') cmdcnt,
coalesce(split_part(split_part(cmd,';',2),':',2),'0') cmdsize,
coalesce(split_part(split_part(lmd,';',1),':',2),'0') lmdcnt,
coalesce(split_part(split_part(lmd,';',2),':',2),'0') lmdsize
from a)
select '{6}' rptid,'回收站对象数' rptitem,b.cmdcnt,b.lmdcnt,'{0}' from b;
end;
'''.format(targetid, begintime, endtime, targetid, begintime, endtime, rpt_id)
            pg.execute(sqlcs)

        if sizeresult:
            # print("msg=" + sizeresult)
            sqlss = '''
begin;
delete from rpt_stat_item where rpt_id='{6}' and rpt_item='回收站大小' and target_id='{0}';
insert into rpt_stat_item (rpt_id,rpt_item,rpt_value,rpt_value_l,target_id)
with a as (
select lm.error_data lmd,cm.error_data cmd from 
(select item_desc,error_data from dc_job_log_detail d where dc_log_id=(
select max(id) from dc_job_log l where target_id='{0}' 
and l.handle_time + interval '1 month' between '{1}' and '{2}') 
and item_seq=13) lm
full join
(select item_desc,error_data from dc_job_log_detail d where dc_log_id=(
select max(id) from dc_job_log l where target_id='{3}' and l.handle_time 
	between '{4}' and '{5}') and item_seq=13) cm
on lm.item_desc=cm.item_desc
),b as (
select
coalesce(split_part(split_part(cmd,';',1),':',2),'0') cmdcnt,
coalesce(split_part(split_part(cmd,';',2),':',2),'0') cmdsize,
coalesce(split_part(split_part(lmd,';',1),':',2),'0') lmdcnt,
coalesce(split_part(split_part(lmd,';',2),':',2),'0') lmdsize
from a)
select '{6}' rptid,'回收站大小' rptitem,b.cmdsize,b.lmdsize,'{0}' target_id from b;
end;
'''.format(targetid, begintime, endtime, targetid, begintime, endtime, rpt_id)
            pg.execute(sqlss)

        if cyclebinnote:
            # print("SCREEN_BEGIN问题与发现:\\n" + cyclebinnote + "SCREEN_END")
            cyclebinnote = '''问题与发现：
''' + cyclebinnote
            ismf = '''
begin;
delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module='other_recycle';

insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'other_recycle' rpt_finding_module,
0 rpt_finding_type,'' rpt_sub_id,'' iname,
'回收站分析' rpt_finding_label,
'信息' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
0 rpt_finding_level;
end;
'''.format(rpt_id, targetid, cyclebinnote)
            pg.execute(ismf)

    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

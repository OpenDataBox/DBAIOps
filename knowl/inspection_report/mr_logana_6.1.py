#!/usr/bin/env python3
# -*- encoding:utf-8 -*-
import sys

sys.path.append('/usr/software/knowl')
import PGUtil
import CommUtil
import ResultCode
import DBUtil
import psycopg2
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def getValue(db, sql):
    result = db.execute(sql)
    if (result.code != 0):
        msg = result.msg
        print("msg=WORD_BEGIN" + msg + "WORD_END")
        sys.exit()
    return result.msg


def getlogdbinfo(pg, targetid, begin_time, end_time):
    ana = ""
    startcnt = 0
    shutNormalcnt = 0
    shutOther = 0
    head = ['序号', '时间', '启动与关闭', '类型', '日志信息']
    des = "数据库启动与关闭"
    sqlgetloginfo = '''
select row_number() over() as rownum,t.* from 
(select begin_time,case when log_code in ('EVT-00002','ORA-00004') then '关闭'
when log_code='EVT-00001' then '启动' end as operation,' ' as operation_type,log_text from log_detail
where log_code in ('EVT-00001','EVT-00002','ORA-00004') and begin_time between '{0}' and '{1}' 
 and target_id='{2}' order by begin_time) t '''.format(begin_time, end_time, targetid)
    sqlgetloginfocursor = getValue(pg, sqlgetloginfo)
    sqlgetloginforesult = sqlgetloginfocursor.fetchall()
    for resulttolist in sqlgetloginforesult:
        sqlgetloginforesult[sqlgetloginforesult.index(resulttolist)] = list(resulttolist)

    for row in sqlgetloginforesult:
        if row[2] == '启动':
            if 'Starting ORACLE instance (normal)' in row[4]:
                row[3] = "normal"
            elif 'Starting ORACLE instance (upgrade)' in row[4]:
                row[3] = "upgrade"
            elif 'Starting ORACLE instance (migrade)' in row[4]:
                row[3] = "migrade"
            elif 'Starting ORACLE instance (restrict)' in row[4]:
                row[3] = "restrict"
        if row[2] == '关闭':
            if 'Shutting down instance (immediate)' in row[4]:
                row[3] = "immediate"
            elif 'Shutting down instance (normal)' in row[4]:
                row[3] = "normal"
            elif 'Shutting down instance (abort)' in row[4]:
                row[3] = "abort"
            elif 'Shutting down instance (transactional)' in row[4]:
                row[3] = "transactional"
            else:
                row[3] = "database异常终止"

    # print(sqlgetloginforesult)

    for row in sqlgetloginforesult:
        if row[2] == '启动':
            startcnt += 1
        elif row[2] == '关闭' and row[3] == 'normal':
            shutNormalcnt += 1
        elif row[2] == '关闭' and row[3] != 'normal':
            shutOther += 1
    if startcnt > 0 or shutNormalcnt > 0 or shutOther > 0:
        ana = "本月数据库实例出现启动%s次，关闭%s次，其中正常关闭%s次，非正常关闭%s次。数据库启动关闭的详细日志如下：" % (
        startcnt, shutNormalcnt + shutOther, shutNormalcnt, shutOther)
    else:
        ana = "本月未发现数据库启动与关闭相关操作。"

    sqlresult = CommUtil.createTable(head, sqlgetloginforesult, des)
    return ana, sqlresult


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
        logdbinfonote, logdbinforesult = getlogdbinfo(pg, targetid, begintime, endtime)
        if logdbinforesult:
            # print("msg=SCREEN_BEGIN" + logdbinfonote + "SCREEN_END")
            insql_mf = '''
begin;
delete from rpt_inst_restart where rpt_id='{0}' and target_id='{1}';
insert into rpt_inst_restart(rpt_id,target_id,rpt_happen_time,rpt_oper,rpt_typ,rpt_log_info)
select '{0}' rptid,'{1}' target_id, begin_time,
       case
         when log_code in ('EVT-00002', 'ORA-00004') then
          '关闭'
         when log_code = 'EVT-00001' then
          '启动'
       end as operation,
       case when log_text like '%normal%' then 'normal'
	   when log_text like '%upgrade%' then 'upgrade'
	   when log_text like '%migrade%' then 'migrade'
	   when log_text like '%restrict%' then 'restrict'
	   when log_text like '%immediate%' then 'immediate'
	   when log_text like '%abort%' then 'abort'
	   when log_text like '%transactional%' then 'transactional'
	   else '异常'	   
	   end as operation_type,
       log_text
  from log_detail
 where log_code in ('EVT-00001', 'EVT-00002', 'ORA-00004')
   and begin_time between '{2}' and '{3}'
   and target_id = '{1}';
end;
'''.format(rpt_id, targetid, begintime, endtime)
            pg.execute(insql_mf)

        if logdbinfonote:
            # print("msg=" + logdbinforesult)
            ismf = '''
begin;
delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module='db_start_shutdown_ri';

insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'db_start_shutdown_ri' rpt_finding_module,
0 rpt_finding_type,'' rpt_sub_id,'' iname,
'数据库启动与关闭' rpt_finding_label,
'信息' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
0 rpt_finding_level;
end;
'''.format(rpt_id, targetid, logdbinfonote)
            pg.execute(ismf)

    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

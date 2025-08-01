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


##get max snap id according to date and target_id
def getmaxsnap(pg, targetid, begin_time, end_time):
    maxsnapid = ""
    sql = '''select max(snap_id::numeric ) from p_oracle_cib where target_id='{0}' and 
     record_time > '{1}'
    and record_time < '{2}' '''.format(targetid, begin_time, end_time)

    sqlrersult = getsqlresult(pg, sql)

    if sqlrersult:
        for row in sqlrersult:
            if not row[0] is None:
                maxsnapid = row[0]
            else:
                maxsnapid = -1
    else:
        maxsnapid = -1

    return maxsnapid


def backupana(pg, targetid, begin_time, end_time):
    ana = ""
    backupType = []
    backupdict = {}
    head = ['备份时间', '完成时间', '类型', '状态', '耗时', '大小(mb)']
    des = "备份分析"
    backupanaresult = []
    maxsnapid = getmaxsnap(pg, targetid, begin_time, end_time)
    sqlbackupinfo = '''
select start_time,end_time,input_type,status,ELAPSED_SECONDS/3600 hours,OUTPUT_BYTES/1024/1024 output_size_mb 
from backup_history where dbid::numeric =(select cib_value::numeric from p_oracle_cib where 
index_id='2201000' and cib_name = 'dbid' and target_id='{0}' and snap_id='{1}') 
and start_time between '{2}' and '{3}' order by start_time'''.format(targetid, maxsnapid, begin_time, end_time)
    # print(sqlbackupinfo)
    sqlbackupana1 = '''
select start_time,hours,output_device_type from 
(select start_time,ELAPSED_SECONDS/3600 hours,output_device_type from backup_history
where dbid::numeric =(select cib_value::numeric from p_oracle_cib where 
index_id='2201000' and cib_name = 'dbid' and target_id='{0}' and snap_id='{1}') and status='COMPLETED' and 
/*input_type in ('DB FULL','DB INCR') and*/ start_time between '{2}' and '{3}' 
order by start_time desc) foo limit 1'''.format(targetid, maxsnapid, begin_time, end_time)
    # print(sqlbackupana1)
    sqlbackupana2 = '''
    select '' as note,start_time from 
    (select start_time,ELAPSED_SECONDS/3600 hours,output_device_type from backup_history
    where dbid::numeric =(select cib_value::numeric from p_oracle_cib where 
    index_id='2201000' and cib_name = 'dbid' and target_id='{0}' and snap_id='{1}') and status='FAILED' and 
    /*input_type in ('DB FULL','DB INCR') and*/ start_time between '{2}' and '{3}' 
    order by start_time desc) foo limit 1'''.format(targetid, maxsnapid, begin_time, end_time)
    # print(sqlbackupana2)
    sqlbackupana3 = '''
    select '' as note,count(*) failcnt from 
    (select start_time,ELAPSED_SECONDS/3600 hours,output_device_type from backup_history
    where dbid::numeric =(select cib_value::numeric from p_oracle_cib where 
    index_id='2201000' and cib_name = 'dbid' and target_id='{0}' and snap_id='{1}') and status='FAILED' and 
    /*input_type in ('DB FULL','DB INCR') and*/ start_time between '{2}' and '{3}' 
    order by start_time desc) foo '''.format(targetid, maxsnapid, begin_time, end_time)
    # print(sqlbackupana3)
    sqlbackupana1result = getsqlresult(pg, sqlbackupana1)
    sqlbackupana2result = getsqlresult(pg, sqlbackupana2)
    sqlbackupana3result = getsqlresult(pg, sqlbackupana3)
    sqlbackupinforesult = getsqlresult(pg, sqlbackupinfo)

    for row in sqlbackupana1result:
        backupdict['最近一次成功全备时间'] = row[0]
        backupdict['最近一次成功全备耗时'] = row[1]
        backupdict['最近一次成功全备介质'] = row[2]

    for key, value in backupdict.items():
        backupanaresult.append([key, value])

    for row in sqlbackupana2result:
        row[0] = "最近一次失败全备时间"
        backupanaresult.append(row)

    for row in sqlbackupana3result:
        row[0] = "全备失败次数"
        if row[1] > 0:
            backupanaresult.append(row)

    if sqlbackupinforesult:
        for row in sqlbackupinforesult:
            if row[2] in ('DB FULL', 'DB INCR', 'DATAFILE FULL', 'DATAFILE INCR') and int(row[1].strftime("%H")) >= 8:
                ana += "数据文件的备份延续到8点之后，建议调整备份时间窗口，避免备份影响业务。"
            if row[4] >= 10:
                ana += "备份时间超过10小时，建议提升备份性能。"
            backupType.append(row[2])

        if "ARCHIVELOG" not in set(backupType):
            ana += "缺少归档备份，请增加归档备份策略。"
        if 'DB FULL' in set(backupType) or 'DB INCR' in set(backupType) or 'DATAFILE FULL' in set(
                backupType) or 'DATAFILE INCR' in set(backupType):
            pass
        else:
            ana += "缺少数据文件备份，请增加数据文件备份策略。"

    backupinforesult = CommUtil.createTable(head, sqlbackupinforesult, des)
    sqlresults = CommUtil.createTable('', backupanaresult, '')

    return ana, backupinforesult, sqlresults


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
        maxsnapid = getmaxsnap(pg, targetid, begintime, endtime)
        backupananote, backupinforesult, backupanaresult = backupana(pg, targetid, begintime, endtime)
        if backupinforesult:
            ##print("msg=" + backupinforesult)
            sqlrbh = '''
begin;
delete from rpt_backup_history where rpt_id='{0}' and target_id='{1}';
insert into rpt_backup_history(rpt_id,target_id,rpt_start_time,rpt_type,rpt_state,rpt_time,rpt_size)
select '{0}' rptid,'{1}' target_id,start_time,input_type,status,ELAPSED_SECONDS/3600 hours,OUTPUT_BYTES/1024/1024 output_size_mb 
from backup_history where dbid::numeric =(select cib_value::numeric from p_oracle_cib where 
index_id='2201000' and cib_name = 'dbid' and target_id='{1}' and snap_id='{2}') 
and start_time between '{3}' and '{4}' order by start_time;
end;'''.format(rpt_id, targetid, maxsnapid, begintime, endtime)
            pg.execute(sqlrbh)

        if backupanaresult:
            # print("msg=" + backupanaresult)
            sqlrbs = '''
begin;
delete from rpt_backup_summary where rpt_id='{12}' and target_id='{0}';
insert into rpt_backup_summary(rpt_id,target_id,rpt_fullbackup_datetime,rpt_fullbackup_times_consume,rpt_fullbackup_media,rpt_fail_count)
with a as (
select start_time,hours,output_device_type from 
(select start_time,ELAPSED_SECONDS/3600 hours,output_device_type from backup_history
where dbid::numeric =(select cib_value::numeric from p_oracle_cib where 
index_id='2201000' and cib_name = 'dbid' and target_id='{0}' and snap_id='{1}') and status='COMPLETED' and 
/*input_type in ('DB FULL','DB INCR') and*/ start_time between '{2}' and '{3}' 
order by start_time desc) foo limit 1),
b as (select '' as note,start_time from 
    (select start_time,ELAPSED_SECONDS/3600 hours,output_device_type from backup_history
    where dbid::numeric =(select cib_value::numeric from p_oracle_cib where 
    index_id='2201000' and cib_name = 'dbid' and target_id='{4}' and snap_id='{5}') and status='FAILED' and 
    /*input_type in ('DB FULL','DB INCR') and*/ start_time between '{6}' and '{7}' 
    order by start_time desc) foo limit 1),
c as (select '' as note,count(*) failcnt from 
    (select start_time,ELAPSED_SECONDS/3600 hours,output_device_type from backup_history
    where dbid::numeric =(select cib_value::numeric from p_oracle_cib where 
    index_id='2201000' and cib_name = 'dbid' and target_id='{8}' and snap_id='{9}') and status='FAILED' and 
    /*input_type in ('DB FULL','DB INCR') and*/ start_time between '{10}' and '{11}' 
    order by start_time desc) foo)
select '{12}' rptid, '{0}' target_id,(select start_time from a) rfd,	
(select hours from a) rftc,
(select output_device_type from a) rfm,
(select failcnt from c) rfc;
end;
'''.format(targetid, maxsnapid, begintime, endtime, targetid, maxsnapid, begintime, endtime, targetid, maxsnapid,
           begintime, endtime, rpt_id)
            pg.execute(sqlrbs)

        if backupananote:
            backupananote = """建议：
""" + backupananote
            ismf = '''
begin;
delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module='backup_history';
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'backup_history' rpt_finding_module,
0 rpt_finding_type,'' rpt_sub_id,'' iname,
'备份分析' rpt_finding_label,
'信息' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
0 rpt_finding_level;
end;
'''.format(rpt_id, targetid, backupananote)
            pg.execute(ismf)
            # print("SCREEN_BEGIN" + backupananote + "SCREEN_END")

    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

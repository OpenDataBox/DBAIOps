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


def getdbid(pg, targetid):
    dbid = ""
    sql = "select subuid from mgt_system where uid='{0}'".format(targetid)
    sqlresult = getsqlresult(pg, sql)
    for row in sqlresult:
        dbid = row[0]
    return dbid


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


def logswitchinfo(pg, targetid, begin_time, end_time):
    ana = ""
    head = ['日期', '实例', '最高次数/小时', '平均次数/小时']
    des = "日志切换分析"
    logfilesize = None
    archivelogfilesize = None
    threadlogcnt = []
    subuid = getdbid(pg, targetid)
    maxdbsnapid = getmaxsnap(pg, subuid, begin_time, end_time)
    sqllogswitch = '''
select to_char(log_day,'yyyymmdd'),thread,max(log_count) max_cnt,round(avg(log_count)) avg_cnt from log_history
where dbid = '{0}'  and log_day between '{1}' and '{2}' group by to_char(log_day,'yyyymmdd'),thread 
order by 1,2'''.format(subuid, begin_time, end_time)
    # print(sqllogswitch)
    sqllogswitchresult = getsqlresult(pg, sqllogswitch)

    sqlarchivedlogsize = '''
select round(avg(log_size/1024/1024)) archivelogsize from log_history  
where dbid = '{0}' and log_day between '{1}' and '{2}' 
'''.format(subuid, begin_time, end_time)
    # print(sqlarchivedlogsize)
    archivelogsize = getsqlresult(pg, sqlarchivedlogsize)
    # print(archivelogsize)

    sqlloginfo = '''
    select col1 as thread,col2 as loggroup,col6 as status,col4 as members,col5 as siz,col3 as sequence,col7 as archived from
    p_oracle_cib where index_id='2201003' and target_id='%s'
    and snap_id='%s' and seq_id=1''' % (subuid, maxdbsnapid)
    # print(sqlloginfo)
    logsizeresult = getsqlresult(pg, sqlloginfo)

    sqlthreadlogcnt = '''
    select col1 thread,count(col2) from p_oracle_cib where index_id='2201003' and target_id='%s'
    and snap_id='%s' and seq_id<>0 group by col1 ''' % (subuid, maxdbsnapid)
    # print(sqlthreadlogcnt)
    loggroupcntresult = getsqlresult(pg, sqlthreadlogcnt)
    # print(sqlthreadlogcnt)

    for row in logsizeresult:
        logfilesize = int(row[4])

    for row in loggroupcntresult:
        threadlogcnt.append(row[1])

    for row in sqllogswitchresult:
        if len(threadlogcnt):
            if row[2] > 6 and min(threadlogcnt) < 3:
                ana += "每小时日志切换次数最大超过6次，但单个线程日志组数量小于3，建议每个线程的日志组数量增加到3个以上。"
        if logfilesize:
            if row[2] > 10 and logfilesize < 500:
                ana += "每小时日志切换次数最大超过10次，但日志文件的SIZE小于500M，建议将日志文件的大小调大到适当的值。"

    for row in archivelogsize:
        # print(row)
        if row[0] is not None:
            if logfilesize:
                if row[0] < logfilesize / 2:
                    ana += "数据库手动日志切换太频繁，建议减少手动切换的频率。"

    sqlresult = CommUtil.createTable(head, sqllogswitchresult, des)

    return sqlresult, ana


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

        subuid = getdbid(pg, targetid)
        logswitchresult, logswitchnote = logswitchinfo(pg, targetid, begintime, endtime)
        if logswitchresult:
            ##print("msg=" + logswitchresult)
            lssql = '''
begin;
delete from rpt_log_history where rpt_id='{0}' and target_id='{1}';
insert into rpt_log_history(rpt_id,target_id,rpt_inst,rpt_time,rpt_max,rpt_avg)
select '{0}' rptid,{1} target_id,thread,to_char(log_day,'yyyymmdd'),max(log_count) max_cnt,round(avg(log_count)) avg_cnt 
  from log_history
 where dbid = '{2}'  and log_day between '{3}' and '{4}' group by to_char(log_day,'yyyymmdd'),thread 
 order by 1,2;
end;'''.format(rpt_id, targetid, subuid, begintime, endtime)
            pg.execute(lssql)

        if logswitchnote:
            ##print("SCREEN_BEGIN问题与发现:\\n" + logswitchnote+"SCREEN_END")
            logswitchnote = """问题与发现：
""" + logswitchnote
            ismf = '''
begin;
delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module='log_history';

insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'log_history' rpt_finding_module,
0 rpt_finding_type,'' rpt_sub_id,'' iname,
'日志切换分析' rpt_finding_label,
'信息' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
0 rpt_finding_level;
end;
'''.format(rpt_id, targetid, logswitchnote)
            pg.execute(ismf)

    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

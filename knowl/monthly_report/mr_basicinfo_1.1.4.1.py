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


def getdbid(pg, targetid):
    dbid = ""
    sql = "select subuid from mgt_system where uid='{0}'".format(targetid)
    sqlcursor = getValue(pg, sql)
    sqlresult = sqlcursor.fetchall()
    for row in sqlresult:
        dbid = row[0]
    return dbid


def getmaxsnap(pg, targetid, begin_time, end_time):
    sql = f'''
select max(record_time)
from p_oracle_cib
where target_id = '{targetid}'
  and record_time > '{begin_time}'
  and record_time < '{end_time}' 
    '''
    sql2 = f'''
    select max(record_time) from p_oracle_cib where target_id='{targetid}' 
    '''
    sqlcursor = getValue(pg, sql)
    sqlrersult = sqlcursor.fetchone()
    if sqlrersult[0] is not None:
        maxsnapid = sqlrersult[0]
    else:
        sqlcursor = getValue(pg, sql2)
        sqlrersult = sqlcursor.fetchone()
        maxsnapid = sqlrersult[0]
    return maxsnapid


def getloggroupinfo(pg, targetid, begin_time, end_time):
    ana = ""
    logmemberscnt = []
    logfilesize = []
    logfilestatus = []
    threadlogcnt = []
    head = ["线程", "组号", "状态", "日志大小(mb)", "成员数量", "序号", "是否归档"]
    des = "在线日志组信息"
    dbid = getdbid(pg, targetid)
    maxsnapid = getmaxsnap(pg, dbid, begin_time, end_time)
    sqlloginfo = '''
select col1 as thread,col2 as loggroup,col6 as status,col5 as siz,col4 as members,col3 as sequence,col7 as archived from
p_oracle_cib where index_id='2201003' and target_id='%s'
and record_time='%s' and seq_id<>0''' % (dbid, maxsnapid)
    # print(sqlloginfo)
    loginfocursor = getValue(pg, sqlloginfo)
    loginforesults = loginfocursor.fetchall()
    sqlResult = CommUtil.createTable(head, loginforesults, des)
    sqlthreadlogcnt = '''
select col1 thread,count(col2) from p_oracle_cib where index_id='2201003' and target_id='%s'
and record_time='%s' and seq_id<>0 group by col1 ''' % (dbid, maxsnapid)
    # print(sqlthreadlogcnt)
    threadlogcntcursor = getValue(pg, sqlthreadlogcnt)
    threadlogcntresults = threadlogcntcursor.fetchall()
    for row in threadlogcntresults:
        threadlogcnt.append(row[1])
    if threadlogcnt:
        if min(threadlogcnt) < 3:
            ana += "每个线程最少需要3个日志组，建议增加至3个。"
        if len(set(threadlogcnt)) > 1:
            ana += "线程间日志组数量不一致，请保持不同线程间日志组数量一致。"
    for row in loginforesults:
        logmemberscnt.append(row[4])
    if len(set(logmemberscnt)) > 1:
        ana += "不同的日志组的成员数量不同，建议统一。"
    if '1' in logmemberscnt:
        ana += "建议每个日志组有2个成员，以提高数据库的可靠性。"
    for row in loginforesults:
        logfilesize.append(row[3])
        logfilestatus.append(2)
    if len(set(logfilesize)) > 1:
        ana += "存在不同日志组的文件大小不一致，建议所有日志组的文件大小一致。"
    if "UNUSED" in logfilestatus or "CLEARING" in logfilestatus or "CLEARING_CURRENT" in logfilestatus:
        ana += "存在CURRENT,ACTIVE,INACTIVE之外状态的日志组，请检查相关日志组状态。"

    return sqlResult, ana


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
        snapid = getmaxsnap(pg, subuid, begintime, endtime)
        loggroupinfo_result, loggroupinfonote = getloggroupinfo(pg, targetid, begintime, endtime)
        if loggroupinfo_result:
            # print("msg=" + loggroupinfo_result)
            sqllr = '''
begin;
delete from rpt_oracle_cib where rpt_id='{0}' and target_id='{1}' and seq_id=5;
insert into rpt_oracle_cib(rpt_id,target_id,index_id,seq_id,col1,col2,col3,col4,col5,col6,col7)
select '{0}' rptid,'{1}' target_id,seq_id index_id,5 seq_id,
case when seq_id=0 then '线程' else col1 end as thread,
case when seq_id=0 then '组号' else col2 end as loggroup,
case when seq_id=0 then '状态' else col6 end as status,
case when seq_id=0 then '日志大小(mb)' else col5 end as siz,
case when seq_id=0 then '成员数量' else col4 end as members,
case when seq_id=0 then '序号' else col3 end as sequence,
case when seq_id=0 then '是否归档' else col7 end as archived 
from
p_oracle_cib where index_id='2201003' and target_id='{2}'
and record_time='{3}';
end;
'''.format(rpt_id, targetid, subuid, snapid)
            pg.execute(sqllr)

        if loggroupinfonote:
            loggroupinfonote = """问题与发现：
""" + loggroupinfonote
            # print("SCREEN_BEGIN问题与发现:\\n" + loggroupinfonote+"SCREEN_END")
            ismf = '''
begin;
delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module='basic_redolog';
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'basic_redolog' rpt_finding_module,
0 rpt_finding_type,'' rpt_sub_id,'' iname,
'在线日志组情况' rpt_finding_label,
'信息' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level;
end;
'''.format(rpt_id, targetid, loggroupinfonote)
            pg.execute(ismf)

    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

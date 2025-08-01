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


def getValue(db, sql):
    result = db.execute(sql)
    if (result.code != 0):
        msg = result.msg
        print("msg=WORD_BEGIN" + msg + "WORD_END")
        sys.exit()
    return result.msg


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


def getdbid(pg, targetid):
    dbid = ""
    sql = "select subuid from mgt_system where uid='{0}'".format(targetid)
    sqlcursor = getValue(pg, sql)
    sqlresult = sqlcursor.fetchall()
    for row in sqlresult:
        dbid = row[0]
    return dbid


def getlogfileinfo(pg, targetid, begin_time, end_time):
    ana = ""
    logmemberloccnt = []
    head = ["组号", "状态", "文件名", "备注"]
    des = "在线日志文件信息"
    filelist = []
    dbid = getdbid(pg, targetid)
    maxsnapid = getmaxsnap(pg, dbid, begin_time, end_time)
    sqllogfileinfo = '''
select col1,case when col2 is null then ' ' when col4='' then ' ' else col2 end,col4,' ' as note from p_oracle_cib where index_id='2201008' and target_id='{0}'	
and record_time='{1}' and seq_id<>0'''.format(dbid, maxsnapid)
    # print(sqllogfileinfo)
    # print(sqllogfileinfo)
    sqllogfileinfocursor = getValue(pg, sqllogfileinfo)
    sqllogfileinforesults = sqllogfileinfocursor.fetchall()

    for resulttolist in sqllogfileinforesults:
        sqllogfileinforesults[sqllogfileinforesults.index(resulttolist)] = list(resulttolist)

    for row in sqllogfileinforesults:
        if row[1] != ' ':
            row[3] = "日志文件存在问题,请检查。"
    sqlResult = CommUtil.createTable(head, sqllogfileinforesults, des)

    for row in sqllogfileinforesults:
        filelist.append((row[0], '/'.join(row[2].split('/')[:-1])))

    for row in set(filelist):
        if filelist.count(row) > 1:
            ana += "同一日志组的不同成员建议存放于不同的目录下，以提高数据库的可靠性。"

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

        loggroupinfo_result, loggroupinfonote = getlogfileinfo(pg, targetid, begintime, endtime)
        if loggroupinfo_result:
            # print("msg=" + loggroupinfo_result)
            sqllr = '''
begin;
delete from rpt_oracle_cib where rpt_id='{0}' and target_id='{1}' and seq_id=6;
insert into rpt_oracle_cib(rpt_id,target_id,index_id,seq_id,col1,col2,col3,col4)
select '{0}' rptid,'{1}' target_id,seq_id index_id,6 seq_id,col1 zh,
case when col2 is null then col3 else col2 end status,
case when seq_id=0 then '文件名' else col4 end col4,
case when seq_id=0 then '备注' else '' end as note 
from p_oracle_cib where index_id='2201008' and target_id='{2}' 
and record_time='{3}';
end;
'''.format(rpt_id, targetid, subuid, snapid)
            pg.execute(sqllr)
        if loggroupinfonote:
            # print("SCREEN_BEGIN问题与发现:\\n" + loggroupinfonote+"SCREEN_END")
            loggroupinfonote = """问题与发现：
""" + loggroupinfonote
            ismf = '''
begin;
delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module='basic_logfile';

insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'basic_logfile' rpt_finding_module,
0 rpt_finding_type,'' rpt_sub_id,'' iname,
'在线日志文件情况' rpt_finding_label,
'信息' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level;
end;
'''.format(rpt_id, targetid, loggroupinfonote)
            pg.execute(ismf)

    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

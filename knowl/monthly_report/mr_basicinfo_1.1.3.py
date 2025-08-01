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
    # print(sql)
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


def getControlfileInfo(pg, targetid, begin_time, end_time):
    ana = ""
    filelocation = []
    head = ["状态", "文件名", "是否位于恢复区域", "块大小", "文件大小(mb)", "备注"]
    des = "控制文件信息"
    dbid = getdbid(pg, targetid)
    maxsnapid = getmaxsnap(pg, dbid, begin_time, end_time)
    sql = '''
select case when col2 is null then ' '
when col2='' then ' ' else col2 end status,col1 as name,col5 IS_RECOVERY_DEST_FILE,col3 block_size,col4 file_size_blks,' ' as note
from p_oracle_cib where index_id=2201007 and target_id='{0}' and seq_id<>0 and 
record_time ='{1}' '''.format(dbid, maxsnapid)
    # print(sql)
    cursor = getValue(pg, sql)
    results = cursor.fetchall()
    # print(results)
    for resulttolist in results:
        results[results.index(resulttolist)] = list(resulttolist)

    for row in results:
        if row[0] != ' ':
            row[5] = '控制文件存在问题'
        else:
            row[5] = ' '
        row[4] = round(int(row[3]) * int(row[4]) / 1024 / 1024, 2)
    sqlResult = CommUtil.createTable(head, results, des)
    if len(results) == 1:
        ana += "控制文件只有一个，存在安全风险，建议至少设置2个控制文件，提高数据库整体的可靠性。"
    for row in results:
        if row[0] != ' ':
            ana += "控制文件：%s存在问题，请深入核查。" % row[1]
        filelocation.append('/'.join(row[1].split('/')[:-1]))

    if len(filelocation) != len(set(filelocation)) and len(results) > 1:
        ana += "所有控制文件都存放在同一个目录下：建议不同的控制文件放置在不同的目录下，以提高数据库整体的可靠性。"

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

        controlfileinforesult, controfilenote = getControlfileInfo(pg, targetid, begintime, endtime)
        if controlfileinforesult:
            # print("msg=" + controlfileinforesult)
            sqlcff = '''
begin;
delete from rpt_oracle_cib where rpt_id='{0}' and target_id='{1}' and seq_id=4;
insert into rpt_oracle_cib(rpt_id,target_id,index_id,seq_id,col1,col2,col3,col4,col5,col6)
select '{0}' rptid,'{1}' target_id,seq_id index_id,4 seq_id,col2 status,col1 as name,
case when col5='恢复区' then '是否位于恢复区域' else col5 end IS_RECOVERY_DEST_FILE,
col3 block_size,
case when col4='块数' then '文件大小(mb)' else col4 end file_size_blks,'' as note
from p_oracle_cib where index_id=2201007 and target_id='{2}' 
and record_time ='{3}';
end;
'''.format(rpt_id, targetid, subuid, snapid)
            pg.execute(sqlcff)

        if controfilenote:
            # print("SCREEN_BEGIN问题与发现:\\n" + controfilenote+"SCREEN_END")
            controfilenote = """问题与发现：
""" + controfilenote
            ismf = '''
begin;
delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module='basic_controlfile';

insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'basic_controlfile' rpt_finding_module,
0 rpt_finding_type,'' rpt_sub_id,'' iname,
'控制文件' rpt_finding_label,
'信息' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level;
end;
'''.format(rpt_id, targetid, controfilenote)
            pg.execute(ismf)

    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

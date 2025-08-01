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
    # print(sql)
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


def getcomponentinfo(pg, targetid, begin_time, end_time):
    ana = ""
    head = ['序号', '组件', '版本', '状态']
    des = "数据库组件及状态"
    dbid = getdbid(pg, targetid)
    maxdbsnapid = getmaxsnap(pg, dbid, begin_time, end_time)
    sqlcompinfo = '''select row_number()over() as seq,t.* from (select col1 as component,col2 as version,col3 as status from p_oracle_cib 
where index_id='2201009'  and target_id='%s' and record_time='%s' and seq_id<>0) t ''' % (dbid, maxdbsnapid)
    # print(sqlcompinfo)
    cursor = getValue(pg, sqlcompinfo)
    results = cursor.fetchall()
    for row in results:
        if row[3] != 'VALID':
            ana += "%s组件存在问题，请检查组件。" % row[1]

    sqlResult = CommUtil.createTable(head, results, des)
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
        componentresult, componentnote = getcomponentinfo(pg, targetid, begintime, endtime)
        if componentresult:
            ##print("msg=" + componentresult)
            sqlct = '''
begin;
delete from rpt_oracle_cib where rpt_id='{0}' and target_id='{1}' and seq_id=3;
insert into rpt_oracle_cib(rpt_id,target_id,index_id,seq_id,col1,col2,col3,col4)
select '{0}' rptid,'{1}' target_id,seq_id index_id,3 seqid,
       case when seq_id=0 then '序号' else seq_id::varchar end c1,col1,col2,col3
  from p_oracle_cib 
 where index_id='2201009' and target_id='{2}' 
   and record_time='{3}';
end;
'''.format(rpt_id, targetid, subuid, snapid)
            pg.execute(sqlct)

        if componentnote:
            # print("SCREEN_BEGIN问题与发现:\\n" + componentnote + "SCREEN_END")
            componentnote = """问题与发现：
""" + componentnote
            ismf = '''
begin;
delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module='basic_dbcomponents';

insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'basic_dbcomponents' rpt_finding_module,
0 rpt_finding_type,'' rpt_sub_id,'' iname,
'数据库组件及状态' rpt_finding_label,
'信息' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level;
end;
'''.format(rpt_id, targetid, componentnote)
            pg.execute(ismf)

    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

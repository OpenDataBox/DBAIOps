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


def getdbid(pg, targetid):
    dbid = ""
    sql = "select subuid from mgt_system where uid='{0}'".format(targetid)
    sqlcursor = getValue(pg, sql)
    sqlresult = sqlcursor.fetchall()
    for row in sqlresult:
        dbid = row[0]
    return dbid


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


def getdbinfo(pg, targetid, begin_time, end_time):
    head = []
    des = ""
    dbid = getdbid(pg, targetid)
    maxdbsnapid = getmaxsnap(pg, dbid, begin_time, end_time)
    maxinstsnapid = getmaxsnap(pg, targetid, begin_time, end_time)
    sqldbinfo = '''
select cib_name,cib_value from (select cib_name,case when cib_value=null then ' '
when cib_value='' then ' ' else cib_value end cib_value from p_oracle_cib where index_id='2201000' and 
cib_name in ('db_name','database_role','dbid','version','psu','nls_characterset','log_mode','cdb') and 
target_id='{0}' and record_time='{1}'
union			  
 select cib_name,case when cib_value=null then ' '
when cib_value='' then ' ' else cib_value end cib_value from p_oracle_cib where target_id='{0}' and cib_name in (
 'db_block_size') and index_id='2201010' and record_time='{1}'
union
select 'total_datafile_size' as cib_name,trim(sum(case when col4 is null then '0'
when col4='' then '0' else col4 end::numeric)::varchar) as cib_value  from p_oracle_cib where 
index_id='2201004' and target_id='{2}' and record_time='{3}' and seq_id<>0	
union
select 'tablespace_count' as cib_name,trim(count(distinct col1)::varchar) as cib_value from p_oracle_cib where 
index_id='2201006' and target_id='{2}' and record_time='{3}' and seq_id<>0													 
union
select 'datafiles_count' as cib_name,trim(count(distinct col1)::varchar) as cib_value from p_oracle_cib where 
index_id='2201004' and target_id='{2}' and record_time='{3}' and seq_id<>0													 
union
select 'tempfiles_count' as cib_name,trim(count(distinct col1)::varchar ) as cib_value from p_oracle_cib where 
index_id='2201005' and target_id='{2}' and record_time='{3}' and seq_id<>0
union
select 'controlfiles_count' as cib_name,trim(count(distinct col1)::varchar) as cib_value from p_oracle_cib where 
index_id='2201007' and target_id='{2}' and record_time='{3}' and seq_id<>0
union
select 'redolog_size' as cib_name, case when col5 is null then '0'
when col5='' then '0' else col5 end cib_value from p_oracle_cib where 
index_id='2201003' and target_id='{2}' and record_time='{3}' and seq_id=1
union
select 'redologgroup_count' as cib_name, trim(count(col2)::varchar) as cib_value from p_oracle_cib where 
index_id='2201003' and target_id='{2}' and record_time='{3}' and seq_id<>0													 
union
select 'pdb count' as cib_name,trim(count(distinct col2)::varchar) cib_value from p_oracle_cib where 
index_id='2201002' and target_id='{2}' and record_time='{3}' and seq_id<>0 and col2 not in ('CDB$ROOT','PDB$SEED')
union
select 'redologmembers_count' as cib_name, case when col4 is null then '0' when col4='' then '0' else col4 end as cib_value from p_oracle_cib where 
index_id='2201003' and target_id='{2}' and record_time='{3}' and seq_id=1) as foo order by 
case when cib_name='db_name' then 1 when cib_name='database_role' then 2 when cib_name='dbid' then 3 
 when cib_name='version' then 4 when cib_name='psu' then 5 when cib_name='nls_characterset' then 6 when cib_name='log_mode' then 7 
 when cib_name='db_block_size' then 8 when cib_name='total_datafile_size' then 9 when cib_name='tablespace_count' then 10 
 when cib_name='datafiles_count' then 11 when cib_name='tempfiles_count' then 12 when cib_name='controlfiles_count' then 13 
 when cib_name='redolog_size' then 14 when cib_name='redologgroup_count' then 15 when cib_name='redologmembers_count' then 16 
 when cib_name='cdb' then 17 when cib_name='pdb count' then 18 end'''.format(targetid, maxinstsnapid, dbid, maxdbsnapid)
    # print(sqldbinfo)
    sqldbinfocursor = getValue(pg, sqldbinfo)
    sqldbinforesults = sqldbinfocursor.fetchall()
    for resulttolist in sqldbinforesults:
        sqldbinforesults[sqldbinforesults.index(resulttolist)] = list(resulttolist)

    for row in sqldbinforesults:
        if row[0] == 'db_name':
            row[0] = '数据库名称'
        if row[0] == 'database_role':
            row[0] = '数据库角色'
        if row[0] == 'dbid':
            row[0] = 'DBID'
        if row[0] == 'version':
            row[0] = 'RDBMS版本'
        if row[0] == 'psu':
            row[0] = 'PSU信息'
        if row[0] == 'nls_characterset':
            row[0] = '字符集'
        if row[0] == 'log_mode':
            row[0] = '归档模式'
        if row[0] == 'db_block_size':
            row[0] = 'DB_BLOCK大小'
        if row[0] == 'total_datafile_size':
            row[0] = '所有数据文件占用磁盘空间(MB)'
        if row[0] == 'tablespace_count':
            row[0] = '表空间个数'
        if row[0] == 'datafiles_count':
            row[0] = '数据文件个数'
        if row[0] == 'tempfiles_count':
            row[0] = '临时文件个数'
        if row[0] == 'controlfiles_count':
            row[0] = '控制文件个数'
        if row[0] == 'redolog_size':
            row[0] = '日志文件大小(MB)'
        if row[0] == 'redologgroup_count':
            row[0] = '日志组数目'
        if row[0] == 'redologmembers_count':
            row[0] = '每组日志文件成员数量'
        if row[0] == 'cdb':
            row[0] = 'CDB'
            if row[1] == ' ':
                row[1] = 'NO'
        if row[0] == 'pdb count':
            row[0] = 'PDB个数'

    sqlresult = CommUtil.createTable(head, sqldbinforesults, des)

    sql = ""
    cnt = 1
    for res in sqldbinforesults:
        sql += "select '" + str(res[0]) + "' c1,'" + str(res[1]) + "' c2," + str(cnt) + " c3 union all "
        cnt += 1
    sql = sql[0:-10]
    p1 = sql

    return sqlresult, p1


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

        dbinforesult, sqli = getdbinfo(pg, targetid, begintime, endtime)
        if dbinforesult:
            # print("msg=" + dbinforesult)
            sqlf = """
begin;
delete from rpt_oracle_cib where rpt_id='{0}' and target_id='{1}' and seq_id=2;
insert into rpt_oracle_cib(rpt_id,target_id,cib_name,cib_value,index_id,seq_id)
select '{0}' rptid,'{1}' target_id,res.c1,res.c2,res.c3,2 seqid
from ({2}) res;
end;""".format(rpt_id, targetid, sqli)
            pg.execute(sqlf)

    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

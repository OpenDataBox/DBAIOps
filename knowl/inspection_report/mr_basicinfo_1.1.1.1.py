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
        print(sql)
        print("msg=WORD_BEGIN" + result.msg + "WORD_END")
        sys.exit()
    return result.msg


def getinstinfo(pg, targetid, begin_time, end_time):
    head = []
    des = ""
    sgainfo = ''
    pgainfo = ''
    sqlinstinfo = f'''select cib_name,cib_value from (
select  cib_name,case when cib_value is null then ' '
when cib_value='' then ' ' else cib_value end cib_value from p_oracle_cib where  target_id='{targetid}' and cib_name in 
('db_name','version','psu','platform_name','log_mode') and index_id='2201000'
 union 
 select cib_name,case when cib_value is null then ' '
when cib_value='' then ' ' else cib_value end cib_value from p_oracle_cib where target_id='{targetid}' and cib_name in (
 'cluster_database','memory_target','sga_target','pga_aggregate_target') and index_id='2201010'
 union 
 select cib_name,case when cib_value is null then ' '
when cib_value='' then ' ' else cib_value end cib_value from p_oracle_cib where target_id='{targetid}' and cib_name 
 in ('NUM_CPUS','PHYSICAL_MEMORY_BYTES') and index_id='2201012'
 union
select 'archive_dest' as cib_name,case when col2 is null then ' '
when col2='' then ' ' else col2 end cib_value  from p_oracle_cib where index_id='2201013' and target_id='{targetid}'
and seq_id=1
union
select 'boot_ip' as cib_name,case when ip is null then ' '
when ip='' then ' ' else ip end cib_value  from mgt_system where uid='{targetid}'
union 
 select cib_name,case when cib_value is null then ' '
when cib_value='' then ' ' else cib_value end cib_value  from p_oracle_cib where  target_id='{targetid}' and cib_name in 
('instance_name','host_name') and index_id='2201001') as foo
 order by case when cib_name='instance_name' then 1 when cib_name='db_name' then 2 when cib_name='cluster_database' then 3 
 when cib_name='version' then 4 when cib_name='psu' then 5 when cib_name='host_name' then 6 when cib_name='platform_name' then 7
 when cib_name='boot_ip' then 8 when cib_name='NUM_CPUS' then 9 when cib_name='PHYSICAL_MEMORY_BYTES' then 10 
 when cib_name='memory_target' then 11 when cib_name='sga_target' then 12 when cib_name='pga_aggregate_target' then 13 
 when cib_name='log_mode' then 14 when cib_name='archive_dest' then 15 end'''
    sqlinstinfocursor = getValue(pg, sqlinstinfo)
    sqlinstinforesults = sqlinstinfocursor.fetchall()

    for resulttolist in sqlinstinforesults:
        sqlinstinforesults[sqlinstinforesults.index(resulttolist)] = list(resulttolist)

    for row in sqlinstinforesults:
        if row[0] == 'sga_target':
            row[1] = int(row[1]) / 1024 / 1024
            sgainfo = row[1]

        if row[0] == 'pga_aggregate_target':
            row[1] = int(row[1]) / 1024 / 1024
            pgainfo = row[1]

        if row[0] == 'memory_target':
            row[1] = int(row[1]) / 1024 / 1024

    for row in sqlinstinforesults:
        if row[0] == 'memory_target' and str(row[1]) == '0.0':
            row[1] = sgainfo + pgainfo
        if row[0] == 'instance_name':
            row[0] = '数据库实例'
        if row[0] == 'db_name':
            row[0] = '数据库名称'
        if row[0] == 'cluster_database':
            row[0] = 'RAC'
        if row[0] == 'version':
            row[0] = 'RDBMS版本'
        if row[0] == 'psu':
            row[0] = 'PSU信息'
        if row[0] == 'host_name':
            row[0] = '主机名'
        if row[0] == 'platform_name':
            row[0] = '操作系统'
        if row[0] == 'boot_ip':
            row[0] = '物理IP'
        if row[0] == 'NUM_CPUS':
            row[0] = 'CPU数量'
        if row[0] == 'PHYSICAL_MEMORY_BYTES':
            row[0] = '物理内存'
        if row[0] == 'memory_target':
            row[0] = '数据库内存(mb)'
        if row[0] == 'sga_target':
            row[0] = 'SGA(mb)'
        if row[0] == 'pga_aggregate_target':
            row[0] = 'PGA(mb)'
        if row[0] == 'log_mode':
            row[0] = '归档模式'
        if row[0] == 'archive_dest':
            row[0] = '归档目录'

    sqlresult = CommUtil.createTable(head, sqlinstinforesults, des)

    sql = ""
    cnt = 1
    for res in sqlinstinforesults:
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
    job_id = dbInfo['jobId']
    db_id = dbInfo['dbId']
    pg = PGUtil.Postgre(dbip, username, password, pgport, dbname)

    try:
        instinforesult, sqli = getinstinfo(pg, targetid, begintime, endtime)
        if instinforesult:
            sqlf = """
begin;
delete from rpt_oracle_cib where rpt_id='{0}' and target_id='{1}' and seq_id=1;
insert into rpt_oracle_cib(rpt_id,target_id,cib_name,cib_value,index_id,seq_id)
select '{0}' rptid,'{1}' target_id,res.c1,res.c2,res.c3,1 seqid
from ({2}) res;
end;""".format(rpt_id, targetid, sqli)
            pg.execute(sqlf)

    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

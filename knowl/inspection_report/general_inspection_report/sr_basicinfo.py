#!/usr/bin/env python3
import sys
sys.path.append('/usr/software/knowl')
import PGUtil
import CommUtil
import io
import DBUtil
import DBUtil
import psycopg2
from datetime import datetime
from JavaRsa import encrypt

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def getmaxsnap(pg, targetid, begin_time, end_time):
    maxsnapid = ""
    begin_date = datetime.strptime(begin_time, '%Y-%m-%d')
    end_date = datetime.strptime(end_time, '%Y-%m-%d')
    print(begin_date)
    print(end_date)
    sql = '''select max(snap_id::numeric ) from p_oracle_cib_his where target_id='{0}' and (
     (record_time > to_date('{1}','yyyy-mm-dd hh24:mi:ss')
    and record_time < to_date('{2}','yyyy-mm-dd hh24:mi:ss')) 
    or to_char(record_time,'yyyy-mm-dd') <= to_char(to_date('{2}' ,'yyyy-mm-dd') ,'yyyy-mm-dd'))
'''.format(targetid, begin_time, end_time)
    sqlcursor = DBUtil.getValue(pg, sql)
    sqlrersult = sqlcursor.fetchall()

    if sqlrersult:
        for row in sqlrersult:
            if not row[0] is None:
                maxsnapid = row[0]
            else:
                maxsnapid = -1
    else:
        maxsnapid = -1

    return maxsnapid


def getbasicinfo(pg, targetid, begin_time, end_time):
    head = []
    des = ""
    sgainfo = ''
    pgainfo = ''
    maxsnapid = getmaxsnap(pg, targetid, begin_time, end_time)
    sqlinstinfo = '''select cib_name,cib_value from (
select  cib_name,case when cib_value is null then ' '
when cib_value='' then ' ' else cib_value end cib_value from p_oracle_cib where  target_id='{0}' and cib_name in 
('db_name','version','psu','platform_name','log_mode') and index_id='2201000' and
 snap_id='{1}'
 union 
 select cib_name,case when cib_value is null then ' '
when cib_value='' then ' ' else cib_value end cib_value from p_oracle_cib where target_id='{0}' and cib_name in (
 'cluster_database','memory_target','sga_target','pga_aggregate_target') and index_id='2201010'
 and snap_id='{1}'
 union 
 select cib_name,case when cib_value is null then ' '
when cib_value='' then ' ' else cib_value end cib_value from p_oracle_cib where target_id='{0}' and cib_name 
 in ('NUM_CPUS','PHYSICAL_MEMORY_BYTES') and index_id='2201012' and snap_id = '{1}'
 union
select 'archive_dest' as cib_name,case when col2 is null then ' '
when col2='' then ' ' else col2 end cib_value  from p_oracle_cib where index_id='2201013' and target_id='{0}'
and seq_id=1 and snap_id='{1}'
union
select 'boot_ip' as cib_name,case when ip is null then ' '
when ip='' then ' ' else ip end cib_value  from mgt_system where uid='{0}'
union 
 select cib_name,case when cib_value is null then ' '
when cib_value='' then ' ' else cib_value end cib_value  from p_oracle_cib where  target_id='{0}' and cib_name in 
('instance_name','host_name') and index_id='2201001' and
 snap_id='{1}') as foo
 order by case when cib_name='instance_name' then 1 when cib_name='db_name' then 2 when cib_name='cluster_database' then 3 
 when cib_name='version' then 4 when cib_name='psu' then 5 when cib_name='host_name' then 6 when cib_name='platform_name' then 7
 when cib_name='boot_ip' then 8 when cib_name='NUM_CPUS' then 9 when cib_name='PHYSICAL_MEMORY_BYTES' then 10 
 when cib_name='memory_target' then 11 when cib_name='sga_target' then 12 when cib_name='pga_aggregate_target' then 13 
 when cib_name='log_mode' then 14 when cib_name='archive_dest' then 15 end'''.format(targetid, maxsnapid)
    sqlinstinfocursor = DBUtil.getValue(pg, sqlinstinfo)
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

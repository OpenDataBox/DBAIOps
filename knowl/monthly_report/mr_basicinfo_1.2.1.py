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


def getsgainfo(pg, targetid, begin_time, end_time):
    head = ["参数", "数值", "建议/说明"]
    des = "主要缓冲区参数配置"
    maxsnapid = getmaxsnap(pg, targetid, begin_time, end_time)
    # dbid = getdbid(pg,targetid)
    sqlgetsgainfo = '''select cib_name,round(cib_value::numeric/1024::numeric/1024::numeric,2) as siz_mb,' ' as note from p_oracle_cib where  cib_name in 
    ('memory_target','sga_target','db_cache_size','__db_cache_size','db_keep_cache_size','shared_pool_size','__shared_pool_size') 
    and  target_id ='%s' and record_time='%s' order by case when cib_name='memory_target' then 1 when cib_name='sga_target' then 2 else 1000 end''' % (
    targetid, maxsnapid)
    sqlgetsgainfocursor = getValue(pg, sqlgetsgainfo)
    sqlgetsgainforesults = sqlgetsgainfocursor.fetchall()
    for resulttolist in sqlgetsgainforesults:
        sqlgetsgainforesults[sqlgetsgainforesults.index(resulttolist)] = list(resulttolist)
    for result in sqlgetsgainforesults:
        if result[0] == 'memory_target' and str(result[1]) == '0.00':
            result[2] = "MEMORY_TARGET未启用"
        if result[0] == 'sga_target' and str(result[1]) == '0.00':
            result[2] = "SGA_TARGET未启用"
        if result[0] == 'db_cache_size' and str(result[1]) == '0.00':
            result[2] = "建议设置一个DB_CACHE_SIZE的初始值，数值参考__db_cache_size的值"
        if result[0] == 'db_keep_cache_size' and str(result[1]) == '0.00':
            result[2] = "KEEP池未启用"
        if result[0] == 'shared_pool_size' and str(result[1]) == '0.00':
            result[2] = "未设置共享池的初始值，建议设置共享池的初始值为__shared_pool_size"
        if result[0] == '__db_cache_size':
            result[2] = "当前DB_CACHE的大小"
        if result[0] == '__shared_pool_size':
            result[2] = "当前SHARED_POOL的大小"
    sqlresult = CommUtil.createTable(head, sqlgetsgainforesults, des)
    sql = ""
    for res in sqlgetsgainforesults:
        sql += "select '" + str(res[0]) + "' c1,'" + str(res[1]) + "' c2,'" + str(res[2]) + "' c3 union all "
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
        sgainforesult, sqli = getsgainfo(pg, targetid, begintime, endtime)
        if sgainforesult:
            # print("msg=" + sgainforesult)
            sqlf = """begin;
delete from rpt_sga_parameter where rpt_id='{0}' and target_id='{1}';
insert into rpt_sga_parameter(rpt_id,target_id,rpt_seq,rpt_paramter_name,rpt_value,rpt_notes)
select '{0}' rptid,'{1}' target_id,row_number() over(order by res.c1) cnt,res.c1,res.c2,res.c3
from ({2}) res;
end;""".format(rpt_id, targetid, sqli)
            pg.execute(sqlf)

    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

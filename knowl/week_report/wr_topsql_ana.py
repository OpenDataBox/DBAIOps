#!/usr/bin/env python3
# -*- encoding:utf-8 -*-
import sys

sys.path.append('/usr/software/knowl')
import PGUtil
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


def gettopsqlwithuserid(pg, begin_time, end_time, rptwk_id, userid):
    sql = '''
begin;
delete from rptwk_top_sql where rptwk_id='{2}';
insert into rptwk_top_sql(rptwk_id,mgt_name,rptwk_topsql_count,rptwk_topsql_count_l,rptwk_topsql_count_diff)
select '{2}' rwtwk_id,m.name,
COALESCE ( cw_sql_cnt, 0 ) cw_cnt,
COALESCE ( lw_sql_cnt, 0 ) lw_cnt,
CASe WHEN lw_sql_cnt IS NULL THEN
'100%' ELSE round(( COALESCE ( cw_sql_cnt, 0 ) :: NUMERIC - COALESCE ( lw_sql_cnt, 0 ) :: NUMERIC ) / lw_sql_cnt * 100, 2 ) || '%' END change from 
(select target_id,count(distinct sql_id) cw_sql_cnt from sqlcheck w,user_obj_association u user_obj_association u where begin_time  between '{0}' and '{1}'
and w.target_id=u.target_id  and u.use_flag=true and u.user_id={3} group by target_id) cw full join 
(select target_id,count(distinct sql_id) lw_sql_cnt from sqlcheck w,user_obj_association u where begin_time + interval '1 week' between '{0}' and '{1}'
and w.target_id=u.target_id  and u.use_flag=true and u.user_id={3} group by target_id) lw on cw.target_id=lw.target_id
join mgt_system m on cw.target_id= m.uid;
end;
'''.format(begin_time, end_time, rptwk_id, userid)
    # print(sql)
    pg.execute(sql)


def gettopsqladmin(pg, begin_time, end_time, rptwk_id):
    sql = '''
begin;
delete from rptwk_top_sql where rptwk_id='{2}';
insert into rptwk_top_sql(rptwk_id,mgt_name,rptwk_topsql_count,rptwk_topsql_count_l,rptwk_topsql_count_diff)
select '{2}' rwtwk_id,m.name,
COALESCE ( cw_sql_cnt, 0 ) cw_cnt,
COALESCE ( lw_sql_cnt, 0 ) lw_cnt,
CASe WHEN lw_sql_cnt IS NULL THEN
'100%' ELSE round(( COALESCE ( cw_sql_cnt, 0 ) :: NUMERIC - COALESCE ( lw_sql_cnt, 0 ) :: NUMERIC ) / lw_sql_cnt * 100, 2 ) || '%' END change from
(select target_id,count(distinct sql_id) cw_sql_cnt from sqlcheck w where begin_time  between '{0}' and '{1}'
 group by target_id) cw full join
(select target_id,count(distinct sql_id) lw_sql_cnt from sqlcheck w where begin_time + interval '1 week' between '{0}' and '{1}'
group by target_id) lw on cw.target_id=lw.target_id
join mgt_system m on cw.target_id= m.uid;
end;
'''.format(begin_time, end_time, rptwk_id)
    # print(sql)
    pg.execute(sql)


if __name__ == '__main__':
    dbInfo = eval(sys.argv[1])
    ##pg info
    dbip = dbInfo['pg_ip']
    dbname = dbInfo['pg_dbname']
    username = dbInfo['pg_usr']
    password = dbInfo['pg_pwd']
    pgport = dbInfo['pg_port']
    ##ora info
    # usr = dbInfo['ora_usr']
    # pwd = dbInfo['ora_pwd']
    # host = dbInfo['ora_ip']
    # port = dbInfo['ora_port']
    # database = dbInfo['ora_sid']

    targetid = dbInfo['targetId']
    begintime = dbInfo['start_time']
    endtime = dbInfo['end_time']

    userid = dbInfo['userId']
    rptwk_id = dbInfo['rptwk_id']
    job_id = dbInfo['jobId']
    db_id = dbInfo['dbId']
    pg = PGUtil.Postgre(dbip, username, password, pgport, dbname)

    try:
        if userid == "-1":
            gettopsqladmin(pg, begintime, endtime, rptwk_id)
        else:
            gettopsqlwithuserid(pg, begintime, endtime, rptwk_id, userid)
    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

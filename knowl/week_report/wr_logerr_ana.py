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


def getlogerrwithuseid(pg, begin_time, end_time, rptwk_id, userid):
    sql = '''
begin;
delete from rptwk_logerror_detail where rptwk_id='{2}';
insert into rptwk_logerror_detail(rptwk_id,data_type,data_name,rptwk_logerror_count,rptwk_logerror_count_l,rptwk_logerror_count_diff,rptwk_logerror_rank,rptwk_logerror_rank_l)
select '{2}' rptwk_id,log_type,item,cwcnt,lwcnt,change,
case when log_type = 0 then row_number() over (partition by log_type order by cwcnt desc)  
else row_number() over (partition by log_type order by cwcnt desc)  end cw_rank,
case when log_type = 0 then row_number() over (partition by log_type order by lwcnt desc)  
else row_number() over (partition by log_type order by lwcnt desc)  end lw_rank
from 
(select case when cw.log_type is null then lw.log_type else cw.log_type end log_type,
case when cw.item is null then lw.item else cw.item end item,
coalesce(cwcnt,0) cwcnt, coalesce(lwcnt,0) lwcnt,
case when lwcnt is null then '100%' else round((coalesce(cwcnt,0)::numeric-coalesce(lwcnt,0)::numeric)/lwcnt*100,2)||'%' end change
from
(select 0 log_type,log_code item,count(*) cwcnt from log_detail l,user_obj_association u where begin_time between '{0}' and '{1}'
 and u.use_flag=true and l.target_id=u.target_id and u.user_id='{3}'
group by log_code
union all
select 1,name,count(*) from log_detail l,mgt_system s,user_obj_association u where l.target_id=s.uid and 
begin_time between '{0}' and '{1}' and u.use_flag=true and l.target_id=u.target_id and u.user_id='{3}' group by name) cw full join
(select 0 log_type,log_code item,count(*) lwcnt from log_detail l,user_obj_association u where 
 begin_time + interval '1 week' between '{0}' and '{1}' and u.use_flag=true and l.target_id=u.target_id and u.user_id='{3}'
group by log_code
union all
select 1,name,count(*) from log_detail l,mgt_system s,user_obj_association u  where l.target_id=s.uid and 
begin_time + interval '1 week' between '{0}' and '{1}' and u.use_flag=true and l.target_id=u.target_id and u.user_id='{3}' group by name) lw
on cw.log_type=lw.log_type and cw.item=lw.item) res;
end;
'''.format(begin_time, end_time, rptwk_id, userid)
    # print(sql)
    pg.execute(sql)


def getlogerradmin(pg, begin_time, end_time, rptwk_id):
    sql = '''
begin;
delete from rptwk_logerror_detail where rptwk_id='{2}';
insert into rptwk_logerror_detail(rptwk_id,data_type,data_name,rptwk_logerror_count,rptwk_logerror_count_l,rptwk_logerror_count_diff,rptwk_logerror_rank,rptwk_logerror_rank_l)
select '{2}' rptwk_id,log_type,item,cwcnt,lwcnt,change,
case when log_type = 0 then row_number() over (partition by log_type order by cwcnt desc)
else row_number() over (partition by log_type order by cwcnt desc)  end cw_rank,
case when log_type = 0 then row_number() over (partition by log_type order by lwcnt desc)
else row_number() over (partition by log_type order by lwcnt desc)  end lw_rank
from
(select case when cw.log_type is null then lw.log_type else cw.log_type end log_type,
case when cw.item is null then lw.item else cw.item end item,
coalesce(cwcnt,0) cwcnt, coalesce(lwcnt,0) lwcnt,
case when lwcnt is null then '100%' else round((coalesce(cwcnt,0)-coalesce(lwcnt,0))/lwcnt*100,2)||'%' end change
from
(select 0 log_type,log_code item,count(*) cwcnt from log_detail where begin_time between '{0}' and '{1}'
group by log_code
union all
select 1,name,count(*) from log_detail l,mgt_system s where l.target_id=s.uid and
begin_time between '{0}' and '{1}' group by name) cw full join
(select 0 log_type,log_code item,count(*) lwcnt from log_detail where
 begin_time + interval '1 week' between '{0}' and '{1}'
group by log_code
union all
select 1,name,count(*) from log_detail l,mgt_system s where l.target_id=s.uid and
begin_time + interval '1 week' between '{0}' and '{1}' group by name) lw
on cw.log_type=lw.log_type and cw.item=lw.item) res;
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
    userid = dbInfo['userId']
    ##ora info
    # usr = dbInfo['ora_usr']
    # pwd = dbInfo['ora_pwd']
    # host = dbInfo['ora_ip']
    # port = dbInfo['ora_port']
    # database = dbInfo['ora_sid']

    targetid = dbInfo['targetId']
    begintime = dbInfo['start_time']
    endtime = dbInfo['end_time']

    rptwk_id = dbInfo['rptwk_id']
    job_id = dbInfo['jobId']
    db_id = dbInfo['dbId']
    pg = PGUtil.Postgre(dbip, username, password, pgport, dbname)

    try:
        if userid == "-1":
            getlogerradmin(pg, begintime, endtime, rptwk_id)
        else:
            getlogerrwithuseid(pg, begintime, endtime, rptwk_id, userid)
    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

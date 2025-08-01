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


def getscorewithuserid(pg, begin_time, end_time, rptwk_id, userid):
    sql = '''
begin;
delete from rptwk_score_avg where rptwk_id='{2}';
insert into rptwk_score_avg(rptwk_id,mgt_name,
rptwk_health_avg,rptwk_health_avg_l,rptwk_health_avg_diff,
rptwk_perf_avg,rptwk_perf_avg_l,rptwk_perf_avg_diff,
rptwk_load_avg,rptwk_load_avg_l,rptwk_load_avg_diff,
target_id,rptwk_health_rank,rptwk_perf_rank,rptwk_load_rank,
rptwk_health_rankchange,rptwk_perf_rankchange,rptwk_load_rankchange,
rptwk_health_rank_l,rptwk_perf_rank_l,rptwk_load_rank_l)
select '{2}',m.name,health_avg_c,health_avg_l,health_diff,
perf_avg_c,perf_avg_l,perf_diff,load_avg_c,load_avg_l,load_diff,
target_id,health_rank_c,perf_rank_c,load_rank_c,
health_rank_c-health_rank_l,perf_rank_c-perf_rank_l,load_rank_c-load_rank_l,
health_rank_l,perf_rank_l,load_rank_l
 from
(select cw.target_id,coalesce(cw.health_avg_c,0) health_avg_c,coalesce(row_number()over( order by cw.health_avg_c desc nulls last),0) health_rank_c ,
coalesce(lw.health_avg_l,0) health_avg_l,coalesce(row_number()over( order by lw.health_avg_l desc nulls last),0) health_rank_l,
coalesce(cw.health_avg_c,0)-coalesce(lw.health_avg_l,0) health_diff,
coalesce(cw.perf_avg_c,0) perf_avg_c,coalesce(row_number()over( order by cw.perf_avg_c desc nulls last),0) perf_rank_c,
coalesce(lw.perf_avg_l,0) perf_avg_l,coalesce(row_number()over( order by lw.perf_avg_l desc nulls last),0) perf_rank_l,
coalesce(cw.perf_avg_c,0)-coalesce(lw.perf_avg_l,0) perf_diff,
coalesce(cw.load_avg_c,0) load_avg_c,coalesce(row_number()over( order by cw.load_avg_c desc nulls last),0) load_rank_c,
coalesce(lw.load_avg_l,0) load_avg_l,coalesce(row_number()over( order by lw.load_avg_l desc nulls last),0) load_rank_l,
coalesce(cw.load_avg_c,0)-coalesce(lw.load_avg_l,0) load_diff from
(select h.target_id,health_avg as health_avg_c,perf_avg as perf_avg_c,load_avg as load_avg_c from 
(select target_id,round(avg(health_score)::numeric,2) health_avg from h_health_check a,h_health_check_deduct b where record_time 
 between '{0}' and '{1}' and a.use_flag=true and a.health_check_id=b.health_check_id  
 group by target_id order by target_id) h left join
(select target_id,round(avg(b.perf_score)::numeric,2) perf_avg,round(avg(b.load_score)::numeric,2) load_avg from p_perf_eva a,p_perf_eva_his b where a.eva_id=b.eva_id and b.record_time
between '{0}' and '{1}' and a.use_flag=true 
group by target_id order by target_id) p
on h.target_id=p.target_id join user_obj_association u on h.target_id=u.target_id where 
u.use_flag=true and u.user_id={3}) cw left join
(select h.target_id,health_avg as health_avg_l,perf_avg as perf_avg_l,load_avg as load_avg_l from 
(select target_id,round(avg(health_score)::numeric,2) health_avg from h_health_check a,h_health_check_deduct b where 
 record_time + interval '1 week' between '{0}' and '{1}' and a.use_flag=true and a.health_check_id=b.health_check_id 
 group by target_id order by target_id) h left join
(select target_id,round(avg(b.perf_score)::numeric,2) perf_avg,round(avg(b.load_score)::numeric,2) load_avg from p_perf_eva a,p_perf_eva_his b where a.eva_id=b.eva_id and 
b.record_time + interval '1 week' between '{0}' and '{1}' and a.use_flag=true 
group by target_id order by target_id) p
on h.target_id=p.target_id join user_obj_association u on h.target_id=u.target_id where 
u.use_flag=true and u.user_id={3}) lw on cw.target_id=lw.target_id) score,mgt_system m where
score.target_id=m.uid;
end;
'''.format(begin_time, end_time, rptwk_id, userid)
    # print(sql)
    pg.execute(sql)

    sql2 = '''
begin;
insert into rptwk_score_avg(rptwk_id,mgt_name,rptwk_health_avg,rptwk_health_avg_l,rptwk_perf_avg,rptwk_perf_avg_l,rptwk_load_avg,rptwk_load_avg_l)
select rptwk_id,-1 mgt_name,round(avg(coalesce(rptwk_health_avg::numeric,0)),2),
round(avg(coalesce(rptwk_health_avg_l::numeric,0)),2),
round(avg(coalesce(rptwk_perf_avg::numeric,0)),2),
round(avg(coalesce(rptwk_perf_avg_l::numeric,0)),2),
round(avg(coalesce(rptwk_load_avg::numeric,0)),2),
round(avg(coalesce(rptwk_load_avg_l::numeric,0)),2)
from rptwk_score_avg  where rptwk_id='{0}' group by rptwk_id;
end;
'''.format(rptwk_id)
    # print(sql2)
    pg.execute(sql2)


def getscoreadmin(pg, begin_time, end_time, rptwk_id):
    sql = '''
begin;
delete from rptwk_score_avg where rptwk_id='{2}';
insert into rptwk_score_avg(rptwk_id,mgt_name,
rptwk_health_avg,rptwk_health_avg_l,rptwk_health_avg_diff,
rptwk_perf_avg,rptwk_perf_avg_l,rptwk_perf_avg_diff,
rptwk_load_avg,rptwk_load_avg_l,rptwk_load_avg_diff,
target_id,rptwk_health_rank,rptwk_perf_rank,rptwk_load_rank,
rptwk_health_rankchange,rptwk_perf_rankchange,rptwk_load_rankchange,
rptwk_health_rank_l,rptwk_perf_rank_l,rptwk_load_rank_l)
select '{2}',m.name,health_avg_c,health_avg_l,health_diff,
perf_avg_c,perf_avg_l,perf_diff,load_avg_c,load_avg_l,load_diff,
target_id,health_rank_c,perf_rank_c,load_rank_c,
health_rank_c-health_rank_l,perf_rank_c-perf_rank_l,load_rank_c-load_rank_l,
health_rank_l,perf_rank_l,load_rank_l
 from
(select cw.target_id,coalesce(cw.health_avg_c,0) health_avg_c,coalesce(row_number()over( order by cw.health_avg_c desc nulls last),0) health_rank_c ,
coalesce(lw.health_avg_l,0) health_avg_l,coalesce(row_number()over( order by lw.health_avg_l desc nulls last),0) health_rank_l,
coalesce(cw.health_avg_c,0)-coalesce(lw.health_avg_l,0) health_diff,
coalesce(cw.perf_avg_c,0) perf_avg_c,coalesce(row_number()over( order by cw.perf_avg_c desc nulls last),0) perf_rank_c,
coalesce(lw.perf_avg_l,0) perf_avg_l,coalesce(row_number()over( order by lw.perf_avg_l desc nulls last),0) perf_rank_l,
coalesce(cw.perf_avg_c,0)-coalesce(lw.perf_avg_l,0) perf_diff,
coalesce(cw.load_avg_c,0) load_avg_c,coalesce(row_number()over( order by cw.load_avg_c desc nulls last),0) load_rank_c,
coalesce(lw.load_avg_l,0) load_avg_l,coalesce(row_number()over( order by lw.load_avg_l desc nulls last),0) load_rank_l,
coalesce(cw.load_avg_c,0)-coalesce(lw.load_avg_l,0) load_diff from
(select h.target_id,health_avg as health_avg_c,perf_avg as perf_avg_c,load_avg as load_avg_c from
(select target_id,round(avg(health_score)::numeric,2) health_avg from h_health_check a,h_health_check_deduct b where record_time
 between '{0}' and '{1}' and a.use_flag=true and a.health_check_id=b.health_check_id
 group by target_id order by target_id) h left join
(select target_id,round(avg(b.perf_score)::numeric,2) perf_avg,round(avg(b.load_score)::numeric,2) load_avg from p_perf_eva a,p_perf_eva_his b where a.eva_id=b.eva_id and b.record_time
between '{0}' and '{1}' and a.use_flag=true
group by target_id order by target_id) p
on h.target_id=p.target_id) cw left join
(select h.target_id,health_avg as health_avg_l,perf_avg as perf_avg_l,load_avg as load_avg_l from
(select target_id,round(avg(health_score)::numeric,2) health_avg from h_health_check a,h_health_check_deduct b where
 record_time + interval '1 week' between '{0}' and '{1}' and a.use_flag=true and a.health_check_id=b.health_check_id
 group by target_id order by target_id) h left join
(select target_id,round(avg(b.perf_score)::numeric,2) perf_avg,round(avg(b.load_score)::numeric,2) load_avg from p_perf_eva a,p_perf_eva_his b where a.eva_id=b.eva_id and
b.record_time + interval '1 week' between '{0}' and '{1}' and a.use_flag=true
group by target_id order by target_id) p
on h.target_id=p.target_id) lw on cw.target_id=lw.target_id) score,mgt_system m where
score.target_id=m.uid;
end;
'''.format(begin_time, end_time, rptwk_id)
    # print(sql)
    pg.execute(sql)

    sql2 = '''
begin;
insert into rptwk_score_avg(rptwk_id,mgt_name,rptwk_health_avg,rptwk_health_avg_l,rptwk_perf_avg,rptwk_perf_avg_l,rptwk_load_avg,rptwk_load_avg_l)
select rptwk_id,-1 mgt_name,round(avg(coalesce(rptwk_health_avg::numeric,0)),2),
round(avg(coalesce(rptwk_health_avg_l::numeric,0)),2),
round(avg(coalesce(rptwk_perf_avg::numeric,0)),2),
round(avg(coalesce(rptwk_perf_avg_l::numeric,0)),2),
round(avg(coalesce(rptwk_load_avg::numeric,0)),2),
round(avg(coalesce(rptwk_load_avg_l::numeric,0)),2)
from rptwk_score_avg  where rptwk_id='{0}' group by rptwk_id;
end;
'''.format(rptwk_id)
    # print(sql2)
    pg.execute(sql2)


if __name__ == '__main__':
    dbInfo = eval(sys.argv[1])
    dbip = dbInfo['pg_ip']
    dbname = dbInfo['pg_dbname']
    username = dbInfo['pg_usr']
    password = dbInfo['pg_pwd']
    pgport = dbInfo['pg_port']
    userid = dbInfo['userId']
    targetid = dbInfo['targetId']
    begintime = dbInfo['start_time']
    endtime = dbInfo['end_time']

    rptwk_id = dbInfo['rptwk_id']
    job_id = dbInfo['jobId']
    db_id = dbInfo['dbId']
    pg = PGUtil.Postgre(dbip, username, password, pgport, dbname)

    try:
        if userid == "-1":
            getscoreadmin(pg, begintime, endtime, rptwk_id)
        else:
            getscorewithuserid(pg, begintime, endtime, rptwk_id, userid)
    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

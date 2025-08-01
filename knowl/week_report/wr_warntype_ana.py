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


def getwarntypewithuserid(pg, begin_time, end_time, rptwk_id, userid):
    sql = '''
begin;
delete from rptwk_warntype_sum where rptwk_id='{2}';
insert into rptwk_warntype_sum(rptwk_id,warntype,rptwk_warn_count,rptwk_warn_count_l,rptwk_warn_count_diff)
select '{2}' rptwk_id,case when cw.warn_part is null then lw.warn_part else cw.warn_part end wart_type,coalesce(cw_cnt,0) cw_cnt,coalesce(lw_cnt,0) lw_cnt,
case when lw_cnt is null then '100%' else round((coalesce(cw_cnt,0)::numeric-coalesce(lw_cnt,0)::numeric)/lw_cnt*100,2)||'%' end change from (select warn_part,coalesce(count(*),0) cw_cnt 
FROM mon_warn_log w,user_obj_association u where  warn_time between '{0}' and '{1}' and w.device_id=u.target_id  and u.use_flag=true and u.user_id={3} group by warn_part) cw full join
(select warn_part, coalesce(count(*),0) lw_cnt FROM mon_warn_log w,user_obj_association u where 
 warn_time + interval '1 week' between '{0}' and '{1}' and w.device_id=u.target_id  and u.use_flag=true and u.user_id={3}
group by warn_part ) lw on cw.warn_part=lw.warn_part;
end;
'''.format(begin_time, end_time, rptwk_id, userid)
    # print(sql)
    pg.execute(sql)


def getwarntypeadmin(pg, begin_time, end_time, rptwk_id):
    sql = '''
begin;
delete from rptwk_warntype_sum where rptwk_id='{2}';
insert into rptwk_warntype_sum(rptwk_id,warntype,rptwk_warn_count,rptwk_warn_count_l,rptwk_warn_count_diff)
select '{2}' rptwk_id,case when cw.warn_part is null then lw.warn_part else cw.warn_part end wart_type,coalesce(cw_cnt,0) cw_cnt,coalesce(lw_cnt,0) lw_cnt,case when lw_cnt is null then '100%' else round((coalesce(cw_cnt,0)::numeric-coalesce(lw_cnt,0)::numeric)/lw_cnt*100,2)||'%' end change from (select warn_part,coalesce(count(*),0) cw_cnt FROM mon_warn_log where
 warn_time between '{0}' and '{1}' group by warn_part) cw full join
(select warn_part, coalesce(count(*),0) lw_cnt FROM mon_warn_log where
 warn_time + interval '1 week' between '{0}' and '{1}'
group by warn_part ) lw on cw.warn_part=lw.warn_part;
end;
'''.format(begin_time, end_time, rptwk_id)
    # print(sql)
    pg.execute(sql)


def getsumwarntype(pg, rptwk_id):
    sql = '''
begin;
delete from rptwk_warntype_sum where rptwk_id='{0}' and warntype = '-1';
insert into rptwk_warntype_sum(rptwk_id,warntype,rptwk_warn_count,rptwk_warn_count_l,rptwk_warn_count_diff)
select '{0}','-1',cw_total,lw_total,round((cw_total::numeric-lw_total::numeric)/lw_total::numeric * 100,2)||'%' from
(select sum(rptwk_warn_count) cw_total,sum(rptwk_warn_count_l) lw_total from rptwk_warnlevel_sum where rptwk_id='{0}') as foo;
end;
'''.format(rptwk_id)
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
            getwarntypeadmin(pg, begintime, endtime, rptwk_id)
        else:
            getwarntypewithuserid(pg, begintime, endtime, rptwk_id, userid)
        getsumwarntype(pg, rptwk_id)
    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

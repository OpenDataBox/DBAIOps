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


def getwarndetailwithuserid(pg, begin_time, end_time, rptwk_id, userid):
    sql = '''
select '{2}' rptwk_id,case when cw.warntype is null then lw.warntype else cw.warntype end warntype,
case when cw.item is null then lw.item else cw.item end item,
coalesce(cwcnt,0) cwcnt,coalesce(lwcnt,0) lwcnt,case when lwcnt is null then '100%' else round((coalesce(cwcnt,0)::numeric-coalesce(lwcnt,0))::numeric/lwcnt::numeric*100,2)||'%' end change,
case when cw.warntype='实例' then row_number() over(partition by cw.warntype order by cwcnt desc) else 0 end cw_rank,
case when lw.warntype='实例' then row_number() over(partition by lw.warntype order by lwcnt desc) else 0 end lw_rank
from 
(select '基线' warntype,description item,count(*) cwcnt from mon_warn_log w,mon_index b,user_obj_association u where warn_time between '{0}' and '{1}'
and warn_part='基线' and w.index_id=b.index_id and w.device_id=u.target_id  and u.use_flag=true and u.user_id={3} group by description 
union all
select '健康评分',description,count(*) cnt from mon_warn_log w,mon_index b,user_obj_association u where warn_time between '{0}' and '{1}'
and warn_part='健康评分' and w.index_id=b.index_id and w.device_id=u.target_id  and u.use_flag=true and u.user_id={3} group by description
union all
select '运维经验',split_part(catalog,'-',3), count(*) cnt from mon_warn_log w,user_obj_association u where warn_time between '{0}' and '{1}'
and warn_part='运维经验' and w.device_id=u.target_id  and u.use_flag=true and u.user_id={3} group by split_part(catalog,'-',3)
union all
select '日检',split_part(catalog,'-',3), count(*) cnt from mon_warn_log w,user_obj_association u where warn_time between '{0}' and '{1}'
and warn_part='日检' and w.device_id=u.target_id  and u.use_flag=true and u.user_id={3} group by split_part(catalog,'-',3)
union all
select 'Oracle数据库日志',split_part(catalog,'-',2), count(*) cnt from mon_warn_log w ,user_obj_association u where warn_time between '{0}' and '{1}'
and warn_part='Oracle数据库日志' and w.device_id=u.target_id  and u.use_flag=true and u.user_id={3} group by split_part(catalog,'-',2)
union all
select 'ASM日志',split_part(catalog,'-',2), count(*) cnt from mon_warn_log w,user_obj_association u where warn_time between '{0}' and '{1}'
and warn_part='ASM日志' and w.device_id=u.target_id  and u.use_flag=true and u.user_id={3} group by split_part(catalog,'-',2)
union all
select '实例',name,count(*) from mon_warn_log w,mgt_system s,user_obj_association u where warn_time between '{0}' and '{1}'
and w.device_id=s.uid and w.device_id=u.target_id  and u.use_flag=true and u.user_id={3} group by name) cw full join
(select '基线' warntype,description item,count(*) lwcnt from mon_warn_log w,mon_index b,user_obj_association u where warn_time + interval '1 week' between '{0}' and '{1}'
and warn_part='基线' and w.index_id=b.index_id and w.device_id=u.target_id  and u.use_flag=true and u.user_id={3} group by description 
union all
select '健康评分',description,count(*) cnt from mon_warn_log w,mon_index b,user_obj_association u where warn_time + interval '1 week' between '{0}' and '{1}'
and warn_part='健康评分' and w.index_id=b.index_id and w.device_id=u.target_id  and u.use_flag=true and u.user_id={3} group by description
union all
select '运维经验',split_part(catalog,'-',3), count(*) cnt from mon_warn_log w,user_obj_association u where warn_time + interval '1 week' between '{0}' and '{1}'
and warn_part='运维经验' and w.device_id=u.target_id  and u.use_flag=true and u.user_id={3} group by split_part(catalog,'-',3)
union all
select '日检',split_part(catalog,'-',3), count(*) cnt from mon_warn_log w,user_obj_association u where warn_time + interval '1 week' between '{0}' and '{1}'
and warn_part='日检' and w.device_id=u.target_id  and u.use_flag=true and u.user_id={3} group by split_part(catalog,'-',3)
union all
select 'Oracle数据库日志',split_part(catalog,'-',2), count(*) cnt from mon_warn_log w,user_obj_association u where warn_time + interval '1 week' between '{0}' and '{1}'
and warn_part='Oracle数据库日志' and w.device_id=u.target_id  and u.use_flag=true and u.user_id={3} group by split_part(catalog,'-',2)
union all
select 'ASM日志',split_part(catalog,'-',2), count(*) cnt from mon_warn_log w,user_obj_association u where warn_time + interval '1 week' between '{0}' and '{1}'
and warn_part='ASM日志' and w.device_id=u.target_id  and u.use_flag=true and u.user_id={3} group by split_part(catalog,'-',2)
union all
select '实例',name,count(*) from mon_warn_log w,mgt_system s,user_obj_association u where warn_time + interval '1 week' between '{0}' and '{1}'
and w.device_id=s.uid and w.device_id=u.target_id  and u.use_flag=true and u.user_id={3} group by name) lw on cw.warntype=lw.warntype and cw.item=lw.item
'''.format(begin_time, end_time, rptwk_id, userid)
    # print(sql)
    sqlcursor = getValue(pg, sql)
    sqlresults = sqlcursor.fetchall()
    for resulttolist in sqlresults:
        sqlresults[sqlresults.index(resulttolist)] = list(resulttolist)
    for row in sqlresults:
        if row[1] == '实例':
            row[5] = row[6] - row[7]
    sql2 = ''
    for row in sqlresults:
        sql2 += "select '" + row[0] + "','" + row[1] + "','" + row[2] + "'," + str(row[3]) + "," + str(
            row[4]) + ",'" + str(row[5]) + "'," + str(row[6]) + "," + str(row[7]) + " union all "
    sql2 = sql2[0:-10]
    sql3 = '''
begin;
delete from rptwk_warn_detail where rptwk_id='{0}';
insert into rptwk_warn_detail(rptwk_id,warn_type,data_name,rptwk_warn_count,rptwk_warn_count_l,rptwk_warn_count_diff,rptwk_warn_count_rank,rptwk_warn_count_rank_l) select * from ({1}) res;
end;'''.format(rptwk_id, sql2)
    # print(sql3)
    pg.execute(sql3)


def getwarndetailadmin(pg, begin_time, end_time, rptwk_id):
    sql = '''
select '{2}' rptwk_id,case when cw.warntype is null then lw.warntype else cw.warntype end warntype,
case when cw.item is null then lw.item else cw.item end item,
coalesce(cwcnt,0) cwcnt,coalesce(lwcnt,0) lwcnt,case when lwcnt is null then '100%' else round((coalesce(cwcnt,0)::numeric-coalesce(lwcnt,0))::numeric/lwcnt::numeric*100,2)||'%' end change,
case when cw.warntype='实例' then row_number() over(partition by cw.warntype order by cwcnt desc) else 0 end cw_rank,
case when lw.warntype='实例' then row_number() over(partition by lw.warntype order by lwcnt desc) else 0 end lw_rank
from
(select '基线' warntype,description item,count(*) cwcnt from mon_warn_log w,mon_index b where warn_time between '{0}' and '{1}'
and warn_part='基线' and w.index_id=b.index_id group by description
union all
select '健康评分',description,count(*) cnt from mon_warn_log w,mon_index b where warn_time between '{0}' and '{1}'
and warn_part='健康评分' and w.index_id=b.index_id group by description
union all
select '运维经验',split_part(catalog,'-',3), count(*) cnt from mon_warn_log w where warn_time between '{0}' and '{1}'
and warn_part='运维经验' group by split_part(catalog,'-',3)
union all
select '日检',split_part(catalog,'-',3), count(*) cnt from mon_warn_log w where warn_time between '{0}' and '{1}'
and warn_part='日检' group by split_part(catalog,'-',3)
union all
select 'Oracle数据库日志',split_part(catalog,'-',2), count(*) cnt from mon_warn_log w where warn_time between '{0}' and '{1}'
and warn_part='Oracle数据库日志' group by split_part(catalog,'-',2)
union all
select 'ASM日志',split_part(catalog,'-',2), count(*) cnt from mon_warn_log w where warn_time between '{0}' and '{1}'
and warn_part='ASM日志' group by split_part(catalog,'-',2)
union all
select '实例',name,count(*) from mon_warn_log w,mgt_system s where warn_time between '{0}' and '{1}'
and w.device_id=s.uid group by name) cw full join
(select '基线' warntype,description item,count(*) lwcnt from mon_warn_log w,mon_index b where warn_time + interval '1 week' between '{0}' and '{1}'
and warn_part='基线' and w.index_id=b.index_id group by description
union all
select '健康评分',description,count(*) cnt from mon_warn_log w,mon_index b where warn_time + interval '1 week' between '{0}' and '{1}'
and warn_part='健康评分' and w.index_id=b.index_id group by description
union all
select '运维经验',split_part(catalog,'-',3), count(*) cnt from mon_warn_log w where warn_time + interval '1 week' between '{0}' and '{1}'
and warn_part='运维经验' group by split_part(catalog,'-',3)
union all
select '日检',split_part(catalog,'-',3), count(*) cnt from mon_warn_log w where warn_time + interval '1 week' between '{0}' and '{1}'
and warn_part='日检' group by split_part(catalog,'-',3)
union all
select 'Oracle数据库日志',split_part(catalog,'-',2), count(*) cnt from mon_warn_log w where warn_time + interval '1 week' between '{0}' and '{1}'
and warn_part='Oracle数据库日志' group by split_part(catalog,'-',2)
union all
select 'ASM日志',split_part(catalog,'-',2), count(*) cnt from mon_warn_log w where warn_time + interval '1 week' between '{0}' and '{1}'
and warn_part='ASM日志' group by split_part(catalog,'-',2)
union all
select '实例',name,count(*) from mon_warn_log w,mgt_system s where warn_time + interval '1 week' between '{0}' and '{1}'
and w.device_id=s.uid group by name) lw on cw.warntype=lw.warntype and cw.item=lw.item
'''.format(begin_time, end_time, rptwk_id)
    # print(sql)
    sqlcursor = getValue(pg, sql)
    sqlresults = sqlcursor.fetchall()
    for resulttolist in sqlresults:
        sqlresults[sqlresults.index(resulttolist)] = list(resulttolist)
    for row in sqlresults:
        if row[1] == '实例':
            row[5] = row[6] - row[7]
    sql2 = ''
    for row in sqlresults:
        sql2 += "select '" + row[0] + "','" + row[1] + "','" + row[2] + "'," + str(row[3]) + "," + str(
            row[4]) + ",'" + str(row[5]) + "'," + str(row[6]) + "," + str(row[7]) + " union all "
    sql2 = sql2[0:-10]
    sql3 = '''
begin;
delete from rptwk_warn_detail where rptwk_id='{0}';
insert into rptwk_warn_detail(rptwk_id,warn_type,data_name,rptwk_warn_count,rptwk_warn_count_l,rptwk_warn_count_diff,rptwk_warn_count_rank,rptwk_warn_count_rank_l) select * from ({1}) res;
end;'''.format(rptwk_id, sql2)
    # print(sql3)
    pg.execute(sql3)


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
            getwarndetailadmin(pg, begintime, endtime, rptwk_id)
        else:
            getwarndetailwithuserid(pg, begintime, endtime, rptwk_id, userid)
    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

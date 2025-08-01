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
        msg = result.msg
        print("msg=WORD_BEGIN" + msg + "WORD_END")
        sys.exit()
    return result.msg


def getperformanceinfo(pg, targetid, begin_time, end_time):
    head = ['性能指标', '上月平均值', '本月平均值', '变化', '说明']
    des = "性能指标信息"
    sqlperfinfo = '''
select cm.description,coalesce(lm.avgscore,0) lmavgscore,coalesce(cm.avgscore,0) cmavgscore,
round((coalesce(cm.avgscore,0)-coalesce(lm.avgscore,0))::numeric,2) as change,' ' as note from 
(select i.description,"avgScore" avgscore from r_m_indexdata r,mon_index i where r.index_id in 
(2190055,2190057,2190058,2190059,2190060,2190061,2190062,
2190064,2190065,2190040,2190041,2190049,2190042,2190044) and r.uid='{0}' and i.use_flag=true
and r.begin_time + interval '1 month' between '{1}' and '{2}'
and r.index_id=i.index_id and index_type=219) lm 
full join
(select i.description,"avgScore" avgscore from r_m_indexdata r,mon_index i where r.index_id in 
(2190055,2190057,2190058,2190059,2190060,2190061,2190062,
2190064,2190065,2190040,2190041,2190049,2190042,2190044) and r.uid='{0}' and i.use_flag=true
and r.begin_time between '{1}' and '{2}'and r.index_id=i.index_id and index_type=219) cm 
on lm.description=cm.description'''.format(targetid, begin_time, end_time)
    # print(sqlperfinfo)
    sqlperfinfocursor = getValue(pg, sqlperfinfo)
    sqlperfinforesult = sqlperfinfocursor.fetchall()

    for resulttolist in sqlperfinforesult:
        sqlperfinforesult[sqlperfinforesult.index(resulttolist)] = list(resulttolist)

    sqlresult = CommUtil.createTable(head, sqlperfinforesult, des)

    return sqlresult


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
        perfinforesult = getperformanceinfo(pg, targetid, begintime, endtime)
        if perfinforesult:
            # print("msg=" + perfinforesult)
            sqlpf = '''
begin;
delete from rpt_perf_worktime where rpt_id='{0}' and target_id='{1}';
insert into rpt_perf_worktime(rpt_id,target_id,rpt_ind_id,rpt_name,rpt_avg_val,rpt_avg_val_l,rpt_avg_diff,rpt_node)
select distinct '{0}' rptid,'{1}' target_id,coalesce(cm.index_id,lm.index_id) index_id,
coalesce(cm.description,lm.description) description,coalesce(lm.avgscore,0) lmav,
coalesce(cm.avgscore,0) cmav,
round((coalesce(cm.avgscore,0)-coalesce(lm.avgscore,0))::numeric,2) as change,'' as note 
from 
(select r.index_id, i.description,"avgScore" avgscore from r_m_indexdata r,mon_index i where r.index_id in 
(2190055,2190057,2190058,2190059,2190060,2190061,2190062,
2190064,2190065,2190040,2190041,2190049,2190042,2190044) and r.uid='{1}' and i.use_flag=true
and r.begin_time + interval '1 month' between '{2}' and '{3}'
and r.index_id=i.index_id and index_type=219) lm
full join
(select r.index_id,i.description,"avgScore" avgscore from r_m_indexdata r,mon_index i where r.index_id in 
(2190055,2190057,2190058,2190059,2190060,2190061,2190062,
2190064,2190065,2190040,2190041,2190049,2190042,2190044) and r.uid='{1}' and i.use_flag=true
and r.begin_time between '{2}' and '{3}' 
and r.index_id=i.index_id and index_type=219) cm 
on lm.description=cm.description;
end;
'''.format(rpt_id, targetid, begintime, endtime)
            pg.execute(sqlpf)

    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

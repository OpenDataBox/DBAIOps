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


def getwaitclassinfo(pg, targetid, begin_time, end_time):
    head = ['本月排名', '等待类别', '本月平均等待时间', '上月排名', '上月平均等待时间', '变化', '说明']
    des = ""
    sqlwaitcalss = '''
select coalesce(cm.rn,0) crn,cm.name,      
       coalesce(cm.avgscore,0) cavg,
       coalesce(lm.rn,0) lrn,
       coalesce(lm.avgscore,0) lavg,
       coalesce(cm.avgscore,0)-coalesce(lm.avgscore,0) diff,
       '' note
  from (select row_number() over(order by avgscore desc) as rn, t.*
          from (select name, round(avg("avgScore")::numeric,2) as avgscore
                  from r_m_perf_item_detail w, sys_dict s, p_perf_eva p
                 where w.wait_class = s.value ::numeric
                   and s.type = 'wait_class'
                   /*and p.use_flag = true*/
                   and w.perf_eva_id = p.eva_id
                   and p.target_id = '{0}'
                   and w.begin_time + interval
                 '1 month' between '{1}' and '{2}'
                 group by name) t) lm full join
       (select row_number() over(order by avgscore desc) as rn, t.*
          from (select name, round(avg("avgScore")::numeric,2) as avgscore
                  from r_m_perf_item_detail w, sys_dict s, p_perf_eva p
                 where w.wait_class = s.value::numeric
                   and s.type = 'wait_class'
                   /*and p.use_flag = true*/
                   and w.perf_eva_id = p.eva_id
                   and p.target_id = '{0}'
                   and w.begin_time between '{1}' and '{2}'
				 group by name
		) t) cm
 on lm.name = cm.name
 order by 1
'''.format(targetid, begin_time, end_time)
    # print(sqlwaitcalss)
    sqlwaitcalsscursor = getValue(pg, sqlwaitcalss)
    sqlwaitcalssresult = sqlwaitcalsscursor.fetchall()
    for resulttolist in sqlwaitcalssresult:
        sqlwaitcalssresult[sqlwaitcalssresult.index(resulttolist)] = list(resulttolist)

    sqlresult = CommUtil.createTable(head, sqlwaitcalssresult, des)
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
        waitclassresult = getwaitclassinfo(pg, targetid, begintime, endtime)
        if waitclassresult:
            # print("msg=" + waitclassresult)
            sqlwcr = '''
begin;
delete from rpt_wait_class where rpt_id='{0}' and target_id='{1}';
insert into rpt_wait_class(rpt_id,target_id,rpt_class_id,rpt_metric_value,rpt_rank,rpt_metric_value_l,rpt_rank_l,rpt_diff,rpt_note)
select '{0}' rptid,'{1}' target_id,coalesce(cm.name,lm.name),
       coalesce(cm.avgscore,0) cavg,
       coalesce(cm.rn,0) crn,
       coalesce(lm.avgscore,0) lavg,
       coalesce(lm.rn,0) lrn,
       coalesce(cm.avgscore,0)-coalesce(lm.avgscore,0) diff,
       '' note
  from (select row_number() over(order by avgscore desc) as rn, t.*
          from (select name, round(avg("avgScore")::numeric,2) as avgscore
                  from r_m_perf_item_detail w, sys_dict s, p_perf_eva p
                 where w.wait_class = s.value ::numeric
                   and s.type = 'wait_class'
                   /*and p.use_flag = true*/
                   and w.perf_eva_id = p.eva_id
                   and p.target_id = '{1}'
                   and w.begin_time + interval
                 '1 month' between '{2}' and '{3}'
                 group by name) t) lm full join
       (select row_number() over(order by avgscore desc) as rn, t.*
          from (select name, round(avg("avgScore")::numeric,2) as avgscore
                  from r_m_perf_item_detail w, sys_dict s, p_perf_eva p
                 where w.wait_class = s.value::numeric
                   and s.type = 'wait_class'
                   /*and p.use_flag = true*/
                   and w.perf_eva_id = p.eva_id
                   and p.target_id = '{1}'
                   and w.begin_time between '{2}' and '{3}'
				 group by name
		) t) cm
 on lm.name = cm.name
 order by 1;
end;
'''.format(rpt_id, targetid, begintime, endtime)
            pg.execute(sqlwcr)

    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

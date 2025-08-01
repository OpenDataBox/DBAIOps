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


def getdeduct(pg, targetid, begin_time, end_time):
    head = ['指标名称', '指标描述', '扣分次数', '指标平均值', '指标最小值', '指标最大值', '说明']
    des = "性能指标扣分详情"
    sqlperftip = '''
select description,remark,deduct_cnt,avgscore,minscore,maxsocre,note from 
(select i.description,i.remark,i.index_id ,"avgScore" avgscore,"minScore" minscore, "maxScore" maxsocre,' ' as note 
from r_m_indexdata r,mon_index i where r.index_id in 
(2190055,2190057,2190058,2190059,2190060,2190061,2190062,
2190064,2190065,2190040,2190041,2190049,2190042,2190044) and r.uid='{0}' 
and r.begin_time between '{1}' and '{2}'and 
r.index_id=i.index_id and index_type=219 and use_flag=true ) tmp1,
(select metric_id,count(*) deduct_cnt from p_perf_eva_detail where record_time between '{1}' and '{2}'
 and metric_id in (2190055,2190057,2190058,2190059,2190060,2190061,2190062,
2190064,2190065,2190040,2190041,2190049,2190042,2190044) and target_id='{0}' and eva_level in ('C','D') group by metric_id) tmp2
where tmp1.index_id=tmp2.metric_id'''.format(targetid, begin_time, end_time)
    sqlperftipcursor = getValue(pg, sqlperftip)
    sqlperftipresult = sqlperftipcursor.fetchall()

    for resulttolist in sqlperftipresult:
        sqlperftipresult[sqlperftipresult.index(resulttolist)] = list(resulttolist)

    sqlresult = CommUtil.createTable(head, sqlperftipresult, des)

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
        perfinforesult = getdeduct(pg, targetid, begintime, endtime)
        if perfinforesult:
            ##print("msg=" + perfinforesult)
            sqlpfr = '''
begin;
delete from rpt_scope_detail where rpt_id='{0}' and target_id='{1}' and rpt_scope_category='P_OTHER';
insert into rpt_scope_detail(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_note,
                        rpt_scope_count,rpt_scope_ded_avg,rpt_scope_ded_max) 
select distinct '{0}' rptid,'{1}' target_id,'P_OTHER' rsc,index_id, iname,description, remark, deduct_cnt, avgscore, maxsocre
  from (select i.description,
               i.remark,
               i.index_id,
			   r.iname,
               "avgScore" avgscore,
               "minScore" minscore,
               "maxScore" maxsocre,
               '' as note
          from r_m_indexdata r, mon_index i
         where r.index_id in (2190055,
                              2190057,
                              2190058,
                              2190059,
                              2190060,
                              2190061,
                              2190062,
                              2190064,
                              2190065,
                              2190040,
                              2190041,
                              2190049,
                              2190042,
                              2190044)
           and r.uid = '{1}'
           and r.begin_time between '{2}' and '{3}'
           and r.index_id = i.index_id
           and index_type = 219
           and use_flag = true) tmp1,
       (select metric_id, count(*) deduct_cnt
          from p_perf_eva_detail
         where record_time between '{2}' and '{3}'
           and metric_id in (2190055,
                             2190057,
                             2190058,
                             2190059,
                             2190060,
                             2190061,
                             2190062,
                             2190064,
                             2190065,
                             2190040,
                             2190041,
                             2190049,
                             2190042,
                             2190044)
           and target_id = '{1}'
           and eva_level in ('C', 'D')
         group by metric_id) tmp2
 where tmp1.index_id = tmp2.metric_id;
end;
'''.format(rpt_id, targetid, begintime, endtime)
            pg.execute(sqlpfr)

    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

sys.path.append('/usr/software/knowl')
import DBUtil
import psycopg2
import re
import PGUtil
import ResultCode
import tags


def register(file_name):
    ltag = ['2.1', 'OS']
    return tags.register(ltag, file_name)


class Result(object):
    def __str__(self):
        return "\n".join("{}={}".format(k, getattr(self, k))
                         for k in self.__dict__.keys())


def getValue(ora, sql):
    result = ora.execute(sql)
    if (result.code != 0):
        print("msg=" + result.msg)
        sys.exit()
    return result.msg


def parseURL(url):
    pattern = r'(\w+):(\w+)([thin:@/]+)([0-9.]+):(\d+)([:/])(\w+)'
    matchObj = re.match(pattern, url, re.I)
    return matchObj.group(2), matchObj.group(4), matchObj.group(5), matchObj.group(7)


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
        result = ""

        ##健康总体分图表数据
        insql = '''
begin;
delete from rpt_health_score_reportdata where rpt_id='{0}' and target_id='{1}';

with a as (
select * from mon_indexdata_his where index_id = 2180400 and uid = '{1}' and record_time between '{2}' and '{3}'
)
insert into rpt_health_score_reportdata(rpt_id,target_id,rpt_metric_id,iname,"minScore","maxScore","avgScore","count","total",
									   "maxTime","minTime",begin_time,end_time)
select '{0}' rpt_id,a.uid target_id,a.index_id rpt_metric_id,a.iname,
round(min(a.value::numeric),2) minscore,
round(max(a.value::numeric),2) maxscore,
round(avg(a.value::numeric),2) avgscore,
count(a.value) cnt,
round(sum(a.value::numeric),2) total,
(select max(record_time) from a bb where bb.value::numeric=max(a.value::numeric)) maxtime,
(select min(record_time) from a bb where bb.value::numeric=min(a.value::numeric)) mintime,
to_timestamp(to_char(record_time,'yyyy-mm-dd hh24')||':00:00','yyyy-mm-dd hh24:mi:ss') begin_time,
'{3}' end_time 		
  from  a
   group by a.uid,a.index_id,a.iname ,to_char(record_time,'yyyy-mm-dd hh24');

end;
'''.format(rpt_id, targetid, begintime, endtime)
        pg.execute(insql)

        ##健康分项分图表数据
        insql_1 = '''
begin;
delete from rpt_health_item_score_reportdata where rpt_id='{0}' and target_id='{1}';

with rdis as (select hc.target_id,h.* from h_health_check_item_score h, h_health_check hc
  where hc.target_id in ('{1}') and h.record_time between '{2}' and '{3}'
        and hc.health_check_id = h.health_check_id and hc.use_flag = TRUE )
insert into rpt_health_item_score_reportdata(rpt_id,target_id,model_id,model_item_id,model_item_name,
"minScore","maxScore","avgScore","count","total","maxTime","minTime",begin_time,end_time)
select 
'{0}' rpt_id,rdis.target_id,hmi.model_id,hmi.model_item_id,hmi.model_item_name,
round(min(rdis.score::numeric),2) minscore,
round(max(rdis.score::numeric),2) maxscore,
round(avg(rdis.score::numeric),2) avgscore,
count(rdis.score) cnt,
round(sum(rdis.score::numeric),2) total,
(select max(record_time) from rdis bb where bb.score:: numeric=max(rdis.score:: numeric)
) maxtime,
(select min(record_time) from rdis bb where bb.score:: numeric=min(rdis.score:: numeric)
) mintime,
to_timestamp(to_char(record_time,'yyyy-mm-dd hh24')||':00:00','yyyy-mm-dd hh24:mi:ss') begin_time,
'{3}' end_time 		
from  rdis,
 ( SELECT * FROM h_model_item WHERE use_flag = TRUE ) AS hmi 
WHERE   hmi.model_item_id = rdis.model_item_id 
group by rdis.target_id,hmi.model_id,hmi.model_item_id,hmi.model_item_name,to_char(record_time,'yyyy-mm-dd hh24');
	
end;
'''.format(rpt_id, targetid, begintime, endtime)
        pg.execute(insql_1)


    except psycopg2.DatabaseError as e:
       errorInfo = str(e)
       print("异常：" + errorInfo)

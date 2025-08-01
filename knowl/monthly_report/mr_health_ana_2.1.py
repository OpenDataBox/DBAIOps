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

insert into rpt_health_score_reportdata(rpt_id,target_id,rpt_metric_id,iname,"minScore","maxScore","avgScore","count","total",
									   "maxTime","minTime",begin_time,end_time)
SELECT
'{0}' rpt_id,a.uid target_id,a.index_id rpt_metric_id,a.iname,a."minScore",a."maxScore",a."avgScore",a."count",
a."total",a."maxTime",a."minTime",a.begin_time,a.end_time 
FROM
	r_d_indexdata AS A 
WHERE	
	A.uid IN ('{1}')
	AND to_char( A.begin_time, 'YYYY-MM-DD HH24:MI:SS' ) >= '{2}' 
	AND to_char( A.begin_time, 'YYYY-MM-DD HH24:MI:SS' ) < '{3}' 
	AND A.index_id = '2180400' 
/*ORDER BY A.begin_time ASC*/;
end;
'''.format(rpt_id, targetid, begintime, endtime)
        pg.execute(insql)

        ##健康分项分图表数据
        insql_1 = '''
begin;
delete from rpt_health_item_score_reportdata where rpt_id='{0}' and target_id='{1}';

insert into rpt_health_item_score_reportdata(rpt_id,target_id,model_id,model_item_id,model_item_name,
"minScore","maxScore","avgScore","count","total","maxTime","minTime",begin_time,end_time)
SELECT '{0}' rpt_id,hcheck.target_id,hmi.model_id,hmi.model_item_id,hmi.model_item_name,
    rdis."minScore",rdis."maxScore",rdis."avgScore",rdis."count",rdis."total",
	rdis."maxTime",rdis."minTime",rdis.begin_time,rdis.end_time 
FROM
	r_d_health_item_score AS rdis,
	( SELECT * FROM h_health_check WHERE use_flag = TRUE ) AS hcheck,
	( SELECT * FROM h_model_item WHERE use_flag = TRUE ) AS hmi 
WHERE hcheck.target_id IN ( '{1}' )
	AND to_char( rdis.begin_time, 'YYYY-MM-DD HH24:MI:SS' ) >= '{2}'
	AND to_char( rdis.begin_time, 'YYYY-MM-DD HH24:MI:SS' ) < '{3}'
	AND hcheck.health_check_id = rdis.health_check_id 
	AND hmi.model_item_id = rdis.model_item_id 
/*ORDER BY rdis.begin_time*/;
end;
'''.format(rpt_id, targetid, begintime, endtime)
        pg.execute(insql_1)


    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

    # except Exception as e:
    #    errorInfo = str(e)
    #    print("异常：" + errorInfo)

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
    ltag = ['0', 'Summary']
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


def getLastRpt(pg, rptid, targetid):
    lrptid = ""
    sql = '''
select b.rpt_id
  from rpt_db_instance a,rpt_main b
 where a.db_id in (select db_id from rpt_main where rpt_id ='{0}')
   and a.target_id = '{1}'
   and a.rpt_id=b.rpt_id
   and a.db_id = b.db_id 
   and a.rpt_instance_status not in (0,3)
 order by b.rpt_report_date desc 
 limit 1
'''.format(rptid, targetid)
    cursor = getValue(pg, sql)
    result = cursor.fetchone()

    if result:
        for rows in result:
            if not row[0] is None:
                lrptid = row[0]
            else:
                lrptid = ""
    else:
        lrptid = ""
    if lrptid == rptid:
        lrptid = ""

    return lrptid


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
        ##update rpt_findings default ques_check oper_type
        qlrsql = getLastRpt(pg, rpt_id, targetid)

        insql = '''
begin;

update rpt_finding set ques_check =0 ,oper_type=0
where rpt_finding_level = 1
  and rpt_id = '{0}'
  and target_id = '{1}';

update rpt_finding aa
set ques_check=res.tag
from (
	select cm.rpt_id,cm.target_id,cm.rpt_finding_module,cm.rpt_finding_id,
	case when lm.oper_type = 1 then 1
	when lm.oper_type = 2 then 2
	else 0 end tag
	from 
	(select * from rpt_finding
	where rpt_id = '{0}'
	  and target_id = '{1}'
	  and rpt_finding_level =1) cm left join (
	select * from rpt_finding
	where rpt_id = '{2}'
	  and target_id = '{1}'
	  and rpt_finding_level =1
	) lm on cm.rpt_finding_module=lm.rpt_finding_module
	and coalesce(cm.rpt_sub_id,' ')=coalesce(lm.rpt_sub_id,' ')
) res 
where aa.rpt_id=res.rpt_id 
  and aa.target_id=res.target_id
  and aa.rpt_finding_module=res.rpt_finding_module
  and aa.rpt_finding_id=res.rpt_finding_id;

end ;
'''.format(rpt_id, targetid, qlrsql)
        pg.execute(insql)

    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

    # except Exception as e:
    #    errorInfo = str(e)
    #    print("异常：" + errorInfo)

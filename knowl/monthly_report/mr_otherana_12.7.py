#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

sys.path.append('/usr/software/knowl')
import DBUtil
import psycopg2
import cx_Oracle as oracle
import re
import PGUtil
import ResultCode
import tags


def register(file_name):
    ltag = ['12.7', 'degree']
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


def getUsrProf(conn, targetid, bt, et):
    p1 = ""
    sql = """
select distinct col1,col2,col3,col4
from p_oracle_cib where  record_time =
(select max(record_time) from p_oracle_cib 
where target_id = '{0}'
and index_id = 2202005
and record_time between '{1}' and '{2}'
) and index_id = 2202005
and target_id = '{0}'
and seq_id <> 0
""".format(targetid, bt, et)

    cursor = getValue(conn, sql)
    results = cursor.fetchall()

    resld = []

    if (len(results) > 0):
        for x in results:
            resld.append(dict(owner=x[0], objname=x[1], ttype=x[2], degree=x[3]))

        sql = ""
        for res in resld:
            sql += "select '" + res.get('owner') + "' c1,'" + res.get('objname') + "' c2,'" + res.get(
                'ttype') + "' c3,'" + res.get('degree') + "' c4 union all "
        sql = sql[0:-10]
        p1 = sql

    return p1


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
        ##ora = orautil.Oracle(host, usr, pwd, port, database)

        resup = getUsrProf(pg, targetid, begintime, endtime)
        if (len(resup) > 0):
            sqlf = """
begin;
delete from rpt_degree_obj where rpt_id='{0}' and target_id='{2}';

insert into rpt_degree_obj(rpt_id,target_id,rpt_owner,rpt_obj_name,rpt_obj_type,rpt_degree,rpt_note)
select '{0}' rptid,'{2}' target_id,res.c1,res.c2,res.c3,res.c4::int,''
from ({1}) res;
end;""".format(rpt_id, resup, targetid)
            pg.execute(sqlf)

    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

    except oracle.DatabaseError as e:
        if not ora is None:
            ora.close()

    # except Exception as e:
    #    errorInfo = str(e)
    #    print("异常：" + errorInfo)

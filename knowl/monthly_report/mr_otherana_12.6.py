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
    ltag = ['12.6', 'AUDIT']
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


def getDumpDes(conn, targetid, bt, et):
    p1 = ""
    sql = """
select distinct col1,col2,col3,col4
from p_oracle_cib where  record_time =
(select max(record_time) from p_oracle_cib 
where target_id = '{0}'
and index_id = 2202004
and record_time between '{1}' and '{2}'
) and index_id = 2202004
and target_id = '{0}'
and seq_id <> 0
""".format(targetid, bt, et)

    cursor = getValue(conn, sql)
    results = cursor.fetchall()

    resld = []

    if (len(results) > 0):
        for x in results:
            resld.append(dict(acol1=x[0], acol2=x[1], acol3=x[2], acol4=x[3]))

        sql = ""
        for res in resld:
            sql += "select '" + res.get('acol1') + "' c1," + res.get('acol2') + " c2,'" + res.get(
                'acol3') + "' c3,'" + res.get('acol4') + "' c4 union all "
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
        resup = getDumpDes(pg, targetid, begintime, endtime)
        if (len(resup) > 0):
            sqlf = """
begin;
delete from rpt_audit_inode where rpt_id='{0}' and target_id='{1}';

insert into rpt_audit_inode(rpt_id,target_id,rpt_audit_loc,rpt_audit_cnt,rpt_inode_ratio,rpt_note)
select '{0}' rptid,'{1}' target_id,res.c1,res.c2,res.c3,res.c4
from ({2}) res;
end;""".format(rpt_id, targetid, resup)
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

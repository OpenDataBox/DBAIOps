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


def getsqlresult(db, sql):
    result = db.execute(sql)
    if (result.code != 0):
        msg = result.msg
        print("msg=WORD_BEGIN" + msg + "WORD_END")
        sys.exit()

    sqlresult = result.msg.fetchall()
    for resulttolist in sqlresult:
        sqlresult[sqlresult.index(resulttolist)] = list(resulttolist)
    return sqlresult


def security(pg, target_id, bt, et):
    p1 = ""
    head = ['用户名', '权限', '备注']
    des = "数据库权限分析"
    sql = """
select distinct col1,col2,col3 
from p_oracle_cib where  record_time =
(select max(record_time) from p_oracle_cib 
where target_id = '{0}'
and index_id = 2202001
and record_time between '{1}' and '{2}'
) and index_id = 2202001
and target_id = '{0}'
and seq_id <> 0
""".format(target_id, bt, et)
    securityresult = getsqlresult(pg, sql)

    resld = []
    sqlresult = CommUtil.createTable(head, securityresult, des)
    if len(securityresult) > 0:
        for x in securityresult:
            resld.append(dict(grantee=x[0], granted_role=x[1], note=x[2]))

        sqlres = ""
        for res in resld:
            sqlres += "select '" + res.get('grantee') + "' c1,'" + res.get('granted_role') + "' c2,'" + str(
                res.get('note')) + "' c3 union all "
        sqlres = sqlres[0:-10]
        p1 = sqlres

    return sqlresult, p1


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
        ##conn = orautil.Oracle(host, usr, pwd, port, database)
        securityresult, resql = security(pg, targetid, begintime, endtime)
        if securityresult:
            # print("msg=" + securityresult)
            sqlf = """
begin;
delete from rpt_unsysuser where rpt_id='{0}' and target_id='{2}';
insert into rpt_unsysuser(rpt_id,rpt_userpt_name,rpt_userpt_permissions,rpt_notes,target_id)
select '{0}' rptid,res.c1,res.c2,res.c3,'{2}' target_id
from ({1}) res;
end;
""".format(rpt_id, resql, targetid)
            pg.execute(sqlf)

    except psycopg2.DatabaseError as e:
        if not conn is None:
            conn.close()

    except oracle.DatabaseError as e:
        if not ora is None:
            ora.close()

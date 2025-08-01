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


def novalidobject(pg, targetid, begin_time, end_time):
    ana = ""
    head = ['对象类型', '本月无效数', '上月无效数', '差异']
    des = "无效对象分析"
    p1 = ""
    lmnovalidcnt = {}
    cmnovalidcnt = {}
    resultlist = []
    sql = '''
select lm.error_data lm_addinfo,cm.error_data cm_addinfo from 
(select item_desc,case when error_data ='' then null else error_data end error_data from dc_job_log_detail d where dc_log_id=(
select max(id) from dc_job_log l where target_id='{0}' 
and l.handle_time + interval '1 month' between '{1}' and '{2}') and item_desc='失效对象检查') lm
full join
(select item_desc,case when error_data ='' then null else error_data end error_data from dc_job_log_detail d where dc_log_id=(
select max(id) from dc_job_log l where target_id='{0}' and l.handle_time between '{1}' and '{2}')
 and item_desc='失效对象检查') cm 
 on lm.item_desc=cm.item_desc'''.format(targetid, begin_time, end_time)
    novalidresult = getsqlresult(pg, sql)
    if len(novalidresult) > 0:
        ana = '''建议：
1、修复或删除无效对象
'''

    for row in novalidresult:
        if row[0] is not None:
            for n in row[0][0:-1].split(','):
                lmnovalidcnt[n.split('-')[1]] = n.split('-')[2]
        if row[1] is not None:
            for n in row[1][0:-1].split(','):
                cmnovalidcnt[n.split('-')[1]] = n.split('-')[2]

    for key, value in cmnovalidcnt.items():
        if key not in lmnovalidcnt.keys():
            lmnovalidcnt[key] = 0
        resultlist.append((key, value, lmnovalidcnt[key], int(value) - int(lmnovalidcnt[key])))

    sqlresult = CommUtil.createTable(head, resultlist, des)

    sqlres = ""
    for res in resultlist:
        sqlres += "select '" + res[0] + "' c1," + str(int(res[1])) + " c2," + str(int(res[2])) + " c3 union all "
    sqlres = sqlres[0:-10]
    p1 = sqlres

    return ana, sqlresult, p1


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
        novalidnote, novalidresult, rsql = novalidobject(pg, targetid, begintime, endtime)
        if novalidresult:
            # print("msg=" + novalidresult)
            sqlf = """
begin;
delete from rpt_invalid_obj where rpt_id='{0}' and target_id='{2}';
insert into rpt_invalid_obj(rpt_id,target_id,rpt_type,rpt_count,rpt_count_l)
select '{0}' rptid,'{2}' target_id,res.c1,res.c2,res.c3
from ({1}) res;
end;""".format(rpt_id, rsql, targetid)
            pg.execute(sqlf)

        if novalidnote:
            # print("SCREEN_BEGIN问题与发现:\\n" + novalidnote + "SCREEN_END")
            ismf = '''
begin;
delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module='other_invalid';

insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'other_invalid' rpt_finding_module,
0 rpt_finding_type,'' rpt_sub_id,'' iname,
'无效对象分析' rpt_finding_label,
'信息' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
0 rpt_finding_level;
end;
'''.format(rpt_id, targetid, novalidnote)
            pg.execute(ismf)

    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

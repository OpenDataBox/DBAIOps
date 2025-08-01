#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

sys.path.append('/usr/software/knowl')
import DBUtil
import psycopg2
import re
import json
import PGUtil
from datetime import datetime, timedelta
import ResultCode
import os
import subprocess

returncode = []


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


def parseURL(url):
    pattern = r'(\w+):(\w+)([thin:@/]+)([0-9.]+):(\d+)([:/])(\w+)'
    matchObj = re.match(pattern, url, re.I)
    return matchObj.group(2), matchObj.group(4), matchObj.group(5), matchObj.group(7)


def finalstatus(pg, rptwk_id):
    sql = '''
begin;
update rptwk_main set rpt_status=1 where rptwk_id='{0}';
end;'''.format(rptwk_id)
    pg.execute(sql)


def domr(param1, mr_script):
    ana = ""
    script = os.path.join("python3 /usr/software/knowl/week_report/", mr_script)
    cmd = script + " '" + json.dumps(param1) + "'"
    print(cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
    p.wait()
    returncode.append(p.returncode)
    if p.returncode == 0:
        for line in p.stdout.readlines():
            ana += line.decode('utf-8').strip() + '\n'
        print(ana)
    else:
        for line in p.stdout.readlines():
            ana += line.decode('utf-8').strip() + '\n'
        print("msg=" + mr_script + "Execution Failed Reason:" + ana)


if __name__ == '__main__':
    param1 = eval(sys.argv[1])
    selfparam = sys.argv[3]
    tmp = "'" + selfparam + "'"
    tmp1 = tmp.replace("=", "': '").replace(";", "','")
    tmp2 = tmp1[0:-3]
    tmp3 = "{" + tmp2 + "}"
    tmp4 = eval(tmp3)
    param = {}
    param.update(param1)
    param.update(tmp4)
    # sd=datetime.now()-timedelta(days=datetime.now().date().weekday()+7)
    # year=sd.year
    # month=sd.month
    # day=sd.day
    # ed=sd+timedelta(days=6)
    # endyear= ed.year
    # endmonth= ed.month
    # endday = ed.day
    # if param['planType'] == '1':
    # param['start_time'] = datetime(year,month,day,0,0,0).strftime('%Y-%m-%d %H:%M:%S')
    # param['end_time'] = datetime(endyear,endmonth,endday,23,59,59).strftime('%Y-%m-%d %H:%M:%S')
    if param['planType'] == '4':
        sd = datetime.now() - timedelta(days=datetime.now().date().weekday() + 7)
        ed = sd + timedelta(days=6)
        year = sd.year
        month = sd.month
        day = sd.day
        endyear = ed.year
        endmonth = ed.month
        endday = ed.day
        param['start_time'] = datetime(year, month, day, 0, 0, 0).strftime('%Y-%m-%d %H:%M:%S')
        param['end_time'] = datetime(endyear, endmonth, endday, 23, 59, 59).strftime('%Y-%m-%d %H:%M:%S')
        weeks = int(datetime(year, month, day).strftime("%W")) + 1
    elif param['planType'] == '7':
        sd = datetime.strptime(param['start_time'], '%Y-%m-%d %H:%M:%S')
        ed = datetime.strptime(param['end_time'], '%Y-%m-%d %H:%M:%S')
        year = sd.year
        month = sd.month
        day = sd.day
        endyear = ed.year
        endmonth = ed.month
        endday = ed.day
        weeks = int(sd.strftime("%W")) + 1

    dbip = param['pg_ip']
    dbname = param['pg_dbname']
    username = param['pg_usr']
    password = param['pg_pwd']
    pgport = param['pg_port']
    job_id = param['jobId']
    db_id = param['dbId']
    target_id = param['targetId']
    planType = param['planType']
    begintime = param['start_time']
    endtime = param['end_time']
    rptwk_id = "WR-" + str(param['triggerID'])
    param['rptwk_id'] = rptwk_id

    pg = PGUtil.Postgre(dbip, username, password, pgport, dbname)

    try:
        # print(param)
        domr(param, "wr_score_ana.py")
        domr(param, "wr_warnlevel_ana.py")
        domr(param, "wr_warntype_ana.py")
        domr(param, "wr_warndetail_ana.py")
        domr(param, "wr_logerr_ana.py")
        domr(param, "wr_topsql_ana.py")
        # domr(param,"mr_health_ana_2.2.1.py")
        # domr(param,"mr_health_ana_2.2.2.py")
        # domr(param,"mr_health_ana_2.2.3.py")
        # domr(param,"mr_health_ana_2.2.4.py")
        # domr(param,"mr_health_ana_2.2.5.py")
        # domr(param,"mr_health_ana_2.2.6.py")
        # domr(param,"mr_health_ana_2.2.7.py")
        # domr(param,"mr_top_sql_ana_7.0.py")
        # domr(param,"mr_logana_6.1.py")
        # domr(param,"mr_logana_6.2.1.py")
        # domr(param,"mr_logana_6.2.2.py")
        # domr(param,"mr_logana_6.2.3.py")
        # domr(param,"mr_logswitch_10.py")
        # domr(param,"mr_summ_ana_0.py")
        finalstatus(pg, rptwk_id)
        print("msg=success")

    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

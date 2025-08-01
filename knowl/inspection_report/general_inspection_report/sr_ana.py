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
from itertools import chain

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


def finalstatus(pg, rpt_id, target_id, planType, job_id):
    # if len(set(returncode)) == 1 and 0 in set(returncode):
    #    sql1 = "update rpt_db_instance set rpt_instance_status=1 where rpt_id='{0}' and target_id='{1}';".format(rpt_id,target_id)
    # else:
    #    sql1 = "update rpt_db_instance set rpt_instance_status=3 where rpt_id='{0}' and target_id='{1}';".format(rpt_id,target_id)
    sql1 = "update rpt_db_instance set rpt_instance_status=1 where rpt_id='{0}' and target_id='{1}';".format(rpt_id,
                                                                                                             target_id)
    pg.execute(sql1)
    sql2 = '''
select distinct rpt_instance_status from rpt_db_instance where rpt_id='{0}';
'''.format(rpt_id)
    instance_status = getsqlresult(pg, sql2)
    instance_status = list(chain.from_iterable(instance_status))
    print(instance_status)
    if len(set(instance_status)) == 1 and 1 in set(instance_status):
        sql3 = '''
update rpt_main set rpt_status=1 where rpt_id='{0}' and rpt_type =3
'''.format(rpt_id)
        pg.execute(sql3)
    elif 3 in set(instance_status):
        sql3 = '''
update rpt_main set rpt_status=3 where rpt_id='{0}' and rpt_type =3
'''.format(rpt_id)
        pg.execute(sql3)

    if planType == '1':
        sql4 = 'update rpt_state_inspection_job set job_status=1 where job_id={0}'.format(job_id)
    else:
        sql4 = 'update rpt_state_inspection_job set job_status=3 where job_id={0}'.format(job_id)
    pg.execute(sql4)

    sql5 = '''
select job_status from rpt_state_inspection_job where plan_id =
(select plan_id from rpt_state_inspection_job where job_id={0});
'''.format(job_id)
    job_status = getsqlresult(pg, sql5)
    job_status = list(chain.from_iterable(job_status))
    if len(set(job_status)) == 1 and 3 in set(job_status):
        sql6 = '''
update rpt_state_inspection_plan set plan_status=3 where plan_id = 
(select plan_id from rpt_state_inspection_job where job_id={0})
'''.format(job_id)
        pg.execute(sql6)


def domr(param1, mr_script):
    ana = ""
    script = os.path.join("/usr/software/knowl/inspection_report/", mr_script)
    cmd = 'python3 ' + script + " '" + json.dumps(param1) + "'"
    print(cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
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
    month = (datetime.now().replace(day=1) - timedelta(days=1)).month
    year = (datetime.now().replace(day=1) - timedelta(days=1)).year
    day = (datetime.now().replace(day=1) - timedelta(days=1)).day
    # if param['planType'] == '1':
    #    param['start_time'] = datetime(year,month,1,0,0,0).strftime('%Y-%m-%d %H:%M:%S')
    #    param['end_time'] = datetime(year,month,day,23,59,59).strftime('%Y-%m-%d %H:%M:%S')

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
    rpt_id = "RI-" + str(param['triggerID'])
    param['rptid'] = rpt_id

    pg = PGUtil.Postgre(dbip, username, password, pgport, dbname)

    try:
        domr(param, "sr_basicinfo.py")
        finalstatus(pg, rpt_id, target_id, planType, job_id)
        print("msg=rpt_id=" + rpt_id + ";target_id=" + param['targetId'] + ";")

    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

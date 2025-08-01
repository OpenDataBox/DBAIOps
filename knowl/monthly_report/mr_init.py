#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

sys.path.append('/usr/software/knowl')
import DBUtil
import psycopg2
import PGUtil
from datetime import datetime, timedelta
import ResultCode

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


def initstatus(pg, job_id, db_id, rpt_id, begin_time, end_time):
    # sql1 = 'select count(*) from rpt_db_instance where db_id={0} and rpt_instance_status=0'.format(db_id)
    # sql3 = 'select distinct rpt_id from rpt_db_instance where db_id={0} and rpt_instance_status=0'.format(db_id)
    # rpt_id = getsqlresult(pg,sql3)[0][0]
    # sql5 = '''select job_id from rpt_main where rpt_id='{0}' and db_id={1}'''.format(rpt_id,db_id)
    # check_job_id = getsqlresult(pg,sql5)[0][0]

    # initcheck = getsqlresult(pg,sql1)
    # print(initcheck)
    # if initcheck[0][0] == 0:
    # rpt_id = str(uuid.uuid1())
    sql2 = '''
begin;
insert into rpt_main(rpt_id,rpt_create_date,rpt_report_date,job_id,db_id,rpt_type,rpt_status,rpt_start_date,rpt_end_date) values('{0}','{1}','{1}',{2},{3},1,0,'{4}','{5}');
update rpt_db_instance set rpt_instance_status=3 where db_id={3} and rpt_instance_status=0;
insert into rpt_db_instance(rpt_id,db_id,db_name,target_id,target_subid,mgt_name,connect_ip,rpt_instance_status) select '{0}' rpt_id,mgt_system.groupdbid,db_name,uid,subuid,mgt_system.name,ip
,0 from group_db inner join mgt_system on group_db.id = mgt_system.groupdbid where mgt_system.use_flag = true and  mgt_system.groupdbid = {3};
end;
'''.format(rpt_id, datetime.now(), job_id, db_id, begin_time, end_time)
    # print(sql2)
    pg.execute(sql2)
    # else:
    #    sql3 = 'select distinct rpt_id from rpt_db_instance where db_id={0} and rpt_instance_status=0'.format(db_id)
    #    rpt_id = getsqlresult(pg,sql3)[0][0]

    sql4 = '''
begin;
update rpt_inspection_job set job_status=2 where job_id=(select job_id from rpt_main where rpt_id='{0}');
update rpt_inspection_plan set plan_status=2 where plan_id = 
(select plan_id from rpt_inspection_job where job_id=(select job_id from rpt_main where rpt_id='{0}'));
end;
'''.format(rpt_id)
    # print(sql4)
    pg.execute(sql4)


if __name__ == '__main__':
    print(sys.argv[1])
    print(sys.argv[3])
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
    if param['planType'] == '1':
        param['start_time'] = datetime(year, month, 1, 0, 0, 0).strftime('%Y-%m-%d %H:%M:%S')
        param['end_time'] = datetime(year, month, day, 23, 59, 59).strftime('%Y-%m-%d %H:%M:%S')

    dbip = param['pg_ip']
    dbname = param['pg_dbname']
    username = param['pg_usr']
    password = param['pg_pwd']
    pgport = param['pg_port']
    job_id = param['jobId']
    db_id = param['dbId']
    target_id = param['targetId']
    planType = param['planType']
    rpt_id = param['triggerID']
    print('rpt_id' + rpt_id)
    begin_time = param['start_time']
    end_time = param['end_time']

    pg = PGUtil.Postgre(dbip, username, password, pgport, dbname)

    try:
        initstatus(pg, job_id, db_id, rpt_id, begin_time, end_time)
    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

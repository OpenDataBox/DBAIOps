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


def initstatus(pg, job_id, rptwk_id, begin_time, end_time, rptwk_name, rptwk_title):
    sql2 = '''
begin;
insert into rptwk_main(rptwk_id,rptwk_name,rptwk_create_date,job_id,rpt_status,rpt_start_date,rpt_end_date,rptwk_title) values('{0}','{1}','{2}','{3}',0,'{4}','{5}','{6}');
end;
'''.format(rptwk_id, rptwk_name, datetime.now(), job_id, begin_time, end_time, rptwk_title)
    # print(sql2)
    pg.execute(sql2)


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
    sd = datetime.now() - timedelta(days=datetime.now().date().weekday() + 7)
    # year=sd.year
    # month=sd.month
    # day=sd.day
    ed = sd + timedelta(days=6)
    # endyear= ed.year
    # endmonth= ed.month
    # endday = ed.day
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
    begin_time = param['start_time']
    end_time = param['end_time']
    rptwk_id = "WR-" + str(param['triggerID'])
    param['rptwk_id'] = rptwk_id
    rptwk_title = param['weekName']
    rptwk_name = param['weekName'] + ' (' + str(year) + '年' + str(month) + '月' + str(day) + '日-' + str(
        endyear) + '年' + str(endmonth) + '月' + str(endday) + '日 第' + str(weeks) + '周)'

    pg = PGUtil.Postgre(dbip, username, password, pgport, dbname)

    try:
        initstatus(pg, job_id, rptwk_id, begin_time, end_time, rptwk_name, rptwk_title)
    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

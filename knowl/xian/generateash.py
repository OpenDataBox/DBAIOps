#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys

sys.path.append('/usr/software/knowl')
import DBUtil
import CommUtil
from datetime import datetime, timedelta


def generateash(conn, begin_time, end_time):
    ash_path = f"http://{CommUtil.get_ip()}:18090/awr/"
    sql = '''select dbid, instance_number from v$instance, v$database'''
    cs = DBUtil.getValue(conn, sql)
    rs = cs.fetchone()
    inst_number = rs[1]
    dbid = rs[0]
    ash_date = datetime.strftime(end_time, '%m%d')
    ash_time = datetime.strftime(end_time, '%H%M')

    ash_file_name = "ashrpt_" + str(inst_number) + "_" + ash_date + "_" + ash_time + ".html"
    fp = open("/usr/software/report/awr/" + ash_file_name, 'w')
    sql = '''select * from table(dbms_workload_repository.ash_report_html({0},{1},to_date('{2}','yyyy-mm-dd hh24:mi:ss'),
to_date('{3}','yyyy-mm-dd hh24:mi:ss'))) '''.format(dbid, inst_number, begin_time, end_time)
    cursor = DBUtil.getValue(conn, sql)
    res = cursor.fetchall()
    for row in res:
        print(row[0], file=fp)
    fp.close()
    print("msg=" + ash_path + ash_file_name)


def checkSampleTime(conn, begin_time, end_time):
    sql = '''select min(sample_time),max(sample_time), max(startup_time)  from dba_hist_active_sess_history t1, v$database t2, v$instance t3 
where t1.dbid=t2.dbid and t3.instance_number=t1.instance_number'''
    cs = DBUtil.getValue(conn, sql)
    rs = cs.fetchone()
    min_time = rs[0]
    start_time = rs[2]
    if min_time > begin_time:
        return 0
    if begin_time < start_time < end_time:
        return 1
    else:
        return 2


if __name__ == "__main__":
    ora = DBUtil.get_ora_env()
    bt, sz = DBUtil.get_date_env()
    if bt and sz:
        bt = datetime.strptime(bt, '%Y-%m-%d %H:%M:%S')
        et = bt + timedelta(minutes=int(sz))
    else:
        bt = datetime.strptime(bt, '%Y-%m-%d %H:%M:%S')
        et = bt + timedelta(minutes=int(15))
    start_time = ''
    min_time = ''
    flag = checkSampleTime(ora, bt, et)
    if flag == 1:
        print("msg=选择的时间窗口之间发生过数据库重新启动,无法生成ASH报告,请重新选择时间，数据库重启时间为:{0}.".format(start_time))
    elif flag == 0:
        print("msg=开始时间比数据库最早可用的采样时间早，因此无法基于选定的时间窗口生成ASH报告，ASH最早的采样时间为：{0}".format(min_time))
    else:
        generateash(ora, bt, et)


#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys

sys.path.append('/usr/software/knowl')
import DBUtil
from datetime import datetime, timedelta


def getsnapid(conn, begin_time=None, end_time=None):
    result = ''
    if begin_time is None:
        sql = '''select d.name,s.dbid,s.instance_number,snap_id,to_char(end_interval_time,'yyyy-mm-dd hh24:mi:ss') end_time from dba_hist_snapshot s,v$instance i,v$database d
where s.instance_number=i.instance_number and d.dbid=s.dbid and end_interval_time > sysdate - 7 order by end_interval_time desc'''
    else:
        sql = '''select d.name,s.dbid,s.instance_number,snap_id,to_char(end_interval_time,'yyyy-mm-dd hh24:mi:ss') end_time from dba_hist_snapshot s,v$instance i,v$database d
where s.instance_number=i.instance_number and d.dbid=s.dbid and end_interval_time between to_date('{0}','yyyy-mm-dd hh24:mi:ss') and to_date('{1}','yyyy-mm-dd hh24:mi:ss') order by end_interval_time desc
'''.format(begin_time, end_time)
    cursor = DBUtil.getValue(conn, sql)
    res = cursor.fetchall()
    for row in res:
        result += str(row) + "%a%"
    print("msg=" + result)


if __name__ == "__main__":
    ora = DBUtil.get_ora_env()
    bt, sz = DBUtil.get_date_env()
    if bt and sz:
        szz = 120
        if float(sz) < 120:
            szz = 120
        btt = datetime.strptime(bt, '%Y-%m-%d %H:%M:%S') - timedelta(minutes=int(szz))
        ett = datetime.strptime(bt, '%Y-%m-%d %H:%M:%S') + timedelta(minutes=int(sz))
        getsnapid(ora, btt, ett)
    else:
        getsnapid(ora)

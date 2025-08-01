#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@文件    :metric_shentong.py
@说明    :神通数据库metric指标
@时间    :2023/09/14 09:47:53
@作者    :xxxx
@版本    :2.0.1
'''

import json
import sys
sys.path.append('/usr/software/knowl')
import DBUtil
import CommUtil
from datetime import datetime


def get_uptime(db, metric):
    sql = "select round((sysdate-STARTUP_TIME)*24*60*60) FROM v$instance"
    cs = DBUtil.getValue(db, sql)
    rs = cs.fetchone()
    if rs and rs[0]:
        metric.append(dict(index_id=f"2380001", value=str(rs[0])))


def get_sysstat(db, metric):
    sql = "select stat_id,value from v$sysstat"
    cs = DBUtil.getValue(db, sql)
    rs = cs.fetchall()
    for row in rs:
        stat_id = row[0]
        value = row[1]
        if float(stat_id) < 10:
            metric.append(dict(index_id=f"238100{stat_id}", value=str(value)))
        elif float(stat_id) < 100:
            metric.append(dict(index_id=f"23810{stat_id}", value=str(value)))
        else:
            metric.append(dict(index_id=f"2381{stat_id}", value=str(value)))


def get_session(db, metric):
    sql = "SELECT count(*) FROM v$session WHERE status = 'ACTIVE' AND TYPE != 'BACKGROUND';"
    sql2 = "SELECT count(*) FROM v$session WHERE status = 'ACTIVE'"
    sql3 = "SELECT count(*) FROM v$session WHERE TYPE != 'BACKGROUND';"
    sql4 = "SELECT count(*) FROM v$session;"
    cs = DBUtil.getValue(db, sql)
    rs = cs.fetchone()
    if rs and rs[0]:
        metric.append(dict(index_id=f"2380002", value=str(rs[0])))
    cs = DBUtil.getValue(db, sql2)
    rs = cs.fetchone()
    if rs and rs[0]:
        metric.append(dict(index_id=f"2380005", value=str(rs[0])))
    cs = DBUtil.getValue(db, sql3)
    rs = cs.fetchone()
    if rs and rs[0]:
        metric.append(dict(index_id=f"2380003", value=str(rs[0])))
    cs = DBUtil.getValue(db, sql4)
    rs = cs.fetchone()
    if rs and rs[0]:
        metric.append(dict(index_id=f"2380004", value=str(rs[0])))


def get_lock_sessions(db, metric):
    """获取等待会话信息"""
    sql = "SELECT IN_WAIT_SECS/1000/1000 FROM v$wait_chains;"
    cs = DBUtil.getValue(db, sql)
    rs = cs.fetchall()
    if rs:
        metric.append(dict(index_id="2380006", value=str(len(rs))))
        metric.append(dict(index_id="2380008", value=str(max([0 if not r[0] else r[0] for r in rs]))))
    else:
        metric.append(dict(index_id="2380006", value=str(0)))
        metric.append(dict(index_id="2380008", value=str(0)))

        
def server_main(st, metric):
    get_uptime(st, metric)
    get_sysstat(st, metric)
    get_session(st, metric)
    get_lock_sessions(st, metric)


if __name__ == '__main__':
    dbInfo = eval(sys.argv[1])
    metric = []
    db_flag = 0
    cur_time = datetime.now()
    st = DBUtil.get_shentong_env(exflag=3)
    metric.append(dict(index_id="1000102", value=str(round((datetime.now() - cur_time).microseconds/1000,0))))
    rs = []
    if st.conn:
        metric.append(dict(index_id="2380000", value="连接成功"))
        server_main(st, metric)
    else:
        metric.append(dict(index_id="2380000", value="连接失败"))
    lat_time = datetime.now()
    diff_ms = (lat_time - cur_time).microseconds
    metric.append(dict(index_id="1000101", value=str(round(diff_ms/1000,0))))
    print('{"results":' + json.dumps(metric, ensure_ascii=False) + '}')

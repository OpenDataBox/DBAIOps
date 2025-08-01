#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@文件    :metric_yashan.py
@说明    :崖山数据库metric指标
@时间    :2023/11/02 11:10:57
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
    sql = "select round(((sysdate - to_date(to_char(STARTUP_TIME,'yyyy-mm-dd hh24:mi:ss'),'yyyy-mm-dd hh24:mi:ss'))*24*60*60)) FROM v$instance"
    cs = DBUtil.getValue(db, sql)
    rs = cs.fetchone()
    if rs and rs[0]:
        metric.append(dict(index_id=f"2390001", value=str(rs[0])))


def get_sysstat(db, metric):
    sql = "select STATISTIC#,value from v$sysstat"
    cs = DBUtil.getValue(db, sql)
    rs = cs.fetchall()
    for row in rs:
        stat_id = row[0]
        value = row[1]
        if float(stat_id) < 10:
            metric.append(dict(index_id=f"239100{stat_id}", value=str(value)))
        elif float(stat_id) < 100:
            metric.append(dict(index_id=f"23910{stat_id}", value=str(value)))
        else:
            metric.append(dict(index_id=f"2391{stat_id}", value=str(value)))


def get_session(db, metric):
    sql = "SELECT count(*) FROM v$session WHERE status = 'ACTIVE' AND TYPE != 'BACKGROUND'"
    sql2 = "SELECT count(*) FROM v$session WHERE status = 'ACTIVE'"
    sql3 = "SELECT count(*) FROM v$session WHERE TYPE != 'BACKGROUND'"
    sql4 = "SELECT count(*) FROM v$session"
    cs = DBUtil.getValue(db, sql)
    rs = cs.fetchone()
    if rs and rs[0]:
        metric.append(dict(index_id=f"2390002", value=str(rs[0])))
    cs = DBUtil.getValue(db, sql2)
    rs = cs.fetchone()
    if rs and rs[0]:
        metric.append(dict(index_id=f"2390005", value=str(rs[0])))
    cs = DBUtil.getValue(db, sql3)
    rs = cs.fetchone()
    if rs and rs[0]:
        metric.append(dict(index_id=f"2390003", value=str(rs[0])))
    cs = DBUtil.getValue(db, sql4)
    rs = cs.fetchone()
    if rs and rs[0]:
        metric.append(dict(index_id=f"2390004", value=str(rs[0])))


def lock_session(db, metric):
    sql = "SELECT count(*) FROM v$session s WHERE lockwait IS NOT null"
    cs = DBUtil.getValue(db, sql)
    rs = cs.fetchone()
    if rs and rs[0]:
        metric.append(dict(index_id=f"2390006", value=str(rs[0])))
    else:
        metric.append(dict(index_id=f"2390006", value=str(0)))


def get_wait_event(db, metric):
    """获取等待事件信息"""
    sql = "SELECT rownum,event,TOTAL_WAITS,TIME_WAITED FROM V$SYSTEM_EVENT WHERE length(event) > 0 ORDER BY event"
    cs = DBUtil.getValue(db, sql)
    rs = cs.fetchall()
    for row in rs:
        stat_id = row[0]
        event = row[1]
        total_waits = row[2]
        total_waittime = row[3]
        if float(stat_id) < 10:
            metric.append(dict(index_id=f"239300{stat_id}", value=str(total_waits)))
            metric.append(dict(index_id=f"239500{stat_id}", value=str(total_waittime)))
        elif float(stat_id) < 100:
            metric.append(dict(index_id=f"23930{stat_id}", value=str(total_waits)))
            metric.append(dict(index_id=f"23950{stat_id}", value=str(total_waittime)))
        else:
            metric.append(dict(index_id=f"2393{stat_id}", value=str(total_waits)))
            metric.append(dict(index_id=f"2395{stat_id}", value=str(total_waittime)))


def get_process(db, metric):
    sql = "select count(1) from v$process"
    cs = DBUtil.getValue(db, sql)
    rs = cs.fetchone()
    if rs and rs[0]:
        metric.append(dict(index_id=f"2390007", value=str(rs[0])))

def get_plancase(db, metric):
    """采集解析次数"""
    sql = "SELECT sum(CREATE_TOTAL),sum(REUSE_TOTAL) FROM V$PLANCACHE"
    cs = DBUtil.getValue(db, sql)
    rs = cs.fetchone()
    if rs and rs[0]:
        metric.append(dict(index_id=f"2390019", value=str(rs[0])))
        metric.append(dict(index_id=f"2390020", value=str(rs[1])))


def get_rowlocks(db, metric):
    """采集行锁会话数"""
    sql = "SELECT Count(*) FROM V$LOCK  WHERE REQUEST = 'ROW'"
    cs = DBUtil.getValue(db, sql)
    rs = cs.fetchone()
    if rs and rs[0]:
        metric.append(dict(index_id=f"2390023", value=str(rs[0])))

def get_rowlock_maxtime(db, metric):
    """采集行锁会话数"""
    sql = """
    SELECT
        max(CASE when to_number(lockwait) > 0 THEN  round(((sysdate - to_date(to_char(EXEC_START_TIME,'yyyy-mm-dd hh24:mi:ss'),'yyyy-mm-dd hh24:mi:ss'))*24*60*60))
        ELSE 0
        END) AS wait_time
    FROM
        v$session s
    """
    cs = DBUtil.getValue(db, sql)
    rs = cs.fetchone()
    if rs and rs[0]:
        metric.append(dict(index_id=f"2390024", value=str(rs[0])))

def get_trans_maxtime(db, metric):
    """采集事务最大时间"""
    sql = """
     SELECT max(round(((sysdate - to_date(to_char(start_date,'yyyy-mm-dd hh24:mi:ss'),'yyyy-mm-dd hh24:mi:ss'))*24*60*60))) AS trans_time,count(*) total_trans FROM V$TRANSACTION
    """
    cs = DBUtil.getValue(db, sql)
    rs = cs.fetchone()
    if rs and rs[0]:
        metric.append(dict(index_id=f"2390025", value=str(rs[0])))
        metric.append(dict(index_id=f"2390026", value=str(rs[1])))


def get_idle_trans(db, metric):
    """采集空闲事务数"""
    sql = """
     SELECT
        count(*) total_trans
    FROM
        V$TRANSACTION
        WHERE Status='IDLE'
    """
    cs = DBUtil.getValue(db, sql)
    rs = cs.fetchone()
    if rs:
        metric.append(dict(index_id=f"2390027", value=str(rs[0])))
    else:
        metric.append(dict(index_id=f"2390027", value=str(0)))


def server_main(yas, metric):
    get_uptime(yas, metric)
    get_sysstat(yas, metric)
    get_session(yas, metric)
    get_wait_event(yas, metric)
    lock_session(yas, metric)
    get_process(yas, metric)
    get_plancase(yas, metric)
    get_rowlocks(yas, metric)
    get_rowlock_maxtime(yas, metric)
    get_trans_maxtime(yas, metric)
    get_idle_trans(yas, metric)

if __name__ == '__main__':
    dbInfo = eval(sys.argv[1])
    metric = []
    db_flag = 0
    cur_time = datetime.now()
    st = DBUtil.get_yashan_env(exflag=3)
    metric.append(dict(index_id="1000102", value=str(round((datetime.now() - cur_time).microseconds/1000,0))))
    rs = []
    if st.conn:
        metric.append(dict(index_id="2390000", value="连接成功"))
        server_main(st, metric)
    else:
        metric.append(dict(index_id="2390000", value="连接失败"))
    lat_time = datetime.now()
    diff_ms = (lat_time - cur_time).microseconds
    metric.append(dict(index_id="1000101", value=str(round(diff_ms/1000,0))))
    print('{"results":' + json.dumps(metric, ensure_ascii=False) + '}')

#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@文件    :metric_tidb.py
@说明    :TiDB 运行指标采集
@时间    :2024/05/11 09:19:18
@作者    :xxxx
@版本    :2.0.1
'''


import sys
from datetime import datetime
sys.path.append('/usr/software/knowl')
import json
import DBUtil


def cs(val, dt=False):
    if val is None:
        return ''
    else:
        if dt:
            return val.strftime('%Y-%m-%d %H:%M:%S')
        else:
            if isinstance(val, list):
                return val
            else:
                return str(val)

def get_cluster_health(tidb, metric):
    "获取TiDB集群运行指标"
    # 获取当前时间戳
    sql = "SELECT UNIX_TIMESTAMP();"
    cur = DBUtil.getValue(tidb, sql)
    rs = cur.fetchone()
    if rs:
        metric.append(dict(index_id="2480001", value=str(rs[0])))

    # 内存使用情况
    sql = """
    SELECT
        MEMORY_TOTAL ,
        MEMORY_LIMIT ,
        MEMORY_CURRENT ,
        MEMORY_MAX_USED,
        SESSION_KILL_LAST ,
        SESSION_KILL_TOTAL,
        GC_LAST,GC_TOTAL,
        DISK_USAGE,QUERY_FORCE_DISK
    FROM
        information_schema.MEMORY_USAGE;
    """
    # cur = DBUtil.getValue(tidb, sql)
    # rs = cur.fetchone()
    rs = []
    if rs:
        metric.append(dict(index_id="2480002", value=str(rs[0])))
        metric.append(dict(index_id="2480003", value=str(rs[1])))
        metric.append(dict(index_id="2480004", value=str(rs[2])))
        metric.append(dict(index_id="2480005", value=str(rs[3])))
        metric.append(dict(index_id="2480006", value=str(rs[4])))
        metric.append(dict(index_id="2480007", value=str(rs[5])))
        metric.append(dict(index_id="2480008", value=str(rs[6])))
        metric.append(dict(index_id="2480009", value=str(rs[7])))
        metric.append(dict(index_id="2480010", value=str(rs[8])))
        metric.append(dict(index_id="2480011", value=str(rs[9])))
    # 查看会话
    sql = """
    SELECT
        instance,COMMAND,count(*)
    FROM
        information_schema.CLUSTER_PROCESSLIST group by instance,COMMAND
    """
    cur = DBUtil.getValue(tidb, sql)
    rs = cur.fetchall()
    total_ses = 0
    total_active = 0
    total_vars = {}
    active_vars = {}
    if rs:
        for row in rs:
            inst_name = row[0]
            sess_stat = row[1]
            sess_num = float(row[2])
            total_ses += sess_num
            if inst_name in total_vars.keys():
                total_vars[inst_name] += sess_num
            else:
                total_vars[inst_name] = 1
            if sess_stat == 'Query':
                total_active += sess_num
                if inst_name in active_vars.keys():
                    active_vars[inst_name] += sess_num
                else:
                    active_vars[inst_name] = 1
    total_vars['total'] = total_ses
    active_vars['total'] = total_active
    for r in total_vars.keys():
        metric.append(dict(index_id="2480012", value=[dict(name=r,value=cs(total_vars[r]))]))
    for r in active_vars.keys():
        metric.append(dict(index_id="2480013", value=[dict(name=r,value=cs(active_vars[r]))]))
    # CPU使用情况
    sql = """
    select
        `instance` ,
        mode ,
        value
    from
        METRICS_SCHEMA.node_cpu_usage
    where
        time = (
        select
            time
        from
            METRICS_SCHEMA.node_cpu_usage
        order by
            1 desc
        limit 1);
    """
    cur = DBUtil.getValue(tidb, sql)
    rs = cur.fetchall()
    cpu_used = []
    for row in rs:
        inst_name = row[0]
        mode = row[1]
        value = row[2]
        if mode == 'idle':
            cpu_useage = 100-float(value)
            cpu_used.append(cpu_useage)
            metric.append(dict(index_id="2480014", value=[dict(name=inst_name,value=cs(cpu_useage))]))
    metric.append(dict(index_id="2480014", value=[dict(name='avg',value=cs(sum(cpu_used)/len(cpu_used)))]))
    metric.append(dict(index_id="2480014", value=[dict(name='max',value=cs(max(cpu_used)))]))
    metric.append(dict(index_id="2480014", value=[dict(name='min',value=cs(min(cpu_used)))]))
    # 磁盘剩余空间
    sql = """
    select
        `instance` ,
        mountpoint ,
        value,device
    from
        METRICS_SCHEMA.node_disk_available_size
    where
        time = (
        select
            time
        from
            METRICS_SCHEMA.node_disk_available_size
        order by
            1 desc
        limit 1);
    """
    cur = DBUtil.getValue(tidb, sql)
    rs = cur.fetchall()
    tmp_list = []
    for row in rs:
        inst_name = row[0]
        mount_point = row[1]
        value = round(float(row[2])/1024,2)
        metric.append(dict(index_id="1001017", value=[dict(name=inst_name + '-' + row[3],value=cs(value))]))
        if mount_point == '/':
            tmp_list.append(float(value))
            metric.append(dict(index_id="1001013", value=[dict(name=inst_name,value=cs(value))]))
    metric.append(dict(index_id="1001013", value=[dict(name='avg',value=cs(sum(tmp_list)/len(tmp_list)))]))
    metric.append(dict(index_id="1001013", value=[dict(name='max',value=cs(max(tmp_list)))]))
    metric.append(dict(index_id="1001013", value=[dict(name='min',value=cs(min(tmp_list)))]))
    # 磁盘总大小
    sql = """
    select
        `instance` ,
        mountpoint ,
        value,device
    from
        METRICS_SCHEMA.node_disk_size
    where
        time = (
        select
            time
        from
            METRICS_SCHEMA.node_disk_size
        order by
            1 desc
        limit 1);
    """
    cur = DBUtil.getValue(tidb, sql)
    rs = cur.fetchall()
    tmp_list = []
    for row in rs:
        inst_name = row[0]
        mount_point = row[1]
        value = round(float(row[2])/1024,2)
        metric.append(dict(index_id="1000303", value=[dict(name=inst_name + '-' + mount_point,value=cs(value))]))
        metric.append(dict(index_id="1001023", value=[dict(name=inst_name + '-' + row[3],value=cs(value))]))
        if mount_point == '/':
            tmp_list.append(float(value))
            metric.append(dict(index_id="1001012", value=[dict(name=inst_name,value=cs(value))]))
    metric.append(dict(index_id="1001012", value=[dict(name='avg',value=cs(sum(tmp_list)/len(tmp_list)))]))
    metric.append(dict(index_id="1001012", value=[dict(name='max',value=cs(max(tmp_list)))]))
    metric.append(dict(index_id="1001012", value=[dict(name='min',value=cs(min(tmp_list)))]))
    # 磁盘使用率
    sql = """
    select
        `instance` ,
        device  ,
        case when `value` is Null then 0 else `value` end as "value"
    from
        METRICS_SCHEMA.node_disk_usage
    where
        time = (
        select
            time
        from
            METRICS_SCHEMA.node_disk_usage
        order by
            1 desc
        limit 1);
    """
    cur = DBUtil.getValue(tidb, sql)
    rs = cur.fetchall()
    tmp_list = []
    for row in rs:
        inst_name = row[0]
        mount_point = row[1]
        value = round(float(row[2]),2)
        metric.append(dict(index_id="1001016", value=[dict(name=inst_name + '-' + mount_point,value=cs(value))]))
        metric.append(dict(index_id="1000300", value=[dict(name=inst_name + '-' + mount_point,value=cs(value))]))
        if 'root' in mount_point:
            tmp_list.append(float(value))
            metric.append(dict(index_id="1001005", value=[dict(name=inst_name,value=cs(cpu_useage))]))
    metric.append(dict(index_id="1001005", value=[dict(name='avg',value=cs(sum(tmp_list)/len(tmp_list)))]))
    metric.append(dict(index_id="1001005", value=[dict(name='max',value=cs(max(tmp_list)))]))
    metric.append(dict(index_id="1001005", value=[dict(name='min',value=cs(min(tmp_list)))]))
    # 磁盘读延迟
    sql = """
    select
        `instance` ,
        case when `value` is Null then 0 else `value` end as "value"
    from
        METRICS_SCHEMA.node_disk_read_latency
    where
        time = (
        select
            time
        from
            METRICS_SCHEMA.node_disk_read_latency
        order by
            1 desc
        limit 1);
    """
    cur = DBUtil.getValue(tidb, sql)
    rs = cur.fetchall()
    tmp_list = []
    total_latency = []
    for row in rs:
        inst_name = row[0]
        if float(row[1]) >=0:
            value = round(float(row[1]),2)
            total_latency.append(value)
            tmp_list.append(float(value))
            metric.append(dict(index_id="1001024", value=[dict(name=inst_name,value=cs(value))]))
    if tmp_list:
        metric.append(dict(index_id="1001024", value=[dict(name='avg',value=cs(sum(tmp_list)/len(tmp_list)))]))
        metric.append(dict(index_id="1001024", value=[dict(name='max',value=cs(max(tmp_list)))]))
        metric.append(dict(index_id="1001024", value=[dict(name='min',value=cs(min(tmp_list)))]))
    # 磁盘写延迟
    sql = """
    select
        `instance` ,
        case when `value` is Null then 0 else `value` end as "value"
    from
        METRICS_SCHEMA.node_disk_write_latency
    where
        time = (
        select
            time
        from
            METRICS_SCHEMA.node_disk_write_latency
        order by
            1 desc
        limit 1);
    """
    cur = DBUtil.getValue(tidb, sql)
    rs = cur.fetchall()
    tmp_list = []
    for row in rs:
        inst_name = row[0]
        if float(row[1]) >=0:
            value = round(float(row[1]),2)
            total_latency.append(value)
            tmp_list.append(float(value))
            metric.append(dict(index_id="1001025", value=[dict(name=inst_name,value=cs(value))]))
    if tmp_list:
        metric.append(dict(index_id="1001025", value=[dict(name='avg',value=cs(sum(tmp_list)/len(tmp_list)))]))
        metric.append(dict(index_id="1001025", value=[dict(name='max',value=cs(max(tmp_list)))]))
        metric.append(dict(index_id="1001025", value=[dict(name='min',value=cs(min(tmp_list)))]))
    metric.append(dict(index_id="1001006", value=[dict(name='avg',value=cs(sum(total_latency)/len(total_latency)))]))
    metric.append(dict(index_id="1001006", value=[dict(name='max',value=cs(max(total_latency)))]))
    metric.append(dict(index_id="1001006", value=[dict(name='min',value=cs(min(total_latency)))]))
    # 磁盘读IO KBPS
    sql = """
    select
        `instance` ,
        case when `value` is Null then 0 else `value` end as "value"
    from
        METRICS_SCHEMA.node_disk_throughput
    where
        time = (
        select
            time
        from
            METRICS_SCHEMA.node_disk_throughput
        order by
            1 desc
        limit 1);
    """
    cur = DBUtil.getValue(tidb, sql)
    rs = cur.fetchall()
    tmp_list = []
    for row in rs:
        inst_name = row[0]
        if float(row[1]) >=0:
            value = round(float(row[1])/1024,2)
            tmp_list.append(float(value))
            metric.append(dict(index_id="1001101", value=[dict(name=inst_name,value=cs(value))]))
    if tmp_list:
        metric.append(dict(index_id="1001101", value=[dict(name='avg',value=cs(sum(tmp_list)/len(tmp_list)))]))
        metric.append(dict(index_id="1001101", value=[dict(name='max',value=cs(max(tmp_list)))]))
        metric.append(dict(index_id="1001101", value=[dict(name='min',value=cs(min(tmp_list)))]))
    # 磁盘写IOPS
    sql = """
    select
        `instance` ,
        case when `value` is Null then 0 else `value` end as "value"
    from
        METRICS_SCHEMA.node_disk_iops
    where
        time = (
        select
            time
        from
            METRICS_SCHEMA.node_disk_iops
        order by
            1 desc
        limit 1);
    """
    cur = DBUtil.getValue(tidb, sql)
    rs = cur.fetchall()
    tmp_list = []
    for row in rs:
        inst_name = row[0]
        if float(row[1]) >=0:
            value = round(float(row[1]),2)
            tmp_list.append(float(value))
            metric.append(dict(index_id="1001100", value=[dict(name=inst_name,value=cs(value))]))
    if tmp_list:
        metric.append(dict(index_id="1001100", value=[dict(name='avg',value=cs(sum(tmp_list)/len(tmp_list)))]))
        metric.append(dict(index_id="1001100", value=[dict(name='max',value=cs(max(tmp_list)))]))
        metric.append(dict(index_id="1001100", value=[dict(name='min',value=cs(min(tmp_list)))]))
    # 内存使用率
    sql = """
    select
        `instance` ,
        case when `value` is Null then 0 else `value` end as "value"
    from
        METRICS_SCHEMA.node_memory_usage
    where
        time = (
        select
            time
        from
            METRICS_SCHEMA.node_memory_usage
        order by
            1 desc
        limit 1);
    """
    cur = DBUtil.getValue(tidb, sql)
    rs = cur.fetchall()
    tmp_list = []
    for row in rs:
        inst_name = row[0]
        if float(row[1]) >=0:
            value = round(float(row[1]),2)
            tmp_list.append(float(value))
            metric.append(dict(index_id="1001004", value=[dict(name=inst_name,value=cs(value))]))
    metric.append(dict(index_id="1001004", value=[dict(name='avg',value=cs(sum(tmp_list)/len(tmp_list)))]))
    metric.append(dict(index_id="1001004", value=[dict(name='max',value=cs(max(tmp_list)))]))
    metric.append(dict(index_id="1001004", value=[dict(name='min',value=cs(min(tmp_list)))]))
    # 内存剩余大小
    sql = """
    select
        `instance` ,
        case when `value` is Null then 0 else `value` end as "value"
    from
        METRICS_SCHEMA.node_memory_free
    where
        time = (
        select
            time
        from
            METRICS_SCHEMA.node_memory_free
        order by
            1 desc
        limit 1);
    """
    cur = DBUtil.getValue(tidb, sql)
    rs = cur.fetchall()
    tmp_list = []
    for row in rs:
        inst_name = row[0]
        if float(row[1]) >=0:
            value = round(float(row[1])/1024,2)
            tmp_list.append(float(value))
            metric.append(dict(index_id="1001007", value=[dict(name=inst_name,value=cs(value))]))
    metric.append(dict(index_id="1001007", value=[dict(name='avg',value=cs(sum(tmp_list)/len(tmp_list)))]))
    metric.append(dict(index_id="1001007", value=[dict(name='max',value=cs(max(tmp_list)))]))
    metric.append(dict(index_id="1001007", value=[dict(name='min',value=cs(min(tmp_list)))]))
    # swap 已使用大小
    sql = """
    select
        `instance` ,
        case when `value` is Null then 0 else `value` end as "value"
    from
        METRICS_SCHEMA.node_memory_swap_used
    where
        time = (
        select
            time
        from
            METRICS_SCHEMA.node_memory_swap_used
        order by
            1 desc
        limit 1);
    """
    cur = DBUtil.getValue(tidb, sql)
    rs = cur.fetchall()
    tmp_list = []
    for row in rs:
        inst_name = row[0]
        if float(row[1]) >=0:
            value = round(float(row[1])/1024,2)
            tmp_list.append(float(value))
            metric.append(dict(index_id="1001027", value=[dict(name=inst_name,value=cs(value))]))
    metric.append(dict(index_id="1001027", value=[dict(name='avg',value=cs(sum(tmp_list)/len(tmp_list)))]))
    metric.append(dict(index_id="1001027", value=[dict(name='max',value=cs(max(tmp_list)))]))
    metric.append(dict(index_id="1001027", value=[dict(name='min',value=cs(min(tmp_list)))]))
    # 网络接收丢包
    sql = """
    select
        `instance` ,
        case when `value` is Null then 0 else `value` end as "value"
    from
        METRICS_SCHEMA.node_network_in_drops
    where
        time = (
        select
            time
        from
            METRICS_SCHEMA.node_network_in_drops
        order by
            1 desc
        limit 1);
    """
    cur = DBUtil.getValue(tidb, sql)
    rs = cur.fetchall()
    tmp_list = []
    net_tmp = []
    for row in rs:
        if float(row[1]) >=0:
            value = round(float(row[1]),2)
            tmp_list.append(float(value))
            net_tmp.append(value)
            metric.append(dict(index_id="1001028", value=[dict(name=inst_name,value=cs(value))]))
    metric.append(dict(index_id="1001028", value=[dict(name='avg',value=cs(sum(tmp_list)/len(tmp_list)))]))
    metric.append(dict(index_id="1001028", value=[dict(name='max',value=cs(max(tmp_list)))]))
    metric.append(dict(index_id="1001028", value=[dict(name='min',value=cs(min(tmp_list)))]))
    # 网络发送丢包
    sql = """
    select
        `instance` ,
        case when `value` is Null then 0 else `value` end as "value"
    from
        METRICS_SCHEMA.node_network_out_drops
    where
        time = (
        select
            time
        from
            METRICS_SCHEMA.node_network_out_drops
        order by
            1 desc
        limit 1);
    """
    cur = DBUtil.getValue(tidb, sql)
    rs = cur.fetchall()
    tmp_list = []
    for row in rs:
        inst_name = row[0]
        if float(row[1]) >=0:
            value = round(float(row[1]),2)
            tmp_list.append(float(value))
            net_tmp.append(value)
            metric.append(dict(index_id="1001029", value=[dict(name=inst_name,value=cs(value))]))
    metric.append(dict(index_id="1001029", value=[dict(name='avg',value=cs(sum(tmp_list)/len(tmp_list)))]))
    metric.append(dict(index_id="1001029", value=[dict(name='max',value=cs(max(tmp_list)))]))
    metric.append(dict(index_id="1001029", value=[dict(name='min',value=cs(min(tmp_list)))]))
    metric.append(dict(index_id="1001020", value=[dict(name='avg',value=cs(sum(net_tmp)/len(net_tmp)))]))
    metric.append(dict(index_id="1001020", value=[dict(name='max',value=cs(max(net_tmp)))]))
    metric.append(dict(index_id="1001020", value=[dict(name='min',value=cs(min(net_tmp)))]))
    # 网络接收字节
    sql = """
    select
        `instance` ,
        case when `value` is Null then 0 else `value` end as "value"
    from
        METRICS_SCHEMA.node_network_in_traffic
    where
        time = (
        select
            time
        from
            METRICS_SCHEMA.node_network_in_traffic
        order by
            1 desc
        limit 1);
    """
    cur = DBUtil.getValue(tidb, sql)
    rs = cur.fetchall()
    tmp_list = []
    for row in rs:
        inst_name = row[0]
        if float(row[1]) >=0:
            value = round(float(row[1]),2)
            tmp_list.append(float(value))
            metric.append(dict(index_id="1000021", value=[dict(name=inst_name,value=cs(value))]))
    metric.append(dict(index_id="1000021", value=[dict(name='avg',value=cs(sum(tmp_list)/len(tmp_list)))]))
    metric.append(dict(index_id="1000021", value=[dict(name='max',value=cs(max(tmp_list)))]))
    metric.append(dict(index_id="1000021", value=[dict(name='min',value=cs(min(tmp_list)))]))
    # 网络发送字节
    sql = """
    select
        `instance` ,
        case when `value` is Null then 0 else `value` end as "value"
    from
        METRICS_SCHEMA.node_network_out_traffic
    where
        time = (
        select
            time
        from
            METRICS_SCHEMA.node_network_out_traffic
        order by
            1 desc
        limit 1);
    """
    cur = DBUtil.getValue(tidb, sql)
    rs = cur.fetchall()
    tmp_list = []
    for row in rs:
        inst_name = row[0]
        if float(row[1]) >=0:
            value = round(float(row[1]),2)
            tmp_list.append(float(value))
            metric.append(dict(index_id="1000022", value=[dict(name=inst_name,value=cs(value))]))
    metric.append(dict(index_id="1000022", value=[dict(name='avg',value=cs(sum(tmp_list)/len(tmp_list)))]))
    metric.append(dict(index_id="1000022", value=[dict(name='max',value=cs(max(tmp_list)))]))
    metric.append(dict(index_id="1000022", value=[dict(name='min',value=cs(min(tmp_list)))]))
    # 阻塞进程数
    sql = """
    select
        `instance` ,
        case when `value` is Null then 0 else `value` end as "value"
    from
        METRICS_SCHEMA.node_processes_blocked
    where
        time = (
        select
            time
        from
            METRICS_SCHEMA.node_processes_blocked
        order by
            1 desc
        limit 1);
    """
    cur = DBUtil.getValue(tidb, sql)
    rs = cur.fetchall()
    tmp_list = []
    for row in rs:
        inst_name = row[0]
        if float(row[1]) >=0:
            value = round(float(row[1]),2)
            tmp_list.append(float(value))
            metric.append(dict(index_id="1001030", value=[dict(name=inst_name,value=cs(value))]))
    metric.append(dict(index_id="1001030", value=[dict(name='avg',value=cs(sum(tmp_list)/len(tmp_list)))]))
    metric.append(dict(index_id="1001030", value=[dict(name='max',value=cs(max(tmp_list)))]))
    metric.append(dict(index_id="1001030", value=[dict(name='min',value=cs(min(tmp_list)))]))
    # TIDB QPS
    sql = """
    select
        `instance`,sum(case when `value` is Null then 0 else `value` end)
    from
        METRICS_SCHEMA.tidb_qps npb 
    where
        time = (
        select
            time
        from
            METRICS_SCHEMA.tidb_qps
        order by
            1 desc
        limit 1) group by `instance`
    """
    cur = DBUtil.getValue(tidb, sql)
    rs = cur.fetchall()
    tmp_list = []
    for row in rs:
        inst_name = row[0]
        if float(row[1]) >=0:
            value = round(float(row[1]),2)
            tmp_list.append(float(value))
            metric.append(dict(index_id="2480015", value=[dict(name=inst_name,value=cs(value))]))
    metric.append(dict(index_id="2480015", value=[dict(name='avg',value=cs(sum(tmp_list)/len(tmp_list)))]))
    metric.append(dict(index_id="2480015", value=[dict(name='max',value=cs(max(tmp_list)))]))
    metric.append(dict(index_id="2480015", value=[dict(name='min',value=cs(min(tmp_list)))]))
    # 事务
    sql = "SELECT count(*) FROM INFORMATION_SCHEMA.TIDB_TRX;"
    cur = DBUtil.getValue(tidb, sql)
    rs = cur.fetchone()
    if rs:
        metric.append(dict(index_id="2480016", value=cs(rs[0])))
    sql = "SELECT count(*) FROM INFORMATION_SCHEMA.TIDB_TRX where START_TIME >= DATE_SUB(now(),INTERVAL 1 hour);"
    cur = DBUtil.getValue(tidb, sql)
    rs = cur.fetchone()
    if rs:
        metric.append(dict(index_id="2480017", value=cs(rs[0])))
    sql = "SELECT  TIMESTAMPDIFF(SECOND, now(), start_time) FROM INFORMATION_SCHEMA.TIDB_TRX;"
    cur = DBUtil.getValue(tidb, sql)
    rs = cur.fetchone()
    if rs:
        metric.append(dict(index_id="2480018", value=cs(rs[0])))
    sql = "SELECT count(*) FROM INFORMATION_SCHEMA.TIDB_TRX where STATE = 'Running';"
    cur = DBUtil.getValue(tidb, sql)
    rs = cur.fetchone()
    if rs:
        metric.append(dict(index_id="2480020", value=cs(rs[0])))
    sql = "SELECT count(*) FROM INFORMATION_SCHEMA.TIDB_TRX where STATE = 'LockWaiting';"
    cur = DBUtil.getValue(tidb, sql)
    rs = cur.fetchone()
    if rs:
        metric.append(dict(index_id="2480019", value=cs(rs[0])))
    sql = "SELECT count(*) FROM INFORMATION_SCHEMA.TIDB_TRX where STATE = 'Committing';"
    cur = DBUtil.getValue(tidb, sql)
    rs = cur.fetchone()
    if rs:
        metric.append(dict(index_id="2480021", value=cs(rs[0])))
    sql = "SELECT count(*) FROM INFORMATION_SCHEMA.TIDB_TRX where STATE = 'RollingBack';"
    cur = DBUtil.getValue(tidb, sql)
    rs = cur.fetchone()
    if rs:
        metric.append(dict(index_id="2480022", value=cs(rs[0])))
    # DDL 95分位时间
    sql = """
    select
        `instance`,sum(case when `value` is Null then 0 else `value` end)
    from
        METRICS_SCHEMA.tidb_ddl_duration npb 
    where
        time = (
        select
            time
        from
            METRICS_SCHEMA.tidb_ddl_duration
        order by
            1 desc
        limit 1) group by `instance`
    """
    cur = DBUtil.getValue(tidb, sql)
    rs = cur.fetchall()
    tmp_list = []
    for row in rs:
        inst_name = row[0]
        if float(row[1]) >=0:
            value = round(float(row[1]),2)
            tmp_list.append(float(value))
            metric.append(dict(index_id="2480023", value=[dict(name=inst_name,value=cs(value))]))
    metric.append(dict(index_id="2480023", value=[dict(name='avg',value=cs(sum(tmp_list)/len(tmp_list)))]))
    metric.append(dict(index_id="2480023", value=[dict(name='max',value=cs(max(tmp_list)))]))
    metric.append(dict(index_id="2480023", value=[dict(name='min',value=cs(min(tmp_list)))]))
    # TIDB编译 95分位时间
    sql = """
    select
        `instance`,sum(case when `value` is Null then 0 else `value` end)
    from
        METRICS_SCHEMA.tidb_ddl_duration npb 
    where
        time = (
        select
            time
        from
            METRICS_SCHEMA.tidb_ddl_duration
        order by
            1 desc
        limit 1) group by `instance`
    """
    cur = DBUtil.getValue(tidb, sql)
    rs = cur.fetchall()
    tmp_list = []
    for row in rs:
        inst_name = row[0]
        if float(row[1]) >=0:
            value = round(float(row[1]),2)
            tmp_list.append(float(value))
            metric.append(dict(index_id="2480024", value=[dict(name=inst_name,value=cs(value))]))
    metric.append(dict(index_id="2480024", value=[dict(name='avg',value=cs(sum(tmp_list)/len(tmp_list)))]))
    metric.append(dict(index_id="2480024", value=[dict(name='max',value=cs(max(tmp_list)))]))
    metric.append(dict(index_id="2480024", value=[dict(name='min',value=cs(min(tmp_list)))]))
    # TSO等待时间
    sql = """
    select
        `instance`,sum(case when `value` is Null then 0 else `value` end)
    from
        METRICS_SCHEMA.pd_tso_wait_total_time npb 
    where
        time = (
        select
            time
        from
            METRICS_SCHEMA.pd_tso_wait_total_time
        order by
            1 desc
        limit 1) group by `instance`
    """
    cur = DBUtil.getValue(tidb, sql)
    rs = cur.fetchall()
    tmp_list = []
    for row in rs:
        inst_name = row[0]
        if float(row[1]) >=0:
            value = round(float(row[1]),2)
            tmp_list.append(float(value))
            metric.append(dict(index_id="2480025", value=[dict(name=inst_name,value=cs(value))]))
    metric.append(dict(index_id="2480025", value=[dict(name='avg',value=cs(sum(tmp_list)/len(tmp_list)))]))
    metric.append(dict(index_id="2480025", value=[dict(name='max',value=cs(max(tmp_list)))]))
    metric.append(dict(index_id="2480025", value=[dict(name='min',value=cs(min(tmp_list)))]))
    # 本地事务等待时间
    sql = """
    select
        `instance`,sum(case when `value` is Null then 0 else `value` end)
    from
        METRICS_SCHEMA.tidb_transaction_local_latch_wait_total_time npb 
    where
        time = (
        select
            time
        from
            METRICS_SCHEMA.tidb_transaction_local_latch_wait_total_time
        order by
            1 desc
        limit 1) group by `instance`
    """
    cur = DBUtil.getValue(tidb, sql)
    rs = cur.fetchall()
    tmp_list = []
    for row in rs:
        inst_name = row[0]
        if float(row[1]) >=0:
            value = round(float(row[1]),2)
            tmp_list.append(float(value))
            metric.append(dict(index_id="2480026", value=[dict(name=inst_name,value=cs(value))]))
    metric.append(dict(index_id="2480026", value=[dict(name='avg',value=cs(sum(tmp_list)/len(tmp_list)))]))
    metric.append(dict(index_id="2480026", value=[dict(name='max',value=cs(max(tmp_list)))]))
    metric.append(dict(index_id="2480026", value=[dict(name='min',value=cs(min(tmp_list)))]))
    # 每秒命令执行次数
    sql = """
    select
        `type`,sum(case when `value` is Null then 0 else `value` end)
    from
        METRICS_SCHEMA.tidb_ops_statement npb 
    where
        time = (
        select
            time
        from
            METRICS_SCHEMA.tidb_ops_statement
        order by
            1 desc
        limit 1) group by `type`
    """
    cur = DBUtil.getValue(tidb, sql)
    rs = cur.fetchall()
    tmp_list = []
    for row in rs:
        inst_name = row[0]
        if float(row[1]) >=0:
            value = round(float(row[1]),2)
            tmp_list.append(float(value))
            metric.append(dict(index_id="2480026", value=[dict(name=inst_name,value=cs(value))]))
    metric.append(dict(index_id="2480026", value=[dict(name='avg',value=cs(sum(tmp_list)/len(tmp_list)))]))
    metric.append(dict(index_id="2480026", value=[dict(name='max',value=cs(max(tmp_list)))]))
    metric.append(dict(index_id="2480026", value=[dict(name='min',value=cs(min(tmp_list)))]))
    # KV写入大小
    sql = """
    select
        `instance`,sum(case when `value` is Null then 0 else `value` end)
    from
        METRICS_SCHEMA.tidb_kv_write_total_size npb 
    where
        time = (
        select
            time
        from
            METRICS_SCHEMA.tidb_kv_write_total_size
        order by
            1 desc
        limit 1) group by `instance`
    """
    cur = DBUtil.getValue(tidb, sql)
    rs = cur.fetchall()
    tmp_list = []
    for row in rs:
        inst_name = row[0]
        if float(row[1]) >=0:
            value = round(float(row[1]),2)
            tmp_list.append(float(value))
            metric.append(dict(index_id="2480027", value=[dict(name=inst_name,value=cs(value))]))
    metric.append(dict(index_id="2480027", value=[dict(name='avg',value=cs(sum(tmp_list)/len(tmp_list)))]))
    metric.append(dict(index_id="2480027", value=[dict(name='max',value=cs(max(tmp_list)))]))
    metric.append(dict(index_id="2480027", value=[dict(name='min',value=cs(min(tmp_list)))]))
    # 死锁数
    sql = """
    select
        `instance`,sum(case when `value` is Null then 0 else `value` end)
    from
        METRICS_SCHEMA.tikv_lock_manager_deadlock_detect_total_count npb 
    where
        time = (
        select
            time
        from
            METRICS_SCHEMA.tikv_lock_manager_deadlock_detect_total_count
        order by
            1 desc
        limit 1) group by `instance`
    """
    cur = DBUtil.getValue(tidb, sql)
    rs = cur.fetchall()
    tmp_list = []
    if rs:
        for row in rs:
            inst_name = row[0]
            if float(row[1]) >=0:
                value = round(float(row[1]),2)
                tmp_list.append(float(value))
                metric.append(dict(index_id="2480028", value=[dict(name=inst_name,value=cs(value))]))
    else:
        tmp_list.append(0)
    metric.append(dict(index_id="2480028", value=[dict(name='avg',value=cs(sum(tmp_list)/len(tmp_list)))]))
    metric.append(dict(index_id="2480028", value=[dict(name='max',value=cs(max(tmp_list)))]))
    metric.append(dict(index_id="2480028", value=[dict(name='min',value=cs(min(tmp_list)))]))


if __name__=="__main__":
    metric = []
    cur_time = datetime.now()
    st = DBUtil.get_tidb_env(exflag=3)
    metric.append(dict(index_id="1000102", value=str(round((datetime.now() - cur_time).microseconds/1024,0))))
    rs = []
    if st.conn:
        metric.append(dict(index_id="2480000", value="连接成功"))
        get_cluster_health(st, metric)
    else:
        metric.append(dict(index_id="2480000", value="连接失败"))
    lat_time = datetime.now()
    diff_ms = (lat_time - cur_time).microseconds
    metric.append(dict(index_id="1000101", value=str(round(diff_ms/1024,0))))
    print('{"results":' + json.dumps(metric, ensure_ascii=False) + '}')
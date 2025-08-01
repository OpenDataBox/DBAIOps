#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@文件    :cib_tidb.py
@说明    :TiDB基本信息采集
@时间    :2024/05/11 09:19:08
@作者    :xxxx
@版本    :2.0.1
'''

import sys
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
            return str(val)


def get_cluster_basic(tidb, metric):
    "获取集群基本信息"
    sql = "select * from information_schema.cluster_info"
    cur = DBUtil.getValue(tidb, sql)
    rs = cur.fetchall()
    vals = []
    temp = []
    for row in rs:
        if row[0] not in temp:
            vals.append(dict(name=row[0] + '_version', value=row[3]))
            vals.append(dict(name=row[0] + '_start_time', value=row[5]))
            vals.append(dict(name=row[0] + '_uptime', value=row[6]))
            temp.append(row[0])
    # 集群硬件配置
    sql3 = "select distinct type, name,value from information_schema.CLUSTER_HARDWARE ndi where ndi.DEVICE_TYPE = 'cpu';"
    cur3 = DBUtil.getValue(tidb, sql3)
    rs3 = cur3.fetchall()
    for row in rs3:
        vals.append(dict(name=row[0] + '_' + row[1], value=row[2]))
    # 集群配置
    sql2 = "select distinct type,t.key,t.value from information_schema.cluster_config t where t.key in ('log.slow-query-file','log.file.filename');"
    cur2 = DBUtil.getValue(tidb, sql2)
    rs2 = cur2.fetchall()
    for row in rs2:
        vals.append(dict(name=row[0] + '_' + row[1].replace(".","_"), value=row[2]))
    metric.append(dict(index_id="2470001", value=vals))


def get_cluster_info(tidb, metric):
    "获取集群信息"
    sql = "select * from information_schema.cluster_info"
    cur = DBUtil.getValue(tidb, sql)
    rs = cur.fetchall()
    vals = []
    vals.append(dict(c1='节点类型', c2='实例地址', c3='API地址', c4='版本号', c5='Commit Hash', c6='启动时间', c7='运行时间', c8='服务器 ID', c9=None, c10=None))
    for row in rs:
        vals.append(dict(c1=row[0], c2=cs(row[1]), c3=cs(row[2]), c4=cs(row[3]), c5=cs(row[4]), c6=cs(row), c7=cs(row[6]), c8=cs(row[7]), c9=None, c10=None))
    metric.append(dict(index_id="2470002", content=vals))


def get_cluster_config(tidb, metric):
    "获取集群参数配置"
    sql = "select distinct `KEY`,VALUE from information_schema.cluster_config"
    cur = DBUtil.getValue(tidb, sql)
    rs = cur.fetchall()
    vals = []
    for row in rs:
        vals.append(dict(name=row[0], value=cs(row[1])))
    metric.append(dict(index_id="2470003", value=vals))


def get_cluster_variables(tidb, metric):
    "获取集群参数配置"
    # sql = "select variable_name,SUBSTRING(current_value,1,3500) from information_schema.variables_info"
    sql = "select variable_name,SUBSTRING(VARIABLE_VALUE ,1,3500) from information_schema.SESSION_VARIABLES" # 7以下版本
    cur = DBUtil.getValue(tidb, sql)
    rs = cur.fetchall()
    vals = []
    for row in rs:
        vals.append(dict(name=row[0], value=cs(row[1])))
    metric.append(dict(index_id="2470004", value=vals))


if __name__=="__main__":
    tidb = DBUtil.get_tidb_env()
    metric = []
    get_cluster_basic(tidb, metric)
    get_cluster_info(tidb, metric)
    get_cluster_config(tidb, metric)
    get_cluster_variables(tidb, metric)
    print('{"cib":' + json.dumps(metric) + '}')
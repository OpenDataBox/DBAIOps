#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@文件    :cib_db2.py
@说明    :DB2 基本信息采集
@时间    :2024/05/14 11:13:16
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

def get_db2_basic(db2, metric):
    vals = []
    sql = "SELECT last_backup,db_path from table(MON_GET_DATABASE(-2))"
    rs = DBUtil.getValue(db2, sql)
    for r in rs:
        for key, value in r.items():
            vals.append(dict(name=key, value=cs(value)))
    sql = "SELECT * FROM TABLE (MON_GET_INSTANCE(-2));"
    rs = DBUtil.getValue(db2, sql)
    for r in rs:
        for key, value in r.items():
            vals.append(dict(name=key, value=cs(value)))
    metric.append(dict(index_id="2490001", value=vals))


def get_db2_dbcfg(db2, metric):
    "数据库配置参数信息"
    sql = "select * from SYSIBMADM.DBCFG;"
    rs = DBUtil.getValue(db2, sql)
    vals = []
    vals.append(dict(c1='参数名称', c2='当前值',c3='参数当前值的特定信息', c4='磁盘上的参数值', c5='参数延迟值', c6='参数值类型', c7='数据库分区号', c8='数据库成员', c9=None, c10=None))
    for row in rs:
        vals.append(dict(c1=row['NAME'], c2=cs(row['VALUE']), c3=cs(row['VALUE_FLAGS']), c4=cs(row['DEFERRED_VALUE']), c5=cs(row['DEFERRED_VALUE_FLAGS']), c6=cs(row['DATATYPE']), c7=cs(row['DBPARTITIONNUM']), c8=cs(row['MEMBER']), c9=None, c10=None))
    metric.append(dict(index_id="2490002", content=vals))


def get_db2_dbmcfg(db2, metric):
    "数据库管理器配置参数信息"
    sql = "select * from SYSIBMADM.DBMCFG;"
    rs = DBUtil.getValue(db2, sql)
    vals = []
    vals.append(dict(c1='参数名称', c2='当前值',c3='参数当前值的特定信息', c4='磁盘上的参数值', c5='参数延迟值', c6='参数值类型', c7=None, c8=None, c9=None, c10=None))
    for row in rs:
        vals.append(dict(c1=row['NAME'], c2=cs(row['VALUE']), c3=cs(row['VALUE_FLAGS']), c4=cs(row['DEFERRED_VALUE']), c5=cs(row['DEFERRED_VALUE_FLAGS']), c6=cs(row['DATATYPE']), c7=None, c8=None, c9=None, c10=None))
    metric.append(dict(index_id="2490003", content=vals))
    

def get_db2_variables(db2, metric):
    sql = "SELECT name ,value FROM SYSIBMADM.DBCFG;"
    rs = DBUtil.getValue(db2, sql)
    vals = []
    for row in rs:
        vals.append(dict(name=row['NAME'], value=cs(row['VALUE'])))
    metric.append(dict(index_id="2490004", value=vals))


if __name__=="__main__":
    db2 = DBUtil.get_db2_env()
    metric = []
    get_db2_basic(db2, metric)
    get_db2_dbcfg(db2, metric)
    get_db2_dbmcfg(db2, metric)
    get_db2_variables(db2, metric)
    print('{"cib":' + json.dumps(metric) + '}')
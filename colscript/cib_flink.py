#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@文件    :cib_flink.py
@说明    :Flink 基本信息采集
@时间    :2022/04/06 15:11:49
@作者    :xxxx
@版本    :2.0.1
'''

import sys
import json
import time
sys.path.append('/usr/software/knowl')
import DBUtil

def format_timestamp(timestamp):
    timeStamp_sec = float(timestamp/1000) 
    timeArray = time.localtime(timeStamp_sec) 
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray) 
    return otherStyleTime


def cib_main(flink_clt,metric):
    """Flink Cib 采集入口

    Args:
        flink_clt (_type_): _description_
        metric (_type_): _description_
    """

    # 获取作业管理器配置信息
    response, out = flink_clt.getJobManagerConfig()
    var = []
    if response.status == 200:
        for row in out:
            var.append(dict(name=row['key'], value=row['value']))
        metric.append(dict(index_id='4990002', value=var))

    # 获取系统配置信息
    var2 = []
    response, out = flink_clt.getSystemSonfig()
    if response.status == 200:
        var2.append(dict(name='refresh-interval', value=out['refresh-interval']))
        var2.append(dict(name='timezone-name', value=out['timezone-name']))
        var2.append(dict(name='timezone-offset', value=out['timezone-offset']))
        var2.append(dict(name='flink-version', value=out['flink-version']))
    response, out = flink_clt.getSystemOverview()
    if response.status == 200:
        var2.append(dict(name='flink-commit', value=out['flink-commit']))
        var2.append(dict(name='taskmanagers', value=out['taskmanagers']))
        var2.append(dict(name='slots-total', value=out['slots-total']))
    metric.append(dict(index_id='4990001', value=var2))

    # 任务管理器信息
    response,out = flink_clt.getTaskManager()
    vals = []
    vals.append(
            dict(c1='ID', c2='路径', c3='数据端口', c4='JMX端口', c5='最近一次心跳时间', c6='Slot总数', c7='可用SLOT数', c8=None, c9=None, c10=None))
    if response.status == 200:
        for row in out['taskmanagers']:
            otherStyleTime = format_timestamp(row['timeSinceLastHeartbeat'])
            vals.append(dict(c1=row['id'], c2=row['path'], c3=row['dataPort'], c4=row['jmxPort'], c5=otherStyleTime, c6=row['slotsNumber'], c7=row['freeSlots'], c8=None, c9=None, c10=None))
    metric.append(dict(index_id="4990003", content=vals))
    
    # 作业管理器信息
    response,out = flink_clt.getJobStatus()
    vals = []
    vals.append(
            dict(c1='ID', c2='名称', c3='状态', c4='开始时间', c5='结束时间', c6='持续时间(秒)', c7='最近修改时间', c8=None, c9=None, c10=None))
    if response.status == 200:
        for row in out['jobs']:
            end_time = row['end-time']
            if end_time != -1:
                end_time = format_timestamp(end_time)
            vals.append(dict(c1=row['jid'], c2=row['name'], c3=row['state'], c4=str(format_timestamp(row['start-time'])), c5=str(end_time), c6=str(round(row['duration']/1000,2)), c7=str(format_timestamp(row['last-modification'])), c8=None, c9=None, c10=None))
    metric.append(dict(index_id="4990004", content=vals))

if __name__ == '__main__':
    objinfo = eval(sys.argv[1])
    metric = []
    flink_ctl = DBUtil.get_flink_client(objinfo)
    cib_main(flink_ctl,metric)
    print('{"cib":' + json.dumps(metric) + '}')
        
#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@文件    :metric_goldendb.py
@说明    :
@时间    :2024/06/18 09:27:42
@作者    :xxxx
@版本    :2.0.1
'''


import sys
import base64
import json
import numpy
import time
import requests
from datetime import datetime
from elasticsearch import Elasticsearch
sys.path.append('/usr/software/knowl')
import DBUtil
from JavaRsa import decrypt
from DBAIOps_logger import Logger

import warnings
warnings.filterwarnings("ignore")


log = Logger('gdb_collect.log')



def tuple2(arr, f=False):
    s = ''
    for v in arr:
        if v is None:
            v = 'null'
        v = str(v).replace("'", "''")
        if s:
            if f:
                s += ",'%s'" % str(v)
            else:
                s += ",%s" % str(v)
        else:
            if f:
                s = "'%s'" % str(v)
            else:
                s = "%s" % str(v)
    if s and f:
        s = '(%s)' % s
    return s


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


def is_number(s):
    try:
        float(s)  # 尝试将字符串转换为浮点数
        return True
    except ValueError:
        return False


def cs2(val, dt=False):
    if val is None:
        return ''
    else:
        if dt:
            return val.strftime('%Y-%m-%d %H:%M:%S')
        elif is_number(val):
            return float(val)
        else:
            return str(val)


def insert_if_not_exists(targetId, index_id, value):
    if targetId:
        if targetId[:4] == '2205':
            index_type = '285'
        else:
            index_type = '202'
        if global_metric:
            is_exist = False
            for item in global_metric:
                if item["targetId"] == targetId:
                    is_exist = True
                    if str(index_id)[:3] == '100':
                        index_type = '100'
                    elif str(index_id)[:3] == '300':
                        index_type = '300'
                    item["results"].append({"index_id": index_type + str(str(index_id)[3:]), "value": cs(value)})
                    break # 找到了就退出
            if not is_exist:
                if str(index_id)[:3] == '100':
                    new_entry = {
                        "targetId": targetId,
                        "indexType": index_type,
                        "results": [{"index_id": str(index_id), "value": cs(value)}]
                    }
                elif str(index_id)[:3] == '300':
                    new_entry = {
                        "targetId": targetId,
                        "indexType": index_type,
                        "results": [{"index_id": str(index_id), "value": cs(value)}]
                    }
                else:
                    new_entry = {
                        "targetId": targetId,
                        "indexType": index_type,
                        "results": [{"index_id": index_type + str(str(index_id)[3:]), "value": cs(value)}]
                    }
                global_metric.append(new_entry)
        else:
            if str(index_id)[:3] == '100':
                new_entry = {
                    "targetId": targetId,
                    "indexType": index_type,
                    "results": [{"index_id": str(index_id), "value": cs(value)}]
                }
            elif str(index_id)[:3] == '300':
                new_entry = {
                    "targetId": targetId,
                    "indexType": index_type,
                    "results": [{"index_id": str(index_id), "value": cs(value)}]
                }
            else:
                new_entry = {
                    "targetId": targetId,
                    "indexType": index_type,
                    "results": [{"index_id": index_type + str(str(index_id)[3:]), "value": cs(value)}]
                }
            global_metric.append(new_entry)

def get_uid_by_ip(node_ip, port=None,p_ip=None,p_port=None):
    if port:
        sql = f"select uid from mgt_system ms where ip = '{node_ip}' and port='{port}' and use_flag and subuid is not null"
    else:
        sql = f"select uid from mgt_system ms where ip = '{node_ip}' and use_flag and subuid is not null"
    cursor = DBUtil.getValue(pg, sql)
    result = cursor.fetchone()
    uid = None
    if result is not None:
        uid = result[0]
    else:
        if p_ip and p_port:
            sql = f"""
            select uid from mgt_system ms 
            where ip = '{node_ip}' and use_flag 
            and subuid in (select uid from mgt_system where ip = '{p_ip}' and port='{p_port}' and use_flag and subuid is not null)
            and port != '{p_port}'
            union
            select uid from mgt_system ms 
            where ip = '{node_ip}' and use_flag 
            and subuid in (select subuid from mgt_system where ip = '{p_ip}' and port='{p_port}' and use_flag and subuid is not null)
            and port='{port}'
            """
            cursor = DBUtil.getValue(pg, sql)
            result = cursor.fetchone()
            if result is not None:
                uid = result[0]
    return uid


def get_osinfo(host, user, base64_pwd, port):
    """获取OS相关信息"""
    
    url = f"https://{host}:{port}/open_api/insight/external/collect/searchHostCollectData?collectIdList=213"
    payload = {}
    headers = {
    'Cookie': 'SESSION=NWQ4ZTdlNjUtZWEwZi00ODZlLTk2ODMtNGRiZjFkYmExMTQw; JSESSIONID=5EF3A199858F08059A8E37402C2432F9',
    'username': user,
    'password': base64_pwd,
    'Content-Type': 'application/json'
    }
    proxies = {
            "http": None,
            "https": None,
            }
    response = requests.get(url, headers=headers, data=payload, verify=False, timeout=5, proxies=proxies)
    if response and response.status_code == 200:
        msg = response.json()
        data = msg["data"]
        host_data = data['collectDataList']
        ioutil = []
        cpu = []
        mem = []
        disk = []
        for w in host_data:
            hlist = w['dataList']
            for r in hlist:
                ip = r['hostIp']
                totalCpu = r['totalCpu']
                hostCpu = r['hostCpu']
                hostMem = r['hostMem']
                hostDisk = r['hostDisk']
                hostIoUtil = r['hostIoUtil']
                ioutil.append(hostIoUtil)
                cpu.append(hostCpu)
                mem.append(hostMem)
                disk.append(hostDisk)
                # uid = get_uid_by_ip(ip)
                # insert_if_not_exists(uid, 1000200, cs(totalCpu))
                # insert_if_not_exists(uid, 1001102, cs(hostIoUtil))
                # insert_if_not_exists(uid, 1001003, cs(hostCpu))
                # insert_if_not_exists(uid, 1001004, cs(hostMem))
                # insert_if_not_exists(uid, 1000320, cs(hostDisk))
                # insert_if_not_exists(uid, 1000321, cs(hostDisk))
                # insert_if_not_exists(uid, 1000322, cs(hostDisk))
                # insert_if_not_exists(uid, 1000300, cs(hostDisk))
                insert_if_not_exists(targetId, 1000200, [dict(name=ip,value=cs(totalCpu))])
                insert_if_not_exists(targetId, 1001102, [dict(name=ip,value=cs(hostIoUtil))])
                insert_if_not_exists(targetId, 1001003, [dict(name=ip,value=cs(hostCpu))])
                insert_if_not_exists(targetId, 1001004, [dict(name=ip,value=cs(hostMem))])
                insert_if_not_exists(targetId, 1000320, [dict(name=ip,value=cs(hostDisk))])
                insert_if_not_exists(targetId, 1000321, [dict(name=ip,value=cs(hostDisk))])
                insert_if_not_exists(targetId, 1000322, [dict(name=ip,value=cs(hostDisk))])
                # insert_if_not_exists(targetId, 1000300, [dict(name=ip,value=cs(hostDisk))])
                # 磁盘信息
                diskInfo = r['diskInfos']
                ddelay = []
                dreadKbSzie = []
                dusedRatio = []
                dwriteCount = []
                dreadCount = []
                dwriteKbSzie = []
                for d in diskInfo:
                    diskName = d['diskName']
                    delay = d['delay']
                    readKbSzie = d['readKbSize']
                    usedRatio = d['usedRatio']
                    writeCount = d['writeCount']
                    readCount = d['readCount']
                    writeKbSzie = d['writeKbSize']
                    ddelay.append(cs2(delay))
                    dreadKbSzie.append(cs2(readKbSzie))
                    dusedRatio.append(cs2(usedRatio))
                    dwriteCount.append(cs2(writeCount))
                    dreadCount.append(cs2(readCount))
                    dwriteKbSzie.append(cs2(writeKbSzie))
                    # insert_if_not_exists(uid, 1001107, [dict(name=diskName,value=cs(delay))])
                    # insert_if_not_exists(uid, 1001108, [dict(name=diskName,value=cs(readKbSzie))])
                    # insert_if_not_exists(uid, 1001109, [dict(name=diskName,value=cs(usedRatio))])
                    # insert_if_not_exists(uid, 1001110, [dict(name=diskName,value=cs(writeCount))])
                    # insert_if_not_exists(uid, 1001111, [dict(name=diskName,value=cs(readCount))])
                    # insert_if_not_exists(uid, 1001112, [dict(name=diskName,value=cs(writeKbSzie))])

                # 网络信息
                netInfo = r['hostNetCardInfos']
                in_lost = []
                in_rate = []
                in_size = []
                out_lost = []
                out_rate = []
                out_size = []
                # 1001209	所有网络接口总流量
                for n in netInfo:
                    netCardName = n['netCardName']
                    netInputLostRate = n['netInputLostRate']
                    netInputRate = n['netInputRate']  # 1000021	网络接收流量，字节
                    netInputSize = n['netInputSize']  # kb
                    netOutputLostRate = n['netOutputLostRate']
                    netOutputRate = n['netOutputRate'] # 1000022	网络发送流量，字节
                    netOutputSize = n['netOutputSize'] # kb
                    in_lost.append(cs2(netInputLostRate))
                    in_rate.append(cs2(netInputRate))
                    in_size.append(cs2(netInputSize))
                    out_lost.append(cs2(netOutputLostRate))
                    out_rate.append(cs2(netOutputRate))
                    out_size.append(cs2(netOutputSize))
                    # insert_if_not_exists(uid, 1001103, [dict(name=netCardName,value=cs(netInputLostRate))])
                    # insert_if_not_exists(uid, 1000021, [dict(name=netCardName,value=cs(netInputRate*1024))])
                    # insert_if_not_exists(uid, 1001104, [dict(name=netCardName,value=cs(netInputSize))])
                    # insert_if_not_exists(uid, 1001105, [dict(name=netCardName,value=cs(netOutputLostRate))])
                    # insert_if_not_exists(uid, 1000022, [dict(name=netCardName,value=cs(netOutputRate*1024))])
                    # insert_if_not_exists(uid, 1001106, [dict(name=netCardName,value=cs(netOutputSize))])
        
        # 网络
        insert_if_not_exists(targetId, 1001103, [dict(name="max",value=cs(max(in_lost)))])
        insert_if_not_exists(targetId, 1001103, [dict(name="min",value=cs(min(in_lost)))])
        insert_if_not_exists(targetId, 1001103, [dict(name="total",value=cs(sum(in_lost)))])
        insert_if_not_exists(targetId, 1001103, [dict(name="avg",value=cs(round(sum(in_lost)/len(in_lost),2)))])
        insert_if_not_exists(targetId, 1000021, [dict(name="max",value=cs(max(in_rate)))])
        insert_if_not_exists(targetId, 1000021, [dict(name="min",value=cs(min(in_rate)))])
        insert_if_not_exists(targetId, 1000021, [dict(name="total",value=cs(sum(in_rate)))])
        insert_if_not_exists(targetId, 1000021, [dict(name="avg",value=cs(round(sum(in_rate)/len(in_rate),2)))])
        insert_if_not_exists(targetId, 1001104, [dict(name="max",value=cs(max(in_size)))])
        insert_if_not_exists(targetId, 1001104, [dict(name="min",value=cs(min(in_size)))])
        insert_if_not_exists(targetId, 1001104, [dict(name="total",value=cs(sum(in_size)))])
        insert_if_not_exists(targetId, 1001104, [dict(name="avg",value=cs(round(sum(in_size)/len(in_size),2)))])
        insert_if_not_exists(targetId, 1001105, [dict(name="max",value=cs(max(out_lost)))])
        insert_if_not_exists(targetId, 1001105, [dict(name="min",value=cs(min(out_lost)))])
        insert_if_not_exists(targetId, 1001105, [dict(name="total",value=cs(sum(out_lost)))])
        insert_if_not_exists(targetId, 1001105, [dict(name="avg",value=cs(round(sum(out_lost)/len(out_lost),2)))])
        insert_if_not_exists(targetId, 1000022, [dict(name="max",value=cs(max(out_rate)))])
        insert_if_not_exists(targetId, 1000022, [dict(name="min",value=cs(min(out_rate)))])
        insert_if_not_exists(targetId, 1000022, [dict(name="total",value=cs(sum(out_rate)))])
        insert_if_not_exists(targetId, 1000022, [dict(name="avg",value=cs(round(sum(out_rate)/len(out_rate),2)))])
        insert_if_not_exists(targetId, 1001106, [dict(name="max",value=cs(max(out_size)))])
        insert_if_not_exists(targetId, 1001106, [dict(name="min",value=cs(min(out_size)))])
        insert_if_not_exists(targetId, 1001106, [dict(name="total",value=cs(sum(out_size)))])
        insert_if_not_exists(targetId, 1001106, [dict(name="avg",value=cs(round(sum(out_size)/len(out_size),2)))])

        # 内存/CPU/磁盘使用率
        insert_if_not_exists(targetId, 1001003, [dict(name="max",value=cs(max(cpu)))])
        insert_if_not_exists(targetId, 1001003, [dict(name="min",value=cs(min(cpu)))])
        insert_if_not_exists(targetId, 1001003, [dict(name="avg",value=cs(round(sum(cpu)/len(cpu),2)))])
        insert_if_not_exists(targetId, 1001004, [dict(name="max",value=cs(max(mem)))])
        insert_if_not_exists(targetId, 1001004, [dict(name="min",value=cs(min(mem)))])
        insert_if_not_exists(targetId, 1001004, [dict(name="avg",value=cs(round(sum(mem)/len(mem),2)))])
        insert_if_not_exists(targetId, 1000320, [dict(name="max",value=cs(max(disk)))])
        insert_if_not_exists(targetId, 1000320, [dict(name="min",value=cs(min(disk)))])
        insert_if_not_exists(targetId, 1000320, [dict(name="avg",value=cs(round(sum(disk)/len(disk),2)))])
        insert_if_not_exists(targetId, 1000321, [dict(name="max",value=cs(max(disk)))])
        insert_if_not_exists(targetId, 1000321, [dict(name="min",value=cs(min(disk)))])
        insert_if_not_exists(targetId, 1000321, [dict(name="avg",value=cs(round(sum(disk)/len(disk),2)))])
        insert_if_not_exists(targetId, 1000322, [dict(name="max",value=cs(max(disk)))])
        insert_if_not_exists(targetId, 1000322, [dict(name="min",value=cs(min(disk)))])
        insert_if_not_exists(targetId, 1000322, [dict(name="avg",value=cs(round(sum(disk)/len(disk),2)))])
        # insert_if_not_exists(targetId, 1000300, [dict(name="max",value=cs(max(disk)))])
        # insert_if_not_exists(targetId, 1000300, [dict(name="min",value=cs(min(disk)))])
        # insert_if_not_exists(targetId, 1000300, [dict(name="avg",value=cs(round(sum(disk)/len(disk),2)))])
        insert_if_not_exists(targetId, 1001102, [dict(name="max",value=cs(max(ioutil)))])
        insert_if_not_exists(targetId, 1001102, [dict(name="min",value=cs(min(ioutil)))])
        insert_if_not_exists(targetId, 1001102, [dict(name="avg",value=cs(round(sum(ioutil)/len(ioutil),2)))])

        # 磁盘
        insert_if_not_exists(targetId, 1001107, [dict(name="max",value=cs(max(ddelay)))])
        insert_if_not_exists(targetId, 1001107, [dict(name="min",value=cs(min(ddelay)))])
        insert_if_not_exists(targetId, 1001107, [dict(name="total",value=cs(sum(ddelay)))])
        insert_if_not_exists(targetId, 1001107, [dict(name="avg",value=cs(round(sum(ddelay)/len(ddelay),2)))])

        insert_if_not_exists(targetId, 1001108, [dict(name="max",value=cs(max(dreadKbSzie)))])
        insert_if_not_exists(targetId, 1001108, [dict(name="min",value=cs(min(dreadKbSzie)))])
        insert_if_not_exists(targetId, 1001108, [dict(name="total",value=cs(sum(dreadKbSzie)))])
        insert_if_not_exists(targetId, 1001108, [dict(name="avg",value=cs(round(sum(dreadKbSzie)/len(dreadKbSzie),2)))])

        insert_if_not_exists(targetId, 1001109, [dict(name="max",value=cs(max(dusedRatio)))])
        insert_if_not_exists(targetId, 1001109, [dict(name="min",value=cs(min(dusedRatio)))])
        insert_if_not_exists(targetId, 1001109, [dict(name="total",value=cs(sum(dusedRatio)))])
        insert_if_not_exists(targetId, 1001109, [dict(name="avg",value=cs(round(sum(dusedRatio)/len(dusedRatio),2)))])

        insert_if_not_exists(targetId, 1001110, [dict(name="max",value=cs(max(dwriteCount)))])
        insert_if_not_exists(targetId, 1001110, [dict(name="min",value=cs(min(dwriteCount)))])
        insert_if_not_exists(targetId, 1001110, [dict(name="total",value=cs(sum(dwriteCount)))])
        insert_if_not_exists(targetId, 1001110, [dict(name="avg",value=cs(round(sum(dwriteCount)/len(dwriteCount),2)))])

        insert_if_not_exists(targetId, 1001111, [dict(name="max",value=cs(max(dreadCount)))])
        insert_if_not_exists(targetId, 1001111, [dict(name="min",value=cs(min(dreadCount)))])
        insert_if_not_exists(targetId, 1001111, [dict(name="total",value=cs(sum(dreadCount)))])
        insert_if_not_exists(targetId, 1001111, [dict(name="avg",value=cs(round(sum(dreadCount)/len(dreadCount),2)))])

        insert_if_not_exists(targetId, 1001112, [dict(name="max",value=cs(max(dwriteKbSzie)))])
        insert_if_not_exists(targetId, 1001112, [dict(name="min",value=cs(min(dwriteKbSzie)))])
        insert_if_not_exists(targetId, 1001112, [dict(name="total",value=cs(sum(dwriteKbSzie)))])
        insert_if_not_exists(targetId, 1001112, [dict(name="avg",value=cs(round(sum(dwriteKbSzie)/len(dwriteKbSzie),2)))])


def get_monitor_data(host, user, base64_pwd, port, clusterId):
    """查询租户类统计信息"""
    url = f"https://{host}:{port}/open_api/insight/external/monitorCollect/searchMonitorData?collectIdList=63,200,201,202,206,207,208,210,302&clusterId={clusterId}"
    payload = {}
    headers = {
    'Cookie': 'SESSION=NWQ4ZTdlNjUtZWEwZi00ODZlLTk2ODMtNGRiZjFkYmExMTQw; JSESSIONID=5EF3A199858F08059A8E37402C2432F9',
    'username': user,
    'password': base64_pwd,
    'Content-Type': 'application/json'
    }
    proxies = {
            "http": None,
            "https": None,
            }
    try:
        response = requests.get(url, headers=headers, data=payload, verify=False, timeout=5, proxies=proxies)
    except Exception as e:
        insight_access_ip = DBUtil.get_aviable_insight_ip(pg, host, port)
        if insight_access_ip is not None:
            url = f"https://{insight_access_ip}:{port}/open_api/insight/external/monitorCollect/searchMonitorData?collectIdList=63,200,201,202,206,207,208,210,302&clusterId={clusterId}"
    response = requests.get(url, headers=headers, data=payload, verify=False, timeout=5, proxies=proxies)
    if response and response.status_code == 200:
        msg = response.json()
        cdatalist = msg["data"]['collectDataList']
        for r in cdatalist:
            collectId = r['collectId']
            if collectId == '200': # 计算节点性能统计，CN
                dataList = r['dataList']
                ctps = []
                ctotalTrans = []
                cfailTrans = []
                cdisTrans = []
                cdisTransAbcommit = []
                cdisWriteTrans = []
                cnonDisWriteTrans = []
                ctotalStatements = []
                cpressedStatments = []
                ccrossNodeDisWtrans = []
                cnonCrossNodeWtrans = []
                cqpsRead = []
                cqpsWrite = []
                if dataList:
                    for c in dataList:
                        node = c['ip']+':'+ str(c['port'])
                        uid = get_uid_by_ip(c['ip'], c['port'])
                        tps = c['tps']
                        totalTrans = c['totalTrans']
                        failTrans = c['failTrans']
                        disTrans = c['disTrans']
                        disTransAbcommit = c['disTransAbcommit']
                        disWriteTrans = c['disWriteTrans']
                        nonDisWriteTrans = c['nonDisWriteTrans']
                        totalStatements = c['totalStatements']
                        pressedStatments = c['pressedStatments']
                        crossNodeDisWtrans = c['crossNodeDisWtrans']
                        nonCrossNodeWtrans = c['nonCrossNodeWtrans']
                        qpsRead = c['qpsRead']
                        qpsWrite = c['qpsWrite']
                        ctps.append(tps)
                        ctotalTrans.append(totalTrans)
                        cfailTrans.append(failTrans)
                        cdisTrans.append(disTrans)
                        cdisTransAbcommit.append(disTransAbcommit)
                        cdisWriteTrans.append(disWriteTrans)
                        cnonDisWriteTrans.append(nonDisWriteTrans)
                        ctotalStatements.append(totalStatements)
                        cpressedStatments.append(pressedStatments)
                        ccrossNodeDisWtrans.append(crossNodeDisWtrans)
                        cnonCrossNodeWtrans.append(nonCrossNodeWtrans)
                        cqpsRead.append(qpsRead)
                        cqpsWrite.append(qpsWrite)
                        insert_if_not_exists(targetId, 2850001, [dict(name=node,value=cs(tps))])
                        insert_if_not_exists(targetId, 2850002, [dict(name=node,value=cs(totalTrans))])
                        insert_if_not_exists(targetId, 2850003, [dict(name=node,value=cs(failTrans))])
                        insert_if_not_exists(targetId, 2850004, [dict(name=node,value=cs(disTrans))])
                        insert_if_not_exists(targetId, 2850042, [dict(name=node,value=cs(disTransAbcommit))])
                        insert_if_not_exists(targetId, 2850005, [dict(name=node,value=cs(disWriteTrans))])
                        insert_if_not_exists(targetId, 2850006, [dict(name=node,value=cs(nonDisWriteTrans))])
                        insert_if_not_exists(targetId, 2850007, [dict(name=node,value=cs(totalStatements))])
                        insert_if_not_exists(targetId, 2850008, [dict(name=node,value=cs(pressedStatments))])
                        insert_if_not_exists(targetId, 2850009, [dict(name=node,value=cs(crossNodeDisWtrans))])
                        insert_if_not_exists(targetId, 2850010, [dict(name=node,value=cs(nonCrossNodeWtrans))])
                        insert_if_not_exists(targetId, 2850011, [dict(name=node,value=cs(qpsRead))])
                        insert_if_not_exists(targetId, 2850012, [dict(name=node,value=cs(qpsWrite))])
                        # insert_if_not_exists(uid, index_id=2850001, value=cs(tps))
                        # insert_if_not_exists(uid, index_id=2850002, value=cs(totalTrans))
                        # insert_if_not_exists(uid, index_id=2850003, value=cs(failTrans))
                        # insert_if_not_exists(uid, index_id=2850004, value=cs(disTrans))
                        # insert_if_not_exists(uid, index_id=2850042, value=cs(disTransAbcommit))
                        # insert_if_not_exists(uid, index_id=2850005, value=cs(disWriteTrans))
                        # insert_if_not_exists(uid, index_id=2850006, value=cs(nonDisWriteTrans))
                        # insert_if_not_exists(uid, index_id=2850007, value=cs(totalStatements))
                        # insert_if_not_exists(uid, index_id=2850008, value=cs(pressedStatments))
                        # insert_if_not_exists(uid, index_id=2850009, value=cs(crossNodeDisWtrans))
                        # insert_if_not_exists(uid, index_id=2850010, value=cs(nonCrossNodeWtrans))
                        # insert_if_not_exists(uid, index_id=2850011, value=cs(qpsRead))
                        # insert_if_not_exists(uid, index_id=2850012, value=cs(qpsWrite))
                if ctps:
                    # 最大值，最小值，平均值，汇总
                    insert_if_not_exists(targetId, 2850001, [dict(name='max',value=cs(max(ctps)))])
                    insert_if_not_exists(targetId, 2850001, [dict(name='min',value=cs(min(ctps)))])
                    insert_if_not_exists(targetId, 2850001, [dict(name='avg',value=cs(round(sum(ctps)/len(ctps),2)))])
                    insert_if_not_exists(targetId, 2850001, [dict(name='total',value=cs(sum(ctps)))])
                else:
                    insert_if_not_exists(targetId, 2850001, [dict(name='max',value=cs(0))])
                    insert_if_not_exists(targetId, 2850001, [dict(name='min',value=cs(0))])
                    insert_if_not_exists(targetId, 2850001, [dict(name='avg',value=cs(0))])
                    insert_if_not_exists(targetId, 2850001, [dict(name='total',value=cs(0))])
                if ctotalTrans:
                    # 最大值，最小值，平均值，汇总
                    insert_if_not_exists(targetId, 2850002, [dict(name='max',value=cs(max(ctotalTrans)))])
                    insert_if_not_exists(targetId, 2850002, [dict(name='min',value=cs(min(ctotalTrans)))])
                    insert_if_not_exists(targetId, 2850002, [dict(name='avg',value=cs(round(sum(ctotalTrans)/len(ctotalTrans),2)))])
                    insert_if_not_exists(targetId, 2850002, [dict(name='total',value=cs(sum(ctotalTrans)))])
                else:
                    insert_if_not_exists(targetId, 2850002, [dict(name='max',value=cs(0))])
                    insert_if_not_exists(targetId, 2850002, [dict(name='min',value=cs(0))])
                    insert_if_not_exists(targetId, 2850002, [dict(name='avg',value=cs(0))])
                    insert_if_not_exists(targetId, 2850002, [dict(name='total',value=cs(0))])
                if cfailTrans:
                    # 最大值，最小值，平均值，汇总
                    insert_if_not_exists(targetId, 2850003, [dict(name='max',value=cs(max(cfailTrans)))])
                    insert_if_not_exists(targetId, 2850003, [dict(name='min',value=cs(min(cfailTrans)))])
                    insert_if_not_exists(targetId, 2850003, [dict(name='avg',value=cs(round(sum(cfailTrans)/len(cfailTrans),2)))])
                    insert_if_not_exists(targetId, 2850003, [dict(name='total',value=cs(sum(cfailTrans)))])
                else:
                    insert_if_not_exists(targetId, 2850003, [dict(name='max',value=cs(0))])
                    insert_if_not_exists(targetId, 2850003, [dict(name='min',value=cs(0))])
                    insert_if_not_exists(targetId, 2850003, [dict(name='avg',value=cs(0))])
                    insert_if_not_exists(targetId, 2850003, [dict(name='total',value=cs(0))])
                if cdisTrans:
                    # 最大值，最小值，平均值，汇总
                    insert_if_not_exists(targetId, 2850004, [dict(name='max',value=cs(max(cdisTrans)))])
                    insert_if_not_exists(targetId, 2850004, [dict(name='min',value=cs(min(cdisTrans)))])
                    insert_if_not_exists(targetId, 2850004, [dict(name='avg',value=cs(round(sum(cdisTrans)/len(cdisTrans),2)))])
                    insert_if_not_exists(targetId, 2850004, [dict(name='total',value=cs(sum(cdisTrans)))])
                else:
                    insert_if_not_exists(targetId, 2850004, [dict(name='max',value=cs(0))])
                    insert_if_not_exists(targetId, 2850004, [dict(name='min',value=cs(0))])
                    insert_if_not_exists(targetId, 2850004, [dict(name='avg',value=cs(0))])
                    insert_if_not_exists(targetId, 2850004, [dict(name='total',value=cs(0))])
                if cdisTransAbcommit:
                    # 最大值，最小值，平均值，汇总
                    insert_if_not_exists(targetId, 2850042, [dict(name='max',value=cs(max(cdisTransAbcommit)))])
                    insert_if_not_exists(targetId, 2850042, [dict(name='min',value=cs(min(cdisTransAbcommit)))])
                    insert_if_not_exists(targetId, 2850042, [dict(name='avg',value=cs(round(sum(cdisTransAbcommit)/len(cdisTransAbcommit),2)))])
                    insert_if_not_exists(targetId, 2850042, [dict(name='total',value=cs(sum(cdisTransAbcommit)))])
                else:
                    insert_if_not_exists(targetId, 2850042, [dict(name='max',value=cs(0))])
                    insert_if_not_exists(targetId, 2850042, [dict(name='min',value=cs(0))])
                    insert_if_not_exists(targetId, 2850042, [dict(name='avg',value=cs(0))])
                    insert_if_not_exists(targetId, 2850042, [dict(name='total',value=cs(0))])
                if cdisWriteTrans:
                    # 最大值，最小值，平均值，汇总
                    insert_if_not_exists(targetId, 2850005, [dict(name='max',value=cs(max(cdisWriteTrans)))])
                    insert_if_not_exists(targetId, 2850005, [dict(name='min',value=cs(min(cdisWriteTrans)))])
                    insert_if_not_exists(targetId, 2850005, [dict(name='avg',value=cs(round(sum(cdisWriteTrans)/len(cdisWriteTrans),2)))])
                    insert_if_not_exists(targetId, 2850005, [dict(name='total',value=cs(sum(cdisWriteTrans)))])
                else:
                    insert_if_not_exists(targetId, 2850005, [dict(name='max',value=cs(0))])
                    insert_if_not_exists(targetId, 2850005, [dict(name='min',value=cs(0))])
                    insert_if_not_exists(targetId, 2850005, [dict(name='avg',value=cs(0))])
                    insert_if_not_exists(targetId, 2850005, [dict(name='total',value=cs(0))])
                if cnonDisWriteTrans:
                    # 最大值，最小值，平均值，汇总
                    insert_if_not_exists(targetId, 2850006, [dict(name='max',value=cs(max(cnonDisWriteTrans)))])
                    insert_if_not_exists(targetId, 2850006, [dict(name='min',value=cs(min(cnonDisWriteTrans)))])
                    insert_if_not_exists(targetId, 2850006, [dict(name='avg',value=cs(round(sum(cnonDisWriteTrans)/len(cnonDisWriteTrans),2)))])
                    insert_if_not_exists(targetId, 2850006, [dict(name='total',value=cs(sum(cnonDisWriteTrans)))])
                else:
                    insert_if_not_exists(targetId, 2850006, [dict(name='max',value=cs(0))])
                    insert_if_not_exists(targetId, 2850006, [dict(name='min',value=cs(0))])
                    insert_if_not_exists(targetId, 2850006, [dict(name='avg',value=cs(0))])
                    insert_if_not_exists(targetId, 2850006, [dict(name='total',value=cs(0))])
                if ctotalStatements:
                    # 最大值，最小值，平均值，汇总
                    insert_if_not_exists(targetId, 2850007, [dict(name='max',value=cs(max(ctotalStatements)))])
                    insert_if_not_exists(targetId, 2850007, [dict(name='min',value=cs(min(ctotalStatements)))])
                    insert_if_not_exists(targetId, 2850007, [dict(name='avg',value=cs(round(sum(ctotalStatements)/len(ctotalStatements),2)))])
                    insert_if_not_exists(targetId, 2850007, [dict(name='total',value=cs(sum(ctotalStatements)))])
                else:
                    insert_if_not_exists(targetId, 2850007, [dict(name='max',value=cs(0))])
                    insert_if_not_exists(targetId, 2850007, [dict(name='min',value=cs(0))])
                    insert_if_not_exists(targetId, 2850007, [dict(name='avg',value=cs(0))])
                    insert_if_not_exists(targetId, 2850007, [dict(name='total',value=cs(0))])
                if cpressedStatments:
                    # 最大值，最小值，平均值，汇总
                    insert_if_not_exists(targetId, 2850008, [dict(name='max',value=cs(max(cpressedStatments)))])
                    insert_if_not_exists(targetId, 2850008, [dict(name='min',value=cs(min(cpressedStatments)))])
                    insert_if_not_exists(targetId, 2850008, [dict(name='avg',value=cs(round(sum(cpressedStatments)/len(cpressedStatments),2)))])
                    insert_if_not_exists(targetId, 2850008, [dict(name='total',value=cs(sum(cpressedStatments)))])
                else:
                    insert_if_not_exists(targetId, 2850008, [dict(name='max',value=cs(0))])
                    insert_if_not_exists(targetId, 2850008, [dict(name='min',value=cs(0))])
                    insert_if_not_exists(targetId, 2850008, [dict(name='avg',value=cs(0))])
                    insert_if_not_exists(targetId, 2850008, [dict(name='total',value=cs(0))])
                if ccrossNodeDisWtrans:
                    # 最大值，最小值，平均值，汇总
                    insert_if_not_exists(targetId, 2850009, [dict(name='max',value=cs(max(ccrossNodeDisWtrans)))])
                    insert_if_not_exists(targetId, 2850009, [dict(name='min',value=cs(min(ccrossNodeDisWtrans)))])
                    insert_if_not_exists(targetId, 2850009, [dict(name='avg',value=cs(round(sum(ccrossNodeDisWtrans)/len(ccrossNodeDisWtrans),2)))])
                    insert_if_not_exists(targetId, 2850009, [dict(name='total',value=cs(sum(ccrossNodeDisWtrans)))])
                else:
                    insert_if_not_exists(targetId, 2850009, [dict(name='max',value=cs(0))])
                    insert_if_not_exists(targetId, 2850009, [dict(name='min',value=cs(0))])
                    insert_if_not_exists(targetId, 2850009, [dict(name='avg',value=cs(0))])
                    insert_if_not_exists(targetId, 2850009, [dict(name='total',value=cs(0))])
                if cnonCrossNodeWtrans:
                    # 最大值，最小值，平均值，汇总
                    insert_if_not_exists(targetId, 2850010, [dict(name='max',value=cs(max(cnonCrossNodeWtrans)))])
                    insert_if_not_exists(targetId, 2850010, [dict(name='min',value=cs(min(cnonCrossNodeWtrans)))])
                    insert_if_not_exists(targetId, 2850010, [dict(name='avg',value=cs(round(sum(cnonCrossNodeWtrans)/len(cnonCrossNodeWtrans),2)))])
                    insert_if_not_exists(targetId, 2850010, [dict(name='total',value=cs(sum(cnonCrossNodeWtrans)))])
                else:
                    insert_if_not_exists(targetId, 2850010, [dict(name='max',value=cs(0))])
                    insert_if_not_exists(targetId, 2850010, [dict(name='min',value=cs(0))])
                    insert_if_not_exists(targetId, 2850010, [dict(name='avg',value=cs(0))])
                    insert_if_not_exists(targetId, 2850010, [dict(name='total',value=cs(0))])
                if cqpsRead:
                    # 最大值，最小值，平均值，汇总
                    insert_if_not_exists(targetId, 2850011, [dict(name='max',value=cs(max(cqpsRead)))])
                    insert_if_not_exists(targetId, 2850011, [dict(name='min',value=cs(min(cqpsRead)))])
                    insert_if_not_exists(targetId, 2850011, [dict(name='avg',value=cs(round(sum(cqpsRead)/len(cqpsRead),2)))])
                    insert_if_not_exists(targetId, 2850011, [dict(name='total',value=cs(sum(cqpsRead)))])
                else:
                    insert_if_not_exists(targetId, 2850011, [dict(name='max',value=cs(0))])
                    insert_if_not_exists(targetId, 2850011, [dict(name='min',value=cs(0))])
                    insert_if_not_exists(targetId, 2850011, [dict(name='avg',value=cs(0))])
                    insert_if_not_exists(targetId, 2850011, [dict(name='total',value=cs(0))])
                if cqpsWrite:
                    # 最大值，最小值，平均值，汇总
                    insert_if_not_exists(targetId, 2850012, [dict(name='max',value=cs(max(cqpsWrite)))])
                    insert_if_not_exists(targetId, 2850012, [dict(name='min',value=cs(min(cqpsWrite)))])
                    insert_if_not_exists(targetId, 2850012, [dict(name='avg',value=cs(round(sum(cqpsWrite)/len(cqpsWrite),2)))])
                    insert_if_not_exists(targetId, 2850012, [dict(name='total',value=cs(sum(cqpsWrite)))])
                else:
                    insert_if_not_exists(targetId, 2850012, [dict(name='max',value=cs(0))])
                    insert_if_not_exists(targetId, 2850012, [dict(name='min',value=cs(0))])
                    insert_if_not_exists(targetId, 2850012, [dict(name='avg',value=cs(0))])
                    insert_if_not_exists(targetId, 2850012, [dict(name='total',value=cs(0))])
            elif collectId == '201':
                dataList = r['dataList']
                dselectNum = []
                dupdateNum = []
                ddeleteNum = []
                dinsertNum = []
                dtableLockConflictRate = []
                drowlockAvgWaitTime = []
                dbufferDirtPageRate = []
                dbufferHitRate = []
                dtempTableUsedNum = []
                dfileTempTableUsedRate = []
                dbinlogDiskUsedStat = []
                dredoLogWaitStat = []
                if dataList:
                    for c in dataList:
                        node = c['ip']+':'+str(c['port'])
                        uid = get_uid_by_ip(c['ip'], c['port'])
                        dbRole = c['dbRole']
                        selectNum = c['selectNum']
                        updateNum = c['updateNum']
                        deleteNum = c['deleteNum']
                        insertNum = c['insertNum']
                        tableLockConflictRate = c['tableLockConflictRate']
                        rowlockAvgWaitTime = c['rowlockAvgWaitTime']
                        bufferDirtPageRate = c['bufferDirtPageRate']
                        bufferHitRate = c['bufferHitRate']
                        tempTableUsedNum = c['tempTableUsedNum']
                        fileTempTableUsedRate = c['fileTempTableUsedRate']
                        binlogDiskUsedStat = c['binlogDiskUsedStat']
                        redoLogWaitStat = c['redoLogWaitStat']
                        dselectNum.append(selectNum)
                        dupdateNum.append(updateNum)
                        ddeleteNum.append(deleteNum)
                        dinsertNum.append(insertNum)
                        dtableLockConflictRate.append(tableLockConflictRate)
                        drowlockAvgWaitTime.append(rowlockAvgWaitTime)
                        dbufferDirtPageRate.append(bufferDirtPageRate)
                        dbufferHitRate.append(bufferHitRate)
                        dtempTableUsedNum.append(tempTableUsedNum)
                        dfileTempTableUsedRate.append(fileTempTableUsedRate)
                        dbinlogDiskUsedStat.append(binlogDiskUsedStat)
                        dredoLogWaitStat.append(redoLogWaitStat)
                        insert_if_not_exists(targetId, 2850043, [dict(name=node,value=cs(dbRole))])
                        insert_if_not_exists(targetId, 2850013, [dict(name=node,value=cs(selectNum))])
                        insert_if_not_exists(targetId, 2850014, [dict(name=node,value=cs(updateNum))])
                        insert_if_not_exists(targetId, 2850015, [dict(name=node,value=cs(deleteNum))])
                        insert_if_not_exists(targetId, 2850016, [dict(name=node,value=cs(insertNum))])
                        insert_if_not_exists(targetId, 2850017, [dict(name=node,value=cs(tableLockConflictRate))])
                        insert_if_not_exists(targetId, 2850018, [dict(name=node,value=cs(rowlockAvgWaitTime))])
                        insert_if_not_exists(targetId, 2850019, [dict(name=node,value=cs(bufferDirtPageRate))])
                        insert_if_not_exists(targetId, 2850020, [dict(name=node,value=cs(bufferHitRate))])
                        insert_if_not_exists(targetId, 2850021, [dict(name=node,value=cs(tempTableUsedNum))])
                        insert_if_not_exists(targetId, 2850022, [dict(name=node,value=cs(fileTempTableUsedRate))])
                        insert_if_not_exists(targetId, 2850023, [dict(name=node,value=cs(binlogDiskUsedStat))])
                        insert_if_not_exists(targetId, 2850024, [dict(name=node,value=cs(redoLogWaitStat))])
                        insert_if_not_exists(uid, index_id=2850000, value=cs('连接成功'))
                        insert_if_not_exists(uid, index_id=2850043, value=cs(dbRole))
                        insert_if_not_exists(uid, index_id=2850013, value=cs(selectNum))
                        insert_if_not_exists(uid, index_id=2850014, value=cs(updateNum))
                        insert_if_not_exists(uid, index_id=2850015, value=cs(deleteNum))
                        insert_if_not_exists(uid, index_id=2850016, value=cs(insertNum))
                        insert_if_not_exists(uid, index_id=2850017, value=cs(tableLockConflictRate))
                        insert_if_not_exists(uid, index_id=2850018, value=cs(rowlockAvgWaitTime))
                        insert_if_not_exists(uid, index_id=2850019, value=cs(bufferDirtPageRate))
                        insert_if_not_exists(uid, index_id=2850020, value=cs(bufferHitRate))
                        insert_if_not_exists(uid, index_id=2850021, value=cs(tempTableUsedNum))
                        insert_if_not_exists(uid, index_id=2850022, value=cs(fileTempTableUsedRate))
                        insert_if_not_exists(uid, index_id=2850023, value=cs(binlogDiskUsedStat))
                        insert_if_not_exists(uid, index_id=2850024, value=cs(redoLogWaitStat))
                if dselectNum:
                    # 最大值，最小值，平均值，汇总
                    insert_if_not_exists(targetId, 2850013, [dict(name='max',value=cs(max(dselectNum)))])
                    insert_if_not_exists(targetId, 2850013, [dict(name='min',value=cs(min(dselectNum)))])
                    insert_if_not_exists(targetId, 2850013, [dict(name='avg',value=cs(round(sum(dselectNum)/len(dselectNum),2)))])
                    insert_if_not_exists(targetId, 2850013, [dict(name='total',value=cs(sum(dselectNum)))])
                else:
                    insert_if_not_exists(targetId, 2850013, [dict(name='max',value=cs(0))])
                    insert_if_not_exists(targetId, 2850013, [dict(name='min',value=cs(0))])
                    insert_if_not_exists(targetId, 2850013, [dict(name='avg',value=cs(0))])
                    insert_if_not_exists(targetId, 2850013, [dict(name='total',value=cs(0))])
                if dupdateNum:
                    # 最大值，最小值，平均值，汇总
                    insert_if_not_exists(targetId, 2850014, [dict(name='max',value=cs(max(dupdateNum)))])
                    insert_if_not_exists(targetId, 2850014, [dict(name='min',value=cs(min(dupdateNum)))])
                    insert_if_not_exists(targetId, 2850014, [dict(name='avg',value=cs(round(sum(dupdateNum)/len(dupdateNum),2)))])
                    insert_if_not_exists(targetId, 2850014, [dict(name='total',value=cs(sum(dupdateNum)))])
                else:                                  
                    insert_if_not_exists(targetId, 2850014, [dict(name='max',value=cs(0))])
                    insert_if_not_exists(targetId, 2850014, [dict(name='min',value=cs(0))])
                    insert_if_not_exists(targetId, 2850014, [dict(name='avg',value=cs(0))])
                    insert_if_not_exists(targetId, 2850014, [dict(name='total',value=cs(0))])
                if ddeleteNum:
                    # 最大值，最小值，平均值，汇总
                    insert_if_not_exists(targetId, 2850015, [dict(name='max',value=cs(max(ddeleteNum)))])
                    insert_if_not_exists(targetId, 2850015, [dict(name='min',value=cs(min(ddeleteNum)))])
                    insert_if_not_exists(targetId, 2850015, [dict(name='avg',value=cs(round(sum(ddeleteNum)/len(ddeleteNum),2)))])
                    insert_if_not_exists(targetId, 2850015, [dict(name='total',value=cs(sum(ddeleteNum)))])
                else:                                   
                    insert_if_not_exists(targetId, 2850015, [dict(name='max',value=cs(0))])
                    insert_if_not_exists(targetId, 2850015, [dict(name='min',value=cs(0))])
                    insert_if_not_exists(targetId, 2850015, [dict(name='avg',value=cs(0))])
                    insert_if_not_exists(targetId, 2850015, [dict(name='total',value=cs(0))])
                if dinsertNum:
                    # 最大值，最小值，平均值，汇总
                    insert_if_not_exists(targetId, 2850016, [dict(name='max',value=cs(max(dinsertNum)))])
                    insert_if_not_exists(targetId, 2850016, [dict(name='min',value=cs(min(dinsertNum)))])
                    insert_if_not_exists(targetId, 2850016, [dict(name='avg',value=cs(round(sum(dinsertNum)/len(dinsertNum),2)))])
                    insert_if_not_exists(targetId, 2850016, [dict(name='total',value=cs(sum(dinsertNum)))])
                else:                                   
                    insert_if_not_exists(targetId, 2850016, [dict(name='max',value=cs(0))])
                    insert_if_not_exists(targetId, 2850016, [dict(name='min',value=cs(0))])
                    insert_if_not_exists(targetId, 2850016, [dict(name='avg',value=cs(0))])
                    insert_if_not_exists(targetId, 2850016, [dict(name='total',value=cs(0))])
                if dtableLockConflictRate:
                    # 最大值，最小值，平均值，汇总
                    insert_if_not_exists(targetId, 2850017, [dict(name='max',value=cs(max(dtableLockConflictRate)))])
                    insert_if_not_exists(targetId, 2850017, [dict(name='min',value=cs(min(dtableLockConflictRate)))])
                    insert_if_not_exists(targetId, 2850017, [dict(name='avg',value=cs(round(sum(dtableLockConflictRate)/len(dtableLockConflictRate),2)))])
                    insert_if_not_exists(targetId, 2850017, [dict(name='total',value=cs(sum(dtableLockConflictRate)))])
                else:                                   
                    insert_if_not_exists(targetId, 2850017, [dict(name='max',value=cs(0))])
                    insert_if_not_exists(targetId, 2850017, [dict(name='min',value=cs(0))])
                    insert_if_not_exists(targetId, 2850017, [dict(name='avg',value=cs(0))])
                    insert_if_not_exists(targetId, 2850017, [dict(name='total',value=cs(0))])
                if drowlockAvgWaitTime:
                    # 最大值，最小值，平均值，汇总
                    insert_if_not_exists(targetId, 2850018, [dict(name='max',value=cs(max(drowlockAvgWaitTime)))])
                    insert_if_not_exists(targetId, 2850018, [dict(name='min',value=cs(min(drowlockAvgWaitTime)))])
                    insert_if_not_exists(targetId, 2850018, [dict(name='avg',value=cs(round(sum(drowlockAvgWaitTime)/len(drowlockAvgWaitTime),2)))])
                    insert_if_not_exists(targetId, 2850018, [dict(name='total',value=cs(sum(drowlockAvgWaitTime)))])
                else:                                   
                    insert_if_not_exists(targetId, 2850018, [dict(name='max',value=cs(0))])
                    insert_if_not_exists(targetId, 2850018, [dict(name='min',value=cs(0))])
                    insert_if_not_exists(targetId, 2850018, [dict(name='avg',value=cs(0))])
                    insert_if_not_exists(targetId, 2850018, [dict(name='total',value=cs(0))])
                if dbufferDirtPageRate:
                    # 最大值，最小值，平均值，汇总
                    insert_if_not_exists(targetId, 2850019, [dict(name='max',value=cs(max(dbufferDirtPageRate)))])
                    insert_if_not_exists(targetId, 2850019, [dict(name='min',value=cs(min(dbufferDirtPageRate)))])
                    insert_if_not_exists(targetId, 2850019, [dict(name='avg',value=cs(round(sum(dbufferDirtPageRate)/len(dbufferDirtPageRate),2)))])
                    insert_if_not_exists(targetId, 2850019, [dict(name='total',value=cs(sum(dbufferDirtPageRate)))])
                else:                                  
                    insert_if_not_exists(targetId, 2850019, [dict(name='max',value=cs(0))])
                    insert_if_not_exists(targetId, 2850019, [dict(name='min',value=cs(0))])
                    insert_if_not_exists(targetId, 2850019, [dict(name='avg',value=cs(0))])
                    insert_if_not_exists(targetId, 2850019, [dict(name='total',value=cs(0))])
                if dbufferHitRate:
                    # 最大值，最小值，平均值，汇总
                    insert_if_not_exists(targetId, 2850020, [dict(name='max',value=cs(max(dbufferHitRate)))])
                    insert_if_not_exists(targetId, 2850020, [dict(name='min',value=cs(min(dbufferHitRate)))])
                    insert_if_not_exists(targetId, 2850020, [dict(name='avg',value=cs(round(sum(dbufferHitRate)/len(dbufferHitRate),2)))])
                    insert_if_not_exists(targetId, 2850020, [dict(name='total',value=cs(sum(dbufferHitRate)))])
                else:                               
                    insert_if_not_exists(targetId, 2850020, [dict(name='max',value=cs(0))])
                    insert_if_not_exists(targetId, 2850020, [dict(name='min',value=cs(0))])
                    insert_if_not_exists(targetId, 2850020, [dict(name='avg',value=cs(0))])
                    insert_if_not_exists(targetId, 2850020, [dict(name='total',value=cs(0))])
                if dtempTableUsedNum:
                    # 最大值，最小值，平均值，汇总
                    insert_if_not_exists(targetId, 2850021, [dict(name='max',value=cs(max(dtempTableUsedNum)))])
                    insert_if_not_exists(targetId, 2850021, [dict(name='min',value=cs(min(dtempTableUsedNum)))])
                    insert_if_not_exists(targetId, 2850021, [dict(name='avg',value=cs(round(sum(dtempTableUsedNum)/len(dtempTableUsedNum),2)))])
                    insert_if_not_exists(targetId, 2850021, [dict(name='total',value=cs(sum(dtempTableUsedNum)))])
                else:                  
                    insert_if_not_exists(targetId, 2850021, [dict(name='max',value=cs(0))])
                    insert_if_not_exists(targetId, 2850021, [dict(name='min',value=cs(0))])
                    insert_if_not_exists(targetId, 2850021, [dict(name='avg',value=cs(0))])
                    insert_if_not_exists(targetId, 2850021, [dict(name='total',value=cs(0))])
                if dfileTempTableUsedRate:
                    # 最大值，最小值，平均值，汇总
                    insert_if_not_exists(targetId, 2850022, [dict(name='max',value=cs(max(dfileTempTableUsedRate)))])
                    insert_if_not_exists(targetId, 2850022, [dict(name='min',value=cs(min(dfileTempTableUsedRate)))])
                    insert_if_not_exists(targetId, 2850022, [dict(name='avg',value=cs(round(sum(dfileTempTableUsedRate)/len(dfileTempTableUsedRate),2)))])
                    insert_if_not_exists(targetId, 2850022, [dict(name='total',value=cs(sum(dfileTempTableUsedRate)))])
                else:                                
                    insert_if_not_exists(targetId, 2850022, [dict(name='max',value=cs(0))])
                    insert_if_not_exists(targetId, 2850022, [dict(name='min',value=cs(0))])
                    insert_if_not_exists(targetId, 2850022, [dict(name='avg',value=cs(0))])
                    insert_if_not_exists(targetId, 2850022, [dict(name='total',value=cs(0))])
                if dbinlogDiskUsedStat:
                    # 最大值，最小值，平均值，汇总
                    insert_if_not_exists(targetId, 2850023, [dict(name='max',value=cs(max(dbinlogDiskUsedStat)))])
                    insert_if_not_exists(targetId, 2850023, [dict(name='min',value=cs(min(dbinlogDiskUsedStat)))])
                    insert_if_not_exists(targetId, 2850023, [dict(name='avg',value=cs(round(sum(dbinlogDiskUsedStat)/len(dbinlogDiskUsedStat),2)))])
                    insert_if_not_exists(targetId, 2850023, [dict(name='total',value=cs(sum(dbinlogDiskUsedStat)))])
                else:                                
                    insert_if_not_exists(targetId, 2850023, [dict(name='max',value=cs(0))])
                    insert_if_not_exists(targetId, 2850023, [dict(name='min',value=cs(0))])
                    insert_if_not_exists(targetId, 2850023, [dict(name='avg',value=cs(0))])
                    insert_if_not_exists(targetId, 2850023, [dict(name='total',value=cs(0))])
                if dredoLogWaitStat:
                    # 最大值，最小值，平均值，汇总
                    insert_if_not_exists(targetId, 2850024, [dict(name='max',value=cs(max(dredoLogWaitStat)))])
                    insert_if_not_exists(targetId, 2850024, [dict(name='min',value=cs(min(dredoLogWaitStat)))])
                    insert_if_not_exists(targetId, 2850024, [dict(name='avg',value=cs(round(sum(dredoLogWaitStat)/len(dredoLogWaitStat),2)))])
                    insert_if_not_exists(targetId, 2850024, [dict(name='total',value=cs(sum(dredoLogWaitStat)))])
                else:                                
                    insert_if_not_exists(targetId, 2850024, [dict(name='max',value=cs(0))])
                    insert_if_not_exists(targetId, 2850024, [dict(name='min',value=cs(0))])
                    insert_if_not_exists(targetId, 2850024, [dict(name='avg',value=cs(0))])
                    insert_if_not_exists(targetId, 2850024, [dict(name='total',value=cs(0))])
            elif collectId == '202':
                dataList = r['dataList']
                galiveDrdcLink = []
                glink = []
                if dataList:
                    for c in dataList:
                        node = c['ip']+':'+str(c['port'])
                        uid = get_uid_by_ip(c['ip'], c['port'])
                        aliveDrdcLink = c['aliveDrdcLink']
                        link = c['link']
                        galiveDrdcLink.append(aliveDrdcLink)
                        glink.append(link)
                        insert_if_not_exists(targetId, 2850025, [dict(name=node,value=cs(aliveDrdcLink))])
                        insert_if_not_exists(targetId, 2850026, [dict(name=node,value=cs(link))])
                        # insert_if_not_exists(uid, index_id = 2850025, value=cs(aliveDrdcLink))
                        # insert_if_not_exists(uid, index_id = 2850026, value=cs(link))
                if galiveDrdcLink:
                    # 最大值，最小值，平均值，汇总
                    insert_if_not_exists(targetId, 2850025, [dict(name='max',value=cs(max(galiveDrdcLink)))])
                    insert_if_not_exists(targetId, 2850025, [dict(name='min',value=cs(min(galiveDrdcLink)))])
                    insert_if_not_exists(targetId, 2850025, [dict(name='avg',value=cs(round(sum(galiveDrdcLink)/len(galiveDrdcLink),2)))])
                    insert_if_not_exists(targetId, 2850025, [dict(name='total',value=cs(sum(galiveDrdcLink)))])
                else:                                  
                    insert_if_not_exists(targetId, 2850025, [dict(name='max',value=cs(0))])
                    insert_if_not_exists(targetId, 2850025, [dict(name='min',value=cs(0))])
                    insert_if_not_exists(targetId, 2850025, [dict(name='avg',value=cs(0))])
                    insert_if_not_exists(targetId, 2850025, [dict(name='total',value=cs(0))])
                if glink:
                    # 最大值，最小值，平均值，汇总
                    insert_if_not_exists(targetId, 2850026, [dict(name='max',value=cs(max(glink)))])
                    insert_if_not_exists(targetId, 2850026, [dict(name='min',value=cs(min(glink)))])
                    insert_if_not_exists(targetId, 2850026, [dict(name='avg',value=cs(round(sum(glink)/len(glink),2)))])
                    insert_if_not_exists(targetId, 2850026, [dict(name='total',value=cs(sum(glink)))])
                else:                                 
                    insert_if_not_exists(targetId, 2850026, [dict(name='max',value=cs(0))])
                    insert_if_not_exists(targetId, 2850026, [dict(name='min',value=cs(0))])
                    insert_if_not_exists(targetId, 2850026, [dict(name='avg',value=cs(0))])
                    insert_if_not_exists(targetId, 2850026, [dict(name='total',value=cs(0))])
            elif collectId == '206':
                dataList = r['dataList']
                gactiveGtidNum = []
                if dataList:
                    for c in dataList:
                        node = c['ip']+':'+str(c['port'])
                        uid = get_uid_by_ip(c['ip'], c['port'])
                        activeGtidNum = c['activeGtidNum']
                        gactiveGtidNum.append(activeGtidNum)
                        insert_if_not_exists(targetId, 2850027, [dict(name=node,value=cs(activeGtidNum))])
                        # insert_if_not_exists(uid, index_id = 2850027, value=cs(activeGtidNum))
                if gactiveGtidNum:
                    # 最大值，最小值，平均值，汇总
                    insert_if_not_exists(targetId, 2850027, [dict(name='max',value=cs(max(gactiveGtidNum)))])
                    insert_if_not_exists(targetId, 2850027, [dict(name='min',value=cs(min(gactiveGtidNum)))])
                    insert_if_not_exists(targetId, 2850027, [dict(name='avg',value=cs(round(sum(gactiveGtidNum)/len(gactiveGtidNum),2)))])
                    insert_if_not_exists(targetId, 2850027, [dict(name='total',value=cs(sum(gactiveGtidNum)))])
                else:                               
                    insert_if_not_exists(targetId, 2850027, [dict(name='max',value=cs(0))])
                    insert_if_not_exists(targetId, 2850027, [dict(name='min',value=cs(0))])
                    insert_if_not_exists(targetId, 2850027, [dict(name='avg',value=cs(0))])
                    insert_if_not_exists(targetId, 2850027, [dict(name='total',value=cs(0))])
            elif collectId == '207':
                dataList = r['dataList']
                ggetGtidTime = []
                ggetGtidNum = []
                gfreeGtidTime = []
                gfreeGtidNum = []
                if dataList:
                    for c in dataList:
                        node = c['ip']+':'+str(c['port'])
                        uid = get_uid_by_ip(c['ip'], c['port'])
                        getGtidTime = c['getGtidTime']
                        getGtidNum = c['getGtidNum']
                        freeGtidTime = c['freeGtidTime']
                        freeGtidNum = c['freeGtidNum']
                        ggetGtidTime.append(getGtidTime)
                        ggetGtidNum.append(getGtidNum)
                        gfreeGtidTime.append(freeGtidTime)
                        gfreeGtidNum.append(freeGtidNum)
                        insert_if_not_exists(targetId, 2850028, [dict(name=node,value=cs(getGtidTime))])
                        insert_if_not_exists(targetId, 2850029, [dict(name=node,value=cs(getGtidNum))])
                        insert_if_not_exists(targetId, 2850030, [dict(name=node,value=cs(freeGtidTime))])
                        insert_if_not_exists(targetId, 2850031, [dict(name=node,value=cs(freeGtidNum))])
                        # insert_if_not_exists(uid, index_id = 2850028, value=cs(getGtidTime))
                        # insert_if_not_exists(uid, index_id = 2850029, value=cs(getGtidNum))
                        # insert_if_not_exists(uid, index_id = 2850030, value=cs(freeGtidTime))
                        # insert_if_not_exists(uid, index_id = 2850031, value=cs(freeGtidNum))
                if ggetGtidTime:
                    # 最大值，最小值，平均值，汇总
                    insert_if_not_exists(targetId, 2850028, [dict(name='max',value=cs(max(ggetGtidTime)))])
                    insert_if_not_exists(targetId, 2850028, [dict(name='min',value=cs(min(ggetGtidTime)))])
                    insert_if_not_exists(targetId, 2850028, [dict(name='avg',value=cs(round(sum(ggetGtidTime)/len(ggetGtidTime),2)))])
                    insert_if_not_exists(targetId, 2850028, [dict(name='total',value=cs(sum(ggetGtidTime)))])
                else:                                    
                    insert_if_not_exists(targetId, 2850028, [dict(name='max',value=cs(0))])
                    insert_if_not_exists(targetId, 2850028, [dict(name='min',value=cs(0))])
                    insert_if_not_exists(targetId, 2850028, [dict(name='avg',value=cs(0))])
                    insert_if_not_exists(targetId, 2850028, [dict(name='total',value=cs(0))])
                if ggetGtidNum:
                    # 最大值，最小值，平均值，汇总
                    insert_if_not_exists(targetId, 2850029, [dict(name='max',value=cs(max(ggetGtidNum)))])
                    insert_if_not_exists(targetId, 2850029, [dict(name='min',value=cs(min(ggetGtidNum)))])
                    insert_if_not_exists(targetId, 2850029, [dict(name='avg',value=cs(round(sum(ggetGtidNum)/len(ggetGtidNum),2)))])
                    insert_if_not_exists(targetId, 2850029, [dict(name='total',value=cs(sum(ggetGtidNum)))])
                else:                                    
                    insert_if_not_exists(targetId, 2850029, [dict(name='max',value=cs(0))])
                    insert_if_not_exists(targetId, 2850029, [dict(name='min',value=cs(0))])
                    insert_if_not_exists(targetId, 2850029, [dict(name='avg',value=cs(0))])
                    insert_if_not_exists(targetId, 2850029, [dict(name='total',value=cs(0))])
                if gfreeGtidTime:
                    # 最大值，最小值，平均值，汇总
                    insert_if_not_exists(targetId, 2850030, [dict(name='max',value=cs(max(gfreeGtidTime)))])
                    insert_if_not_exists(targetId, 2850030, [dict(name='min',value=cs(min(gfreeGtidTime)))])
                    insert_if_not_exists(targetId, 2850030, [dict(name='avg',value=cs(round(sum(gfreeGtidTime)/len(gfreeGtidTime),2)))])
                    insert_if_not_exists(targetId, 2850030, [dict(name='total',value=cs(sum(gfreeGtidTime)))])
                else:                                  
                    insert_if_not_exists(targetId, 2850030, [dict(name='max',value=cs(0))])
                    insert_if_not_exists(targetId, 2850030, [dict(name='min',value=cs(0))])
                    insert_if_not_exists(targetId, 2850030, [dict(name='avg',value=cs(0))])
                    insert_if_not_exists(targetId, 2850030, [dict(name='total',value=cs(0))])
                if gfreeGtidNum:
                    # 最大值，最小值，平均值，汇总
                    insert_if_not_exists(targetId, 2850031, [dict(name='max',value=cs(max(gfreeGtidNum)))])
                    insert_if_not_exists(targetId, 2850031, [dict(name='min',value=cs(min(gfreeGtidNum)))])
                    insert_if_not_exists(targetId, 2850031, [dict(name='avg',value=cs(round(sum(gfreeGtidNum)/len(gfreeGtidNum),2)))])
                    insert_if_not_exists(targetId, 2850031, [dict(name='total',value=cs(sum(gfreeGtidNum)))])
                else:                                  
                    insert_if_not_exists(targetId, 2850031, [dict(name='max',value=cs(0))])
                    insert_if_not_exists(targetId, 2850031, [dict(name='min',value=cs(0))])
                    insert_if_not_exists(targetId, 2850031, [dict(name='avg',value=cs(0))])
                    insert_if_not_exists(targetId, 2850031, [dict(name='total',value=cs(0))])
            elif collectId == '208':
                dataList = r['dataList']
                ctransNum = []
                ctransFailedNum = []
                ctransTotalExectime = []
                if dataList:
                    for c in dataList:
                        node = c['ip']+':'+str(c['port'])
                        uid = get_uid_by_ip(c['ip'], c['port'])
                        transNum = c['transNum']
                        transFailedNum = c['transFailedNum']
                        transTotalExectime = c['transTotalExectime']
                        ctransNum.append(transNum)
                        ctransFailedNum.append(transFailedNum)
                        ctransTotalExectime.append(transTotalExectime)
                        insert_if_not_exists(targetId, 2850032, [dict(name=node,value=cs(transNum))])
                        insert_if_not_exists(targetId, 2850033, [dict(name=node,value=cs(transFailedNum))])
                        insert_if_not_exists(targetId, 2850034, [dict(name=node,value=cs(transTotalExectime))])
                if ctransNum:
                    # 最大值，最小值，平均值，汇总
                    insert_if_not_exists(targetId, 2850032, [dict(name='max',value=cs(max(ctransNum)))])
                    insert_if_not_exists(targetId, 2850032, [dict(name='min',value=cs(min(ctransNum)))])
                    insert_if_not_exists(targetId, 2850032, [dict(name='avg',value=cs(round(sum(ctransNum)/len(ctransNum),2)))])
                    insert_if_not_exists(targetId, 2850032, [dict(name='total',value=cs(sum(ctransNum)))])
                else:                                  
                    insert_if_not_exists(targetId, 2850032, [dict(name='max',value=cs(0))])
                    insert_if_not_exists(targetId, 2850032, [dict(name='min',value=cs(0))])
                    insert_if_not_exists(targetId, 2850032, [dict(name='avg',value=cs(0))])
                    insert_if_not_exists(targetId, 2850032, [dict(name='total',value=cs(0))])
                if ctransFailedNum:
                    # 最大值，最小值，平均值，汇总
                    insert_if_not_exists(targetId, 2850033, [dict(name='max',value=cs(max(ctransFailedNum)))])
                    insert_if_not_exists(targetId, 2850033, [dict(name='min',value=cs(min(ctransFailedNum)))])
                    insert_if_not_exists(targetId, 2850033, [dict(name='avg',value=cs(round(sum(ctransFailedNum)/len(ctransFailedNum),2)))])
                    insert_if_not_exists(targetId, 2850033, [dict(name='total',value=cs(sum(ctransFailedNum)))])
                else:                               
                    insert_if_not_exists(targetId, 2850033, [dict(name='max',value=cs(0))])
                    insert_if_not_exists(targetId, 2850033, [dict(name='min',value=cs(0))])
                    insert_if_not_exists(targetId, 2850033, [dict(name='avg',value=cs(0))])
                    insert_if_not_exists(targetId, 2850033, [dict(name='total',value=cs(0))])
                if ctransTotalExectime:
                    # 最大值，最小值，平均值，汇总
                    insert_if_not_exists(targetId, 2850034, [dict(name='max',value=cs(max(ctransTotalExectime)))])
                    insert_if_not_exists(targetId, 2850034, [dict(name='min',value=cs(min(ctransTotalExectime)))])
                    insert_if_not_exists(targetId, 2850034, [dict(name='avg',value=cs(round(sum(ctransTotalExectime)/len(ctransTotalExectime),2)))])
                    insert_if_not_exists(targetId, 2850034, [dict(name='total',value=cs(sum(ctransTotalExectime)))])
                else:                               
                    insert_if_not_exists(targetId, 2850034, [dict(name='max',value=cs(0))])
                    insert_if_not_exists(targetId, 2850034, [dict(name='min',value=cs(0))])
                    insert_if_not_exists(targetId, 2850034, [dict(name='avg',value=cs(0))])
                    insert_if_not_exists(targetId, 2850034, [dict(name='total',value=cs(0))])
            elif collectId == '210':
                dataList = r['dataList']
                dsyncLogDelayTime = []
                dsyncLogGap = []
                drelayLogDelayTime = []
                drelayLogGap = []
                if dataList:
                    for c in dataList:
                        node = c['ip']+':'+str(c['port'])
                        uid = get_uid_by_ip(c['ip'], c['port'])
                        groupSwitching = c['groupSwitching']
                        dbRole = c['dbRole']
                        hlwm = c['hlwm']
                        syncLogDelayTime = c['syncLogDelayTime']
                        syncLogGap = c['syncLogGap']
                        relayLogDelayTime = c['relayLogDelayTime']
                        relayLogGap = c['relayLogGap']
                        dsyncLogDelayTime.append(syncLogDelayTime)
                        dsyncLogGap.append(syncLogGap)
                        drelayLogDelayTime.append(relayLogDelayTime)
                        drelayLogGap.append(relayLogGap)
                        insert_if_not_exists(targetId, 2850044, [dict(name=node,value=cs(groupSwitching))])
                        insert_if_not_exists(targetId, 2850035, [dict(name=node,value=cs(dbRole))])
                        insert_if_not_exists(targetId, 2850036, [dict(name=node,value=cs(hlwm))])
                        insert_if_not_exists(targetId, 2850037, [dict(name=node,value=cs(syncLogDelayTime))])
                        insert_if_not_exists(targetId, 2850038, [dict(name=node,value=cs(syncLogGap))])
                        insert_if_not_exists(targetId, 2850039, [dict(name=node,value=cs(relayLogDelayTime))])
                        insert_if_not_exists(targetId, 2850040, [dict(name=node,value=cs(relayLogGap))])
                        # insert_if_not_exists(uid ,index_id = 2850044, value=cs(groupSwitching))
                        # insert_if_not_exists(uid ,index_id = 2850035, value=cs(dbRole))
                        # insert_if_not_exists(uid ,index_id = 2850036, value=cs(hlwm))
                        # insert_if_not_exists(uid ,index_id = 2850037, value=cs(syncLogDelayTime))
                        # insert_if_not_exists(uid ,index_id = 2850038, value=cs(syncLogGap))
                        # insert_if_not_exists(uid ,index_id = 2850039, value=cs(relayLogDelayTime))
                        # insert_if_not_exists(uid ,index_id = 2850040, value=cs(relayLogGap))
                if dsyncLogDelayTime:
                    # 最大值，最小值，平均值，汇总
                    insert_if_not_exists(targetId, 2850037, [dict(name='max',value=cs(max(dsyncLogDelayTime)))])
                    insert_if_not_exists(targetId, 2850037, [dict(name='min',value=cs(min(dsyncLogDelayTime)))])
                    insert_if_not_exists(targetId, 2850037, [dict(name='avg',value=cs(round(sum(dsyncLogDelayTime)/len(dsyncLogDelayTime),2)))])
                    insert_if_not_exists(targetId, 2850037, [dict(name='total',value=cs(sum(dsyncLogDelayTime)))])
                else:                                
                    insert_if_not_exists(targetId, 2850037, [dict(name='max',value=cs(0))])
                    insert_if_not_exists(targetId, 2850037, [dict(name='min',value=cs(0))])
                    insert_if_not_exists(targetId, 2850037, [dict(name='avg',value=cs(0))])
                    insert_if_not_exists(targetId, 2850037, [dict(name='total',value=cs(0))])
                if dsyncLogGap:
                    # 最大值，最小值，平均值，汇总
                    insert_if_not_exists(targetId, 2850038, [dict(name='max',value=cs(max(dsyncLogGap)))])
                    insert_if_not_exists(targetId, 2850038, [dict(name='min',value=cs(min(dsyncLogGap)))])
                    insert_if_not_exists(targetId, 2850038, [dict(name='avg',value=cs(round(sum(dsyncLogGap)/len(dsyncLogGap),2)))])
                    insert_if_not_exists(targetId, 2850038, [dict(name='total',value=cs(sum(dsyncLogGap)))])
                else:                                 
                    insert_if_not_exists(targetId, 2850038, [dict(name='max',value=cs(0))])
                    insert_if_not_exists(targetId, 2850038, [dict(name='min',value=cs(0))])
                    insert_if_not_exists(targetId, 2850038, [dict(name='avg',value=cs(0))])
                    insert_if_not_exists(targetId, 2850038, [dict(name='total',value=cs(0))])
                if drelayLogDelayTime:
                    # 最大值，最小值，平均值，汇总
                    insert_if_not_exists(targetId, 2850039, [dict(name='max',value=cs(max(drelayLogDelayTime)))])
                    insert_if_not_exists(targetId, 2850039, [dict(name='min',value=cs(min(drelayLogDelayTime)))])
                    insert_if_not_exists(targetId, 2850039, [dict(name='avg',value=cs(round(sum(drelayLogDelayTime)/len(drelayLogDelayTime),2)))])
                    insert_if_not_exists(targetId, 2850039, [dict(name='total',value=cs(sum(drelayLogDelayTime)))])
                else:                                
                    insert_if_not_exists(targetId, 2850039, [dict(name='max',value=cs(0))])
                    insert_if_not_exists(targetId, 2850039, [dict(name='min',value=cs(0))])
                    insert_if_not_exists(targetId, 2850039, [dict(name='avg',value=cs(0))])
                    insert_if_not_exists(targetId, 2850039, [dict(name='total',value=cs(0))])
                if drelayLogGap:
                    # 最大值，最小值，平均值，汇总
                    insert_if_not_exists(targetId, 2850040, [dict(name='max',value=cs(max(drelayLogGap)))])
                    insert_if_not_exists(targetId, 2850040, [dict(name='min',value=cs(min(drelayLogGap)))])
                    insert_if_not_exists(targetId, 2850040, [dict(name='avg',value=cs(round(sum(drelayLogGap)/len(drelayLogGap),2)))])
                    insert_if_not_exists(targetId, 2850040, [dict(name='total',value=cs(sum(drelayLogGap)))])
                else:                            
                    insert_if_not_exists(targetId, 2850040, [dict(name='max',value=cs(0))])
                    insert_if_not_exists(targetId, 2850040, [dict(name='min',value=cs(0))])
                    insert_if_not_exists(targetId, 2850040, [dict(name='avg',value=cs(0))])
                    insert_if_not_exists(targetId, 2850040, [dict(name='total',value=cs(0))])
            elif collectId == '302':
                dataList = r['dataList']
                dlockWaitNum = []
                if dataList:
                    for c in dataList:
                        node = c['ip']+':'+str(c['port'])
                        uid = get_uid_by_ip(c['ip'], c['port'])
                        lockWaitNum = c['lockWaitNum']
                        dlockWaitNum.append(lockWaitNum)
                        insert_if_not_exists(targetId, 2850041, [dict(name=node,value=cs(lockWaitNum))])
                        # insert_if_not_exists(uid ,index_id = 2850041, value=cs(lockWaitNum))
                if dlockWaitNum:
                    # 最大值，最小值，平均值，汇总
                    insert_if_not_exists(targetId, 2850041, [dict(name='max',value=cs(max(dlockWaitNum)))])
                    insert_if_not_exists(targetId, 2850041, [dict(name='min',value=cs(min(dlockWaitNum)))])
                    insert_if_not_exists(targetId, 2850041, [dict(name='avg',value=cs(round(sum(dlockWaitNum)/len(dlockWaitNum),2)))])
                    insert_if_not_exists(targetId, 2850041, [dict(name='total',value=cs(sum(dlockWaitNum)))])
                else:
                    insert_if_not_exists(targetId, 2850041, [dict(name='max',value=cs(0))])
                    insert_if_not_exists(targetId, 2850041, [dict(name='min',value=cs(0))])
                    insert_if_not_exists(targetId, 2850041, [dict(name='avg',value=cs(0))])
                    insert_if_not_exists(targetId, 2850041, [dict(name='total',value=cs(0))])


def get_all_dns(db, dnInfo, num, instanceType):
    "从CN节点采集所有DN分片信息"
    storage_str = ""
    if instanceType == 1:
        storage_str = f" storagedb g{num}"
    sql = f"""
        select
        case VARIABLE_NAME
        when 'ABORTED_CLIENTS'
            then '2852001'
        when 'ABORTED_CONNECTS'
            then '2852002'
        when 'BYTES_RECEIVED'
            then '2852003'
        when 'BYTES_SENT'
            then '2852004'
        when 'CONNECTIONS'
            then '2852005'
        when 'QCACHE_HITS'
            then '2852006'
        when 'QCACHE_INSERTS'
            then '2852007'
        when 'COM_SELECT'
            then '2852008'
        when 'FLUSH_COMMANDS'
            then '2852134'
        when 'COM_STMT_PREPARE'
            then '2852010'
        when 'COM_STMT_EXECUTE'
            then '2852011'
        when 'COM_STMT_CLOSE'
            then '2852012'
        when 'COM_COMMIT'
            then '2852013'
        when 'COM_ROLLBACK'
            then '2852014'
        when 'QUESTIONS'
            then '2852015'
        when 'QUERIES'
            then '2852016'
        when 'HANDLER_READ_FIRST'
            then '2852017'
        when 'HANDLER_READ_KEY'
            then '2852018'
        when 'HANDLER_READ_LAST'
            then '2852019'
        when 'HANDLER_READ_NEXT'
            then '2852020'
        when 'HANDLER_READ_PREV'
            then '2852021'
        when 'HANDLER_READ_RND'
            then '2852022'
        when 'HANDLER_READ_RND_NEXT'
            then '2852023'
        when 'SELECT_FULL_JOIN'
            then '2852024'
        when 'SELECT_FULL_RANGE_JOIN'
            then '2852025'
        when 'SELECT_RANGE'
            then '2852026'
        when 'SELECT_SCAN'
            then '2852027'
        when 'SELECT RANGE CHECK'
            then '2852028'
        when 'SORT_RANGE'
            then '2852029'
        when 'SORT_SCAN'
            then '2852030'
        when 'SORT_ROWS'
            then '2852031'
        when 'SORT_MERGE_PASSES'
            then '2852032'
        when 'INNODB_ROWS_DELETED'
            then '2852033'
        when 'INNODB_ROWS_INSERTED'
            then '2852034'
        when 'INNODB_ROWS_UPDATED'
            then '2852035'
        when 'INNODB_ROWS_READ'
            then '2852036'
        when 'INNODB_BUFFER_POOL_READ_REQUESTS'
            then '2852037'
        when 'INNODB_BUFFER_POOL_READS'
            then '2852038'
        when 'INNODB_BUFFER_POOL_WAIT_FREE'
            then '2852039'
        when 'INNODB_BUFFER_POOL_WRITE_REQUESTS'
            then '2852040'
        when 'INNODB_BUFFER_POOL_PAGES_FREE'
            then '2852041'
        when 'INNODB_BUFFER_POOL_PAGES_TOTAL'
            then '2852042'
        when 'INNODB_DATA_READS'
            then '2852043'
        when 'INNODB_DATA_READ'
            then '2852044'
        when 'INNODB_DATA_PENDING_READS'
            then '2852045'
        when 'INNODB_DATA_WRITES'
            then '2852046'
        when 'INNODB_DATA_WRITTEN'
            then '2852047'
        when 'INNODB_DATA_FSYNCS'
            then '2852048'
        when 'INNODB_DATA_PENDING_WRITES'
            then '2852049'
        when 'INNODB_DATA_PENDING_FSYNCS'
            then '2852050'
        when 'INNODB_DBLWR_WRITES'
            then '2852051'
        when 'INNODB_DBLWR_PAGES_WRITTEN'
            then '2852052'
        when 'INNODB_LOG_WAITS'
            then '2852053'
        when 'INNODB_LOG_WRITE_REQUESTS'
            then '2852054'
        when 'INNODB_LOG_WRITES'
            then '2852055'
        when 'INNODB_OS_LOG_WRITTEN'
            then '2852056'
        when 'INNODB_OS_LOG_FSYNCS'
            then '2852057'
        when 'INNODB_OS_LOG_PENDING_WRITES'
            then '2852058'
        when 'INNODB_OS_LOG_PENDING_FSYNCS'
            then '2852059'
        when 'INNODB_ROW_LOCK_TIME'
            then '2852060'
        when 'INNODB_ROW_LOCK_TIME_AVG'
            then '2852061'
        when 'INNODB_ROW_LOCK_WAITS'
            then '2852062'
        when 'INNODB_ROW_LOCK_CURRENT_WAITS'
            then '2852063'
        when 'TABLE_LOCKS_IMMEDIATE'
            then '2852064'
        when 'TABLE_LOCKS_WAITED'
            then '2852065'
        when 'CREATED_TMP_DISK_TABLES'
            then '2852066'
        when 'CREATED_TMP_TABLES'
            then '2852067'
        when 'CREATED_TMP_FILES'
            then '2852068'
        when 'THREADS_RUNNING'
            then '2852069'
        when 'THREADS_CONNECTED'
            then '2852070'
        when 'THREADS_CREATED'
            then '2852071'
        when 'OPENED_FILES'
            then '2852072'
        when 'OPENED_TABLES'
            then '2852073'
        when 'OPENED_TABLE_DEFINITIONS'
            then '2852074'
        when 'OPEN_FILES'
            then '2852075'
        when 'OPEN_TABLES'
            then '2852076'
        when 'OPEN_TABLE_DEFINITIONS'
            then '2852077'
        when 'TABLE_OPEN_CACHE_HITS'
            then '2852078'
        when 'TABLE_OPEN_CACHE_MISSES'
            then '2852079'
        when 'TABLE_OPEN_CACHE_OVERFLOWS'
            then '2852080'
        when 'PREPARED_STMT_COUNT'
            then '2852081'
        when 'KEY_READS'
            then '2852082'
        when 'KEY_READ_REQUESTS'
            then '2852083'
        when 'KEY_WRITES'
            then '2852084'
        when 'KEY_WRITE_REQUESTS'
            then '2852085'
        when 'KEY_BLOCKS_UNUSED'
            then '2852086'
        when 'SLOW_QUERIES'
            then '2852087'
        when 'SLOW_LAUNCH_THREADS'
            then '2852088'
        when 'MAX_EXECUTION_TIME_EXCEEDED'
            then '2852089'
        when 'LOCKED_CONNECTS'
            then '2852090'
        when 'BINLOG_CACHE_DISK_USE'
            then '2852091'
        when 'BINLOG_CACHE_USE'
            then '2852092'
        when 'BINLOG_STMT_CACHE_DISK_USE'
            then '2852093'
        when 'BINLOG_STMT_CACHE_USE'
            then '2852094'
        when 'INNODB_AVAILABLE_UNDO_LOGS'
            then '2852095'
        when 'KEY_BLOCKS_UNUSED'
            then '2852102'
        when 'UPTIME'
            then '2852199'
        when 'UPTIME_SINCE_FLUSH_STATUS'
            then '2852200'
        when 'INNODB_PAGE_SIZE' then '2852109'
        when 'INNODB_BUFFER_POOL_PAGES_DATA' then '2852119'
        when 'INNODB_BUFFER_POOL_PAGES_MISC' then '2852120'
        when 'INNODB_BUFFER_POOL_PAGES_DIRTY' then '2852121'
        when 'INNODB_BUFFER_POOL_PAGES_FLUSHED' then '2852122'
        when 'INNODB_PAGES_CREATED' then '2852123'
        when 'INNODB_PAGES_READ' then '2852124'
        when 'INNODB_PAGES_WRITTEN' then '2852125'
        when 'QCACHE_FREE_BLOCKS' then '2852129'
        when 'QCACHE_FREE_MEMORY' then '2852130'
        when 'QCACHE_LOWMEM_PRUNES' then '2852131'
        when 'PERFORMANCE_SCHEMA_HOSTS_LOST' then '2852132'
        else VARIABLE_NAME end as name,
        VARIABLE_VALUE         as value
        from performance_schema.global_status
        where VARIABLE_NAME in (
        'ABORTED_CLIENTS',
        'ABORTED_CONNECTS',
        'BYTES_RECEIVED',
        'BYTES_SENT',
        'CONNECTIONS',
        'QCACHE_HITS',
        'QCACHE_INSERTS',
        'COM_SELECT',
        'FLUSH_COMMANDS',
        'COM_STMT_PREPARE',
        'COM_STMT_EXECUTE',
        'COM_STMT_CLOSE',
        'COM_COMMIT',
        'COM_ROLLBACK',
        'QUESTIONS',
        'QUERIES',
        'HANDLER_READ_FIRST',
        'HANDLER_READ_KEY',
        'HANDLER_READ_LAST',
        'HANDLER_READ_NEXT',
        'HANDLER_READ_PREV',
        'HANDLER_READ_RND',
        'HANDLER_READ_RND_NEXT',
        'SELECT_FULL_JOIN',
        'SELECT_FULL_RANGE_JOIN',
        'SELECT_RANGE',
        'SELECT_SCAN',
        'SELECT RANGE CHECK',
        'SORT_RANGE',
        'SORT_SCAN',
        'SORT_ROWS',
        'SORT_MERGE_PASSES',
        'INNODB_ROWS_DELETED',
        'INNODB_ROWS_INSERTED',
        'INNODB_ROWS_UPDATED',
        'INNODB_ROWS_READ',
        'INNODB_BUFFER_POOL_READ_REQUESTS',
        'INNODB_BUFFER_POOL_READS',
        'INNODB_BUFFER_POOL_WAIT_FREE',
        'INNODB_BUFFER_POOL_WRITE_REQUESTS',
        'INNODB_BUFFER_POOL_PAGES_FREE',
        'INNODB_BUFFER_POOL_PAGES_TOTAL',
        'INNODB_DATA_READS',
        'INNODB_DATA_READ',
        'INNODB_DATA_PENDING_READS',
        'INNODB_DATA_WRITES',
        'INNODB_DATA_WRITTEN',
        'INNODB_DATA_FSYNCS',
        'INNODB_DATA_PENDING_WRITES',
        'INNODB_DATA_PENDING_FSYNCS',
        'INNODB_DBLWR_WRITES',
        'INNODB_DBLWR_PAGES_WRITTEN',
        'INNODB_LOG_WAITS',
        'INNODB_LOG_WRITE_REQUESTS',
        'INNODB_LOG_WRITES',
        'INNODB_OS_LOG_WRITTEN',
        'INNODB_OS_LOG_FSYNCS',
        'INNODB_OS_LOG_PENDING_WRITES',
        'INNODB_OS_LOG_PENDING_FSYNCS',
        'INNODB_ROW_LOCK_TIME',
        'INNODB_ROW_LOCK_TIME_AVG',
        'INNODB_ROW_LOCK_WAITS',
        'INNODB_ROW_LOCK_CURRENT_WAITS',
        'TABLE_LOCKS_IMMEDIATE',
        'TABLE_LOCKS_WAITED',
        'CREATED_TMP_DISK_TABLES',
        'CREATED_TMP_TABLES',
        'CREATED_TMP_FILES',
        'THREADS_RUNNING',
        'THREADS_CONNECTED',
        'THREADS_CREATED',
        'OPENED_FILES',
        'OPENED_TABLES',
        'OPENED_TABLE_DEFINITIONS',
        'OPEN_FILES',
        'OPEN_TABLES',
        'OPEN_TABLE_DEFINITIONS',
        'TABLE_OPEN_CACHE_HITS',
        'TABLE_OPEN_CACHE_MISSES',
        'TABLE_OPEN_CACHE_OVERFLOWS',
        'PREPARED_STMT_COUNT',
        'KEY_READS',
        'KEY_READ_REQUESTS',
        'KEY_WRITES',
        'KEY_WRITE_REQUESTS',
        'KEY_BLOCKS_UNUSED',
        'SLOW_QUERIES',
        'SLOW_LAUNCH_THREADS',
        'MAX_EXECUTION_TIME_EXCEEDED',
        'LOCKED_CONNECTS',
        'BINLOG_CACHE_DISK_USE',
        'BINLOG_CACHE_USE',
        'BINLOG_STMT_CACHE_DISK_USE',
        'BINLOG_STMT_CACHE_USE',
        'INNODB_AVAILABLE_UNDO_LOGS',
        'KEY_BLOCKS_UNUSED',
        'INNODB_PAGE_SIZE',
        'INNODB_BUFFER_POOL_PAGES_DATA',
        'INNODB_BUFFER_POOL_PAGES_MISC',
        'INNODB_BUFFER_POOL_PAGES_DIRTY',
        'INNODB_BUFFER_POOL_PAGES_FLUSHED',
        'INNODB_PAGES_CREATED',
        'INNODB_PAGES_READ',
        'INNODB_PAGES_WRITTEN',
        'QCACHE_FREE_BLOCKS',
        'QCACHE_FREE_MEMORY',
        'QCACHE_LOWMEM_PRUNES',
        'PERFORMANCE_SCHEMA_HOSTS_LOST',
        'UPTIME',
        'UPTIME_SINCE_FLUSH_STATUS'
        ) {storage_str};
    """
    cur = DBUtil.getValue(db, sql)
    rs = cur.fetchall()
    uid = get_uid_by_ip(dnInfo['dbIp'], dnInfo['dbPort'])
    for r in rs:
        index_id = r[0]
        value = r[1]
        if index_id == '2852199':
            uptime.append(value)
        elif index_id == '2852070':
            threads_connect.append(float(value))
            sql = f"select VARIABLE_VALUE  from performance_schema.global_variables where VARIABLE_NAME = 'MAX_CONNECTIONS' {storage_str}"
            cur = DBUtil.getValue(db, sql)
            rs = cur.fetchone()
            if rs:
                conn_usage = round(float(value) / float(rs[0]) * 100,2)
                conn_used.append(conn_usage)
                insert_if_not_exists(targetId, 2850045, [dict(name=dnInfo['dbIp'] + ':' + str(dnInfo['dbPort']),value=cs(conn_usage))])
        elif index_id == '2852069':
            threads_running.append(float(value))
        insert_if_not_exists(uid, index_id.replace('2852','2850'), value)
        insert_if_not_exists(targetId, index_id, [dict(name=dnInfo['dbIp'] + ':' + str(dnInfo['dbPort']),value=cs(value))])


variables_dict = {'admin_commands': 2851002, 'assign_to_keycache': 2851004, 'alter_db': 2851006, 'alter_event': 2851008, 'alter_function': 2851010, 'alter_instance': 2851012, 'alter_procedure': 2851014, 'alter_resource_group': 2851016, 'alter_server': 2851018, 'alter_table': 2851020, 'alter_tablespace': 2851022, 'alter_user': 2851024, 'alter_user_default_role': 2851026, 'analyze': 2851028, 'begin': 2851030, 'binlog': 2851032, 'call_procedure': 2851034, 'change_db': 2851036, 'change_master': 2851038, 'change_repl_filter': 2851040, 'change_replication_source': 2851042, 'check': 2851044, 'checksum': 2851046, 'clone': 2851048, 'commit': 2851050, 'create_db': 2851052, 'create_event': 2851054, 'create_function': 2851056, 'create_index': 2851058, 'create_procedure': 2851060, 'create_role': 2851062, 'create_server': 2851064, 'create_table': 2851066, 'create_resource_group': 2851068, 'create_trigger': 2851070, 'create_udf': 2851072, 'create_user': 2851074, 'create_view': 2851076, 'create_spatial_reference_system': 2851078, 'dealloc_sql': 2851080, 'delete': 2851082, 'delete_multi': 2851084, 'do': 2851086, 'drop_db': 2851088, 'drop_event': 2851090, 'drop_function': 2851092, 'drop_index': 2851094, 'drop_procedure': 2851096, 'drop_resource_group': 2851098, 'drop_role': 2851100, 'drop_server': 2851102, 'drop_spatial_reference_system': 2851104, 'drop_table': 2851106, 'drop_trigger': 2851108, 'drop_user': 2851110, 'drop_view': 2851112, 'empty_query': 2851114, 'execute_sql': 2851116, 'explain_other': 2851118, 'flush': 2851120, 'get_diagnostics': 2851122, 'grant': 2851124, 'grant_roles': 2851126, 'ha_close': 2851128, 'ha_open': 2851130, 'ha_read': 2851132, 'help': 2851134, 'import': 2851136, 'insert': 2851138, 'insert_select': 2851140, 'install_component': 2851142, 'install_plugin': 2851144, 'kill': 2851146, 'load': 2851148, 'lock_instance': 2851150, 'lock_tables': 2851152, 'merge_into': 2851154, 'optimize': 2851156, 'preload_keys': 2851158, 'prepare_sql': 2851160, 'purge': 2851162, 'purge_before_date': 2851164, 'release_savepoint': 2851166, 'rename_table': 2851168, 'flashback_table': 2851170, 'purge_table': 2851172, 'rename_user': 2851174, 'repair': 2851176, 'replace': 2851178, 'replace_select': 2851180, 'reset': 2851182, 'resignal': 2851184, 'restart': 2851186, 'revoke': 2851188, 'revoke_all': 2851190, 'revoke_roles': 2851192, 'rollback': 2851194, 'rollback_to_savepoint': 2851196, 'savepoint': 2851198, 'select': 2851200, 'set_option': 2851202, 'set_password': 2851204, 'set_resource_group': 2851206, 'set_role': 2851208, 'signal': 2851210, 'show_binlog_events': 2851212, 'show_binlogs': 2851214, 'show_binlog_gtidset': 2851216, 'show_charsets': 2851218, 'show_collations': 2851220, 'show_create_db': 2851222, 'show_create_event': 2851224, 'show_create_func': 2851226, 'show_create_proc': 2851228, 'show_create_table': 2851230, 'show_create_trigger': 2851232, 'show_databases': 2851234, 'show_engine_logs': 2851236, 'show_engine_mutex': 2851238, 'show_engine_status': 2851240, 'show_events': 2851242, 'show_errors': 2851244, 'show_fields': 2851246, 'show_function_code': 2851248, 'show_function_status': 2851250, 'show_grants': 2851252, 'show_keys': 2851254, 'show_master_status': 2851256, 'show_open_tables': 2851258, 'show_package_status': 2851260, 'show_package_body_status': 2851262, 'show_plugins': 2851264, 'show_privileges': 2851266, 'show_procedure_code': 2851268, 'show_procedure_status': 2851270, 'show_processlist': 2851272, 'show_profile': 2851274, 'show_profiles': 2851276, 'show_relaylog_events': 2851278, 'show_replicas': 2851280, 'show_slave_hosts': 2851282, 'show_replica_status': 2851284, 'show_slave_status': 2851286, 'show_status': 2851288, 'show_storage_engines': 2851290, 'show_table_status': 2851292, 'show_tables': 2851294, 'show_triggers': 2851296, 'show_variables': 2851298, 'show_warnings': 2851300, 'show_create_user': 2851302, 'shutdown': 2851304, 'replica_start': 2851306, 'slave_start': 2851308, 'replica_stop': 2851310, 'slave_stop': 2851312, 'group_replication_start': 2851314, 'group_replication_stop': 2851316, 'stmt_execute': 2851318, 'stmt_batch_execute': 2851320, 'stmt_close': 2851322, 'stmt_fetch': 2851324, 'stmt_prepare': 2851326, 'stmt_reset': 2851328, 'stmt_send_long_data': 2851330, 'truncate': 2851332, 'uninstall_component': 2851334, 'uninstall_plugin': 2851336, 'unlock_instance': 2851338, 'unlock_tables': 2851340, 'update': 2851342, 'update_multi': 2851344, 'xa_commit': 2851346, 'xa_end': 2851348, 'xa_prepare': 2851350, 'xa_recover': 2851352, 'xa_rollback': 2851354, 'xa_start': 2851356, 'execute_immediate': 2851358, 'call_declare_block': 2851360, 'create_profile': 2851362, 'alter_profile': 2851364, 'drop_profile': 2851366, 'show_user_profile': 2851368, 'copy_table': 2851370, 'show_quicksync_status': 2851372, 'show_threadpool_status': 2851374, 'show_preparedstmtpool_status': 2851376, 'show_slave_sync_replay_status': 2851378, 'blacklist': 2851380, 'outline': 2851382, 'create_sequence': 2851384, 'alter_sequence': 2851386, 'drop_sequence': 2851388, 'show_tcmalloc_status': 2851390, 'show_slow_low_status': 2851392, 'stmt_reprepare': 2851394}


def get_global_statsus(db, dnInfo,num , instanceType):
    storage_str = ""
    if instanceType == 1:
        storage_str = f" storagedb g{num}"
    sql = f"show global status like 'Com_%' {storage_str}"
    cur = DBUtil.getValue(db, sql)
    rs = cur.fetchall()
    for r in rs:
        variable_name = r[0]
        value = r[1]
        uid = get_uid_by_ip(dnInfo['dbIp'], dnInfo['dbPort'])
        index_id = variables_dict.get(variable_name.replace('Com_',''))
        if index_id:
            insert_if_not_exists(uid, index_id, value)
            insert_if_not_exists(targetId, index_id, [dict(name=dnInfo['dbIp'] + ':' + str(dnInfo['dbPort']),value=cs(value))])

def get_tbs_size(db, dnInfo,num , instanceType):
    storage_str = ""
    if instanceType == 1:
        storage_str = f" storagedb g{num}"
    sql = f"""
        select
            sum(file_size)
        from
            information_schema.INNODB_TABLESPACES
        where SPACE_TYPE = 'General'
        {storage_str}"""
    cur = DBUtil.getValue(db, sql)
    rs = cur.fetchall()
    for r in rs:
        value = r[0]
        uid = get_uid_by_ip(dnInfo['dbIp'], dnInfo['dbPort'])
        insert_if_not_exists(uid, 2850454, value)
        insert_if_not_exists(targetId, 2850454, [dict(name=dnInfo['dbIp'] + ':' + str(dnInfo['dbPort']),value=cs(value))])
    sql = f"""
        select
            sum(file_size)
        from
            information_schema.INNODB_TABLESPACES
        where SPACE_TYPE = 'System'
        {storage_str}"""
    cur = DBUtil.getValue(db, sql)
    rs = cur.fetchall()
    for r in rs:
        value = r[0]
        uid = get_uid_by_ip(dnInfo['dbIp'], dnInfo['dbPort'])
        insert_if_not_exists(uid, 2850455, value)
        insert_if_not_exists(targetId, 2850455, [dict(name=dnInfo['dbIp'] + ':' + str(dnInfo['dbPort']),value=cs(value))])


def get_delay_from_es(ip, clusterId, dn_count):
    "通过ES采集GDB延迟信息"
    es = Elasticsearch(f"http://{ip}:9200",http_auth=('elastic', 'Insight@2021_es'), timeout=20)

    # 定义查询语句，按照 timeStamp 降序排列，获取第一条数据
    query = {
    "sort": [
        {
            "timeStamp": {
                "order": "desc"
            }
        }
    ],
    "size": dn_count,
    "query": {
        "bool": {
            "filter": [
                {
                    "term": {
                        "clusterId": clusterId
                    }
                }
            ]
        }
    }
}

    try:
        result = es.search(index='insight-dbstatdelayinfo', body=query)
        # 获取结果
        if result['hits']['total'] > 0:
            sync_delay_list = result['hits']['hits']
            dn_dict = DBUtil.get_tenancy_dn_info(pg, targetId)
            for row in sync_delay_list:
                res = row['_source']
                dbRole = res['dbRole']
                if dbRole == 0:
                    role = 'slave'
                else:
                    role = 'master'
                hlwm = res['hlwm']
                timeStamp = res['timeStamp']
                syncLogGap = res['syncLogGap']
                relayLogGap = res['relayLogGap']
                syncLogDelayTime = res['syncLogDelayTime']
                relayLogDelayTime = res['relayLogDelayTime']
                dbid = res['dbId']
                # 判断采集时间不超过10分钟
                if (datetime.now() - datetime.strptime(timeStamp,'%Y-%m-%d %H:%M:%S')).seconds < 600:
                    if dn_dict is not None:
                        dn = dn_dict[str(dbid)] + '-' + role
                        insert_if_not_exists(targetId, 2850035, [dict(name=dn, value=cs(dbRole))])
                        insert_if_not_exists(targetId, 2850036, [dict(name=dn, value=cs(hlwm))])
                        insert_if_not_exists(targetId, 2850037, [dict(name=dn, value=cs(syncLogDelayTime))])
                        insert_if_not_exists(targetId, 2850038, [dict(name=dn, value=cs(syncLogGap))])
                        insert_if_not_exists(targetId, 2850039, [dict(name=dn, value=cs(relayLogDelayTime))])
                        insert_if_not_exists(targetId, 2850040, [dict(name=dn, value=cs(relayLogGap))])
    except Exception as e:
        log.warning(f"{ip}, {clusterId} get_delay_from_es error:{e}")


def get_proxystat_from_es(ip, clusterId):
    es = Elasticsearch(f"http://{ip}:9200",http_auth=('elastic', 'Insight@2021_es'), timeout=20)

    # 定义查询语句，按照 timeStamp 降序排列，获取第一条数据
    query = {
    "sort": [
        {
            "endTime": {
                "order": "desc"
            }
        }
    ],
    "size": 1,
    "query": {
        "bool": {
            "filter": [
                {
                    "term": {
                        "reserved1": clusterId
                    }
                }
            ]
        }
    }
}

    try:
        result = es.search(index='insight-dbproxystatistic', body=query)
        # 获取结果
        if result['hits']['total'] > 0:
            res = result['hits']['hits'][0]['_source']
            endTime = res['endTime']
            tps = res['statistic1']
            totalTrans = res['statistic2']
            failTrans = res['statistic3']
            disTrans = res['statistic4']
            disTransAbcommit = res['statistic5']
            disWriteTrans = res['statistic6']
            nonDisWriteTrans = res['statistic7']
            totalStatements = res['statistic8']
            pressedStatments = res['statistic9']
            crossNodeDisWtrans = res['statistic10']
            nonCrossNodeWtrans = res['statistic11']
            qpsRead = res['statistic12']
            qpsWrite = res['statistic13']
            # 判断采集时间不超过10分钟
            if endTime > (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() - 600))):
                    insert_if_not_exists(targetId, 2850001, cs(tps))
                    insert_if_not_exists(targetId, 2850002, cs(totalTrans))
                    insert_if_not_exists(targetId, 2850003, cs(failTrans))
                    insert_if_not_exists(targetId, 2850004, cs(disTrans))
                    insert_if_not_exists(targetId, 2850042, cs(disTransAbcommit))
                    insert_if_not_exists(targetId, 2850005, cs(disWriteTrans))
                    insert_if_not_exists(targetId, 2850006, cs(nonDisWriteTrans))
                    insert_if_not_exists(targetId, 2850007, cs(totalStatements))
                    insert_if_not_exists(targetId, 2850008, cs(pressedStatments))
                    insert_if_not_exists(targetId, 2850009, cs(crossNodeDisWtrans))
                    insert_if_not_exists(targetId, 2850010, cs(nonCrossNodeWtrans))
                    insert_if_not_exists(targetId, 2850011, cs(qpsRead))
                    insert_if_not_exists(targetId, 2850012, cs(qpsWrite))
            else:
                log.warning(f"{ip}, {clusterId} dbproxystatistic index time is too old, time is {endTime}")

    except Exception as e:
        log.warning(f"{ip}, {clusterId} get_proxystat_from_es error:{e}")


def get_dbstat_from_es(ip, clusterId):
    es = Elasticsearch(f"http://{ip}:9200",http_auth=('elastic', 'Insight@2021_es'), timeout=20)

    # 定义查询语句，按照 timeStamp 降序排列，获取第一条数据
    query = {
    "sort": [
        {
            "endTime": {
                "order": "desc"
            }
        }
    ],
    "size": 1,
    "query": {
        "bool": {
            "filter": [
                {
                    "term": {
                        "reserved1": clusterId
                    }
                }
            ]
        }
    }
}
    try:
        result = es.search(index='insight-dbstatistic', body=query)
    # 获取结果
        if result['hits']['total'] > 0:
            res = result['hits']['hits'][0]['_source']
            dbRole = res['reserved2']
            selectNum = res['statistic1']
            updateNum = res['statistic2']
            deleteNum = res['statistic3']
            insertNum = res['statistic4']
            tableLockConflictRate = res['statistic5']
            rowlockAvgWaitTime = res['statistic6']
            bufferDirtPageRate = res['statistic7']
            bufferHitRate = res['statistic8']
            tempTableUsedNum = res['statistic9']
            fileTempTableUsedRate = res['statistic10']
            binlogDiskUsedStat = res['statistic11']
            redoLogWaitStat = res['statistic12']
            insert_if_not_exists(targetId, 2850043, cs(dbRole))
            insert_if_not_exists(targetId, 2850014, cs(selectNum))
            insert_if_not_exists(targetId, 2850015, cs(updateNum))
            insert_if_not_exists(targetId, 2850016, cs(deleteNum))
            insert_if_not_exists(targetId, 2850017, cs(tableLockConflictRate))
            insert_if_not_exists(targetId, 2850018, cs(rowlockAvgWaitTime))
            insert_if_not_exists(targetId, 2850019, cs(bufferDirtPageRate))
            insert_if_not_exists(targetId, 2850020, cs(bufferHitRate))
            insert_if_not_exists(targetId, 2850021, cs(tempTableUsedNum))
            insert_if_not_exists(targetId, 2850022, cs(fileTempTableUsedRate))
            insert_if_not_exists(targetId, 2850023, cs(binlogDiskUsedStat))
            insert_if_not_exists(targetId, 2850024, cs(redoLogWaitStat))
    except Exception as e:
        log.warning(f"{ip}, {clusterId} get_dbstat_from_es error:{e}")


def update_db_role(pg, dn):
    ip = dn['dbIp']
    port = dn['dbPort']
    num = dn['num']
    primary_ip = None
    primary_port = None
    is_display = 'false'
    if num == -1:
        primary_ip = dn['primaryIp']
        primary_port = dn['primaryPort']
    target_id = get_uid_by_ip(ip, port, primary_ip, primary_port)
    sql = f"select cib_value from p_normal_cib pnc where target_id = '{target_id}' and index_id = 1000005 and cib_name = 'onDashBoard'"
    cusr = DBUtil.getValue(pg, sql)
    rs = cusr.fetchall()
    cur = pg.conn.cursor()
    if rs:
        sql2 = f"update p_normal_cib set cib_value = '{is_display}',record_time='{cur_time}' where target_id = '{target_id}' and index_id = 1000005 and cib_name = 'onDashBoard'"
    else:
        sql2 = f"insert into p_normal_cib(target_id, index_id, cib_name, cib_value,record_time) values('{target_id}', 1000005, 'onDashBoard', '{is_display}','{cur_time}')"
    cur.execute(sql2)
    pg.conn.commit()

def os_cluster(db, uid):
    mets = {}
    cnmets = {}
    dnmets = {}
    cnt = 0
    suc = 0
    hs = {}
    cnhs = set()
    dnhs = set()
    sql = "select cib_name,cib_value from p_normal_cib where target_id='%s' and index_id=1000001 and cib_name in ('_ips','_cnips','_dnips')" % uid
    cs1 = DBUtil.getValue(db, sql)
    rs = cs1.fetchall()
    ips = set()
    cnips = set()
    dnips = set()
    ctime = time.time()
    if rs:
        for row in rs:
            arr = row[1].split(',')
            if row[0] == '_ips':
                for ip in arr:
                    ips.add(ip)
            elif row[0] == '_cnips':
                for ip in arr:
                    cnips.add(ip)
            else:
                for ip in arr:
                    dnips.add(ip)
        sql = "select in_ip,uid from mgt_device where in_ip in %s and use_flag" % tuple2(ips, True)
        cs2 = DBUtil.getValue(db, sql)
        rs2 = cs2.fetchall()
        if rs2:
            for row in rs2:
                hs[row[1]] = row[0]
                cnt += 1
                if row[0] in cnips:
                    cnhs.add(row[1])
                if row[0] in dnips:
                    dnhs.add(row[1])
    rfs = []
    disk_fs = []
    fs_inode = []
    disk_size = []
    time.sleep(5)
    for id in hs.keys():
        sql = '''select index_id,value,record_time,iname from mon_indexdata where uid='%s' and index_id in (
3000300,3000303,3000000,3000301,3000009,3000003,3000004,3000005,3000006,3000007,3001031,3000100,3000101,3000209,3000021,3000018,3000019,3000014,3000015
)''' % id
        cs2 = DBUtil.getValue(db, sql)
        rs2 = cs2.fetchall()
        met = {}
        if rs2:
            for row in rs2:
                # ts = time.mktime(row[2].timetuple())
                if row[0] != 3000000:
                    if time.mktime(row[2].timetuple()) > ctime - 600:
                        if row[0] == 3000005:
                            rfs.append(dict(name=hs[id], value=row[1]))
                        elif row[0] == 3000300:
                            disk_fs.append(dict(name=hs[id] + '-' + row[3], value=row[1]))
                        elif row[0] == 3000301:
                            fs_inode.append(dict(name=hs[id] + '-' + row[3], value=row[1]))
                        elif row[0] == 3000303:
                            disk_size.append(dict(name=hs[id] + '-' + row[3], value=row[1]))
                        elif row[0] in [3000100,3000003,3000006,3000004,3000014]:
                            insert_if_not_exists(targetId, str(1001000 + (row[0] % 1000)), value=[dict(name=hs[id], value=row[1])])
                        if met.get(row[0]) is not None:
                            met[row[0]].append(float(row[1]))
                        else:
                            met[row[0]] = [float(row[1])]
                else:
                    met[row[0]] = [row[0], row[1], row[2]]
        if met.get(3000000) is None or time.mktime(met[3000000][2].timetuple()) < ctime - 600:
            continue
        if met[3000000][1] != '连接成功':
            continue
        del met[3000000]
        suc += 1
        for k in met.keys():
            if k == 3000021:
                adj = 0
                mv = met[k]
                for i in range(len(mv)):
                    if mv[i] < 0 and mv[i] < adj:
                        adj = mv[i]
                if adj < 0:
                    for i in range(len(mv)):
                        mv[i] -= adj                
            if mets.get(k) is not None:
                mets[k] += met[k]
            else:
                mets[k] = met[k]
            if id in cnhs:
                if cnmets.get(k) is not None:
                    cnmets[k] += met[k]
                else:
                    cnmets[k] = met[k]
            if id in dnhs:
                if dnmets.get(k) is not None:
                    dnmets[k] += met[k]
                else:
                    dnmets[k] = met[k]
    if suc > 0:
        for k in mets.keys():
            vals = []
            # if k not in [3000005,3000300]:
            vals.append(dict(name="min", value=str(numpy.min(mets[k]))))
            vals.append(dict(name="max", value=str(numpy.max(mets[k]))))
            vals.append(dict(name="avg", value=str(round(numpy.mean(mets[k]),3))))
            vals.append(dict(name="std", value=str(round(numpy.std(mets[k]),3))))
            if k in [3000100,3000003,3000006,3000004]:
                if cnmets.get(k):
                    vals.append(dict(name="cn_min", value=str(numpy.min(cnmets[k]))))
                    vals.append(dict(name="cn_max", value=str(numpy.max(cnmets[k]))))
                    vals.append(dict(name="cn_avg", value=str(round(numpy.mean(cnmets[k]),3))))
                if dnmets.get(k):
                    vals.append(dict(name="dn_min", value=str(numpy.min(dnmets[k]))))
                    vals.append(dict(name="dn_max", value=str(numpy.max(dnmets[k]))))
                    vals.append(dict(name="dn_avg", value=str(round(numpy.mean(dnmets[k]),3))))
            insert_if_not_exists(targetId, str(1001000 + (k % 1000)), value=vals)
    if rfs:
        insert_if_not_exists(targetId, '1001005', value=rfs)
    if disk_fs:
        insert_if_not_exists(targetId, '1000300', value=disk_fs)
    if fs_inode:
        insert_if_not_exists(targetId, '1000301', value=fs_inode)
    if disk_size:
        insert_if_not_exists(targetId, '1000303', value=disk_size)
    insert_if_not_exists(targetId, '1001999', value=str(cnt))
    insert_if_not_exists(targetId, '1001998', value=str(suc))


def get_gdb_version(conn):
    sql = '''show variables like 'goldendb_version' '''
    cs1 = DBUtil.getValue(conn, sql)
    gdb_version = cs1.fetchone()[1]
    gdb_main_version_list = gdb_version.split('-')[1].split('.')[0:-1]
    gdb_main_version = '.'.join(gdb_main_version_list).split('DBV')[1]
    return gdb_main_version


if __name__ == '__main__':
    metric = []
    global_metric = []
    cur_time = datetime.now()
    dbInfo = eval(sys.argv[1])
    targetId, pg = DBUtil.get_pg_env()
    lat_time = datetime.now()
    diff_ms = (lat_time - cur_time).microseconds
    # isInsight = DBUtil.golden_is_insight(pg, targetId)
    db = DBUtil.get_gdb_env(exflag=2)
    insert_if_not_exists(targetId, 1000101, str(round(diff_ms/1000,0)))
    uptime = []
    conn_used = []
    threads_connect = []
    threads_running = []
    os_cluster(pg, targetId)
    if db.conn:
        gdb_version = get_gdb_version(db)
        instanceType = DBUtil.get_gdb_instanceType(db)
        insert_if_not_exists(targetId, 2850000, "连接成功")
        dns = DBUtil.get_golden_dns_by_insight(db)
        for dn in dns:
            ip = dn['dbIp']
            port = dn['dbPort']
            num = dn['num']
            # update_db_role(pg, dn) # 更新主从角色是否显示，从不显示
            if num != -1:
                uid = get_uid_by_ip(dn['dbIp'], dn['dbPort'])
                insert_if_not_exists(uid, 2850000, "连接成功")
                get_all_dns(db, dn, dn['num'], instanceType)
                get_global_statsus(db, dn, dn['num'], instanceType)
                get_tbs_size(db, dn, dn['num'] , instanceType)
        if uptime:
            insert_if_not_exists(targetId, 2850199, cs(max(uptime)))
        if conn_used:
            insert_if_not_exists(targetId, 2850045, [dict(name='max',value=cs(max(conn_used)))])
            insert_if_not_exists(targetId, 2850045, [dict(name='min',value=cs(min(conn_used)))])
        if threads_running:
            insert_if_not_exists(targetId, 2852069, [dict(name='max',value=cs(max(threads_running)))])
            insert_if_not_exists(targetId, 2852069, [dict(name='min',value=cs(min(threads_running)))])
            insert_if_not_exists(targetId, 2852069, [dict(name='avg',value=cs(round(sum(threads_running)/len(threads_running),0)))])
            insert_if_not_exists(targetId, 2852069, [dict(name='total',value=cs(sum(threads_running)))])
        if threads_connect:
            insert_if_not_exists(targetId, 2852070, [dict(name='max',value=cs(max(threads_connect)))])
            insert_if_not_exists(targetId, 2852070, [dict(name='min',value=cs(min(threads_connect)))])
            insert_if_not_exists(targetId, 2852070, [dict(name='avg',value=cs(round(sum(threads_connect)/len(threads_connect),0)))])
            insert_if_not_exists(targetId, 2852070, [dict(name='total',value=cs(sum(threads_connect)))])
        isInsight, insight_ip, insight_port, insight_user, insight_pwd, clusterId = DBUtil.get_insight_info(pg, targetId)
        if isInsight and gdb_version >= '6.1.03':
            base64_pwd = base64.b64encode(decrypt(insight_pwd,1).encode('utf-8')).decode()
            # get_osinfo(insight_ip, insight_user, base64_pwd, insight_port)
            get_monitor_data(insight_ip, insight_user, base64_pwd, insight_port, clusterId)
        else:
            es_ip = DBUtil.get_insight_ip(pg, insight_ip, insight_port)
            if es_ip:
                dn_count = DBUtil.get_tenancy_dn_count(pg, targetId)
                if dn_count is not None:
                    get_delay_from_es(es_ip, clusterId, dn_count)
                else:
                    get_delay_from_es(es_ip, clusterId, 2)
                get_proxystat_from_es(es_ip,clusterId)
                get_dbstat_from_es(es_ip, clusterId)
    else:
        insert_if_not_exists(targetId, 2850000, "连接失败")
    lat_time2 = datetime.now()
    diff_ms2 = (lat_time2 - cur_time).microseconds
    insert_if_not_exists(targetId, 1000102, str(round(diff_ms2/1000,0)))
    print(json.dumps(global_metric))

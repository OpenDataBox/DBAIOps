#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@文件    :cib_goldendb.py
@说明    :
@时间    :2024/06/18 09:27:45
@作者    :xxxx
@版本    :2.0.1
'''
import json
import re
import sys
import base64
import requests
from datetime import datetime
from collections import defaultdict

sys.path.append('/usr/software/knowl')
from JavaRsa import decrypt
import GoldenUtil
from CommUtil import check_mysql_proc
import DBUtil

import warnings

warnings.filterwarnings("ignore")

datadir = ""
ibdir = ""
ibdata = ""
ibtmp = ""
ibtbs = 0
targetId = None


class Result(object):
    # pass
    def __str__(self):
        return "\n".join("{}={}".format(k, getattr(self, k))
                         for k in self.__dict__.keys())


def relate_mysql(db, sql):
    result = Result()
    rs = db.execute(sql)
    if rs.code == 0:
        result.code = rs.code
        result.msg = rs.msg.fetchall()
    else:
        result.code = 1
        result.msg = ''
    return result


def tuple2(arr, f=False):
    s = ''
    for v in arr:
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


def extract_date(index_name):
    match = re.match(r'logstash-(\d{4}\.\d{2}.\d{2})', index_name)
    if match:
        return datetime.strptime(match.group(1), '%Y.%m.%d')
    else:
        return datetime.min  # 返回一个很早的日期作为默认值


def insert_if_not_exists(target_id, index_id, value):
    if target_id:
        if target_id[:4] == '2205':
            index_type = '284'
        else:
            index_type = '221'
        for item in global_metric:
            if item["targetId"] == target_id:
                if value and isinstance(value, list) and 'c1' in value[0].keys():
                    item["results"].append({"index_id": index_type + str(str(index_id)[3:]), "content": value})
                else:
                    item["results"].append({"index_id": index_type + str(str(index_id)[3:]), "value": cs(value)})
                break
        else:
            if isinstance(value, list) and 'c1' in value[0].keys():
                new_entry = {
                    "targetId": target_id,
                    "indexType": index_type,
                    "results": [{"index_id": index_type + str(str(index_id)[3:]), "content": cs(value)}]
                }
            else:
                new_entry = {
                    "targetId": target_id,
                    "indexType": index_type,
                    "results": [{"index_id": index_type + str(str(index_id)[3:]), "value": cs(value)}]
                }
            global_metric.append(new_entry)


def get_uid_by_ip(node_ip, port=None):
    if port:
        sql = f"select uid from mgt_system ms where ip = '{node_ip}' and port='{port}' and use_flag and subuid is not null"
    else:
        sql = f"select uid from mgt_system ms where ip = '{node_ip}' and uid like '2104%' and use_flag and subuid is not null"
    cursor = DBUtil.getValue(pg, sql)
    result = cursor.fetchone()
    uid = None
    if result is not None:
        uid = result[0]
    return uid


def get_goldendb_summary(isInsight, gdb_version, target_ip=None, username=None, base64_pwd=None, port=None,
                         clusterId=None):
    """采集goldendb基本信息
    """
    totalCpu = 0
    totalMem = 0
    vals = []
    vals3 = []
    dnvals = []
    cnvals = []
    gtmvals = []
    ips = set()
    dnips = set()
    cnips = set()
    localtenancyDesc = ""
    ips.add(db_ip)
    if isInsight:
        clusterId = int(clusterId)
        insight_access_ip = None
        cnurl = f"https://{target_ip}:{port}/open_api/insight/container/tenancy/searchCN?clusterId={clusterId}"
        dnurl = f"https://{target_ip}:{port}/open_api/insight/container/tenancy/searchDN?clusterId={clusterId}"
        gtmurl = f"https://{target_ip}:{port}/open_api/insight/container/tenancy/searchGTM?clusterId={clusterId}"
        tenancyurl = f"https://{target_ip}:{port}/open_api/insight/container/tenancy/searchTenancy"
        payload = {}
        headers = {
            'username': username,
            'password': base64_pwd,
            'Content-Type': 'application/json'
        }
        proxies = {
            "http": None,
            "https": None,
        }
        #check_insight
        try:
            dn_reponse = requests.get(dnurl, headers=headers, data=payload, verify=False, timeout=5, proxies=proxies)
        except Exception as e:
            insight_access_ip = DBUtil.get_aviable_insight_ip(pg, insight_ip, insight_port)
            if insight_access_ip is not None:
                cnurl = f"https://{insight_access_ip}:{port}/open_api/insight/container/tenancy/searchCN?clusterId={clusterId}"
                dnurl = f"https://{insight_access_ip}:{port}/open_api/insight/container/tenancy/searchDN?clusterId={clusterId}"
                gtmurl = f"https://{insight_access_ip}:{port}/open_api/insight/container/tenancy/searchGTM?clusterId={clusterId}"
                tenancyurl = f"https://{insight_access_ip}:{port}/open_api/insight/container/tenancy/searchTenancy"

        # DN
        dn_reponse = requests.get(dnurl, headers=headers, data=payload, verify=False, timeout=5, proxies=proxies)
        if dn_reponse and dn_reponse.status_code == 200:
            msg = dn_reponse.json()
            if msg["data"] and isinstance(msg["data"], dict):
                if gdb_version >= '6.1.03':
                    dnvals.append(
                        dict(c1='集群ID', c2='名称', c3='IP', c4='PORT', c5='安装目录', c6='数据目录', c7='日志目录', c8='角色', c9='状态',
                             c10='资源'))
                    for r in msg["data"]['list']:
                        dnvals.append({
                            'c1': r['clusterId'],
                            'c2': cs(r['dbName']),
                            'c3': cs(r['dbIp']),
                            'c4': cs(r['dbPort']),
                            'c5': cs(r['installPath']),
                            'c6': cs(r['dataPath']),
                            'c7': cs(r['dataLogPath']),
                            'c8': cs(r['dbRole']),
                            'c9': cs(r['dbStatus']),
                            'c10': cs(r['resourceUnit'])
                        })
                        ips.add(r['dbIp'])
                        dnips.add(r['dbIp'])
                else:
                    dnvals.append(dict(c1='集群ID', c2='名称', c3='IP', c4='PORT', c5='角色', c6='状态'))
                    for r in msg["data"]['list']:
                        dnvals.append({
                            'c1': r['clusterId'],
                            'c2': cs(r['dbName']),
                            'c3': cs(r['dbIp']),
                            'c4': cs(r['dbPort']),
                            'c5': cs(r['dbRole']),
                            'c6': cs(r['dbStatus'])
                        })
                        ips.add(r['dbIp'])
                        dnips.add(r['dbIp'])
        # CN
        cn_reponse = requests.get(cnurl, headers=headers, data=payload, verify=False, timeout=5, proxies=proxies)
        if cn_reponse and cn_reponse.status_code == 200:
            msg = cn_reponse.json()
            if msg["data"] and isinstance(msg["data"], dict):
                if gdb_version >= '6.1.03':
                    cnvals.append(
                        dict(c1='集群ID', c2='名称', c3='IP', c4='PORT', c5='安装目录', c6='状态', c7='城市', c8='机房', c9='资源',
                             c10='服务端口'))
                    for r in msg["data"]['list']:
                        cnvals.append({
                            'c1': r['clusterId'],
                            'c2': cs(r['cnName']),
                            'c3': cs(r['cnIp']),
                            'c4': cs(r['cnPort']),
                            'c5': cs(r['installPath']),
                            'c6': cs(r['cnStatus']),
                            'c7': cs(r['cityName']),
                            'c8': cs(r['roomName']),
                            'c9': cs(r['resourceUnit']),
                            'c10': cs(r['servicePortList'][0]['servicePort']),
                        })
                        ips.add(r['cnIp'])
                        cnips.add(r['cnIp'])
                else:
                    cnvals.append(dict(c1='集群ID', c2='名称', c3='IP', c4='PORT', c5='状态', c6='城市'))
                    for r in msg["data"]['list']:
                        cnvals.append({
                            'c1': r['clusterId'],
                            'c2': cs(r['cnName']),
                            'c3': cs(r['cnIp']),
                            'c4': cs(r['cnPort']),
                            'c5': cs(r['cnStatus']),
                            'c6': cs(r['cnCity'])
                        })
                        ips.add(r['cnIp'])
                        cnips.add(r['cnIp'])
        # GTM
        gtm_reponse = requests.get(gtmurl, headers=headers, data=payload, verify=False, timeout=5, proxies=proxies)
        if gtm_reponse and gtm_reponse.status_code == 200:
            msg = gtm_reponse.json()
            if msg["data"] and isinstance(msg["data"], dict):
                if gdb_version >= '6.1.03':
                    gtmvals.append(
                        dict(c1='集群ID', c2='IP', c3='运行端口', c4='服务端口', c5='安装目录', c6='状态', c7='机房', c8='城市', c9='资源',
                             c10='是否备份'))
                    for r in msg["data"]['list']:
                        gtmvals.append({
                            'c1': r['clusterId'],
                            'c2': cs(r['gtmIp']),
                            'c3': cs(r['gtmPort']),
                            'c4': cs(r['gtmSrcPort']),
                            'c5': cs(r['installPath']),
                            'c6': cs(r['status']),
                            'c7': cs(r['roomName']),
                            'c8': cs(r['cityName']),
                            'c9': cs(r['resourceUnit']),
                            'c10': cs(r['gtmBackup'])
                        })
                        ips.add(r['gtmIp'])
                else:
                    gtmvals.append(dict(c1='集群ID', c2='IP', c3='运行端口', c4='服务端口', c5='状态', c6='城市', c7='是否备份'))
                    for r in msg["data"]['list']:
                        gtmvals.append({
                            'c1': r['clusterId'],
                            'c2': cs(r['gtmIp']),
                            'c3': cs(r['gtmPort']),
                            'c4': cs(r['gtmSrcPort']),
                            'c5': cs(r['status']),
                            'c6': cs(r['gtmCity']),
                            'c7': cs(r['gtmBackup'])
                        })
                        ips.add(r['gtmIp'])
        # tenancy
        flag = 0
        cluster_name = DBUtil.get_cluster_name(pg, insight_ip, port)
        sql = '''select record_time,cib_value from p_normal_cib t1, mgt_system t2 where index_id=1000001 and cib_name='_tenancyDesc'
    and target_id::varchar  like '2205%' and t2.use_flag=True and t2.uid=t1.target_id and 
t2.name like '{0}' and target_id='{1}' '''.format(cluster_name, targetId)
        cs1 = DBUtil.getValue(pg, sql)
        rs1 = cs1.fetchone()
        if rs1:
            sample_time = rs1[0]
            localtenancyDesc = rs1[1]
            if sample_time is None:
                flag = 1
            else:
                if (datetime.now() - sample_time).seconds > 300:
                    flag = 1
        else:
            flag = 1
        if flag == 1:
            tenancy_reponse = requests.get(tenancyurl, headers=headers, data=payload, verify=False, timeout=5,
                                           proxies=proxies)
            if tenancy_reponse and tenancy_reponse.status_code == 200:
                msg = tenancy_reponse.json()

                # print(cluster_name)
                if msg["data"] and isinstance(msg["data"], dict):
                    datalist = msg["data"]['list']
                    for r in datalist:
                        tenancyName = r['tenancyName']
                        tenancyId = r['clusterId']
                        tenancyDesc = r['tenancyDesc']
                        object_uid = DBUtil.get_uid_by_object_name(pg, cluster_name, tenancyName, tenancyId)
                        if object_uid == targetId:
                            localtenancyDesc = tenancyDesc
                        sql = '''
    begin;
    delete from p_normal_cib where target_id='{0}' and index_id=1000001 and cib_name='_tenancyDesc';
    insert into p_normal_cib(target_id,index_id,cib_name,cib_value,record_time) 
    values('{0}',1000001,'_tenancyDesc','{1}','{2}');
    end;
    '''.format(object_uid, tenancyDesc, datetime.now())
                        # print(sql)
                        pg.execute(sql)
        # 获取OS相关信息
        if insight_access_ip is not None:
            url = f"https://{insight_access_ip}:{port}/open_api/insight/external/collect/searchHostCollectData?collectIdList=213"
        else:
            url = f"https://{target_ip}:{port}/open_api/insight/external/collect/searchHostCollectData?collectIdList=213"
        payload = {}
        headers = {
            'Cookie': 'SESSION=NWQ4ZTdlNjUtZWEwZi00ODZlLTk2ODMtNGRiZjFkYmExMTQw; JSESSIONID=5EF3A199858F08059A8E37402C2432F9',
            'username': username,
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
            if data['collectDataList']:

                vals3.append(dict(c1='IP', c2='机房名', c3='主机名', c4='CPU数', c5='总内存(GB)', c6='挂载点目录'))
                for h in data['collectDataList']:
                    host_data = h['dataList']
                    for r in host_data:
                        ip = r['hostIp']
                        if ip in ips:
                            totalCpu += int(r['totalCpu'])
                            totalMem += int(r['totalMem'])
                            vals.append(dict(name="host_ip", value=cs(ip)))
                            vals.append(dict(name="host_name", value=cs(r['hostName'])))
                            vals3.append(
                                dict(c1=ip, c2=r['roomName'], c3=r['hostName'], c4=r['totalCpu'], c5=r['totalMem'],
                                     c6=r['dirName']))
        # insight info
        flag = 0
        sql_check = '''select max(record_time) from mgt_platform_connection_info t1, mgt_platform t2 where t1.platform_id=t2.platform_id
 and t2.ip='{0}' and t2.port='{1}'   '''.format(insight_ip, insight_port)
        cs_check = DBUtil.getValue(pg, sql_check)
        rs_check = cs_check.fetchone()
        if rs_check:
            sample_time = rs_check[0]
            if sample_time is None:
                flag = 1
            else:
                if (datetime.now() - sample_time).seconds > 300:
                    flag = 1
        if flag == 1:
            mds_ip, mds_port, mds_user, mds_pwd = DBUtil.get_gdb_mds(pg, insight_ip, insight_port)
            if mds_ip and mds_port and mds_user and mds_pwd:
                mds_db = GoldenUtil.GDB(mds_ip, mds_user, mds_pwd, mds_port, dbname='mds', exflag=2)
                if not mds_db.conn:
                    mds_db, platform_id = DBUtil.get_available_mds_conn(pg, insight_ip, insight_port, mds_ip)
                else:
                    sql_p = '''select platform_id from mgt_platform where ip='{0}' and 
port='{1}' and use_flag=True'''.format(insight_ip, insight_port)
                    cs_p = DBUtil.getValue(pg, sql_p)
                    platform_id = cs_p.fetchone()[0]
                if mds_db is not None:
                    if gdb_version > '6':
                        sql2 = '''select host_ip,type,port,install_path, version, app_user, state,role
             from goldendb_insight.insight_install_info where type='insightServer' '''
                    else:
                        sql2 = '''select host_ip,type,port,install_path, version, app_user
                        from goldendb_insight.insight_install_info where type='insightServer' '''
                    cs2 = DBUtil.getValue(mds_db, sql2)
                    rs2 = cs2.fetchall()
                    if rs2:
                        if gdb_version > '6':
                            sql3 = '''
    begin;
    delete from mgt_platform_connection_info where platform_id='{0}';
    insert into mgt_platform_connection_info(platform_id, host_ip, type, port, install_path,
    version, app_user,state,role) values'''.format(platform_id)
                            for row in rs2:
                                sql3 += '''('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}'),'''.format(platform_id, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
                            sql3 = sql3[0:-1]
                            sql3 += ''';
    end;'''
                        else:
                            sql3 = '''
                            begin;
                            delete from mgt_platform_connection_info where platform_id='{0}';
                            insert into mgt_platform_connection_info(platform_id, host_ip, type, port, install_path,
                            version, app_user) values'''.format(platform_id)
                            for row in rs2:
                                sql3 += '''('{0}','{1}','{2}','{3}','{4}','{5}','{6}'),'''.format(platform_id, row[0], row[1], row[2], row[3], row[4], row[5])
                            sql3 = sql3[0:-1]
                            sql3 += ''';
                            end;'''
                        pg.execute(sql3)
    else:
        # tenancy
        flag = 0
        cluster_name = DBUtil.get_cluster_name(pg, insight_ip, port)
        sql = '''select record_time,cib_value from p_normal_cib t1, mgt_system t2 where index_id=1000001 and cib_name='_tenancyDesc'
            and target_id::varchar  like '2205%' and t2.use_flag=True and t2.uid=t1.target_id and 
        t2.name like '%{0}%' and target_id='{1}' '''.format(cluster_name, targetId)
        cs1 = DBUtil.getValue(pg, sql)
        rs1 = cs1.fetchone()
        if rs1:
            sample_time = rs1[0]
            localtenancyDesc = rs1[1]
            if sample_time is None:
                flag = 1
            else:
                if (datetime.now() - sample_time).seconds > 300:
                    flag = 1
        else:
            flag = 1
        if flag == 1:
            sql = '''select method1 from mgt_platform where ip='{0}' 
            and port='{1}' and use_flag=True '''.format(target_ip, port)
            cs1 = DBUtil.getValue(pg, sql)
            rs1 = cs1.fetchone()
            mds_info = json.loads(rs1[0])
            mds_ip = mds_info['mds_ip']
            mds_port = mds_info['mds_port']
            mds_user = mds_info['mds_user_name']
            mds_pwd = mds_info['mds_user_pwd']
            mds_db = GoldenUtil.GDB(mds_ip, mds_user, mds_pwd, mds_port, dbname='mds', exflag=2)
            if not mds_db.conn:
                mds_db, _ = DBUtil.get_available_mds_conn(pg, target_ip, port, mds_ip, 'mds')
            if mds_db is not None and mds_db.conn:
                sql = '''select tenancy_name,tenancy_desc,cluster_id from goldendb_insight.insight_tenancy_application'''
                cs2 = DBUtil.getValue(mds_db, sql)
                rs2 = cs2.fetchall()
                for row in rs2:
                    tenancyName = row[0]
                    tenancyId = row[2]
                    tenancyDesc = row[1]
                    object_uid = DBUtil.get_uid_by_object_name(pg, cluster_name, tenancyName, tenancyId)
                    if object_uid == targetId:
                        localtenancyDesc = tenancyDesc
                    # print(object_uid)
                    sql = '''
                    begin;
                    delete from p_normal_cib where target_id='{0}' and index_id=1000001 and cib_name='_tenancyDesc';
                    insert into p_normal_cib(target_id,index_id,cib_name,cib_value,record_time) 
                    values('{0}',1000001,'_tenancyDesc','{1}','{2}');
                    end;
                    '''.format(object_uid, tenancyDesc, datetime.now())
                    pg.execute(sql)
        # es_ip = DBUtil.get_insight_ip(pg, target_ip, port)
        mds_ip, mds_port, mds_user, mds_pwd = DBUtil.get_gdb_mds(pg, insight_ip, insight_port)
        mds_db = GoldenUtil.GDB(mds_ip, mds_user, mds_pwd, mds_port, dbname='mds', exflag=2)
        if not mds_db.conn:
            mds_db, platform_id = DBUtil.get_available_mds_conn(pg, target_ip, port, mds_ip, 'mds')
        if mds_db is not None and mds_db.conn:
            # insight info
            flag = 0
            sql_check = '''select max(record_time) from mgt_platform_connection_info t1, mgt_platform t2 where t1.platform_id=t2.platform_id
             and t2.ip='{0}' and t2.port='{1}'   '''.format(insight_ip, insight_port)
            cs_check = DBUtil.getValue(pg, sql_check)
            rs_check = cs_check.fetchone()
            if rs_check:
                sample_time = rs_check[0]
                if sample_time is None:
                    flag = 1
                else:
                    if (datetime.now() - sample_time).seconds > 300:
                        flag = 1
            if flag == 1:
                mds_ip, mds_port, mds_user, mds_pwd = DBUtil.get_gdb_mds(pg, insight_ip, insight_port)
                if mds_ip and mds_port and mds_user and mds_pwd:
                    mds_db = GoldenUtil.GDB(mds_ip, mds_user, mds_pwd, mds_port, dbname='mds', exflag=2)
                    if not mds_db.conn:
                        mds_db, platform_id = DBUtil.get_available_mds_conn(pg, insight_ip, insight_port, mds_ip)
                    else:
                        sql_p = '''select platform_id from mgt_platform where ip='{0}' and 
            port='{1}' and use_flag=True'''.format(insight_ip, insight_port)
                        cs_p = DBUtil.getValue(pg, sql_p)
                        platform_id = cs_p.fetchone()[0]
                    if mds_db is not None:
                        if gdb_version > '6':
                            sql2 = '''select host_ip,type,port,install_path, version, app_user, state,role
                         from goldendb_insight.insight_install_info where type='insightServer' '''
                        else:
                            sql2 = '''select host_ip,type,port,install_path, version, app_user
                                    from goldendb_insight.insight_install_info where type='insightServer' '''
                        cs2 = DBUtil.getValue(mds_db, sql2)
                        rs2 = cs2.fetchall()
                        if rs2:
                            if gdb_version > '6':
                                sql3 = '''
                begin;
                delete from mgt_platform_connection_info where platform_id='{0}';
                insert into mgt_platform_connection_info(platform_id, host_ip, type, port, install_path,
                version, app_user,state,role) values'''.format(platform_id)
                                for row in rs2:
                                    sql3 += '''('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}'),'''.format(platform_id, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
                                sql3 = sql3[0:-1]
                                sql3 += ''';
                end;'''
                            else:
                                sql3 = '''
                                        begin;
                                        delete from mgt_platform_connection_info where platform_id='{0}';
                                        insert into mgt_platform_connection_info(platform_id, host_ip, type, port, install_path,
                                        version, app_user) values'''.format(platform_id)
                                for row in rs2:
                                    sql3 += '''('{0}','{1}','{2}','{3}','{4}','{5}','{6}'),'''.format(platform_id, row[0], row[1], row[2], row[3], row[4], row[5])
                                sql3 = sql3[0:-1]
                                sql3 += ''';
                                        end;'''
                            pg.execute(sql3)

            # DN
            if gdb_version >= '6.1.03':
                sqlDN = '''select db_id,cluster_id,db_name,db_ip, t1.db_port,t1.db_role,db_status,t2.room_id,t2.user_dir,
                t2.db_data_dir from mds.db_info t1, goldendb_insight.insight_install_db_info t2 where t1.db_ip = t2.host_ip and 
                t1.db_port= t2.db_port and cluster_id={0}'''.format(clusterId)
            else:
                sqlDN = '''select db_id,cluster_id,db_name,db_ip, t1.db_port,t1.db_role,db_status,t2.room_name,t2.user_dir,
                t2.db_data_dir from mds.db_info t1, goldendb_insight.insight_install_db_info t2 where t1.db_ip = t2.host_ip and 
                t1.db_port= t2.db_port and cluster_id={0}'''.format(clusterId)
            cs1 = DBUtil.getValue(mds_db, sqlDN)
            res = cs1.fetchall()
            # 获取结果
            if res:
                dnvals.append(
                    dict(c1='集群ID', c2='名称', c3='序号', c4='IP', c5='PORT', c6='安装目录', c7='数据目录', c8='角色', c9='状态'))
                for row in res:
                    dnvals.append({
                        'c1': row[1],
                        'c2': cs(row[2]),
                        'c3': cs(row[0]),
                        'c4': cs(row[3]),
                        'c5': cs(row[4]),
                        'c6': cs(row[8]),
                        'c7': cs(row[9]),
                        'c8': cs(row[5]),
                        'c9': cs(row[6])
                    })
                    ips.add(row[3])
                    dnips.add(row[3])
            # CN
            sqlCN = '''select t4.cluster_id,t3.proxy_name,proxy_ip,t3.proxy_port,user_dir,t3.proxy_status,t5.proxy_port service_port
from goldendb_insight.insight_tenancy_proxy_resource t1,goldendb_insight.insight_install_proxy_info t2,mds.proxy_info t3, goldendb_insight.insight_tenancy_application t4,
mds.conn_instance_info t5, mds.proxy_instance_info t6
where t1.id=t2.id and t1.tenancy_id=t4.id and t4.cluster_id={0} and t2.host_ip=t3.proxy_ip and t3.proxy_port=t2.listen_port and t5.cluster_id=t4.cluster_id
and t6.proxy_id=t3.proxy_id and t6.conn_instance_id=t5.conn_instance_id'''.format(clusterId)
            cs2 = DBUtil.getValue(mds_db, sqlCN)
            res = cs2.fetchall()
            # 获取结果
            if res:
                cnvals.append(dict(c1='集群ID', c2='名称', c3='IP', c4='PORT', c5='安装目录', c6='状态', c7='服务端口'))
                for row in res:
                    cnvals.append({
                        'c1': row[0],
                        'c2': cs(row[1]),
                        'c3': cs(row[2]),
                        'c4': cs(row[3]),
                        'c5': cs(row[4]),
                        'c6': cs(row[5]),
                        'c7': cs(row[6])
                    })
                    ips.add(row[2])
                    cnips.add(row[2])

            # GTM
            use_system_gtm = DBUtil.is_use_system_gtm(mds_db, clusterId)
            if use_system_gtm:
                if gdb_version >= '6.1.03':
                    sqlGTM = '''SELECT gtm_id,{0},gtm_ip,gtm_port,user_dir,gtm_status,gtm_backup,room_id from 
        mds.gtm_info t1,goldendb_insight.insight_install_gtm_info t2 where gtm_cluster_id=0 and t1.gtm_ip=t2.host_ip and 
        t1.gtm_port=t2.monitor_port'''.format(clusterId)
                else:
                    sqlGTM = '''SELECT gtm_id,{0},gtm_ip,gtm_port,user_dir,gtm_status,gtm_backup,room_name from 
                    mds.gtm_info t1,goldendb_insight.insight_install_gtm_info t2 where gtm_cluster_id=0 and t1.gtm_ip=t2.host_ip and 
                    t1.gtm_port=t2.monitor_port'''.format(clusterId)
            else:
                if gdb_version >= '6.1.03':
                    sqlGTM = '''select gtm_id,t4.cluster_id,gtm_ip,gtm_port,user_dir,t3.gtm_status,gtm_backup,room_id from 
            goldendb_insight.insight_tenancy_gtm_resource t1,goldendb_insight.insight_install_gtm_info t2,mds.gtm_info t3, goldendb_insight.insight_tenancy_application t4
            where t1.install_id=t2.id and t4.id=tenancy_id and t4.cluster_id={0} and t2.host_ip=t3.gtm_ip and t2.monitor_port=t3.gtm_port'''.format(
                        clusterId)
                else:
                    sqlGTM = '''select gtm_id,t4.cluster_id,gtm_ip,gtm_port,user_dir,t3.gtm_status,gtm_backup,room_name from 
                    goldendb_insight.insight_tenancy_gtm_resource t1,goldendb_insight.insight_install_gtm_info t2,mds.gtm_info t3, goldendb_insight.insight_tenancy_application t4
                    where t1.install_id=t2.id and t4.id=tenancy_id and t4.cluster_id={0} and t2.host_ip=t3.gtm_ip and t2.monitor_port=t3.gtm_port'''.format(
                        clusterId)
            cs2 = DBUtil.getValue(mds_db, sqlGTM)
            res = cs2.fetchall()
            # 获取结果
            if res:
                gtmvals.append(
                    dict(c1='集群ID', c2='IP', c3='运行端口', c4='安装目录', c5='状态', c6='是否备份'))
                for row in res:
                    gtmvals.append({
                        'c1': row[1],
                        'c2': cs(row[2]),
                        'c3': cs(row[3]),
                        'c4': cs(row[4]),
                        'c5': cs(row[5]),
                        'c6': cs(row[6])
                    })
                    ips.add(row[2])
            # Os
            sqlOS = '''select t1.host_ip,host_name,status,total_cpu,total_mem,dir_name from goldendb_insight.host_info t1,
goldendb_insight.host_used_dir t2, goldendb_insight.insight_tenancy_db_resource t3,goldendb_insight.insight_tenancy_application t4
where t1.id=t2.host_id and t3.host_ip=t1.host_ip and t3.tenancy_id=t4.id and t4.cluster_id={0}
union 
select t1.host_ip,host_name,status,total_cpu,total_mem,dir_name from goldendb_insight.host_info t1,
goldendb_insight.host_used_dir t2, goldendb_insight.insight_tenancy_proxy_resource t3,goldendb_insight.insight_tenancy_application t4
where t1.id=t2.host_id and t3.host_ip=t1.host_ip and t3.tenancy_id=t4.id and t4.cluster_id={0}
'''.format(clusterId)
            cs2 = DBUtil.getValue(mds_db, sqlOS)
            res = cs2.fetchall()
            # 获取结果
            if res:
                vals3.append(dict(c1='IP', c2='主机名', c3='CPU数', c4='总内存(GB)', c5='挂载点目录'))
                ip_set = set()
                for row in res:
                    if row[0] not in ip_set:
                        vals.append(dict(name="host_ip", value=cs(row[0])))
                        vals.append(dict(name="host_name", value=cs(row[1])))
                        totalCpu += row[2]
                        totalMem += row[3]
                        ip_set.add(row[0])
                    vals3.append(dict(c1=row[0], c2=row[1], c3=row[2], c4=row[3],
                                      c5=row[4]))
    vals.append(dict(name="totalCpu", value=cs(totalCpu)))
    vals.append(dict(name="totalMem", value=cs(totalMem)))
    vals.append(dict(name="totalDNs", value=cs(len(dnips))))
    vals.append(dict(name="totalCNs", value=cs(len(cnips))))
    vals.append(dict(name="CNIPaddress", value=cs(' '.join(cnips))))
    vals.append(dict(name="DNIPaddress", value=cs(' '.join(dnips))))
    vals.append(dict(name='cnPort', value=cs(cn_port)))
    vals.append(dict(name='tenancyDesc', value=cs(localtenancyDesc)))
    if instanceType:
        vals.append(dict(name="ShardsType", value='多分片'))
    else:
        vals.append(dict(name="ShardsType", value='单分片'))
    if cnvals:
        insert_if_not_exists(targetId, index_id="2840001", value=cnvals)
    if dnvals:
        insert_if_not_exists(targetId, index_id="2840002", value=dnvals)
    if gtmvals:
        insert_if_not_exists(targetId, index_id="2840003", value=gtmvals)
    if vals and vals3:
        insert_if_not_exists(targetId, index_id="2840005", value=vals)
        insert_if_not_exists(targetId, index_id="2840004", value=vals3)
    gs_os(pg, targetId, ips, cnips, dnips)


CIB_BASIC = set([
    'VERSION',
    'VERSION_COMMENT',
    'COLLATION_SERVER',
    'CHARACTER_SET_SERVER',
    'BASEDIR',
    'DATADIR',
    'HOSTNAME',
    'PORT',
    'SERVER_ID',
    'SERVER_UUID',
    'LOG_ERROR',
    'TMPDIR',
    'SOCKET',
    'GOLDENDB_VERSION','INNODB_VERSION','PROTOCOL_VERSION'
])
CIB_PARAM = set([
    'INNODB_BUFFER_POOL_SIZE',
    'SYNC_BINLOG',
    'BINLOG_FORMAT',
    'INNODB_FLUSH_LOG_AT_TRX_COMMIT',
    'READ_ONLY',
    'LOG_SLAVE_UPDATES',
    'INNODB_IO_CAPACITY',
    'QUERY_CACHE_TYPE',
    'QUERY_CACHE_SIZE',
    'MAX_CONNECTIONS',
    'MAX_CONNECT_ERRORS',
    'WAIT_TIMEOUT',
    'TMP_TABLE_SIZE',
    'SORT_BUFFER_SIZE',
    'MAX_ALLOWED_PACKET',
    'INNODB_LOCK_WAIT_TIMEOUT',
    'KEY_BUFFER_SIZE',
    'READ_BUFFER_SIZE',
    'INNODB_LOG_FILE_SIZE',
    'INNODB_LOG_BUFFER_SIZE',
    'INNODB_FILE_PER_TABLE',
    'PERFORMANCE_SCHEMA',
    'INNODB_PAGE_SIZE',
    'TABLE_DEFINITION_CACHE',
    'TABLE_OPEN_CACHE',
    'TABLE_OPEN_CACHE_INSTANCES',
    'OPEN_FILES_LIMIT',
    'INNODB_OPEN_FILES',
    'THREAD_CACHE_SIZE',
    'HOST_CACHE_SIZE',
    'INNODB_LOG_FILES_IN_GROUP',
    'INNODB_LOG_GROUP_HOME_DIR',
    'INNODB_DATA_FILE_PATH',
    'INNODB_TEMP_DATA_FILE_PATH',
    'INNODB_BUFFER_POOL_FILENAME',
    'INNODB_DATA_HOME_DIR',
    'INNODB_UNDO_TABLESPACES',
    'INNODB_UNDO_DIRECTORY',
    'LOG_BIN',
    'LOG_BIN_BASENAME',
    'LONG_QUERY_TIME',
    'BINLOG_CACHE_SIZE',
    'MAX_HEAP_TABLE_SIZE',
    'KEY_CACHE_BLOCK_SIZE',
    'BINLOG_STMT_CACHE_SIZE',
    'DEFAULT_STORAGE_ENGINE',
    'PERFORMANCE_SCHEMA_HOSTS_SIZE',
    'LOG_WARNINGS',
    'FLUSH_TIME',
    'GENERAL_LOG',
    'LOCK_WAIT_TIMEOUT',
    'SKIP_NAME_RESOLVE',
    'SLOW_QUERY_LOG',
    'SLOW_QUERY_LOG_FILE',
    'SYSTEM_TIME_ZONE',
    'LOG_TIMESTAMPS',
    'INNODB_READ_IO_THREADS',
    'INNODB_WRITE_IO_THREADS',
    'INNODB_PAGE_CLEANERS',
    'INNODB_MAX_DIRTY_PAGES_PCT',
    'INNODB_STATS_PERSISTENT',
    'INNODB_STATS_AUTO_RECALC',
    'INNODB_THREAD_CONCURRENCY',
    'INNODB_BUFFER_POOL_INSTANCES',
    'INNODB_FLUSH_METHOD',
    'INNODB_FLUSH_NEIGHBORS',
    'INNODB_LRU_SCAN_DEPTH',
    'FLUSH_LOG_AT_TRX_COMMIT',
    'CONNECT_TIMEOUT',
    'JOIN_BUFFER_SIZE',
    'READ_RND_BUFFER_SIZE',
    'THREAD_STACK',
    'EXPIRE_LOGS_DAYS', 'BIND_ADDRESS'
])


def cib1(db, dbInfo, num, instanceType, summary_vars):
    global ibdata
    global ibtmp
    global datadir
    vals2 = []
    vals3 = []
    vals4 = []
    storage_str = ""
    if instanceType == 1:
        storage_str = f" storagedb g{num}"
        vals3.append(dict(name='groupid', value=cs(num)))
    else:
        vals3.append(dict(name='groupid', value=cs(0)))
    sql = f"select * from performance_schema.global_variables {storage_str}"
    result = relate_mysql(db, sql)
    if result.code == 0:
        addr = ""
        for row in result.msg:
            if row[0].upper() in CIB_BASIC:
                summary_vars.append(dict(name=row[0].lower(), value=cs(row[1])))
                vals3.append(dict(name=row[0].lower(), value=cs(row[1])))
                vals4.append(dict(name=row[0].lower(), value=cs(row[1])))
                vals2.append(dict(name=f"{row[0].lower()}({dbInfo['dbIp']}:{dbInfo['dbPort']})", value=cs(row[1])))
                if row[0].upper() == 'HOSTNAME':
                    if addr == "":
                        addr = cs(row[1])
                    else:
                        addr = cs(row[1]) + addr
                elif row[0].upper() == 'PORT':
                    if addr == "":
                        addr = ':' + cs(row[1])
                    else:
                        addr += ':' + cs(row[1])
                elif row[0].upper() == 'DATADIR':
                    datadir = row[1]
            elif row[0].upper() in CIB_PARAM:
                vals4.append(dict(name=row[0].lower(), value=cs(row[1])))
                vals2.append(dict(name=f"{row[0].lower()}({dbInfo['dbIp']}:{dbInfo['dbPort']})", value=cs(row[1])))
                if row[0].upper() == 'INNODB_DATA_FILE_PATH':
                    ibdata = row[1]
                elif row[0].upper() == 'INNODB_TEMP_DATA_FILE_PATH':
                    ibtmp = row[1]
                elif row[0].upper() == 'INNODB_UNDO_TABLESPACES':
                    if cs(row[1]) != '':
                        ibtbs = int(row[1])
                elif row[0].upper() == 'INNODB_UNDO_DIRECTORY':
                    ibdir = row[1]
        if addr != "":
            summary_vars.append(dict(name="address", value=addr))
            vals3.append(dict(name="address", value=addr))
    sql = f'select schema_name from information_schema.schemata'
    result = relate_mysql(db, sql)
    dbs = None
    if result.code == 0:
        for row in result.msg:
            if dbs is None:
                dbs = row[0]
            else:
                dbs += ',' + row[0]
    summary_vars.append(dict(name='databases', value=cs(dbs)))
    uid = get_uid_by_ip(dbInfo['dbIp'], dbInfo['dbPort'])
    insert_if_not_exists(uid, index_id="2210001", value=vals3)
    # insert_if_not_exists(targetId, index_id="2840005", value=vals)
    insert_if_not_exists(uid, index_id="2210002", value=vals4)
    insert_if_not_exists(targetId, index_id="2840006", value=vals2)


def getfiles(ts, sstr, arr):
    isize = None
    xsize = None
    ibs = sstr.split(';')
    cnt = 0
    for row in ibs:
        cols = row.split(':')
        if len(cols) > 1:
            t = len(cols[1])
            if cols[1][t - 1].lower() == 'k':
                isize = int(cols[1][0:t - 1]) * 1024
            elif cols[1][t - 1].lower() == 'm':
                isize = int(cols[1][0:t - 1]) * 1024 * 1024
            elif cols[1][t - 1].lower() == 'g':
                isize = int(cols[1][0:t - 1]) * 1024 * 1024 * 1024
            if len(cols) > 2 and cols[2].lower() == 'autoextend':
                if len(cols) > 4:
                    t = len(cols[4])
                    if cols[4][t - 1].lower() == 'k':
                        xsize = int(cols[4][0:t - 1]) * 1024
                    elif cols[4][t - 1].lower() == 'm':
                        xsize = int(cols[4][0:t - 1]) * 1024 * 1024
                    elif cols[4][t - 1].lower() == 'g':
                        xsize = int(cols[4][0:t - 1]) * 1024 * 1024 * 1024
            arr.append(
                dict(c1='InnoDB', c2=datadir + cols[0], c3=ts, c4=cs(isize), c5=cs(xsize)))
            cnt += 1
    return cnt


def cib2(db, dbInfo, num, instanceType):
    global version

    storage_str = ""
    if instanceType == 1:
        storage_str = f" storagedb g{num}"
    vals = []
    vals2 = []
    vals.append(dict(c1='引擎', c2='文件名', c3='表空间', c4='初始大小', c5='最大长度', c6='自动扩展大小', c7='可用大小', c8='状态'))
    vals2.append(dict(c1='引擎', c2='文件名', c3='表空间', c4='初始大小', c5='最大长度', c6='自动扩展大小', c7='可用大小', c8='状态', c9='DN'))
    t1 = 0
    t2 = 0
    for i in range(ibtbs):
        fname = ibdir + '/ibundo' + str(i + 1)
        vals.append(dict(c1='InnoDB', c2=fname, c3='innodb_undo', c4=cs(10 * 1024 * 1024), c5=''))
    sql = f"select ENGINE,FILE_NAME,TABLESPACE_NAME,INITIAL_SIZE,MAXIMUM_SIZE,autoextend_size,data_free,status from information_schema.files where TABLESPACE_NAME not like 'innodb_file_per_table_%' order by data_free asc limit 10 {storage_str}"
    result = relate_mysql(db, sql)
    if result.code == 0 and len(result.msg) > 0:
        for row in result.msg:
            if (t1 > 0 and row[2] == 'innodb_system') or (t2 > 0 and row[2] == 'innodb_temporary'):
                continue
            vals.append(dict(c1=cs(row[0]), c2=row[1], c3=cs(row[2]), c4=cs(row[3]), c5=cs(row[4]), c6=cs(row[5]),
                             c7=cs(row[6]), c8=cs(row[7])))
            vals2.append(dict(c1=cs(row[0]), c2=row[1], c3=cs(row[2]), c4=cs(row[3]), c5=cs(row[4]), c6=cs(row[5]),
                              c7=cs(row[6]), c8=cs(row[7]), c9=dbInfo['dbIp'] + ':' + str(dbInfo['dbPort'])))
    uid = get_uid_by_ip(dbInfo['dbIp'], dbInfo['dbPort'])
    if len(vals) > 1:
        insert_if_not_exists(uid, index_id="2840011", value=vals)
        insert_if_not_exists(targetId, index_id="2840011", value=vals2)


def cib_db(db, dbInfo, num, instanceType):
    """获取各个数据库信息

    Args:
        dbInfo ([type]): [description]
        db ([type]): [description]
        metric ([type]): [description]
    """
    vals = []
    vals2 = []
    storage_str = ""
    if instanceType == 1:
        storage_str = f" storagedb g{num}"
    flag_v = check_mysql_proc(db)
    if flag_v == 1:
        proc_name = 'monitor_information_proc'
        proc_args = ('table_schema , sum(table_rows) , round(sum(data_length / 1024 / 1024 / 1024), 2) as tab_size, round(sum(index_length / 1024 / 1024 / 1024), 2) as index_size , round(sum(DATA_LENGTH + INDEX_LENGTH)/ 1024 / 1024 / 1024, 2) as total_size, count(*) table_nums','tables',f'group by table_schema order by sum(data_length + INDEX_LENGTH) desc')
        result = db.execute_proc(proc_name,proc_args)
    else:
        sql = f"""
        select
            table_schema ,
            sum(table_rows) ,
            round(sum(data_length / 1024 / 1024 / 1024), 2) as tab_size,
            round(sum(index_length / 1024 / 1024 / 1024), 2) as index_size ,
            round(sum(DATA_LENGTH + INDEX_LENGTH)/ 1024 / 1024 / 1024, 2) as total_size,
            count(*) table_nums
        from
            information_schema.tables
        group by
            table_schema
        order by
            sum(data_length + INDEX_LENGTH) desc
        {storage_str}
        """
        result = relate_mysql(db, sql)
    if result.code == 0 and len(result.msg) > 0:
        vals.append(dict(c1='数据库名', c2='总数据行', c3='数据大小(GB)', c4='索引大小(GB)', c5='总大小(GB)', c6='表数量'))
        vals2.append(dict(c1='数据库名', c2='总数据行', c3='数据大小(GB)', c4='索引大小(GB)', c5='总大小(GB)', c6='表数量', c7='DN'))
        for row in result.msg:
            vals.append(dict(c1=row[0], c2=cs(row[1]), c3=cs(row[2]), c4=cs(row[3]), c5=cs(row[4]), c6=cs(row[5])))
            vals2.append(dict(c1=row[0], c2=cs(row[1]), c3=cs(row[2]), c4=cs(row[3]), c5=cs(row[4]), c6=cs(row[5]),
                              c7=dbInfo['dbIp'] + ':' + str(dbInfo['dbPort'])))
    uid = get_uid_by_ip(dbInfo['dbIp'], dbInfo['dbPort'])
    if len(vals) > 1:
        insert_if_not_exists(uid, index_id="2840007", value=vals)
        insert_if_not_exists(targetId, index_id="2840007", value=vals2)


def cib_table(db, dbInfo, num, instanceType):
    """获取TOP 20大小表

    Args:
        db ([type]): [description]
        metric ([type]): [description]
    """
    vals = []
    vals2 = []
    storage_str = ""
    if instanceType == 1:
        storage_str = f" storagedb g{num}"
    sql = f"""
    select
        TABLE_SCHEMA ,
        TABLE_NAME ,
        round(data_length / 1024 / 1024 / 1024, 2) data_size_gb,
        round(index_length / 1024 / 1024 / 1024, 2) index_size_gb,
        round((data_length + index_length) / 1024 / 1024 / 1024, 2) total_size,
        round(DATA_FREE*100 /(DATA_LENGTH + INDEX_LENGTH), 2) frag_ratio,
        ENGINE
    from
        information_schema.tables
    order by
        5 desc
    limit 20
    {storage_str}
    """
    result = relate_mysql(db, sql)
    if result.code == 0 and len(result.msg) > 0:
        vals.append(dict(c1='数据库名', c2='表名', c3='数据大小(GB)', c4='索引大小(GB)', c5='总大小(GB)', c6='碎片率', c7='存储引擎'))
        vals2.append(dict(c1='数据库名', c2='表名', c3='数据大小(GB)', c4='索引大小(GB)', c5='总大小(GB)', c6='碎片率', c7='存储引擎', c8='DN'))
        for row in result.msg:
            vals.append(dict(c1=row[0], c2=cs(row[1]), c3=cs(row[2]), c4=cs(row[3]), c5=cs(row[4]), c6=cs(row[5]),
                             c7=cs(row[6])))
            vals2.append(dict(c1=row[0], c2=cs(row[1]), c3=cs(row[2]), c4=cs(row[3]), c5=cs(row[4]), c6=cs(row[5]),
                              c7=cs(row[6]), c8=dbInfo['dbIp'] + ':' + str(dbInfo['dbPort'])))
    uid = get_uid_by_ip(dbInfo['dbIp'], dbInfo['dbPort'])
    if len(vals) > 1:
        insert_if_not_exists(uid, index_id="2840008", value=vals)
        insert_if_not_exists(targetId, index_id="2840008", value=vals2)


def cib_index(db, dbInfo, num, instanceType):
    """获取TOP 20 索引大小

    Args:
        b ([type]): [description]
        metric ([type]): [description]
    """
    vals = []
    vals2 = []
    storage_str = ""
    if instanceType == 1:
        storage_str = f" storagedb g{num}"
    sql = f"""
    select
        database_name,
        table_name,
        index_name,
        round((stat_value*(select variable_value from performance_schema.global_variables where variable_name = 'innodb_page_size'))/ 1024 / 1024/ 1024, 2) SizeGB
    from
        mysql.innodb_index_stats iis
    where
        stat_name = 'size'
        and index_name  not in('GEN_CLUST_INDEX','PRIMARY')
        order by 4 desc
    limit 20
    {storage_str}
    """
    result = relate_mysql(db, sql)
    if result.code == 0 and len(result.msg) > 0:
        vals.append(dict(c1='数据库名', c2='表名', c3='索引名', c4='索引大小(GB)'))
        vals2.append(dict(c1='数据库名', c2='表名', c3='索引名', c4='索引大小(GB)', c5='DN'))
        for row in result.msg:
            vals.append(dict(c1=row[0], c2=cs(row[1]), c3=cs(row[2]), c4=cs(row[3])))
            vals2.append(dict(c1=row[0], c2=cs(row[1]), c3=cs(row[2]), c4=cs(row[3]),
                              c5=dbInfo['dbIp'] + ':' + str(dbInfo['dbPort'])))
    uid = get_uid_by_ip(dbInfo['dbIp'], dbInfo['dbPort'])
    if len(vals) > 1:
        insert_if_not_exists(uid, index_id="2840009", value=cs(vals))
        insert_if_not_exists(targetId, index_id="2840009", value=cs(vals2))


def gs_os(db, uid, srvs, cnsrvs, dnsrvs):
    if srvs:
        sql = "select cib_name,cib_value from p_normal_cib where target_id='%s' and index_id=1000001 and cib_name in ('_ips','_cnips','_dnips')" % uid
        cs1 = DBUtil.getValue(db, sql)
        rs1 = cs1.fetchall()
        ips = set()
        cnips = set()
        dnips = set()
        if rs1:
            for row in rs1:
                if row[0] == '_ips':
                    arr = row[1].split(',')
                    for ip in arr:
                        ips.add(ip)
                elif row[0] == '_cnips':
                    arr = row[1].split(',')
                    for ip in arr:
                        cnips.add(ip)
                else:
                    arr = row[1].split(',')
                    for ip in arr:
                        dnips.add(ip)
        vs = set()
        for row in srvs:
            vs.add(row)
        cnvs = set()
        for row in cnsrvs:
            cnvs.add(row)
        dnvs = set()
        for row in dnsrvs:
            dnvs.add(row)
        sql = """select b.in_ip,b.uid,b.in_username,b.in_password,b.port,b.position,b.life,d.name from mgt_device b,sys_dict d
where d.type='device_opersys' and b.opersys=d.value::numeric and in_ip in %s and b.use_flag""" % tuple2(vs.union(ips),
                                                                                                        True)
        cs2 = DBUtil.getValue(db, sql)
        rs2 = cs2.fetchall()
        if rs2:
            hosts = {}
            for row in rs2:
                hosts[row[0]] = [row[1], row[2], row[3], row[4], row[5], row[6], row[7]]
            try:
                cur = db.conn.cursor()
                if vs.union(ips):
                    for ip in vs.union(ips):
                        row = hosts.get(ip)
                        if row:
                            sql = "delete from p_normal_cib where target_id='%s' and index_id=1000001 and cib_name='_ping'" % \
                                  row[0]
                            cur.execute(sql)
                ss = ''
                ss2 = ''
                ss3 = ''
                f = True
                for ip in vs:
                    if ss:
                        ss += ',' + ip
                    else:
                        ss = ip
                    if ip in cnvs:
                        if ss2:
                            ss2 += ',' + ip
                        else:
                            ss2 = ip
                    if ip in dnvs:
                        if ss3:
                            ss3 += ',' + ip
                        else:
                            ss3 = ip
                    row = hosts.get(ip)
                    if row:
                        vs2 = vs.copy()
                        if len(vs2) > 1:
                            vs2.remove(ip)
                        if f:
                            s = '+' + tuple2(vs2)
                            f = False
                        else:
                            s = tuple2(vs2)
                        if vs2:
                            sql = "insert into p_normal_cib(target_id,index_id,cib_name,cib_value,record_time) values('%s',1000001,'_ping','%s',now())" % (
                            row[0], s)
                            cur.execute(sql)
                sql = "delete from p_normal_cib where target_id='%s' and index_id=1000001 and cib_name in ('_ips','_cnips','_dnips')" % uid
                cur.execute(sql)
                sql = "insert into p_normal_cib(target_id,index_id,cib_name,cib_value,record_time) values('%s',1000001,'_ips','%s',now())" % (
                uid, ss)
                cur.execute(sql)
                sql = "insert into p_normal_cib(target_id,index_id,cib_name,cib_value,record_time) values('%s',1000001,'_cnips','%s',now())" % (
                uid, ss2)
                cur.execute(sql)
                sql = "insert into p_normal_cib(target_id,index_id,cib_name,cib_value,record_time) values('%s',1000001,'_dnips','%s',now())" % (
                uid, ss3)
                cur.execute(sql)
                db.conn.commit()
            except Exception as e:
                db.conn.rollback()


def cib_tbs(db, dbInfo, num, instanceType):
    vals = []
    vals2 = []
    storage_str = ""
    if instanceType == 1:
        storage_str = f" storagedb g{num}"
    sql = f"""
    select
        name,
        page_size,
        space_type,
        round(file_size/1024/1024,2),
        round(allocated_size/1024/1024,2),
        autoextend_size,
        server_version,
        encryption,
        state
    from
        information_schema.INNODB_TABLESPACES
    order by allocated_size desc limit 10
    {storage_str}
    """
    result = relate_mysql(db, sql)
    if result.code == 0 and len(result.msg) > 0:
        vals.append(
            dict(c1='表空间', c2='页大小(字节)', c3='类型', c4='文件大小(GB)', c5='已分配大小(GB)', c6='自动扩展大小', c7='创建时的版本', c8='加密？',
                 c9='状态', ))
        vals2.append(
            dict(c1='表空间', c2='页大小(字节)', c3='类型', c4='文件大小(GB)', c5='已分配大小(GB)', c6='自动扩展大小', c7='创建时的版本', c8='加密？',
                 c9='状态', c10='DN'))
        for row in result.msg:
            vals.append(dict(c1=row[0], c2=cs(row[1]), c3=cs(row[2]), c4=cs(row[3]), c5=cs(row[4]), c6=cs(row[5]),
                             c7=cs(row[6]), c8=cs(row[7]), c9=cs(row[8])))
            vals2.append(dict(c1=row[0], c2=cs(row[1]), c3=cs(row[2]), c4=cs(row[3]), c5=cs(row[4]), c6=cs(row[5]),
                              c7=cs(row[6]), c8=cs(row[7]), c9=cs(row[8]),
                              c10=dbInfo['dbIp'] + ':' + str(dbInfo['dbPort'])))
    uid = get_uid_by_ip(dbInfo['dbIp'], dbInfo['dbPort'])
    if len(vals) > 1:
        insert_if_not_exists(uid, index_id="2840010", value=vals)
        insert_if_not_exists(targetId, index_id="2840010", value=vals2)


if __name__ == '__main__':
    dbInfo = eval(sys.argv[1])
    db_ip = dbInfo['target_ip']
    targetId, pg = DBUtil.get_pg_env()
    global_metric = []
    # isInsight = DBUtil.golden_is_insight(pg, targetId)
    db = DBUtil.get_gdb_env(exflag=1)
    cn_port = dbInfo['target_port']
    dns = []
    if db.conn:
        sql = '''show variables like 'goldendb_version' '''
        result = relate_mysql(db, sql)
        if result.code == 0 and len(result.msg) > 0:
            if result.msg[0][1]:
                gdb_version = result.msg[0][1]
        gdb_main_version_list = gdb_version.split('-')[1].split('.')[0:-1]
        gdb_main_version = '.'.join(gdb_main_version_list).split('DBV')[1]
        instanceType = DBUtil.get_gdb_instanceType(db)
        clusterId = None
        isInsight, insight_ip, insight_port, insight_user, insight_pwd, clusterId = DBUtil.get_insight_info(pg,
                                                                                                            targetId)

        if isInsight:
            base64_pwd = base64.b64encode(decrypt(insight_pwd, 1).encode('utf-8')).decode()
            get_goldendb_summary(isInsight, gdb_main_version, insight_ip, insight_user, base64_pwd, insight_port,
                                 clusterId)
        else:
            get_goldendb_summary(isInsight, gdb_main_version, insight_ip, port=insight_port, clusterId=clusterId)
        dns = DBUtil.get_golden_dns_by_insight(db)
        instanceType = DBUtil.get_gdb_instanceType(db)
        summary_vars = []
        for dn in dns:
            cib1(db, dn, dn['num'], instanceType, summary_vars)
            cib2(db, dn, dn['num'], instanceType)
            cib_db(db, dn, dn['num'], instanceType)
            cib_table(db, dn, dn['num'], instanceType)
            cib_index(db, dn, dn['num'], instanceType)
            cib_tbs(db, dn, dn['num'], instanceType)
        merged_dict = defaultdict(set)

        # 按照 name 进行合并
        for item in summary_vars:
            merged_dict[item["name"]].add(item["value"])

        # 将集合转换为字符串并用逗号分隔
        output_list = [{"name": k, "value": ",".join(v)} for k, v in merged_dict.items()]
        insert_if_not_exists(targetId, index_id="2840005", value=output_list)
    print(json.dumps(global_metric))

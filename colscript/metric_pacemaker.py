#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@文件    :metric_pacemaker.py
@说明    :pacemake 指标采集
@时间    :2021/08/31 15:12:16
@作者    :xxxx
@版本    :2.0.1
'''

import sys
import json
from lxml import etree
sys.path.append('/usr/software/knowl')
import DBUtil
import sshSession


metric = []


def get_cib_from_xml(ssh):
    "将pcs返回结果保存为xml文件"
    out = ssh.exec_cmd("pcs cluster cib").strip('')
    with open('/tmp/pcs.xml','w') as f:
        for i in out.split('\n'):
            f.write(i)
    return '/tmp/pcs.xml'


def parse_cib(ssh):
    "解析pacemaker cib 信息，为xml格式"
    cib_file = get_cib_from_xml(ssh)
    xml_tree = etree.parse(cib_file)
    root = xml_tree.getroot()
    fail_count = 0
    offline_node_count = 0
    for elments in root:
        first_tag = elments.tag
        if first_tag == 'status':
            for elment in elments:
                sec_tag = elment.tag
                node_stat = elment.get('crmd')
                if node_stat != 'online':
                    offline_node_count += float(node_stat)
                if sec_tag == 'node_state': # # 集群配置信息 
                    for e in elment:
                        if e.tag == 'transient_attributes':
                            for ee in e:
                                for tt in ee:
                                    atrribut_name=tt.get('name')
                                    if 'fail-count' in atrribut_name:
                                        atrribut_value=tt.get('value')
                                        fail_count += float(atrribut_value)
    metric.append(dict(index_id=2340001, value=fail_count))
    metric.append(dict(index_id=2340002, value=offline_node_count))


def health_score(pg,ip):
    "获取该节点上PG软件对象的健康分"
    sql = f"""
    select
        min(total_score)
    from
        h_health_check hhc,
        mgt_system ms
    where
        hhc.target_id = ms.uid
        and update_time > now() - interval '30m'
        and ms.ip = '{ip}'
        and type = '4'
    """
    cs = DBUtil.getValue(pg,sql)
    rs = cs.fetchone()
    if rs and rs[0]:
        metric.append(dict(index_id=2340003, value=rs[0]))
    else:
        metric.append(dict(index_id=2340003, value=100))


if __name__ == '__main__':
    dbInfo = eval(sys.argv[1])
    ip = dbInfo['target_ip']
    pg = DBUtil.get_pg_from_cfg()
    sql = f"SELECT in_username ,in_password ,port FROM mgt_device md WHERE md.in_ip = '{ip}'"
    cs = DBUtil.getValue(pg, sql)
    rs = cs.fetchone()
    if rs:
        user = rs[0]
        user_pwd = rs[1]
        port = rs[2]
        if dbInfo.get('protocol') == '1':
            device_proto = "SSH"
        elif dbInfo.get('protocol') == '2':
            device_proto = "RSH"
        else:
            device_proto = "SSH"
        ssh = sshSession.sshSession(ip, user, user_pwd, port, device_proto, dbInfo.get('life'))
        ip = dbInfo["target_ip"]
        pg = DBUtil.get_pg_from_cfg()
        cmd_str = "ps -ef|grep pcsd|grep -v grep|wc -l"
        out = ssh.exec_cmd(cmd_str).strip()
        if float(out) > 0:
            metric.append(dict(index_id="2340000", value="连接成功"))
            parse_cib(ssh)
            health_score(pg, ip)
        else:
            ana = 'Pacemaker进程不存在！'
            metric.append(dict(index_id="2340000", value="连接失败"))
        print('{"results":' + json.dumps(metric) + '}')
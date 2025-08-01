#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@文件    :cib_pacemaker.py
@说明    :Pacemake cib 信息采集
@时间    :2021/08/31 09:06:28
@作者    :xxxx
@版本    :2.0.1
'''

import sys
import json
from lxml import etree
sys.path.append('/usr/software/knowl')
import sshSession
import DBUtil

metric = []

def vals_append(key, value, vals):
    vals.append(dict(name=key, value=str(value)))


def table_append(tab_list, c1=None, c2=None, c3=None, c4=None, c5=None, c6=None, c7=None, c8=None, c9=None, c10=None):
    tab_list.append(dict(c1=c1, c2=c2, c3=c3, c4=c4, c5=c5, c6=c6, c7=c7, c8=c8, c9=c9, c10=c10))


def get_cib_from_xml(ssh):
    "将pcs返回结果保存为xml文件"
    out = ssh.exec_cmd("pcs cluster cib").strip('')
    with open('/tmp/pcs.xml','w') as f:
        for i in out.split('\n'):
            f.write(i)
    return '/tmp/pcs.xml'


def parse_cib(ssh,ip):
    "解析pacemaker cib 信息，为xml格式"
    cib_file = get_cib_from_xml(ssh)
    xml_tree = etree.parse(cib_file)
    root = xml_tree.getroot()
    # 集群基本信息
    crm_feature_set = root.get('crm_feature_set')
    pce_verion = root.get('validate-with')
    cib_updates = root.get('num_updates')
    cib_laste_time = root.get('cib-last-written')
    cib_update_origin = root.get('update-origin')
    cib_update_client = root.get('update-client')
    cib_update_user = root.get('update-user')
    cib_have_quorum = root.get('have-quorum')
    vals = []
    vals_append("crm_feature_set", crm_feature_set,vals)
    vals_append("pacemaker_version", pce_verion,vals)
    vals_append("num_updates", cib_updates,vals)
    vals_append("cib_last_written", cib_laste_time,vals)
    vals_append("cib_update_origin", cib_update_origin,vals)
    vals_append("cib_update_client", cib_update_client,vals)
    vals_append("cib_update_user", cib_update_user,vals)
    vals_append("cib_have_quorum", cib_have_quorum,vals)
    vals_append("ip", ip,vals)
    metric.append(dict(index_id=2330001, value=vals))
    for elments in root:
        for elment in elments:
            sec_tag = elment.tag
            if sec_tag == 'crm_config': # # 集群配置信息 
                vals = []
                for e in elment:
                    if e.tag == 'cluster_property_set':
                        for ee in e:
                            atrribut_name=ee.get('name')
                            atrribut_value=ee.get('value')
                            vals_append(atrribut_name, atrribut_value,vals)
                metric.append(dict(index_id=2330002, value=vals))
            elif sec_tag == 'nodes': # 集群节点信息
                members_list = []
                table_append(members_list, "节点ID", "节点名", "属性名", "属性值")
                for e in elment:
                    if e.tag == 'node':
                        node_name = e.get('uname')
                        for ee in e:
                            node_id = ee.get('id')
                            for t in ee:
                                atrribut_name=t.get('name')
                                atrribut_value=t.get('value')
                            table_append(members_list, node_id, node_name, atrribut_name, atrribut_value)
            elif sec_tag == 'resources': # 集群资源配置信息
                for e in elment:
                    third_tag = e.tag
                    if third_tag == 'master':   # 主资源相关信息
                        for ee in e:
                            fouth_tag = ee.tag
                            if fouth_tag == 'primitive':
                                for t in ee:
                                    five_tag = t.tag
                                    if five_tag == 'instance_attributes':  # 资源属性
                                        vals = []
                                        for tt in t:
                                            atrribut_name=tt.get('name')
                                            atrribut_value=tt.get('value')
                                            vals_append(atrribut_name, atrribut_value,vals)
                                        metric.append(dict(index_id=2330004, value=vals))
                                    elif five_tag == 'operations':  # 资源操作配置信息
                                        members_list2 = []
                                        table_append(members_list2, "操作ID", "操作名", "异常操作","角色", "超时时间")
                                        for tt in t:
                                            operations_id=tt.get('id')
                                            operations_name=tt.get('name')
                                            operations_fail=tt.get('on-fail')
                                            operations_role=tt.get('role')
                                            operations_value=tt.get('timeout')
                                            table_append(members_list2, operations_id, operations_name, operations_fail,operations_role, operations_value)
                            elif fouth_tag == 'meta_attributes':  # 集群元数据配置
                                vals = []
                                for t in ee:
                                    atrribut_name=t.get('name')
                                    atrribut_value=t.get('value')
                                    vals_append(atrribut_name, atrribut_value,vals)
                                    metric.append(dict(index_id=2330006, value=vals))
                    elif third_tag == 'group':   # 其他资源相关信息
                        vals = []
                        group_id = e.get('id')
                        members_list3 = []
                        table_append(members_list3, "资源组", "资源名", "配置名","配置值")
                        for ee in e:
                            fouth_tag = ee.tag
                            res_name = ee.get('id')
                            if fouth_tag == 'primitive':
                                for t in ee:
                                    five_tag = t.tag
                                    if five_tag == 'instance_attributes':  # 资源属性
                                        for tt in t:
                                            atrribut_name=tt.get('name')
                                            atrribut_value=tt.get('value')
                                            table_append(members_list3, group_id, res_name, atrribut_name,atrribut_value)
                                    elif five_tag == 'operations':  # 资源操作配置信息
                                        members_list4 = []
                                        table_append(members_list4, "资源组", "资源名", "操作ID", "操作名", "异常操作","角色", "超时时间")
                                        for tt in t:
                                            operations_id=tt.get('id')
                                            operations_name=tt.get('name')
                                            operations_fail=tt.get('on-fail')
                                            operations_role=tt.get('role')
                                            operations_value=tt.get('timeout')
                                            table_append(members_list4,group_id,res_name, operations_id, operations_name, operations_fail,operations_role, operations_value)
    metric.append(dict(index_id=2330003, content=members_list))
    metric.append(dict(index_id=2330005, content=members_list2))
    metric.append(dict(index_id=2330007, content=members_list3))
    metric.append(dict(index_id=2330008, content=members_list4))


if __name__ == '__main__':
    dbinfo = eval(sys.argv[1])
    ip = dbinfo['target_ip']
    pg = DBUtil.get_pg_from_cfg()
    sql = f"SELECT in_username ,in_password ,port FROM mgt_device md WHERE md.in_ip = '{ip}'"
    cs = DBUtil.getValue(pg,sql)
    rs = cs.fetchone()
    if rs:
        user = rs[0]
        user_pwd = rs[1]
        port = rs[2]
        if dbinfo.get('protocol') == '1':
            device_proto = "SSH"
        elif dbinfo.get('protocol') == '2':
            device_proto = "RSH"
        else:
            device_proto = "SSH"
        ssh_user, ssh_path = DBUtil.get_sshkey_info(pg)
        ssh = sshSession.sshSession(ip, user, user_pwd, port, device_proto, dbinfo.get('life'), ssh_user, ssh_path)
        parse_cib(ssh, ip)
    print('{"cib":' + json.dumps(metric) + '}')
#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

sys.path.append('/usr/software/knowl')

import DBUtil as dbu

import json


def register(file_name):
    res = []
    print('{"params_reg":[]}')


def getlinuxservice():
    score = 0
    fres = []
    vs = 0
    vt = []
    vtn = []
    cmd = "chkconfig --list|grep -E \"ip6tables|iptables|sshd|network|vsftpd|ntp|dhcpd|bluetooth|nfs|nfslock|ypbind|postfix|cups|cpuspeed\""
    vres = helper.openCmd(cmd).strip()
    cmd_rl = "runlevel|awk '{print $2}'"
    vres_rl = helper.openCmd(cmd_rl).strip()
    for x in vres.split("\n"):
        if x.startswith("ip6tables"):
            if str(vres_rl) + ":off" not in x:
                vs += 1
                vt.append("ip6tables服务未关闭")
            else:
                vtn.append("ip6tables服务已关闭")
        if x.startswith("iptables"):
            if str(vres_rl) + ":off" not in x:
                vs += 1
                vt.append("iptables服务未关闭")
            else:
                vtn.append("ip6table服务已关闭")
        if x.startswith("sshd"):
            if str(vres_rl) + ":on" not in x:
                vs += 1
                vt.append("sshd服务未打开")
            else:
                vtn.append("sshd服务已打开")
        if x.startswith("NetworkManager"):
            if str(vres_rl) + ":off" not in x:
                vs += 1
                vt.append("NetworkManager服务未关闭")
            else:
                vtn.append("NetworkManager服务已关闭")
        if x.startswith("vsftpd"):
            if str(vres_rl) + ":off" not in x:
                vs += 1
                vt.append("vsftpd服务未关闭")
            else:
                vtn.append("vsftpd服务已关闭")
        if x.startswith("ntpd") and not x.startswith("ntpdate"):
            if str(vres_rl) + ":on" not in x:
                vs += 1
                vt.append("ntpd服务未开启")
            else:
                vtn.append("ntpd服务已开启")
        if x.startswith("dhcpd"):
            if str(vres_rl) + ":off" not in x:
                vs += 1
                vt.append("dhcpd服务未关闭")
            else:
                vtn.append("dhcpd服务已关闭")
        if x.startswith("bluetooth"):
            if str(vres_rl) + ":off" not in x:
                vs += 1
                vt.append("bluetooth服务未关闭")
            else:
                vtn.append("bluetooth服务已关闭")
        if x.startswith("nfs") and not x.startswith("nfs-rdma") and not x.startswith("nfslock"):
            if str(vres_rl) + ":off" not in x:
                vs += 1
                vt.append("nfs服务未关闭")
            else:
                vtn.append("nfs服务已关闭")
        if x.startswith("nfslock"):
            if str(vres_rl) + ":off" not in x:
                vs += 1
                vt.append("nfslock服务未关闭")
            else:
                vtn.append("nfslock服务已关闭")
        if x.startswith("ypbind"):
            if str(vres_rl) + ":off" not in x:
                vs += 1
                vt.append("ypbind服务未关闭")
            else:
                vtn.append("ypbind服务已关闭")
        if x.startswith("postfix"):
            if str(vres_rl) + ":off" not in x:
                vs += 1
                vt.append("postfix服务未关闭")
            else:
                vtn.append("postfix服务已关闭")
        if x.startswith("cups"):
            if str(vres_rl) + ":off" not in x:
                vs += 1
                vt.append("cups服务未关闭")
            else:
                vtn.append("cups服务已关闭")
        if x.startswith("cpuspeed"):
            if str(vres_rl) + ":off" not in x:
                vs += 1
                vt.append("cpuspeed服务未关闭")
            else:
                vtn.append("cpuspeed服务已关闭")

    if vs > 0:
        score += 1
        fres.append(dict(rkey="系统服务检查", rval="\n".join(str(i) for i in vt), rtype=1, rnote="系统服务配置不合规"))
    else:
        if vtn == []:
            vtn.append("系统服务配置合规")
        fres.append(dict(rkey="系统服务检查", rval="\n".join(str(i) for i in vtn), rtype=0, rnote="系统服务配置合规"))
    return score, fres


if __name__ == '__main__':
    """'{"deviceId":"110100011","in_ip":"60.60.60.116","in_os":"RedHat","in_port":"22","in_pwd":"A/uOt/N48/t8wkiYVPA9qG/U6oTl6gRIlq9x4CNbuA5tgaELSobkkEdS1EaM7Fxqj6gmwPHr0kv6HP0PytI2PCXUDfDxH0dnz88ZL94N1AuQdhLsx6e1O/McX8osfqsEhwtJCEAd/Y+XmM06vnBBgPB0PTzvJbpmTzbTG1WR61E=","in_uid":"110600001","in_username":"root","in_usr":"root"}'"""
    """'{"deviceId":"110100012","in_ip":"60.60.60.205","in_os":"RedHat","in_port":"22","in_pwd":"NQTZWN7c6qx/Mjc1LiIRl2xlPj5+5w5jsAdbpQN1E21dnqazfAImji5PIWczjMHyEuy6h8bl9O18InFiHB6D0oQiZimRSZHrgmJoEsh34DWRIpy10+82DexjWO69nJWRzDlwUJ+bGi/H5av9RESVe4EEToJsUljAHZJPcoZ5Ep4=","in_uid":"110600002","in_username":"root","in_usr":"root"}'"""
    check_item = ['系统版本检查', '系统时区检查', '系统可用磁盘空间检查', '系统内存检查', '系统字符集检查', '系统网卡个数检查', '系统文件系统检查', '系统RPM包检查', '系统服务检查',
                  '系统Selinux检查', '系统透明大页检查', '系统安全配置检查', '系统参数配置检查']
    ostype, deviceId, helper = dbu.get_ssh_help()
    # dbInfo = eval(sys.argv[1])

    try:
        s9, f9 = getlinuxservice()
        if f9:
            # print('{"check":' + json.dumps(f9[0]) + '}')
            print('msg=' + json.dumps(f9[0]))



    except Exception as e:
        errorInfo = str(e)
        print("异常：" + errorInfo)

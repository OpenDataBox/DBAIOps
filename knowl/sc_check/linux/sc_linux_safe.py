#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

sys.path.append('/usr/software/knowl')

import DBUtil as dbu

import json


def register(file_name):
    res = []
    print('{"params_reg":[]}')


def getlinuxsafe():
    score = 0
    fres = []

    vs = 0
    vt = []
    vtn = []

    # 用户口令复杂度设置
    cmd = "cat /etc/pam.d/system-auth-ac|grep minlen=8"
    vres = helper.openCmd(cmd).strip()
    if vres == "" and "No such file" not in vres:
        vs += 1
        vt.append(
            "用户口令复杂度设置不合规，建议设置：/etc/pam.d/system-auth-ac修改password    requisite   pam_cracklib.so minlen=8 dcredit=-1 ucredit=-1 ocredit=-1 lcredit=-1 retry=5 difok=4")
    else:
        vtn.append("用户口令复杂度设置合规")

    # 口令生存期限制
    cmd = "cat /etc/login.defs |grep  \"^PASS_MAX_DAYS\"|awk '{print $2}'"
    vres = helper.openCmd(cmd).strip()
    if vres:
        if int(vres) > 90 and "No such file" not in vres:
            vs += 1
            vt.append("口令生存期限制长于90天不合规，建议设置：/etc/login.defs修改PASS_MAX_DAYS  90")
        else:
            vtn.append("口令生存期限制等于90天合规")

    # 账号锁定策略
    cmd = "cat /etc/pam.d/login |grep \"^auth\"|grep \"deny\"|grep \"even_deny_root\"|grep \"unlock_time\""
    vres = helper.openCmd(cmd).strip()
    if vres == "" and "No such file" not in vres:
        vs += 1
        vt.append(
            "账号锁定策略设置不合规，建议设置：/etc/pam.d/login第一行添加auth required pam_tally2.so file=/var/log/tallylog deny=5 even_deny_root unlock_time=1200")
    else:
        vtn.append("账号锁定策略设置合规")

    # 超时设置
    cmd = "cat /etc/profile|grep \"TMOUT=60\""
    vres = helper.openCmd(cmd).strip()
    if vres == "" and "No such file" not in vres:
        vs += 1
        vt.append("超时设置不合规，建议设置：/etc/profile增加TMOUT=60")
    else:
        vtn.append("超时设置合规")

    ##禁用非加密远程登录协议
    # su命令使用限制
    cmd = "cat /etc/pam.d/su|grep \"^auth\"|grep -E \"sufficient|required\"|wc -l"
    vres = helper.openCmd(cmd).strip()
    if int(vres) < 2 and "No such file" not in vres:
        vs += 1
        vt.append(
            "su命令使用限制设置不合规，建议设置：/etc/pam.d/su添加auth        sufficient     /lib/security/pam_rootok.so  debug\nauth        required        /lib/security/pam_wheel.so group=wheel")
    else:
        vtn.append("su命令使用限制设置合规")

    # 启用日志记录和安全审计功能
    cmd = "cat /etc/rsyslog.conf|grep -E \"/var/log/secure|/var/adm/messages\"|wc -l"
    vres = helper.openCmd(cmd).strip()
    if int(vres) < 2 and "No such file" not in vres:
        vs += 1
        vt.append(
            "启用日志记录和安全审计功能不合规，建议设置：/etc/rsyslog.conf 修改authpriv.*      /var/log/secure\n*.err;kern.debug;daemon.notice;      /var/adm/messages")
    else:
        vtn.append("启用日志记录和安全审计功能合规")

    ##关闭无效自启动服务
    # snmp服务卸载
    cmd = "rpm -qa|grep snmp"
    vres = helper.openCmd(cmd).strip()
    if vres != "" and "No such file" not in vres:
        vs += 1
        vt.append("snmp服务已经安装不合规，建议设置：关闭snmpd服务并禁用开机自启动")
    else:
        vtn.append("snmp服务未安装合规")

    # 禁用ctrl+alt+del组合键
    cmd = "cat /etc/init/control-alt-delete.conf |grep \"start on control-alt-delete\""
    vres = helper.openCmd(cmd).strip()
    if vres != "" and not vres.startswith("#") and "No such file" not in vres:
        vs += 1
        vt.append("禁用ctrl+alt+del组合键不合规，建议设置：/etc/init/control-alt-delete.conf注释如下行 start on control-alt-delete")
    else:
        vtn.append("禁用ctrl+alt+del组合键合规")

    if vs > 0:
        score += 1
        fres.append(dict(rkey="系统安全配置检查", rval="\n".join(str(i) for i in vt), rtype=1, rnote="系统安全配置不合规"))
    else:
        fres.append(dict(rkey="系统安全配置检查", rval="\n".join(str(i) for i in vtn), rtype=0, rnote="系统安全配置合规"))
    return score, fres


if __name__ == '__main__':
    """'{"deviceId":"110100011","in_ip":"60.60.60.116","in_os":"RedHat","in_port":"22","in_pwd":"A/uOt/N48/t8wkiYVPA9qG/U6oTl6gRIlq9x4CNbuA5tgaELSobkkEdS1EaM7Fxqj6gmwPHr0kv6HP0PytI2PCXUDfDxH0dnz88ZL94N1AuQdhLsx6e1O/McX8osfqsEhwtJCEAd/Y+XmM06vnBBgPB0PTzvJbpmTzbTG1WR61E=","in_uid":"110600001","in_username":"root","in_usr":"root"}'"""
    """'{"deviceId":"110100012","in_ip":"60.60.60.205","in_os":"RedHat","in_port":"22","in_pwd":"NQTZWN7c6qx/Mjc1LiIRl2xlPj5+5w5jsAdbpQN1E21dnqazfAImji5PIWczjMHyEuy6h8bl9O18InFiHB6D0oQiZimRSZHrgmJoEsh34DWRIpy10+82DexjWO69nJWRzDlwUJ+bGi/H5av9RESVe4EEToJsUljAHZJPcoZ5Ep4=","in_uid":"110600002","in_username":"root","in_usr":"root"}'"""
    check_item = ['系统版本检查', '系统时区检查', '系统可用磁盘空间检查', '系统内存检查', '系统字符集检查', '系统网卡个数检查', '系统文件系统检查', '系统RPM包检查', '系统服务检查',
                  '系统Selinux检查', '系统透明大页检查', '系统安全配置检查', '系统参数配置检查']
    ostype, deviceId, helper = dbu.get_ssh_help()
    # dbInfo = eval(sys.argv[1])

    try:
        s12, f12 = getlinuxsafe()
        if f12:
            # print('{"check":' + json.dumps(f12[0]) + '}')
            print('msg=' + json.dumps(f12[0]))


    except Exception as e:
        errorInfo = str(e)
        print("异常：" + errorInfo)

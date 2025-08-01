#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

sys.path.append('/usr/software/knowl')

import DBUtil as dbu

import DBUtil
import psycopg2
import re
import json
import ResultCode


# global score
# score = 0
# fres = []


class Result(object):
    def __str__(self):
        return "\n".join("{}={}".format(k, getattr(self, k))
                         for k in self.__dict__.keys())


def getValue(ora, sql):
    result = ora.execute(sql)
    if (result.code != 0):
        print("msg=" + result.msg)
        sys.exit()
    return result.msg


def getsqlresult(db, sql):
    result = db.execute(sql)
    if (result.code != 0):
        msg = result.msg
        print("msg=WORD_BEGIN" + msg + "WORD_END")
        sys.exit()

    sqlresult = result.msg.fetchall()
    for resulttolist in sqlresult:
        sqlresult[sqlresult.index(resulttolist)] = list(resulttolist)
    return sqlresult


def parseURL(url):
    pattern = r'(\w+):(\w+)([thin:@/]+)([0-9.]+):(\d+)([:/])(\w+)'
    matchObj = re.match(pattern, url, re.I)
    return matchObj.group(2), matchObj.group(4), matchObj.group(5), matchObj.group(7)


def register(file_name):
    res = []
    print('{"params_reg":[]}')


def getparam(pgconn, param_name):
    sql = """select value from sc_param where sc_name='%s'""" % (param_name)

    cursor = getValue(pgconn, sql)
    results = cursor.fetchall()

    return ""


def getaixsafe():
    score = 0
    fres = []

    vs = 0
    vt = []

    # 口令策略及生存期限制
    cmd = "\"cat /etc/security/user|grep -E \\\"minlen = 8\\\"|\\\"minother = 2\\\"|\\\"maxage = 12\\\"\""
    vres = helper.openCmd(cmd).strip()
    if not ("minlen" in vres and "minother" in vres and "maxage" in vres) and not "No such file" in vres:
        vs += 1
        vt.append("""口令策略及生存期限制，建议设置：loginretries = 5
maxage = 12        
minalpha = 1            
minlen = 8              
minother = 2            
pwdwarntime = 15""")

    # snmp服务卸载
    cmd = "lssrc -a|grep snmpd"
    vres = helper.openCmd(cmd).strip()
    if "active" in vres and "No such file" not in vres:
        vs += 1
        vt.append("snmp服务已经安装不合规，请关闭snmpd服务：stopsrc -s snmpd")

    # 账号锁定
    cmd = "\"cat /etc/shadow|grep -E \\\"deamon|bin|sys|adm|uucp|nuucp|printq|guest|nobody|lpd|sshd\\\" |awk -F \\\":\\\" '{print $1\\\" \\\"$2}'\""
    vres = helper.openCmd(cmd).strip()
    for x in vres.split("\n"):
        if x.split(" ")[0] == "deamon":
            if x.split(" ")[1] != "NP":
                vs += 1
                vt.append("deamon用户未锁定")
        if x.split(" ")[0] == "bin":
            if x.split(" ")[1] != "NP":
                vs += 1
                vt.append("bin用户未锁定")
        if x.split(" ")[0] == "sys":
            if x.split(" ")[1] != "NP":
                vs += 1
                vt.append("sys用户未锁定")
        if x.split(" ")[0] == "adm":
            if x.split(" ")[1] != "NP":
                vs += 1
                vt.append("adm用户未锁定")
        if x.split(" ")[0] == "uucp":
            if x.split(" ")[1] != "NP":
                vs += 1
                vt.append("uucp用户未锁定")
        if x.split(" ")[0] == "nuucp":
            if x.split(" ")[1] != "NP":
                vs += 1
                vt.append("nuucp用户未锁定")
        if x.split(" ")[0] == "printq":
            if x.split(" ")[1] != "NP":
                vs += 1
                vt.append("printq用户未锁定")
        if x.split(" ")[0] == "guest":
            if x.split(" ")[1] != "NP":
                vs += 1
                vt.append("guest用户未锁定")
        if x.split(" ")[0] == "nobody":
            if x.split(" ")[1] != "NP":
                vs += 1
                vt.append("nobody用户未锁定")
        if x.split(" ")[0] == "lpd":
            if x.split(" ")[1] != "NP":
                vs += 1
                vt.append("lpd用户未锁定")
        if x.split(" ")[0] == "sshd":
            if x.split(" ")[1] != "NP":
                vs += 1
                vt.append("sshd用户未锁定")

    # 账户认证失败次数限制
    cmd = "\"cat /etc/security/login.cfg|grep -E \\\"logindisable|logininterval\\\"\""
    vres = helper.openCmd(cmd).strip()
    if not ("logindisable" in vres and "logininterval" in vres and "#" not in vres) and "No such file" not in vres:
        vs += 1
        vt.append("账户认证失败次数限制配置不合规，建议设置：/etc/security/login.cfg logindisable = 5 logininterval = 120")

    # Ssh方式账户认证失败次数限制
    cmd = "\"cat /etc/ssh/sshd_config|grep \\\"MaxAuthTries 5\\\"\""
    vres = helper.openCmd(cmd).strip()
    if vres == "" and "No such file" not in vres:
        vs += 1
        vt.append("Ssh方式账户认证失败次数限制不合规，建议设置：/etc/ssh/sshd_config MaxAuthTries 5")

    # 超时设置
    cmd = "cat /etc/profile|grep \"TMOUT=60\""
    vres = helper.openCmd(cmd).strip()
    if vres == "" and "No such file" not in vres:
        vs += 1
        vt.append("超时设置不合规，建议设置：/etc/profile export TMOUT=60")

    # 安全事件日志
    cmd = "\"cat /etc/syslog.conf|grep \\\"*.err;kern.debug;daemon.notice;\\\"|grep \\\"/var/adm/messages\\\"\""
    vres = helper.openCmd(cmd).strip()
    if vres == "" and "No such file" not in vres:
        vs += 1
        vt.append("安全事件日志配置不合规，建议设置：/etc/syslog.conf *.err;kern.debug;daemon.notice;        /var/adm/messages")

    # 重要文件suid、sgid权限

    # Su权限
    cmd = "\"cat /etc/security/user|grep \\\"sugroups = ALL\\\"\""
    vres = helper.openCmd(cmd).strip()
    if vres == "" and "No such file" not in vres:
        vs += 1
        vt.append("su权限配置不合规，建议设置：/etc/security/user sugroups = ALL")

    if vs > 0:
        score += 1
        fres.append(dict(rkey="系统安全配置检查", rval="\n".join(str(i) for i in vt), rtype=1, rnote="系统安全配置不合规"))
    else:
        fres.append(dict(rkey="系统安全配置检查", rval="安全检查通过", rtype=0, rnote="系统安全配置合规"))
    return score, fres


if __name__ == '__main__':
    """'{"deviceId":"110100011","in_ip":"60.60.60.116","in_os":"RedHat","in_port":"22","in_pwd":"A/uOt/N48/t8wkiYVPA9qG/U6oTl6gRIlq9x4CNbuA5tgaELSobkkEdS1EaM7Fxqj6gmwPHr0kv6HP0PytI2PCXUDfDxH0dnz88ZL94N1AuQdhLsx6e1O/McX8osfqsEhwtJCEAd/Y+XmM06vnBBgPB0PTzvJbpmTzbTG1WR61E=","in_uid":"110600001","in_username":"root","in_usr":"root"}'"""
    """'{"deviceId":"110100012","in_ip":"60.60.60.205","in_os":"RedHat","in_port":"22","in_pwd":"NQTZWN7c6qx/Mjc1LiIRl2xlPj5+5w5jsAdbpQN1E21dnqazfAImji5PIWczjMHyEuy6h8bl9O18InFiHB6D0oQiZimRSZHrgmJoEsh34DWRIpy10+82DexjWO69nJWRzDlwUJ+bGi/H5av9RESVe4EEToJsUljAHZJPcoZ5Ep4=","in_uid":"110600002","in_username":"root","in_usr":"root"}'"""
    check_item = ['系统版本检查', '系统时区检查', '系统可用磁盘空间检查', '系统内存检查', '系统字符集检查', '系统网卡个数检查', '系统文件系统检查', '系统RPM包检查', '系统服务检查',
                  '系统Selinux检查', '系统透明大页检查', '系统安全配置检查', '系统参数配置检查']
    ostype, deviceId, helper = dbu.get_ssh_help()
    # dbInfo = eval(sys.argv[1])

    try:
        s12, f12 = getaixsafe()
        # print(f12)

        if f12 != []:
            # print('{"check":' + json.dumps(f12[0]) + '}')
            print('msg=' + json.dumps(f12[0]))

    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

    except Exception as e:
        errorInfo = str(e)
        print("异常：" + errorInfo)

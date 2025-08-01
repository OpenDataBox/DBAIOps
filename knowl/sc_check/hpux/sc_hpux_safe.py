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


def gethpuxsafe():
    score = 0
    fres = []

    vs = 0
    vt = []
    vtn = []

    # 口令策略及生存期限制
    cmd = "\"cat /etc/security/user|grep \\\"^MIN_PASSWORD_LENGTH\\\"|\\\"^PASSWORD_MIN_UPPER_CASE_CHARS\\\"|\\\"^PASSWORD_MIN_SPECIAL_CHARS\\\"|\\\"^PASSWORD_MIN_LOWER_CASE_CHARS\\\"|\\\"^ALLOW_NULL_PASSWORD\\\"|\\\"^PASSWORD_MIN_DIGIT_CHARS\\\"\""
    vres = helper.openCmd(cmd).strip()
    if not (
            "MIN_PASSWORD_LENGTH" in vres and "PASSWORD_MIN_UPPER_CASE_CHARS" in vres and "PASSWORD_MIN_SPECIAL_CHARS" in vres and "PASSWORD_MIN_LOWER_CASE_CHARS" in vres and "ALLOW_NULL_PASSWORD" in vres and "PASSWORD_MIN_DIGIT_CHARS" in vres) and not "No such file" in vres:
        vs += 1
        vt.append("""口令策略及生存期限制，建议设置：
MIN_PASSWORD_LENGTH=8             #设定最小用户密码长度为8位
PASSWORD_MIN_UPPER_CASE_CHARS=1   #表示至少包括1个大写字母 
PASSWORD_MIN_DIGIT_CHARS=1        #表示至少包括1个数字
PASSWORD_MIN_SPECIAL_CHARS=1       #表示至少包括1个特殊字符
PASSWORD_MIN_LOWER_CASE_CHARS=1    #表示至少包括1个小写字母
ALLOW_NULL_PASSWORD=0             #表示密码不能为空""")
    else:
        vtn.append("口令策略及生存期限制合规")

    # snmp服务卸载
    cmd = "swlist -l product | grep snmp"
    vres = helper.openCmd(cmd).strip()
    if vres != "" and "No such file" not in vres:
        vs += 1
        vt.append("snmp服务已经安装不合规，请关闭snmpd服务：/usr/sbin/snmpd stop")
    else:
        vtn.append("snmp服务未安装合规")

    # 账号锁定
    cmd = "\"cat /etc/shadow|grep \\\"deamon|bin|sys|adm|lp|smtp|uucp|nuucp|listen|guest|nobody|lpd|noaccess\\\" |awk -F \\\":\\\" '{print $1\\\" \\\"$2}'\""
    vres = helper.openCmd(cmd).strip()
    for x in vres.split("\n"):
        if x.split(" ")[0] == "deamon":
            if x.split(" ")[1] != "NP":
                vs += 1
                vt.append("deamon用户未锁定")
            else:
                vtn.append("deamon用户已锁定")
        if x.split(" ")[0] == "bin":
            if x.split(" ")[1] != "NP":
                vs += 1
                vt.append("bin用户未锁定")
            else:
                vtn.append("bin用户已锁定")
        if x.split(" ")[0] == "sys":
            if x.split(" ")[1] != "NP":
                vs += 1
                vt.append("sys用户未锁定")
            else:
                vtn.append("sys用户已锁定")
        if x.split(" ")[0] == "adm":
            if x.split(" ")[1] != "NP":
                vs += 1
                vt.append("adm用户未锁定")
            else:
                vtn.append("adm用户已锁定")
        if x.split(" ")[0] == "lp":
            if x.split(" ")[1] != "NP":
                vs += 1
                vt.append("lp用户未锁定")
            else:
                vtn.append("lp用户已锁定")
        if x.split(" ")[0] == "smtp":
            if x.split(" ")[1] != "NP":
                vs += 1
                vt.append("smtp用户未锁定")
            else:
                vtn.append("smtp用户已锁定")
        if x.split(" ")[0] == "uucp":
            if x.split(" ")[1] != "NP":
                vs += 1
                vt.append("uucp用户未锁定")
            else:
                vtn.append("uucp用户已锁定")
        if x.split(" ")[0] == "nuucp":
            if x.split(" ")[1] != "NP":
                vs += 1
                vt.append("nuucp用户未锁定")
            else:
                vtn.append("nuucp用户已锁定")
        if x.split(" ")[0] == "listen":
            if x.split(" ")[1] != "NP":
                vs += 1
                vt.append("listen用户未锁定")
            else:
                vtn.append("listen用户已锁定")
        if x.split(" ")[0] == "guest":
            if x.split(" ")[1] != "NP":
                vs += 1
                vt.append("guest用户未锁定")
            else:
                vtn.append("guest用户已锁定")
        if x.split(" ")[0] == "nobody":
            if x.split(" ")[1] != "NP":
                vs += 1
                vt.append("nobody用户未锁定")
            else:
                vtn.append("nobody用户已锁定")
        if x.split(" ")[0] == "lpd":
            if x.split(" ")[1] != "NP":
                vs += 1
                vt.append("lpd用户未锁定")
            else:
                vtn.append("lpd用户已锁定")
        if x.split(" ")[0] == "noaccess":
            if x.split(" ")[1] != "NP":
                vs += 1
                vt.append("noaccess用户未锁定")
            else:
                vtn.append("noaccess用户已锁定")

    # 账户认证失败次数限制
    cmd = "\"cat /etc/default/security|grep \\\"^AUTH_MAXTRIES\\\"\""
    vres = helper.openCmd(cmd).strip()
    if not ("AUTH_MAXTRIES" in vres and "#" not in vres) and "No such file" not in vres:
        vs += 1
        vt.append("账户认证失败次数限制配置不合规，建议设置：/etc/default/security AUTH_MAXTRIES=5")
    else:
        vtn.append("账户认证失败次数限制配置合规")

    # 超时设置
    cmd = "\"cat /etc/profile|grep \\\"TMOUT=60\\\"\""
    vres = helper.openCmd(cmd).strip()
    if vres == "" and "No such file" not in vres:
        vs += 1
        vt.append("超时设置不合规，建议设置：/etc/profile readonly TMOUT=60; export TMOUT")
    else:
        vtn.append("超时设置合规")

    # 用户umask值
    cmd = "\"cat /etc/profile|grep \\\"^umask 022\\\"\""
    vres = helper.openCmd(cmd).strip()
    if vres == "" and "No such file" not in vres:
        vs += 1
        vt.append("用户umask设置不合规，建议设置：/etc/profile umask 022")
    else:
        vtn.append("用户umask设置合规")

    # 安全事件日志
    cmd = "\"cat /etc/syslog.conf|grep \\\"*.info;mail.none\\\"|grep \\\"/var/adm/syslog/syslog.log\\\"\""
    vres = helper.openCmd(cmd).strip()
    if vres == "" and "No such file" not in vres:
        vs += 1
        vt.append("安全事件日志配置不合规，建议设置：/etc/syslog.conf *.info;mail.none        /var/adm/syslog/syslog.log")
    else:
        vtn.append("安全事件日志配置合规")

    # 重要系统文件权限
    cmd = "ll /etc/passwd /etc/group|awk '{print $1}'|sort -u"
    vres = helper.openCmd(cmd).strip()
    if vres != "-rw-r--r--" and "No such file" not in vres:
        vs += 1
        vt.append("重要系统文件权限不合规，建议设置：chmod 644 /etc/passwd chmod 644 /etc/group")
    else:
        vtn.append("重要系统文件权限合规")

    # 限制root远程登录
    cmd = "\"cat /etc/opt/ssh/sshd_config|grep \\\"^PermitRootLogin\\\"|grep \\\"yes\\\"\""
    vres = helper.openCmd(cmd).strip()
    if vres == "" and "No such file" not in vres:
        vs += 1
        vt.append("限制root用户远程登录配置不合规，建议设置：/etc/opt/ssh/sshd_config PermitRootLogin yes")
    else:
        vtn.append("限制root用户远程登录配置合规")

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
        s12, f12 = gethpuxsafe()
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

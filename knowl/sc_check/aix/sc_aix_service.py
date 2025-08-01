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


def getaixservice():
    score = 0
    fres = []
    vs = 0
    vt = []
    vtn = []
    cmd = "lssrc -a|grep -E \"daytime|smtp|time|rexec|rlogin|rsh|rpc.tooltalk|uucp|bootps|finger|sendmail\""
    vres = helper.openCmd(cmd).strip()
    for x in vres.split("\n"):
        if x.startswith("daytime"):
            if " active" in x:
                vs += 1
                vt.append("daytime服务未关闭")
            else:
                vtn.append("daytime服务已关闭")
        if x.startswith("smtp"):
            if " active" in x:
                vs += 1
                vt.append("smtp服务未关闭")
            else:
                vtn.append("smtp服务已关闭")
        if x.startswith("time"):
            if " active" in x:
                vs += 1
                vt.append("time服务未关闭")
            else:
                vtn.append("time服务已关闭")
        if x.startswith("rexec"):
            if " active" in x:
                vs += 1
                vt.append("rexec服务未关闭")
            else:
                vtn.append("rexec服务已关闭")
        if x.startswith("rlogin"):
            if " active" in x:
                vs += 1
                vt.append("rlogin服务未关闭")
            else:
                vtn.append("rlogin服务已关闭")
        if x.startswith("rsh"):
            if " active" in x:
                vs += 1
                vt.append("rsh服务未关闭")
            else:
                vtn.append("rsh服务已关闭")
        if x.startswith("rpc.tooltalk"):
            if " active" in x:
                vs += 1
                vt.append("rpc.tooltalk服务未关闭")
            else:
                vtn.append("rpc.tooltalk服务已关闭")
        if x.startswith("uucp"):
            if " active" in x:
                vs += 1
                vt.append("uucp服务未关闭")
            else:
                vtn.append("uucp服务已关闭")
        if x.startswith("bootps"):
            if " active" in x:
                vs += 1
                vt.append("bootps服务未关闭")
            else:
                vtn.append("bootps服务已关闭")
        if x.startswith("finger"):
            if " active" in x:
                vs += 1
                vt.append("finger服务未关闭")
            else:
                vtn.append("finger服务已关闭")
        if x.startswith("sendmail"):
            if " active" in x:
                vs += 1
                vt.append("sendmail服务未关闭")
            else:
                vtn.append("sendmail服务已关闭")

    if vs > 0:
        score += 1
        fres.append(dict(rkey="系统服务检查", rval="\n".join(str(i) for i in vt), rtype=1, rnote="系统服务配置不合规"))
    else:
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
        s9, f9 = getaixservice()
        # print(f9)

        if f9 != []:
            # print('{"check":' + json.dumps(f9[0]) + '}')
            print('msg=' + json.dumps(f9[0]))

    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

    except Exception as e:
        errorInfo = str(e)
        print("异常：" + errorInfo)

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


def gethpuxfs():
    score = 0
    fres = []
    vs = 0
    vt = []
    cmd = "bdf |grep -v \"Mounted\"|awk '{print $6\" \"$2}'"
    vres = helper.openCmd(cmd).strip()
    if "/var " not in vres:
        vt.append("/var分区不存在")
    if "/tmp " not in vres:
        vt.append("/tmp分区不存在")
    if "/u01 " not in vres:
        vt.append("/u01分区不存在")

    for x in vres.split("\n"):
        if x.split(" ")[0] == "/var":
            vs += 1
            if int(x.split(" ")[1]) < 10485760:
                vs -= 1
                vt.append("/var空间小于要求的10G")
        if x.split(" ")[0] == "/tmp":
            vs += 1
            if int(x.split(" ")[1]) < 20971520:
                vs -= 1
                vt.append("/tmp空间小于要求的20G")
        if x.split(" ")[0] == "/u01":
            vs += 1
            if int(x.split(" ")[1]) < 83886080:
                vs -= 1
                vt.append("/u01空间小于要求的80G")
        if x.split(" ")[0] == "/":
            vs += 1
            if int(x.split(" ")[1]) < 52428800:
                vs -= 1
                vt.append("/空间小于要求的50G")

    if vs != 4:
        score += 1
        fres.append(dict(rkey="系统文件系统检查", rval="\n".join(str(i) for i in vt), rtype=1, rnote="系统文件系统配置不合规"))
    else:
        fres.append(dict(rkey="系统文件系统检查", rval="如下文件系统" + vres + "合规", rtype=0, rnote="系统文件系统配置合规"))
    return score, fres


if __name__ == '__main__':
    """'{"deviceId":"110100011","in_ip":"60.60.60.116","in_os":"RedHat","in_port":"22","in_pwd":"A/uOt/N48/t8wkiYVPA9qG/U6oTl6gRIlq9x4CNbuA5tgaELSobkkEdS1EaM7Fxqj6gmwPHr0kv6HP0PytI2PCXUDfDxH0dnz88ZL94N1AuQdhLsx6e1O/McX8osfqsEhwtJCEAd/Y+XmM06vnBBgPB0PTzvJbpmTzbTG1WR61E=","in_uid":"110600001","in_username":"root","in_usr":"root"}'"""
    """'{"deviceId":"110100012","in_ip":"60.60.60.205","in_os":"RedHat","in_port":"22","in_pwd":"NQTZWN7c6qx/Mjc1LiIRl2xlPj5+5w5jsAdbpQN1E21dnqazfAImji5PIWczjMHyEuy6h8bl9O18InFiHB6D0oQiZimRSZHrgmJoEsh34DWRIpy10+82DexjWO69nJWRzDlwUJ+bGi/H5av9RESVe4EEToJsUljAHZJPcoZ5Ep4=","in_uid":"110600002","in_username":"root","in_usr":"root"}'"""
    check_item = ['系统版本检查', '系统时区检查', '系统可用磁盘空间检查', '系统内存检查', '系统字符集检查', '系统网卡个数检查', '系统文件系统检查', '系统RPM包检查', '系统服务检查',
                  '系统Selinux检查', '系统透明大页检查', '系统安全配置检查', '系统参数配置检查']
    ostype, deviceId, helper = dbu.get_ssh_help()
    # dbInfo = eval(sys.argv[1])

    try:
        s7, f7 = gethpuxfs()
        # print(f7)

        if f7 != []:
            # print('{"check":' + json.dumps(f7[0]) + '}')
            print('msg=' + json.dumps(f7[0]))

    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

    except Exception as e:
        errorInfo = str(e)
        print("异常：" + errorInfo)

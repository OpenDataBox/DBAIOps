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


def getaixparam():
    score = 0
    fres = []

    vs = 0
    vt = []
    vtr = []
    ci = ['maxfree', 'minfree', 'lru_file_repage', 'maxperm%', 'minperm%', 'maxclient%']
    ci_no = ['Maxuproc', 'aio_maxreqs', 'rfc1323', 'ipqmaxlen', 'sb_max', 'tcp_sendspace', 'tcp_recvspace',
             'udp_recvspace', 'udp_sendspace', 'tcp_ephemeral_high', 'tcp_ephemeral_low', 'udp_ephemeral_high',
             'udp_ephemeral_low']

    cmd1 = "lsattr -El sys0|grep maxuproc|awk '{print $2}'"
    vres1 = helper.openCmd(cmd1).strip()
    if vres1 != "" and not "No such file" in vres1:
        if int(vres1) != 16384:
            vs += 1
            vt.append("Maxuproc设置不合规，建议值：16384")

    cmd2 = "ioo -F -a |grep -w aio_maxreqs|awk '{print $3}'"
    vres2 = helper.openCmd(cmd2).strip()
    if vres2 != "" and not "No such file" in vres2:
        if int(vres2) != 65536:
            vs += 1
            vt.append("aio_maxreqs设置不合规，建议值：65536")

    cmd3 = "no -a | grep -E \"ipqmaxlen|rfc1323|sb_max|udp_recvspace|udp_sendspace|tcp_recvspace|tcp_sendspace|tcp_ephemeral_high|tcp_ephemeral_low|udp_ephemeral_high|udp_ephemeral_low\""
    vres3 = helper.openCmd(cmd3)
    if vres3 and not "No such file" in vres3:
        for x in vres3.split("\n"):
            x = x.strip()
            if x.split(" ")[0] == "rfc1323":
                if x.split(" ")[2] != 1:
                    vs += 1
                    vt.append("rfc1323设置不合规，建议值：1")
            if x.split(" ")[0] == "sb_max":
                if x.split(" ")[2] != 4194304:
                    vs += 1
                    vt.append("sb_max设置不合规，建议值：4194304")
            if x.split(" ")[0] == "ipqmaxlen":
                if x.split(" ")[2] != 512:
                    vs += 1
                    vt.append("ipqmaxlen设置不合规，建议值：512")
            if x.split(" ")[0] == "udp_recvspace":
                if x.split(" ")[2] != 65536:
                    vs += 1
                    vt.append("udp_recvspace设置不合规，建议值：65536")
            if x.split(" ")[0] == "udp_sendspace":
                if x.split(" ")[2] != 65536:
                    vs += 1
                    vt.append("udp_sendspace设置不合规，建议值：65536")
            if x.split(" ")[0] == "tcp_recvspace":
                if x.split(" ")[2] != 1048576:
                    vs += 1
                    vt.append("tcp_recvspace设置不合规，建议值：1048576")
            if x.split(" ")[0] == "tcp_sendspace":
                if x.split(" ")[2] != 1048576:
                    vs += 1
                    vt.append("tcp_sendspace设置不合规，建议值：1048576")
            if x.split(" ")[0] == "tcp_ephemeral_high":
                if x.split(" ")[2] != 65535:
                    vs += 1
                    vt.append("tcp_ephemeral_high设置不合规，建议值：65535")
            if x.split(" ")[0] == "tcp_ephemeral_low":
                if x.split(" ")[2] != 20000:
                    vs += 1
                    vt.append("tcp_ephemeral_low设置不合规，建议值：20000")
            if x.split(" ")[0] == "udp_ephemeral_high":
                if x.split(" ")[2] != 65535:
                    vs += 1
                    vt.append("udp_ephemeral_high设置不合规，建议值：65535")
            if x.split(" ")[0] == "udp_ephemeral_low":
                if x.split(" ")[2] != 20000:
                    vs += 1
                    vt.append("udp_ephemeral_low设置不合规，建议值：20000")

    cmd = "vmo -a -F"
    vres = helper.openCmd(cmd)
    for x in vres.split("\n"):
        x = x.strip()
        if x.split(" ")[0] in ci:
            vtr.append(dict(name=x.split(" ")[0], value=x.split(" ")[2]))

    for x in vtr:
        if x.get("name") == "maxfree":
            if int(x.get("value")) != 1088:
                vs += 1
                vt.append(x.get("name") + "设置不合规，建议值：1088")

        if x.get("name") == "minfree":
            if int(x.get("value")) != 960:
                vs += 1
                vt.append(x.get("name") + "设置不合规，建议值：960")

        if x.get("name") == "lru_file_repage":
            if int(x.get("value")) != 0:
                vs += 1
                vt.append(x.get("name") + "设置不合规，建议值：0")

        if x.get("name") == "maxperm%":
            if int(x.get("value")) != 10:
                vs += 1
                vt.append(x.get("name") + "设置不合规，建议值：10%")

        if x.get("name") == "minperm%":
            if int(x.get("value")) != 3:
                vs += 1
                vt.append(x.get("name") + "设置不合规，建议值：3%")

        if x.get("name") == "maxclient%":
            if int(x.get("value")) != 10:
                vs += 1
                vt.append(x.get("name") + "设置不合规，建议值：10%")

    if vs > 0:
        score += 1
        fres.append(dict(rkey="系统参数配置检查", rval="\n".join(str(i) for i in vt), rtype=1, rnote="系统参数配置不合规"))
    else:
        fres.append(dict(rkey="系统参数配置检查", rval="AiX系统参数设置合规", rtype=0, rnote="系统参数配置合规"))
    return score, fres


if __name__ == '__main__':
    """'{"deviceId":"110100011","in_ip":"60.60.60.116","in_os":"RedHat","in_port":"22","in_pwd":"A/uOt/N48/t8wkiYVPA9qG/U6oTl6gRIlq9x4CNbuA5tgaELSobkkEdS1EaM7Fxqj6gmwPHr0kv6HP0PytI2PCXUDfDxH0dnz88ZL94N1AuQdhLsx6e1O/McX8osfqsEhwtJCEAd/Y+XmM06vnBBgPB0PTzvJbpmTzbTG1WR61E=","in_uid":"110600001","in_username":"root","in_usr":"root"}'"""
    """'{"deviceId":"110100012","in_ip":"60.60.60.205","in_os":"RedHat","in_port":"22","in_pwd":"NQTZWN7c6qx/Mjc1LiIRl2xlPj5+5w5jsAdbpQN1E21dnqazfAImji5PIWczjMHyEuy6h8bl9O18InFiHB6D0oQiZimRSZHrgmJoEsh34DWRIpy10+82DexjWO69nJWRzDlwUJ+bGi/H5av9RESVe4EEToJsUljAHZJPcoZ5Ep4=","in_uid":"110600002","in_username":"root","in_usr":"root"}'"""
    check_item = ['系统版本检查', '系统时区检查', '系统可用磁盘空间检查', '系统内存检查', '系统字符集检查', '系统网卡个数检查', '系统文件系统检查', '系统RPM包检查', '系统服务检查',
                  '系统Selinux检查', '系统透明大页检查', '系统安全配置检查', '系统参数配置检查']
    ostype, deviceId, helper = dbu.get_ssh_help()
    # dbInfo = eval(sys.argv[1])

    try:
        s13, f13 = getaixparam()
        # print(f13)

        if f13 != []:
            # print('{"check":' + json.dumps(f13[0]) + '}')
            print('msg=' + json.dumps(f13[0]))

    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

    except Exception as e:
        errorInfo = str(e)
        print("异常：" + errorInfo)

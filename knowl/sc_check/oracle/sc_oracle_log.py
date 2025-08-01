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

# ostype, deviceId, helper = dbu.get_ssh_help()

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


def getoralog(ora):
    score = 0
    fres = []
    vs = 0
    vt = []
    lg = []
    sql = """select group#,thread#,members,blocksize,bytes/1024/1024 size_mb from v$log"""
    cursor = getValue(ora, sql)
    rs = cursor.fetchall()

    if not rs == []:
        for x in rs:
            lg.append(x[0])
            if int(x[4]) < 1024:
                vs += 1
                vt.append("当前数据库日志组：" + str(x[0]) + "日志文件大小：" + str(x[4]) + "MB，不符合规范要求的1024MB")

    if len(set(lg)) <= 12:
        vs += 1
        vt.append("当前数据库日志组个数为：" + str(len(set(lg))) + "不合规，建议日志组为12组以上")

    if vs > 0:
        score += 1
        fres.append(
            dict(rkey="数据库日志文件组、文件大小检查", rval="\n".join(str(i) for i in vt), rtype=1, rnote="数据库日志文件组、文件大小检查不合规"))
    else:
        fres.append(dict(rkey="数据库日志文件组、文件大小检查", rval="日志检查通过", rtype=0, rnote="数据库日志文件组、文件大小检查合规"))
    return score, fres


if __name__ == '__main__':
    """'{"deviceId":"110100011","in_ip":"60.60.60.116","in_os":"RedHat","in_port":"22","in_pwd":"A/uOt/N48/t8wkiYVPA9qG/U6oTl6gRIlq9x4CNbuA5tgaELSobkkEdS1EaM7Fxqj6gmwPHr0kv6HP0PytI2PCXUDfDxH0dnz88ZL94N1AuQdhLsx6e1O/McX8osfqsEhwtJCEAd/Y+XmM06vnBBgPB0PTzvJbpmTzbTG1WR61E=","in_uid":"110600001","in_username":"root","in_usr":"root"}'"""
    """'{"deviceId":"110100012","in_ip":"60.60.60.205","in_os":"RedHat","in_port":"22","in_pwd":"NQTZWN7c6qx/Mjc1LiIRl2xlPj5+5w5jsAdbpQN1E21dnqazfAImji5PIWczjMHyEuy6h8bl9O18InFiHB6D0oQiZimRSZHrgmJoEsh34DWRIpy10+82DexjWO69nJWRzDlwUJ+bGi/H5av9RESVe4EEToJsUljAHZJPcoZ5Ep4=","in_uid":"110600002","in_username":"root","in_usr":"root"}'"""
    """'{"deviceId":"110100012","ora_ip":"60.60.60.169","ora_port":"1521","ora_pwd":"bSb/BhBjqyaFjEnF/26Hji4uMgxJ59mLMNqacX6CbXpqmG56iph4TvXuaeeaxq8LeW798JrRS9zwUgcjcnCd4/JgOGFzAB+X2sKnjWMCtbEOvGJyp9sU3+6Gw+RyMbzMh4q6HIf1weVIktaLqRaSd9Z03bdti6IdS1xTyT1d3wc=","ora_usr":"system","ora_sid":"orcl","ora_pwd_sys":"bSb/BhBjqyaFjEnF/26Hji4uMgxJ59mLMNqacX6CbXpqmG56iph4TvXuaeeaxq8LeW798JrRS9zwUgcjcnCd4/JgOGFzAB+X2sKnjWMCtbEOvGJyp9sU3+6Gw+RyMbzMh4q6HIf1weVIktaLqRaSd9Z03bdti6IdS1xTyT1d3wc=","ora_usr_sys":"sys"}'"""
    check_item = ['数据库版本检查', '数据库端口检查', '表空间配置检查', '数据文件自动扩展检查', '数据库参数检查', '日志文件组、文件大小检查', '控制文件个数检查', '密码过期策略禁用检查',
                  '密码5次过期策略检查']
    ora = dbu.get_ora_env()
    # dbInfo = eval(sys.argv[1])

    # host = dbInfo['ora_ip']
    # port = dbInfo['ora_port']
    # dbname = dbInfo['ora_sid']
    # usr_sys = dbInfo['ora_usr_sys']
    # pwd_sys = CommUtil.decrypt(dbInfo['ora_pwd_sys'])

    # dsnsys = oracle.makedsn(host, port, dbname)
    # connsys = oracle.connect(usr_sys, pwd_sys, dsnsys, oracle.SYSDBA)

    try:
        s6, f6 = getoralog(ora)
        # print(f6)

        if f6 != []:
            # print('{"check":' + json.dumps(f6[0]) + '}')
            print('msg=' + json.dumps(f6[0]))

    except Exception as e:
        errorInfo = str(e)
        print("异常：" + errorInfo)

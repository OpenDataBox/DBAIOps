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
    res.append(dict(ename='adisk_size', cname='AiX系统磁盘可用空间大小', desc='AiX磁盘可用空间大小，单位：GB'))
    print('{"params_reg":' + json.dumps(res) + '}')


def getparam(pgconn, param_name):
    sql = """select value from sc_param where sc_name='%s'""" % (param_name)

    cursor = getValue(pgconn, sql)
    results = cursor.fetchall()

    return ""


def getaixspace():
    score = 0
    fres = []
    cmd = "df -g|grep -v \"proc\"|awk '{print $3}'|awk '{sum += $1} END {print sum}'"
    vres = helper.openCmd(cmd).strip()
    # if int(vres) < 314572800 and "No such file" not in vres:
    if float(vres) < float(param_in) and "No such file" not in vres:
        score += 1
        fres.append(dict(rkey="系统可用磁盘空间检查", rval="当前系统可用磁盘空间为：" + str(vres) + "GB，不符合规范要求的" + param_in + "GB", rtype=1,
                         rnote="系统可用磁盘空间不合规"))
    else:
        fres.append(dict(rkey="系统可用磁盘空间检查", rval="当前系统可用磁盘空间为：" + str(vres) + "GB，符合规范要求的" + param_in + "GB", rtype=0,
                         rnote="系统可用磁盘空间合规"))
    return score, fres


if __name__ == '__main__':
    """'{"deviceId":"110100011","in_ip":"60.60.60.11","in_os":"RedHat","in_port":"22","in_pwd":"A/uOt/N48/t8wkiYVPA9qG/U6oTl6gRIlq9x4CNbuA5tgaELSobkkEdS1EaM7Fxqj6gmwPHr0kv6HP0PytI2PCXUDfDxH0dnz88ZL94N1AuQdhLsx6e1O/McX8osfqsEhwtJCEAd/Y+XmM06vnBBgPB0PTzvJbpmTzbTG1WR61E=","in_uid":"110600001","in_username":"root","in_usr":"root"}' '' '{"adisk_size":"300"}'"""
    check_item = ['系统版本检查', '系统时区检查', '系统可用磁盘空间检查', '系统内存检查', '系统字符集检查', '系统网卡个数检查', '系统文件系统检查', '系统RPM包检查', '系统服务检查',
                  '系统Selinux检查', '系统透明大页检查', '系统安全配置检查', '系统参数配置检查']
    ostype, deviceId, helper = dbu.get_ssh_help()
    # dbInfo = eval(sys.argv[1])
    extparam = eval(sys.argv[3])
    param_in = extparam['adisk_size']

    try:
        s3, f3 = getaixspace()
        # print(f3)

        if f3 != []:
            # print('{"check":' + json.dumps(f3[0]) + '}')
            print('msg=' + json.dumps(f3[0]))

    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

    # except Exception as e:
    #    errorInfo = str(e)
    #    print("异常：" + errorInfo)

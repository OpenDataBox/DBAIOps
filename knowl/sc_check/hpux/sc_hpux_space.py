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
    res.append(dict(ename='hdisk_size', cname='HPUX系统磁盘可用空间大小', desc='HPUX磁盘可用空间大小，单位：GB'))
    print('{"params_reg":' + json.dumps(res) + '}')


def getparam(pgconn, param_name):
    sql = """select value from sc_param where sc_name='%s'""" % (param_name)

    cursor = getValue(pgconn, sql)
    results = cursor.fetchall()

    return ""


def gethpuxspace():
    score = 0
    fres = []
    cmd = "bdf |awk '{print $2}'|awk '{sum += $1} END {printf \"%d\", sum}'"
    vres = helper.openCmd(cmd).strip()
    if int(vres) / 1024 / 1024 < int(param_in) and "No such file" not in vres:
        score += 1
        fres.append(dict(rkey="系统可用磁盘空间检查",
                         rval="当前系统可用磁盘空间为：" + str(round(int(vres) / 1024 / 1024, 2)) + "GB，不符合规范要求的" + param_in + "GB",
                         rtype=1, rnote="系统可用磁盘空间不合规"))
    else:
        fres.append(dict(rkey="系统可用磁盘空间检查",
                         rval="当前系统可用磁盘空间为：" + str(round(int(vres) / 1024 / 1024, 2)) + "GB，符合规范要求的" + param_in + "GB",
                         rtype=0, rnote="系统可用磁盘空间合规"))
    return score, fres


if __name__ == '__main__':
    check_item = ['系统版本检查', '系统时区检查', '系统可用磁盘空间检查', '系统内存检查', '系统字符集检查', '系统网卡个数检查', '系统文件系统检查', '系统RPM包检查', '系统服务检查',
                  '系统Selinux检查', '系统透明大页检查', '系统安全配置检查', '系统参数配置检查']
    ostype, deviceId, helper = dbu.get_ssh_help()
    # dbInfo = eval(sys.argv[1])
    extparam = eval(sys.argv[3])
    param_in = extparam['hdisk_size']

    try:
        s3, f3 = gethpuxspace()
        # print(f3)

        if f3 != []:
            # print('{"check":' + json.dumps(f3[0]) + '}')
            print('msg=' + json.dumps(f3[0]))

    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

    except Exception as e:
        errorInfo = str(e)
        print("异常：" + errorInfo)

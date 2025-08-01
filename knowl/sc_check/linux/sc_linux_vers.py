#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

sys.path.append('/usr/software/knowl')

import DBUtil as dbu

import json


def register(file_name):
    res = []
    res.append(dict(ename='os_ver', cname='系统版本', desc='系统版本，示例：6.8，7.2'))
    print('{"params_reg":' + json.dumps(res) + '}')


def getlinuxversion():
    score = 0
    fres = []
    cmd = "cat /etc/redhat-release |awk '{if(NF>5) print $7;else if(NF==5) print $4}'"
    vres = helper.openCmd(cmd).strip()
    # if vres != "6.8" and "No such file" not in vres:
    if vres != param_in and "No such file" not in vres:
        score += 1
        fres.append(dict(rkey="系统版本检查", rval="当前系统版本：" + vres + "不符合规范要求的版本：" + param_in, rtype=1, rnote="系统版本不合规"))
    else:
        fres.append(dict(rkey="系统版本检查", rval="当前系统版本：" + vres + "合规", rtype=0, rnote="系统版本合规"))
    return score, fres


if __name__ == '__main__':
    """'{"deviceId":"110100011","in_ip":"60.60.60.116","in_os":"RedHat","in_port":"22","in_pwd":"A/uOt/N48/t8wkiYVPA9qG/U6oTl6gRIlq9x4CNbuA5tgaELSobkkEdS1EaM7Fxqj6gmwPHr0kv6HP0PytI2PCXUDfDxH0dnz88ZL94N1AuQdhLsx6e1O/McX8osfqsEhwtJCEAd/Y+XmM06vnBBgPB0PTzvJbpmTzbTG1WR61E=","in_uid":"110600001","in_username":"root","in_usr":"root"}'"""
    """'{"deviceId":"110100012","in_ip":"60.60.60.205","in_os":"RedHat","in_port":"22","in_pwd":"NQTZWN7c6qx/Mjc1LiIRl2xlPj5+5w5jsAdbpQN1E21dnqazfAImji5PIWczjMHyEuy6h8bl9O18InFiHB6D0oQiZimRSZHrgmJoEsh34DWRIpy10+82DexjWO69nJWRzDlwUJ+bGi/H5av9RESVe4EEToJsUljAHZJPcoZ5Ep4=","in_uid":"110600002","in_username":"root","in_usr":"root"}'"""
    check_item = ['系统版本检查', '系统时区检查', '系统可用磁盘空间检查', '系统内存检查', '系统字符集检查', '系统网卡个数检查', '系统文件系统检查', '系统RPM包检查', '系统服务检查',
                  '系统Selinux检查', '系统透明大页检查', '系统安全配置检查', '系统参数配置检查']
    # dbInfo = eval(sys.argv[2])
    ostype, deviceId, helper = dbu.get_ssh_help()
    extparam = eval(sys.argv[3])
    param_in = extparam['os_ver']

    try:
        # register(file_name)
        s1, f1 = getlinuxversion()

        if f1:
            # print('{"check":' + json.dumps(f1[0]) + '}')
            print('msg=' + json.dumps(f1[0]))

    except Exception as e:
        errorInfo = str(e)
        print("异常：" + errorInfo)

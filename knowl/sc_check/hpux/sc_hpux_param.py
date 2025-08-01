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


def gethpuxparam():
    score = 0
    fres = []

    vs = 0
    vt = []
    nproc = 4096
    cmd_np = "/usr/sbin/kctune|grep nproc|awk '{print $2}'"
    vres_np = helper.openCmd(cmd_np).strip()
    if vres_np != "" and not "No such file" in vres_np:
        if int(vres_np) > 4096:
            nproc = int(vres_np)

    cmd_mem = "swapinfo -m |grep \"memory\"|awk '{print $2}'"
    vres_mem = helper.openCmd(cmd_mem).strip()
    if vres_mem != "" and not "No such file" in vres_mem:
        mem = int(vres_mem)

    cl = ['bufpages',
          'dbc_max_pct',
          'dbc_min_pct',
          'fs_async',
          'ksi_alloc_max',
          'max_async_ports',
          'maxfiles',
          'maxfiles_lim',
          'maxtsiz',
          'max_fcp_reqs',
          'maxusers',
          'maxvgs',
          'nfile',
          'nflocks',
          'npty',
          'num_tachyon_adapters',
          'o_sync_is_o_dsync',
          'semmap',
          'semmni',
          'semmns',
          'semmnu',
          'semvmx',
          'shmmax',
          'shmmni',
          'shmseg',
          'streampipes',
          'swapmem_on',
          'swchunk',
          'vps_ceiling'
          ]

    for x in cl:
        cmd = "/usr/sbin/kctune -q " + x + "|tail -1|awk '{print $2}'"
        vres = helper.openCmd(cmd).strip()
        if not vres.startswith("ERROR:"):
            if x == 'bufpages' and int(vres) != 0 and not "No such file" in vres:
                vs += 1
                vt.append("bufpages设置不合规，设置值：" + vres + "，建议值：0")
            if x == 'dbc_max_pct' and (int(vres) < 3 or int(vres) > 10) and not "No such file" in vres:
                vs += 1
                vt.append("dbc_max_pct设置不合规，设置值：" + vres + "，建议值：介于3和10")
            if x == 'dbc_min_pct' and (int(vres) < 2 or int(vres) > 5) and not "No such file" in vres:
                vs += 1
                vt.append("dbc_min_pct设置不合规，设置值：" + vres + "，建议值：介于2和5")
            if x == 'fs_async' and int(vres) != 0 and not "No such file" in vres:
                vs += 1
                vt.append("fs_async设置不合规，设置值：" + vres + "，建议值：0")
            if x == 'ksi_alloc_max' and int(vres) != nproc * 8 and not "No such file" in vres:
                vs += 1
                vt.append("ksi_alloc_max设置不合规，设置值：" + vres + "，建议值:" + str(nproc * 8))
            if x == 'max_async_ports' and int(vres) < 78 and not "No such file" in vres:
                vs += 1
                vt.append("max_async_ports设置不合规，设置值：" + vres + "，建议值：初始化文件中的'processes'值+oracle后台进程数")
            if x == 'maxfiles' and int(vres) != 1024 and not "No such file" in vres:
                vs += 1
                vt.append("maxfiles设置不合规，设置值：" + vres + "，建议值：1024")
            if x == 'maxfiles_lim' and int(vres) != 1024 and not "No such file" in vres:
                vs += 1
                vt.append("maxfiles_lim设置不合规，设置值：" + vres + "，建议值：1024")
            if x == 'maxtsiz' and int(vres) != 134217728 and not "No such file" in vres:
                vs += 1
                vt.append("maxtsiz设置不合规，设置值：" + vres + "，建议值:128M")
            if x == 'max_fcp_reqs' and int(vres) != 512 and not "No such file" in vres:
                vs += 1
                vt.append("max_fcp_reqs设置不合规，设置值：" + vres + "，建议值：512")
            if x == 'maxusers' and int(vres) < 64 and not "No such file" in vres:
                vs += 1
                vt.append("maxusers设置不合规，设置值：" + vres + "，建议值：64 + number of concurrent Oracle DB users")
            if x == 'maxvgs' and (int(vres) > 256 or int(vres) < 10) and not "No such file" in vres:
                vs += 1
                vt.append("maxvgs设置不合规，设置值：" + vres + "，建议值：系统的VG个数")
            if x == 'nfile' and abs(int(vres) - (nproc * 15 + 2048)) < 10 and not "No such file" in vres:
                vs += 1
                vt.append("nfile设置不合规，设置值：" + vres + "，建议值:" + str(nproc * 15 + 2048))
            if x == 'nflocks' and int(vres) < 200 and not "No such file" in vres:
                vs += 1
                vt.append("nflocks设置不合规，设置值：" + vres + "，建议值：200或者200+10*(num_clients)")
            if x == 'npty' and int(vres) < 60 and not "No such file" in vres:
                vs += 1
                vt.append("npty设置不合规，设置值：" + vres + "，建议值：60+the number of client users")
            if x == 'num_tachyon_adapters' and (int(vres) > 5 or int(vres) < 0) and not "No such file" in vres:
                vs += 1
                vt.append("num_tachyon_adapters设置不合规，设置值：" + vres + "，建议值：最小值0，最大值5")
            if x == 'o_sync_is_o_dsync' and int(vres) != 0 and not "No such file" in vres:
                vs += 1
                vt.append("o_sync_is_o_dsync设置不合规，设置值：" + vres + "，建议值:0")
            if x == 'semmni' and int(vres) != nproc and not "No such file" in vres:
                vs += 1
                vt.append("semmni设置不合规，设置值：" + vres + "，建议值:" + str(nproc))
            if x == 'semmns' and int(vres) != nproc * 2 and not "No such file" in vres:
                vs += 1
                vt.append("semmns设置不合规，设置值：" + vres + "，建议值:" + str(nproc * 2))
            if x == 'shmmax' and int(vres) != mem and not "No such file" in vres:
                vs += 1
                vt.append("shmmax设置不合规，设置值：" + vres + "，建议值:" + str(mem))
            if x == 'semmap' and int(vres) != nproc + 2 and not "No such file" in vres:
                vs += 1
                vt.append("semmap设置不合规，设置值：" + vres + "，建议值:" + str(nproc + 2))
            if x == 'semmnu' and int(vres) != nproc - 4 and not "No such file" in vres:
                vs += 1
                vt.append("semmnu设置不合规，设置值：" + vres + "，建议值:" + str(nproc - 4))
            if x == 'semvmx' and int(vres) != 32767 and not "No such file" in vres:
                vs += 1
                vt.append("semvmx设置不合规，设置值：" + vres + "，建议值:32767")
            if x == 'shmmni' and int(vres) != nproc and not "No such file" in vres:
                vs += 1
                vt.append("shmmni设置不合规，设置值：" + vres + "，建议值:" + str(nproc))
            if x == 'shmseg' and int(vres) != int(nproc / 8) and not "No such file" in vres:
                vs += 1
                vt.append("shmseg设置不合规，设置值：" + vres + "，建议值:" + str(int(nproc / 8)))
            if x == 'streampipes' and int(vres) != 0 and not "No such file" in vres:
                vs += 1
                vt.append("streampipes设置不合规，设置值：" + vres + "，建议值:0")
            if x == 'swapmem_on' and int(vres) != 1 and not "No such file" in vres:
                vs += 1
                vt.append("swapmem_on设置不合规，设置值：" + vres + "，建议值:1")
            if x == 'swchunk' and int(vres) < 4096 and not "No such file" in vres:
                vs += 1
                vt.append("swchunk设置不合规，设置值：" + vres + "，建议值:4096")
            if x == 'vps_ceiling' and int(vres) != 64 and not "No such file" in vres:
                vs += 1
                vt.append("vps_ceiling设置不合规，设置值：" + vres + "，建议值:64")

    if vs > 0:
        score += 1
        fres.append(dict(rkey="系统参数配置检查", rval="\n".join(str(i) for i in vt), rtype=1, rnote="系统参数配置不合规"))
    else:
        fres.append(dict(rkey="系统参数配置检查", rval="HPUX系统参数设置合规", rtype=0, rnote="系统参数配置合规"))
    return score, fres


if __name__ == '__main__':
    """'{"deviceId":"110100011","in_ip":"60.60.60.116","in_os":"RedHat","in_port":"22","in_pwd":"A/uOt/N48/t8wkiYVPA9qG/U6oTl6gRIlq9x4CNbuA5tgaELSobkkEdS1EaM7Fxqj6gmwPHr0kv6HP0PytI2PCXUDfDxH0dnz88ZL94N1AuQdhLsx6e1O/McX8osfqsEhwtJCEAd/Y+XmM06vnBBgPB0PTzvJbpmTzbTG1WR61E=","in_uid":"110600001","in_username":"root","in_usr":"root"}'"""
    """'{"deviceId":"110100012","in_ip":"60.60.60.205","in_os":"RedHat","in_port":"22","in_pwd":"NQTZWN7c6qx/Mjc1LiIRl2xlPj5+5w5jsAdbpQN1E21dnqazfAImji5PIWczjMHyEuy6h8bl9O18InFiHB6D0oQiZimRSZHrgmJoEsh34DWRIpy10+82DexjWO69nJWRzDlwUJ+bGi/H5av9RESVe4EEToJsUljAHZJPcoZ5Ep4=","in_uid":"110600002","in_username":"root","in_usr":"root"}'"""
    check_item = ['系统版本检查', '系统时区检查', '系统可用磁盘空间检查', '系统内存检查', '系统字符集检查', '系统网卡个数检查', '系统文件系统检查', '系统RPM包检查', '系统服务检查',
                  '系统Selinux检查', '系统透明大页检查', '系统安全配置检查', '系统参数配置检查']
    ostype, deviceId, helper = dbu.get_ssh_help()
    # dbInfo = eval(sys.argv[1])

    try:
        s13, f13 = gethpuxparam()
        # print(f13)

        if f13 != []:
            # print('{"check":' + json.dumps(f13[0]) + '}')
            print('msg=' + json.dumps(f13[0]))

    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

    # except Exception as e:
    #    errorInfo = str(e)
    #    print("异常：" + errorInfo)

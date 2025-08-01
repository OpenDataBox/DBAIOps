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


def getoraparam(ora):
    score = 0
    fres = []
    vs = 0
    vt = []
    sql_mem = """select value from v$osstat where stat_name ='PHYSICAL_MEMORY_BYTES'"""
    cursor_mem = getValue(ora, sql_mem)
    rs_mem = cursor_mem.fetchone()
    if rs_mem:
        sys_mem = int(rs_mem[0])

    sql_awri = """select snap_interval,
case when snap_interval=INTERVAL '30' MINUTE then 1 else 0 end 
 from dba_hist_wr_control"""

    cursor_awri = getValue(ora, sql_awri)
    rs_awri = cursor_awri.fetchone()
    if rs_awri:
        if rs_awri[1] == 0:
            vs += 1
            vt.append("AWR的SNAP_INTERVAL参数设置不合规，建议间隔：30分钟")

    sql_asa = """select client_name,status from DBA_AUTOTASK_CLIENT
where client_name = 'auto space advisor'"""

    cursor_asa = getValue(ora, sql_asa)
    rs_asa = cursor_asa.fetchone()
    if rs_asa:
        if rs_asa[1] == 'ENABLED':
            vs += 1
            vt.append("AUTOSPACEADVISOR参数设置不合规，建议：关闭")

    param_item = ['sga_target', 'pga_aggregate_target', 'sga_max_size', 'db_cache_size', 'shared_pool_size',
                  'memory_target', 'session_cached_cursors', 'log_buffer', 'parallel_force_local', 'open_cursors',
                  'processes',
                  'db_files', 'undo_retention', 'recyclebin', 'log_archive_dest_1', 'large_pool_size', 'audit_trail']

    sql = """select name,value from v$parameter2 
where name in ('sga_target','pga_aggregate_target','sga_max_size','db_cache_size','shared_pool_size',
'memory_target','session_cached_cursors','log_buffer','parallel_force_local','open_cursors','processes',
'db_files','undo_retention','recyclebin','log_archive_dest_1','large_pool_size','audit_trail')
"""
    cursor = getValue(ora, sql)
    rs = cursor.fetchall()
    if not rs == []:
        for x in rs:
            if x[0] == 'sga_target' and abs((sys_mem * 0.56) - int(x[1])) > 10240:
                vs += 1
                vt.append("SGA_TARGET参数设置不合规，建议初始值为：" + str(int(sys_mem * 0.56)))

            if x[0] == 'pga_aggregate_target' and abs((sys_mem * 0.14) - int(x[1])) > 10240:
                vs += 1
                vt.append("PGA_AGGREGATE_TARGET参数设置不合规，建议初始值为：" + str(int(sys_mem * 0.14)))

            if x[0] == 'sga_max_size' and abs((sys_mem * 0.56) - int(x[1])) > 10240:
                vs += 1
                vt.append("SGA_MAX_SIZE参数设置不合规，建议初始值为：" + str(int(sys_mem * 0.56)))

            if x[0] == 'db_cache_size' and abs((sys_mem * 0.28) - int(x[1])) > 10240:
                vs += 1
                vt.append("DB_CACHE_SIZE参数设置不合规，建议初始值为：" + str(int(sys_mem * 0.28)))

            if x[0] == 'shared_pool_size' and abs((sys_mem * 0.14) - int(x[1])) > 10240:
                vs += 1
                vt.append("SHARED_POOL_SIZE参数设置不合规，建议初始值为：" + str(int(sys_mem * 0.14)))

            if x[0] == 'memory_target' and int(x[1]) != 0:
                vs += 1
                vt.append("MEMORY_TARGET参数设置不合规，建议初始值为：0")

            if x[0] == 'session_cached_cursors' and int(x[1]) != 300:
                vs += 1
                vt.append("SESSION_CACHED_CURSORS参数设置不合规，建议初始值为：300")

            if x[0] == 'log_buffer' and int(x[1]) / 1024 / 1024 != 200:
                vs += 1
                vt.append("LOG_BUFFER参数设置不合规，建议初始值为：200M")

            if x[0] == 'parallel_force_local' and x[1] != 'TRUE':
                vs += 1
                vt.append("PARALLEL_FORCE_LOCAL参数设置不合规，建议初始值为：TRUE")

            if x[0] == 'open_cursors' and int(x[1]) != 500:
                vs += 1
                vt.append("OPEN_CURSORS参数设置不合规，建议初始值为：500")

            if x[0] == 'processes' and int(x[1]) != 5000:
                vs += 1
                vt.append("PROCESSES参数设置不合规，建议初始值为：5000")

            if x[0] == 'db_files' and int(x[1]) != 2000:
                vs += 1
                vt.append("DB_FILES参数设置不合规，建议初始值为：2000")

            if x[0] == 'undo_retention' and int(x[1]) != 10800:
                vs += 1
                vt.append("UNDO_RETENTION参数设置不合规，建议初始值为：10800")

            if x[0] == 'recyclebin' and x[1] != 'OFF':
                vs += 1
                vt.append("RECYCLEBIN参数设置不合规，建议初始值为：OFF")

            if x[0] == 'log_archive_dest_1':
                if x[1]:
                    if not x[1].startswith("+ARCH"):
                        vs += 1
                        vt.append("LOG_ARCHIVE_DEST_1参数设置不合规，建议初始值为：+ARCH")
                else:
                    vs += 1
                    vt.append("LOG_ARCHIVE_DEST_1参数设置不合规，建议初始值为：+ARCH")

            if x[0] == 'large_pool_size' and int(x[1]) / 1024 / 1024 != 256:
                vs += 1
                vt.append("LARGE_POOL_SIZE参数设置不合规，建议初始值为：256M")

            if x[0] == 'audit_trail' and x[1] != 'NONE':
                vs += 1
                vt.append("AUDIT_TRAIL参数设置不合规，建议初始值为：NONE")

    sqlsys = """select x.ksppinm name, y.ksppstvl value, x.ksppdesc describ
  from sys.x_$ksppi x, sys.x_$ksppcv y
 where x.inst_id = userenv('instance')
   and y.inst_id = userenv('instance')
   and x.indx = y.indx
   and x.ksppinm in ('_serial_direct_read',
                     '_gc_policy_time',
                     '_gc_undo_affinity',
                     '_optimizer_extended_cursor_sharing_rel',
                     '_optimizer_extended_cursor_sharing')
"""
    # cursys = connsys.cursor()
    # rrsys = cursys.execute(sqlsys)
    # rowsys = cursys.fetchall()
    cursor = getValue(ora, sqlsys)
    rowsys = cursor.fetchall()

    if rowsys:
        for x in rowsys:
            if x[0] == '_serial_direct_read' and x[1].upper() != 'NEVER':
                vs += 1
                vt.append("_SERIAL_DIRECT_READ参数设置不合规，建议初始值为：NEVER")

            if x[0] == '_gc_undo_affinity' and x[1] != 'FALSE':
                vs += 1
                vt.append("_GC_UNDO_AFFINITY参数设置不合规，建议初始值为：FALSE")

            if x[0] == '_gc_policy_time' and int(x[1].upper()) != 0:
                vs += 1
                vt.append("_GC_POLICT_TIME参数设置不合规，建议初始值为：0")

            if x[0] == '_optimizer_extended_cursor_sharing' and x[1].upper() != 'NONE':
                vs += 1
                vt.append("_OPTIMIZER_EXTENDED_CURSOR_SHARING参数设置不合规，建议初始值为：NONE")

            if x[0] == '_optimizer_extended_cursor_sharing_rel' and x[1].upper() != 'NONE':
                vs += 1
                vt.append("_OPTIMIZER_EXTENDED_CURSOR_SHARING_REL参数设置不合规，建议初始值为：NONE")

    if vs > 0:
        score += 1
        fres.append(dict(rkey="数据库参数检查", rval="\n".join(str(i) for i in vt), rtype=1, rnote="数据库参数检查不合规"))
    else:
        fres.append(dict(rkey="数据库参数检查", rval="参数检查通过", rtype=0, rnote="数据库参数检查合规"))
    return score, fres


if __name__ == '__main__':
    check_item = ['数据库版本检查', '数据库端口检查', '表空间配置检查', '数据文件自动扩展检查', '数据库参数检查', '日志文件组、文件大小检查', '控制文件个数检查', '密码过期策略禁用检查',
                  '密码5次过期策略检查']
    ora = dbu.get_ora_env()
    try:
        s5, f5 = getoraparam(ora)
        # print(f5)

        if f5 != []:
            # print('{"check":' + json.dumps(f5[0]) + '}')
            print('msg=' + json.dumps(f5[0]))

    except Exception as e:
        errorInfo = str(e)
        print("异常：" + errorInfo)

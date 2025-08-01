import json
import sys
import traceback
import time
from collections import Iterable

import jpype
import psycopg2
from jpype import *

sys.path.append('/usr/software/knowl')
# import DBUtil
import JavaUtil
import JavaRsa
import JMXUtil
from CommUtil import FormatTime
import HttpJmxUtil
from HttpJmxUtil import HttpJmx

OLD_GC = {'MarkSweepCompact', 'PS MarkSweep', 'ConcurrentMarkSweep',
          'Garbage collection optimized for short pausetimes Old Collector',
          'Garbage collection optimized for throughput Old Collector',
          'Garbage collection optimized for deterministic pausetimes Old Collector'}

def cs(val, dt=False):
    if val is None:
        return ''
    else:
        if dt:
            return val.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return str(val)

class Result(object):
    # pass
    def __str__(self):
        return "\n".join("{}={}".format(k, getattr(self, k))
                         for k in self.__dict__.keys())

def relate_pg2(conn, sql, nrow=0):
    result = Result()
    try:
        cur = conn.conn.cursor()
        cur.execute(sql)
        msg = []
        if nrow == 0:
            rows = cur.fetchall()
            for row in rows:
                msg.append(row)
        else:
            for i in range(nrow):
                row = cur.fetchone()
                if row is None:
                    break
                msg.append(row)
        result.code = 0
        result.msg = msg
    except psycopg2.ProgrammingError:
        result.code = 2
        result.msg = "SQL Error"
    except psycopg2.OperationalError:
        result.code = 1
        result.msg = "Connect Error"
    return result

def idx_jvm(jmx, metric):
    mbs = jmx.queryNames(javax.management.ObjectName('java.lang:type=GarbageCollector,name=*'), None)
    gcs = [item for item in mbs]
    mbs = jmx.queryNames(javax.management.ObjectName('java.lang:type=MemoryPool,name=*'), None)
    pools = [item for item in mbs]
    threading_object = "java.lang:type=Threading"
    arr = jmx.getAttributes(javax.management.ObjectName(threading_object), ['ThreadCount', 'DaemonThreadCount'])
    if len(arr) > 1:
        thread_count = arr[0].getValue().intValue()
        daemon_thread_count = arr[1].getValue().intValue()
        metric.append(dict(index_id="1000617", value=str(thread_count)))  # 活跃线程数量
        metric.append(dict(index_id="1000618", value=str(daemon_thread_count)))  # 活跃守护线程数量
        metric.append(dict(index_id="1000619", value=str(thread_count - daemon_thread_count)))  # 活跃普通线程数量
    arr = jmx.getAttributes(javax.management.ObjectName("java.lang:type=Memory"), ['HeapMemoryUsage', 'NonHeapMemoryUsage'])
    if arr:
        mem = arr[0].getValue()
        committed_mem = mem.get('committed').longValue()
        used_mem = mem.get('used').longValue()
        max_mem = mem.get('max').longValue()
        metric.append(dict(index_id="1000620", value=str(committed_mem - used_mem)))  # 空闲堆内存
        metric.append(dict(index_id="1000621", value=str(committed_mem)))  # 已分配堆内存
        metric.append(dict(index_id="1000622", value=str(used_mem)))  # 已使用堆内存
        metric.append(dict(index_id="1000623", value=str(round(used_mem * 100 / committed_mem, 2))))  # 堆内存使用率
        metric.append(dict(index_id="1000633", value=str(max_mem)))  # 最大堆内存
    load_class_count = jmx.getAttributes(javax.management.ObjectName("java.lang:type=ClassLoading"), "LoadedClassCount")
    metric.append(dict(index_id="1000604", value=str(load_class_count.intValue())))
    total_compiliation_time = jmx.getAttributes(javax.management.ObjectName("java.lang:type=Compilation"), "TotalCompilationTime")
    metric.append(dict(index_id="1000605", value=str(total_compiliation_time.longValue())))
    n1 = n2 = t1 = t2 = t3 = 0
    for gc in gcs:
        nm = gc.getCanonicalName()
        arr = jmx.getAttributes(nm, ['Name', 'CollectionCount', 'CollectionTime', 'LastGcInfo'])
        if arr:
            if str(arr[0].getValue()) in OLD_GC:
                n2 += arr[1].getValue().longValue()
                t2 += arr[2].getValue().longValue()
            n1 += arr[1].getValue().longValue()
            t1 += arr[2].getValue().longValue()
            if str(arr[0].getValue()) == "G1 Young Generation":
                t3 += arr[3].getValue().get("duration").longValue()
    if gcs:
        metric.append(dict(index_id="1000606", value=str(n1)))  # 垃圾收集调用次数
        metric.append(dict(index_id="1000607", value=str(t1)))  # 垃圾收集调用时间(ms)
        metric.append(dict(index_id="1000608", value=str(n2)))  # 老生代垃圾收集调用次数
        metric.append(dict(index_id="1000609", value=str(t2)))  # 老生代垃圾收集调用时间(ms)
        metric.append(dict(index_id="1000636", value=str(t3)))  # 最后一次GC花费的时间，单位ms
    for mp in pools:
        nm = mp.getCanonicalName()
        arr = jmx.getAttributes(nm, ['Name', 'Usage'])
        if str(arr[0].getValue()) == 'Metaspace':
            n1 = arr[1].getValue().get('committed').longValue()
            n2 = arr[1].getValue().get('used').longValue()
            metric.append(dict(index_id="1000630", value=str(n1)))  # 已分配元数据空间
            metric.append(dict(index_id="1000631", value=str(n2)))  # 已使用元数据空间
            metric.append(dict(index_id="1000632", value=str(round(n2 * 100 / n1, 2))))  # 元数据空间使用率
            break
    arr = jmx.getAttributes(javax.management.ObjectName("java.lang:type=OperatingSystem"),
                            ["OpenFileDescriptorCount", "MaxFileDescriptorCount"])
    if arr:
        metric.append(dict(index_id="1000634", value=str(arr[0].getValue().longValue())))
        metric.append(dict(index_id="1000635", value=str(arr[1].getValue().longValue())))
    arr = jmx.getAttributes(javax.management.ObjectName("java.lang:type=Runtime"), ["Uptime","Name"])
    metric.append(dict(index_id="5059999", value=str(round(arr[0].getValue().longValue() / 1000))))  # Uptime
    metric.append(dict(index_id="1000600", value=str(round(arr[0].getValue().longValue() / 1000))))  # Uptime
    pid = arr[1].getValue().split('@')[0]
    metric.append(dict(index_id="1000639", value=str(pid)))
    mbs = jmx.queryNames(javax.management.ObjectName('java.nio:type=BufferPool,name=*'), None)
    for m in mbs:
        nm = m.getCanonicalName()
        arr = jmx.getAttributes(nm, ['Count', 'TotalCapacity', 'MemoryUsed'])
        if arr:
            n1 = arr[0].getValue().longValue()
            n2 = arr[1].getValue().longValue()
            n3 = arr[2].getValue().longValue()
            if str(nm).find("name=mapped") >= 0:
                metric.append(dict(index_id="1000640", value=str(n1)))
                metric.append(dict(index_id="1000641", value=str(n2)))
                metric.append(dict(index_id="1000642", value=str(n3)))
                if n2 > 0:
                    metric.append(dict(index_id="1000643", value=str(round(n3 * 100 / n2, 2))))
                else:
                    metric.append(dict(index_id="1000643", value=str(0)))
            elif str(nm).find("name=direct") >= 0:
                metric.append(dict(index_id="1000644", value=str(n1)))
                metric.append(dict(index_id="1000645", value=str(n2)))
                metric.append(dict(index_id="1000646", value=str(n3)))
                if n2 > 0:
                    metric.append(dict(index_id="1000647", value=str(round(n3 * 100 / n2, 2))))
                else:
                    metric.append(dict(index_id="1000647", value=str(0)))

def idx_jvm2(jmx, metric):
    gcs = []
    pools = []
    mbs = jmx.queryNames('java.lang:type=GarbageCollector,name=*', None)
    for m in mbs:
        gcs.append(m)
    mbs = jmx.queryNames('java.lang:type=MemoryPool,name=*', None)
    for m in mbs:
        pools.append(m)
    object = "java.lang:type=Threading"
    arr = jmx.getAttributes(object, ['ThreadCount', 'DaemonThreadCount'])
    if arr:
        metric.append(dict(index_id="1000617", value=str(arr[0][1])))
        if len(arr) > 1:
            metric.append(dict(index_id="1000618", value=str(arr[1][1])))
            metric.append(dict(index_id="1000619", value=str(int(arr[0][1]) - int(arr[1][1]))))
        else:
            metric.append(dict(index_id="1000618", value=str(0)))
            metric.append(dict(index_id="1000619", value=str(arr[0][1])))
    object = "java.lang:type=Memory"
    arr = jmx.getAttributes(object, ['HeapMemoryUsage', 'NonHeapMemoryUsage'])
    if arr:
        mem = arr[0][1]
        n1 = int(mem.get('committed'))
        n2 = int(mem.get('used'))
        n3 = int(mem.get('max'))
        metric.append(dict(index_id="1000620", value=str(n1 - n2)))
        metric.append(dict(index_id="1000621", value=str(n1)))
        metric.append(dict(index_id="1000622", value=str(n2)))
        metric.append(dict(index_id="1000623", value=str(round(n2 * 100 / n1, 2))))
        metric.append(dict(index_id="1000633", value=str(n3)))
    object = "java.lang:type=ClassLoading"
    attribute = "LoadedClassCount"
    n = jmx.getAttribute(object, attribute)
    metric.append(dict(index_id="1000604", value=str(n)))  # JVM当前装载类
    object = "java.lang:type=Compilation"
    attribute = "TotalCompilationTime"
    n = jmx.getAttribute(object, attribute)
    metric.append(dict(index_id="1000605", value=str(n)))
    n1 = 0
    n2 = 0
    t1 = 0
    t2 = 0
    t3 = 0
    for gc in gcs:
        nm = gc
        arr = jmx.getAttributes(nm, ['Name', 'CollectionCount', 'CollectionTime', 'LastGcInfo'])
        if arr:
            if str(arr[0][1]) in OLD_GC:
                n2 += int(arr[1][1])
                t2 += int(arr[2][1])
            n1 += int(arr[1][1])
            t1 += int(arr[2][1])
            if str(arr[0][1]) == "G1 Young Generation":
                t3 = int(arr[3][1].get("duration"))
    if gcs:
        metric.append(dict(index_id="1000606", value=str(n1)))  # 垃圾收集调用次数
        metric.append(dict(index_id="1000607", value=str(t1)))  # 垃圾收集调用时间(ms)
        metric.append(dict(index_id="1000608", value=str(n2)))  # 老生代垃圾收集调用次数
        metric.append(dict(index_id="1000609", value=str(t2)))  # 老生代垃圾收集调用时间(ms)
        metric.append(dict(index_id="1000636", value=str(t3)))  # 最后一次GC花费的时间，单位ms
    for mp in pools:
        nm = mp
        arr = jmx.getAttributes(nm, ['Name', 'Usage'])
        if str(arr[0][1]) == 'Metaspace':
            n1 = int(arr[1][1].get('committed'))
            n2 = int(arr[1][1].get('used'))
            metric.append(dict(index_id="1000630", value=str(n1)))  # 已分配元数据空间
            metric.append(dict(index_id="1000631", value=str(n2)))  # 已使用元数据空间
            metric.append(dict(index_id="1000632", value=str(round(n2 * 100 / n1, 2))))
            break
    arr = jmx.getAttributes("java.lang:type=OperatingSystem", ["OpenFileDescriptorCount", "MaxFileDescriptorCount"])
    if arr:
        metric.append(dict(index_id="1000634", value=str(arr[0][1])))
        metric.append(dict(index_id="1000635", value=str(arr[1][1])))
    arr = jmx.getAttributes("java.lang:type=Runtime", ["Uptime","Name"])
    metric.append(dict(index_id="5059999", value=str(round(int(arr[0][1]) / 1000))))  # Uptime
    metric.append(dict(index_id="1000600", value=str(round(int(arr[0][1]) / 1000))))  # Uptime
    pid = arr[1][1].split('@')[0]
    metric.append(dict(index_id="1000639", value=str(pid)))
    mbs = jmx.queryNames('java.nio:type=BufferPool,name=*', None)
    for m in mbs:
        nm = m
        arr = jmx.getAttributes(nm, ['Count', 'TotalCapacity', 'MemoryUsed'])
        if arr:
            n1 = int(arr[0][1])
            n2 = int(arr[1][1])
            n3 = int(arr[2][1])
            if str(nm).find("name=mapped") >= 0:
                metric.append(dict(index_id="1000640", value=str(n1)))
                metric.append(dict(index_id="1000641", value=str(n2)))
                metric.append(dict(index_id="1000642", value=str(n3)))
                if n2 > 0:
                    metric.append(dict(index_id="1000643", value=str(round(n3 * 100 / n2, 2))))
                else:
                    metric.append(dict(index_id="1000643", value=str(0)))
            elif str(nm).find("name=direct") >= 0:
                metric.append(dict(index_id="1000644", value=str(n1)))
                metric.append(dict(index_id="1000645", value=str(n2)))
                metric.append(dict(index_id="1000646", value=str(n3)))
                if n2 > 0:
                    metric.append(dict(index_id="1000647", value=str(round(n3 * 100 / n2, 2))))
                else:
                    metric.append(dict(index_id="1000647", value=str(0)))

def idx_ugi(jmx, metric):
    try:
        if isinstance(jmx, HttpJmx):
            mb = 'Hadoop:service=HBase,name=UgiMetrics'
        else:
            mb = javax.management.ObjectName('Hadoop:service=HBase,name=UgiMetrics')
        alist = ['LoginSuccessNumOps',
'LoginSuccessAvgTime',
'LoginFailureNumOps',
'LoginFailureAvgTime',
'GetGroupsNumOps',
'GetGroupsAvgTime',
'RenewalFailuresTotal',
'RenewalFailures']
        got = set()
        vvv = jmx.getAttributes(mb, alist)
        for vv in vvv:
            if vv is not None:
                if isinstance(jmx, HttpJmx):
                    nm = vv[0]
                    ve = vv[1]
                else:
                    nm = vv.getName()
                    ve = vv.getValue()
                if nm:
                    got.add(nm)
                if not ve is None:
                    metric.append(dict(index_id=str(5050200+alist.index(nm)), value=str(ve)))
                    #print("insert into mon_index(index_type,use_flag,create_by,create_date,index_id,description,warn_rule) select 505,use_flag,create_by,create_date,%d,'%s',warn_rule from mon_index where index_id=5010350;" % (5050200+alist.index(nm),nm))
        for nm in set(alist)-got:
            metric.append(dict(index_id=str(5050200+alist.index(nm)), value=str(0)))
    except javax.management.RuntimeOperationsException as e:
        bt = str(e)
        exc_type, exc_value, exc_tb = sys.exc_info()
        for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
            bt += "\n%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname)
        print(bt)
        print(exc_type)
        print(exc_value)

def idx_cluster(jmx, metric):
    try:
        if isinstance(jmx, HttpJmx):
            mb = 'Hadoop:service=HBase,name=Master,sub=Server'
        else:
            mb = javax.management.ObjectName('Hadoop:service=HBase,name=Master,sub=Server')
        alist = ['numRegionServers',
'numDeadRegionServers',
'clusterRequests',
'averageLoad']
        vvv = jmx.getAttributes(mb, alist)
        for vv in vvv:
            if vv is not None:
                if isinstance(jmx, HttpJmx):
                    nm = vv[0]
                    ve = vv[1]
                else:
                    nm = vv.getName()
                    ve = vv.getValue()
                if not ve is None:
                    metric.append(dict(index_id=str(5050001+alist.index(nm)), value=str(ve)))
                    #print("insert into mon_index(index_type,use_flag,create_by,create_date,index_id,description,warn_rule) select 505,use_flag,create_by,create_date,%d,'%s',warn_rule from mon_index where index_id=5010350" % (5050001+alist.index(nm),nm))
        if isinstance(jmx, HttpJmx):
            mb = 'Hadoop:service=HBase,name=Master,sub=AssignmentManager'
        else:
            mb = javax.management.ObjectName('Hadoop:service=HBase,name=Master,sub=AssignmentManager')
        alist = ['ritOldestAge',
'ritCountOverThreshold',
'ritCount',
#'AssignTime_num_ops',
#'AssignTime_mean',
'RitDuration_num_ops',
'RitDuration_mean']
        vvv = jmx.getAttributes(mb, alist)
        for vv in vvv:
            if vv is not None:
                if isinstance(jmx, HttpJmx):
                    nm = vv[0]
                    ve = vv[1]
                else:
                    nm = vv.getName()
                    ve = vv.getValue()
                if not ve is None:
                    metric.append(dict(index_id=str(5050010+alist.index(nm)), value=str(ve)))
                    #print("insert into mon_index(index_type,use_flag,create_by,create_date,index_id,description,warn_rule) select 505,use_flag,create_by,create_date,%d,'%s',warn_rule from mon_index where index_id=5010350" % (5050010+alist.index(nm),nm))
        if isinstance(jmx, HttpJmx):
            mb = 'Hadoop:service=HBase,name=Master,sub=Balancer'
        else:
            mb = javax.management.ObjectName('Hadoop:service=HBase,name=Master,sub=Balancer')
        alist = ['BalancerCluster_num_ops']
        vvv = jmx.getAttributes(mb, alist)
        for vv in vvv:
            if vv is not None:
                if isinstance(jmx, HttpJmx):
                    nm = vv[0]
                    ve = vv[1]
                else:
                    nm = vv.getName()
                    ve = vv.getValue()
                if not ve is None:
                    metric.append(dict(index_id=str(5050020+alist.index(nm)), value=str(ve)))
                    #print("insert into mon_index(index_type,use_flag,create_by,create_date,index_id,description,warn_rule) select 505,use_flag,create_by,create_date,%d,'%s',warn_rule from mon_index where index_id=5010350" % (5050020+alist.index(nm),nm))
    except javax.management.RuntimeOperationsException as e:
        bt = str(e)
        exc_type, exc_value, exc_tb = sys.exc_info()
        for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
            bt += "\n%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname)
        print(bt)
        print(exc_type)
        print(exc_value)

def idx_rpc(jmx, typ, metric):
    try:
        if isinstance(jmx, HttpJmx):
            mb = 'Hadoop:service=HBase,name=%s,sub=IPC' % typ
        else:
            mb = javax.management.ObjectName('Hadoop:service=HBase,name=%s,sub=IPC' % typ)
        alist = ['queueSize',
'numOpenConnections',
'numActiveHandler',
'receivedBytes',
'sentBytes',
'authenticationSuccesses',
'authenticationFailures',
'authenticationFallbacks',
'authorizationSuccesses',
'authorizationFailures',
'exceptions',
'TotalCallTime_num_ops',
'ProcessCallTime_mean',
'QueueCallTime_mean',
'TotalCallTime_mean']
        vvv = jmx.getAttributes(mb, alist)
        for vv in vvv:
            if vv is not None:
                if isinstance(jmx, HttpJmx):
                    nm = vv[0]
                    ve = vv[1]
                else:
                    nm = vv.getName()
                    ve = vv.getValue()
                if not ve is None:
                    metric.append(dict(index_id=str(5050400+alist.index(nm)), value=str(ve)))
                    #print("insert into mon_index(index_type,use_flag,create_by,create_date,index_id,description,warn_rule) select 505,use_flag,create_by,create_date,%d,'%s',warn_rule from mon_index where index_id=5010350" % (5050400+alist.index(nm),nm))
    except javax.management.RuntimeOperationsException as e:
        bt = str(e)
        exc_type, exc_value, exc_tb = sys.exc_info()
        for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
            bt += "\n%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname)
        print(bt)
        print(exc_type)
        print(exc_value)

def idx_io(jmx, metric):
    try:
        if isinstance(jmx, HttpJmx):
            mb = 'Hadoop:service=HBase,name=RegionServer,sub=IO'
        else:
            mb = javax.management.ObjectName('Hadoop:service=HBase,name=RegionServer,sub=IO')
        alist = ['fsChecksumFailureCount',
'FsPReadTime_num_ops',
'FsPReadTime_mean',
'FsWriteTime_num_ops',
'FsWriteTime_mean',
'FsReadTime_num_ops',
'FsReadTime_mean']
        vvv = jmx.getAttributes(mb, alist)
        for vv in vvv:
            if vv is not None:
                if isinstance(jmx, HttpJmx):
                    nm = vv[0]
                    ve = vv[1]
                else:
                    nm = vv.getName()
                    ve = vv.getValue()
                if not ve is None:
                    metric.append(dict(index_id=str(5050500+alist.index(nm)), value=str(ve)))
                    #print("insert into mon_index(index_type,use_flag,create_by,create_date,index_id,description,warn_rule) select 505,use_flag,create_by,create_date,%d,'%s',warn_rule from mon_index where index_id=5010350" % (5050500+alist.index(nm),nm))
    except javax.management.RuntimeOperationsException as e:
        bt = str(e)
        exc_type, exc_value, exc_tb = sys.exc_info()
        for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
            bt += "\n%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname)
        print(bt)
        print(exc_type)
        print(exc_value)

def idx_wal(jmx, metric):
    try:
        if isinstance(jmx, HttpJmx):
            mb = 'Hadoop:service=HBase,name=RegionServer,sub=WAL'
        else:
            mb = javax.management.ObjectName('Hadoop:service=HBase,name=RegionServer,sub=WAL')
        alist = ['appendCount',
'slowAppendCount',
'rollRequest',
'errorRollRequest',
'writtenBytes',
'AppendTime_num_ops',
'AppendTime_mean',
'AppendSize_mean',
'SyncTime_num_ops',
'SyncTime_mean',
'slowSyncRollRequest']
        vvv = jmx.getAttributes(mb, alist)
        for vv in vvv:
            if vv is not None:
                if isinstance(jmx, HttpJmx):
                    nm = vv[0]
                    ve = vv[1]
                else:
                    nm = vv.getName()
                    ve = vv.getValue()
                if not ve is None:
                    metric.append(dict(index_id=str(5050520+alist.index(nm)), value=str(ve)))
                    #print("insert into mon_index(index_type,use_flag,create_by,create_date,index_id,description,warn_rule) select 505,use_flag,create_by,create_date,%d,'%s',warn_rule from mon_index where index_id=5010350" % (5050520+alist.index(nm),nm))
    except javax.management.RuntimeOperationsException as e:
        bt = str(e)
        exc_type, exc_value, exc_tb = sys.exc_info()
        for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
            bt += "\n%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname)
        print(bt)
        print(exc_type)
        print(exc_value)

def idx_wal2(jmx, metric):
    alist = ['appendCount',
'slowAppendCount',
'rollRequest',
'errorRollRequest',
'writtenBytes',
'AppendTime_num_ops',
'AppendTime_mean',
'AppendSize_mean',
'SyncTime_num_ops',
'SyncTime_mean',
'slowSyncRollRequest']
    for nm in alist:
        metric.append(dict(index_id=str(5050520+alist.index(nm)), value=str(0)))

def idx_table(jmx, metric):
    try:
        if isinstance(jmx, HttpJmx):
            mb = 'Hadoop:service=HBase,name=RegionServer,sub=Tables'
        else:
            mb = javax.management.ObjectName('Hadoop:service=HBase,name=RegionServer,sub=Tables')
        alist = ['numTables']
        vvv = jmx.getAttributes(mb, alist)
        for vv in vvv:
            if vv is not None:
                if isinstance(jmx, HttpJmx):
                    nm = vv[0]
                    ve = vv[1]
                else:
                    nm = vv.getName()
                    ve = vv.getValue()
                if not ve is None:
                    metric.append(dict(index_id=str(5050300+alist.index(nm)), value=str(ve)))
                    #print("insert into mon_index(index_type,use_flag,create_by,create_date,index_id,description,warn_rule) select 505,use_flag,create_by,create_date,%d,'%s',warn_rule from mon_index where index_id=5010350" % (5050300+alist.index(nm),nm))
        if isinstance(jmx, HttpJmx):
            mb = 'Hadoop:service=HBase,name=RegionServer,sub=TableLatencies'
        else:
            mb = javax.management.ObjectName('Hadoop:service=HBase,name=RegionServer,sub=TableLatencies')
        alist = ['Namespace_hbase_table_namespace_metric_getTime_num_ops',
'Namespace_hbase_table_namespace_metric_getTime_mean',
'Namespace_hbase_table_namespace_metric_scanTime_num_ops',
'Namespace_hbase_table_namespace_metric_scanTime_mean',
'Namespace_hbase_table_namespace_metric_putTime_num_ops',
'Namespace_hbase_table_namespace_metric_putTime_mean',
'Namespace_hbase_table_namespace_metric_incrementTime_num_ops',
'Namespace_hbase_table_namespace_metric_incrementTime_mean',
'Namespace_hbase_table_namespace_metric_appendTime_num_ops',
'Namespace_hbase_table_namespace_metric_appendTime_mean',
'Namespace_hbase_table_namespace_metric_deleteTime_num_ops',
'Namespace_hbase_table_namespace_metric_deleteTime_mean']
        vvv = jmx.getAttributes(mb, alist)
        for vv in vvv:
            if vv is not None:
                if isinstance(jmx, HttpJmx):
                    nm = vv[0]
                    ve = vv[1]
                else:
                    nm = vv.getName()
                    ve = vv.getValue()
                if not ve is None:
                    metric.append(dict(index_id=str(5050310+alist.index(nm)), value=str(ve)))
                    #print("insert into mon_index(index_type,use_flag,create_by,create_date,index_id,description,warn_rule) select 505,use_flag,create_by,create_date,%d,'%s',warn_rule from mon_index where index_id=5010350" % (5050310+alist.index(nm),nm))
    except javax.management.RuntimeOperationsException as e:
        bt = str(e)
        exc_type, exc_value, exc_tb = sys.exc_info()
        for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
            bt += "\n%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname)
        print(bt)
        print(exc_type)
        print(exc_value)

def idx_region(jmx, metric):
    try:
        if isinstance(jmx, HttpJmx):
            mb = 'Hadoop:service=HBase,name=RegionServer,sub=Server'
        else:
            mb = javax.management.ObjectName('Hadoop:service=HBase,name=RegionServer,sub=Server')
        alist = ['hlogFileCount',
'hlogFileSize',
'memStoreSize',
'storeCount',
'storeFileCount',
'storeFileSize',
'flushedCellsSize',
'updatesBlockedTime',
'splitQueueLength',
'compactionQueueLength',
'flushQueueLength',
'slowAppendCount',
'slowDeleteCount',
'slowGetCount',
'slowIncrementCount',
'slowPutCount',
'splitRequestCount',
'splitSuccessCount',
'blockCacheCount',
'blockCacheHitCount',
'blockCacheMissCount',
'blockCacheExpressHitPercent',
'blockCacheSize',
'staticBloomSize',
'staticIndexSize',
'storeFileIndexSize',
'totalRequestCount',
'readRequestCount',
'writeRequestCount',
'mutationsWithoutWALCount',
'mutationsWithoutWALSize',
'Replay_num_ops',
'Replay_mean',
'Replay_num_ops',
'Replay_mean',
'FlushTime_num_ops',
'FlushTime_mean',
'Append_num_ops',
'Append_mean',
'CheckAndMutate_num_ops',
'CheckAndMutate_mean',
'Delete_num_ops',
'Delete_mean',
'Increment_num_ops',
'Increment_mean',
'Put_num_ops',
'Put_mean',
'Get_num_ops',
'Get_mean',
'ScanTime_num_ops',
'ScanTime_mean',
'ScanSize_mean',
'totalBytesRead',
'localBytesRead',
'flushedCellsCount',
'percentFilesLocal',
'percentFilesLocalSecondaryRegions']
        vvv = jmx.getAttributes(mb, alist)
        for vv in vvv:
            if vv is not None:
                if isinstance(jmx, HttpJmx):
                    nm = vv[0]
                    ve = vv[1]
                else:
                    nm = vv.getName()
                    ve = vv.getValue()
                if not ve is None:
                    metric.append(dict(index_id=str(5050100+alist.index(nm)), value=str(ve)))
                    #print("insert into mon_index(index_type,use_flag,create_by,create_date,index_id,description,warn_rule) select 505,use_flag,create_by,create_date,%d,'%s',warn_rule from mon_index where index_id=5010350" % (5050100+alist.index(nm),nm))
    except javax.management.RuntimeOperationsException as e:
        bt = str(e)
        exc_type, exc_value, exc_tb = sys.exc_info()
        for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
            bt += "\n%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname)
        print(bt)
        print(exc_type)
        print(exc_value)

def fillInfo(pg, target_id, dbInfo):
    sql = "select ip,port,user,password from mgt_system where uid='%s' and use_flag" % target_id
    result = relate_pg2(pg, sql)
    if result.code == 0 and len(result.msg) > 0:
        dbInfo['target_ip'] = result.msg[0][0]
        dbInfo['target_port'] = result.msg[0][1]
        dbInfo['target_usr'] = result.msg[0][2]
        dbInfo['target_pwd'] = result.msg[0][3]

if __name__ == '__main__':
    dbInfo = eval(sys.argv[1])
    pg, target_id = JavaUtil.get_pg_env(dbInfo, 0)
    fillInfo(pg, target_id, dbInfo)
    host = dbInfo['target_ip']
    port = dbInfo['target_port']
    usr = dbInfo['target_usr']
    pwd = dbInfo['target_pwd']
    ct = time.time()
    if pwd:
        pwd = JavaRsa.decrypt_java(pwd)
    #jmxsoc = JMXUtil.connect(host, port, 'rmi', usr, pwd)
    #jmx = jmxsoc.getMBeanServerConnection();
    #jmxsoc = JMXUtil.Jmx(host, port, 'rmi', usr, pwd)
    #jmx = jmxsoc.jmx
    jmxsoc = None
    jmx = HttpJmxUtil.HttpJmx(host, port, usr, pwd)
    jmx.connect()
    ct2 = time.time()
    typ = -1
    if isinstance(jmx, HttpJmx):
        mbs = jmx.queryNames('Hadoop:service=HBase,name=Master,sub=Server',None)
    else:
        mbs = jmx.queryNames(javax.management.ObjectName('Hadoop:service=HBase,name=Master,sub=Server'),None)
    if mbs:
        typ = 0
    else:
        if isinstance(jmx, HttpJmx):
            mbs = jmx.queryNames('Hadoop:service=HBase,name=RegionServer,sub=Server',None)
        else:
            mbs = jmx.queryNames(javax.management.ObjectName('Hadoop:service=HBase,name=RegionServer,sub=Server'),None)
        if mbs:
            typ = 1
    if typ == -1:
        print("msg=对象类型非HMaster或RegionServer")
        sys.exit(1)
    metric = []
    metric.append(dict(index_id="1000102", value=str(int((ct2-ct)*1000))))
    metric.append(dict(index_id="5010000", value="连接成功"))
    if typ == 0:
        if isinstance(jmx, HttpJmx):
            idx_jvm2(jmx, metric)
        else:
            idx_jvm(jmx, metric)
        idx_cluster(jmx, metric)
        idx_ugi(jmx, metric)
        idx_rpc(jmx, 'Master', metric)
        idx_io(jmx, metric)
        idx_wal2(jmx, metric)
    else:
        if isinstance(jmx, HttpJmx):
            idx_jvm2(jmx, metric)
        else:
            idx_jvm(jmx, metric)
        idx_region(jmx, metric)
        idx_ugi(jmx, metric)
        idx_table(jmx, metric)
        idx_rpc(jmx, 'RegionServer', metric)
        idx_io(jmx, metric)
        idx_wal(jmx, metric)
    if jmxsoc:
        jmxsoc.close();
    ct3 = time.time()
    metric.append(dict(index_id="1000101", value=str(int((ct3-ct2)*1000))))
    print('{"results":' + json.dumps(metric) + '}')

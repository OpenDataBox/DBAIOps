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
        cur = conn.cursor()
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

def jmx_get_attribute(jmx, object_name, attribute=None):
    ev = None
    try:
        if isinstance(attribute, list) or not attribute:
            ev = []
            arr = jmx.getAttributes(javax.management.ObjectName(object_name), attribute)
        else:
            arr = jmx.getAttribute(javax.management.ObjectName(object_name), attribute)
    except:
        arr = ev
    return arr


def metric_append(metric, index_id, value):
    if isinstance(value, list):
        metric.append(dict(index_id=index_id, value=value))
    else:
        metric.append(dict(index_id=index_id, value=str(value)))

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
    metric.append(dict(index_id="5010001", value=str(round(arr[0].getValue().longValue() / 1000))))  # Uptime
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
    metric.append(dict(index_id="5010001", value=str(round(int(arr[0][1]) / 1000))))  # Uptime
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

def idx_process_oom_score(helper):
    runtime_object = f"java.lang:type=Runtime"
    attr_name = ['Name']
    attr = jmx_get_attribute(jmx, runtime_object, attr_name)
    process_id = attr[0].getValue().split('@')[0]
    cmd = f"cat /proc/{process_id}/oom_score"
    oom_score = helper.exec_cmd(cmd).strip()
    metric_append(metric, 1000638, oom_score)

def idx_nnload(jmx, metric):
    vals = None
    mb = None
    try:
        if isinstance(jmx, HttpJmx):
            mb = 'Hadoop:service=NameNode,name=NameNodeActivity'
        else:
            mb = javax.management.ObjectName('Hadoop:service=NameNode,name=NameNodeActivity')
        alist = ['CreateFileOps',
'FilesCreated',
'FilesAppended',
'GetBlockLocations',
'FilesRenamed',
'FilesTruncated',
'GetListingOps',
'DeleteFileOps',
'FilesDeleted',
'FileInfoOps',
'AddBlockOps',
'GetAdditionalDatanodeOps',
'CreateSymlinkOps',
'GetLinkTargetOps',
'FilesInGetListingOps',
'SuccessfulReReplications',
'NumTimesReReplicationNotScheduled',
'TimeoutReReplications',
'AllowSnapshotOps',
'DisallowSnapshotOps',
'CreateSnapshotOps',
'DeleteSnapshotOps',
'RenameSnapshotOps',
'ListSnapshottableDirOps',
'SnapshotDiffReportOps',
'BlockReceivedAndDeletedOps',
'StorageBlockReportOps',
'BlockOpsQueued',
'BlockOpsBatched',
'TransactionsNumOps',
'TransactionsAvgTime',
'SyncsNumOps',
'SyncsAvgTime',
'TransactionsBatchedInSync',
'BlockReportNumOps',
'BlockReportAvgTime',
'CacheReportNumOps',
'CacheReportAvgTime',
'GenerateEDEKTimeNumOps',
'GenerateEDEKTimeAvgTime',
'WarmUpEDEKTimeNumOps',
'WarmUpEDEKTimeAvgTime',
'ResourceCheckTimeNumOps',
'ResourceCheckTimeAvgTime',
'SafeModeTime',
'FsImageLoadTime',
'GetEditNumOps',
'GetEditAvgTime',
'GetImageNumOps',
'GetImageAvgTime',
'PutImageNumOps',
'PutImageAvgTime',
'TotalFileOps']
        vvv = jmx.getAttributes(mb, alist)
        for vv in vvv:
            if vv:
                if isinstance(jmx, HttpJmx):
                    nm = vv[0]
                    ve = vv[1]
                else:
                    nm = str(vv.getName())
                    ve = vv.getValue()
                if not ve is None:
                    if nm.find('AvgTime') > 0:
                        metric.append(dict(index_id=str(5011100+alist.index(nm)), value=str(ve)))
                    else: 
                        metric.append(dict(index_id=str(5010100+alist.index(nm)), value=str(ve)))
    except javax.management.RuntimeOperationsException as e:
        bt = str(e)
        exc_type, exc_value, exc_tb = sys.exc_info()
        for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
            bt += "\n%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname)
        print(bt)
        print(exc_type)
        print(exc_value)

def idx_ugi(jmx, mb, metric):
    try:
        #mb = javax.management.ObjectName('Hadoop:service=NameNode,name=UgiMetrics')
        alist = ['LoginSuccessNumOps',
'LoginSuccessAvgTime',
'LoginFailureNumOps',
'LoginFailureAvgTime',
'GetGroupsNumOps',
'GetGroupsAvgTime',
'RenewalFailuresTotal',
'RenewalFailures']
        vvv = jmx.getAttributes(mb, alist)
        for vv in vvv:
            if vv:
                if isinstance(jmx, HttpJmx):
                    nm = vv[0]
                    ve = vv[1]
                else:
                    nm = str(vv.getName())
                    ve = vv.getValue()
                if not ve is None:
                    if nm.find('AvgTime') > 0:
                        metric.append(dict(index_id=str(5011200+alist.index(nm)), value=str(ve)))
                    else: 
                        metric.append(dict(index_id=str(5010200+alist.index(nm)), value=str(ve)))
    except javax.management.RuntimeOperationsException as e:
        bt = str(e)
        exc_type, exc_value, exc_tb = sys.exc_info()
        for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
            bt += "\n%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname)
        print(bt)
        print(exc_type)
        print(exc_value)

def idx_nnst(jmx, metric):
    try:
        if isinstance(jmx, HttpJmx):
            mb = 'Hadoop:service=NameNode,name=NameNodeStatus'
        else:
            mb = javax.management.ObjectName('Hadoop:service=NameNode,name=NameNodeStatus')
        alist = ['CreateFileOps',
'NNRole',
'HostAndPort',
'SecurityEnabled',
'LastHATransitionTime',
'BytesWithFutureGenerationStamps',
'SlowPeersReport',
'SlowDisksReport',
'State']
        vvv = jmx.getAttributes(mb, alist)
        for vv in vvv:
            if vv:
                if isinstance(jmx, HttpJmx):
                    nm = vv[0]
                    ve = vv[1]
                else:
                    nm = str(vv.getName())
                    ve = vv.getValue()
    except javax.management.RuntimeOperationsException as e:
        bt = str(e)
        exc_type, exc_value, exc_tb = sys.exc_info()
        for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
            bt += "\n%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname)
        print(bt)
        print(exc_type)
        print(exc_value)

def idx_nninfo(jmx, metric):
    try:
        if isinstance(jmx, HttpJmx):
            mb = 'Hadoop:service=NameNode,name=NameNodeInfo'
        else:
            mb = javax.management.ObjectName('Hadoop:service=NameNode,name=NameNodeInfo')
        alist = ['Used',
'Version',
'Total',
'UpgradeFinalized',
'ClusterId',
'Free',
'Safemode',
'NonDfsUsedSpace',
'PercentUsed',
'BlockPoolUsedSpace',
'PercentBlockPoolUsed',
'PercentRemaining',
'CacheCapacity',
'CacheUsed',
'TotalBlocks',
'TotalFiles',
'NumberOfMissingBlocks',
'NumberOfMissingBlocksWithReplicationFactorOne',
'LiveNodes',
'DeadNodes',
'DecomNodes',
'EnteringMaintenanceNodes',
'BlockPoolId',
'NameDirStatuses',
'NodeUsage',
'NameJournalStatus',
'JournalTransactionInfo',
'NNStarted',
'NNStartedTimeInMillis',
'CompileInfo',
'CorruptFiles',
'NumberOfSnapshottableDirs',
'DistinctVersionCount',
'DistinctVersions',
'SoftwareVersion',
'NameDirSize',
'RollingUpgradeStatus',
'Threads']
        vvv = jmx.getAttributes(mb, alist)
        for vv in vvv:
            if vv:
                if isinstance(jmx, HttpJmx):
                    nm = vv[0]
                    ve = vv[1]
                else:
                    nm = str(vv.getName())
                    ve = vv.getValue()
    except javax.management.RuntimeOperationsException as e:
        bt = str(e)
        exc_type, exc_value, exc_tb = sys.exc_info()
        for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
            bt += "\n%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname)
        print(bt)
        print(exc_type)
        print(exc_value)

def idx_fsns(jmx, metric):
    try:
        if isinstance(jmx, HttpJmx):
            mb = 'Hadoop:service=NameNode,name=FSNamesystem'
        else:
            mb = javax.management.ObjectName('Hadoop:service=NameNode,name=FSNamesystem')
        alist = ['MissingBlocks',
'MissingReplOneBlocks',
'ExpiredHeartbeats',
'TransactionsSinceLastCheckpoint',
'TransactionsSinceLastLogRoll',
'LastWrittenTransactionId',
'LastCheckpointTime',
'CapacityTotal',
'CapacityTotalGB',
'CapacityUsed',
'CapacityUsedGB',
'CapacityRemaining',
'CapacityRemainingGB',
'CapacityUsedNonDFS',
'TotalLoad',
'SnapshottableDirectories',
'Snapshots',
'NumEncryptionZones',
'LockQueueLength',
'BlocksTotal',
'NumFilesUnderConstruction',
'NumActiveClients',
'FilesTotal',
'PendingReplicationBlocks',
'UnderReplicatedBlocks',
'CorruptBlocks',
'ScheduledReplicationBlocks',
'PendingDeletionBlocks',
'ExcessBlocks',
'NumTimedOutPendingReplications',
'PostponedMisreplicatedBlocks',
'PendingDataNodeMessageCount',
'MillisSinceLastLoadedEdits',
'BlockCapacity',
'NumLiveDataNodes',
'NumDeadDataNodes',
'NumDecomLiveDataNodes',
'NumDecomDeadDataNodes',
'VolumeFailuresTotal',
'EstimatedCapacityLostTotal',
'NumDecommissioningDataNodes',
'StaleDataNodes',
'NumStaleStorages',
'TotalFiles',
'TotalSyncCount',
'NumInMaintenanceLiveDataNodes',
'NumInMaintenanceDeadDataNodes',
'NumEnteringMaintenanceDataNodes']
        vvv = jmx.getAttributes(mb, alist)
        for vv in vvv:
            if vv:
                if isinstance(jmx, HttpJmx):
                    nm = vv[0]
                    ve = vv[1]
                else:
                    nm = str(vv.getName())
                    ve = vv.getValue()
                if not ve is None:
                    if nm.find('AvgTime') > 0:
                        metric.append(dict(index_id=str(5011300+alist.index(nm)), value=str(ve)))
                    else:
                        metric.append(dict(index_id=str(5010300+alist.index(nm)), value=str(ve)))
    except javax.management.RuntimeOperationsException as e:
        bt = str(e)
        exc_type, exc_value, exc_tb = sys.exc_info()
        for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
            bt += "\n%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname)
        print(bt)
        print(exc_type)
        print(exc_value)

def idx_rpc(jmx, mb, metric):
    try:
        #mb = javax.management.ObjectName('Hadoop:service=NameNode,name=RpcActivityForPort9000')
        alist = ['ReceivedBytes',
'SentBytes',
'RpcQueueTimeNumOps',
'RpcQueueTimeAvgTime',
'RpcLockWaitTimeNumOps',
'RpcLockWaitTimeAvgTime',
'RpcProcessingTimeNumOps',
'RpcProcessingTimeAvgTime',
'DeferredRpcProcessingTimeNumOps',
'DeferredRpcProcessingTimeAvgTime',
'RpcAuthenticationFailures',
'RpcAuthenticationSuccesses',
'RpcAuthorizationFailures',
'RpcAuthorizationSuccesses',
'RpcClientBackoff',
'RpcSlowCalls',
'NumOpenConnections',
'CallQueueLength',
'NumDroppedConnections']
        vvv = jmx.getAttributes(mb, alist)
        i = 0
        for vv in vvv:
            if vv:
                if isinstance(jmx, HttpJmx):
                    nm = vv[0]
                    ve = vv[1]
                else:
                    nm = str(vv.getName())
                    ve = vv.getValue()
                if not ve is None:
                    if nm.find('AvgTime') > 0:
                        metric.append(dict(index_id=str(5011400+alist.index(nm)), value=str(ve)))
                    else:
                        metric.append(dict(index_id=str(5010400+alist.index(nm)), value=str(ve)))
            elif i == 4:
                metric.append(dict(index_id=str(5010400+alist.index('RpcLockWaitTimeNumOps')), value=str(0)))
            elif i == 5:
                metric.append(dict(index_id=str(5011400+alist.index('RpcLockWaitTimeAvgTime')), value=str(0)))
            i += 1
    except javax.management.RuntimeOperationsException as e:
        bt = str(e)
        exc_type, exc_value, exc_tb = sys.exc_info()
        for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
            bt += "\n%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname)
        print(bt)
        print(exc_type)
        print(exc_value)

def idx_fsds(jmx, metric):
    try:
        if isinstance(jmx, HttpJmx):
            mb = 'Hadoop:service=DataNode,name=FSDatasetState'
        else:
            mb = javax.management.ObjectName('Hadoop:service=DataNode,name=FSDatasetState')
        alist = ['Capacity',
'DfsUsed',
'Remaining',
'NumFailedVolumes',
'LastVolumeFailureDate',
'EstimatedCapacityLostTotal',
'CacheUsed',
'CacheCapacity',
'NumBlocksCached',
'NumBlocksFailedToCache',
'NumBlocksFailedToUnCache']
        vvv = jmx.getAttributes(mb, alist)
        for vv in vvv:
            if vv:
                if isinstance(jmx, HttpJmx):
                    nm = vv[0]
                    ve = vv[1]
                else:
                    nm = str(vv.getName())
                    ve = vv.getValue()
                if not ve is None:
                    metric.append(dict(index_id=str(5010500+alist.index(nm)), value=str(ve)))
    except javax.management.RuntimeOperationsException as e:
        bt = str(e)
        exc_type, exc_value, exc_tb = sys.exc_info()
        for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
            bt += "\n%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname)
        print(bt)
        print(exc_type)
        print(exc_value)

def idx_dnload(jmx, mb, metric):
    try:
        #mb = javax.management.ObjectName('Hadoop:service=DataNode,name=DataNodeActivity-test54-50010')
        alist = ['BytesWritten',
'TotalWriteTime',
'BytesRead',
'TotalReadTime',
'BlocksWritten',
'BlocksRead',
'BlocksReplicated',
'BlocksRemoved',
'BlocksVerified',
'BlockVerificationFailures',
'BlocksCached',
'BlocksUncached',
'ReadsFromLocalClient',
'ReadsFromRemoteClient',
'WritesFromLocalClient',
'WritesFromRemoteClient',
'BlocksGetLocalPathInfo',
'RemoteBytesRead',
'RemoteBytesWritten',
'RamDiskBlocksWrite',
'RamDiskBlocksWriteFallback',
'RamDiskBytesWrite',
'RamDiskBlocksReadHits',
'RamDiskBlocksEvicted',
'RamDiskBlocksEvictedWithoutRead',
'RamDiskBlocksEvictionWindowMsNumOps',
'RamDiskBlocksEvictionWindowMsAvgTime',
'RamDiskBlocksLazyPersisted',
'RamDiskBlocksDeletedBeforeLazyPersisted',
'RamDiskBytesLazyPersisted',
'RamDiskBlocksLazyPersistWindowMsNumOps',
'RamDiskBlocksLazyPersistWindowMsAvgTime',
'FsyncCount',
'VolumeFailures',
'DatanodeNetworkErrors',
'ReadBlockOpNumOps',
'ReadBlockOpAvgTime',
'WriteBlockOpNumOps',
'WriteBlockOpAvgTime',
'BlockChecksumOpNumOps',
'BlockChecksumOpAvgTime',
'CopyBlockOpNumOps',
'CopyBlockOpAvgTime',
'ReplaceBlockOpNumOps',
'ReplaceBlockOpAvgTime',
'HeartbeatsNumOps',
'HeartbeatsAvgTime',
'HeartbeatsTotalNumOps',
'HeartbeatsTotalAvgTime',
'LifelinesNumOps',
'LifelinesAvgTime',
'BlockReportsNumOps',
'BlockReportsAvgTime',
'IncrementalBlockReportsNumOps',
'IncrementalBlockReportsAvgTime',
'CacheReportsNumOps',
'CacheReportsAvgTime',
'PacketAckRoundTripTimeNanosNumOps',
'PacketAckRoundTripTimeNanosAvgTime',
'FlushNanosNumOps',
'FlushNanosAvgTime',
'FsyncNanosNumOps',
'FsyncNanosAvgTime',
'SendDataPacketBlockedOnNetworkNanosNumOps',
'SendDataPacketBlockedOnNetworkNanosAvgTime',
'SendDataPacketTransferNanosNumOps',
'SendDataPacketTransferNanosAvgTime',
'BlocksInPendingIBR',
'BlocksReceivingInPendingIBR',
'BlocksReceivedInPendingIBR',
'BlocksDeletedInPendingIBR']
        vvv = jmx.getAttributes(mb, alist)
        for vv in vvv:
            if vv:
                if isinstance(jmx, HttpJmx):
                    nm = vv[0]
                    ve = vv[1]
                else:
                    nm = str(vv.getName())
                    ve = vv.getValue()
                if not ve is None:
                    if nm.find('AvgTime') > 0:
                        metric.append(dict(index_id=str(5011600+alist.index(nm)), value=str(ve)))
                    else:
                        metric.append(dict(index_id=str(5010600+alist.index(nm)), value=str(ve)))
    except javax.management.RuntimeOperationsException as e:
        bt = str(e)
        exc_type, exc_value, exc_tb = sys.exc_info()
        for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
            bt += "\n%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname)
        print(bt)
        print(exc_type)
        print(exc_value)

def idx_dninfo(jmx, metric):
    try:
        if isinstance(jmx, HttpJmx):
            mb = 'Hadoop:service=DataNode,name=DataNodeInfo'
        else:
            mb = javax.management.ObjectName('Hadoop:service=DataNode,name=DataNodeInfo')
        alist = ['Version',
'XceiverCount',
'DatanodeNetworkCounts',
'XmitsInProgress',
'RpcPort',
'DataPort',
'HttpPort',
'NamenodeAddresses',
'DatanodeHostname',
'BPServiceActorInfo',
'VolumeInfo',
'ClusterId',
'SendPacketDownstreamAvgInfo',
'SlowDisks']
        vvv = jmx.getAttributes(mb, alist)
        for vv in vvv:
            if vv:
                if isinstance(jmx, HttpJmx):
                    nm = vv[0]
                    ve = vv[1]
                else:
                    nm = str(vv.getName())
                    ve = vv.getValue()
    except javax.management.RuntimeOperationsException as e:
        bt = str(e)
        exc_type, exc_value, exc_tb = sys.exc_info()
        for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
            bt += "\n%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname)
        print(bt)
        print(exc_type)
        print(exc_value)

def idx_vol(jmx, mb, metric):
    try:
        #mb = javax.management.ObjectName('Hadoop:service=DataNode,name=DataNodeVolume')
        alist = ['TotalMetadataOperations',
'MetadataOperationRateNumOps',
'MetadataOperationRateAvgTime',
'TotalDataFileIos',
'DataFileIoRateNumOps',
'DataFileIoRateAvgTime',
'FlushIoRateNumOps',
'FlushIoRateAvgTime',
'SyncIoRateNumOps',
'SyncIoRateAvgTime',
'ReadIoRateNumOps',
'ReadIoRateAvgTime',
'WriteIoRateNumOps',
'WriteIoRateAvgTime',
'TotalFileIoErrors',
'FileIoErrorRateNumOps',
'FileIoErrorRateAvgTime']
        vvv = jmx.getAttributes(mb, alist)
        for vv in vvv:
            if vv:
                if isinstance(jmx, HttpJmx):
                    nm = vv[0]
                    ve = vv[1]
                else:
                    nm = str(vv.getName())
                    ve = vv.getValue()
                if not ve is None:
                    metric.append(dict(index_id=str(5010700+alist.index(nm)), value=str(ve)))
        #print(vs)
    except javax.management.RuntimeOperationsException as e:
        bt = str(e)
        exc_type, exc_value, exc_tb = sys.exc_info()
        for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
            bt += "\n%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname)
        print(bt)
        print(exc_type)
        print(exc_value)

if __name__ == '__main__':
    dbInfo = eval(sys.argv[1])
    pg, target_id = JavaUtil.get_pg_env(dbInfo, 0)
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
        mbs = jmx.queryNames('Hadoop:service=NameNode,name=*',None)
    else:
        mbs = jmx.queryNames(javax.management.ObjectName('Hadoop:service=NameNode,name=*'),None)
    if mbs:
        typ = 0
    else:
        if isinstance(jmx, HttpJmx):
            mbs = jmx.queryNames('Hadoop:service=DataNode,name=*',None)
        else:
            mbs = jmx.queryNames(javax.management.ObjectName('Hadoop:service=DataNode,name=*'),None)
        if mbs:
            typ = 1
    if typ == -1:
        print("msg=对象类型非NameNode或DataNode")
        sys.exit(1)
    metric = []
    metric.append(dict(index_id="1000102", value=str(int((ct2-ct)*1000))))
    metric.append(dict(index_id="5010000", value="连接成功"))
    if typ == 0:
        if isinstance(jmx, HttpJmx):
            idx_jvm2(jmx, metric)
        else:
            idx_jvm(jmx, metric)
        idx_nnload(jmx, metric)
        idx_nnst(jmx, metric)
        idx_nninfo(jmx, metric)
        idx_fsns(jmx, metric)
        f1 = False
        for m in mbs:
            #print(m)
            if not f1 and str(m).find('RpcActivityForPort') >= 0:
                idx_rpc(jmx, m, metric)
                f1 = True
            elif str(m).find('UgiMetrics') >= 0:
                idx_ugi(jmx, m, metric)
    else:
        if isinstance(jmx, HttpJmx):
            idx_jvm2(jmx, metric)
        else:
            idx_jvm(jmx, metric)
        idx_dninfo(jmx, metric)
        idx_fsds(jmx, metric)
        f1 = False
        f2 = False
        f3 = False
        for m in mbs:
            #print(m)
            if not f1 and str(m).find('RpcActivityForPort') >= 0:
                idx_rpc(jmx, m, metric)
                f1 = True
            elif not f2 and str(m).find('DataNodeActivity') >= 0:
                idx_dnload(jmx, m, metric)
                f2 = True
            elif str(m).find('UgiMetrics') >= 0:
                idx_ugi(jmx, m, metric)
            #elif not f3 and str(m).find('DataNodeVolume') >= 0:
            #    idx_vol(jmx, m, metric)
    if jmxsoc:
        jmxsoc.close();
    ct3 = time.time()
    metric.append(dict(index_id="1000101", value=str(int((ct3-ct2)*1000))))
    print('{"results":' + json.dumps(metric) + '}')

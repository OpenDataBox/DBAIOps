import json
import sys
import time
import jpype
from jpype import java, javax

sys.path.append('/usr/software/knowl')

import DBUtil
import JavaRsa

metric = []

OLD_GC = [
    'MarkSweepCompact',
    'PS MarkSweep',
    'ConcurrentMarkSweep',
    'Garbage collection optimized for short pausetimes Old Collector',
    'Garbage collection optimized for throughput Old Collector',
    'Garbage collection optimized for deterministic pausetimes Old Collector'
]


Requests = ['LeaderAndIsr',
'OffsetCommit',
'WriteTxnMarkers',
'DescribeProducers',
'Heartbeat',
'SaslHandshake',
'DescribeConfigs',
'OffsetFetch',
'DeleteGroups',
'ListGroups',
'AlterIsr',
'IncrementalAlterConfigs',
'DescribeClientQuotas',
'AlterClientQuotas',
'SyncGroup',
'FetchFollower',
'TxnOffsetCommit',
'DescribeLogDirs',
'JoinGroup',
'DescribeDelegationToken',
'ControlledShutdown',
'Produce',
'CreateTopics',
'AlterPartitionReassignments',
'RenewDelegationToken',
'Fetch',
'CreateDelegationToken',
'ListPartitionReassignments',
'DescribeUserScramCredentials',
'OffsetDelete',
'AlterReplicaLogDirs',
'DescribeGroups',
'LeaveGroup',
'EndTxn',
'AlterUserScramCredentials',
'DeleteAcls',
'FetchConsumer',
'UpdateFeatures',
'AddPartitionsToTxn',
'CreatePartitions',
'ElectLeaders',
'AlterConfigs',
'SaslAuthenticate',
'FindCoordinator',
'DescribeCluster',
'CreateAcls',
'DeleteTopics',
'DescribeAcls',
'Metadata',
'InitProducerId',
'ApiVersions',
'StopReplica',
'ListOffsets',
'AddOffsetsToTxn',
'OffsetForLeaderEpoch',
'DeleteRecords',
'ExpireDelegationToken',
'UpdateMetadata'
]


def initjvm():
    # print(getDefaultJVMPath())
    if not jpype.isJVMStarted():
        jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", convertStrings=False)


def metric_append(index_id, value):
    if isinstance(value, list):
        metric.append(dict(index_id=index_id, value=value))
    else:
        metric.append(dict(index_id=index_id, value=str(value)))


def jmx_common_value(index_id, object_name):
    object_value = jmx_get_attribute(jmx, object_name, "Value")
    if object_value is not None:
        metric_append(index_id, object_value.longValue())


def jmx_server_value(index_id, type, attr_name):
    object_name = f"kafka.server:type={type},name={attr_name}"
    object_value = jmx_get_attribute(jmx, object_name, "Value")
    if object_value is not None:
        metric_append(index_id, object_value.longValue())


def jmx_controller_value(index_id, attr_name):
    object_name = f"kafka.controller:type=KafkaController,name={attr_name}"
    object_value = jmx_get_attribute(jmx, object_name, "Value")
    if object_value is not None:
        metric_append(index_id, object_value.longValue())


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


def idx_jvm(jmx):
    mbs = jmx.queryNames(javax.management.ObjectName('java.lang:type=GarbageCollector,name=*'), None)
    gcs = [item for item in mbs]
    mbs = jmx.queryNames(javax.management.ObjectName('java.lang:type=MemoryPool,name=*'), None)
    pools = [item for item in mbs]
    threading_object = "java.lang:type=Threading"
    arr = jmx_get_attribute(jmx, threading_object, ['ThreadCount', 'DaemonThreadCount'])
    if len(arr) > 1:
        thread_count = arr[0].getValue().intValue()
        daemon_thread_count = arr[1].getValue().intValue()
        metric_append(1000617, thread_count)  # 活跃线程数量
        metric_append(1000618, daemon_thread_count)  # 活跃守护线程数量
        metric_append(1000619, thread_count - daemon_thread_count)  # 活跃普通线程数量
    arr = jmx_get_attribute(jmx, "java.lang:type=Memory", ['HeapMemoryUsage', 'NonHeapMemoryUsage'])
    if arr:
        mem = arr[0].getValue()
        committed_mem = mem.get('committed').longValue()
        used_mem = mem.get('used').longValue()
        max_mem = mem.get('max').longValue()
        metric_append(1000620, committed_mem - used_mem)  # 空闲堆内存
        metric_append(1000621, committed_mem)  # 已分配堆内存
        metric_append(1000622, used_mem)  # 已使用堆内存
        metric_append(1000623, round(used_mem * 100 / committed_mem, 2))  # 堆内存使用率
        metric_append(1000633, max_mem)  # 最大堆内存
    load_class_count = jmx_get_attribute(jmx, "java.lang:type=ClassLoading", "LoadedClassCount")
    metric_append(1000604, load_class_count.intValue())
    total_compiliation_time = jmx_get_attribute(jmx, "java.lang:type=Compilation", "TotalCompilationTime")
    metric_append(1000605, total_compiliation_time.longValue())
    n1 = n2 = t1 = t2 = t3 = 0
    for gc in gcs:
        nm = gc.getCanonicalName()
        arr = jmx_get_attribute(jmx, nm, ['Name', 'CollectionCount', 'CollectionTime', 'LastGcInfo'])
        if arr:
            if str(arr[0].getValue()) in OLD_GC:
                n2 += arr[1].getValue().longValue()
                t2 += arr[2].getValue().longValue()
            n1 += arr[1].getValue().longValue()
            t1 += arr[2].getValue().longValue()
            if str(arr[0].getValue()) == "G1 Young Generation":
                t3 += arr[3].getValue().get("duration").longValue()
    if gcs:
        metric_append(1000606, n1)  # 垃圾收集调用次数
        metric_append(1000607, t1)  # 垃圾收集调用时间(ms)
        metric_append(1000608, n2)  # 老生代垃圾收集调用次数
        metric_append(1000609, t2)  # 老生代垃圾收集调用时间(ms)
        metric_append(1000636, t3)  # 最后一次GC花费的时间，单位ms
    for mp in pools:
        nm = mp.getCanonicalName()
        arr = jmx_get_attribute(jmx, nm, ['Name', 'Usage'])
        if str(arr[0].getValue()) == 'Metaspace':
            n1 = arr[1].getValue().get('committed').longValue()
            n2 = arr[1].getValue().get('used').longValue()
            metric_append(1000630, n1)  # 已分配元数据空间
            metric_append(1000631, n2)  # 已使用元数据空间
            metric_append(1000632, round(n2 * 100 / n1, 2))  # 元数据空间使用率
            break
    arr = jmx_get_attribute(jmx, "java.lang:type=OperatingSystem",
                            ["OpenFileDescriptorCount", "MaxFileDescriptorCount"])
    if arr:
        metric_append(1000634, arr[0].getValue().longValue())
        metric_append(1000635, arr[1].getValue().longValue())
    arr = jmx_get_attribute(jmx, "java.lang:type=Runtime", ["Uptime","Name"])
    metric_append(4159999, round(arr[0].getValue().longValue() / 1000))  # Uptime
    metric_append(1000600, round(arr[0].getValue().longValue() / 1000))  # Uptime
    pid = arr[1].getValue().split('@')[0]
    metric_append(1000639, pid)
    mbs = jmx.queryNames(javax.management.ObjectName('java.nio:type=BufferPool,name=*'), None)
    for m in mbs:
        nm = m.getCanonicalName()
        arr = jmx_get_attribute(jmx, nm, ['Count', 'TotalCapacity', 'MemoryUsed'])
        if arr:
            n1 = arr[0].getValue().longValue()
            n2 = arr[1].getValue().longValue()
            n3 = arr[2].getValue().longValue()
            if str(nm).find("name=mapped") >= 0:
                metric_append(1000640, n1)
                metric_append(1000641, n2)
                metric_append(1000642, n3)
                if n2 > 0:
                    metric_append(1000643, round(n3 * 100 / n2, 2))
                else:
                    metric_append(1000643, 0)
            elif str(nm).find("name=direct") >= 0:
                metric_append(1000644, n1)
                metric_append(1000645, n2)
                metric_append(1000646, n3)
                if n2 > 0:
                    metric_append(1000647, round(n3 * 100 / n2, 2))
                else:
                    metric_append(1000647, 0)


def idx_process_oom_score(helper):
    runtime_object = f"java.lang:type=Runtime"
    attr_name = ['Name']
    attr = jmx_get_attribute(jmx, runtime_object, attr_name)
    process_id = attr[0].getValue().split('@')[0]
    cmd = f"cat /proc/{process_id}/oom_score"
    oom_score = helper.exec_cmd(cmd).strip()
    metric_append(1000638, oom_score)


def jmx_ct_value(object_name, index_id1, index_id2=None):
    arr = jmx_get_attribute(jmx, object_name, ["Count", "Mean"])
    cnt = None
    tim = None
    for item in arr:
        name = str(item.getName())
        if name == "Count":
            cnt = item.getValue().longValue()
        else:
            tim = item.getValue().doubleValue()
    if cnt is not None:
        metric_append(index_id1, cnt)
        if index_id2 and tim is not None:
            tim = round(tim*cnt,3)
            metric_append(index_id2, tim)


def jmx_rate_value(object_name, index_id1, index_id2):
    arr = jmx_get_attribute(jmx, object_name,
                            ["Count", "MeanRate", "OneMinuteRate", "FiveMinuteRate", "FifteenMinuteRate"])
    metric_append(index_id2,
                  [dict(name=str(item.getName()), value=round(item.getValue().doubleValue(), 2)) for item in arr])
    for item in arr:
        name = str(item.getName())
        value = round(item.getValue().doubleValue(), 2)
        if name == "OneMinuteRate":
            metric_append(index_id1, value)


def jmx_time_value(object_name, index_id1, index_id2):
    arr = jmx_get_attribute(jmx, object_name,
                            ["Max", "Count", "Min", "Max", "StdDev", "50thPercentile", "75thPercentile",
                             "95thPercentile", "98thPercentile", "99thPercentile", "999thPercentile"])
    metric_append(index_id2,
                  [dict(name=str(item.getName()), value=round(item.getValue().doubleValue(), 2)) for item in arr])
    for item in arr:
        name = str(item.getName())
        value = round(item.getValue().doubleValue(), 2)
        if name == "999thPercentile":
            metric_append(index_id1, value)


def idx_server():
    jmx_server_value(4150001, "ReplicaManager", "UnderReplicatedPartitions")  # 非同步分区数量
    jmx_server_value(4150002, "ReplicaManager", "AtMinIsrPartitionCount")
    jmx_server_value(4150003, "ReplicaManager", "LeaderCount")  # 首领数量
    jmx_server_value(4150004, "ReplicaManager", "OfflineReplicaCount")
    jmx_server_value(4150005, "ReplicaManager", "PartitionCount")  # 分区数量
    jmx_server_value(4150006, "ReplicaManager", "ReassigningPartitions")
    jmx_server_value(4150007, "ReplicaManager", "UnderMinIsrPartitionCount")
    object_name = "kafka.server:type=KafkaRequestHandlerPool,name=RequestHandlerAvgIdlePercent"  # 请求处理器空闲率
    object_value = jmx_get_attribute(jmx, object_name, "OneMinuteRate")
    if object_value is not None:
        metric_append(4150008, round(object_value.doubleValue()*100, 2))
    object_name = "kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec"  # 主题流入字节
    jmx_ct_value(object_name, 4151009)
    object_name = "kafka.server:type=BrokerTopicMetrics,name=BytesOutPerSec"  # 主题流出字节
    jmx_ct_value(object_name, 4151010)
    object_name = "kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec"  # 主题流入的消息
    jmx_ct_value(object_name, 4151011)
    object_name = "kafka.server:type=BrokerTopicMetrics,name=BytesRejectedPerSec"
    jmx_ct_value(object_name, 4151012)
    object_name = "kafka.server:type=BrokerTopicMetrics,name=FailedFetchRequestsPerSec"
    jmx_ct_value(object_name, 4151013)
    object_name = "kafka.server:type=BrokerTopicMetrics,name=FailedProduceRequestsPerSec"
    jmx_ct_value(object_name, 4151014)
    object_name = "kafka.server:type=BrokerTopicMetrics,name=FetchMessageConversionsPerSec"
    jmx_ct_value(object_name, 4151015)
    object_name = "kafka.server:type=BrokerTopicMetrics,name=InvalidMagicNumberRecordsPerSec"
    jmx_ct_value(object_name, 4151016)
    object_name = "kafka.server:type=BrokerTopicMetrics,name=InvalidMessageCrcRecordsPerSec"
    jmx_ct_value(object_name, 4151017)
    object_name = "kafka.server:type=BrokerTopicMetrics,name=InvalidOffsetOrSequenceRecordsPerSec"
    jmx_ct_value(object_name, 4151018)
    object_name = "kafka.server:name=NoKeyCompactedTopicRecordsPerSec,type=BrokerTopicMetrics"
    jmx_ct_value(object_name, 4151019)
    object_name = "kafka.server:name=ProduceMessageConversionsPerSec,type=BrokerTopicMetrics"
    jmx_ct_value(object_name, 4151020)
    object_name = "kafka.server:name=ReassignmentBytesOutPerSec,type=BrokerTopicMetrics"
    jmx_ct_value(object_name, 4151021)
    object_name = "kafka.server:name=ReassignmentBytesInPerSec,type=BrokerTopicMetrics"
    jmx_ct_value(object_name, 4151022)
    object_name = "kafka.server:name=ReplicationBytesInPerSec,type=BrokerTopicMetrics"
    jmx_ct_value(object_name, 4151023)
    object_name = "kafka.server:name=ReplicationBytesOutPerSec,type=BrokerTopicMetrics"
    jmx_ct_value(object_name, 4151024)
    object_name = "kafka.server:name=TotalProduceRequestsPerSec,type=BrokerTopicMetrics"
    jmx_ct_value(object_name, 4151025)
    object_name = "kafka.server:name=TotalFetchRequestsPerSec,type=BrokerTopicMetrics"
    jmx_ct_value(object_name, 4151026)
    object_name = "kafka.server:type=ReplicaManager,name=IsrExpandsPerSec"
    jmx_ct_value(object_name, 4151027)
    object_name = "kafka.server:type=ReplicaManager,name=FailedIsrUpdatesPerSec"
    jmx_ct_value(object_name, 4151028)
    object_name = "kafka.server:type=ReplicaManager,name=IsrShrinksPerSec"
    jmx_ct_value(object_name, 4151029)
    object_name = "kafka.network:type=SocketServer,name=NetworkProcessorAvgIdlePercent"
    object_value = jmx_get_attribute(jmx, object_name, "Value")
    if object_value is not None:
        metric_append(4150030, round(object_value.doubleValue()*100, 2))


def idx_zookeeper():
    object_name = "kafka.server:type=SessionExpireListener,name=ZooKeeperAuthFailuresPerSec"
    jmx_ct_value(object_name, 4141501)
    object_name = "kafka.server:type=SessionExpireListener,name=ZooKeeperDisconnectsPerSec"
    jmx_ct_value(object_name, 4141502)
    object_name = "kafka.server:type=SessionExpireListener,name=ZooKeeperExpiresPerSec"
    jmx_ct_value(object_name, 4141503)
    object_name = "kafka.server:type=SessionExpireListener,name=ZooKeeperReadOnlyConnectsPerSec"
    jmx_ct_value(object_name, 4141504)
    object_name = "kafka.server:type=SessionExpireListener,name=ZooKeeperSaslAuthenticationsPerSec"
    jmx_ct_value(object_name, 4141505)
    object_name = "kafka.server:type=SessionExpireListener,name=ZooKeeperSyncConnectsPerSec"
    jmx_ct_value(object_name, 4141506)


def idx_controller():
    jmx_controller_value(4150051, "ActiveControllerCount")  # 活跃控制器数量
    jmx_controller_value(4150052, "ControllerState")
    jmx_controller_value(4150053, "GlobalPartitionCount")
    jmx_controller_value(4150054, "GlobalTopicCount")
    jmx_controller_value(4150055, "OfflinePartitionsCount")  # 离线分区数量
    jmx_controller_value(4150056, "PreferredReplicaImbalanceCount")
    jmx_controller_value(4150057, "ReplicasIneligibleToDeleteCount")
    jmx_controller_value(4150058, "ReplicasToDeleteCount")
    jmx_controller_value(4150059, "TopicsIneligibleToDeleteCount")
    jmx_controller_value(4150060, "TopicsToDeleteCount")
    object_name = "kafka.controller:type=ControllerStats,name=AutoLeaderBalanceRateAndTimeMs"
    jmx_ct_value(object_name, 4151301, 4151401)
    object_name = "kafka.controller:type=ControllerStats,name=ControlledShutdownRateAndTimeMs"
    jmx_ct_value(object_name, 4151302, 4151402)
    object_name = "kafka.controller:type=ControllerStats,name=ControllerChangeRateAndTimeMs"
    jmx_ct_value(object_name, 4151303, 4151403)
    object_name = "kafka.controller:type=ControllerStats,name=ControllerShutdownRateAndTimeMs"
    jmx_ct_value(object_name, 4151304, 4151404)
    object_name = "kafka.controller:type=ControllerStats,name=IsrChangeRateAndTimeMs"
    jmx_ct_value(object_name, 4151305, 4151405)
    object_name = "kafka.controller:type=ControllerStats,name=LeaderAndIsrResponseReceivedRateAndTimeMs"
    jmx_ct_value(object_name, 4151306, 4151406)
    object_name = "kafka.controller:type=ControllerStats,name=LeaderElectionRateAndTimeMs"
    jmx_ct_value(object_name, 4151307, 4151407)
    object_name = "kafka.controller:type=ControllerStats,name=ListPartitionReassignmentRateAndTimeMs"
    jmx_ct_value(object_name, 4151308, 4151408)
    object_name = "kafka.controller:type=ControllerStats,name=LogDirChangeRateAndTimeMs"
    jmx_ct_value(object_name, 4151309, 4151409)
    object_name = "kafka.controller:type=ControllerStats,name=ManualLeaderBalanceRateAndTimeMs"
    jmx_ct_value(object_name, 4151310, 4151410)
    object_name = "kafka.controller:type=ControllerStats,name=PartitionReassignmentRateAndTimeMs"
    jmx_ct_value(object_name, 4151311, 4151411)
    object_name = "kafka.controller:type=ControllerStats,name=TopicChangeRateAndTimeMs"
    jmx_ct_value(object_name, 4151312, 4151412)
    object_name = "kafka.controller:type=ControllerStats,name=TopicDeletionRateAndTimeMs"
    jmx_ct_value(object_name, 4151313, 4151413)
    object_name = "kafka.controller:type=ControllerStats,name=TopicUncleanLeaderElectionEnableRateAndTimeMs"
    jmx_ct_value(object_name, 4151314, 4151414)
    object_name = "kafka.controller:type=ControllerStats,name=UncleanLeaderElectionEnableRateAndTimeMs"
    jmx_ct_value(object_name, 4151315, 4151415)
    object_name = "kafka.controller:type=ControllerStats,name=UncleanLeaderElectionsPerSec"
    jmx_ct_value(object_name, 4151316)
    object_name = "kafka.log:type=LogFlushStats,name=LogFlushRateAndTimeMs"
    jmx_ct_value(object_name, 4151317, 4151417)


def idx_request():
    mbs = jmx.queryNames(javax.management.ObjectName('kafka.network:type=RequestMetrics,name=TotalTimeMs,request=*'),None)
    for m in mbs:
        nm = m.getCanonicalName()
        ks = str(nm).split(',')
        r = None
        for k in ks:
            if k.find('request=') == 0:
                r = k[8:]
                break
        if r:
            try:
                i = Requests.index(r)
            except:
                i = -1
            if i >= 0:
                arr = jmx_get_attribute(jmx, nm, ["Count", "Mean"])
                cnt = None
                tim = None
                for item in arr:
                    name = str(item.getName())
                    if name == "Count":
                        cnt = item.getValue().longValue()
                    else:
                        tim = item.getValue().doubleValue()
                if cnt is not None:
                    metric_append(4151101 + i, cnt)
                    if tim is not None:
                        tim = round(tim*cnt,3)
                        metric_append(4151201 + i, tim)
    object_name = "kafka.network:type=RequestMetrics,name=RequestQueueTimeMs,request=Produce"
    jmx_ct_value(object_name, 4151181, 4151281)
    object_name = "kafka.network:type=RequestMetrics,name=RequestQueueTimeMs,request=FetchFollower"
    jmx_ct_value(object_name, 4151182, 4151282)
    object_name = "kafka.network:type=RequestMetrics,name=RequestQueueTimeMs,request=FetchConsumer"
    jmx_ct_value(object_name, 4151183, 4151283)


if __name__ == '__main__':
    dbInfo = eval(sys.argv[1])
    if dbInfo['target_ip'] == '0.0.0.0':
        target_id, pg = DBUtil.get_pg_env(dbInfo, 0)
        import health_kafka_cluster
        health_kafka_cluster.do_kafka(pg, dbInfo, target_id, metric)
        JMX = None
    else:
        JavaRsa.initjvm()
        ct = time.time()
        kafka, JMX = DBUtil.get_kafka_env(dbInfo)
    # jmx验证判断
    if JMX and JMX.connect:
        jmx = JMX.jmxsoc.getMBeanServerConnection()
        ct2 = time.time()
        metric_append(1000102, int((ct2-ct)*1000))
        metric_append(4150000, "连接成功")
        idx_jvm(jmx)
        idx_server()
        idx_controller()
        idx_request()
        idx_zookeeper()
        #_, _, helper = DBUtil.get_ssh_session()
        #idx_process_oom_score(helper)
        JMX.jmxsoc.close()
        ct3 = time.time()
        metric_append(1000101, int((ct3-ct2)*1000))
    print('{"results":' + json.dumps(metric, ensure_ascii=False) + '}')

#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@文件    :metric_flink.py
@说明    :Flink 运行指标采集
@时间    :2022/04/06 15:12:01
@作者    :xxxx
@版本    :2.0.1
'''

import sys
import json
sys.path.append('/usr/software/knowl')
import DBUtil


def metric_main(flink_clt,metric):
    """采集入口

    Args:
        clt (_type_): Flink API
    """

    # 获取作业管理器运行信息
    jobmanager_metrics = {'Status.JVM.GarbageCollector.PS_MarkSweep.Time':5000056
    ,'Status.JVM.Memory.Mapped.TotalCapacity':5000057
    ,'taskSlotsAvailable':5000058
    ,'taskSlotsTotal':5000059
    ,'Status.JVM.Memory.Mapped.MemoryUsed':5000060
    ,'Status.JVM.CPU.Time':5000061
    ,'Status.JVM.Threads.Count':5000062
    ,'Status.JVM.Memory.Heap.Committed':5000063
    ,'Status.JVM.Memory.Metaspace.Committed':5000064
    ,'Status.JVM.GarbageCollector.PS_MarkSweep.Count':5000065
    ,'Status.JVM.GarbageCollector.PS_Scavenge.Time':5000066
    ,'Status.JVM.Memory.Direct.Count':5000067
    ,'Status.JVM.GarbageCollector.PS_Scavenge.Count':5000068
    ,'Status.JVM.Memory.NonHeap.Max':5000069
    ,'numRegisteredTaskManagers':5000070
    ,'Status.JVM.Memory.NonHeap.Committed':5000071
    ,'Status.JVM.Memory.NonHeap.Used':5000072
    ,'Status.JVM.Memory.Metaspace.Max':5000073
    ,'Status.JVM.Memory.Direct.MemoryUsed':5000074
    ,'Status.JVM.Memory.Direct.TotalCapacity':5000075
    ,'numRunningJobs':5000076
    ,'Status.JVM.ClassLoader.ClassesLoaded':5000077
    ,'Status.JVM.Memory.Mapped.Count':5000078
    ,'Status.JVM.Memory.Metaspace.Used':5000079
    ,'Status.JVM.CPU.Load':5000080
    ,'Status.JVM.Memory.Heap.Used':5000081
    ,'Status.JVM.Memory.Heap.Max':5000082
    ,'Status.JVM.ClassLoader.ClassesUnloaded':5000083}

    response, out = flink_clt.getJobManagerMetric()
    if response.status == 200:
        msgs = ''
        for row in out:
            msgs = msgs + row['id'] + ','
        msgs = msgs[:-1]
        response, out = flink_clt.getJobManagerMetricValue(msgs)
        if response.status == 200:
            for row in out:
                metric_name = row['id']
                metric_value = row['value']
                if metric_name in jobmanager_metrics.keys():
                    metric.append(dict(index_id=jobmanager_metrics[metric_name], value=metric_value))

    # 获取作业运行信息
    job_metrics = {'numberOfFailedCheckpoints':5000042
    ,'lastCheckpointSize':5000043
    ,'totalNumberOfCheckpoints':5000044
    ,'lastCheckpointRestoreTimestamp':5000045
    ,'restartingTime':5000046
    ,'uptime':5000047
    ,'numberOfInProgressCheckpoints':5000048
    ,'downtime':5000049
    ,'numberOfCompletedCheckpoints':5000050
    ,'lastCheckpointProcessedData':5000051
    ,'numRestarts':5000052
    ,'fullRestarts':5000053
    ,'lastCheckpointDuration':5000054
    ,'lastCheckpointPersistedData':5000055}

    response, out = flink_clt.getJobMetric()
    if response.status == 200:
        msgs = ''
        for row in out:
            msgs = msgs + row['id'] + ','
        msgs = msgs[:-1]
        response, out = flink_clt.getJobMetricValue(msgs)
        if response.status == 200:
            for row in out:
                metric_name = row['id']
                metric_value = row['min']
                if metric_name in job_metrics.keys():
                    metric.append(dict(index_id=job_metrics[metric_name], value=metric_value))

    # 获取任务管理器运行信息
    response, out = flink_clt.getTaskManager()
    if response.status == 200:
        for row in out['taskmanagers']:
            task_name = row['id']
            slot_used_per = 100 - round(row['freeSlots'] * 100 /row['slotsNumber'],2)
            metric.append(dict(index_id='5000001', value=[dict(name=task_name, value=str(slot_used_per))]))
            cpu_cores_used = 100 - round(row['freeResource']['cpuCores'] * 100 /row['totalResource']['cpuCores'],2)
            metric.append(dict(index_id='5000002', value=[dict(name=task_name, value=str(cpu_cores_used))]))
            heapmem_used = 100 - round(row['freeResource']['taskHeapMemory'] * 100 /row['totalResource']['taskHeapMemory'],2)
            metric.append(dict(index_id='5000003', value=[dict(name=task_name, value=str(heapmem_used))]))
            if row['totalResource']['taskOffHeapMemory'] != 0:
                taskOffHeapMemory_used = 100 - round(row['freeResource']['taskOffHeapMemory'] * 100 /row['totalResource']['taskOffHeapMemory'],2)
            else:
                taskOffHeapMemory_used = 0
            metric.append(dict(index_id='5000004', value=[dict(name=task_name, value=str(taskOffHeapMemory_used))]))
            managedMemory_used = 100 - round(row['freeResource']['managedMemory'] * 100 /row['totalResource']['managedMemory'],2)
            metric.append(dict(index_id='5000005', value=[dict(name=task_name, value=str(managedMemory_used))]))
            networkMemory_used = 100 - round(row['freeResource']['networkMemory'] * 100 /row['totalResource']['networkMemory'],2)
            metric.append(dict(index_id='5000006', value=[dict(name=task_name, value=str(networkMemory_used))]))
            Memory_used = 100 - round(row['hardware']['freeMemory'] * 100 /row['hardware']['physicalMemory'],2)
            metric.append(dict(index_id='5000007', value=[dict(name=task_name, value=str(Memory_used))]))

    # 获取作业管理器运行信息
    taskmanager_metrics = {'Status.Network.AvailableMemorySegments':5000008
    ,'Status.JVM.Memory.Mapped.TotalCapacity':5000009
    ,'Status.Network.TotalMemorySegments':5000010
    ,'Status.JVM.Memory.Mapped.MemoryUsed':5000011
    ,'Status.Flink.Memory.Managed.Total':5000012
    ,'Status.JVM.CPU.Time':5000013
    ,'Status.JVM.GarbageCollector.G1_Young_Generation.Count':5000014
    ,'Status.JVM.Threads.Count':5000015
    ,'Status.Shuffle.Netty.UsedMemory':5000016
    ,'Status.JVM.Memory.Heap.Committed':5000017
    ,'Status.Shuffle.Netty.TotalMemory':5000018
    ,'Status.JVM.Memory.Metaspace.Committed':5000019
    ,'Status.JVM.Memory.Direct.Count':5000020
    ,'Status.Shuffle.Netty.AvailableMemorySegments':5000021
    ,'Status.JVM.Memory.NonHeap.Max':5000022
    ,'Status.Shuffle.Netty.TotalMemorySegments':5000023
    ,'Status.JVM.Memory.NonHeap.Committed':5000024
    ,'Status.JVM.Memory.NonHeap.Used':5000025
    ,'Status.JVM.Memory.Metaspace.Max':5000026
    ,'Status.JVM.GarbageCollector.G1_Old_Generation.Count':5000027
    ,'Status.JVM.Memory.Direct.MemoryUsed':5000028
    ,'Status.JVM.Memory.Direct.TotalCapacity':5000029
    ,'Status.JVM.GarbageCollector.G1_Old_Generation.Time':5000030
    ,'Status.Shuffle.Netty.UsedMemorySegments':5000031
    ,'Status.JVM.ClassLoader.ClassesLoaded':5000032
    ,'Status.JVM.Memory.Mapped.Count':5000033
    ,'Status.Flink.Memory.Managed.Used':5000034
    ,'Status.JVM.Memory.Metaspace.Used':5000035
    ,'Status.JVM.CPU.Load':5000036
    ,'Status.JVM.Memory.Heap.Used':5000037
    ,'Status.JVM.Memory.Heap.Max':5000038
    ,'Status.JVM.ClassLoader.ClassesUnloaded':5000039
    ,'Status.JVM.GarbageCollector.G1_Young_Generation.Time':5000040
    ,'Status.Shuffle.Netty.AvailableMemory':5000041}


    response, out = flink_clt.getTaskManagerMetric()
    if response.status == 200:
        msgs = ''
        for row in out:
            msgs = msgs + row['id'] + ','
        msgs = msgs[:-1]
        response, out = flink_clt.getTaskManagerMetricValue(msgs)
        Shuffle_mem_used = Shuffle_mem_total = 0
        if response.status == 200:
            for row in out:
                metric_name = row['id']
                metric_value = row['min']
                if metric_name in taskmanager_metrics.keys():
                    metric.append(dict(index_id=taskmanager_metrics[metric_name], value=metric_value))
                # 计算Shuffle.Netty.内存使用率
                if metric_name == 'Status.Shuffle.Netty.UsedMemory':
                    Shuffle_mem_used = metric_value
                if metric_name == 'Status.Shuffle.Netty.TotalMemory':
                    Shuffle_mem_total = metric_value
        Shuffle_mem_used_per = round(Shuffle_mem_used/Shuffle_mem_total,2)
        metric.append(dict(index_id=5000088, value=Shuffle_mem_used_per))

    # 获取其他信息
    response, out = flink_clt.getSystemOverview()
    if response.status == 200:
        slot_used_per = 100 - round(out['slots-available'] * 100 /out['slots-total'],2)
        metric.append(dict(index_id=5000084, value=slot_used_per))
        metric.append(dict(index_id=5000085, value=str(out['jobs-running'])))
        metric.append(dict(index_id=5000086, value=str(out['jobs-finished'])))
        metric.append(dict(index_id=5000087, value=str(out['jobs-cancelled'])))
        metric.append(dict(index_id=5000088, value=str(out['jobs-failed'])))

if __name__ == '__main__':
    objinfo = eval(sys.argv[1])
    metric = []
    flink_ctl = DBUtil.get_flink_client(objinfo)
    metric_main(flink_ctl,metric)
    if metric:
        metric.append(dict(index_id='5000000', value='连接成功'))
    else:
        metric.append(dict(index_id='5000000', value='连接失败'))
    print('{"results":' + json.dumps(metric) + '}')
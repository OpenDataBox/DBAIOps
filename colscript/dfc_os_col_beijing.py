"测试RDS连通性"
import sys
import json
from datetime import datetime, timedelta
from aliyunsdkcore import client
from aliyunsdkcore.profile import region_provider
from aliyunsdkrds.request.v20140815 import DescribeDBInstancesRequest, DescribeDBInstanceAttributeRequest,DescribeResourceUsageRequest,DescribeDBInstancePerformanceRequest


def GetDiskUsageRatio(DBInstanceId,metric):
    # 磁盘总空间使用量
    ResourceUsage = DescribeDBInstanceAttributeRequest.DescribeDBInstanceAttributeRequest()
    ResourceUsage.set_accept_format('json')
    ResourceUsage.set_DBInstanceId(DBInstanceId)
    ResourceUsageInfo = clt.do_action_with_exception(ResourceUsage)
    # print(ResourceUsageInfo)
    if (json.loads(ResourceUsageInfo))['Items']['DBInstanceAttribute']:
        DBInstanceStorage = (json.loads(ResourceUsageInfo))['Items']['DBInstanceAttribute'][0]['DBInstanceStorage']
    else:
        print('不存在该实例，请确认实例ID相关参数是否正常')
        sys.exit(1)
    DBInstanceStorage_Bytes = round(int(DBInstanceStorage) * 1024 * 1024 * 1024, 2)
    # print(str(DBInstanceStorage_Bytes))
    # 磁盘已使用量
    ResourceUsage = DescribeResourceUsageRequest.DescribeResourceUsageRequest()
    ResourceUsage.set_accept_format('json')
    ResourceUsage.set_DBInstanceId(DBInstanceId)
    ResourceUsageInfo = clt.do_action_with_exception(ResourceUsage)
    DiskUsed = (json.loads(ResourceUsageInfo))["DiskUsed"]  # 已使用大小，单位：字节
    # 磁盘占用百分比
    diskused_ratio = round(DiskUsed / DBInstanceStorage_Bytes * 100,2)
    metric.append(dict(index_id=3000005, value=str(diskused_ratio)))


def get_cpu_mem(DBInstanceId,StartTime,EndTime,metric):
    Performance = DescribeDBInstancePerformanceRequest.DescribeDBInstancePerformanceRequest()
    Performance.set_accept_format('json')
    Performance.set_DBInstanceId(DBInstanceId)
    Performance.set_Key("MySQL_MemCpuUsage") # 0:CPU使用率 1:内存使用率
    Performance.set_StartTime(StartTime)
    Performance.set_EndTime(EndTime)
    PerformanceInfo = clt.do_action_with_exception(Performance)
    # print(PerformanceInfo)
    Info = (json.loads(PerformanceInfo))
    Value = Info['PerformanceKeys']['PerformanceKey'][0]['Values']['PerformanceValue'][-1]['Value']
    cpu_used = str(Value).split('&')[0]
    mem_used = str(Value).split('&')[1]
    metric.append(dict(index_id=3000003, value=str(cpu_used)))
    metric.append(dict(index_id=3000004, value=str(mem_used)))


def get_network(DBInstanceId,StartTime,EndTime,metric):
    Performance = DescribeDBInstancePerformanceRequest.DescribeDBInstancePerformanceRequest()
    Performance.set_accept_format('json')
    Performance.set_DBInstanceId(DBInstanceId)
    Performance.set_Key("MySQL_NetworkTraffic") # 0:输入 1:输出
    Performance.set_StartTime(StartTime)
    Performance.set_EndTime(EndTime)
    PerformanceInfo = clt.do_action_with_exception(Performance)
    # print(PerformanceInfo)
    Info = (json.loads(PerformanceInfo))
    Value = Info['PerformanceKeys']['PerformanceKey'][0]['Values']['PerformanceValue'][-1]['Value']
    network_in = str(Value).split('&')[0]
    network_out = str(Value).split('&')[1]
    metric.append(dict(index_id=3000204, value=str(network_in)))
    metric.append(dict(index_id=3000206, value=str(network_out)))


if __name__ == '__main__':
    # 下面四个配置项需要替换成自己的
    global endpoint , regionid, as_client
    dbinfo = eval(sys.argv[1])
    uid = dbinfo["in_uid"]
    objtype = uid[:2]
    if objtype == '18':  # RDS
        accesskeyid = dbinfo["accessKeyId"]       # 访问KEY
        accesssecret = dbinfo["secret"]           # 访问密钥
        regionid = dbinfo["regionId"]             # 地域ID
        endpoint = dbinfo["endPoint"]             # RDS的endpoint
        dbinstanceid = dbinfo["dbInstanceId"]     # RDS实例ID

        EndTime =  (datetime.now() - timedelta(hours=8)).strftime("%Y-%m-%dT%H:%MZ")
        StartTime =  (datetime.now() - timedelta(hours=9)).strftime("%Y-%m-%dT%H:%MZ")

        region_provider.modify_point('rds', regionid, endpoint)
        clt = client.AcsClient(accesskeyid, accesssecret, regionid)
        metric = []
        try:
            metric.append(dict(index_id="3000000", value='连接成功'))
            rdsrequest = DescribeDBInstancesRequest.DescribeDBInstancesRequest()
            rdsrequest.set_accept_format('json')
            clt.do_action_with_exception(rdsrequest)
        except Exception as e:
            metric.append(dict(index_id="3000000", value='连接失败'))

        GetDiskUsageRatio(dbinstanceid, metric)
        get_cpu_mem(dbinstanceid,StartTime,EndTime,metric)
        get_network(dbinstanceid,StartTime,EndTime,metric)
        print('{"results":' + json.dumps(metric,ensure_ascii=False) + '}')

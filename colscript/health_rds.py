"测试RDS连通性"

import sys
import json
from datetime import datetime,timedelta
from aliyunsdkasapi.ASClient import ASClient
from aliyunsdkasapi.AsapiRequest import AsapiRequest
import warnings

warnings.filterwarnings("ignore")

def instance_totalsize(clt,DBInstanceId):
    # 获取实例存储空间
    req = AsapiRequest('Rds', "2014-08-15", "DescribeDBInstanceAttribute", endpoint)
    req.add_body_params("DBInstanceId", DBInstanceId)
    req.add_header("x-acs-regionid", regionid)
    req.add_header("x-acs-instanceid", DBInstanceId)
    # 设置请求方式
    req.set_method("POST")
    # 设置调用源,主要是标识调用来源,无实际作用,可随意设置,必填项
    clt.setSdkSource('DBAIOps-rds-sdk')
    response = clt.do_request(req)
    per_info = json.loads(response.decode('utf-8'))
    total_gb = per_info['Items']['DBInstanceAttribute'][0]['DBInstanceStorage']
    return total_gb


def GetDiskUsageRatio(as_client,DBInstanceId,metric):
    # 获取实例存储空间
    total_gb = instance_totalsize(as_client,DBInstanceId)
    
    req = AsapiRequest('Rds', "2014-08-15", "DescribeResourceUsage", endpoint)   # 空间使用信息，不包括总空间大小
    req.add_body_params("DBInstanceId", DBInstanceId)
    req.add_header("x-acs-regionid", regionid)
    req.add_header("x-acs-instanceid", DBInstanceId)
    # 设置请求方式
    req.set_method("POST")
    # 设置调用源,主要是标识调用来源,无实际作用,可随意设置,必填项
    as_client.setSdkSource('DBAIOps-rds-sdk')

    response = as_client.do_request(req)
    per_info = json.loads(response.decode('utf-8'))
    DiskUsed = per_info['DiskUsed']
    # 磁盘占用百分比
    DBInstanceStorage_Bytes = int(total_gb) * 1024 * 1024 * 1024
    diskused_ratio = round(DiskUsed / DBInstanceStorage_Bytes * 100,2)
    metric.append(dict(index_id="3000005", value=str(diskused_ratio)))


def get_cpu_mem(DBInstanceId,StartTime,EndTime,metric):
    Info = get_instance_performance(as_client,DBInstanceId,"MySQL_MemCpuUsage",StartTime,EndTime)
    Value = Info['PerformanceKeys']['PerformanceKey'][0]['Values']['PerformanceValue'][-1]['Value']
    cpu_used = str(Value).split('&')[0]
    mem_used = str(Value).split('&')[1]
    metric.append(dict(index_id="3000003", value=str(cpu_used)))
    metric.append(dict(index_id="3000004", value=str(mem_used)))


def get_network(DBInstanceId,StartTime,EndTime,metric):
    Info = get_instance_performance(as_client,DBInstanceId,"MySQL_NetworkTraffic",StartTime,EndTime)
    Value = Info['PerformanceKeys']['PerformanceKey'][0]['Values']['PerformanceValue'][-1]['Value']
    network_in = str(Value).split('&')[0]
    network_out = str(Value).split('&')[1]
    metric.append(dict(index_id="3000204", value=str(network_in)))
    metric.append(dict(index_id="3000206", value=str(network_out)))


def get_instance_performance(as_client,dbinstanceid,masterkey,starttime,endtime):
    """获取RDS实例的性能指标

    Args:
        DBInstanceId (_type_): RDS实例ID
        MasterKey (_type_): 指标分类KEY
        StartTime (_type_): 开始时间
        EndTime (_type_): 结束时间

    Returns:
        _type_: json
    """
    req = AsapiRequest('Rds', "2014-08-15", "DescribeDBInstancePerformance", endpoint)   # 性能信息
    req.add_body_params("DBInstanceId", dbinstanceid)
    req.add_body_params("Key", masterkey)
    req.add_body_params("StartTime", starttime)
    req.add_body_params("EndTime", endtime)
    req.add_header("x-acs-regionid", regionid)
    req.add_header("x-acs-instanceid", dbinstanceid)
    # 设置请求方式
    req.set_method("POST")
    # 设置调用源,主要是标识调用来源,无实际作用,可随意设置,必填项
    as_client.setSdkSource('DBAIOps-rds-sdk')
    try:
        response = as_client.do_request(req)
        per_info = json.loads(response.decode('utf-8'))
        return per_info
    except Exception as e:
        print('Error:',e)
        sys.exit(1)

def parseParam(params):
    if params[0] == '{':
        paramDict = eval(params)
    else:
        paramDict = {}
        paramsList = params.split(",")
        for item in paramsList:
            if item != "":
                if "=" in item:
                    index = item.find("=")
                    paramDict[item[:index]] = item[index + 1:].strip()
    return paramDict

def main():
    # 下面四个配置项需要替换成自己的
    global endpoint , regionid, as_client
    dbinfo = eval(sys.argv[1])
    uid = dbinfo["in_uid"]
    objtype = uid[:2]
    prop = dbInfo.get('otherConf','')
    if objtype == '18' or prop:  # RDS
        if objtype == '18':
            accesskeyid = dbinfo["accessKeyId"]    # 访问KEY
            accesssecret = dbinfo["secret"]  # 访问密钥
            regionid = dbinfo["regionId"]       # 地域ID
            endpoint = dbinfo["endPoint"]       # RDS的endpoint
            dbinstanceid = dbinfo["dbInstanceId"]   # RDS实例ID
        else:
            info = parseParam(prop)
            accesskeyid = info["accessKeyId"]    # 访问KEY
            accesssecret = info["secret"]  # 访问密钥
            regionid = info["regionId"]       # 地域ID
            endpoint = info["endPoint"]       # RDS的endpoint
            dbinstanceid = dbinfo["dbInstanceId"]   # RDS实例ID
        # 由于RDS使用的UTC时间，所以北京时间需要减去8小时
        EndTime =  (datetime.now() - timedelta(hours=8)).strftime("%Y-%m-%dT%H:%MZ")
        StartTime = (datetime.now() - timedelta(hours=9)).strftime("%Y-%m-%dT%H:%MZ")
        # accesssecret = decrypt(accesssecret)
        # 1. 创建Request, Product产品名称, Version接口版本, Action接口名称, asapi-endpoint ASAPI服务访问域名
        req = AsapiRequest('Rds',
                           "2014-08-15",
                           "DescribeDBInstancePerformance",
                           endpoint)
        # 2. 业务信息
        req.add_body_params("DBInstanceId", dbinstanceid)
        req.add_body_params("Key", accesskeyid)
        req.add_body_params("StartTime", StartTime)
        req.add_body_params("EndTime", EndTime)

        req.add_header("x-acs-regionid", regionid)
        req.add_header("x-acs-instanceid", dbinstanceid)
        # 4. 设置请求方式
        req.set_method("POST")
        # 5. 用环境信息初始化ASClient timeout设置请求超时时间，cert_file设置证书文件，verify是否验证证书
        as_client = ASClient(accesskeyid,
                             accesssecret,
                             regionid,
                             timeout=2000,
                             cert_file=None,
                             verify=False)
        # 6. 设置调用源,主要是标识调用来源,无实际作用,可随意设置,必填项
        as_client.setSdkSource("asapi-6164@sgepri.sgcc.com.cn")
        flag = 0
        metric = []
        try:
            response = as_client.do_request(req)
            isSucc = json.loads(response.decode('utf-8'))
            if not isSucc['asapiSuccess']:
                metric.append(dict(index_id="3000000", value='连接失败'))
            else:
                metric.append(dict(index_id="3000000", value='连接成功'))
        except Exception as Err:
            metric.append(dict(index_id="3000000", value='连接失败'))
        GetDiskUsageRatio(as_client,dbinstanceid, metric)
        get_cpu_mem(dbinstanceid,StartTime,EndTime,metric)
        get_network(dbinstanceid,StartTime,EndTime,metric)
        print('{"results":' + json.dumps(metric,ensure_ascii=False) + '}')

if __name__ == '__main__':
    main()

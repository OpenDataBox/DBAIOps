import json
import sys
import time
from datetime import datetime
import jpype
from kafka.admin import ConfigResource, ConfigResourceType
from jpype import *

sys.path.append('/usr/software/knowl')
import DBUtil
import JavaUtil


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


def vals_append(key, value):
    vals.append(dict(name=key, value=str(value)))


def table_append(tab_list, c1=None, c2=None, c3=None, c4=None, c5=None, c6=None, c7=None, c8=None, c9=None, c10=None):
    tab_list.append(dict(c1=c1, c2=c2, c3=c3, c4=c4, c5=c5, c6=c6, c7=c7, c8=c8, c9=c9, c10=c10))


def jmx_get_attribute(jmx, object_name, attribute=None):
    if isinstance(attribute, list) or not attribute:
        arr = jmx.getAttributes(javax.management.ObjectName(object_name), attribute)
    else:
        arr = jmx.getAttribute(javax.management.ObjectName(object_name), attribute)
    return arr


def utc2datetime(val):
    format = '%Y-%m-%d %H:%M:%S'
    d = datetime.fromtimestamp(val)
    return d.strftime(format)


def jmx_runtime_cib(jmx):
    runtime_object = f"java.lang:type=Runtime"
    attr_name = ['StartTime', 'VmName', 'VmVendor', 'VmVersion', 'Uptime', 'Name']
    attr = jmx_get_attribute(jmx, runtime_object, attr_name)
    StartTime = int(attr[0].getValue() / 1000)
    vals_append('StartTime', utc2datetime(StartTime))  # 启动时间
    VmName = attr[1].getValue()
    VmVendor = attr[2].getValue()
    VmVersion = attr[3].getValue()
    #vals_append('VmName', f"{VmName} 版本 {VmVersion}")  # 虚拟机
    vals_append('VmName', VmName)
    vals_append('VmVersion', VmVersion)
    vals_append('VmVendor', VmVendor)  # 供应商
    Uptime = attr[4].getValue()
    # run_time = datetime.fromtimestamp(time.time() - Uptime / 10000 - StartTime).strftime('%d天%H小时%M分钟')
    run_time = datetime.fromtimestamp(time.time() - Uptime / 1000 - StartTime).strftime('%d{x}%H{y}%M{z}').format(
        x='天', y='小时', z='分钟')
    vals_append('Uptime', run_time)  # 运行时间
    Name = attr[5].getValue()
    vals_append('SrvName', Name)  # 名称
    vals_append('PID', Name.split('@')[0])  # 进程ID
    vals_append('Hostname', Name.split('@')[1])  # 进程ID


def jmx_operating_system_cib(jmx):
    ops_object = f"java.lang:type=OperatingSystem"
    attr_name = ['AvailableProcessors', 'Version', 'Name']
    attr = jmx_get_attribute(jmx, ops_object, attr_name)
    cpu_count = attr[0].getValue()
    vals_append('cpu_count', cpu_count)
    kernel_version = attr[1].getValue()
    name = attr[2].getValue()
    vals_append('kernel_version', f'{name} {kernel_version}')


def jmx_connect_value(metric, jmxsoc, broker_id):
    """
    获取当前会话数，当前活跃会话数，I/O延迟
    :param jmxsoc:
    :param broker_id:
    """
    object_name = f"kafka.server:type=controller-channel-metrics,broker-id={broker_id}"
    attr_name = ["connection-creation-total", "connection-count", "io-time-ns-avg"]
    index_id = [4150030, 4150031, 4150032]
    object_value = jmx_get_attribute(jmxsoc.jmx, object_name, attr_name)
    for index, value in enumerate(object_value):
        metric.append(dict(index_id=index_id[index], value=value.getValue()))


def get_kafka_info(metric, kafka, jmxsoc):
    """
    获取kafka的连接对象
    :param mertic
    :param kafka
    """
    client = kafka.client
    cluster = client.describe_cluster()
    brokers = cluster["brokers"]
    cluster_id = cluster["cluster_id"]
    controller_id = cluster["controller_id"]
    brokers_list = []
    table_append(brokers_list, "节点ID", "IP地址", "端口")
    node_id = 0
    # brokers [{'node_id': 1, 'host': '60.60.60.118', 'port': 9092, 'rack': None}]
    for broker in brokers:
        table_append(brokers_list, broker['node_id'], broker["host"], broker['port'])
        # 获取当前broker中的会话信息
        #if jmxsoc and jmxsoc.connect:
        #    jmx_connect_value(metric, jmxsoc, broker_id=broker["node_id"])
        if dbInfo['target_ip'] == broker['host']:
            node_id = broker['node_id']
    vals_append("cluster_id", cluster_id)  # 集群ID
    vals_append("node_id", node_id)  # 节点ID
    vals_append("controller_id", controller_id)  # 控制器ID
    vals_append("brokers_count", len(brokers))  # brokers 数量
    config = client.describe_configs(config_resources=[ConfigResource(ConfigResourceType.BROKER, node_id)])
    parameters = config[0].resources
    data = {}
    params = []
    for item in parameters[0][4]:
        if item[1] and item[0]:
            data[item[0]] = item[1]
    try:
        vals_append("listeners", data["listeners"])  # 监听地址
    except KeyError:
        vals_append("listeners", f'{data["host.name"]}:{data["port"]}')  # 监听地址,过时参数
    vals_append("zookeeper", data.get("zookeeper.connect"))  # zookeeper列表
    vals_append("log.dirs", data.get("log.dirs"))  # 持久化消息的目录
    vals_append("advertised.listeners", data.get("advertised.listeners"))  # 对外公布的监听器
    vals_append("recovery_threads_num", data.get("num.recovery.threads.per.data.dir"))  # 每日志路径恢复线程数
    vals_append("auto_create_topics", data.get("auto.create.topics.enable"))  # 是否自动创建主题
    vals_append("delete.topic.enable", data.get("delete.topic.enable"))  # 是否允许删除topic
    vals_append("partitions_num", data.get("num.partitions"))  # 主题默认分区数
    vals_append("log_retention_hours", data.get("log.retention.hours"))  # 数据保留小时数
    vals_append("log_retention_bytes", data.get("log.retention.bytes"))  # 数据保留容量
    vals_append("log_segment_bytes", data.get("log.segment.bytes"))  # 日志片段大小
    vals_append("max_connection", data.get("max.connections"))  # 最大连接数
    vals_append("message_max_bytes", data.get("message.max.bytes"))  # 消息最大长度
    vals_append("unclean.leader.election.enable", data.get("unclean.leader.election.enable"))  # 是否允许unclean leader
    vals_append("auto.leader.rebalance.enable", data.get("auto.leader.rebalance.enable"))  # 是否允许定期进行Leader选举
    vals_append("num.network.threads", data.get("num.network.threads"))  # 网络线程数
    vals_append("num.io.threads", data.get("num.io.threads"))  # io线程数
    for key, value in data.items():
        params.append(dict(name=key, value=value))
    metric.append(dict(index_id=4160002, value=params))
    metric.append(dict(index_id=4160003, content=brokers_list))
    topics_list = []
    table_append(topics_list, "主题名称", "错误代码", "分区ID", "leader", "replicas", "isr", "offline_replicas")
    topics = client.describe_topics()
    for topic in topics:
        name = topic['topic']
        if name.find('__consumer_offsets') != 0:
            for item in topic["partitions"]:
                table_append(topics_list, name, item["error_code"], item["partition"], item['leader'], item["replicas"], item["isr"], item["offline_replicas"])
    metric.append(dict(index_id=4160004, content=topics_list))
    return cluster_id


def kafka_cluster(pg, target_id, cid):
    sql = "select subuid from mgt_system where uid='%s'" % target_id
    result = relate_pg2(pg, sql)
    if result.code == 0:
        if len(result.msg) == 1 and result.msg[0][0] == cid:
            return 0
    else:
        return -1
    cur = pg.conn.cursor()
    sql = "update mgt_system set subuid='%s' where uid='%s'" % (cid, target_id)
    cur.execute(sql)
    pg.conn.commit()


def jmx_remote(jmxsoc):
    # JMX基本信息采集
    if jmxsoc.connect:
        jmx_runtime_cib(jmxsoc.jmx)
        jmx_operating_system_cib(jmx_soc.jmx)
        jmxsoc.jmxsoc.close()


if __name__ == '__main__':
    dbInfo = eval(sys.argv[1])
    target_id, pg = DBUtil.get_pg_env(dbInfo, 0)
    if dbInfo['target_ip'] == '0.0.0.0':
        import cib_kafka_cluster
        cib_kafka_cluster.main(pg, target_id)
    else:
        metric = []
        vals = []
        JavaUtil.initjvm()
        kafka, jmx_soc = DBUtil.get_kafka_env(dbInfo)
        if kafka:
            cid = get_kafka_info(metric, kafka, jmx_soc)
            #raise IndexError(cid + ':' + target_id)
            if cid:
                kafka_cluster(pg, target_id, cid)
        if jmx_soc:
            jmx_remote(jmx_soc)
        metric.append(dict(index_id=4160001, value=vals))
        print('{"cib":' + json.dumps(metric) + '}')

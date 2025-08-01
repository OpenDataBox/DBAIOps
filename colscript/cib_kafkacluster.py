import json
import sys
import time
from datetime import datetime
import psycopg2
import jpype
from kafka.admin import ConfigResource, ConfigResourceType
from jpype import *

sys.path.append('/usr/software/knowl')
import DBUtil
import JavaUtil
import KafkaUtil

vals = []

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


def tuple2(arr):
    s = ''
    for v in arr:
        if s:
            s += ",'%s'" % str(v)
        else:
            s = "'%s'" % str(v)
    if s:
        s = '(%s)' % s
    return s


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


def get_kafka_info(pg, target_id, metric):
    #sql = "select cib_value from p_normal_cib where index_id=1000001 and cib_name='members' and target_id='%s'" % target_id
    sql = "select ip,port from mgt_system where uid='%s' and use_flag" % target_id
    result = relate_pg2(pg, sql)
    if result.code != 0 or len(result.msg) == 0 or not result.msg[0][0]:
        return
    #bs = set(result.msg[0][0].split(','))
    ip = result.msg[0][0]
    port = result.msg[0][1]
    #sql = "select uid,ip,port,username,password from mgt_system where uid in %s and use_flag" % (tuple2(bs))
    sql = "select uid,ip,port,username,password from mgt_system where ip='%s' and port=%s and uid like '2901%%' and use_flag" % (ip,port)
    result = relate_pg2(pg, sql)
    cs = set()
    hosts = ''
    usr = ''
    pwd = ''
    if result.code == 0:
        for row in result.msg:
            cs.add(row[0])
            if hosts:
                hosts += ',%s:%s' % (row[1],row[2])
            else:
                hosts = '%s:%s' % (row[1],row[2])
                usr = row[3]
                pwd = row[4]
                if usr and pwd:
                    pwd = JavaUtil.decrypt(pwd)
    bs = cs     ######
    if not cs or cs != bs:
        return
    """
    获取kafka的连接对象
    """
    kafka = KafkaUtil.Kafka(hosts,usr,pwd)
    client = kafka.client
    cluster = client.describe_cluster()
    brokers = cluster["brokers"]
    cluster_id = cluster["cluster_id"]
    controller_id = cluster["controller_id"]
    brokers_list = []
    table_append(brokers_list, "节点ID", "IP地址", "端口")
    for broker in brokers:
        table_append(brokers_list, broker['node_id'], broker["host"], broker['port'])
    metric.append(dict(index_id=4180003, content=brokers_list))
    vals_append("cluster_id", cluster_id)  # 集群ID
    vals_append("controller_id", controller_id)  # 控制器ID
    vals_append("brokers_count", len(brokers))  # brokers 数量
    config = client.describe_configs(config_resources=[ConfigResource(ConfigResourceType.BROKER, brokers[0]['node_id'])])
    parameters = config[0].resources
    for item in parameters[0][4]:
        if item[0] == 'zookeeper.connect':
            vals_append("zookeeper", item[1])  # zookeeper列表
            break
    topics_list = []
    table_append(topics_list, "主题名称", "错误代码", "分区ID", "leader", "replicas", "isr", "offline_replicas")
    topics = client.describe_topics()
    for topic in topics:
        name = topic['topic']
        if name.find('__consumer_offsets') == 0:
            continue
        for item in topic["partitions"]:
            table_append(topics_list, name, item["error_code"], item["partition"], item['leader'], item["replicas"], item["isr"], item["offline_replicas"])
    metric.append(dict(index_id=4180004, content=topics_list))
    sql = "select uid from mgt_system where subuid='%s' and uid<>'%s' and uid like '2903%%' and use_flag" % (cluster_id,target_id)
    result = relate_pg2(pg, sql)
    if result.code == 0 and len(result.msg) > 0:
        return
    #sql = "select target_id from p_oracle_cib where index_id=4160001 and cib_name='cluster_id' and cib_value='%s'" % (cluster_id)
    #result = relate_pg2(pg, sql)
    #if result.code == 0:
    #    for row in result.msg:
    #        if row[0] in cs:
    #            cs.remove(row[0])
    #        else:
    #            bs.add(row[0])
    #if cs:
    #    return
    bs.add(target_id)
    sql = "update mgt_system set subuid='%s' where uid in %s and (subuid is null or subuid<>'%s') and use_flag" % (cluster_id, tuple2(bs), cluster_id)
    cur = pg.conn.cursor()
    cur.execute(sql)
    pg.conn.commit()


def main(pg, target_id):
    metric = []
    get_kafka_info(pg, target_id, metric)
    metric.append(dict(index_id=4180001, value=vals))
    print('{"cib":' + json.dumps(metric) + '}')


if __name__ == '__main__':
    dbInfo = eval(sys.argv[1])
    target_id, pg = DBUtil.get_pg_env(dbInfo, 0)
    main(pg, target_id)

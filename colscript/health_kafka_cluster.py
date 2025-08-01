import sys
import time
import traceback

from kafka import (KafkaClient, KafkaConsumer)
from kafka.admin import ConfigResource, ConfigResourceType
from kafka.structs import TopicPartition

sys.path.append('/usr/software/knowl')

import DBUtil
import os_svc
import JavaUtil
import KafkaUtil
import zk

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
    except Exception as e:
        result.code = 1
        result.msg = str(e)
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

def cat_ret(ostype, lines, start, stop, par):
    vals = []
    cmd = None
    cnt = 0
    pid = None
    for i in range(start, stop):
      cnt += 1
      line, cmd = os_svc.getOsline(lines[i])
      if not line is None:
        n,b,e = os_svc.getNumber(line)
        if not n is None:
          pid = int(n)
      if not cmd is None:
        break
    return pid, cmd, start + cnt - 1

def do_kafka(pg, dbInfo, targetId, metric):
    sql = "select cib_name,cib_value from p_normal_cib where index_id=1000001 and cib_name in ('brokers','_brokers') and target_id='%s'" % targetId
    result = relate_pg2(pg, sql)
    if result.code != 0:
        return
    ov = None
    nv = None
    for row in result.msg:
        if row[0] == 'brokers':
            nv = row[1]
        else:
            ov = row[1]
    if nv:
        bs = set(nv.split(','))
    else:
        return
    if ov:
        os = set(ov.split(','))
        if os != bs:
            return
    #sql = "select uid,ip,port,username,password,subuid from mgt_system where uid in %s and use_flag" % (tuple2(bs))
    sql = "select uid,ip,port,username,password from mgt_system where subuid=(select subuid from mgt_system where uid='%s' and use_flag) and use_flag" % (targetId)
    result = relate_pg2(pg, sql)
    ks = {}
    ts = set()
    hosts = ''
    usr = ''
    pwd = ''
    if result.code == 0:
        for row in result.msg:
            if row[0] != targetId:
                if row[0] in bs:
                    ts.add(row[0])
                if not ks:
                    usr = row[3]
                    pwd = row[4]
                    if usr and pwd:
                        pwd = JavaUtil.decrypt(pwd)
                ks[row[0]] = '%s:%s' % (row[1],row[2])
    if ts != bs:
        return
    """
    获取kafka的连接对象
    """
    ct = int(time.time())
    mets = {}
    cnt = 0
    fail = 0
    t = 0
    for uid in ks.keys():
        sql = '''select index_id,value,record_time from mon_indexdata where uid='%s' and index_id in (
4150000,
4159999,
4159998,
4150009,
4150010,
4150011,
4150012,
4150013,
4150014,
4150116,
4150122,
4150137,
4150216,
4150222,
4150237,
4150307
)''' % uid
        result = relate_pg2(pg, sql)
        met = {}
        if result.code == 0:
            for row in result.msg:
                #ts = time.mktime(row[2].timetuple())
                if row[0] != 4150000:
                    met[row[0]] = [row[0],float(row[1]),row[2]]
                else:
                    met[row[0]] = [row[0],row[1],row[2]]
        if met.get(4150000) is None or time.mktime(met[4150000][2].timetuple()) < ct - 600:
            continue
        if met[4150000][1] != '连接成功':
            fail += 1
            continue
        if t == 0:
            hosts = ks[uid]
        elif t < 3:
            hosts += ',' + ks[uid]
        t += 1
        if met.get(4159999) and met.get(4159998):
            if time.mktime(met[4159999][2].timetuple()) > ct - 600 and time.mktime(met[4159998][2].timetuple()) > ct - 600:
                cnt += 1
                for m in met.values():
                    if m[0] > 4150000 and m[0] < 4159998 and time.mktime(m[2].timetuple()) > ct - 600:
                        v = None
                        if m[0] == 4150222:
                            if met.get(4150122):
                                v = m[1] * met[4150122][1]
                            if mets.get(4150222+9000) is not None:
                                mets[4150222+9000] += met[4150122][1]
                            else:
                                mets[4150222+9000] = met[4150122][1]
                        elif m[0] == 4150237:
                            if met.get(4150137):
                                v = m[1] * met[4150137][1]
                            if mets.get(4150237+9000) is not None:
                                mets[4150237+9000] += met[4150137][1]
                            else:
                                mets[4150237+9000] = met[4150137][1]
                        elif m[0] == 4150216:
                            if met.get(4150116):
                                v = m[1] * met[4150116][1]
                            if mets.get(4150216+9000) is not None:
                                mets[4150216+9000] += met[4150116][1]
                            else:
                                mets[4150216+9000] = met[4150116][1]
                        else:
                            v = m[1]
                        if v is not None:
                            if mets.get(m[0]) is not None:
                                mets[m[0]] += v
                            else:
                                mets[m[0]] = v
    if cnt > 0:
        for k in mets.keys():
            if k < 4159000:
                if k in [4150222,4150237,4150216]:
                    if mets[k+9000] > 0:
                        v = round(mets[k]/mets[k+9000],2)
                    else:
                        v = 0
                else:
                    v = mets[k]
                metric.append(dict(index_id=str(k+20000), value=str(v)))
    metric.append(dict(index_id='4170000', value='连接成功'))
    metric.append(dict(index_id='4179999', value=str(ct)))
    metric.append(dict(index_id='4179996', value=str(cnt)))
    metric.append(dict(index_id='4179997', value=str(fail)))
    if t > 0:
        kafka = KafkaUtil.Kafka(hosts,usr,pwd)
        client = kafka.client
        cluster = client.describe_cluster()
        brokers = cluster["brokers"]
        controller_id = cluster["controller_id"]
        node_id = controller_id
        t = 0
        tt = 0
        bs = {}
        for broker in brokers:
            if controller_id == broker['node_id']:
                tt += 1
            if node_id < 0:
                node_id = broker['node_id']
            t += 1
            bs[broker['node_id']] = [0,0,0,0]
        metric.append(dict(index_id='4170050', value=str(t)))
        metric.append(dict(index_id='4170051', value=str(tt)))
        metric.append(dict(index_id='4170052', value=str(controller_id)))
        topics = client.describe_topics()
        t1 = 0
        t2 = 0
        t3 = 0
        t4 = 0
        t5 = 0
        t6 = 0
        for topic in topics:
            #name = topic['topic']
            t1 += 1
            for item in topic["partitions"]:
                #table_append(topics_list, name, item["error_code"], item["partition"], item['leader'], item["replicas"], item["isr"], item["offline_replicas"])
                if item['leader'] is not None and item['leader'] >= 0:
                    bs[item['leader']][0] += 1
                    t3 += 1
                for id in item["replicas"]:
                    bs[id][1] += 1
                    t4 += 1
                for id in item["isr"]:
                    bs[id][2] += 1
                    t5 += 1
                for id in item["offline_replicas"]:
                    bs[id][3] += 1
                    t6 += 1
                t2 += 1
        metric.append(dict(index_id='4170054', value=str(t1)))
        metric.append(dict(index_id='4170053', value=str(t2)))
        metric.append(dict(index_id='4170003', value=str(t3)))
        metric.append(dict(index_id='4170005', value=str(t4)))
        metric.append(dict(index_id='4170001', value=str(t4-t5)))
        metric.append(dict(index_id='4170004', value=str(t6)))
        t1,t2 = getLags(kafka, node_id)
        if t1 >= 0:
            metric.append(dict(index_id='4170048', value=str(t1)))
        if t2 >= 0:
            metric.append(dict(index_id='4170049', value=str(t2)))

def robust(func):
    def add_robust(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except javax.management.RuntimeOperationsException as e:
            bt = str(e)
            exc_type, exc_value, exc_tb = sys.exc_info()
            for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
                bt += "\n%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname)
            print(bt)
            print(exc_type)
            print(exc_value)

    return add_robust

def getLags(kk, node_id):
    config = kk.client.describe_configs(config_resources=[ConfigResource(ConfigResourceType.BROKER, node_id)])
    parameters = config[0].resources
    zks = None
    path = '/'
    lag = -1
    lag2 = -1
    for item in parameters[0][4]:
        if item[0] == 'zookeeper.connect':
            zks = item[1]
            if zks.find('/') > 0:
                path = zks[zks.find('/'):]
                zks = zks[0:zks.find('/')]
            break
    cons = []
    zk.zk_kafka_consumers(zks, path, cons)
    if not cons:
        return lag2,lag
    try:
        kafka_consumer = KafkaConsumer(bootstrap_servers=kk.hosts)
    except Exception as e:
        print("Error, cannot connect kafka broker.")
        return lag2,lag
    else:
        kafka_logsize = {}
        kafka_topics = kafka_consumer.topics()
        #print(kafka_consumer.assignment())
        for kafka_topic in kafka_topics:
            kafka_logsize[kafka_topic] = {}
            partitions = kafka_consumer.partitions_for_topic(kafka_topic)
            for partition in partitions:
                offset = kafka_consumer.end_offsets([TopicPartition(kafka_topic, partition)])
                kafka_logsize[kafka_topic][int(partition)] = list(offset.values())[0]
        if kafka_logsize:
            tps = {}
            for metric in cons:
                met = kafka_logsize.get(metric[2])
                if met and met.get(metric[3]) is not None:
                    logsize = kafka_logsize[metric[2]][metric[3]]
                    metric[5] = int(logsize)
                    if metric[6] is not None:
                        l = int(logsize) - int(metric[6])
                        if l > lag:
                            lag = l
                        if tps.get(metric[2]) is not None:
                            tps[metric[2]] += l
                        else:
                            tps[metric[2]] = l
            if lag >= 0:
                if lag == 0:
                    lag2 = 0
                else:
                    for l in tps.values():
                        if l > lag2:
                            lag2 = l
    finally:
        kafka_consumer.close()
    return lag2,lag

if __name__ == '__main__':
    dbInfo = eval(sys.argv[1])
    usr = dbInfo['target_usr']
    host = dbInfo['target_ip']
    port = dbInfo['target_port']
    target_id = dbInfo['targetId']
    targetId, pg = DBUtil.get_pg_env(dbInfo,0)
    if pg.conn is None:
        print('无法连接本地数据库')
        sys.exit()
    metric = []
    do_kafka(pg, dbInfo, targetId, metric)
    print(metric)

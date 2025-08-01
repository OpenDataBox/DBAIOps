import sys
import time, datetime
from datetime import date, datetime, timedelta
import re
import traceback
import json
import psycopg2

from kafka import (KafkaClient, KafkaConsumer)
from kafka.admin import ConfigResource, ConfigResourceType
from kafka.structs import TopicPartition

sys.path.append('/usr/software/knowl')

import CommUtil
import DBUtil
import FormatUtil
import JavaRsa
import JavaUtil
import KafkaUtil
import zk
from baseline import get_sql

ctime = None

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


def get_baseline_limit(pg, target_id, idx):
    bsl = {}
    columns = 'index_id, upper_limit, lower_limit'
    tables = 'baseline_profile_detail b, mgt_system m'
    options = f""" b.profile_id = m.baseline_profile_id
     and m.uid='{target_id}' and b.index_id in ({idx}) and b.use_flag"""
    sql = get_sql(pg, target_id, columns, tables, options)
    result = relate_pg2(pg, sql)
    if result.code == 0:
        for row in result.msg:
            bsl[row[0]] = [row[1],row[2]]
    return bsl


def os_cluster(pg, hs, metric):
    mets = {}
    cnt = 0
    fail = 0
    bsl = get_baseline_limit(pg, list(hs)[0], '3000009,3000003,3000007,3001031,3000100,3000101,3000006,3000209') 
    for uid in hs:
        sql = '''select index_id,value,record_time from mon_indexdata where uid='%s' and index_id in (
3000000,3000009,3000003,3000007,3001031,3000100,3000101,3000006,3000209
)''' % uid
        result = relate_pg2(pg, sql)
        met = {}
        if result.code == 0:
            for row in result.msg:
                #ts = time.mktime(row[2].timetuple())
                if row[0] != 3000000:
                    met[row[0]] = [row[0],float(row[1]),row[2]]
                else:
                    met[row[0]] = [row[0],row[1],row[2]]
        if met.get(3000000) is None or time.mktime(met[3000000][2].timetuple()) < ctime - 600:
            continue
        if met[3000000][1] != '连接成功':
            fail += 1
            continue
        cnt += 1
        for m in met.values():
            if m[0] > 3000000 and time.mktime(m[2].timetuple()) > ctime - 600:
                if mets.get(m[0]) is not None:
                    mets[m[0]][0] += 1
                    mets[m[0]][1] += m[1]
                else:
                    mets[m[0]] = [1,m[1],0]
                if bsl.get(m[0]):
                    if bsl[m[0]][0] is not None:
                        if m[1] > bsl[m[0]][0]:
                            mets[m[0]][2] += 1
                    elif bsl[m[0]][1] is not None:
                        if m[1] < bsl[m[0]][1]:
                            mets[m[0]][2] += 1
                else:
                    mets[m[0]][2] = -1
    if cnt > 0:
        for k in mets.keys():
            metric.append(dict(index_id=str(4190000+(k%1000)),value=str(round(mets[k][1]/mets[k][0],2))))
            if mets[k][2] != -1:
                metric.append(dict(index_id=str(4191000+(k%1000)),value=str(round(mets[k][2]/mets[k][0],2))))
    metric.append(dict(index_id='4199994', value=str(cnt)))
    metric.append(dict(index_id='4199995', value=str(fail)))

def do_kafka(pg, dbInfo, targetId, metric):
    global ctime

    #sql = "select uid,ip,port,username,password,subuid from mgt_system where uid in %s and use_flag" % (tuple2(bs))
    sql = '''select a.uid,a.ip,a.port,a.username,a.password,b.uid from mgt_system a,mgt_device b,mgt_system_device c
where a.subuid=(select subuid from mgt_system where uid='%s' and use_flag) and a.uid like '2901%%' and a.use_flag and a.id=c.sys_id and b.id=c.dev_id and c.use_flag''' % (targetId)
    result = relate_pg2(pg, sql)
    ks = {}
    hs = set()
    hosts = ''
    usr = ''
    pwd = ''
    if result.code == 0:
        for row in result.msg:
            if row[0] != targetId:
                if not ks:
                    usr = row[3]
                    pwd = row[4]
                    if usr and pwd:
                        pwd = JavaUtil.decrypt(pwd)
                ks[row[0]] = '%s:%s' % (row[1],row[2])
                hs.add(row[5])
    """
    获取kafka的连接对象
    """
    ctime = int(time.time())
    mets = {}
    cnt = 0
    fail = 0
    for uid in ks.keys():
        sql = '''select index_id,value,record_time from mon_indexdata where uid='%s' and index_id in (
4150000,
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
4150307,
4153017,4153226,4153227,4153023
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
        if met.get(4150000) is None or time.mktime(met[4150000][2].timetuple()) < ctime - 600:
            continue
        if met[4150000][1] != '连接成功':
            fail += 1
            continue
        if cnt == 0:
            hosts = ks[uid]
        elif cnt < 3:
            hosts += ',' + ks[uid]
        if cnt == 0:
            bsl = get_baseline_limit(pg, uid, '4150009,4150010,4150011,4150012,4150013,4150014,4150116,4150122,4150137,4150216,4150222,4150237,4150307,4153017,4153226,4153227,4153023') 
        cnt += 1
        for m in met.values():
            if m[0] > 4150000 and time.mktime(m[2].timetuple()) > ctime - 600:
                v = None
                if m[0] == 4150222:
                    if met.get(4150122) is not None:
                        v = m[1] * met[4150122][1]
                        if mets.get(4150222+9000) is not None:
                            mets[4150222+9000][0] += 1
                            mets[4150222+9000][1] += met[4150122][1]
                        else:
                            mets[4150222+9000] = [1,met[4150122][1],-1]
                elif m[0] == 4150237:
                    if met.get(4150137) is not None:
                        v = m[1] * met[4150137][1]
                        if mets.get(4150237+9000) is not None:
                            mets[4150237+9000][0] += 1
                            mets[4150237+9000][1] += met[4150137][1]
                        else:
                            mets[4150237+9000] = [1,met[4150137][1],-1]
                elif m[0] == 4150216:
                    if met.get(4150116) is not None:
                        v = m[1] * met[4150116][1]
                        if mets.get(4150216+9000) is not None:
                            mets[4150216+9000][0] += 1
                            mets[4150216+9000][1] += met[4150116][1]
                        else:
                            mets[4150216+9000] = [1,met[4150116][1],-1]
                else:
                    v = m[1]
                if v is not None:
                    if mets.get(m[0]) is not None:
                        mets[m[0]][0] += 1
                        mets[m[0]][1] += v
                    else:
                        mets[m[0]] = [1,v,0]
                    if bsl.get(m[0]):
                        if bsl[m[0]][0] is not None:
                            if m[1] > bsl[m[0]][0]:
                                mets[m[0]][2] += 1
                        elif bsl[m[0]][1] is not None:
                            if m[1] < bsl[m[0]][1]:
                                mets[m[0]][2] += 1
                    else:
                        mets[m[0]][2] = -1
    if cnt > 0:
        for k in mets.keys():
            if k < 4159000:
                if k in [4150222,4150237,4150216]:
                    if mets[k+9000][1] > 0:
                        v = round(mets[k][1]/mets[k+9000][1],2)
                    else:
                        v = 0
                else:
                    v = round(mets[k][1]/mets[k][0],2)
                if k < 4153000:
                    metric.append(dict(index_id=str(k+42000), value=str(v)))
                    if mets[k][2] != -1:
                        metric.append(dict(index_id=str(k+44000), value=str(round(mets[k][2]/mets[k][0],2))))
                else:
                    metric.append(dict(index_id=str(k+43000), value=str(v)))
                    if mets[k][2] != -1:
                        metric.append(dict(index_id=str(k+44000), value=str(round(mets[k][2]/mets[k][0],2))))
    if cnt > 0 and hs:
        os_cluster(pg, hs, metric)
    if cnt+fail == 0:
        metric.append(dict(index_id='4190000', value='连接失败'))
        return
    metric.append(dict(index_id='4190000', value='连接成功'))
    metric.append(dict(index_id='4199999', value=str(ctime)))
    metric.append(dict(index_id='4199996', value=str(cnt)))
    metric.append(dict(index_id='4199997', value=str(fail)))
    if cnt > 0:
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
        metric.append(dict(index_id='4192050', value=str(t)))
        metric.append(dict(index_id='4192051', value=str(tt)))
        metric.append(dict(index_id='4192052', value=str(controller_id)))
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
        metric.append(dict(index_id='4192054', value=str(t1)))
        metric.append(dict(index_id='4192053', value=str(t2)))
        metric.append(dict(index_id='4192003', value=str(t3)))
        metric.append(dict(index_id='4192005', value=str(t4)))
        metric.append(dict(index_id='4192001', value=str(t4-t5)))
        metric.append(dict(index_id='4192004', value=str(t6)))
        t1,t2 = getLags(kafka, node_id)
        if t1 >= 0:
            metric.append(dict(index_id='4192048', value=str(t1)))
        if t2 >= 0:
            metric.append(dict(index_id='4192049', value=str(t2)))

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
    print('{"results":' + json.dumps(metric, ensure_ascii=False) + '}')

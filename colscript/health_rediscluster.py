import sys
import time, datetime
from datetime import date, datetime, timedelta
import re
import traceback
import json

from kafka import (KafkaClient, KafkaConsumer)
from kafka.admin import ConfigResource, ConfigResourceType
from kafka.structs import TopicPartition

sys.path.append('/usr/software/knowl')

import CommUtil
import DBUtil
import FormatUtil
import JavaRsa
import JavaUtil
import zk

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

def get_baseline_limit(pg, target_id, idx):
    bsl = {}
    sql = """
    SELECT
     index_id, upper_limit, lower_limit
 FROM
     baseline_profile_detail b,
     mgt_system m
 WHERE
     b.profile_id = m.baseline_profile_id
     and m.uid='%s' and b.index_id in (%s) and b.use_flag
""" % (target_id, idx)
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
            metric.append(dict(index_id=str(2350000+(k%1000)),value=str(round(mets[k][1]/mets[k][0],2))))
            if mets[k][2] != -1:
                metric.append(dict(index_id=str(2351000+(k%1000)),value=str(round(mets[k][2]/mets[k][0],2))))
    metric.append(dict(index_id='2359994', value=str(cnt)))
    metric.append(dict(index_id='2359995', value=str(fail)))

def do_redis(pg, dbInfo, targetId, metric):
    global ctime

    #sql = "select uid,ip,port,username,password,subuid from mgt_system where uid in %s and use_flag" % (tuple2(bs))
    sql = '''select a.uid,a.ip,a.port,a.username,a.password,b.uid from mgt_system a,mgt_device b,mgt_system_device c
where a.subuid=(select subuid from mgt_system where uid='%s' and use_flag) and a.uid like '2108%%' and a.use_flag and a.id=c.sys_id and b.id=c.dev_id and c.use_flag''' % (targetId)
    result = relate_pg2(pg, sql)
    ks = {}
    hs = set()
    hosts = []
    username = ''
    pwd = ''
    if result.code == 0:
        for row in result.msg:
            if row[0] != targetId:
                if not ks:
                    username = row[3]
                    pwd = row[4]
                    if pwd:
                        pwd = JavaUtil.decrypt(pwd)
                ks[row[0]] = '%s:%s' % (row[1],row[2])
                hs.add(row[5])
    ctime = int(time.time())
    mets = {}
    cnt = 0
    fail = 0
    for uid in ks.keys():
        sql = '''select index_id,value,record_time from mon_indexdata where uid='%s' and index_id in (
2170000,
2170051,
2170108,
2171014,
2170054,
2171007,
2171008,
2170007,
2170006,
2170003,
2171001,
2171011,
2171012,
2171013,
2171002,
2171015,2170112,2171010,2170361,2170363
)''' % uid
        result = relate_pg2(pg, sql)
        met = {}
        if result.code == 0:
            for row in result.msg:
                #ts = time.mktime(row[2].timetuple())
                if row[0] != 2170000:
                    met[row[0]] = [row[0],float(row[1]),row[2]]
                else:
                    met[row[0]] = [row[0],row[1],row[2]]
        if met.get(2170000) is None or time.mktime(met[2170000][2].timetuple()) < ctime - 600:
            continue
        if met[2170000][1] != '连接成功':
            fail += 1
            continue
        if cnt < 3:
            hosts.append(ks[uid])
        if cnt == 0:
            bsl = get_baseline_limit(pg, uid, '2170051,2170108,2171014,2170054,2171007,2171008,2170007,2170006,2170003,2171001,2171011,2171012,2171013,2171002,2171015,2170112,2171010')
        cnt += 1
        for m in met.values():
            if m[0] > 2170000 and time.mktime(m[2].timetuple()) > ctime - 600:
                v = None
                if m[0] == 2171008:
                    if met.get(2171007) is not None:
                        v = m[1] * met[2171007][1]
                        if mets.get(2171008+9000) is not None:
                            mets[2171008+9000][0] += 1
                            mets[2171008+9000][1] += met[2171007][1]
                        else:
                            mets[2171008+9000] = [1,met[2171007][1],-1]
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
            if k < 2179000:
                if k in [2171008]:
                    if mets[k+9000][1] > 0:
                        v = round(mets[k][1]/mets[k+9000][1],2)
                    else:
                        v = 0
                else:
                    v = round(mets[k][1]/mets[k][0],2)
                metric.append(dict(index_id=str(k+182000), value=str(v)))
                if mets[k][2] != -1:
                    metric.append(dict(index_id=str(k+184000), value=str(round(mets[k][2]/mets[k][0],2))))
    if cnt > 0 and hs:
        os_cluster(pg, hs, metric)
    if cnt+fail == 0:
        metric.append(dict(index_id='2350000', value='连接失败'))
        return
    metric.append(dict(index_id='2350000', value='连接成功'))
    metric.append(dict(index_id='2359999', value=str(ctime)))
    metric.append(dict(index_id='2359996', value=str(cnt)))
    metric.append(dict(index_id='2359997', value=str(fail)))
    if cnt > 0:
        conn = failover(pg, targetId, hosts, username, pwd)
        if conn:
            cluster(pg, targetId, conn, metric)

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

def cluster(pg, target_id, conn, metric):
    cluster_enabled = conn.info("cluster")["cluster_enabled"]
    if cluster_enabled == 1:
        result = conn.cluster("info")
        if result.get("cluster_state") is not None:
            metric.append(dict(index_id=2352701, value=str(result["cluster_state"])))
        if result.get("cluster_slots_assigned") is not None:
            metric.append(dict(index_id=2352702, value=str(result["cluster_slots_assigned"])))
            tt = int(float(result["cluster_slots_assigned"]))
            metric.append(dict(index_id=2352720, value=str(round(tt*100/16384,2))))
        else:
            tt = 0
        if result.get("cluster_slots_ok") is not None:
            metric.append(dict(index_id=2352703, value=str(result["cluster_slots_ok"])))
        if result.get("cluster_slots_pfail") is not None:
            metric.append(dict(index_id=2352704, value=str(result["cluster_slots_pfail"])))
            if tt > 0:
                metric.append(dict(index_id=2352721, value=str(round(float(result["cluster_slots_pfail"])*100/tt,2))))
        if result.get("cluster_slots_fail") is not None:
            metric.append(dict(index_id=2352705, value=str(result["cluster_slots_fail"])))
            if tt > 0:
                metric.append(dict(index_id=2352722, value=str(round(float(result["cluster_slots_fail"])*100/tt,2))))
        if result.get("cluster_known_nodes") is not None:
            metric.append(dict(index_id=2352706, value=str(result["cluster_known_nodes"])))
            cnt = int(float(result["cluster_known_nodes"]))
        else:
            cnt = 0
        if result.get("cluster_size") is not None:
            metric.append(dict(index_id=2352707, value=str(result["cluster_size"])))
            mcnt = int(float(result["cluster_size"]))
        else:
            mcnt = 0
        if result.get("cluster_current_epoch") is not None:
            metric.append(dict(index_id=2352708, value=str(result["cluster_current_epoch"])))
        cluster_nodes = conn.cluster("nodes")
        nodes = {}
        fail = 0
        mfail = 0
        for key, item in cluster_nodes.items():
            cluster_port = ""
            ip = key.split(":")[0]
            if '@' in key:
                port, cluster_port = key.split(":")[1].split("@")
            else:
                port = key.split(":")[1]
            flags = item["flags"]
            if flags.find('master') >= 0:
                role = 0
            else:
                role = 1
            if item["connected"]:
                st = 1
            else:
                st = 0
                fail += 1
                if role == 0:
                    mfail += 1
            id = item["master_id"]
            if id == '-':
                id = ''
            nodes[ip+':'+port] = [1,0,0,ip,port,id,role,item["node_id"],int(item["epoch"]),None,st]
        redis_cluster(pg, target_id, nodes)
        if cnt > 0:
            metric.append(dict(index_id=2352718, value=str(fail)))
            metric.append(dict(index_id=2352723, value=str(round(fail*100/cnt,2))))
        if mcnt > 0:
            metric.append(dict(index_id=2352719, value=str(mfail)))
            metric.append(dict(index_id=2352724, value=str(round(mfail*100/mcnt,2))))

def redis_cluster(pg, target_id, nodes):
    sdate = datetime.fromtimestamp(time.time())
    bf = False
    cur = None
    try:
        sql = "select id,seqno,master_host,master_port,master_user,master_id,master_uuid,sql_delay,state,master_uid from ha_mysql where target_id='%s' order by master_id" % target_id
        result = relate_pg2(pg, sql)
        if result.code != 0:
            return
        for row in result.msg:
            s = str(row[2]) + ':' + str(row[3])
            m = nodes.get(s)
            if m is None:
                nodes[s] = [[2, row[0], row[1], row[2], cs(row[3]), row[4], row[5], row[6], row[7], row[9], row[8]]]
            else:
                if m[7] != row[6]:
                    m[0] = 3
                elif m[10] != row[8]:
                    m[0] = 4
                elif m[5] != row[4] or m[6] != row[5] or m[8] != row[7]:
                    m[0] = 5
                else:
                    m[0] = 0
                m[1] = row[0]
                m[2] = row[1]
                m[9] = row[9]
        ids = set()
        for m in nodes.values():
            if not (m[0] == 0 or (m[0] == 2 and m[10] == 2)):
                if m[0] == 1:
                    sql = "select nextval('public.ha_mysql_id')"
                    result = relate_pg2(pg, sql)
                    if result.code == 0 and len(result.msg) > 0:
                        m[1] = result.msg[0][0]
                    else:
                        continue
                bf = True
            if m[0] != 2 and not m[9]:
                s = m[3] + ':' + str(m[4])
                # sql = "select target_id from p_oracle_cib where index_id=2210001 and cib_name='address' and cib_value='%s'" % s
                sql = "select uid,subuid from mgt_system where uid like '2106%%' and ip='%s' and port='%s' and use_flag" % (m[3], m[4])
                result = relate_pg2(pg, sql)
                if result.code == 0 and len(result.msg) > 0:
                    id = result.msg[0][0]
                    id2 = result.msg[0][1]
                    sql = "select cib_value from p_oracle_cib where target_id='%s' and index_id=2160001 and cib_name in ('node_id')" % id
                    result = relate_pg2(conn, sql)
                    if result.code == 0 and len(result.msg) > 0:
                        if result.msg[0][0] == m[7]:
                            m[9] = id
                            if id2 != target_id:
                                ids.add(id)
                            bf = True
                            if m[0] == 0:
                                m[0] = 10
        if bf:
            cur = pg.conn.cursor()
            for m in nodes.values():
                if m[0] == 0 or (m[0] == 2 and m[10] == 2):
                    continue
                s = ""
                t = m[2] + 1
                st = m[10]
                if m[0] > 1:
                    ss = ""
                    if m[0] == 2:
                        s = '退出集群'
                        st = 2
                    elif m[0] == 3:
                        s = '重新加入集群'
                    elif m[0] == 4:
                        s = '节点状态发生变化'
                    elif m[0] == 5:
                        s = '节点配置发生变化'
                    if m[0] == 10:
                        sql = "update ha_mysql set master_uid='%s' where id=%d" % (m[9], m[1])
                    else:
                        if m[9]:
                            ss += ",master_uid='%s'" % m[9]
                        sql = '''update ha_mysql set seqno=%d,state=%d,master_user='%s',master_id=%d,master_uuid='%s',sql_delay=%d%s,update_time=now() 
where id=%d''' % (t, st, m[5], m[6], m[7], m[8], ss, m[1])
                        m[2] = t
                    cur.execute(sql)
                else:
                    s = '加入集群'
                    sql = '''insert into ha_mysql(id,seqno,target_id,master_host,master_port,master_user,master_id,master_uuid,sql_delay,state,master_uid,create_time) 
values(%d,%d,'%s','%s',%s,'%s',%d,'%s',%d,%d,'%s',timestamp '%s')''' % (
                            m[1], t, target_id, m[3], m[4], m[5], m[6], m[7], m[8], st, cs(m[9]), cs(sdate, True))
                    cur.execute(sql)
                    m[2] = t
                if m[0] != 10:
                    sql = "insert into ha_mysql_log(id,seqno,target_id,master_id,master_uid,info,state,create_time,master_uuid) values(%d,%d,'%s','%s','%s','%s',%d,timestamp '%s','%s')" % (
                        m[1], t, target_id, '%s:%s,%d,%d' % (m[3],m[4],m[6],m[8]), cs(m[9]), s, st, cs(sdate, True),
                        cs(m[7]))
                else:
                    sql = "update ha_mysql_log set master_uid='%s' where id=%d and seqno=%d" % (m[9], m[1], m[2])
                cur.execute(sql)
                if ids:
                    sql = "update mgt_system set subuid='%s' where uid in %s and use_flag" % (target_id, tuple2(ids))
                    cur.execute(sql)
            pg.conn.commit()
    except Exception as e:
        #print(e)
        if not cur is None:
            pg.conn.rollback()
    return

def failover(pg, target_id, hosts, username, pwd):
    for h in hosts:
        try:
            arr = h.split(':')
            if len(arr) == 1:
                ip = arr[0]
                pt = port
            else:
                ip = arr[0]
                pt = arr[1]
            conn = get_redis_session(ip, pt, username, pwd)
            if conn:
                break
        except:
            conn = None
    return conn

def get_redis_session(ip, port, username, pwd):
    import redis

    if pwd:
        POOL = redis.ConnectionPool(host=ip, port=port, username=username, password=pwd)
    else:
        POOL = redis.ConnectionPool(host=ip, port=port)
    server = redis.Redis(connection_pool=POOL)
    return server

if __name__ == '__main__':
    dbInfo = eval(sys.argv[1])
    targetId, pg = DBUtil.get_pg_env(dbInfo,0)
    if pg.conn is None:
        print('无法连接本地数据库')
        sys.exit()
    metric = []
    do_redis(pg, dbInfo, targetId, metric)
    print('{"results":' + json.dumps(metric, ensure_ascii=False) + '}')

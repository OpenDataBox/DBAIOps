import json
import os
import sys
import time
from datetime import datetime, timedelta

sys.path.append('/usr/software/knowl')
import DBUtil
import JavaRsa

vals = []
metric = []

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


def cs(val, dt=False):
    if val is None:
        return ''
    else:
        if dt:
            return val.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return str(val)


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


def cib_basic(conn,dbinfo):
    target_ip = dbinfo['target_ip']
    vals_append("host_ip", target_ip)
    result = conn.info()
    info_item = ["redis_version", "process_id", "os", "arch_bits", "redis_mode", "gcc_version", "tcp_port",
                 "uptime_in_days",
                 "executable", "config_file", "connected_clients", "used_memory_human", "used_memory_peak_human",
                 "used_memory_lua_human", "total_system_memory_human", "maxmemory_human", "maxmemory_policy", 'role',
                 "run_id"]
    info_item_zh = ["数据库版本", "进程ID", "操作系统版本", "CPU架构", "运行模式", "GCC版本", "监听端口", "运行天数", "可执行文件路径", "配置文件路径",
                    "客户端连接数", "已用内存", "内存占用峰值", "Lua占用内存", "操作系统内存", "最大可用内存", "内存溢出策略", "角色", "run_id"]
    for item in info_item:
        vals_append(item, result[item])
    config_item = ["bind", "logfile", "loglevel", "requirepass", "appendonly", "save", "appendfsync", ]
    config_item_zh = ["监控IP", "日志文件路径", "日志级别", "密码验证是否开启", "AOF是否开启", "RDB写入配置", "AOF日志刷新策略"]
    db_file_path = os.path.join(conn.config_get("dir")["dir"], conn.config_get("dbfilename")["dbfilename"])
    vals_append("db_file_path", db_file_path)  # 数据文件路径
    for item in config_item:
        if item == 'requirepass':
            if conn.config_get(item)[item]:
                vals_append(item, '是')
            else:
                vals_append(item, '否')
        else:
            vals_append(item, conn.config_get(item)[item])
    append_file_name = conn.config_get("appendfilename")
    if append_file_name:
        vals_append("appendfilename", append_file_name["appendfilename"])  # AOF持久化文件名
    else:
        vals_append("appendfilename", "")
    metric.append(dict(index_id=2360001, value=vals))


def cib_parameters(conn):
    params = []
    result = conn.config_get()
    for key, value in result.items():
        params.append(dict(name=key, value=value))
    metric.append(dict(index_id=2360002, value=params))


def cib_cluster(pg, target_id, conn):
    cluster_enabled = conn.info("cluster")["cluster_enabled"]
    if cluster_enabled == 1:
        cluster_nodes_list = []
        table_append(cluster_nodes_list, "IP", "端口", "集群通讯端口", "node_id", "角色", "master_id",
                     "last_pong_rcvd", "epoch", "slots", "connected")
        cluster_nodes = conn.cluster("nodes")
        nodes = {}
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
            id = item["master_id"]
            if id == '-':
                id = ''
            nodes[ip+':'+port] = [1,0,0,ip,port,id,role,item["node_id"],int(item["epoch"]),None,st]
            table_append(cluster_nodes_list, ip, port, cluster_port, item["node_id"], item["flags"], item["master_id"],
                         item["last_pong_rcvd"], item["epoch"], item["slots"], item["connected"])
        metric.append(dict(index_id=2360004, content=cluster_nodes_list))
        redis_cluster(pg, target_id, nodes)


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
            if not ((m[0] == 0 and m[9]) or (m[0] == 2 and m[10] == 2)):
                if m[0] == 1:
                    sql = "select nextval('public.ha_mysql_id')"
                    result = relate_pg2(pg, sql)
                    if result.code == 0 and len(result.msg) > 0:
                        m[1] = result.msg[0][0]
                    else:
                        continue
                if m[0]:
                    bf = True
            if m[0] != 2 and not m[9]:
                s = m[3] + ':' + str(m[4])
                # sql = "select target_id from p_oracle_cib where index_id=2210001 and cib_name='address' and cib_value='%s'" % s
                sql = "select uid,subuid from mgt_system where uid like '2108%%' and ip='%s' and port='%s' and use_flag" % (m[3], m[4])
                result = relate_pg2(pg, sql)
                if result.code == 0 and len(result.msg) > 0:
                    id = result.msg[0][0]
                    id2 = result.msg[0][1]
                    sql = "select cib_value from p_oracle_cib where target_id='%s' and index_id=2160001 and cib_name in ('node_id')" % id
                    result = relate_pg2(pg, sql)
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
                ids.add(target_id)
                if ids:
                    sql = "update mgt_system set subuid='%s' where uid in %s and use_flag" % (target_id, tuple2(ids))
                    cur.execute(sql)
            pg.conn.commit()
    except Exception as e:
        print(e)
        if not cur is None:
            pg.conn.rollback()
    return


def failover(pg, target_id, host, port, username, pwd):
    hosts = []
    ph = host+':'+port
    f = False
    hs = None
    sql = "select cib_name,cib_value from p_normal_cib where index_id=1000001 and cib_name in ('nodes','_startup') and target_id='%s'" % target_id
    result = relate_pg2(pg, sql)
    if result.code == 0:
        for row in result.msg:
            if row[0] == 'nodes':
                hs = row[1]
            else:
                ph = row[1]
                f = True
    hosts.append(ph)
    if hs:
        arr = hs.split(',')
        for it in arr:
            if it:
                if it != ph:
                    hosts.append(it)
    conn = None
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
                if h != ph:
                    if f:
                        sql = "update p_normal_cib set cib_value='%s',record_time=now() where target_id='%s' and cib_name='_startup' and index_id=1000001" % (h,target_id)
                    else:
                        sql = "insert into p_normal_cib(target_id,index_id,cib_name,cib_value,record_time) values('%s',1000001,'_startup','%s',now())" % (target_id,h)
                    try:
                        cur = pg.conn.cursor()
                        cur.execute(sql)
                        pg.conn.commit()
                    except:
                        pg.conn.rollback()
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

def main():
    dbInfo = eval(sys.argv[1])
    username = dbInfo.get("target_usr")
    password = dbInfo.get("target_pwd")
    if password:
        password = JavaRsa.decrypt(password)
    host = dbInfo["target_ip"]
    port = dbInfo["target_port"]
    target_id, pg = DBUtil.get_pg_env()
    conn = failover(pg, target_id, host, str(port), username, password)
    if conn is None:
        sys.exit(1)
    cib_basic(conn,dbInfo)
    cib_parameters(conn)
    cib_cluster(pg, target_id, conn)
    print('{"cib":' + json.dumps(metric) + '}')

if __name__ == '__main__':
    dbInfo = eval(sys.argv[1])
    username = dbInfo.get("target_usr")
    password = dbInfo.get("target_pwd")
    if password:
        password = JavaRsa.decrypt(password)
    host = dbInfo["target_ip"]
    port = dbInfo["target_port"]
    target_id, pg = DBUtil.get_pg_env(dbInfo)
    conn = failover(pg, target_id, host, str(port), username, password)
    if conn is None:
        sys.exit(1)
    cib_basic(conn,dbInfo)
    cib_parameters(conn)
    cib_cluster(pg, target_id, conn)
    print('{"cib":' + json.dumps(metric) + '}')

import json
import os
import sys


sys.path.append('/usr/software/knowl')
import DBUtil

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
        cur = conn.cursor()
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


def vals_append(key, value):
    vals.append(dict(name=key, value=str(value)))


def table_append(tab_list, c1=None, c2=None, c3=None, c4=None, c5=None, c6=None, c7=None, c8=None, c9=None, c10=None):
    tab_list.append(dict(c1=c1, c2=c2, c3=c3, c4=c4, c5=c5, c6=c6, c7=c7, c8=c8, c9=c9, c10=c10))


def cib_basic(conn,dbinfo):
    target_ip = dbinfo['target_ip']
    vals_append("host_ip", target_ip)
    result = conn.info()
    redis_version_lst = result["redis_version"].split('.')
    redis_version = '.'.join([redis_version_lst[0],redis_version_lst[1]])
    if float(redis_version) > 3:
        info_item = ["redis_version", "process_id", "os", "arch_bits", "redis_mode", "gcc_version", "tcp_port",
                     "uptime_in_days",
                     "executable", "config_file", "connected_clients", "used_memory_human", "used_memory_peak_human",
                     "used_memory_lua_human", "total_system_memory_human", "maxmemory_human", "maxmemory_policy", 'role',
                     "run_id"]
        info_item_zh = ["数据库版本", "进程ID", "操作系统版本", "CPU架构", "运行模式", "GCC版本", "监听端口", "运行天数", "可执行文件路径", "配置文件路径",
                        "客户端连接数", "已用内存", "内存占用峰值", "Lua占用内存", "操作系统内存", "最大可用内存", "内存溢出策略", "角色", "run_id"]
    else:
        info_item = ["redis_version", "process_id", "os", "arch_bits", "redis_mode", "gcc_version", "tcp_port",
                     "uptime_in_days", "connected_clients", "used_memory_human", "used_memory_peak_human", "role", "run_id"]
        info_item_zh = ["数据库版本", "进程ID", "操作系统版本", "CPU架构", "运行模式", "GCC版本", "监听端口", "运行天数",
                        "客户端连接数", "已用内存", "内存占用峰值", "角色", "run_id"]
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


def cib_parameters(conn):
    params = []
    result = conn.config_get()
    for key, value in result.items():
        params.append(dict(name=key, value=value))
    metric.append(dict(index_id=2160002, value=params))


def cib_keyspace(conn):
    result = conn.info("keyspace")
    keyspace_list = []
    table_append(keyspace_list, '数据库ID', "键数量", "带有过期时间的键数量", '键平均存活时间')
    for key, item in result.items():
        table_append(keyspace_list, str(key), str(item["keys"]), str(item["expires"]), str(item["avg_ttl"]))
    metric.append(dict(index_id=2160003, content=keyspace_list))


def cib_cluster(conn):
    result = conn.info("server")
    redis_version_lst = result["redis_version"].split('.')
    redis_version = '.'.join([redis_version_lst[0],redis_version_lst[1]])
    if float(redis_version) > 3:
        node_id = ''
        cluster_enabled = conn.info("cluster")["cluster_enabled"]
        if cluster_enabled == 1:
            cluster_nodes_list = []
            table_append(cluster_nodes_list, "IP", "端口", "集群通讯端口", "node_id", "角色", "master_id",
                         "last_pong_rcvd", "epoch", "slots", "connected")
            cluster_nodes = conn.cluster("nodes")
            for key, item in cluster_nodes.items():
                cluster_port = ""
                ip = key.split(":")[0]
                if '@' in key:
                    port, cluster_port = key.split(":")[1].split("@")
                else:
                    port = key.split(":")[1]
                if item["flags"].find('myself') >= 0:
                    node_id = item["node_id"]
                table_append(cluster_nodes_list, ip, port, cluster_port, item["node_id"], item["flags"], item["master_id"],
                             item["last_pong_rcvd"], item["epoch"], item["slots"],
                             item["connected"])
            metric.append(dict(index_id=2160004, content=cluster_nodes_list))
        vals_append("node_id", node_id)


def set_focus(conn, uid):
    sql = f"select distinct cib_value from p_oracle_cib c where c.target_id='{uid}' and index_id=2160001 and cib_name in ('executable','config_file','db_file_path','logfile')"
    result = relate_pg2(conn, sql)
    path = ''
    if result.code == 0:
        for row in result.msg:
            if path:
                path += ',' + row[0]
            else:
                path = row[0]
    if not path:
        return
    path += ',/,/tmp'
    sql = f"select cib_value from p_normal_cib where target_id='{uid}' and index_id=1000001 and cib_name='_focus_path' order by record_time desc limit 1"
    result = relate_pg2(conn, sql)
    if result.code == 0 and len(result.msg) == 1:
        if path != result.msg[0][0]:
            sql = f"update p_normal_cib set cib_value='{path}',record_time=now() where target_id='{uid}' and index_id=1000001 and cib_name='_focus_path'"
        else:
            sql = None
    else:
        sql = f"insert into p_normal_cib(target_id,index_id,cib_name,cib_value,record_time) values('{uid}',1000001,'_focus_path','{path}',now())"
    if not sql:
        return
    try:
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
    except psycopg2.ProgrammingError:
        conn.rollback()


if __name__ == '__main__':
    dbInfo = eval(sys.argv[1])
    target_id, pg = DBUtil.get_pg_env(None, 0)
    conn = DBUtil.get_redis_env()
    cib_basic(conn,dbInfo)
    cib_parameters(conn)
    cib_keyspace(conn)
    cib_cluster(conn)
    set_focus(pg.conn, target_id)
    metric.append(dict(index_id=2160001, value=vals))
    print('{"cib":' + json.dumps(metric) + '}')

import json
import sys
import time
from datetime import datetime
sys.path.append('/usr/software/knowl')
import DBUtil

vals = []
metric = []
result = {}


def vals_append(index_id, key):
    if result.get(key) is not None:
        if str(result[key]).endswith("%"):
            value = str(result[key]).replace('%', '')
        else:
            value = str(result[key])
        vals.append(dict(index_id=index_id, value=value))


def metric_append(index_id, value):
    if isinstance(value, list):
        vals.append(dict(index_id=index_id, value=value))
    else:
        vals.append(dict(index_id=index_id, value=str(value)))


def dict_get(primary_key, second_key):
    if result.get(primary_key, 0) == 0:
        value = 0
    else:
        value = result[primary_key][second_key]
    return value


def map_commands(commands_list):
    calls = usecs = 0
    for item in commands_list:
        key = f'cmdstat_{item}'
        calls += dict_get(key, 'calls')
        usecs += dict_get(key, 'usec')
    return calls, usecs


def info_stats(conn):
    global result
    string_commands = ["get", "set", "del", "incr", "decr", "incyby", "decrby", "incrbyfloat", "append", "getrange",
                       "setrange", "getbit", "setbit", "bitcount", "bitop", "strlen", "setex", "setrange"]
    list_commands = ["rpush", "lrange", "lindex", "lpop", "lpush", "rpop", "ltrim", "blpop", "brpop", "rpoplpush",
                     "brpoplpush"]
    set_commands = ["sadd", "smembers", "sismember", "srem", "scard", "srandmember", "spop", "smove", "sdiff",
                    "sdiffstore", "sinter", "sinterstore", "sunion", "sunionstore"]
    hash_commands = ["hset", "hget", "hgetall", "hdel", "hmget", "hmset", "hlen", "hexists", "hkeys", "hvals",
                     "hgetall", "hincrby", "hincrbyfloat"]
    sorted_set_commands = ["zadd", "zrange", "zrangebyscore", "zrem", "zcard", "zincrby", "zcount", "zrank", "zscore",
                           "zrevrank", "zrevrange", "zrangebyscore", "zrevrangebyscore", "zremrangebyrank",
                           "zremrangebyscore", "zinterstore", "zunionstore"]
    pub_sub_commands = ["subscribe", "unsubscribe", "pubish", "psubscribe", "punsubscribe"]
    sort_commands = ["sort"]
    expire_commands = ["persist", "ttl", "expire", "expireat", "pttl", "pexpire", "pexpireat"]
    hyperloglog_commands = ["pfadd", "pfcount", "pfmerge"]
    geo_commands = ["geoadd", "geopos", "georadius", "geodist", "georadiusbymember", "geohash"]
    eval_commands = ["eval", "evalsha"]
    get_type_commands = ["get", "hget", "hmget", "scard", "lrange","scan"]
    set_type_commands = ["set", "hset", "hmset", "sadd", "lpop"]
    stream_commands = ["xrange", "xlen", "xadd", "xdel"]

    result = conn.info("server")
    vals_append(2179998, "uptime_in_seconds")
    redis_mode = result["redis_mode"]
    redis_version_lst = result["redis_version"].split('.')
    redis_version = '.'.join([redis_version_lst[0],redis_version_lst[1]])
    result = conn.info("stats")
    # for index, item in enumerate(result):
    #     vals.append(dict(index_id=2170001 + index, value=result[item]))
    vals_append(2170001, "total_connections_received")
    vals_append(2170002, "total_commands_processed")
    vals_append(2170003, "instantaneous_ops_per_sec")
    vals_append(2170008, "rejected_connections")
    vals_append(2170012, "expired_keys")
    vals_append(2170015, "evicted_keys")
    vals_append(2170016, "keyspace_hits")
    vals_append(2170017, "keyspace_misses")
    vals_append(2170018, "pubsub_channels")
    vals_append(2170019, "pubsub_patterns")
    vals_append(2170020, "latest_fork_usec")
    if float(redis_version) > 3:
        vals_append(2170021, "migrate_cached_sockets")
        vals_append(2170022, "slave_expires_tracked_keys")
        vals_append(2170023, "active_defrag_hits")
        vals_append(2170024, "active_defrag_misses")
        vals_append(2170025, "active_defrag_key_hits")
        vals_append(2170026, "active_defrag_key_misses")
        vals_append(2170004, "total_net_input_bytes")
        vals_append(2170005, "total_net_output_bytes")
        vals_append(2170006, "instantaneous_input_kbps")
        vals_append(2170007, "instantaneous_output_kbps")
        vals_append(2170009, "sync_full")
        vals_append(2170010, "sync_partial_ok")
        vals_append(2170011, "sync_partial_err")
        vals_append(2170013, "expired_stale_perc")
        vals_append(2170014, "expired_time_cap_reached_count")
    result = conn.info("clients")
    # for index, item in enumerate(result):
    #     vals.append(dict(index_id=2170051 + index, value=result[item]))
    vals_append(2170051, "connected_clients")
    vals_append(2170052, "client_longest_output_list")
    vals_append(2170053, "client_biggest_input_buf")
    vals_append(2170054, "blocked_clients")
    if float(redis_version) > 3:
        vals_append(2170055, "client_recent_max_input_buffer")
        vals_append(2170056, "client_recent_max_output_buffer")

    result = conn.info("memory")
    vals_append(2170101, "used_memory")
    vals_append(2170102, "used_memory_rss")
    vals_append(2170103, "used_memory_peak")
    vals_append(2170110, "used_memory_lua")
    vals_append(2170112, "mem_fragmentation_ratio")
    if float(redis_version) > 3:
        vals_append(2170104, "used_memory_peak_perc")
        vals_append(2170105, "used_memory_overhead")
        vals_append(2170106, "used_memory_startup")
        vals_append(2170107, "used_memory_dataset")
        vals_append(2170108, "used_memory_dataset_perc")
        vals_append(2170109, "total_system_memory")
        vals_append(2170111, "maxmemory")
        vals_append(2170113, "active_defrag_running")
        vals_append(2170114, "lazyfree_pending_objects")
        used_memory = result["used_memory"]
        used_memory_rss = result["used_memory_rss"]
        max_memory = result["maxmemory"]
        total_system_memory = result["total_system_memory"]
        pct = 0
        if max_memory == 0:
            pct = round(used_memory_rss / (total_system_memory - 2 * 1024 * 1024 * 1024) * 100, 2)
        elif max_memory > 0:
            pct = round(used_memory / max_memory * 100, 2)
        metric_append(2171014, pct)

    result = conn.info("replication")
    vals_append(2170158, "role")
    role = result["role"]
    if role == "slave":
        vals_append(2170151, "master_last_io_seconds_ago")
        vals_append(2170152, "master_sync_in_progress")
    vals_append(2170153, "connected_slaves")
    if float(redis_version) > 3:
        vals_append(2170154, "repl_backlog_active")
        vals_append(2170155, "repl_backlog_size")
        vals_append(2170156, "repl_backlog_first_byte_offset")
        vals_append(2170157, "repl_backlog_histlen")

    result = conn.info("cpu")
    vals_append(2170201, "used_cpu_sys")
    vals_append(2170202, "used_cpu_user")
    vals_append(2170203, "used_cpu_sys_children")
    vals_append(2170204, "used_cpu_user_children")

    result = conn.info("persistence")
    vals_append(2170251, "loading")
    vals_append(2170252, "rdb_changes_since_last_save")
    vals_append(2170253, "rdb_last_save_time")
    vals_append(2170265, "rdb_last_bgsave_status")
    vals_append(2170254, "rdb_last_bgsave_time_sec")
    vals_append(2170255, "rdb_current_bgsave_time_sec")
    vals_append(2170260, "aof_enabled")
    vals_append(2170261, "aof_rewrite_in_progress")
    vals_append(2170262, "aof_rewrite_scheduled")
    vals_append(2170263, "aof_last_bgrewrite_status")
    vals_append(2170257, "aof_last_rewrite_time_sec")
    vals_append(2170258, "aof_current_rewrite_time_sec")
    if float(redis_version) > 3:
        vals_append(2170256, "rdb_last_cow_size")
        vals_append(2170259, "aof_last_cow_size")
        vals_append(2170264, "aof_last_write_status")
        last_save_status = ''
        last_save_operation_consume_time = 0
        last_to_now_change_in_bytes = 0
        last_to_now_in_seconds = 0
        if result['rdb_last_save_time'] or result['aof_enabled']:
            if result['aof_enabled'] == 1:
                last_save_status = result['aof_last_write_status']
                if not redis_version.startswith('3'):
                    last_to_now_change_in_bytes = result['aof_last_cow_size']
                if result['aof_current_rewrite_time_sec']:
                    last_save_operation_consume_time = result['aof_current_rewrite_time_sec']
                else:
                    last_save_operation_consume_time = result['aof_last_rewrite_time_sec']
            else:
                last_save_status = result['rdb_last_bgsave_status']
                if not redis_version.startswith('3'):
                    last_to_now_change_in_bytes = result['rdb_last_cow_size']
                t1 = time.time()
                t2 = result['rdb_last_save_time']
                last_to_now_in_seconds = (datetime.fromtimestamp(t1) - datetime.fromtimestamp(t2)).seconds
                if result['rdb_current_bgsave_time_sec']:
                    last_save_operation_consume_time = result['rdb_current_bgsave_time_sec']
                else:
                    last_save_operation_consume_time = result['rdb_last_bgsave_time_sec']
        
        vals.append(dict(index_id=2170266, value=last_save_status))
        vals.append(dict(index_id=2170267, value=last_save_operation_consume_time))
        if not redis_version.startswith('3'):
            vals.append(dict(index_id=2170268, value=last_to_now_change_in_bytes))
        vals.append(dict(index_id=2170269, value=last_to_now_in_seconds))

    result = conn.info("commandstats")
    metric_append(2170301, [dict(name=key, value=str(item["calls"])) for key, item in result.items()])
    metric_append(2170302, [dict(name=key, value=str(item["usec"])) for key, item in result.items()])
    metric_append(2170303, [dict(name=key, value=str(item["usec_per_call"])) for key, item in result.items()])
    sum_calls = sum_usec = 0
    for key, item in result.items():
        sum_calls += item["calls"]
        sum_usec += item["usec"]

    metric_append(2171005, sum_calls)
    metric_append(2171006, sum_usec)

    string_calls, string_usec = map_commands(string_commands)
    list_calls, list_usec = map_commands(list_commands)
    set_calls, set_usec = map_commands(set_commands)
    hash_calls, hash_usec = map_commands(hash_commands)
    sorted_set_calls, sorted_set_usec = map_commands(sorted_set_commands)
    sort_calls, sort_usec = map_commands(sort_commands)
    get_type_calls, get_type_usec = map_commands(get_type_commands)
    set_type_calls, set_type_usec = map_commands(set_type_commands)
    hyperloglog_calls, hyperloglog_usec = map_commands(hyperloglog_commands)
    geo_calls, geo_usec = map_commands(geo_commands)
    pub_sub_calls, pub_sub_usec = map_commands(pub_sub_commands)
    eval_calls, eval_usec = map_commands(eval_commands)
    expire_calls, expire_usec = map_commands(expire_commands)
    stream_calls, stream_usec = map_commands(stream_commands)

    metric_append(2172000, string_calls)
    metric_append(2172001, string_usec)
    metric_append(2172002, list_calls)
    metric_append(2172003, list_usec)
    metric_append(2172004, set_calls)
    metric_append(2172005, set_usec)
    metric_append(2172006, hash_calls)
    metric_append(2172007, hash_usec)
    metric_append(2172008, sorted_set_calls)
    metric_append(2172009, sorted_set_usec)
    metric_append(2172010, sort_calls)
    metric_append(2172011, sort_usec)
    metric_append(2172012, get_type_calls)
    metric_append(2172013, get_type_usec)
    metric_append(2172014, set_type_calls)
    metric_append(2172015, set_type_usec)
    metric_append(2172016, hyperloglog_calls)
    metric_append(2172017, hyperloglog_usec)
    metric_append(2172018, geo_calls)
    metric_append(2172019, geo_usec)
    metric_append(2172020, pub_sub_calls)
    metric_append(2172021, pub_sub_usec)
    metric_append(2172022, eval_calls)
    metric_append(2172023, eval_usec)
    metric_append(2172024, expire_calls)
    metric_append(2172025, expire_usec)
    metric_append(2172026, stream_calls)
    metric_append(2172027, stream_usec)

    if float(redis_version) > 3:
        cluster_enabled = conn.info("cluster")["cluster_enabled"]
        if cluster_enabled == 1:
            result = conn.cluster("info")
            vals_append(2170701, "cluster_state")
            vals_append(2170702, "cluster_slots_assigned")
            vals_append(2170703, "cluster_slots_ok")
            vals_append(2170704, "cluster_slots_pfail")
            vals_append(2170705, "cluster_slots_fail")
            vals_append(2170706, "cluster_known_nodes")
            vals_append(2170707, "cluster_size")
            vals_append(2170708, "cluster_current_epoch")
            vals_append(2170709, "cluster_my_epoch")
            vals_append(2170710, "cluster_stats_messages_ping_sent")
            vals_append(2170711, "cluster_stats_messages_pong_sent")
            vals_append(2170712, "cluster_stats_messages_sent")
            vals_append(2170713, "cluster_stats_messages_ping_received")
            vals_append(2170714, "cluster_stats_messages_pong_received")
            if result.get("cluster_stats_messages_fail_received", 0) != 0:
                vals_append(2170715, "cluster_stats_messages_fail_received")
            if result.get("cluster_stats_messages_auth", 0) != 0:
                vals_append(2170717, "cluster_stats_messages_auth-ack_received")
            vals_append(2170716, "cluster_stats_messages_received")

    result = conn.info("keyspace")
    key_count = 0
    for key, item in result.items():
        key_count += item["keys"]
    metric_append(2171004, key_count)

    slave_count = 0
    max_lag = 0
    result = conn.info("replication")
    if result["role"] == "master" and redis_mode != "standalone":
        slave_count = result["connected_slaves"]
    if slave_count > 0:
        for i in range(slave_count):
            slave_name = f'slave{i}'
            metric_append(2171009, [dict(name=slave_name, value=result[slave_name]["lag"])])
            max_lag = max(result[slave_name]["lag"], max_lag)
    metric_append(2171010, max_lag)

if __name__ == '__main__':
    conn = DBUtil.get_redis_env()
    if conn:
        metric_append(2170000, '连接成功')
        info_stats(conn)
    else:
        metric_append(2170000, "连接失败")
    msg = '{"results":' + json.dumps(vals) + '}'
    print(msg)

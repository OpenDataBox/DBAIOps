import os
import sys
import json
import time

sys.path.append('/usr/software/knowl')
import DBUtil
import TdsqlUtil
import JavaRsa

def get_metric(pg, tdsql, target_id, metric):
    mkey = ['rstate',
'status',
'oss_status',
'kpstatus',
'master_binlog_dir_used',
'master_cpu_usage',
'master_data_dir_available',
'master_data_dir_usage',
'master_io_usage',
'master_mem_available',
'master_mem_hit_rate',
'mysql_active_thread_count',
'mysql_master_switch',
'mysql_max_binlog_dir_available_usage',
'mysql_max_binlog_dir_usage',
'mysql_max_connect_usage',
'mysql_max_cpu_usage',
'mysql_max_data_dir_available_usage',
'mysql_max_data_dir_usage',
'mysql_max_io_usage',
'mysql_max_mem_available_usage',
'mysql_max_mem_hit_rate',
'mysql_max_mem_usage',
'mysql_max_process_fh_usage',
'mysql_max_request_delete',
'mysql_max_request_insert',
'mysql_max_request_replace',
'mysql_max_request_selectreplace',
'mysql_max_request_update',
'mysql_min_binlog_dir_available',
'mysql_min_slave_delay',
'mysql_slave_max_cpu_usage',
'mysql_sum_alive',
'mysql_sum_binlog_dir_available',
'mysql_sum_binlog_dir_total',
'mysql_sum_binlog_dir_used',
'mysql_sum_conn_active',
'mysql_sum_conn_max',
'mysql_sum_conn_total',
'mysql_sum_data_dir_available',
'mysql_sum_data_dir_total',
'mysql_sum_data_dir_used',
'mysql_sum_Innodb_buffer_pool_reads',
'mysql_sum_Innodb_buffer_pool_read_ahead',
'mysql_sum_Innodb_buffer_pool_read_requests',
'mysql_sum_Innodb_rows_deleted',
'mysql_sum_Innodb_rows_inserted',
'mysql_sum_Innodb_rows_read',
'mysql_sum_Innodb_rows_updated',
'mysql_sum_master_delay',
'mysql_sum_mem_available',
'mysql_sum_mem_total',
'mysql_sum_mem_used',
'mysql_sum_process_fh_used',
'mysql_sum_request_delete',
'mysql_sum_request_insert',
'mysql_sum_request_replace',
'mysql_sum_request_select',
'mysql_sum_request_selectreplace',
'mysql_sum_request_total',
'mysql_sum_request_update',
'mysql_sum_slave_delay',
'mysql_sum_slave_io_running',
'mysql_sum_slave_sql_running',
'mysql_sum_slave_sync',
'mysql_sum_slow_query',
'mysql_sum_Threads_connected',
'mysql_sum_thread_lock_time',
'noman_swcount',
'oss_cpu',
'oss_data_disk',
'oss_log_disk',
'oss_memory',
'proxy_sum_connect_count',
'proxy_sum_connect_max',
'proxy_sum_deny_sql',
'proxy_sum_join_read_bytes',
'proxy_sum_join_write_bytes',
'proxy_sum_number_of_started_tx',
'proxy_sum_number_of_started_xa_tx',
'proxy_sum_other_state_sql',
'proxy_sum_time_range_0',
'proxy_sum_time_range_1',
'proxy_sum_time_range_2',
'proxy_sum_time_range_3',
'proxy_sum_total_embedded_sql',
'proxy_sum_total_error_sql',
'proxy_sum_total_orig_sql',
'proxy_sum_total_read_bytes',
'proxy_sum_total_success_sql',
'proxy_sum_total_write_bytes',
'swcount',
'swcount_fail',
'swcount_uncomplete_maxdelay',
'ddljob_except',
'vip_except',
'ctime',
'mtime']
    ret,res = tdsql.getMetric(pg, target_id)
    if ret == 403:
        if mgt(pg, tdsql, target_id) == 0:
            ret,res = tdsql.getMetric(pg, target_id)
    if ret == 200:
        n = 0
        for row in res:
            try:
                id = mkey.index(row["mkey"])
            except:
                id = -1
            if id >= 0:
                id += 2610002
                metric.append(dict(index_id=str(id), value=str(row["mval"])))
                if id in [2610047,2610048,2610050] and row["mval"]:
                    n += int(row["mval"])
        metric.append(dict(index_id="2610100", value=str(n)))
    return ret

def mgt(pg, tdsql, target_id):
    params = ["cluster/get_list","monitor_data/fetch","cluster/get_capacity","cluster/get_instances","install/get_db_info"]
    sql = f"select cib_name,cib_value from p_normal_cib where target_id='{target_id}' and index_id=1000001 and cib_name in {tuple2(params)}"
    result = fetchAll(pg, sql)
    auths = {}
    if result.code == 0:
        for row in result.msg:
            auths[row[0]] = row[1]
    ret = tdsql.getAuths()
    if ret == 0:
        for h in params:
            if tdsql.auths.get(h):
                if auths.get(h) != tdsql.auths[h]:
                    if h in auths.keys():
                        sql = f"update p_normal_cib set cib_value='{tdsql.auths[h]}',record_time=now() where target_id='{target_id}' and cib_name='{h}' and index_id=1000001"
                    else:
                        sql = f"insert into p_normal_cib(target_id,index_id,cib_name,cib_value,record_time) values('{target_id}',1000001,'{h}','{tdsql.auths[h]}',now())"
                    try:
                        cur = pg.conn.cursor()
                        cur.execute(sql)
                        pg.conn.commit()
                    except:
                        pg.conn.rollback()
    return ret

if __name__ == '__main__':
    dbInfo = eval(sys.argv[1])
    host = dbInfo['target_ip']
    port = dbInfo['target_port']
    #usr = dbInfo['target_usr']
    key = dbInfo['authKey']
    cid = dbInfo['clusterKey']
    iid = dbInfo['instanceId']
    targetId, pg = DBUtil.get_pg_env(dbInfo,0)
    if pg.conn is None:
        print('无法连接本地数据库')
        sys.exit()
    ct = int(time.time())
    metric = []
    tdsql = TdsqlUtil.Tdsql(host, port, key, cid, iid)
    ret = get_metric(pg, tdsql, targetId, metric)
    if ret == 200:
        metric.append(dict(index_id="2610000", value="连接成功"))
    else:
        metric.append(dict(index_id="2610000", value="连接失败"))
    ct2 = time.time()
    metric.append(dict(index_id="1000101", value=str(int((ct2-ct)*1000))))
    print('{"results":' + json.dumps(metric, ensure_ascii=False) + '}')

import sys
from datetime import datetime
sys.path.append('/usr/software/knowl')
import json
import DBUtil

# coding=utf-8

global version
global uid

version = ""
uid = None


def cs(val, dt=False):
    if val is None:
        return ''
    else:
        if dt:
            return val.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return str(val)


def pg_metric(db, metric):
    sql = """
    select (EXTRACT('epoch' FROM now())::bigint - EXTRACT('epoch' FROM pg_postmaster_start_time())::bigint) 
    """
    cursor = DBUtil.getValue(db, sql)
    result = cursor.fetchone()
    metric.append(dict(index_id="2300001", value=cs(result[0])))
    sql_wal_size = "select setting from pg_settings where name='wal_segment_size'"
    cs_wal_size = DBUtil.getValue(db, sql_wal_size)
    rs_wal_size = cs_wal_size.fetchone()
    sql = "SELECT  pg_xlog_location_diff(pg_current_xlog_location(), '000/00000000')"
    cursor = DBUtil.getValue(db, sql)
    cur_lsn_byte = cursor.fetchone()
    metric.append(dict(index_id="2300002", value=cs(cur_lsn_byte[0])))
    sql = "select checkpoint_lsn from pg_control_checkpoint()"
    cursor = DBUtil.getValue(db, sql)
    chk_lsn_byte = cursor.fetchone()
    metric.append(dict(index_id="2300003", value=cs(chk_lsn_byte[0])))
    sql = "select txid_current()"
    cursor = DBUtil.getValue(db, sql)
    result = cursor.fetchone()
    metric.append(dict(index_id="2300005", value=cs(result[0])))
    sql = '''
        select checkpoints_timed,checkpoints_req,buffers_checkpoint, checkpoint_write_time,checkpoint_sync_time,buffers_alloc, 
        buffers_checkpoint,buffers_clean,buffers_backend,maxwritten_clean,buffers_backend_fsync from pg_stat_bgwriter
    '''
    cursor = DBUtil.getValue(db, sql)
    result = cursor.fetchone()
    metric.append(dict(index_id="2300027", value=cs(result[0])))
    metric.append(dict(index_id="2300028", value=cs(result[1])))
    metric.append(dict(index_id="2300029", value=cs(result[2])))
    metric.append(dict(index_id="2300030", value=cs(result[3])))
    metric.append(dict(index_id="2300031", value=cs(result[4])))
    metric.append(dict(index_id="2300032", value=cs(result[5])))
    metric.append(dict(index_id="2300033", value=cs(int(result[6]) + int(result[7] + int(result[8])))))
    metric.append(dict(index_id="2300034", value=cs(result[6])))
    metric.append(dict(index_id="2300035", value=cs(result[7])))
    metric.append(dict(index_id="2300036", value=cs(result[8])))
    metric.append(dict(index_id="2300038", value=cs(result[9])))
    metric.append(dict(index_id="2300039", value=cs(result[10])))

    sql = '''select count(*) from pg_stat_activity'''
    cursor = DBUtil.getValue(db, sql)
    result = cursor.fetchone()
    metric.append(dict(index_id="2300101", value=cs(result[0])))
    sql = """select count(*) from pg_stat_activity where state='active' and client_port IS NOT null"""
    cursor = DBUtil.getValue(db, sql)
    result = cursor.fetchone()
    metric.append(dict(index_id="2300102", value=cs(result[0])))
    sql = """select count(*) from pg_stat_activity where waiting"""
    cursor = DBUtil.getValue(db, sql)
    result = cursor.fetchone()
    metric.append(dict(index_id="2300103", value=cs(result[0])))
    sql = """select count(*) from pg_stat_activity where state='idle in transaction' """
    cursor = DBUtil.getValue(db, sql)
    result = cursor.fetchone()
    metric.append(dict(index_id="2300104", value=cs(result[0])))
    sql = """select count(*) from pg_stat_activity where now()-xact_start > interval '300 second'"""
    cursor = DBUtil.getValue(db, sql)
    result = cursor.fetchone()
    metric.append(dict(index_id="2300105", value=cs(result[0])))
    sql = """select coalesce(extract(epoch from (max(now()-xact_start))),0) from pg_stat_activity where xact_start is not null and client_port IS NOT null"""
    cursor = DBUtil.getValue(db, sql)
    result = cursor.fetchone()
    metric.append(dict(index_id="2300106", value=cs(result[0])))
    sql = """select count(*) from pg_prepared_xacts"""
    cursor = DBUtil.getValue(db, sql)
    result = cursor.fetchone()
    metric.append(dict(index_id="2300107", value=cs(result[0])))
    sql = """ select sum(blks_hit),sum(blks_read),sum(xact_commit),sum(xact_rollback),sum(deadlocks),sum(conflicts),sum(tup_fetched),sum(tup_returned),
        sum(tup_inserted),sum(tup_updated),sum(tup_deleted),sum(temp_files),sum(temp_bytes),sum(blk_read_time),sum(blk_write_time)
        from pg_stat_database"""
    cursor = DBUtil.getValue(db, sql)
    result = cursor.fetchone()
    metric.append(dict(index_id="2300011", value=cs(result[0])))
    metric.append(dict(index_id="2300012", value=cs(result[1])))
    metric.append(dict(index_id="2300013", value=cs(int(result[2]) + int(result[3]))))
    metric.append(dict(index_id="2300014", value=cs(result[2])))
    metric.append(dict(index_id="2300015", value=cs(result[3])))
    metric.append(dict(index_id="2300016", value=cs(result[4])))
    metric.append(dict(index_id="2300017", value=cs(result[5])))
    metric.append(dict(index_id="2300018", value=cs(result[6])))
    metric.append(dict(index_id="2300019", value=cs(result[7])))
    metric.append(dict(index_id="2300020", value=cs(result[8])))
    metric.append(dict(index_id="2300021", value=cs(result[9])))
    metric.append(dict(index_id="2300022", value=cs(result[10])))
    metric.append(dict(index_id="2300023", value=cs(result[11])))
    metric.append(dict(index_id="2300024", value=cs(result[12])))
    metric.append(dict(index_id="2300025", value=cs(result[13])))
    metric.append(dict(index_id="2300026", value=cs(result[14])))
    sql = """select count(*) from pg_locks where not granted"""
    cursor = DBUtil.getValue(db, sql)
    result = cursor.fetchone()
    metric.append(dict(index_id="2300143", value=cs(result[0])))
    sql = "select state,pg_xlog_location_diff(pg_current_xlog_location() ,receiver_flush_location)  flush_lag, pg_xlog_location_diff(pg_current_xlog_location(),receiver_replay_location) replay_lag from pg_stat_replication"
    cursor = DBUtil.getValue(db, sql)
    result = cursor.fetchone()
    if result is not None:
        metric.append(dict(index_id="2300147", value=cs(result[0])))
        metric.append(dict(index_id="2300148", value=cs(result[1])))
        metric.append(dict(index_id="2300149", value=cs(result[2])))
    else:
        metric.append(dict(index_id="2300147", value=""))
        metric.append(dict(index_id="2300148", value=""))
        metric.append(dict(index_id="2300149", value=""))
    sql = "select pg_xlog_location_diff(pg_current_xlog_location(),restart_lsn) from pg_replication_slots"
    cursor = DBUtil.getValue(db, sql)
    result = cursor.fetchone()
    if result is not None:
        metric.append(dict(index_id="2300150", value=cs(result[0])))
    else:
        metric.append(dict(index_id="2300150", value=""))

    # 从gaussdb 2.2开始新增了这个函数：计算 WAL 日志占用空间

    sql = "select sum(size) from pg_ls_waldir()"
    result = db.execute(sql)
    if result.code == 0:
        cursor = result.msg
        result = cursor.fetchone()
        wal_size = result[0]
        metric.append(dict(index_id="2300159", value=cs(wal_size)))


if __name__ == '__main__':
    metric = []
    cur_time = datetime.now()
    dbInfo = eval(sys.argv[1])
    db_name = dbInfo['target_inst']
    user = dbInfo['target_usr']
    password = dbInfo['target_pwd']
    host = dbInfo['target_ip']
    port = dbInfo['target_port']
    lat_time = datetime.now()
    diff_ms = (lat_time - cur_time).microseconds
    metric.append(dict(index_id="1000102", value=str(round(diff_ms/1000,0))))
    gs_conn = DBUtil.get_gaussdb_env(exflag=2)
    if gs_conn.conn:
        metric.append(dict(index_id="2300000", value="连接成功"))
        pg_metric(gs_conn, metric)
    else:
        metric.append(dict(index_id="2300000", value="连接失败"))
    lat_time2 = datetime.now()
    diff_ms2 = (lat_time2 - cur_time).microseconds
    metric.append(dict(index_id="1000101", value=str(round(diff_ms2/1000,0))))
    print('{"results":' + json.dumps(metric,ensure_ascii=False) + '}')

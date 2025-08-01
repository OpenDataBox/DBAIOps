import sys

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


def ver_cmp(ver1, ver2):
    v1 = ver1.split('.')
    v2 = ver2.split('.')
    for i in range(min(len(v1), len(v2))):
        if int(v1[i]) > int(v2[i]):
            return 2
        if int(v1[i]) < int(v2[i]):
            return -2
    t = len(v1) - len(v2)
    if t > 0:
        t = 1
    elif t < 0:
        t = -1
    return t


def lsn2byte(lsn, wal_size):
    lsn_high = lsn.split('/')[0]
    lsn_lower = lsn.split('/')[1]
    lsn_high_int = int(lsn_high, 16)
    if int(wal_size) == 2048:
        lsn_lower_fileno = int(lsn_lower[0:2], 16)
        lsn_lower_offset = int(lsn_lower[2:], 16)
    elif int(wal_size) == 8192:
        lsn_lower_fileno = int(lsn_lower[0:1], 16)
        lsn_lower_offset = int(lsn_lower[1:], 16)
    lsn_byte = lsn_high_int * pow(2, 32) + lsn_lower_fileno * int(wal_size) * 8 * 1024 * 1024 + lsn_lower_offset
    return lsn_byte


def sys_metric(db, metric):
    sql = """
select (EXTRACT('epoch' FROM now())::bigint - EXTRACT('epoch' FROM sys_postmaster_start_time())::bigint) 
    """
    cursor = DBUtil.getValue(db, sql)
    result = cursor.fetchone()
    metric.append(dict(index_id="2380001", value=cs(result[0])))
    sql_wal_size = """select setting from sys_settings where name='wal_segment_size' """
    cs_wal_size = DBUtil.getValue(db, sql_wal_size)
    rs_wal_size = cs_wal_size.fetchone()
    dbv = db.conn.server_version
    if str(dbv).startswith('10'):
        sql = "select sys_current_wal_lsn()"
    else:
        sql = "select sys_current_xlog_location()"
    cursor = DBUtil.getValue(db, sql)
    result = cursor.fetchone()
    cur_lsn_byte = lsn2byte(result[0], rs_wal_size[0])
    metric.append(dict(index_id="2380002", value=cs(cur_lsn_byte)))
    sql = "select checkpoint_location from sys_control_checkpoint()"
    cursor = DBUtil.getValue(db, sql)
    result = cursor.fetchone()
    chk_lsn_byte = lsn2byte(result[0], rs_wal_size[0])
    metric.append(dict(index_id="2380003", value=cs(chk_lsn_byte)))
    sql = "select txid_current()"
    cursor = DBUtil.getValue(db, sql)
    result = cursor.fetchone()
    metric.append(dict(index_id="2380005", value=cs(result[0])))
    sql = '''
select checkpoints_timed,checkpoints_req,buffers_checkpoint, checkpoint_write_time,checkpoint_sync_time,buffers_alloc, 
buffers_checkpoint,buffers_clean,buffers_backend,maxwritten_clean,buffers_backend_fsync from sys_stat_bgwriter
'''
    cursor = DBUtil.getValue(db, sql)
    result = cursor.fetchone()
    metric.append(dict(index_id="2380027", value=cs(result[0])))
    metric.append(dict(index_id="2380028", value=cs(result[1])))
    metric.append(dict(index_id="2380029", value=cs(result[2])))
    metric.append(dict(index_id="2380030", value=cs(result[3])))
    metric.append(dict(index_id="2380031", value=cs(result[4])))
    metric.append(dict(index_id="2380032", value=cs(result[5])))
    metric.append(dict(index_id="2380033", value=cs(int(result[6]) + int(result[7] + int(result[8])))))
    metric.append(dict(index_id="2380034", value=cs(result[6])))
    metric.append(dict(index_id="2380035", value=cs(result[7])))
    metric.append(dict(index_id="2380036", value=cs(result[8])))
    metric.append(dict(index_id="2380038", value=cs(result[9])))
    metric.append(dict(index_id="2380039", value=cs(result[10])))
    sql = '''select archived_count,failed_count,last_archived_wal from sys_stat_archiver'''
    cursor = DBUtil.getValue(db, sql)
    result = cursor.fetchone()
    metric.append(dict(index_id="2380040", value=cs(result[0])))
    metric.append(dict(index_id="2380041", value=cs(result[1])))
    arc_name = result[2]
    if not arc_name:
        arch_lsn = ""
    else:
        arch_lsn = int(arc_name[8:16], 16) * pow(2, 32) + (int(arc_name[16:], 16) + 1) * int(
            rs_wal_size[0]) * 1024 * 1024 * 8
    metric.append(dict(index_id="2380042", value=cs(arch_lsn)))
    sql = '''select count(*) from sys_stat_activity'''
    cursor = DBUtil.getValue(db, sql)
    result = cursor.fetchone()
    metric.append(dict(index_id="2380101", value=cs(result[0])))
    sql = """select count(*) from sys_stat_activity where state='active' """
    cursor = DBUtil.getValue(db, sql)
    result = cursor.fetchone()
    metric.append(dict(index_id="2380102", value=cs(result[0])))
    sql = """select count(*) from sys_stat_activity where wait_event_type is not null"""
    cursor = DBUtil.getValue(db, sql)
    result = cursor.fetchone()
    metric.append(dict(index_id="2380103", value=cs(result[0])))
    sql = """select count(*) from sys_stat_activity where state='idle in transaction' """
    cursor = DBUtil.getValue(db, sql)
    result = cursor.fetchone()
    metric.append(dict(index_id="2380104", value=cs(result[0])))
    sql = """select count(*) from sys_stat_activity where now()-xact_start > interval '600 second'"""
    cursor = DBUtil.getValue(db, sql)
    result = cursor.fetchone()
    metric.append(dict(index_id="2380105", value=cs(result[0])))
    sql = """select extract(epoch from (max(now()-xact_start))) from sys_stat_activity where xact_start is not null"""
    cursor = DBUtil.getValue(db, sql)
    result = cursor.fetchone()
    metric.append(dict(index_id="2380106", value=cs(result[0])))
    sql = """select count(*) from sys_prepared_xacts"""
    cursor = DBUtil.getValue(db, sql)
    result = cursor.fetchone()
    metric.append(dict(index_id="2380107", value=cs(result[0])))
    sql = """ select sum(blks_hit),sum(blks_read),sum(xact_commit),sum(xact_rollback),sum(deadlocks),sum(conflicts),sum(tup_fetched),sum(tup_returned),
sum(tup_inserted),sum(tup_updated),sum(tup_deleted),sum(temp_files),sum(temp_bytes),sum(blk_read_time),sum(blk_write_time)
from sys_stat_database"""
    cursor = DBUtil.getValue(db, sql)
    result = cursor.fetchone()
    metric.append(dict(index_id="2380011", value=cs(result[0])))
    metric.append(dict(index_id="2380012", value=cs(result[1])))
    metric.append(dict(index_id="2380013", value=cs(int(result[2]) + int(result[3]))))
    metric.append(dict(index_id="2380014", value=cs(result[2])))
    metric.append(dict(index_id="2380015", value=cs(result[3])))
    metric.append(dict(index_id="2380016", value=cs(result[4])))
    metric.append(dict(index_id="2380017", value=cs(result[5])))
    metric.append(dict(index_id="2380018", value=cs(result[6])))
    metric.append(dict(index_id="2380019", value=cs(result[7])))
    metric.append(dict(index_id="2380020", value=cs(result[8])))
    metric.append(dict(index_id="2380021", value=cs(result[9])))
    metric.append(dict(index_id="2380022", value=cs(result[10])))
    metric.append(dict(index_id="2380023", value=cs(result[11])))
    metric.append(dict(index_id="2380024", value=cs(result[12])))
    metric.append(dict(index_id="2380025", value=cs(result[13])))
    metric.append(dict(index_id="2380026", value=cs(result[14])))
    sql = """select count(*) from sys_locks"""
    cursor = DBUtil.getValue(db, sql)
    result = cursor.fetchone()
    metric.append(dict(index_id="2380143", value=cs(result[0])))
    sql = """select sys_notification_queue_usage()"""
    cursor = DBUtil.getValue(db, sql)
    result = cursor.fetchone()
    metric.append(dict(index_id="2380144", value=cs(result[0])))
    sql = """select state,sys_current_xlog_location() - flush_location flush_lag, 
sys_current_xlog_location() - replay_location replay_lag from sys_stat_replication"""
    cursor = DBUtil.getValue(db, sql)
    result = cursor.fetchone()
    if result is not None:
        metric.append(dict(index_id="2380147", value=cs(result[0])))
        metric.append(dict(index_id="2380148", value=cs(result[1])))
        metric.append(dict(index_id="2380149", value=cs(result[2])))
    else:
        metric.append(dict(index_id="2380147", value=""))
        metric.append(dict(index_id="2380148", value=""))
        metric.append(dict(index_id="2380149", value=""))
    sql = "select sys_xlog_location_diff(sys_current_xlog_location(),restart_lsn) from sys_replication_slots"
    cursor = DBUtil.getValue(db, sql)
    result = cursor.fetchone()
    if result is not None:
        metric.append(dict(index_id="2380150", value=cs(result[0])))
    else:
        metric.append(dict(index_id="2380150", value=""))


if __name__ == '__main__':
    pg = DBUtil.get_pg_env_target()
    conn = None
    metric = []
    if pg.conn:
        metric.append(dict(index_id="2380000", value="连接成功"))
        sys_metric(pg, metric)
    else:
        metric.append(dict(index_id="2380000", value="连接失败"))
    print('{"results":' + json.dumps(metric) + '}')

# coding=utf-8
import sys
from datetime import datetime
from collections import defaultdict
sys.path.append('/usr/software/knowl')
import json
import DBUtil
from DBAIOps_logger import Logger

log = Logger()

def cs(val, dt=False):
    if val is None:
        return ''
    else:
        if dt:
            return val.strftime('%Y-%m-%d %H:%M:%S')
        else:
            if isinstance(val, list):
                return val
            else:
                return str(val)


def get_dict(d_dict, item):
    value = d_dict.get(item)
    if value is None:
        value = 0
    return str(value)


def insert_if_not_exists(targetId, index_id, value):
    if targetId == 'ALL' and role == 'Primary':
        if cluster_type == 'distributed':
            sql2 = f"select node_host,node_port1 from pgxc_node where node_type in ('D','C')"
            cursor = DBUtil.getValue(gs_conn, sql2)
            result = cursor.fetchall()
            for item in result:
                host_ip = item[0]
                port = item[1]
                sql = f"select uid from mgt_system ms where ip = '{host_ip}' and port= '{port}' and use_flag and subuid is not null"
                cursor = DBUtil.getValue(pg, sql)
                result = cursor.fetchone()
                if result:
                    uid = result[0]
                    targetId = uid
                    if targetId[:4] == '2202':
                        index_type = '286'
                    else:
                        index_type = '230'
                    if global_metric:
                        is_exist = False
                        for item in global_metric:
                            if item["targetId"] == targetId:
                                is_exist = True
                                if str(index_id)[:3] == '100':
                                    index_type = '100'
                                elif str(index_id)[:3] == '300':
                                    index_type = '300'
                                item["results"].append({"index_id": index_type + str(str(index_id)[3:]), "value": cs(value)})
                                break # 找到了就退出
                        if not is_exist:
                            if str(index_id)[:3] == '100':
                                new_entry = {
                                    "targetId": targetId,
                                    "indexType": index_type,
                                    "results": [{"index_id": index_id, "value": cs(value)}]
                                }
                            elif str(index_id)[:3] == '300':
                                new_entry = {
                                    "targetId": targetId,
                                    "indexType": index_type,
                                    "results": [{"index_id": index_id, "value": cs(value)}]
                                }
                            else:
                                new_entry = {
                                    "targetId": targetId,
                                    "indexType": index_type,
                                    "results": [{"index_id": index_type + str(str(index_id)[3:]), "value": cs(value)}]
                                }
                            global_metric.append(new_entry)
                    else:
                        if str(index_id)[:3] == '100':
                            new_entry = {
                                "targetId": targetId,
                                "indexType": index_type,
                                "results": [{"index_id": index_id, "value": cs(value)}]
                            }
                        elif str(index_id)[:3] == '300':
                            new_entry = {
                                "targetId": targetId,
                                "indexType": index_type,
                                "results": [{"index_id": index_id, "value": cs(value)}]
                            }
                        else:
                            new_entry = {
                                "targetId": targetId,
                                "indexType": index_type,
                                "results": [{"index_id": index_type + str(str(index_id)[3:]), "value": cs(value)}]
                            }
                        global_metric.append(new_entry)
    else:       
        if targetId and role == 'Primary':
            if targetId[:4] == '2202':
                index_type = '286'
            else:
                index_type = '230'
            if global_metric:
                is_exist = False
                for item in global_metric:
                    if item["targetId"] == targetId:
                        is_exist = True
                        if str(index_id)[:3] == '100':
                            index_type = '100'
                        elif str(index_id)[:3] == '300':
                            index_type = '300'
                        item["results"].append({"index_id": index_type + str(str(index_id)[3:]), "value": cs(value)})
                        break # 找到了就退出
                if not is_exist:
                    if str(index_id)[:3] == '100':
                        new_entry = {
                            "targetId": targetId,
                            "indexType": index_type,
                            "results": [{"index_id": index_id, "value": cs(value)}]
                        }
                    elif str(index_id)[:3] == '300':
                        new_entry = {
                            "targetId": targetId,
                            "indexType": index_type,
                            "results": [{"index_id": index_id, "value": cs(value)}]
                        }
                    else:
                        new_entry = {
                            "targetId": targetId,
                            "indexType": index_type,
                            "results": [{"index_id": index_type + str(str(index_id)[3:]), "value": cs(value)}]
                        }
                    global_metric.append(new_entry)
            else:
                if str(index_id)[:3] == '100':
                    new_entry = {
                        "targetId": targetId,
                        "indexType": index_type,
                        "results": [{"index_id": index_id, "value": cs(value)}]
                    }
                elif str(index_id)[:3] == '300':
                    new_entry = {
                        "targetId": targetId,
                        "indexType": index_type,
                        "results": [{"index_id": index_id, "value": cs(value)}]
                    }
                else:
                    new_entry = {
                        "targetId": targetId,
                        "indexType": index_type,
                        "results": [{"index_id": index_type + str(str(index_id)[3:]), "value": cs(value)}]
                    }
                global_metric.append(new_entry)


def get_uid_by_nodename(pg, node_name, uids=None):
    if uids:
        return uids
    if cluster_type == 'distributed':
        sql2 = f"select node_host,node_port1 from pgxc_node where node_name='{node_name}' and node_type in ('D','C')"
        cursor = DBUtil.getValue(gs_conn, sql2)
        result = cursor.fetchone()
        host_ip = result[0]
        port = result[1]
        sql = f"select uid from mgt_system ms where ip = '{host_ip}' and port= '{port}' and use_flag and subuid is not null"
        cursor = DBUtil.getValue(pg, sql)
        result = cursor.fetchone()
        if result is not None:
            uid = result[0]
        else:
            uid = None
            log.error(f"get_uid_by_nodename: {node_name} not found,host_ip:{host_ip},port:{port}")
    else:
        uid = targetId
    return uid


def get_uid_by_ip(node_ip, port=None):
    if port:
        sql = f"select uid from mgt_system ms where ip = '{node_ip}' and port='{port}' and use_flag and subuid is not null"
    else:
        sql = f"select uid from mgt_system ms where ip = '{node_ip}' and uid like '2104%' and use_flag and subuid is not null"
    cursor = DBUtil.getValue(pg, sql)
    result = cursor.fetchone()
    uid = None
    if result is not None:
        uid = result[0]
    return uid


def get_indexid_by_desc(pg, uid, index_desc):
    "根据指标名称获取指标ID"
    if uid and uid[:4] == '2104':
        sql = f"select index_id from mon_index where description='{index_desc}' and index_type = 230"
    else:
        sql = f"select index_id from mon_index where description='{index_desc}' and index_type = 286"
    cursor = DBUtil.getValue(pg, sql)
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None


def pgxc_metric(pg, targetId, db, uids=None):
    # 运行时间
    sql = """
    SELECT EXTRACT(EPOCH FROM current_timestamp)::bigint
    """
    cursor = DBUtil.getValue(db, sql)
    result = cursor.fetchone()
    if uids:
        insert_if_not_exists(uids, 2860001, result[0])
    insert_if_not_exists(targetId, 2860001, result[0])
    insert_if_not_exists('ALL', 2860001, result[0])
    # 各个节点的总会话数，活跃会话数
    sql = "select coorname,count(*) from dbe_perf.global_session_stat_activity group by coorname"
    cursor = DBUtil.getValue(db, sql)
    result = cursor.fetchall()
    dn_total = defaultdict(int)
    cn_total = defaultdict(int)
    for row in result:
        node_name = row[0]
        uid2 = get_uid_by_nodename(pg, node_name, uids)
        if uid2:
            insert_if_not_exists(uid2, 2860101, row[1])
            insert_if_not_exists(targetId, 2860101, [dict(name=node_name,value=cs(row[1]))])
        if node_name[:2] == 'cn':
            cn_total[2860101] += row[1]
        elif node_name[:2] == 'dn':
            dn_total[2860101] += row[1]
    for index_id, value in dn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_dn_total',value=cs(value))])
            insert_if_not_exists(targetId, index_id, [dict(name='cluster',value=cs(value))])
    for index_id, value in cn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_cn_total',value=cs(value))])
            insert_if_not_exists(targetId, index_id, [dict(name='cluster',value=cs(value))])

    # 活跃会话
    sql = "select coorname,count(*) from dbe_perf.global_session_stat_activity where state='active' group by coorname"
    cursor = DBUtil.getValue(db, sql)
    result = cursor.fetchall()
    dn_total = defaultdict(int)
    cn_total = defaultdict(int)
    for row in result:
        node_name = row[0]
        uid = get_uid_by_nodename(pg, node_name, uids)
        if uid:
            insert_if_not_exists(uid, 2860102, row[1])
            insert_if_not_exists(targetId, 2860102, [dict(name=node_name,value=cs(row[1]))])
        if node_name[:2] == 'cn':
            cn_total[2860102] += row[1]
        elif node_name[:2] == 'dn':
            dn_total[2860102] += row[1]
    for index_id, value in dn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_dn_total',value=cs(value))])
            insert_if_not_exists(targetId, index_id, [dict(name='cluster',value=cs(value))])
    for index_id, value in cn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_cn_total',value=cs(value))])
            insert_if_not_exists(targetId, index_id, [dict(name='cluster',value=cs(value))])

    # 等待会话
    sql = "select coorname,count(*) from dbe_perf.global_session_stat_activity where waiting group by coorname"
    cursor = DBUtil.getValue(db, sql)
    result = cursor.fetchall()
    dn_total = defaultdict(int)
    cn_total = defaultdict(int)
    if result:
        for row in result:
            node_name = row[0]
            uid = get_uid_by_nodename(pg, node_name, uids)
            insert_if_not_exists(uid, 2860103, row[1])
            insert_if_not_exists(targetId, 2860103, [dict(name=node_name,value=cs(row[1]))])
            if node_name[:2] == 'cn':
                cn_total[2860103] += row[1]
            elif node_name[:2] == 'dn':
                dn_total[2860103] += row[1]
    else:
        insert_if_not_exists(targetId, 2860103, [dict(name='_total',value='0')])
    for index_id, value in dn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_dn_total',value=cs(value))])
    for index_id, value in cn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_cn_total',value=cs(value))])
    
    # 空事务
    sql = "select coorname,count(*) from dbe_perf.global_session_stat_activity where state='idle in transaction' group by coorname"
    cursor = DBUtil.getValue(db, sql)
    result = cursor.fetchall()
    dn_total = defaultdict(int)
    cn_total = defaultdict(int)
    if result:
        for row in result:
            node_name = row[0]
            uid = get_uid_by_nodename(pg, node_name, uids)
            insert_if_not_exists(uid, 2860104, row[1])
            insert_if_not_exists(targetId, 2860104, [dict(name=node_name,value=cs(row[1]))])
            if node_name[:2] == 'cn':
                cn_total[2860104] += row[1]
            elif node_name[:2] == 'dn':
                dn_total[2860104] += row[1]
    else:
        insert_if_not_exists(targetId, 2860104, [dict(name='_total',value='0')])
    for index_id, value in dn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_dn_total',value=cs(value))])
    for index_id, value in cn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_cn_total',value=cs(value))])

    # 长事务
    sql = "select coorname,count(*) from dbe_perf.global_session_stat_activity where now()-xact_start > interval '300 second' and client_addr is not null group by coorname"
    cursor = DBUtil.getValue(db, sql)
    result = cursor.fetchall()
    dn_total = defaultdict(int)
    cn_total = defaultdict(int)
    if result:
        for row in result:
            node_name = row[0]
            uid = get_uid_by_nodename(pg, node_name, uids)
            insert_if_not_exists(uid, 2860105, row[1])
            insert_if_not_exists(targetId, 2860105, [dict(name=node_name,value=cs(row[1]))])
            if node_name[:2] == 'cn':
                cn_total[2300105] += row[1]
            elif node_name[:2] == 'dn':
                dn_total[2300105] += row[1]
    else:
        insert_if_not_exists(targetId, 2860105, [dict(name='_total',value='0')])

    for index_id, value in dn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_dn_total',value=cs(value))])
    for index_id, value in cn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_cn_total',value=cs(value))])
    
    # 最长事务持续时间
    sql = "select coorname,coalesce(extract(epoch from (max(now()-xact_start))),0) from dbe_perf.global_session_stat_activity where xact_start is not null and client_addr is not null group by coorname"
    cursor = DBUtil.getValue(db, sql)
    result = cursor.fetchall()
    dn_total = []
    cn_total = []
    if result:
        for row in result:
            node_name = row[0]
            uid = get_uid_by_nodename(pg, node_name, uids)
            insert_if_not_exists(uid, 2300106, row[1])
            insert_if_not_exists(targetId, 2860106, [dict(name=node_name,value=cs(row[1]))])
            if node_name[:2] == 'cn':
                cn_total.append(row[1])
            elif node_name[:2] == 'dn':
                dn_total.append(row[1])
    else:
        insert_if_not_exists(targetId, 2860106, [dict(name='_total',value='0')])
    if dn_total:
        insert_if_not_exists(targetId, 2860106, [dict(name='_dn_max',value=cs(max(dn_total)))])
    if cn_total:
        insert_if_not_exists(targetId, 2860106, [dict(name='_cn_max',value=cs(max(cn_total)))])

    # 长查询
    sql = "select coorname,count(*) from dbe_perf.global_session_stat_activity where now()-query_start > interval '300 second' and client_addr is not null and state != 'idle' group by coorname"
    cursor = DBUtil.getValue(db, sql)
    result = cursor.fetchall()
    dn_total = defaultdict(int)
    cn_total = defaultdict(int)
    if result:
        for row in result:
            node_name = row[0]
            uid = get_uid_by_nodename(pg, node_name, uids)
            insert_if_not_exists(uid, 2860158, row[1])
            insert_if_not_exists(targetId, 2860158, [dict(name=node_name,value=cs(row[1]))])
            if node_name[:2] == 'cn':
                cn_total[2860158] += row[1]
            elif node_name[:2] == 'dn':
                dn_total[2860158] += row[1]
    else:
        insert_if_not_exists(targetId, 2860158, [dict(name='_total',value='0')])

    # OS_RUNTIME
    sql2 = "select node_name ,name, value from dbe_perf.GLOBAL_OS_RUNTIME"
    cursor = DBUtil.getValue(db, sql2)
    result = cursor.fetchall()
    # 如果node_name是cn_开头的，则把所有cn_开头的节点的数据加起来，如果是dn_开头的，则把所有dn_开头的节点的数据加起来
    dn_total = defaultdict(int)
    cn_total = defaultdict(int)
    for row in result:
        node_name = row[0]
        name = row[1]
        value = row[2]
        index_id = get_indexid_by_desc(pg, uid, name)
        if node_name[:2] == 'cn':
            cn_total[index_id] += row[2]
        elif node_name[:2] == 'dn':
            dn_total[index_id] += row[2]
        uid = get_uid_by_nodename(pg, node_name, uids)
        if index_id:
            insert_if_not_exists(uid, index_id, value)
            insert_if_not_exists(targetId, index_id, [dict(name=node_name,value=cs(value))])
    for index_id, value in dn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_dn_total',value=cs(value))])
    for index_id, value in cn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_cn_total',value=cs(value))])

    # INSTANCE_TIME
    sql3 = "select node_name ,stat_name, value from dbe_perf.GLOBAL_INSTANCE_TIME"
    cursor = DBUtil.getValue(db, sql3)
    result = cursor.fetchall()
    dn_total = defaultdict(int)
    cn_total = defaultdict(int)
    for row in result:
        node_name = row[0]
        uid = get_uid_by_nodename(pg, node_name, uids)
        stat_name = row[1]
        value = row[2]
        index_id = get_indexid_by_desc(pg, uid, stat_name)
        if node_name[:2] == 'cn':
            cn_total[index_id] += row[2]
        elif node_name[:2] == 'dn':
            dn_total[index_id] += row[2]
        if index_id:
            insert_if_not_exists(uid, index_id, value)
            insert_if_not_exists(targetId, index_id, [dict(name=node_name,value=cs(value))])
    for index_id, value in dn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_dn_total',value=cs(value))])
    for index_id, value in cn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_cn_total',value=cs(value))])
    
    # FILE_REDO_IOSTAT
    sql4 = "select * from dbe_perf.GLOBAL_FILE_REDO_IOSTAT"
    cursor = DBUtil.getValue(db, sql4)
    result = cursor.fetchall()
    dn_total = defaultdict(int)
    cn_total = defaultdict(int)
    for row in result:
        node_name = row[0]
        uid = get_uid_by_nodename(pg, node_name, uids)
        if node_name[:2] == 'cn':
            cn_total[2863030] += row[1]
            cn_total[2863031] += row[2]
            cn_total[2863032] += row[3]
            cn_total[2863033] += row[4]
            cn_total[2863034] += row[5]
            cn_total[2863035] += row[6]
        elif node_name[:2] == 'dn':
            dn_total[2863030] += row[1]
            dn_total[2863031] += row[2]
            dn_total[2863032] += row[3]
            dn_total[2863033] += row[4]
            dn_total[2863034] += row[5]
            dn_total[2863035] += row[6]
        insert_if_not_exists(uid, 2863030, row[1])
        insert_if_not_exists(uid, 2863031, row[2])
        insert_if_not_exists(uid, 2863032, row[3])
        insert_if_not_exists(uid, 2863033, row[4])
        insert_if_not_exists(uid, 2863034, row[5])
        insert_if_not_exists(uid, 2863035, row[6])
        insert_if_not_exists(targetId, 2863030, [dict(name=node_name,value=cs(row[1]))])
        insert_if_not_exists(targetId, 2863031, [dict(name=node_name,value=cs(row[2]))])
        insert_if_not_exists(targetId, 2863032, [dict(name=node_name,value=cs(row[3]))])
        insert_if_not_exists(targetId, 2863033, [dict(name=node_name,value=cs(row[4]))])
        insert_if_not_exists(targetId, 2863034, [dict(name=node_name,value=cs(row[5]))])
        insert_if_not_exists(targetId, 2863035, [dict(name=node_name,value=cs(row[6]))])
    for index_id, value in dn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_dn_total',value=cs(value))])
    for index_id, value in cn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_cn_total',value=cs(value))])

    # memory detail
    try:
        sql5 = "select nodename,memorytype,memorymbytes from dbe_perf.GLOBAL_MEMORY_NODE_DETAIL"
        result = db.execute(sql5)
        if result.code == 0:
            result = result.msg.fetchall()
            dn_total = defaultdict(int)
            cn_total = defaultdict(int)
            index_id = None
            for row in result:
                node_name = row[0]
                memorytype = row[1]
                memorymbytes = row[2]
                if memorytype == 'max_process_memory':
                    index_id = 2863227
                elif memorytype == 'process_used_memory':
                    index_id = 2863228
                elif memorytype == 'max_dynamic_memory':
                    index_id = 2863229
                elif memorytype == 'dynamic_used_memory':
                    index_id = 2863230
                elif memorytype == 'dynamic_peak_memory':
                    index_id = 2863231
                elif memorytype == 'dynamic_used_shrctx':
                    index_id = 2863232
                elif memorytype == 'dynamic_peak_shrctx':
                    index_id = 2863233
                elif memorytype == 'max_shared_memory':
                    index_id = 2863234
                elif memorytype == 'shared_used_memory':
                    index_id = 2863235
                elif memorytype == 'max_cstore_memory':
                    index_id = 2863236
                elif memorytype == 'cstore_used_memory':
                    index_id = 2863237
                elif memorytype == 'max_sctpcomm_memory':
                    index_id = 2863238
                elif memorytype == 'sctpcomm_used_memory':
                    index_id = 2863239
                elif memorytype == 'sctpcomm_peak_memory':
                    index_id = 2863240
                elif memorytype == 'other_used_memory':
                    index_id = 2863241
                elif memorytype == 'gpu_max_dynamic_memory':
                    index_id = 2863242
                elif memorytype == 'gpu_dynamic_used_memory':
                    index_id = 2863243
                elif memorytype == 'gpu_dynamic_peak_memory':
                    index_id = 2863244
                elif memorytype == 'pooler_conn_memory':
                    index_id = 2863245
                elif memorytype == 'pooler_freeconn_memory':
                    index_id = 2863246
                elif memorytype == 'storage_compress_memory':
                    index_id = 2863247
                elif memorytype == 'udf_reserved_memory':
                    index_id = 2863248
                if index_id:
                    if node_name[:2] == 'cn':
                        cn_total[index_id] += row[2]
                    elif node_name[:2] == 'dn':
                        dn_total[index_id] += row[2]
                    uid = get_uid_by_nodename(pg, node_name, uids)
                    insert_if_not_exists(uid, index_id, memorymbytes)
                    insert_if_not_exists(targetId, index_id, [dict(name=node_name,value=cs(memorymbytes))])
            for index_id, value in dn_total.items():
                if index_id:
                    insert_if_not_exists(targetId, index_id, [dict(name='_dn_total',value=cs(value))])
            for index_id, value in cn_total.items():
                if index_id:
                    insert_if_not_exists(targetId, index_id, [dict(name='_cn_total',value=cs(value))])
    except Exception as e:
        pass

    # rel_iostat
    sql5 = "select * from dbe_perf.GLOBAL_REL_IOSTAT"
    cursor = DBUtil.getValue(db, sql5)
    result = cursor.fetchall()
    dn_total = defaultdict(int)
    cn_total = defaultdict(int)
    for row in result:
        node_name = row[0]
        uid = get_uid_by_nodename(pg, node_name, uids)
        insert_if_not_exists(uid, 2863036, row[1])
        insert_if_not_exists(uid, 2863037, row[2])
        insert_if_not_exists(uid, 2863038, row[3])
        insert_if_not_exists(uid, 2863039, row[4])
        if node_name[:2] == 'cn':
            cn_total[2863036] += row[1]
            cn_total[2863037] += row[2]
            cn_total[2863038] += row[3]
            cn_total[2863039] += row[4]
        elif node_name[:2] == 'dn':
            dn_total[2863036] += row[1]
            dn_total[2863037] += row[2]
            dn_total[2863038] += row[3]
            dn_total[2863039] += row[4]
        insert_if_not_exists(targetId, 2863036, [dict(name=node_name,value=cs(row[1]))])
        insert_if_not_exists(targetId, 2863037, [dict(name=node_name,value=cs(row[2]))])
        insert_if_not_exists(targetId, 2863038, [dict(name=node_name,value=cs(row[3]))])
        insert_if_not_exists(targetId, 2863039, [dict(name=node_name,value=cs(row[4]))])
    for index_id, value in dn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_dn_total',value=cs(value))])
    for index_id, value in cn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_cn_total',value=cs(value))])

    # stat_database
    sql6 = """
    select node_name,sum(blks_hit),sum(blks_read),sum(xact_commit),sum(xact_rollback),sum(deadlocks),sum(conflicts),sum(tup_fetched),sum(tup_returned),
            sum(tup_inserted),sum(tup_updated),sum(tup_deleted),sum(temp_files),sum(temp_bytes),sum(blk_read_time),sum(blk_write_time)
            from dbe_perf.GLOBAL_STAT_DATABASE group by node_name
    """
    cursor = DBUtil.getValue(db, sql6)
    result = cursor.fetchall()
    dn_total = defaultdict(int)
    cn_total = defaultdict(int)
    for row in result:
        node_name = row[0]
        uid = get_uid_by_nodename(pg, node_name, uids)
        insert_if_not_exists(uid, "2860011", row[1])
        insert_if_not_exists(uid, "2860012", row[2])
        insert_if_not_exists(uid, "2860013", cs(int(row[3]) + int(row[4])))
        insert_if_not_exists(uid, "2860014", row[3])
        insert_if_not_exists(uid, "2860015", row[4])
        insert_if_not_exists(uid, "2860016", row[5])
        insert_if_not_exists(uid, "2860017", row[6])
        insert_if_not_exists(uid, "2860018", row[7])
        insert_if_not_exists(uid, "2860019", row[8])
        insert_if_not_exists(uid, "2860020", row[9])
        insert_if_not_exists(uid, "2860021", row[10])
        insert_if_not_exists(uid, "2860022", row[11])
        insert_if_not_exists(uid, "2860023", row[12])
        insert_if_not_exists(uid, "2860024", row[13])
        insert_if_not_exists(uid, "2860025", row[14])
        insert_if_not_exists(uid, "2860026", row[15])
        if node_name[:2] == 'cn':
            cn_total["2860011"] += row[1]
            cn_total["2860012"] += row[2]
            cn_total["2860013"] += int(row[3]) + int(row[4])
            cn_total["2860014"] += row[3]
            cn_total["2860015"] += row[4]
            cn_total["2860016"] += row[5]
            cn_total["2860017"] += row[6]
            cn_total["2860018"] += row[7]
            cn_total["2860019"] += row[8]
            cn_total["2860020"] += row[9]
            cn_total["2860021"] += row[10]
            cn_total["2860022"] += row[11]
            cn_total["2860023"] += row[12]
            cn_total["2860024"] += row[13]
            cn_total["2860025"] += row[14]
            cn_total["2860026"] += row[15]
            insert_if_not_exists(targetId, "2863294", [dict(name=node_name,value=cs(row[1]))])
            insert_if_not_exists(targetId, "2863295", [dict(name=node_name,value=cs(row[2]))])
        elif node_name[:2] == 'dn':
            dn_total["2860011"] += row[1]
            dn_total["2860012"] += row[2]
            dn_total["2860013"] += int(row[3]) + int(row[4])
            dn_total["2860014"] += row[3]
            dn_total["2860015"] += row[4]
            dn_total["2860016"] += row[5]
            dn_total["2860017"] += row[6]
            dn_total["2860018"] += row[7]
            dn_total["2860019"] += row[8]
            dn_total["2860020"] += row[9]
            dn_total["2860021"] += row[10]
            dn_total["2860022"] += row[11]
            dn_total["2860023"] += row[12]
            dn_total["2860024"] += row[13]
            dn_total["2860025"] += row[14]
            dn_total["2860026"] += row[15]
            insert_if_not_exists(targetId, "2860011", [dict(name=node_name,value=cs(row[1]))])
            insert_if_not_exists(targetId, "2860012", [dict(name=node_name,value=cs(row[2]))])
        insert_if_not_exists(targetId, "2860013", [dict(name=node_name,value=cs(int(row[3]) + int(row[4])))])
        insert_if_not_exists(targetId, "2860014", [dict(name=node_name,value=cs(row[3]))])
        insert_if_not_exists(targetId, "2860015", [dict(name=node_name,value=cs(row[4]))])
        insert_if_not_exists(targetId, "2860016", [dict(name=node_name,value=cs(row[5]))])
        insert_if_not_exists(targetId, "2860017", [dict(name=node_name,value=cs(row[6]))])
        insert_if_not_exists(targetId, "2860018", [dict(name=node_name,value=cs(row[7]))])
        insert_if_not_exists(targetId, "2860019", [dict(name=node_name,value=cs(row[8]))])
        insert_if_not_exists(targetId, "2860020", [dict(name=node_name,value=cs(row[9]))])
        insert_if_not_exists(targetId, "2860021", [dict(name=node_name,value=cs(row[10]))])
        insert_if_not_exists(targetId, "2860022", [dict(name=node_name,value=cs(row[11]))])
        insert_if_not_exists(targetId, "2860023", [dict(name=node_name,value=cs(row[12]))])
        insert_if_not_exists(targetId, "2860024", [dict(name=node_name,value=cs(row[13]))])
        insert_if_not_exists(targetId, "2860025", [dict(name=node_name,value=cs(row[14]))])
        insert_if_not_exists(targetId, "2860026", [dict(name=node_name,value=cs(row[15]))])
    for index_id, value in dn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_dn_total',value=cs(value))])
    for index_id, value in cn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_cn_total',value=cs(value))])

    # workload_sql_count
    sql7 = "select node_name ,select_count ,update_count ,insert_count ,delete_count ,ddl_count ,dml_count ,dcl_count from dbe_perf.SUMMARY_WORKLOAD_SQL_COUNT"
    cursor = DBUtil.getValue(db, sql7)
    result = cursor.fetchall()
    dn_total = defaultdict(int)
    cn_total = defaultdict(int)
    for row in result:
        node_name = row[0]
        uid = get_uid_by_nodename(pg, node_name, uids)
        insert_if_not_exists(uid, 2863041, row[1])
        insert_if_not_exists(uid, 2863042, row[2])
        insert_if_not_exists(uid, 2863043, row[3])
        insert_if_not_exists(uid, 2863044, row[4])
        insert_if_not_exists(uid, 2863045, row[5])
        insert_if_not_exists(uid, 2863046, row[6])
        insert_if_not_exists(uid, 2863047, row[7])
        if node_name[:2] == 'cn':
            cn_total[2863041] += row[1]
            cn_total[2863042] += row[2]
            cn_total[2863043] += row[3]
            cn_total[2863044] += row[4]
            cn_total[2863045] += row[5]
            cn_total[2863046] += row[6]
            cn_total[2863047] += row[7]
        elif node_name[:2] == 'dn':
            dn_total[2863041] += row[1]
            dn_total[2863042] += row[2]
            dn_total[2863043] += row[3]
            dn_total[2863044] += row[4]
            dn_total[2863045] += row[5]
            dn_total[2863046] += row[6]
            dn_total[2863047] += row[7]
        insert_if_not_exists(targetId, 2863041, [dict(name=node_name,value=cs(row[1]))])
        insert_if_not_exists(targetId, 2863042, [dict(name=node_name,value=cs(row[2]))])
        insert_if_not_exists(targetId, 2863043, [dict(name=node_name,value=cs(row[3]))])
        insert_if_not_exists(targetId, 2863044, [dict(name=node_name,value=cs(row[4]))])
        insert_if_not_exists(targetId, 2863045, [dict(name=node_name,value=cs(row[5]))])
        insert_if_not_exists(targetId, 2863046, [dict(name=node_name,value=cs(row[6]))])
        insert_if_not_exists(targetId, 2863047, [dict(name=node_name,value=cs(row[7]))])
    for index_id, value in dn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_dn_total',value=cs(value))])
    for index_id, value in cn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_cn_total',value=cs(value))])

    # WORKLOAD_TRANSACTION
    sql8 = """
    select
        node_name ,
        commit_counter ,
        rollback_counter ,
        round(resp_min/1024,2) resp_min_ms ,
        round(resp_max/1024,2) resp_max_ms,
        round(resp_avg/1024,2) resp_avg_ms,
        round(resp_total/1024,2) resp_total_ms,
        bg_commit_counter ,
        bg_rollback_counter ,
        round(bg_resp_min/1024,2) bg_resp_min_ms,
        round(bg_resp_max/1024,2) bg_resp_max_ms,
        round(bg_resp_avg/1024,2) bg_resp_avg_ms,
        round(bg_resp_total/1024,2) bg_resp_total_ms
    from
        dbe_perf.GLOBAL_WORKLOAD_TRANSACTION
    """
    cursor = DBUtil.getValue(db, sql8)
    result = cursor.fetchall()
    dn_total = defaultdict(int)
    cn_total = defaultdict(int)
    for row in result:
        node_name = row[0]
        uid = get_uid_by_nodename(pg, node_name, uids)
        insert_if_not_exists(uid, 2863048, row[1])
        insert_if_not_exists(uid, 2863049, row[2])
        insert_if_not_exists(uid, 2863050, row[3])
        insert_if_not_exists(uid, 2863051, row[4])
        insert_if_not_exists(uid, 2863052, row[5])
        insert_if_not_exists(uid, 2863053, row[6])
        insert_if_not_exists(uid, 2863054, row[7])
        insert_if_not_exists(uid, 2863055, row[8])
        insert_if_not_exists(uid, 2863056, row[9])
        insert_if_not_exists(uid, 2863057, row[10])
        insert_if_not_exists(uid, 2863058, row[11])
        insert_if_not_exists(uid, 2863059, row[12])
        if node_name[:2] == 'cn':
            cn_total[2863048] += row[1]
            cn_total[2863049] += row[2]
            cn_total[2863050] += row[3]
            cn_total[2863051] += row[4]
            cn_total[2863052] += row[5]
            cn_total[2863053] += row[6]
            cn_total[2863054] += row[7]
            cn_total[2863055] += row[8]
            cn_total[2863056] += row[9]
            cn_total[2863057] += row[10]
            cn_total[2863058] += row[11]
            cn_total[2863059] += row[12]
        elif node_name[:2] == 'dn':
            dn_total[2863048] += row[1]
            dn_total[2863049] += row[2]
            dn_total[2863050] += row[3]
            dn_total[2863051] += row[4]
            dn_total[2863052] += row[5]
            dn_total[2863053] += row[6]
            dn_total[2863054] += row[7]
            dn_total[2863055] += row[8]
            dn_total[2863056] += row[9]
            dn_total[2863057] += row[10]
            dn_total[2863058] += row[11]
            dn_total[2863059] += row[12]
        insert_if_not_exists(targetId, 2863048, [dict(name=node_name,value=cs(row[1]))])
        insert_if_not_exists(targetId, 2863049, [dict(name=node_name,value=cs(row[2]))])
        insert_if_not_exists(targetId, 2863050, [dict(name=node_name,value=cs(row[3]))])
        insert_if_not_exists(targetId, 2863051, [dict(name=node_name,value=cs(row[4]))])
        insert_if_not_exists(targetId, 2863052, [dict(name=node_name,value=cs(row[5]))])
        insert_if_not_exists(targetId, 2863053, [dict(name=node_name,value=cs(row[6]))])
        insert_if_not_exists(targetId, 2863054, [dict(name=node_name,value=cs(row[7]))])
        insert_if_not_exists(targetId, 2863055, [dict(name=node_name,value=cs(row[8]))])
        insert_if_not_exists(targetId, 2863056, [dict(name=node_name,value=cs(row[9]))])
        insert_if_not_exists(targetId, 2863057, [dict(name=node_name,value=cs(row[10]))])
        insert_if_not_exists(targetId, 2863058, [dict(name=node_name,value=cs(row[11]))])
        insert_if_not_exists(targetId, 2863059, [dict(name=node_name,value=cs(row[12]))])
    for index_id, value in dn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_dn_total',value=cs(value))])
    for index_id, value in cn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_cn_total',value=cs(value))])

    # WORKLOAD_SQL_ELAPSE_TIME
    sql9 = """
    select node_name ,
        round(total_select_elapse/1024,2) total_select_elapse_ms,
        round(total_update_elapse/1024,2) total_update_elapse_ms,
        round(total_insert_elapse/1024,2) total_insert_elapse_ms,
        round(total_delete_elapse/1024,2) total_delete_elapse_ms
    from
        dbe_perf.SUMMARY_WORKLOAD_SQL_ELAPSE_TIME
    """
    cursor = DBUtil.getValue(db, sql9)
    result = cursor.fetchall()
    dn_total = defaultdict(int)
    cn_total = defaultdict(int)
    for row in result:
        vals = []
        vals2 = []
        vals3 = []
        vals4 = []
        node_name = row[0]
        uid = get_uid_by_nodename(pg, node_name, uids)
        insert_if_not_exists(uid, 2863060, row[1])
        insert_if_not_exists(uid, 2863061, row[2])
        insert_if_not_exists(uid, 2863062, row[3])
        insert_if_not_exists(uid, 2863063, row[4])
        if node_name[:2] == 'cn':
            cn_total[2863060] += row[1]
            cn_total[2863061] += row[2]
            cn_total[2863062] += row[3]
            cn_total[2863063] += row[4]
        elif node_name[:2] == 'dn':
            dn_total[2863060] += row[1]
            dn_total[2863061] += row[2]
            dn_total[2863062] += row[3]
            dn_total[2863063] += row[4]
        insert_if_not_exists(targetId, 2863060, [dict(name=node_name,value=cs(row[1]))])
        insert_if_not_exists(targetId, 2863061, [dict(name=node_name,value=cs(row[2]))])
        insert_if_not_exists(targetId, 2863062, [dict(name=node_name,value=cs(row[3]))])
        insert_if_not_exists(targetId, 2863063, [dict(name=node_name,value=cs(row[4]))])
    for index_id, value in dn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_dn_total',value=cs(value))])
    for index_id, value in cn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_cn_total',value=cs(value))])

    # database reboot
    sql10 = "select distinct node,timeline from dbe_perf.GLOBAL_TRANSACTIONS_RUNNING_XACTS"
    cursor = DBUtil.getValue(db, sql10)
    result = cursor.fetchall()
    for row in result:
        vals = []
        node_name = row[0]
        uid = get_uid_by_nodename(pg, node_name, uids)
        insert_if_not_exists(uid, 2863064, row[1])
        vals.append(dict(name=node_name,value=cs(row[1])))
        insert_if_not_exists(targetId, 2863064, vals)
    
    # soft/hard parse
    sql11 = """
    select
        node_name ,
        sum(n_hard_parse) total_hard_parse,
        sum(n_soft_parse) total_soft_parse
    from
        dbe_perf.SUMMARY_STATEMENT
    group by
        node_name
    """
    cursor = DBUtil.getValue(db, sql11)
    result = cursor.fetchall()
    dn_total = defaultdict(int)
    cn_total = defaultdict(int)
    for row in result:
        node_name = row[0]
        uid = get_uid_by_nodename(pg, node_name, uids)
        insert_if_not_exists(uid, 2863065, row[1])
        insert_if_not_exists(uid, 2863066, row[2])
        if node_name[:2] == 'cn':
            cn_total[2863065] += row[1]
            cn_total[2863066] += row[2]
        elif node_name[:2] == 'dn':
            dn_total[2863065] += row[1]
            dn_total[2863066] += row[2]
        insert_if_not_exists(targetId, 2863065, [dict(name=node_name,value=cs(row[1]))])
        insert_if_not_exists(targetId, 2863066, [dict(name=node_name,value=cs(row[2]))])
    for index_id, value in dn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_dn_total',value=cs(value))])
    for index_id, value in cn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_cn_total',value=cs(value))])

    # table io
    sql12 = """
    select
        node_name ,
        sum(heap_blks_read) total_heap_blks_read,
        sum(heap_blks_hit) total_heap_blks_hit,
        sum(idx_blks_read) total_idx_blks_read,
        sum(idx_blks_hit) total_idx_blks_hit,
        sum(toast_blks_read) total_toast_blks_read,
        sum(toast_blks_hit) total_toast_blks_hit,
        sum(tidx_blks_read) total_tidx_blks_read,
        sum(tidx_blks_hit) total_tidx_blks_hit
    from
        dbe_perf.GLOBAL_STATIO_ALL_TABLES
    group by
        node_name
    """
    cursor = DBUtil.getValue(db, sql12)
    result = cursor.fetchall()
    dn_total = defaultdict(int)
    cn_total = defaultdict(int)
    for row in result:
        node_name = row[0]
        uid = get_uid_by_nodename(pg, node_name, uids)
        if node_name[:2] == 'cn':
            cn_total[2863278] += row[1]
            cn_total[2863279] += row[2]
            cn_total[2863280] += row[3]
            cn_total[2863281] += row[4]
            cn_total[2863282] += row[5]
            cn_total[2863283] += row[6]
            cn_total[2863284] += row[7]
            cn_total[2863285] += row[8]
            insert_if_not_exists(uid, 2863278, row[1])
            insert_if_not_exists(uid, 2863279, row[2])
            insert_if_not_exists(uid, 2863280, row[3])
            insert_if_not_exists(uid, 2863281, row[4])
            insert_if_not_exists(uid, 2863282, row[5])
            insert_if_not_exists(uid, 2863283, row[6])
            insert_if_not_exists(uid, 2863284, row[7])
            insert_if_not_exists(uid, 2863285, row[8])
            insert_if_not_exists(targetId, 2863278, [dict(name=node_name,value=cs(row[1]))])
            insert_if_not_exists(targetId, 2863279, [dict(name=node_name,value=cs(row[2]))])
            insert_if_not_exists(targetId, 2863280, [dict(name=node_name,value=cs(row[3]))])
            insert_if_not_exists(targetId, 2863281, [dict(name=node_name,value=cs(row[4]))])
            insert_if_not_exists(targetId, 2863282, [dict(name=node_name,value=cs(row[5]))])
            insert_if_not_exists(targetId, 2863283, [dict(name=node_name,value=cs(row[6]))])
            insert_if_not_exists(targetId, 2863284, [dict(name=node_name,value=cs(row[7]))])
            insert_if_not_exists(targetId, 2863285, [dict(name=node_name,value=cs(row[8]))])
        elif node_name[:2] == 'dn':
            dn_total[2863067] += row[1]
            dn_total[2863068] += row[2]
            dn_total[2863069] += row[3]
            dn_total[2863070] += row[4]
            dn_total[2863071] += row[5]
            dn_total[2863072] += row[6]
            dn_total[2863073] += row[7]
            dn_total[2863074] += row[8]
            insert_if_not_exists(uid, 2863067, row[1])
            insert_if_not_exists(uid, 2863068, row[2])
            insert_if_not_exists(uid, 2863069, row[3])
            insert_if_not_exists(uid, 2863070, row[4])
            insert_if_not_exists(uid, 2863071, row[5])
            insert_if_not_exists(uid, 2863072, row[6])
            insert_if_not_exists(uid, 2863073, row[7])
            insert_if_not_exists(uid, 2863074, row[8])
            insert_if_not_exists(targetId, 2863067, [dict(name=node_name,value=cs(row[1]))])
            insert_if_not_exists(targetId, 2863068, [dict(name=node_name,value=cs(row[2]))])
            insert_if_not_exists(targetId, 2863069, [dict(name=node_name,value=cs(row[3]))])
            insert_if_not_exists(targetId, 2863070, [dict(name=node_name,value=cs(row[4]))])
            insert_if_not_exists(targetId, 2863071, [dict(name=node_name,value=cs(row[5]))])
            insert_if_not_exists(targetId, 2863072, [dict(name=node_name,value=cs(row[6]))])
            insert_if_not_exists(targetId, 2863073, [dict(name=node_name,value=cs(row[7]))])
            insert_if_not_exists(targetId, 2863074, [dict(name=node_name,value=cs(row[8]))])
    for index_id, value in dn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_dn_total',value=cs(value))])
    for index_id, value in cn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_cn_total',value=cs(value))])
    
    #index io
    sql12 = """
    select
        node_name,
        sum(idx_blks_read),
        sum(idx_blks_hit)
    from
        dbe_perf.GLOBAL_STATIO_ALL_INDEXES
    group by
        node_name
    """
    cursor = DBUtil.getValue(db, sql12)
    result = cursor.fetchall()
    dn_total = defaultdict(int)
    cn_total = defaultdict(int)
    for row in result:
        node_name = row[0]
        uid = get_uid_by_nodename(pg, node_name, uids)
        insert_if_not_exists(uid, 2863201, row[1])
        insert_if_not_exists(uid, 2863202, row[2])
        if node_name[:2] == 'cn':
            cn_total[2863201] += row[1]
            cn_total[2863202] += row[2]
        elif node_name[:2] == 'dn':
            dn_total[2863201] += row[1]
            dn_total[2863202] += row[2]
        insert_if_not_exists(targetId, 2863201, [dict(name=node_name,value=cs(row[1]))])
        insert_if_not_exists(targetId, 2863202, [dict(name=node_name,value=cs(row[2]))])
    for index_id, value in dn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_dn_total',value=cs(value))])
    for index_id, value in cn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_cn_total',value=cs(value))])

    # sequence io
    sql12 = """
    select
        node_name,
        sum(blks_read),
        sum(blks_hit)
    from
        dbe_perf.GLOBAL_STATIO_ALL_SEQUENCES
    group by
        node_name
    """
    cursor = DBUtil.getValue(db, sql12)
    result = cursor.fetchall()
    dn_total = defaultdict(int)
    cn_total = defaultdict(int)
    for row in result:
        node_name = row[0]
        uid = get_uid_by_nodename(pg, node_name, uids)
        insert_if_not_exists(uid, 2863203, row[1])
        insert_if_not_exists(uid, 2863204, row[2])
        if node_name[:2] == 'cn':
            cn_total[2863203] += row[1]
            cn_total[2863204] += row[2]
        elif node_name[:2] == 'dn':
            dn_total[2863203] += row[1]
            dn_total[2863204] += row[2]
        insert_if_not_exists(targetId, 2863203, [dict(name=node_name,value=cs(row[1]))])
        insert_if_not_exists(targetId, 2863204, [dict(name=node_name,value=cs(row[2]))])
    for index_id, value in dn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_dn_total',value=cs(value))])
    for index_id, value in cn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_cn_total',value=cs(value))])

    # REPLICATION_STAT
    sql13 = """
    select
        node_name,
        state,
        pg_xlog_location_diff(sender_sent_location, receiver_write_location) send_write_lag,
        pg_xlog_location_diff(sender_sent_location,receiver_flush_location) send_flush_lag,
        pg_xlog_location_diff(sender_sent_location,receiver_replay_location) send_replay_lag,
        case sync_priority when 1 then 'sync' else 'async' end sync_priority
    from
        dbe_perf.GLOBAL_REPLICATION_STAT
        """
    cursor = DBUtil.getValue(db, sql13)
    result = cursor.fetchall()
    cluster_state = 'Streaming'
    write_lag = []
    flush_lag = []
    replay_lag = []
    if result:
        for row in result:
            node_name = row[0]
            uid = get_uid_by_nodename(pg, node_name, uids)
            state = row[1]
            send_write_lag = row[2]
            send_flush_lag = row[3]
            send_replay_lag = row[4]
            sync_priority = row[5]
            if state != 'streaming':
                cluster_state = state
            write_lag.append(send_write_lag)
            flush_lag.append(send_flush_lag)
            replay_lag.append(send_replay_lag)
            insert_if_not_exists(uid, 2860147, state)
            insert_if_not_exists(uid, 2863076, send_write_lag)
            insert_if_not_exists(uid, 2860148, send_flush_lag)
            insert_if_not_exists(uid, 2860149, send_replay_lag)
            insert_if_not_exists(uid, 2863079, sync_priority)
            insert_if_not_exists(targetId, 2860147, [dict(name=node_name,value=cs(state))])
            insert_if_not_exists(targetId, 2863076, [dict(name=node_name,value=cs(send_write_lag))])
            insert_if_not_exists(targetId, 2860148, [dict(name=node_name,value=cs(send_flush_lag))])
            insert_if_not_exists(targetId, 2860149, [dict(name=node_name,value=cs(send_replay_lag))])
            insert_if_not_exists(targetId, 2863079, [dict(name=node_name,value=cs(sync_priority))])
        insert_if_not_exists(targetId, 2860147, [dict(name='cluster',value=cs(cluster_state))])
        insert_if_not_exists(targetId, 2863076, [dict(name='cluster',value=cs(max(write_lag)))])
        insert_if_not_exists(targetId, 2860148, [dict(name='cluster',value=cs(max(flush_lag)))])
        insert_if_not_exists(targetId, 2860149, [dict(name='cluster',value=cs(max(replay_lag)))])

    # bgwrite_stat
    sql14 = """
    select node_name,checkpoints_timed,checkpoints_req,buffers_checkpoint, checkpoint_write_time,checkpoint_sync_time,buffers_alloc, 
        buffers_checkpoint,buffers_clean,buffers_backend,maxwritten_clean,buffers_backend_fsync from dbe_perf.GLOBAL_BGWRITER_STAT
    """
    cursor = DBUtil.getValue(db, sql14)
    result = cursor.fetchall()
    dn_total = defaultdict(int)
    cn_total = defaultdict(int)
    for row in result:
        node_name = row[0]
        uid = get_uid_by_nodename(pg, node_name, uids)
        insert_if_not_exists(uid,"2860027", value=cs(row[1]))
        insert_if_not_exists(uid,"2860028", value=cs(row[2]))
        insert_if_not_exists(uid,"2860029", value=cs(row[3]))
        insert_if_not_exists(uid,"2860030", value=cs(row[4]))
        insert_if_not_exists(uid,"2860031", value=cs(row[5]))
        insert_if_not_exists(uid,"2860032", value=cs(row[6]))
        insert_if_not_exists(uid,"2860033", value=cs(int(row[7]) + int(row[8] + int(row[9]))))
        insert_if_not_exists(uid,"2860034", value=cs(row[7]))
        insert_if_not_exists(uid,"2860035", value=cs(row[8]))
        insert_if_not_exists(uid,"2860036", value=cs(row[9]))
        insert_if_not_exists(uid,"2860038", value=cs(row[10]))
        insert_if_not_exists(uid,"2860039", value=cs(row[11]))
        if node_name[:2] == 'cn':
            cn_total[2860027] += row[1]
            cn_total[2860028] += row[2]
            cn_total[2860029] += row[3]
            cn_total[2860030] += row[4]
            cn_total[2860031] += row[5]
            cn_total[2860032] += row[6]
            cn_total[2860033] += int(row[7]) + int(row[8] + int(row[9]))
            cn_total[2860034] += row[7]
            cn_total[2860035] += row[8]
            cn_total[2860036] += row[9]
            cn_total[2860038] += row[10]
            cn_total[2860039] += row[11]
        elif node_name[:2] == 'dn':
            dn_total[2860027] += row[1]
            dn_total[2860028] += row[2]
            dn_total[2860029] += row[3]
            dn_total[2860030] += row[4]
            dn_total[2860031] += row[5]
            dn_total[2860032] += row[6]
            dn_total[2860033] += int(row[7]) + int(row[8] + int(row[9]))
            dn_total[2860034] += row[7]
            dn_total[2860035] += row[8]
            dn_total[2860036] += row[9]
            dn_total[2860038] += row[10]
            dn_total[2860039] += row[11]
        insert_if_not_exists(targetId,"2860027", [dict(name=node_name,value=cs(row[1]))])
        insert_if_not_exists(targetId,"2860028", [dict(name=node_name,value=cs(row[2]))])
        insert_if_not_exists(targetId,"2860029", [dict(name=node_name,value=cs(row[3]))])
        insert_if_not_exists(targetId,"2860030", [dict(name=node_name,value=cs(row[4]))])
        insert_if_not_exists(targetId,"2860031", [dict(name=node_name,value=cs(row[5]))])
        insert_if_not_exists(targetId,"2860032", [dict(name=node_name,value=cs(row[6]))])
        insert_if_not_exists(targetId,"2860033", [dict(name=node_name,value=cs(int(row[7]) + int(row[8] + int(row[9]))))])
        insert_if_not_exists(targetId,"2860034", [dict(name=node_name,value=cs(row[7]))])
        insert_if_not_exists(targetId,"2860035", [dict(name=node_name,value=cs(row[8]))])
        insert_if_not_exists(targetId,"2860036", [dict(name=node_name,value=cs(row[9]))])
        insert_if_not_exists(targetId,"2860038", [dict(name=node_name,value=cs(row[10]))])
        insert_if_not_exists(targetId,"2860039", [dict(name=node_name,value=cs(row[11]))])
    for index_id, value in dn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_dn_total',value=cs(value))])
    for index_id, value in cn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_cn_total',value=cs(value))])

    # ckpt_status
    sql16 = "select * from dbe_perf.GLOBAL_CKPT_STATUS"
    cursor = DBUtil.getValue(db, sql16)
    result = cursor.fetchall()
    dn_total = defaultdict(int)
    cn_total = defaultdict(int)
    for row in result:
        node_name = row[0]
        uid = get_uid_by_nodename(pg, node_name, uids)
        insert_if_not_exists(uid, 2863091, row[2])
        insert_if_not_exists(uid, 2863092, row[3])
        insert_if_not_exists(uid, 2863093, row[4])
        insert_if_not_exists(uid, 2863094, row[5])
        insert_if_not_exists(uid, 2863095, row[6])
        if node_name[:2] == 'cn':
            cn_total[2863091] += row[2]
            cn_total[2863092] += row[3]
            cn_total[2863093] += row[4]
            cn_total[2863094] += row[5]
            cn_total[2863095] += row[6]
        elif node_name[:2] == 'dn':
            dn_total[2863091] += row[2]
            dn_total[2863092] += row[3]
            dn_total[2863093] += row[4]
            dn_total[2863094] += row[5]
            dn_total[2863095] += row[6]
        insert_if_not_exists(targetId, 2863091, [dict(name=node_name,value=cs(row[2]))])
        insert_if_not_exists(targetId, 2863092, [dict(name=node_name,value=cs(row[3]))])
        insert_if_not_exists(targetId, 2863093, [dict(name=node_name,value=cs(row[4]))])
        insert_if_not_exists(targetId, 2863094, [dict(name=node_name,value=cs(row[5]))])
        insert_if_not_exists(targetId, 2863095, [dict(name=node_name,value=cs(row[6]))])
    for index_id, value in dn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_dn_total',value=cs(value))])
    for index_id, value in cn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_cn_total',value=cs(value))])

    # DOUBLE_WRITE_STATUS
    sql17 = """
        select
            node_name ,
            curr_start_page ,
            file_trunc_num ,
            file_reset_num ,
            total_writes ,
            low_threshold_writes ,
            high_threshold_writes ,
            total_pages ,
            low_threshold_pages ,
            high_threshold_pages
        from
            dbe_perf.GLOBAL_DOUBLE_WRITE_STATUS
    """
    cursor = DBUtil.getValue(db, sql17)
    result = cursor.fetchall()
    dn_total = defaultdict(int)
    cn_total = defaultdict(int)
    for row in result:
        node_name = row[0]
        uid = get_uid_by_nodename(pg, node_name, uids)
        insert_if_not_exists(uid, 2863096, row[1])
        insert_if_not_exists(uid, 2863097, row[2])
        insert_if_not_exists(uid, 2863098, row[3])
        insert_if_not_exists(uid, 2863099, row[4])
        insert_if_not_exists(uid, 2863100, row[5])
        insert_if_not_exists(uid, 2863101, row[6])
        insert_if_not_exists(uid, 2863102, row[7])
        insert_if_not_exists(uid, 2863103, row[8])
        if node_name[:2] == 'cn':
            cn_total[2863096] += row[1]
            cn_total[2863097] += row[2]
            cn_total[2863098] += row[3]
            cn_total[2863099] += row[4]
            cn_total[2863100] += row[5]
            cn_total[2863101] += row[6]
            cn_total[2863102] += row[7]
            cn_total[2863103] += row[8]
        elif node_name[:2] == 'dn':
            dn_total[2863096] += row[1]
            dn_total[2863097] += row[2]
            dn_total[2863098] += row[3]
            dn_total[2863099] += row[4]
            dn_total[2863100] += row[5]
            dn_total[2863101] += row[6]
            dn_total[2863102] += row[7]
            dn_total[2863103] += row[8]
        insert_if_not_exists(targetId, 2863096,  [dict(name=node_name,value=cs(row[1]))])
        insert_if_not_exists(targetId, 2863097,  [dict(name=node_name,value=cs(row[2]))])
        insert_if_not_exists(targetId, 2863098,  [dict(name=node_name,value=cs(row[3]))])
        insert_if_not_exists(targetId, 2863099,  [dict(name=node_name,value=cs(row[4]))])
        insert_if_not_exists(targetId, 2863100,  [dict(name=node_name,value=cs(row[5]))])
        insert_if_not_exists(targetId, 2863101,  [dict(name=node_name,value=cs(row[6]))])
        insert_if_not_exists(targetId, 2863102,  [dict(name=node_name,value=cs(row[7]))])
        insert_if_not_exists(targetId, 2863103,  [dict(name=node_name,value=cs(row[8]))])
    for index_id, value in dn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_dn_total',value=cs(value))])
    for index_id, value in cn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_cn_total',value=cs(value))])

    # pagewriter_status
    sql18 = "select node_name ,remain_dirty_page_num,pg_xlog_location_diff(ckpt_redo_point,'0/00000000'),pg_xlog_location_diff(current_xlog_insert_lsn,'0/00000000'),pgwr_actual_flush_total_num from dbe_perf.GLOBAL_PAGEWRITER_STATUS"
    cursor = DBUtil.getValue(db, sql18)
    result = cursor.fetchall()
    dn_total = defaultdict(int)
    cn_total = defaultdict(int)
    for row in result:
        node_name = row[0]
        uid = get_uid_by_nodename(pg, node_name, uids)    
        insert_if_not_exists(uid, 2863104, row[1])
        insert_if_not_exists(uid, 2860003, row[2])
        insert_if_not_exists(uid, 2860002, row[3])
        insert_if_not_exists(uid, 2863276, row[4]) 
        if node_name[:2] == 'cn':
            cn_total[2863104] += row[1]
            cn_total[2863276] += row[4]
        elif node_name[:2] == 'dn':
            dn_total[2863104] += row[1]
            dn_total[2863276] += row[4]
        insert_if_not_exists(targetId, 2863104, [dict(name=node_name,value=cs(row[1]))])
        insert_if_not_exists(targetId, 2860003, [dict(name=node_name,value=cs(row[2]))])
        insert_if_not_exists(targetId, 2860002, [dict(name=node_name,value=cs(row[3]))])
        insert_if_not_exists(targetId, 2863276, [dict(name=node_name,value=cs(row[4]))])
    for index_id, value in dn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_dn_total',value=cs(value))])
    for index_id, value in cn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_cn_total',value=cs(value))])
    
    # record_reset_time
    sql19 = "select node_name ,reset_time from dbe_perf.GLOBAL_RECORD_RESET_TIME"
    cursor = DBUtil.getValue(db, sql19)
    result = cursor.fetchall()
    for row in result:
        node_name = row[0]
        uid = get_uid_by_nodename(pg, node_name, uids)    
        insert_if_not_exists(uid, 2863105, row[1])
        insert_if_not_exists(targetId, 2863105, [dict(name=node_name,value=cs(row[1]))])

    # locks，等待锁数，2860143
    sql20 = "select node_name,count(*) from dbe_perf.GLOBAL_LOCKS where not granted group by node_name"
    cursor = DBUtil.getValue(db, sql20)
    result = cursor.fetchall()
    dn_total = defaultdict(int)
    cn_total = defaultdict(int)
    cn_total[2860143] = 0
    dn_total[2860143] = 0
    for row in result:
        node_name = row[0]
        uid = get_uid_by_nodename(pg, node_name, uids)    
        if node_name[:2] == 'cn':
            cn_total[2860143] += row[1]
        elif node_name[:2] == 'dn':
            dn_total[2860143] += row[1]
        insert_if_not_exists(uid, 2860143, row[1])
        insert_if_not_exists(targetId, 2860143, [dict(name=node_name,value=cs(row[1]))])
    for index_id, value in dn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_dn_total',value=cs(value))])
    for index_id, value in cn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_cn_total',value=cs(value))])

    # 非活跃复制槽
    sql21 = "select node_name ,count(*) from dbe_perf.GLOBAL_REPLICATION_SLOTS where not active group by node_name"
    cursor = DBUtil.getValue(db, sql21)
    result = cursor.fetchall()
    dn_total = defaultdict(int)
    cn_total = defaultdict(int)
    for row in result:
        node_name = row[0]
        uid = get_uid_by_nodename(pg, node_name, uids)    
        if node_name[:2] == 'cn':
            cn_total[2863205] += row[1]
        elif node_name[:2] == 'dn':
            dn_total[2863205] += row[1]
        insert_if_not_exists(uid, 2863205, row[1])
        insert_if_not_exists(targetId, 2863205, [dict(name=node_name,value=cs(row[1]))])
    for index_id, value in dn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_dn_total',value=cs(value))])
    for index_id, value in cn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_cn_total',value=cs(value))])

    # rto
    sql22 = "select node_name ,current_rto from dbe_perf.GLOBAL_RECOVERY_STATUS"
    cursor = DBUtil.getValue(db, sql22)
    result = cursor.fetchall()
    max_rto = 0
    for row in result:
        node_name = row[0]
        rto_info = row[1]
        if rto_info > max_rto:
            max_rto = rto_info
        uid = get_uid_by_nodename(pg, node_name, uids)
        insert_if_not_exists(uid, 2863114, rto_info)
        insert_if_not_exists(targetId, 2863114, [dict(name=node_name,value=cs(rto_info))])
    insert_if_not_exists(targetId, 2863114, [dict(name='_dn_max',value=cs(max_rto))])


    # statement response time
    sql23 = "select p80, p95 from dbe_perf.STATEMENT_RESPONSETIME_PERCENTILE"
    cursor = DBUtil.getValue(db, sql23)
    result = cursor.fetchall()
    for row in result:
        insert_if_not_exists(targetId, 2863207, cs(row[0]))
        insert_if_not_exists(targetId, 2863208, cs(row[1]))

    # threadpool status
    sql24 = "select node_name,worker_info from dbe_perf.GLOBAL_THREADPOOL_STATUS"
    cursor = DBUtil.getValue(db, sql24)
    result = cursor.fetchall()  # worker_info 返回结果：default:128 new:0 expect:128 actual:128 idle:127 pending:0
    cn_max_rate = 0
    dn_max_rate = 0
    node_info = {}
    for row in result:
        node_name = row[0]
        worker_info = row[1]
        node_info[node_name] = {'actual':0, 'idle':0, 'pending':0}
        for row in worker_info.strip().split('\n'):
            f_row = ' '.join(row.replace(": ",":").split()).split(' ')
            actual_thread = f_row[3].split(':')[1]
            idle = f_row[4].split(':')[1]
            pending = f_row[5].split(':')[1]
            node_info[node_name]['actual'] += int(actual_thread)
            node_info[node_name]['idle'] += int(idle)
            node_info[node_name]['pending'] += int(pending)
    for node_name, value in node_info.items():
        uid = get_uid_by_nodename(pg, node_name, uids)
        insert_if_not_exists(uid, 2863210, cs(value['pending']))
        insert_if_not_exists(targetId, 2863210, [dict(name=node_name,value=cs(value['pending']))])
        usage_rate = round((value['actual'] - value['idle'] - value['pending']) / value['actual'], 2) * 100
        insert_if_not_exists(uid, 2863209, cs(usage_rate))
        insert_if_not_exists(targetId, 2863209, [dict(name=node_name,value=cs(usage_rate))])
        if node_name[:2] == 'cn':
            cn_max_rate = max(cn_max_rate, usage_rate)
        elif node_name[:2] == 'dn':
            dn_max_rate = max(dn_max_rate, usage_rate)
    insert_if_not_exists(targetId, 2863209, [dict(name='_cn_max',value=cs(cn_max_rate))])
    insert_if_not_exists(targetId, 2863209, [dict(name='_dn_max',value=cs(dn_max_rate))])


    # file iostat
    sql25 = """
    select
        node_name,
        sum(phyrds) ,
        sum(phywrts) ,
        sum(phyblkrd) ,
        sum(phyblkwrt),
        sum(readtim) ,
        sum(writetim)
    from
        dbe_perf.GLOBAL_FILE_IOSTAT
    group by
        node_name
    """
    cursor = DBUtil.getValue(db, sql25)
    result = cursor.fetchall()
    dn_total = defaultdict(int)
    cn_total = defaultdict(int)
    for row in result:
        node_name = row[0]
        uid = get_uid_by_nodename(pg, node_name, uids)
        insert_if_not_exists(uid, 2863215, row[1])
        insert_if_not_exists(uid, 2863216, row[2])
        insert_if_not_exists(uid, 2863217, row[3])
        insert_if_not_exists(uid, 2863218, row[4])
        insert_if_not_exists(uid, 2863219, row[5])
        insert_if_not_exists(uid, 2863220, row[6])
        if node_name[:2] == 'cn':
            cn_total[2863215] += row[1]
            cn_total[2863216] += row[2]
            cn_total[2863217] += row[3]
            cn_total[2863218] += row[4]
            cn_total[2863219] += row[5]
            cn_total[2863220] += row[6]
        elif node_name[:2] == 'dn':
            dn_total[2863215] += row[1]
            dn_total[2863216] += row[2]
            dn_total[2863217] += row[3]
            dn_total[2863218] += row[4]
            dn_total[2863219] += row[5]
            dn_total[2863220] += row[6]
        insert_if_not_exists(targetId, 2863215, [dict(name=node_name,value=cs(row[1]))])
        insert_if_not_exists(targetId, 2863216, [dict(name=node_name,value=cs(row[2]))])
        insert_if_not_exists(targetId, 2863217, [dict(name=node_name,value=cs(row[3]))])
        insert_if_not_exists(targetId, 2863218, [dict(name=node_name,value=cs(row[4]))])
        insert_if_not_exists(targetId, 2863219, [dict(name=node_name,value=cs(row[5]))])
        insert_if_not_exists(targetId, 2863220, [dict(name=node_name,value=cs(row[6]))])
    for index_id, value in dn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_dn_total',value=cs(value))])
    for index_id, value in cn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_cn_total',value=cs(value))])

    # login logout
    sql27 = "select node_name ,sum(login_counter),sum(logout_counter) from dbe_perf.SUMMARY_USER_LOGIN group by node_name "
    cursor = DBUtil.getValue(db, sql27)
    result = cursor.fetchall()
    dn_total = defaultdict(int)
    cn_total = defaultdict(int)
    for row in result:
        node_name = row[0]
        uid = get_uid_by_nodename(pg, node_name, uids)
        insert_if_not_exists(uid, 2863115, row[1])
        insert_if_not_exists(uid, 2863116, row[2])
        if node_name[:2] == 'cn':
            cn_total[2863115] += row[1]
            cn_total[2863116] += row[2]
        elif node_name[:2] == 'dn':
            dn_total[2863115] += row[1]
            dn_total[2863116] += row[2]
        insert_if_not_exists(targetId, 2863115, [dict(name=node_name,value=cs(row[1]))])
        insert_if_not_exists(targetId, 2863116, [dict(name=node_name,value=cs(row[2]))])
    for index_id, value in dn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_dn_total',value=cs(value))])
    for index_id, value in cn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_cn_total',value=cs(value))])

    # redo status
    sql28 = """
    select
        node_name ,
        read_ptr,
        last_replayed_read_ptr,
        recovery_done_ptr,
        read_xlog_io_counter,
        read_xlog_io_total_dur,
        read_data_io_counter,
        read_data_io_total_dur,
        write_data_io_counter,
        write_data_io_total_dur,
        process_pending_counter,
        process_pending_total_dur,
        apply_counter,
        apply_total_dur,
        speed,
        primary_flush_ptr
    from
        dbe_perf.GLOBAL_REDO_STATUS
    """
    cursor = DBUtil.getValue(db, sql28)
    result = cursor.fetchall()
    dn_total = defaultdict(int)
    cn_total = defaultdict(int)
    for row in result:
        # index_id 从2863254开始
        node_name = row[0]
        uid = get_uid_by_nodename(pg, node_name, uids)
        insert_if_not_exists(uid, 2863254, row[1])
        insert_if_not_exists(uid, 2863255, row[2])
        insert_if_not_exists(uid, 2863256, row[3])
        insert_if_not_exists(uid, 2863257, row[4])
        insert_if_not_exists(uid, 2863258, row[5])
        insert_if_not_exists(uid, 2863259, row[6])
        insert_if_not_exists(uid, 2863260, row[7])
        insert_if_not_exists(uid, 2863261, row[8])
        insert_if_not_exists(uid, 2863262, row[9])
        insert_if_not_exists(uid, 2863263, row[10])
        insert_if_not_exists(uid, 2863264, row[11])
        insert_if_not_exists(uid, 2863265, row[12])
        if node_name[:2] == 'cn':
            cn_total[2863254] += row[1]
            cn_total[2863255] += row[2]
            cn_total[2863256] += row[3]
            cn_total[2863257] += row[4]
            cn_total[2863258] += row[5]
            cn_total[2863259] += row[6]
            cn_total[2863260] += row[7]
            cn_total[2863261] += row[8]
            cn_total[2863262] += row[9]
            cn_total[2863263] += row[10]
            cn_total[2863264] += row[11]
            cn_total[2863265] += row[12]
        elif node_name[:2] == 'dn':
            dn_total[2863254] += row[1]
            dn_total[2863255] += row[2]
            dn_total[2863256] += row[3]
            dn_total[2863257] += row[4]
            dn_total[2863258] += row[5]
            dn_total[2863259] += row[6]
            dn_total[2863260] += row[7]
            dn_total[2863261] += row[8]
            dn_total[2863262] += row[9]
            dn_total[2863263] += row[10]
            dn_total[2863264] += row[11]
            dn_total[2863265] += row[12]
        insert_if_not_exists(targetId, 2863254, [dict(name=node_name,value=cs(row[1]))])
        insert_if_not_exists(targetId, 2863255, [dict(name=node_name,value=cs(row[2]))])
        insert_if_not_exists(targetId, 2863256, [dict(name=node_name,value=cs(row[3]))])
        insert_if_not_exists(targetId, 2863257, [dict(name=node_name,value=cs(row[4]))])
        insert_if_not_exists(targetId, 2863258, [dict(name=node_name,value=cs(row[5]))])
        insert_if_not_exists(targetId, 2863259, [dict(name=node_name,value=cs(row[6]))])
        insert_if_not_exists(targetId, 2863260, [dict(name=node_name,value=cs(row[7]))])
        insert_if_not_exists(targetId, 2863261, [dict(name=node_name,value=cs(row[8]))])
        insert_if_not_exists(targetId, 2863262, [dict(name=node_name,value=cs(row[9]))])
        insert_if_not_exists(targetId, 2863263, [dict(name=node_name,value=cs(row[10]))])
        insert_if_not_exists(targetId, 2863264, [dict(name=node_name,value=cs(row[11]))])
        insert_if_not_exists(targetId, 2863265, [dict(name=node_name,value=cs(row[12]))])
    for index_id, value in dn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_dn_total',value=cs(value))])
    for index_id, value in cn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_cn_total',value=cs(value))])

    # rto_and_rpo_stat
    sql29 = "select hadr_sender_node_name ,current_rto ,current_rpo  from dbe_perf.global_streaming_hadr_rto_and_rpo_stat"
    cursor = DBUtil.getValue(db, sql29)
    result = cursor.fetchall()
    for row in result:
        node_name = row[0]
        rto_info = row[1]
        rpo_info = row[2]
        uid = get_uid_by_nodename(pg, node_name, uids)
        insert_if_not_exists(uid, 2863305, rto_info)
        insert_if_not_exists(uid, 2863306, rpo_info)
        insert_if_not_exists(targetId, 2863305, [dict(name=node_name,value=cs(rto_info))])
        insert_if_not_exists(targetId, 2863306, [dict(name=node_name,value=cs(rpo_info))])

    # database conflicts
    sql30 = """
    select
        node_name ,
        sum(confl_tablespace),
        sum(confl_lock),
        sum(confl_snapshot),
        sum(confl_bufferpin),
        sum(confl_deadlock)
    from
        dbe_perf.GLOBAL_STAT_DATABASE_CONFLICTS
    group by
        node_name
    """
    cursor = DBUtil.getValue(db, sql30)
    result = cursor.fetchall()
    dn_total = defaultdict(int)
    cn_total = defaultdict(int)
    for row in result:
        node_name = row[0]
        uid = get_uid_by_nodename(pg, node_name, uids)
        insert_if_not_exists(uid, 2863307, row[1])
        insert_if_not_exists(uid, 2863308, row[2])
        insert_if_not_exists(uid, 2863309, row[3])
        insert_if_not_exists(uid, 2863310, row[4])
        insert_if_not_exists(uid, 2863311, row[5])
        if node_name[:2] == 'cn':
            cn_total[2863307] += row[1]
            cn_total[2863308] += row[2]
            cn_total[2863309] += row[3]
            cn_total[2863310] += row[4]
            cn_total[2863311] += row[5]
        elif node_name[:2] == 'dn':
            dn_total[2863307] += row[1]
            dn_total[2863308] += row[2]
            dn_total[2863309] += row[3]
            dn_total[2863310] += row[4]
            dn_total[2863311] += row[5]
        insert_if_not_exists(targetId, 2863307, [dict(name=node_name,value=cs(row[1]))])
        insert_if_not_exists(targetId, 2863308, [dict(name=node_name,value=cs(row[2]))])
        insert_if_not_exists(targetId, 2863309, [dict(name=node_name,value=cs(row[3]))])
        insert_if_not_exists(targetId, 2863310, [dict(name=node_name,value=cs(row[4]))])
        insert_if_not_exists(targetId, 2863311, [dict(name=node_name,value=cs(row[5]))])
    for index_id, value in dn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_dn_total',value=cs(value))])
    for index_id, value in cn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_cn_total',value=cs(value))])

    # seq scan
    sql31 = """
    select
        node_name ,
        sum(seq_scan),
        sum(seq_tup_read),
        sum(idx_scan),
        sum(idx_tup_fetch),
        sum(n_tup_hot_upd),
        sum(n_live_tup),
        sum(n_dead_tup),
        sum(vacuum_count),
        sum(autovacuum_count),
        sum(analyze_count),
        sum(autoanalyze_count)
    from
        dbe_perf.GLOBAL_STAT_ALL_TABLES
    group by
        node_name
    """
    cursor = DBUtil.getValue(db, sql31)
    result = cursor.fetchall()
    dn_total = defaultdict(int)
    cn_total = defaultdict(int)
    for row in result:
        node_name = row[0]
        uid = get_uid_by_nodename(pg, node_name, uids)
        insert_if_not_exists(uid, 2862514, row[1])
        insert_if_not_exists(uid, 2862515, row[2])
        insert_if_not_exists(uid, 2862516, row[3])
        insert_if_not_exists(uid, 2862517, row[4])
        insert_if_not_exists(uid, 2863329, row[5])
        insert_if_not_exists(uid, 2863330, row[6])
        insert_if_not_exists(uid, 2863331, row[7])
        insert_if_not_exists(uid, 2863332, row[8])
        insert_if_not_exists(uid, 2863333, row[9])
        insert_if_not_exists(uid, 2863334, row[10])
        insert_if_not_exists(uid, 2863335, row[11])
        if node_name[:2] == 'cn':
            cn_total[2862514] += row[1]
            cn_total[2862515] += row[2]
            cn_total[2862516] += row[3]
            cn_total[2862517] += row[4]
            cn_total[2863329] += row[5]
            cn_total[2863330] += row[6]
            cn_total[2863331] += row[7]
            cn_total[2863332] += row[8]
            cn_total[2863333] += row[9]
            cn_total[2863334] += row[10]
            cn_total[2863335] += row[11]
        elif node_name[:2] == 'dn':
            dn_total[2862514] += row[1]
            dn_total[2862515] += row[2]
            dn_total[2862516] += row[3]
            dn_total[2863329] += row[5]
            dn_total[2863330] += row[6]
            dn_total[2863331] += row[7]
            dn_total[2863332] += row[8]
            dn_total[2863333] += row[9]
            dn_total[2863334] += row[10]
            dn_total[2863335] += row[11]
        insert_if_not_exists(targetId, 2862514, [dict(name=node_name,value=cs(row[1]))])
        insert_if_not_exists(targetId, 2862515, [dict(name=node_name,value=cs(row[2]))])
        insert_if_not_exists(targetId, 2862516, [dict(name=node_name,value=cs(row[3]))])
        insert_if_not_exists(targetId, 2862517, [dict(name=node_name,value=cs(row[4]))])
        insert_if_not_exists(targetId, 2863329, [dict(name=node_name,value=cs(row[5]))])
        insert_if_not_exists(targetId, 2863330, [dict(name=node_name,value=cs(row[6]))])
        insert_if_not_exists(targetId, 2863331, [dict(name=node_name,value=cs(row[7]))])
        insert_if_not_exists(targetId, 2863332, [dict(name=node_name,value=cs(row[8]))])
        insert_if_not_exists(targetId, 2863333, [dict(name=node_name,value=cs(row[9]))])
        insert_if_not_exists(targetId, 2863334, [dict(name=node_name,value=cs(row[10]))])
        insert_if_not_exists(targetId, 2863335, [dict(name=node_name,value=cs(row[11]))])
    for index_id, value in dn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_dn_total',value=cs(value))])
    for index_id, value in cn_total.items():
        if index_id:
            insert_if_not_exists(targetId, index_id, [dict(name='_cn_total',value=cs(value))])

    # dead tuple
    sql32 = """
    select
        node_name ,
        count(*)
    from
        dbe_perf.GLOBAL_STAT_ALL_TABLES
    where
        (n_live_tup + n_dead_tup) > 100000
        and n_dead_tup /(n_live_tup + n_dead_tup) > 0.2
        and n_dead_tup > 0
    group by
        node_name
    """
    cursor = DBUtil.getValue(db, sql32)
    result = cursor.fetchall()
    dn_total = defaultdict(int)
    cn_total = defaultdict(int)
    if result:
        for row in result:
            node_name = row[0]
            uid = get_uid_by_nodename(pg, node_name, uids)
            insert_if_not_exists(uid, 2863341, row[1])
            if node_name[:2] == 'cn':
                cn_total[2863341] += row[1]
            elif node_name[:2] == 'dn':
                dn_total[2863341] += row[1]
        for index_id, value in dn_total.items():
            if index_id:
                insert_if_not_exists(targetId, index_id, [dict(name='_dn_total',value=cs(value))])
        for index_id, value in cn_total.items():
            if index_id:
                insert_if_not_exists(targetId, index_id, [dict(name='_cn_total',value=cs(value))])
        insert_if_not_exists(targetId, 2863341, [dict(name=node_name,value=cs(row[1]))])
    else:
        insert_if_not_exists(targetId, 2863341, [dict(name='_dn_total',value='0')])
        insert_if_not_exists(targetId, 2863341, '0')


def cluster_info(pg, target_ip, dcs):
    ostype, ssh, os_user = DBUtil.getsshinfo_user(pg, target_ip)
    if os_user == 'root':
        cmd = "su - $(ps -ef|grep gaussdb|grep gbase|awk 'NR <=1 {print$1}') -c 'gha_ctl monitor all -l %s'" % dcs
    else:
        cmd = "gha_ctl monitor all -l %s" % dcs
    result  = ssh.exec_cmd(cmd)
    if isinstance(result, tuple):
        insert_if_not_exists(targetId, index_id="2863108", value='Degraded')
        return
    # 逐行解析文本
    data = json.loads(result)

    # Cluster State
    server_info = data['server'][0]
    insert_if_not_exists(targetId, index_id="2863108", value=cs(server_info['state']))
    insert_if_not_exists(targetId, index_id="2863300", value=cs(server_info))
    # 对比组件状态和上次是否一致，不一致则表示发生了切换
    sql = f"select 1 from mon_indexdata mi where mi.uid = '{targetId}' and index_id = 2863108 and value='{server_info['state']}'"
    curs = DBUtil.getValue(pg, sql)
    rs = curs.fetchone()
    if rs and not rs[0]:
        insert_if_not_exists(targetId, index_id="2863322", value='1')
    else:
        insert_if_not_exists(targetId, index_id="2863322", value='0')
    if cluster_type == 'distributed':
        # Coordinator State
        coordinator_info = data['coordinator']
        vals4 = []
        failed_nodes = 0
        total_nodes = 0
        cn_flag = False
        cn_state = False
        for row in coordinator_info:
            node_ip = row['host']
            port = row['port']
            state = row['state']
            total_nodes += 1
            uid = get_uid_by_ip(node_ip, port)
            if state == 'running':
                insert_if_not_exists(uid, index_id="2860000", value='连接成功')
            else:
                failed_nodes += 1
                failed_info += f"CN-{node_ip}:{state}, "
                insert_if_not_exists(uid, index_id="2860000", value=cs(state))
            vals4.append(dict(name=cs(node_ip + ':' + port), value=cs(state)))
            # 对比组件状态和上次是否一致，不一致则表示发生了切换
            sql = f"select 1 from mon_indexdata mi where mi.uid = '{targetId}' and index_id = 2863109 and iname = '{node_ip}' and value='{state}'"
            curs = DBUtil.getValue(pg, sql)
            rs = curs.fetchone()
            if rs and not rs[0]:
                cn_flag = True
            # 记录当前状态，如果不是primary、standby则表示集群状态异常
            if state != 'running':
                cn_state = True
        if cn_state:  # (0:否，1：是)
            insert_if_not_exists(targetId, index_id="2863325", value='1')
        else:
            insert_if_not_exists(targetId, index_id="2863325", value='0')
        if cn_flag:  # (0:否，1：是)
            insert_if_not_exists(targetId, index_id="2863319", value='1')
        else:
            insert_if_not_exists(targetId, index_id="2863319", value='0')
        insert_if_not_exists(targetId, index_id="2863109", value=cs(vals4))
        insert_if_not_exists(targetId, index_id="2863302", value=cs(failed_nodes))
        insert_if_not_exists(targetId, index_id="2863425", value=cs(total_nodes))
        # GTM State
        gtm_info = data['gtm']
        vals5 = []
        failed_nodes = 0
        total_nodes = 0
        gtm_flag = False
        gtm_state = False
        for row in gtm_info:
            node_ip = row['host']
            port = row['port']
            role = row['role']
            conn_state = row['state']
            state = row['state']
            total_nodes += 1
            if conn_state != 'running':
                failed_nodes += 1
                failed_info += f"GTM-{node_ip}:{conn_state}, "
            vals5.append(dict(name=cs(node_ip + ':' + port), value=cs(conn_state)))
            # 对比组件状态和上次是否一致，不一致则表示发生了切换
            sql = f"select 1 from mon_indexdata mi where mi.uid = '{targetId}' and index_id = 2863110 and iname = '{node_ip}' and value='{state}'"
            curs = DBUtil.getValue(pg, sql)
            rs = curs.fetchone()
            if rs and not rs[0]:
                gtm_flag = True
            # 记录当前状态，如果不是primary、standby则表示集群状态异常
            if state != 'Sync':
                gtm_state = True
        if gtm_state:  # (0:否，1：是)
            insert_if_not_exists(targetId, index_id="2863327", value='1')
        else:
            insert_if_not_exists(targetId, index_id="2863327", value='0')
        if gtm_flag:  # (0:否，1：是)
            insert_if_not_exists(targetId, index_id="2863321", value='1')
        else:
            insert_if_not_exists(targetId, index_id="2863321", value='0')
        insert_if_not_exists(targetId, index_id="2863110", value=cs(vals5))
        insert_if_not_exists(targetId, index_id="2863303", value=cs(failed_nodes))
        insert_if_not_exists(targetId, index_id="2863427", value=cs(total_nodes))
    # Datanode State
    datanode_info = data['datanode']
    vals6 = []
    failed_nodes = 0
    total_nodes = 0
    dn_flag = False
    dn_state = False
    for row in datanode_info:
        for key, value in row.items():
            exist_primary = False
            for dn_r in value:  # 同一个组的datanode
                node_ip = dn_r['host']
                port = dn_r['port']
                role = dn_r['role']
                state = dn_r['state']
                total_nodes += 1
                uid = get_uid_by_ip(node_ip, port)
                if role == 'primary':
                    exist_primary = True
                    if state == 'running':
                        insert_if_not_exists(uid, index_id="2860000", value='连接成功')
                    else:
                        insert_if_not_exists(uid, index_id="2860000", value='连接失败')
                vals6.append(dict(name=cs(node_ip + ':' + port), value=cs(state)))
                # 记录当前状态，如果不是primary、standby则表示集群状态异常
                if state != 'running':
                    dn_state = True
                    failed_nodes += 1
                    failed_info += f"DN-{node_ip}:{port}:{state}, "
                # 对比组件状态和上次是否一致，不一致则表示发生了切换
                sql = f"select 1 from mon_indexdata mi where mi.uid = '{targetId}' and index_id = 2863111 and iname = '{node_ip}' and value='{state}'"
                curs = DBUtil.getValue(pg, sql)
                rs = curs.fetchone()
                if rs and not rs[0]:
                    dn_flag = True
            if not exist_primary:
                insert_if_not_exists(uid, index_id="2860000", value='连接失败')
    if dn_state:  # (0:否，1：是)
        insert_if_not_exists(targetId, index_id="2863326", value='1')
    else:
        insert_if_not_exists(targetId, index_id="2863326", value='0')
    if dn_flag:  # (0:否，1：是)
        insert_if_not_exists(targetId, index_id="2863320", value='1')
    else:
        insert_if_not_exists(targetId, index_id="2863320", value='0')
    insert_if_not_exists(targetId, index_id="2863111", value=cs(vals6))
    insert_if_not_exists(targetId, index_id="2863301", value=cs(failed_nodes))
    insert_if_not_exists(targetId, index_id="2863424", value=cs(total_nodes))
    if failed_info:
        failed_info = failed_info[:-1]
    insert_if_not_exists(targetId, index_id="2863434", value=cs(failed_info))
    return datanode_info


def wait_event(pg, db, uids=None):
    sql = """
    select
        type,
        event,
        wait,
        total_wait_time / 1000 as total_wait_time_ms,nodename
    from
        DBE_PERF.GLOBAL_WAIT_EVENTS
    where
        wait > 0
    order by
        type desc,
        event desc
    """
    event_class = {}
    event_info = {}
    event_class_time = {}
    event_info_time = {}
    cursor = DBUtil.getValue(db, sql)
    result = cursor.fetchall()
    if result:
        node_wait = {}
        node_wait_time = {}
        node_info_wait = {}
        node_info_wait_time = {}
        total_event_nums = defaultdict(int)
        total_event_times = defaultdict(int)
        for row in result:
            event_type = row[0]
            event_name = row[1]
            event_waits = row[2]
            event_wait_times = row[3]
            node_name = row[4]
            uid = get_uid_by_nodename(pg, node_name, uids)
            event_str =  event_type + " " + event_name
            # total_event_nums["Total " + event_str] += int(event_waits)
            # total_event_times["Total " + event_str] += int(event_wait_times)
            total_event_nums[event_str] += int(event_waits)
            total_event_times[event_str] += int(event_wait_times)
            # 数据文件相关等待
            if event_name == 'DataFileRead':
                insert_if_not_exists(uid, index_id="2860209", value=str(event_waits))
                insert_if_not_exists(uid, index_id="2860338", value=str(event_wait_times))
                insert_if_not_exists(targetId, index_id="2860209", value=[dict(name=node_name,value=cs(event_waits))])
                insert_if_not_exists(targetId, index_id="2860338", value=[dict(name=node_name,value=cs(event_wait_times))])
            elif event_name == 'DataFileWrite':
                insert_if_not_exists(uid, index_id="2860210", value=str(event_waits))
                insert_if_not_exists(uid, index_id="2860339", value=str(event_wait_times))
                insert_if_not_exists(targetId, index_id="2860210", value=[dict(name=node_name,value=cs(event_waits))])
                insert_if_not_exists(targetId, index_id="2860339", value=[dict(name=node_name,value=cs(event_wait_times))])
            elif event_name == 'WALWrite':
                insert_if_not_exists(uid, index_id="2860211", value=str(event_waits))
                insert_if_not_exists(uid, index_id="2860340", value=str(event_wait_times))
                insert_if_not_exists(targetId, index_id="2860211", value=[dict(name=node_name,value=cs(event_waits))])
                insert_if_not_exists(targetId, index_id="2860340", value=[dict(name=node_name,value=cs(event_wait_times))])
            # 等待类
            if uid not in event_class:
                event_class[uid] = defaultdict(list)
            if event_type not in event_class[uid]:
                event_class[uid][event_type] = 0
            event_class[uid][event_type] += int(event_waits)

            if uid not in event_info:
                event_info[uid] = defaultdict(list)
            if event_type not in event_info[uid]:
                event_info[uid][event_type] = []
            event_info[uid][event_type].append(dict(name=event_name, value=str(event_waits)))

            if uid not in event_class_time:
                event_class[uid] = defaultdict(list)
            if event_type not in event_class[uid]:
                event_class[uid][event_type] = 0
            event_class[uid][event_type] += int(event_waits)

            if uid not in event_info_time:
                event_info[uid] = defaultdict(list)
            if event_type not in event_info[uid]:
                event_info[uid][event_type] = []
            event_info[uid][event_type].append(dict(name=event_name, value=str(event_wait_times)))

            # 统计每个nodename下每个等待类的等待次数
            if node_name not in node_wait:
                node_wait[node_name] = defaultdict(int)
            if event_type not in node_wait[node_name]:
                node_wait[node_name][event_type] = 0
            node_wait[node_name][event_type] += int(event_waits)

            if event_type not in node_info_wait:
                node_info_wait[event_type] = defaultdict(int)
            if event_name not in node_info_wait[event_type]:
                node_info_wait[event_type][event_name] = 0
            node_info_wait[event_type][event_name] += int(event_waits)

            # 统计每个nodename下每个等待类的等待时间
            if node_name not in node_wait_time:
                node_wait_time[node_name] = defaultdict(int)
            if event_type not in node_wait_time[node_name]:
                node_wait_time[node_name][event_type] = 0
            node_wait_time[node_name][event_type] += int(event_wait_times)


            if event_type not in node_info_wait_time:
                node_info_wait_time[event_type] = defaultdict(int)
            if event_name not in node_info_wait_time[event_type]:
                node_info_wait_time[event_type][event_name] = 0
            node_info_wait_time[event_type][event_name] += int(event_wait_times)

            # 等待事件次数，时间
            insert_if_not_exists(uid, index_id="2860331", value=[{"name": event_str, "value": str(event_waits)}])
            insert_if_not_exists(uid, index_id="2860332", value=[{"name": event_str, "value": str(event_wait_times)}])


        # 汇总每个nodename下每个等待类的等待次数
        tmp = []
        for event_str, event_waits in total_event_nums.items():
            tmp.append({"name": event_str, "value": str(event_waits)})
        insert_if_not_exists(targetId, index_id="2860331", value=tmp)

        # 汇总每个nodename下每个等待类的等待时间
        tmp2 = []
        for event_str, event_times in total_event_times.items():
            tmp2.append({"name": event_str, "value": str(event_times)})
        insert_if_not_exists(targetId, index_id="2860332", value=tmp2)
            
        # 等待类
        for uid, we_dict in event_info.items():
            insert_if_not_exists(uid, index_id="2860301", value="0" if not we_dict["BUFFERPIN_EVENT"] else we_dict["BUFFERPIN_EVENT"])
            insert_if_not_exists(uid, index_id="2860302", value="0" if not we_dict["CLIENT_EVENT"] else we_dict["CLIENT_EVENT"])
            insert_if_not_exists(uid, index_id="2860303", value="0" if not we_dict["EXTENSION_EVENT"] else we_dict["EXTENSION_EVENT"])
            insert_if_not_exists(uid, index_id="2860304", value="0" if not we_dict["IO_EVENT"] else we_dict["IO_EVENT"])
            insert_if_not_exists(uid, index_id="2860305", value="0" if not we_dict["IPC_EVENT"] else we_dict["IPC_EVENT"])
            insert_if_not_exists(uid, index_id="2860306", value="0" if not we_dict["LOCK_EVENT"] else we_dict["LOCK_EVENT"])
            insert_if_not_exists(uid, index_id="2860307", value="0" if not we_dict["LWLOCK_EVENT"] else we_dict["LWLOCK_EVENT"])
            insert_if_not_exists(uid, index_id="2860308", value="0" if not we_dict["TIMEOUT_EVENT"] else we_dict["TIMEOUT_EVENT"])
        
        for uid, we_dict in event_info_time.items():
            insert_if_not_exists(uid, index_id="2863360", value="0" if not we_dict["BUFFERPIN_EVENT"] else we_dict["BUFFERPIN_EVENT"])
            insert_if_not_exists(uid, index_id="2863361", value="0" if not we_dict["CLIENT_EVENT"] else we_dict["CLIENT_EVENT"])
            insert_if_not_exists(uid, index_id="2863362", value="0" if not we_dict["EXTENSION_EVENT"] else we_dict["EXTENSION_EVENT"])
            insert_if_not_exists(uid, index_id="2860363", value="0" if not we_dict["IO_EVENT"] else we_dict["IO_EVENT"])
            insert_if_not_exists(uid, index_id="2860364", value="0" if not we_dict["IPC_EVENT"] else we_dict["IPC_EVENT"])
            insert_if_not_exists(uid, index_id="2860365", value="0" if not we_dict["LOCK_EVENT"] else we_dict["LOCK_EVENT"])
            insert_if_not_exists(uid, index_id="2860366", value="0" if not we_dict["LWLOCK_EVENT"] else we_dict["LWLOCK_EVENT"])
            insert_if_not_exists(uid, index_id="2860367", value="0" if not we_dict["TIMEOUT_EVENT"] else we_dict["TIMEOUT_EVENT"])
            
        for uid, wet_dict in event_class.items():
            insert_if_not_exists(uid, index_id="2860311", value=get_dict(wet_dict, "BUFFERPIN_EVENT"))
            insert_if_not_exists(uid, index_id="2860312", value=get_dict(wet_dict, "CLIENT_EVENT"))
            insert_if_not_exists(uid, index_id="2860313", value=get_dict(wet_dict, "EXTENSION_EVENT"))
            insert_if_not_exists(uid, index_id="2860314", value=get_dict(wet_dict, "IO_EVENT_EVENT"))
            insert_if_not_exists(uid, index_id="2860315", value=get_dict(wet_dict, "IPC_EVENT"))
            insert_if_not_exists(uid, index_id="2860316", value=get_dict(wet_dict, "LOCK_EVENT"))
            insert_if_not_exists(uid, index_id="2860317", value=get_dict(wet_dict, "LWLOCK_EVENT"))
            insert_if_not_exists(uid, index_id="2860318", value=get_dict(wet_dict, "TIMEOUT_EVENT"))
            insert_if_not_exists(uid, index_id="2860320", value=get_dict(wet_dict, "STATUS"))
        
        for uid, wet_dict in event_class_time.items():
            insert_if_not_exists(uid, index_id="2863359", value=get_dict(wet_dict, "BUFFERPIN_EVENT"))
            insert_if_not_exists(uid, index_id="2863351", value=get_dict(wet_dict, "CLIENT_EVENT"))
            insert_if_not_exists(uid, index_id="2863352", value=get_dict(wet_dict, "EXTENSION_EVENT"))
            insert_if_not_exists(uid, index_id="2863353", value=get_dict(wet_dict, "IO_EVENT_EVENT"))
            insert_if_not_exists(uid, index_id="2863354", value=get_dict(wet_dict, "IPC_EVENT"))
            insert_if_not_exists(uid, index_id="2863355", value=get_dict(wet_dict, "LOCK_EVENT"))
            insert_if_not_exists(uid, index_id="2863356", value=get_dict(wet_dict, "LWLOCK_EVENT"))
            insert_if_not_exists(uid, index_id="2863357", value=get_dict(wet_dict, "TIMEOUT_EVENT"))
            insert_if_not_exists(uid, index_id="2863358", value=get_dict(wet_dict, "STATUS"))

        # 集群汇总
        for node, wait in node_wait.items():
            insert_if_not_exists(targetId, 2860311, [dict(name=node,value=cs("0" if not wait["BUFFERPIN_EVENT"] else wait["BUFFERPIN_EVENT"]))])
            insert_if_not_exists(targetId, 2860312, [dict(name=node,value=cs("0" if not wait["CLIENT_EVENT"] else wait["CLIENT_EVENT"]))])
            insert_if_not_exists(targetId, 2860313, [dict(name=node,value=cs("0" if not wait["EXTENSION_EVENT"] else wait["EXTENSION_EVENT"]))])
            insert_if_not_exists(targetId, 2860314, [dict(name=node,value=cs("0" if not wait["IO_EVENT"] else wait["IO_EVENT"]))])
            insert_if_not_exists(targetId, 2860315, [dict(name=node,value=cs("0" if not wait["IPC_EVENT"] else wait["IPC_EVENT"]))])
            insert_if_not_exists(targetId, 2860316, [dict(name=node,value=cs("0" if not wait["LOCK_EVENT"] else wait["LOCK_EVENT"]))])
            insert_if_not_exists(targetId, 2860317, [dict(name=node,value=cs("0" if not wait["LWLOCK_EVENT"] else wait["LWLOCK_EVENT"]))])
            insert_if_not_exists(targetId, 2860318, [dict(name=node,value=cs("0" if not wait["TIMEOUT_EVENT"] else wait["TIMEOUT_EVENT"]))])
            insert_if_not_exists(targetId, 2860320, [dict(name=node,value=cs("0" if not wait["STATUS"] else wait["STATUS"]))])

        for node, wait in node_wait_time.items():
            insert_if_not_exists(targetId, 2863359, [dict(name=node,value=cs("0" if not wait["BUFFERPIN_EVENT"] else wait["BUFFERPIN_EVENT"]))])
            insert_if_not_exists(targetId, 2863351, [dict(name=node,value=cs("0" if not wait["CLIENT_EVENT"] else wait["CLIENT_EVENT"]))])
            insert_if_not_exists(targetId, 2863352, [dict(name=node,value=cs("0" if not wait["EXTENSION_EVENT"] else wait["EXTENSION_EVENT"]))])
            insert_if_not_exists(targetId, 2863353, [dict(name=node,value=cs("0" if not wait["IO_EVENT"] else wait["IO_EVENT"]))])
            insert_if_not_exists(targetId, 2863354, [dict(name=node,value=cs("0" if not wait["IPC_EVENT"] else wait["IPC_EVENT"]))])
            insert_if_not_exists(targetId, 2863355, [dict(name=node,value=cs("0" if not wait["LOCK_EVENT"] else wait["LOCK_EVENT"]))])
            insert_if_not_exists(targetId, 2863356, [dict(name=node,value=cs("0" if not wait["LWLOCK_EVENT"] else wait["LWLOCK_EVENT"]))])
            insert_if_not_exists(targetId, 2863357, [dict(name=node,value=cs("0" if not wait["TIMEOUT_EVENT"] else wait["TIMEOUT_EVENT"]))])
            insert_if_not_exists(targetId, 2863358, [dict(name=node,value=cs("0" if not wait["STATUS"] else wait["STATUS"]))])

        for wait_type, wait in node_info_wait.items():
            vals = []
            if wait_type == 'BUFFERPIN_EVENT':
                for event, waits in wait.items():
                    vals.append(dict(name=event,value=cs(waits)))
                insert_if_not_exists(targetId, 2860301, vals)
            elif wait_type == 'CLIENT_EVENT':
                for event, waits in wait.items():
                    vals.append(dict(name=event,value=cs(waits)))
                insert_if_not_exists(targetId, 2860302, vals)
            elif wait_type == 'EXTENSION_EVENT':
                for event, waits in wait.items():
                    vals.append(dict(name=event,value=cs(waits)))
                insert_if_not_exists(targetId, 2860303, vals)
            elif wait_type == 'IO_EVENT':
                for event, waits in wait.items():
                    vals.append(dict(name=event,value=cs(waits)))
                insert_if_not_exists(targetId, 2860304, vals)
            elif wait_type == 'IPC_EVENT':
                for event, waits in wait.items():
                    vals.append(dict(name=event,value=cs(waits)))
                insert_if_not_exists(targetId, 2860305, vals)
            elif wait_type == 'LOCK_EVENT':
                for event, waits in wait.items():
                    vals.append(dict(name=event,value=cs(waits)))
                insert_if_not_exists(targetId, 2860306, vals)
            elif wait_type == 'LWLOCK_EVENT':
                for event, waits in wait.items():
                    vals.append(dict(name=event,value=cs(waits)))
                insert_if_not_exists(targetId, 2860307, vals)
            elif wait_type == 'TIMEOUT_EVENT':
                for event, waits in wait.items():
                    vals.append(dict(name=event,value=cs(waits)))
                insert_if_not_exists(targetId, 2860308, vals)
            elif wait_type == 'STATUS':
                for event, waits in wait.items():
                    vals.append(dict(name=event,value=cs(waits)))
                insert_if_not_exists(targetId, 2860309, vals)

        for wait_type, wait in node_info_wait_time.items():
            vals = []
            if wait_type == 'BUFFERPIN_EVENT':
                for event, waits in wait.items():
                    vals.append(dict(name=event,value=cs(waits)))
                insert_if_not_exists(targetId, 2863360, vals)
            elif wait_type == 'CLIENT_EVENT':
                for event, waits in wait.items():
                    vals.append(dict(name=event,value=cs(waits)))
                insert_if_not_exists(targetId, 2863361, vals)
            elif wait_type == 'EXTENSION_EVENT':
                for event, waits in wait.items():
                    vals.append(dict(name=event,value=cs(waits)))
                insert_if_not_exists(targetId, 2863362, vals)
            elif wait_type == 'IO_EVENT':
                for event, waits in wait.items():
                    vals.append(dict(name=event,value=cs(waits)))
                insert_if_not_exists(targetId, 2863363, vals)
            elif wait_type == 'IPC_EVENT':
                for event, waits in wait.items():
                    vals.append(dict(name=event,value=cs(waits)))
                insert_if_not_exists(targetId, 2863364, vals)
            elif wait_type == 'LOCK_EVENT':
                for event, waits in wait.items():
                    vals.append(dict(name=event,value=cs(waits)))
                insert_if_not_exists(targetId, 2863365, vals)
            elif wait_type == 'LWLOCK_EVENT':
                for event, waits in wait.items():
                    vals.append(dict(name=event,value=cs(waits)))
                insert_if_not_exists(targetId, 2863366, vals)
            elif wait_type == 'TIMEOUT_EVENT':
                for event, waits in wait.items():
                    vals.append(dict(name=event,value=cs(waits)))
                insert_if_not_exists(targetId, 2863367, vals)
            elif wait_type == 'STATUS':
                for event, waits in wait.items():
                    vals.append(dict(name=event,value=cs(waits)))
                insert_if_not_exists(targetId, 2863368, vals)


def collect_all_cns(cns_nodes):
    "需联系所有CN，采集的指标信息"
    sql = "select count(*) from pgxc_node where nodeis_active"
    # 查看所有节点的信息是否一致
    nodes = []
    for gs in cns_nodes:
        curs = DBUtil.getValue(gs, sql)
        rs = curs.fetchone()
        if rs:
            nodes.append(rs[0])
    if len(set(nodes)) > 1:
        insert_if_not_exists(targetId, 2863328, '0')
    else:
        insert_if_not_exists(targetId, 2863328, '1')


def get_metric_from_tpops(is_cloud=False):
    import time
    import statistics
    import gauss_tpops_api as tpops
    ip,port,tp_token = DBUtil.get_tpops_connect_info(pg, targetId)
    if ip and port and tp_token:
        instance_info = tpops.get_gauss_instance(ip, port, tp_token)
        if instance_info.status_code == 200:
            insert_if_not_exists(targetId, index_id="2863435", value=cs('连接成功'))
            instance_info = instance_info.json()
            instances_all = instance_info['instances']
            # 获取实例指标,获取当前时间的前2分钟的指标
            begin_time = int(time.time())*1000 - 300*1000
            end_time = int(time.time())*1000
            total_cns = 0
            total_dns = 0
            total_gtms = 0
            total_cms = 0
            total_etcd = 0
            failed_cns = 0
            failed_dns = 0
            failed_gtms = 0
            failed_cms = 0
            failed_etcd = 0
            failed_info = ''
            for instance in instances_all:
                instance_id = instance['id']
                ips = instance['private_ips']
                nodes = instance['nodes']
                nodes_dict = {}
                for node in nodes:
                    if gs_ip in ips[0]:
                        component_names = node["component_names"]
                        node_stat = node["status"]
                        nodes_dict[node["data_ip"]] = component_names
                        if is_cloud:
                            if node_stat != 'ACTIVE':
                                failed_cns += component_names.count("cn_")
                                failed_dns += component_names.count("dn_")
                                failed_gtms += component_names.count("gtm_")
                                failed_cms += component_names.count("cm_")
                                failed_etcd += component_names.count("etcd_")
                                failed_info += f'{node["data_ip"]}节点上的服务：' + component_names + ';\n'
                            total_cns += component_names.count("cn_")
                            total_dns += component_names.count("dn_")
                            total_gtms += component_names.count("gtm_")
                            total_cms += component_names.count("cm_")
                            total_etcd += component_names.count("etcd_")
                if nodes_dict:
                    # 获取NAS使用率信息
                    metric_names = ["nas_usage","sys011_bytes_in","sys012_bytes_out","sys075_avg_disk_ms_per_write","sys076_avg_disk_ms_per_read",
                    "rds079_gaussv5_current_sleep_time","rds083_gaussv5_standby_delay","rds105_gaussv5_ckpt_delay","rds125_dirty_page_num"
                    ,"rds192_replication_slot_wal_log_size","rds123_xlog_lsn","rds126_xlog_num","rds127_sys_database_size","rds128_user_database_size"
                    ,"sys010_mem_usage","cpu_sys_usage","cpu_user_usage","sys001_cpu_usage","rds124_candidate_slots_num"
                    ,"sys002_idle_usage","cpu_wait_usage","sys016_cpu_load","mem_used_size","sys013_mem_free_size"
                    ,"buffer_size","cache_size","sys024_swap_total_size","sys026_swap_used_size"
                    ,"sys025_swap_used_ratio","sys071_disk_write_throughput","sys072_disk_read_throughput","sys069_iops"]
                    metric_out = tpops.get_gauss_metric(ip, port, tp_token, instance_id, metric_names,begin_time,end_time)
                    if metric_out.status_code == 200:
                        metric_info = metric_out.json()
                        disk_io_dict = {}
                        disk_throughput_dict = {}
                        for metrics in metric_info["metric_infos"][0]["metrics"]:
                            name = metrics["name"]
                            valus_dict = metrics["series"]
                            if name == 'nas_usage':
                                cn_temp = []
                                dn_temp = []
                                for node_name, value in valus_dict.items():
                                    for row in value:
                                        if row != 'null' and row is not None:
                                            insert_if_not_exists(get_uid_by_ip(node_name), 2863392, cs(row))
                                            insert_if_not_exists(targetId, 2863392, [dict(name=node_name,value=cs(row))])
                                            if node_name[:2] == 'cn' or (nodes_dict.get(node_name) and "cn_" in nodes_dict.get(node_name)):
                                                cn_temp.append(row)
                                            if node_name[:2] == 'dn' or (nodes_dict.get(node_name) and "dn_" in nodes_dict.get(node_name)):
                                                dn_temp.append(row)
                                            break;
                                # 计算cn和dn的max,min,total
                                if cn_temp:
                                    insert_if_not_exists(targetId, 2863392, [dict(name="_cn_max",value=cs(max(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863392, [dict(name="_cn_min",value=cs(min(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863392, [dict(name="_cn_total",value=cs(sum(cn_temp)))] )
                                if dn_temp:
                                    insert_if_not_exists(targetId, 2863392, [dict(name="_dn_max",value=cs(max(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863392, [dict(name="_dn_min",value=cs(min(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863392, [dict(name="_dn_total",value=cs(sum(dn_temp)))] )
                            elif name == 'sys069_iops':
                                cn_temp = []
                                dn_temp = []
                                iops_tmp = []
                                for node_name, value in valus_dict.items():
                                    for row in value:
                                        if row != 'null' and row is not None:
                                            iops_tmp.append(row)
                                            insert_if_not_exists(get_uid_by_ip(node_name), 3000100, cs(row))
                                            insert_if_not_exists(get_uid_by_ip(node_name), 2863430, cs(row))
                                            insert_if_not_exists(targetId, 1001100, [dict(name=node_name,value=cs(row))])
                                            insert_if_not_exists(targetId, 2863430, [dict(name=node_name,value=cs(row))])
                                            if node_name[:2] == 'cn' or (nodes_dict.get(node_name) and "cn_" in nodes_dict.get(node_name)):
                                                cn_temp.append(row)
                                            if node_name[:2] == 'dn' or (nodes_dict.get(node_name) and "dn_" in nodes_dict.get(node_name)):
                                                dn_temp.append(row)
                                            break;
                                # 最大值、最小值、平均值
                                if iops_tmp:
                                    insert_if_not_exists(targetId, 1001100, [dict(name="max",value=cs(max(iops_tmp)))] )
                                    insert_if_not_exists(targetId, 1001100, [dict(name="min",value=cs(min(iops_tmp)))] )
                                    insert_if_not_exists(targetId, 1001100, [dict(name="avg",value=cs(sum(iops_tmp)/len(iops_tmp)))])
                                # 计算cn和dn的max,min,total
                                if cn_temp:
                                    insert_if_not_exists(targetId, 2863430, [dict(name="_cn_max",value=cs(max(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863430, [dict(name="_cn_min",value=cs(min(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863430, [dict(name="_cn_total",value=cs(sum(cn_temp)))] )
                                if dn_temp:
                                    insert_if_not_exists(targetId, 2863430, [dict(name="_dn_max",value=cs(max(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863430, [dict(name="_dn_min",value=cs(min(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863430, [dict(name="_dn_total",value=cs(sum(dn_temp)))] )
                            elif name == 'sys072_disk_read_throughput':
                                cn_temp = []
                                dn_temp = []
                                for node_name, value in valus_dict.items():
                                    for row in value:
                                        if row != 'null' and row is not None:
                                            uid = get_uid_by_ip(node_name)
                                            row = round(row/1024,2)
                                            if node_name in disk_throughput_dict.keys():
                                                disk_throughput_dict[node_name] += row
                                            else:
                                                disk_throughput_dict[node_name] = row
                                            insert_if_not_exists(uid, 2863431, cs(row))
                                            insert_if_not_exists(targetId, 2863431, [dict(name=node_name,value=cs(row))])
                                            if node_name[:2] == 'cn' or (nodes_dict.get(node_name) and "cn_" in nodes_dict.get(node_name)):
                                                cn_temp.append(row)
                                            if node_name[:2] == 'dn' or (nodes_dict.get(node_name) and "dn_" in nodes_dict.get(node_name)):
                                                dn_temp.append(row)
                                            break;
                                # 计算cn和dn的max,min,total
                                if cn_temp:
                                    insert_if_not_exists(targetId, 2863431, [dict(name="_cn_max",value=cs(max(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863431, [dict(name="_cn_min",value=cs(min(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863431, [dict(name="_cn_total",value=cs(sum(cn_temp)))] )
                                if dn_temp:
                                    insert_if_not_exists(targetId, 2863431, [dict(name="_dn_max",value=cs(max(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863431, [dict(name="_dn_min",value=cs(min(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863431, [dict(name="_dn_total",value=cs(sum(dn_temp)))] )
                            elif name == 'sys071_disk_write_throughput':
                                cn_temp = []
                                dn_temp = []
                                for node_name, value in valus_dict.items():
                                    for row in value:
                                        if row != 'null' and row is not None:
                                            uid = get_uid_by_ip(node_name)
                                            row = round(row/1024,2)
                                            if node_name in disk_throughput_dict.keys():
                                                disk_throughput_dict[node_name] += row
                                            else:
                                                disk_throughput_dict[node_name] = row
                                            insert_if_not_exists(uid, 2863432, cs(row))
                                            insert_if_not_exists(targetId, 2863432, [dict(name=node_name,value=cs(row))])
                                            if node_name[:2] == 'cn' or (nodes_dict.get(node_name) and "cn_" in nodes_dict.get(node_name)):
                                                cn_temp.append(row)
                                            if node_name[:2] == 'dn' or (nodes_dict.get(node_name) and "dn_" in nodes_dict.get(node_name)):
                                                dn_temp.append(row)
                                            break;
                                # 计算cn和dn的max,min,total
                                if cn_temp:
                                    insert_if_not_exists(targetId, 2863432, [dict(name="_cn_max",value=cs(max(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863432, [dict(name="_cn_min",value=cs(min(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863432, [dict(name="_cn_total",value=cs(sum(cn_temp)))] )
                                if dn_temp:
                                    insert_if_not_exists(targetId, 2863432, [dict(name="_dn_max",value=cs(max(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863432, [dict(name="_dn_min",value=cs(min(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863432, [dict(name="_dn_total",value=cs(sum(dn_temp)))] )                            
                            elif name == 'sys011_bytes_in':
                                cn_temp = []
                                dn_temp = []
                                for node_name, value in valus_dict.items():
                                    for row in value:
                                        if row != 'null' and row is not None:
                                            insert_if_not_exists(get_uid_by_ip(node_name), 2863393, cs(round(row/1024/1024,2)))
                                            insert_if_not_exists(targetId, 2863393, [dict(name=node_name,value=cs(round(row/1024/1024,2)))])
                                            if node_name[:2] == 'cn' or (nodes_dict.get(node_name) and "cn_" in nodes_dict.get(node_name)):
                                                cn_temp.append(row)
                                            if node_name[:2] == 'dn' or (nodes_dict.get(node_name) and "dn_" in nodes_dict.get(node_name)):
                                                dn_temp.append(row)
                                            break;
                                # 计算cn和dn的max,min,total
                                if cn_temp:
                                    insert_if_not_exists(targetId, 2863393, [dict(name="_cn_max",value=cs(round(max(cn_temp)/1024/1024,2)))] )
                                    insert_if_not_exists(targetId, 2863393, [dict(name="_cn_min",value=cs(round(min(cn_temp)/1024/1024,2)))] )
                                    insert_if_not_exists(targetId, 2863393, [dict(name="_cn_total",value=cs(round(sum(cn_temp)/1024/1024,2)))] )
                                if dn_temp:
                                    insert_if_not_exists(targetId, 2863393, [dict(name="_dn_max",value=cs(round(max(dn_temp)/1024/1024,2)))] )
                                    insert_if_not_exists(targetId, 2863393, [dict(name="_dn_min",value=cs(round(min(dn_temp)/1024/1024,2)))] )
                                    insert_if_not_exists(targetId, 2863393, [dict(name="_dn_total",value=cs(round(sum(dn_temp)/1024/1024,2)))] )
                            elif name == 'sys012_bytes_out':
                                cn_temp = []
                                dn_temp = []
                                for node_name, value in valus_dict.items():
                                    for row in value:
                                        if row != 'null' and row is not None:
                                            insert_if_not_exists(get_uid_by_ip(node_name), 2863394, cs(round(row/1024/1024,2)))
                                            insert_if_not_exists(targetId, 2863394, [dict(name=node_name,value=cs(round(row/1024/1024,2)))])
                                            if node_name[:2] == 'cn' or (nodes_dict.get(node_name) and "cn_" in nodes_dict.get(node_name)):
                                                cn_temp.append(row)
                                            if node_name[:2] == 'dn' or (nodes_dict.get(node_name) and "dn_" in nodes_dict.get(node_name)):
                                                dn_temp.append(row)
                                            break;
                                # 计算cn和dn的max,min,total
                                if cn_temp:
                                    insert_if_not_exists(targetId, 2863394, [dict(name="_cn_max",value=cs(round(max(cn_temp)/1024/1024,2)))] )
                                    insert_if_not_exists(targetId, 2863394, [dict(name="_cn_min",value=cs(round(min(cn_temp)/1024/1024,2)))] )
                                    insert_if_not_exists(targetId, 2863394, [dict(name="_cn_total",value=cs(round(sum(cn_temp)/1024/1024,2)))] )
                                if dn_temp:
                                    insert_if_not_exists(targetId, 2863394, [dict(name="_dn_max",value=cs(round(max(dn_temp)/1024/1024,2)))] )
                                    insert_if_not_exists(targetId, 2863394, [dict(name="_dn_min",value=cs(round(min(dn_temp)/1024/1024,2)))] )
                                    insert_if_not_exists(targetId, 2863394, [dict(name="_dn_total",value=cs(round(sum(dn_temp)/1024/1024,2)))] )
                            elif name == 'rds079_gaussv5_current_sleep_time':
                                cn_temp = []
                                dn_temp = []
                                for node_name, value in valus_dict.items():
                                    for row in value:
                                        if row != 'null' and row is not None:
                                            insert_if_not_exists(get_uid_by_ip(node_name), 2863395, cs(row))
                                            insert_if_not_exists(targetId, 2863395, [dict(name=node_name,value=cs(row))])
                                            if node_name[:2] == 'cn' or (nodes_dict.get(node_name) and "cn_" in nodes_dict.get(node_name)):
                                                cn_temp.append(row)
                                            if node_name[:2] == 'dn' or (nodes_dict.get(node_name) and "dn_" in nodes_dict.get(node_name)):
                                                dn_temp.append(row)
                                            break;
                                # 计算cn和dn的max,min,total
                                if cn_temp:
                                    insert_if_not_exists(targetId, 2863395, [dict(name="_cn_max",value=cs(max(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863395, [dict(name="_cn_min",value=cs(min(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863395, [dict(name="_cn_total",value=cs(sum(cn_temp)))] )
                                if dn_temp:
                                    insert_if_not_exists(targetId, 2863395, [dict(name="_dn_max",value=cs(max(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863395, [dict(name="_dn_min",value=cs(min(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863395, [dict(name="_dn_total",value=cs(sum(dn_temp)))] )
                            elif name == 'rds083_gaussv5_standby_delay':
                                cn_temp = []
                                dn_temp = []
                                for node_name, value in valus_dict.items():
                                    for row in value:
                                        if row != 'null' and row is not None:
                                            insert_if_not_exists(get_uid_by_ip(node_name), 2863396, cs(row))
                                            insert_if_not_exists(targetId, 2863396, [dict(name=node_name,value=cs(row))])
                                            if node_name[:2] == 'cn' or (nodes_dict.get(node_name) and "cn_" in nodes_dict.get(node_name)):
                                                cn_temp.append(row)
                                            if node_name[:2] == 'dn' or (nodes_dict.get(node_name) and "dn_" in nodes_dict.get(node_name)):
                                                dn_temp.append(row)
                                            break;
                                # 计算cn和dn的max,min,total
                                if cn_temp:
                                    insert_if_not_exists(targetId, 2863396, [dict(name="_cn_max",value=cs(max(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863396, [dict(name="_cn_min",value=cs(min(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863396, [dict(name="_cn_total",value=cs(sum(cn_temp)))] )
                                if dn_temp:
                                    insert_if_not_exists(targetId, 2863396, [dict(name="_dn_max",value=cs(max(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863396, [dict(name="_dn_min",value=cs(min(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863396, [dict(name="_dn_total",value=cs(sum(dn_temp)))] )
                            elif name == 'rds105_gaussv5_ckpt_delay':
                                cn_temp = []
                                dn_temp = []
                                for node_name, value in valus_dict.items():
                                    for row in value:
                                        if row != 'null' and row is not None:
                                            insert_if_not_exists(get_uid_by_ip(node_name), 2863401, cs(row))
                                            insert_if_not_exists(targetId, 2863397, [dict(name=node_name,value=cs(row))])
                                            if node_name[:2] == 'cn' or (nodes_dict.get(node_name) and "cn_" in nodes_dict.get(node_name)):
                                                cn_temp.append(row)
                                            if node_name[:2] == 'dn' or (nodes_dict.get(node_name) and "dn_" in nodes_dict.get(node_name)):
                                                dn_temp.append(row)
                                            break;
                                # 计算cn和dn的max,min,total
                                if cn_temp:
                                    insert_if_not_exists(targetId, 2863397, [dict(name="_cn_max",value=cs(max(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863397, [dict(name="_cn_min",value=cs(min(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863397, [dict(name="_cn_total",value=cs(sum(cn_temp)))] )
                                if dn_temp:
                                    insert_if_not_exists(targetId, 2863397, [dict(name="_dn_max",value=cs(max(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863397, [dict(name="_dn_min",value=cs(min(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863397, [dict(name="_dn_total",value=cs(sum(dn_temp)))] )
                            elif name == 'rds125_dirty_page_num':
                                cn_temp = []
                                dn_temp = []
                                for node_name, value in valus_dict.items():
                                    for row in value:
                                        if row != 'null' and row is not None:
                                            insert_if_not_exists(get_uid_by_ip(node_name), 2863401, cs(row))
                                            insert_if_not_exists(targetId, 2863398, [dict(name=node_name,value=cs(row))])
                                            if node_name[:2] == 'cn' or (nodes_dict.get(node_name) and "cn_" in nodes_dict.get(node_name)):
                                                cn_temp.append(row)
                                            if node_name[:2] == 'dn' or (nodes_dict.get(node_name) and "dn_" in nodes_dict.get(node_name)):
                                                dn_temp.append(row)
                                            break;
                                # 计算cn和dn的max,min,total
                                if cn_temp:
                                    insert_if_not_exists(targetId, 2863398, [dict(name="_cn_max",value=cs(max(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863398, [dict(name="_cn_min",value=cs(min(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863398, [dict(name="_cn_total",value=cs(sum(cn_temp)))] )
                                if dn_temp:
                                    insert_if_not_exists(targetId, 2863398, [dict(name="_dn_max",value=cs(max(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863398, [dict(name="_dn_min",value=cs(min(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863398, [dict(name="_dn_total",value=cs(sum(dn_temp)))] )
                            elif name == 'rds124_candidate_slots_num':
                                cn_temp = []
                                dn_temp = []
                                for node_name, value in valus_dict.items():
                                    for row in value:
                                        if row != 'null' and row is not None:
                                            insert_if_not_exists(get_uid_by_ip(node_name), 2863401, cs(row))
                                            insert_if_not_exists(targetId, 2863399, [dict(name=node_name,value=cs(row))])
                                            if node_name[:2] == 'cn' or (nodes_dict.get(node_name) and "cn_" in nodes_dict.get(node_name)):
                                                cn_temp.append(row)
                                            if node_name[:2] == 'dn' or (nodes_dict.get(node_name) and "dn_" in nodes_dict.get(node_name)):
                                                dn_temp.append(row)
                                            break;
                                # 计算cn和dn的max,min,total
                                if cn_temp:
                                    insert_if_not_exists(targetId, 2863399, [dict(name="_cn_max",value=cs(max(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863399, [dict(name="_cn_min",value=cs(min(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863399, [dict(name="_cn_total",value=cs(sum(cn_temp)))] )
                                if dn_temp:
                                    insert_if_not_exists(targetId, 2863399, [dict(name="_dn_max",value=cs(max(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863399, [dict(name="_dn_min",value=cs(min(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863399, [dict(name="_dn_total",value=cs(sum(dn_temp)))] )
                            elif name == 'rds192_replication_slot_wal_log_size':
                                cn_temp = []
                                dn_temp = []
                                for node_name, value in valus_dict.items():
                                    if row != 'null' and row is not None:
                                        insert_if_not_exists(get_uid_by_ip(node_name), 2863401, cs(row))
                                        insert_if_not_exists(targetId, 2863400, [dict(name=node_name,value=cs(row))])
                                        if node_name[:2] == 'cn' or (nodes_dict.get(node_name) and "cn_" in nodes_dict.get(node_name)):
                                            cn_temp.append(row)
                                        if node_name[:2] == 'dn' or (nodes_dict.get(node_name) and "dn_" in nodes_dict.get(node_name)):
                                            dn_temp.append(row)
                                        break;
                                # 计算cn和dn的max,min,total
                                if cn_temp:
                                    insert_if_not_exists(targetId, 2863400, [dict(name="_cn_max",value=cs(max(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863400, [dict(name="_cn_min",value=cs(min(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863400, [dict(name="_cn_total",value=cs(sum(cn_temp)))] )
                                if dn_temp:
                                    insert_if_not_exists(targetId, 2863400, [dict(name="_dn_max",value=cs(max(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863400, [dict(name="_dn_min",value=cs(min(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863400, [dict(name="_dn_total",value=cs(sum(dn_temp)))] )
                            elif name == 'rds123_xlog_lsn':
                                cn_temp = []
                                dn_temp = []
                                for node_name, value in valus_dict.items():
                                    for row in value:
                                        if row != 'null' and row is not None:
                                            insert_if_not_exists(get_uid_by_ip(node_name), 2863401, cs(row))
                                            insert_if_not_exists(targetId, 2863401, [dict(name=node_name,value=cs(row))])
                                            if node_name[:2] == 'cn' or (nodes_dict.get(node_name) and "cn_" in nodes_dict.get(node_name)):
                                                cn_temp.append(row)
                                            if node_name[:2] == 'dn' or (nodes_dict.get(node_name) and "dn_" in nodes_dict.get(node_name)):
                                                dn_temp.append(row)
                                            break;
                                # 计算cn和dn的max,min,total
                                if cn_temp:
                                    insert_if_not_exists(targetId, 2863401, [dict(name="_cn_max",value=cs(max(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863401, [dict(name="_cn_min",value=cs(min(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863401, [dict(name="_cn_total",value=cs(sum(cn_temp)))] )
                                if dn_temp:
                                    insert_if_not_exists(targetId, 2863401, [dict(name="_dn_max",value=cs(max(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863401, [dict(name="_dn_min",value=cs(min(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863401, [dict(name="_dn_total",value=cs(sum(dn_temp)))] )
                            elif name == 'rds126_xlog_num':
                                cn_temp = []
                                dn_temp = []
                                for node_name, value in valus_dict.items():
                                    for row in value:
                                        if row != 'null' and row is not None:
                                            insert_if_not_exists(get_uid_by_ip(node_name), 2863401, cs(row))
                                            insert_if_not_exists(targetId, 2863402, [dict(name=node_name,value=cs(row))])
                                            if node_name[:2] == 'cn' or (nodes_dict.get(node_name) and "cn_" in nodes_dict.get(node_name)):
                                                cn_temp.append(row)
                                            if node_name[:2] == 'dn' or (nodes_dict.get(node_name) and "dn_" in nodes_dict.get(node_name)):
                                                dn_temp.append(row)
                                            break;
                                # 计算cn和dn的max,min,total
                                if cn_temp:
                                    insert_if_not_exists(targetId, 2863402, [dict(name="_cn_max",value=cs(max(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863402, [dict(name="_cn_min",value=cs(min(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863402, [dict(name="_cn_total",value=cs(sum(cn_temp)))] )
                                if dn_temp:
                                    insert_if_not_exists(targetId, 2863402, [dict(name="_dn_max",value=cs(max(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863402, [dict(name="_dn_min",value=cs(min(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863402, [dict(name="_dn_total",value=cs(sum(dn_temp)))] )
                            elif name == 'rds127_sys_database_size':
                                cn_temp = []
                                dn_temp = []
                                for node_name, value in valus_dict.items():
                                    for row in value:
                                        if row != 'null' and row is not None:
                                            insert_if_not_exists(get_uid_by_ip(node_name), 2863401, cs(round(row/1024/1024/1024,2)))
                                            insert_if_not_exists(targetId, 2863403, [dict(name=node_name,value=cs(round(row/1024/1024/1024,2)))])
                                            if node_name[:2] == 'cn' or (nodes_dict.get(node_name) and "cn_" in nodes_dict.get(node_name)):
                                                cn_temp.append(row)
                                            if node_name[:2] == 'dn' or (nodes_dict.get(node_name) and "dn_" in nodes_dict.get(node_name)):
                                                dn_temp.append(row)
                                            break;
                                # 计算cn和dn的max,min,total
                                if cn_temp:
                                    insert_if_not_exists(targetId, 2863403, [dict(name="_cn_max",value=cs(round(max(cn_temp)/1024/1024/1024,2)))] )
                                    insert_if_not_exists(targetId, 2863403, [dict(name="_cn_min",value=cs(round(min(cn_temp)/1024/1024/1024,2)))] )
                                    insert_if_not_exists(targetId, 2863403, [dict(name="_cn_total",value=cs(round(sum(cn_temp)/1024/1024/1024,2)))] )
                                if dn_temp:
                                    insert_if_not_exists(targetId, 2863403, [dict(name="_dn_max",value=cs(round(max(dn_temp)/1024/1024/1024,2)))] )
                                    insert_if_not_exists(targetId, 2863403, [dict(name="_dn_min",value=cs(round(min(dn_temp)/1024/1024/1024,2)))] )
                                    insert_if_not_exists(targetId, 2863403, [dict(name="_dn_total",value=cs(round(sum(dn_temp)/1024/1024/1024,2)))] )
                            elif name == 'rds128_user_database_size':
                                cn_temp = []
                                dn_temp = []
                                for node_name, value in valus_dict.items():
                                    for row in value:
                                        if row != 'null' and row is not None:
                                            insert_if_not_exists(get_uid_by_ip(node_name), 2863401, cs(round(row/1024/1024/1024,2)))
                                            insert_if_not_exists(targetId, 2863404, [dict(name=node_name,value=cs(round(row/1024/1024/1024,2)))])
                                            if node_name[:2] == 'cn' or (nodes_dict.get(node_name) and "cn_" in nodes_dict.get(node_name)):
                                                cn_temp.append(row)
                                            if node_name[:2] == 'dn' or (nodes_dict.get(node_name) and "dn_" in nodes_dict.get(node_name)):
                                                dn_temp.append(row)
                                            break;
                                # 计算cn和dn的max,min,total
                                if cn_temp:
                                    insert_if_not_exists(targetId, 2863404, [dict(name="_cn_max",value=cs(round(max(cn_temp)/1024/1024/1024,2)))] )
                                    insert_if_not_exists(targetId, 2863404, [dict(name="_cn_min",value=cs(round(min(cn_temp)/1024/1024/1024,2)))] )
                                    insert_if_not_exists(targetId, 2863404, [dict(name="_cn_total",value=cs(round(sum(cn_temp)/1024/1024/1024,2)))] )
                                if dn_temp:
                                    insert_if_not_exists(targetId, 2863404, [dict(name="_dn_max",value=cs(round(max(dn_temp)/1024/1024/1024,2)))] )
                                    insert_if_not_exists(targetId, 2863404, [dict(name="_dn_min",value=cs(round(min(dn_temp)/1024/1024/1024,2)))] )
                                    insert_if_not_exists(targetId, 2863404, [dict(name="_dn_total",value=cs(round(sum(dn_temp)/1024/1024/1024,2)))] )
                            elif name == 'sys075_avg_disk_ms_per_write':
                                cn_temp = []
                                dn_temp = []
                                for node_name, value in valus_dict.items():
                                    for row in value:
                                        if row != 'null' and row is not None:
                                            uid = get_uid_by_ip(node_name)
                                            if node_name in disk_io_dict.keys():
                                                disk_io_dict[node_name] += row
                                            else:
                                                disk_io_dict[node_name] = row
                                            insert_if_not_exists(uid, 2863405, cs(row))
                                            insert_if_not_exists(targetId, 2863405, [dict(name=node_name,value=cs(row))])
                                            if node_name[:2] == 'cn' or (nodes_dict.get(node_name) and "cn_" in nodes_dict.get(node_name)):
                                                cn_temp.append(row)
                                            if node_name[:2] == 'dn' or (nodes_dict.get(node_name) and "dn_" in nodes_dict.get(node_name)):
                                                dn_temp.append(row)
                                            break;
                                # 计算cn和dn的max,min,total
                                if cn_temp:
                                    insert_if_not_exists(targetId, 2863405, [dict(name="_cn_max",value=cs(max(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863405, [dict(name="_cn_min",value=cs(min(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863405, [dict(name="_cn_total",value=cs(sum(cn_temp)))] )
                                if dn_temp:
                                    insert_if_not_exists(targetId, 2863405, [dict(name="_dn_max",value=cs(max(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863405, [dict(name="_dn_min",value=cs(min(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863405, [dict(name="_dn_total",value=cs(sum(dn_temp)))] )
                            elif name == 'sys076_avg_disk_ms_per_read':
                                cn_temp = []
                                dn_temp = []
                                for node_name, value in valus_dict.items():
                                    for row in value:
                                        if row != 'null' and row is not None:
                                            uid = get_uid_by_ip(node_name)
                                            if node_name in disk_io_dict.keys():
                                                disk_io_dict[node_name] += row
                                            else:
                                                disk_io_dict[node_name] = row
                                            insert_if_not_exists(uid, 2863406, cs(row))
                                            insert_if_not_exists(targetId, 2863406, [dict(name=node_name,value=cs(row))])
                                            if node_name[:2] == 'cn' or (nodes_dict.get(node_name) and "cn_" in nodes_dict.get(node_name)):
                                                cn_temp.append(row)
                                            if node_name[:2] == 'dn' or (nodes_dict.get(node_name) and "dn_" in nodes_dict.get(node_name)):
                                                dn_temp.append(row)
                                            break;
                                # 计算cn和dn的max,min,total
                                if cn_temp:
                                    insert_if_not_exists(targetId, 2863406, [dict(name="_cn_max",value=cs(max(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863406, [dict(name="_cn_min",value=cs(min(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863406, [dict(name="_cn_total",value=cs(sum(cn_temp)))])
                                if dn_temp:
                                    insert_if_not_exists(targetId, 2863406, [dict(name="_dn_max",value=cs(max(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863406, [dict(name="_dn_min",value=cs(min(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863406, [dict(name="_dn_total",value=cs(sum(dn_temp)))])
                            elif name == 'sys001_cpu_usage':
                                cn_temp = []
                                dn_temp = []
                                cpu_temp = []
                                for node_name, value in valus_dict.items():
                                    for row in value:
                                        if row != 'null' and row is not None:
                                            cpu_temp.append(row)
                                            insert_if_not_exists(get_uid_by_ip(node_name), 3000003, cs(row))
                                            insert_if_not_exists(targetId, 1001003, [dict(name=node_name,value=cs(row))])
                                            insert_if_not_exists(targetId, 2863407, [dict(name=node_name,value=cs(row))])
                                            if node_name[:2] == 'cn' or (nodes_dict.get(node_name) and "cn_" in nodes_dict.get(node_name)):
                                                cn_temp.append(row)
                                            if node_name[:2] == 'dn' or (nodes_dict.get(node_name) and "dn_" in nodes_dict.get(node_name)):
                                                dn_temp.append(row)
                                            break;
                                if cpu_temp:
                                    insert_if_not_exists(targetId, 1001003, [dict(name="max",value=cs(max(cpu_temp)))] )
                                    insert_if_not_exists(targetId, 1001003, [dict(name="min",value=cs(min(cpu_temp)))] )
                                    insert_if_not_exists(targetId, 1001003, [dict(name="avg",value=cs(round(sum(cpu_temp)/len(cpu_temp),2)))] )
                                    insert_if_not_exists(targetId, 1001003, [dict(name="std",value=cs(round(statistics.pstdev(cpu_temp),2)))] )
                                # 计算cn和dn的max,min,avg
                                # 计算cn和dn的max,min,avg
                                if cn_temp:
                                    insert_if_not_exists(targetId, 2863407, [dict(name="_cn_max",value=cs(max(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863407, [dict(name="_cn_min",value=cs(min(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863407, [dict(name="_cn_avg",value=cs(round(sum(cn_temp)/len(cn_temp),2)))])
                                if dn_temp:
                                    insert_if_not_exists(targetId, 2863407, [dict(name="_dn_max",value=cs(max(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863407, [dict(name="_dn_min",value=cs(min(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863407, [dict(name="_dn_avg",value=cs(round(sum(dn_temp)/len(dn_temp),2)))])
                            elif name == 'sys010_mem_usage':
                                cn_temp = []
                                dn_temp = []
                                mem_temp = []
                                for node_name, value in valus_dict.items():
                                    for row in value:
                                        if row != 'null' and row is not None:
                                            mem_temp.append(row)
                                            insert_if_not_exists(get_uid_by_ip(node_name), 3001026, cs(row))
                                            insert_if_not_exists(targetId, 1001004, [dict(name=node_name,value=cs(row))])
                                            insert_if_not_exists(targetId, 2863408, [dict(name=node_name,value=cs(row))])
                                            if node_name[:2] == 'cn' or (nodes_dict.get(node_name) and "cn_" in nodes_dict.get(node_name)):
                                                cn_temp.append(row)
                                            if node_name[:2] == 'dn' or (nodes_dict.get(node_name) and "dn_" in nodes_dict.get(node_name)):
                                                dn_temp.append(row)
                                            break;
                                if mem_temp:
                                    insert_if_not_exists(targetId, 1001004, [dict(name="max",value=cs(max(mem_temp)))] )
                                    insert_if_not_exists(targetId, 1001004, [dict(name="min",value=cs(min(mem_temp)))] )
                                    insert_if_not_exists(targetId, 1001004, [dict(name="avg",value=cs(round(sum(mem_temp)/len(mem_temp),2)))] )
                                # 计算cn和dn的max,min,avg
                                if cn_temp:
                                    insert_if_not_exists(targetId, 2863408, [dict(name="_cn_max",value=cs(max(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863408, [dict(name="_cn_min",value=cs(min(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863408, [dict(name="_cn_avg",value=cs(round(sum(cn_temp)/len(cn_temp),2)))])
                                if dn_temp:
                                    insert_if_not_exists(targetId, 2863408, [dict(name="_dn_max",value=cs(max(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863408, [dict(name="_dn_min",value=cs(min(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863408, [dict(name="_dn_avg",value=cs(round(sum(dn_temp)/len(dn_temp),2)))])
                            elif name == 'cpu_sys_usage':
                                cn_temp = []
                                dn_temp = []
                                for node_name, value in valus_dict.items():
                                    for row in value:
                                        if row != 'null' and row is not None:
                                            insert_if_not_exists(get_uid_by_ip(node_name), 2863409, cs(row))
                                            insert_if_not_exists(targetId, 2863409, [dict(name=node_name,value=cs(row))])
                                            if node_name[:2] == 'cn' or (nodes_dict.get(node_name) and "cn_" in nodes_dict.get(node_name)):
                                                cn_temp.append(row)
                                            if node_name[:2] == 'dn' or (nodes_dict.get(node_name) and "dn_" in nodes_dict.get(node_name)):
                                                dn_temp.append(row)
                                            break;
                                # 计算cn和dn的max,min,avg
                                if cn_temp:
                                    insert_if_not_exists(targetId, 2863409, [dict(name="_cn_max",value=cs(max(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863409, [dict(name="_cn_min",value=cs(min(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863409, [dict(name="_cn_avg",value=cs(round(sum(cn_temp)/len(cn_temp),2)))])
                                if dn_temp:
                                    insert_if_not_exists(targetId, 2863409, [dict(name="_dn_max",value=cs(max(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863409, [dict(name="_dn_min",value=cs(min(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863409, [dict(name="_dn_avg",value=cs(round(sum(dn_temp)/len(dn_temp),2)))])
                            elif name == 'cpu_user_usage':
                                cn_temp = []
                                dn_temp = []
                                for node_name, value in valus_dict.items():
                                    for row in value:
                                        if row != 'null' and row is not None:
                                            insert_if_not_exists(get_uid_by_ip(node_name), 2863410, cs(row))
                                            insert_if_not_exists(targetId, 2863410, [dict(name=node_name,value=cs(row))])
                                            if node_name[:2] == 'cn' or (nodes_dict.get(node_name) and "cn_" in nodes_dict.get(node_name)):
                                                cn_temp.append(row)
                                            if node_name[:2] == 'dn' or (nodes_dict.get(node_name) and "dn_" in nodes_dict.get(node_name)):
                                                dn_temp.append(row)
                                            break;
                                # 计算cn和dn的max,min,avg
                                if cn_temp:
                                    insert_if_not_exists(targetId, 2863410, [dict(name="_cn_max",value=cs(max(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863410, [dict(name="_cn_min",value=cs(min(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863410, [dict(name="_cn_avg",value=cs(round(sum(cn_temp)/len(cn_temp),2)))])
                                if dn_temp:
                                    insert_if_not_exists(targetId, 2863410, [dict(name="_dn_max",value=cs(max(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863410, [dict(name="_dn_min",value=cs(min(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863410, [dict(name="_dn_avg",value=cs(round(sum(dn_temp)/len(dn_temp),2)))])
                            elif name == 'sys002_idle_usage':
                                cn_temp = []
                                dn_temp = []
                                for node_name, value in valus_dict.items():
                                    for row in value:
                                        if row != 'null' and row is not None:
                                            insert_if_not_exists(get_uid_by_ip(node_name), 2863411, cs(row))
                                            insert_if_not_exists(targetId, 2863411, [dict(name=node_name,value=cs(row))])
                                            if node_name[:2] == 'cn' or (nodes_dict.get(node_name) and "cn_" in nodes_dict.get(node_name)):
                                                cn_temp.append(row)
                                            if node_name[:2] == 'dn' or (nodes_dict.get(node_name) and "dn_" in nodes_dict.get(node_name)):
                                                dn_temp.append(row)
                                            break;
                                # 计算cn和dn的max,min,avg
                                if cn_temp:
                                    insert_if_not_exists(targetId, 2863411, [dict(name="_cn_max",value=cs(max(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863411, [dict(name="_cn_min",value=cs(min(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863411, [dict(name="_cn_avg",value=cs(round(sum(cn_temp)/len(cn_temp),2)))])
                                if dn_temp:
                                    insert_if_not_exists(targetId, 2863411, [dict(name="_dn_max",value=cs(max(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863411, [dict(name="_dn_min",value=cs(min(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863411, [dict(name="_dn_avg",value=cs(round(sum(dn_temp)/len(dn_temp),2)))])
                            elif name == 'cpu_wait_usage':
                                cn_temp = []
                                dn_temp = []
                                for node_name, value in valus_dict.items():
                                    for row in value:
                                        if row != 'null' and row is not None:
                                            insert_if_not_exists(get_uid_by_ip(node_name), 2863415, cs(row))
                                            insert_if_not_exists(targetId, 2863412, [dict(name=node_name,value=cs(row))])
                                            if node_name[:2] == 'cn' or (nodes_dict.get(node_name) and "cn_" in nodes_dict.get(node_name)):
                                                cn_temp.append(row)
                                            if node_name[:2] == 'dn' or (nodes_dict.get(node_name) and "dn_" in nodes_dict.get(node_name)):
                                                dn_temp.append(row)
                                            break;
                                # 计算cn和dn的max,min,avg
                                if cn_temp:
                                    insert_if_not_exists(targetId, 2863412, [dict(name="_cn_max",value=cs(max(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863412, [dict(name="_cn_min",value=cs(min(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863412, [dict(name="_cn_avg",value=cs(round(sum(cn_temp)/len(cn_temp),2)))])
                                if dn_temp:
                                    insert_if_not_exists(targetId, 2863412, [dict(name="_dn_max",value=cs(max(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863412, [dict(name="_dn_min",value=cs(min(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863412, [dict(name="_dn_avg",value=cs(round(sum(dn_temp)/len(dn_temp),2)))])
                            elif name == 'mem_used_size':
                                cn_temp = []
                                dn_temp = []
                                for node_name, value in valus_dict.items():
                                    for row in value:
                                        if row != 'null' and row is not None:
                                            insert_if_not_exists(get_uid_by_ip(node_name), 2863416, cs(row))
                                            insert_if_not_exists(targetId, 2863416, [dict(name=node_name,value=cs(row))])
                                            if node_name[:2] == 'cn' or (nodes_dict.get(node_name) and "cn_" in nodes_dict.get(node_name)):
                                                cn_temp.append(row)
                                            if node_name[:2] == 'dn' or (nodes_dict.get(node_name) and "dn_" in nodes_dict.get(node_name)):
                                                dn_temp.append(row)
                                            break;
                                # 计算cn和dn的max,min,avg
                                if cn_temp:
                                    insert_if_not_exists(targetId, 2863416, [dict(name="_cn_max",value=cs(max(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863416, [dict(name="_cn_min",value=cs(min(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863416, [dict(name="_cn_avg",value=cs(round(sum(cn_temp)/len(cn_temp),2)))])
                                if dn_temp:
                                    insert_if_not_exists(targetId, 2863416, [dict(name="_dn_max",value=cs(max(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863416, [dict(name="_dn_min",value=cs(min(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863416, [dict(name="_dn_avg",value=cs(round(sum(dn_temp)/len(dn_temp),2)))])
                            elif name == 'sys013_mem_free_size':
                                cn_temp = []
                                dn_temp = []
                                for node_name, value in valus_dict.items():
                                    for row in value:
                                        if row != 'null' and row is not None:
                                            insert_if_not_exists(get_uid_by_ip(node_name), 2863417, cs(row))
                                            insert_if_not_exists(targetId, 2863417, [dict(name=node_name,value=cs(row))])
                                            if node_name[:2] == 'cn' or (nodes_dict.get(node_name) and "cn_" in nodes_dict.get(node_name)):
                                                cn_temp.append(row)
                                            if node_name[:2] == 'dn' or (nodes_dict.get(node_name) and "dn_" in nodes_dict.get(node_name)):
                                                dn_temp.append(row)
                                            break;
                                # 计算cn和dn的max,min,avg
                                if cn_temp:
                                    insert_if_not_exists(targetId, 2863417, [dict(name="_cn_max",value=cs(max(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863417, [dict(name="_cn_min",value=cs(min(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863417, [dict(name="_cn_avg",value=cs(round(sum(cn_temp)/len(cn_temp),2)))])
                                if dn_temp:
                                    insert_if_not_exists(targetId, 2863417, [dict(name="_dn_max",value=cs(max(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863417, [dict(name="_dn_min",value=cs(min(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863417, [dict(name="_dn_avg",value=cs(round(sum(dn_temp)/len(dn_temp),2)))])
                            elif name == 'buffer_size':
                                cn_temp = []
                                dn_temp = []
                                for node_name, value in valus_dict.items():
                                    for row in value:
                                        if row != 'null' and row is not None:
                                            insert_if_not_exists(get_uid_by_ip(node_name), 2863419, cs(row))
                                            insert_if_not_exists(targetId, 2863418, [dict(name=node_name,value=cs(row))])
                                            if node_name[:2] == 'cn' or (nodes_dict.get(node_name) and "cn_" in nodes_dict.get(node_name)):
                                                cn_temp.append(row)
                                            if node_name[:2] == 'dn' or (nodes_dict.get(node_name) and "dn_" in nodes_dict.get(node_name)):
                                                dn_temp.append(row)
                                            break;
                                # 计算cn和dn的max,min,avg
                                if cn_temp:
                                    insert_if_not_exists(targetId, 2863418, [dict(name="_cn_max",value=cs(max(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863418, [dict(name="_cn_min",value=cs(min(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863418, [dict(name="_cn_avg",value=cs(round(sum(cn_temp)/len(cn_temp),2)))])
                                if dn_temp:
                                    insert_if_not_exists(targetId, 2863418, [dict(name="_dn_max",value=cs(max(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863418, [dict(name="_dn_min",value=cs(min(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863418, [dict(name="_dn_avg",value=cs(round(sum(dn_temp)/len(dn_temp),2)))])
                            elif name == 'cache_size':
                                cn_temp = []
                                dn_temp = []
                                for node_name, value in valus_dict.items():
                                    for row in value:
                                        if row != 'null' and row is not None:
                                            insert_if_not_exists(get_uid_by_ip(node_name), 2863419, cs(row))
                                            insert_if_not_exists(targetId, 2863422, [dict(name=node_name,value=cs(row))])
                                            if node_name[:2] == 'cn' or (nodes_dict.get(node_name) and "cn_" in nodes_dict.get(node_name)):
                                                cn_temp.append(row)
                                            if node_name[:2] == 'dn' or (nodes_dict.get(node_name) and "dn_" in nodes_dict.get(node_name)):
                                                dn_temp.append(row)
                                            break;
                                # 计算cn和dn的max,min,avg
                                if cn_temp:
                                    insert_if_not_exists(targetId, 2863422, [dict(name="_cn_max",value=cs(max(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863422, [dict(name="_cn_min",value=cs(min(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863422, [dict(name="_cn_avg",value=cs(round(sum(cn_temp)/len(cn_temp),2)))])
                                if dn_temp:
                                    insert_if_not_exists(targetId, 2863422, [dict(name="_dn_max",value=cs(max(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863422, [dict(name="_dn_min",value=cs(min(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863422, [dict(name="_dn_avg",value=cs(round(sum(dn_temp)/len(dn_temp),2)))])
                            elif name == 'sys024_swap_total_size':
                                cn_temp = []
                                dn_temp = []
                                for node_name, value in valus_dict.items():
                                    for row in value:
                                        if row != 'null' and row is not None:
                                            insert_if_not_exists(get_uid_by_ip(node_name), 2863419, cs(row))
                                            insert_if_not_exists(targetId, 2863419, [dict(name=node_name,value=cs(row))])
                                            if node_name[:2] == 'cn' or (nodes_dict.get(node_name) and "cn_" in nodes_dict.get(node_name)):
                                                cn_temp.append(row)
                                            if node_name[:2] == 'dn' or (nodes_dict.get(node_name) and "dn_" in nodes_dict.get(node_name)):
                                                dn_temp.append(row)
                                            break;
                                # 计算cn和dn的max,min,avg
                                if cn_temp:
                                    insert_if_not_exists(targetId, 2863419, [dict(name="_cn_max",value=cs(max(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863419, [dict(name="_cn_min",value=cs(min(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863419, [dict(name="_cn_avg",value=cs(round(sum(cn_temp)/len(cn_temp),2)))])
                                if dn_temp:
                                    insert_if_not_exists(targetId, 2863419, [dict(name="_dn_max",value=cs(max(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863419, [dict(name="_dn_min",value=cs(min(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863419, [dict(name="_dn_avg",value=cs(round(sum(dn_temp)/len(dn_temp),2)))])
                            elif name == 'sys026_swap_used_size':
                                cn_temp = []
                                dn_temp = []
                                for node_name, value in valus_dict.items():
                                    for row in value:
                                        if row != 'null' and row is not None:
                                            insert_if_not_exists(get_uid_by_ip(node_name), 2863419, cs(row))
                                            insert_if_not_exists(targetId, 2863420, [dict(name=node_name,value=cs(row))])
                                            if node_name[:2] == 'cn' or (nodes_dict.get(node_name) and "cn_" in nodes_dict.get(node_name)):
                                                cn_temp.append(row)
                                            if node_name[:2] == 'dn' or (nodes_dict.get(node_name) and "dn_" in nodes_dict.get(node_name)):
                                                dn_temp.append(row)
                                            break;
                                # 计算cn和dn的max,min,avg
                                if cn_temp:
                                    insert_if_not_exists(targetId, 2863420, [dict(name="_cn_max",value=cs(max(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863420, [dict(name="_cn_min",value=cs(min(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863420, [dict(name="_cn_avg",value=cs(round(sum(cn_temp)/len(cn_temp),2)))])
                                if dn_temp:
                                    insert_if_not_exists(targetId, 2863420, [dict(name="_dn_max",value=cs(max(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863420, [dict(name="_dn_min",value=cs(min(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863420, [dict(name="_dn_avg",value=cs(round(sum(dn_temp)/len(dn_temp),2)))])
                            elif name == 'sys025_swap_used_ratio':
                                cn_temp = []
                                dn_temp = []
                                swap_temp = []
                                for node_name, value in valus_dict.items():
                                    for row in value:
                                        if row != 'null' and row is not None:
                                            swap_temp.append(row)
                                            insert_if_not_exists(get_uid_by_ip(node_name), 3001031, cs(row))
                                            insert_if_not_exists(targetId, 1001022, [dict(name=node_name,value=cs(row))])
                                            insert_if_not_exists(targetId, 1001031, [dict(name=node_name,value=cs(row))])
                                            insert_if_not_exists(targetId, 2863421, [dict(name=node_name,value=cs(row))])
                                            if node_name[:2] == 'cn' or (nodes_dict.get(node_name) and "cn_" in nodes_dict.get(node_name)):
                                                cn_temp.append(row)
                                            if node_name[:2] == 'dn' or (nodes_dict.get(node_name) and "dn_" in nodes_dict.get(node_name)):
                                                dn_temp.append(row)
                                            break;
                                if swap_temp:
                                    insert_if_not_exists(targetId, 1001022, [dict(name="max",value=cs(max(swap_temp)))] )
                                    insert_if_not_exists(targetId, 1001022, [dict(name="min",value=cs(min(swap_temp)))] )
                                    insert_if_not_exists(targetId, 1001022, [dict(name="avg",value=cs(round(sum(swap_temp)/len(swap_temp),2)))])
                                    insert_if_not_exists(targetId, 1001031, [dict(name="max",value=cs(max(swap_temp)))] )
                                    insert_if_not_exists(targetId, 1001031, [dict(name="min",value=cs(min(swap_temp)))] )
                                    insert_if_not_exists(targetId, 1001031, [dict(name="avg",value=cs(round(sum(swap_temp)/len(swap_temp),2)))])
                                # 计算cn和dn的max,min,avg
                                # 计算cn和dn的max,min,avg
                                if cn_temp:
                                    insert_if_not_exists(targetId, 2863421, [dict(name="_cn_max",value=cs(max(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863421, [dict(name="_cn_min",value=cs(min(cn_temp)))] )
                                    insert_if_not_exists(targetId, 2863421, [dict(name="_cn_avg",value=cs(round(sum(cn_temp)/len(cn_temp),2)))])
                                if dn_temp:
                                    insert_if_not_exists(targetId, 2863421, [dict(name="_dn_max",value=cs(max(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863421, [dict(name="_dn_min",value=cs(min(dn_temp)))] )
                                    insert_if_not_exists(targetId, 2863421, [dict(name="_dn_avg",value=cs(round(sum(dn_temp)/len(dn_temp),2)))])
                        if disk_io_dict:
                            io_tmp = []
                            for node_name, row in disk_io_dict.items():
                                io_tmp.append(row)
                                uid = get_uid_by_ip(node_name)
                                insert_if_not_exists(uid, 3000006, cs(row))
                                insert_if_not_exists(targetId, 1001006, [dict(name=node_name,value=cs(row))])
                            # 平均值、最大值、最小值、标准差
                            if io_tmp:
                                insert_if_not_exists(targetId, 1001006, [dict(name="max",value=cs(max(io_tmp)))])
                                insert_if_not_exists(targetId, 1001006, [dict(name="min",value=cs(min(io_tmp)))])
                                insert_if_not_exists(targetId, 1001006, [dict(name="avg",value=cs(round(sum(io_tmp)/len(io_tmp),2)))])
                                insert_if_not_exists(targetId, 1001006, [dict(name="std",value=cs(round(statistics.pstdev(io_tmp),2)))] )
                        if disk_throughput_dict:
                            thro_tmp = []
                            for node_name, row in disk_throughput_dict.items():
                                thro_tmp.append(row)
                                uid = get_uid_by_ip(node_name)
                                insert_if_not_exists(uid, 3000101, cs(row))
                                insert_if_not_exists(targetId, 1001101, [dict(name=node_name,value=cs(row))])
                            # 平均值、最大值、最小值
                            if thro_tmp:
                                insert_if_not_exists(targetId, 1001101, [dict(name="max",value=cs(max(thro_tmp)))])
                                insert_if_not_exists(targetId, 1001101, [dict(name="min",value=cs(min(thro_tmp)))])
                                insert_if_not_exists(targetId, 1001101, [dict(name="avg",value=cs(round(sum(thro_tmp)/len(thro_tmp),2)))])
                    else:
                        print(metric_out)
            if is_cloud:
                insert_if_not_exists(targetId, index_id="2863301", value=cs(failed_dns))
                insert_if_not_exists(targetId, index_id="2863424", value=cs(total_dns))
                insert_if_not_exists(targetId, index_id="2863302", value=cs(failed_cns))
                insert_if_not_exists(targetId, index_id="2863425", value=cs(total_cns))
                insert_if_not_exists(targetId, index_id="2863303", value=cs(failed_gtms))
                insert_if_not_exists(targetId, index_id="2863427", value=cs(total_gtms))
                insert_if_not_exists(targetId, index_id="2863304", value=cs(failed_etcd))
                insert_if_not_exists(targetId, index_id="2863428", value=cs(total_etcd))
                insert_if_not_exists(targetId, index_id="28633423", value=cs(failed_cms))
                insert_if_not_exists(targetId, index_id="2863426", value=cs(total_cms))
                insert_if_not_exists(targetId, index_id="2863434", value=cs(failed_info))
        else:
            insert_if_not_exists(targetId, index_id="2863435", value=cs(instance_info.json()['error_msg']))


def cloud_conn(gs):
    sql = "select node_host,node_port,nodeis_active from pgxc_node"
    cursor = DBUtil.getValue(gs, sql)
    result = cursor.fetchall()
    if result:
        for row in result:
            node_ip = row[0]
            port = row[1]
            nodeis_active = row[2]
            uid = get_uid_by_ip(node_ip, port)
            if nodeis_active:
                insert_if_not_exists(uid, index_id="2860000", value='连接成功')
            else:
                insert_if_not_exists(uid, index_id="2860000", value='连接失败')


if __name__ == '__main__':
    metric = []
    global_metric = []
    cur_time = datetime.now()
    dbInfo = eval(sys.argv[1])
    gs_ip = dbInfo['target_ip']
    role = 'Primary'
    targetId, pg = DBUtil.get_pg_env()
    # 查看集群类型
    cluster_type = DBUtil.get_gauss_type(pg, targetId)     # centralized, distributed
    dsc = DBUtil.get_gbase_dcs(pg, targetId) 
    lat_time = datetime.now()
    diff_ms = (lat_time - cur_time).microseconds
    insert_if_not_exists(targetId, 1000101, str(round(diff_ms/1000,0)))
    gs_conn = DBUtil.get_gaussdb_env(exflag=2)
    if gs_conn.conn:
        insert_if_not_exists(targetId, 2860000, "连接成功")
        is_cloud = DBUtil.gauss_is_cloud(pg, targetId)
        get_metric_from_tpops(is_cloud)
        if cluster_type == 'distributed':
            pgxc_metric(pg, targetId, gs_conn)
            if not is_cloud and dsc:
                cluster_info(pg, gs_ip, dsc)
            cloud_conn(gs_conn)
            wait_event(pg, gs_conn)
            cns_nodes = DBUtil.get_all_cn_envs()
            collect_all_cns(cns_nodes)
        else:
            # 获取所有节点连接信息
            if not is_cloud and dsc:
                nodes_info = cluster_info(pg, gs_ip, dsc)
                if nodes_info:
                    for row in nodes_info:
                        for key, value in row.items():
                            exist_primary = False
                            for dn_r in value:  # 同一个组的datanode
                                ip = dn_r['host_ip']
                                port = dn_r['port']
                                role = dn_r['role']
                                if role in ('Primary', 'Standby'):
                                    read_only = False if role == 'Primary' else True
                                    uid = get_uid_by_ip(ip, port)
                                    dn_conn = DBUtil.get_dn_conn(targetId, ip, port,read_only)
                                    pgxc_metric(pg, targetId, dn_conn, uid)
                                    wait_event(pg, dn_conn, uid)
            else:
                ip = dbInfo['target_ip']
                port = dbInfo['target_port']
                uid = get_uid_by_ip(ip, port)
                pgxc_metric(pg, targetId, gs_conn, uid)
                wait_event(pg, gs_conn, uid)
    else:
        insert_if_not_exists(targetId, 2860000, "连接失败")
    lat_time2 = datetime.now()
    diff_ms2 = (lat_time2 - cur_time).microseconds
    role = 'Primary'
    insert_if_not_exists(targetId, 1000102, str(round(diff_ms2/1000,0)))
    print(json.dumps(global_metric,ensure_ascii=False))
    try:
        DBUtil.update_gauss_config(pg)   # 更新主从角色
    except Exception as e:
        pass

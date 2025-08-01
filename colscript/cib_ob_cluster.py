import sys

sys.path.append('/usr/software/knowl')
import DBUtil
import datetime
import json
import sshSession
import os_svc

global version
srvs = []


def cs(val, dt=False):
    if val is None:
        return ''
    else:
        if dt:
            return val.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return str(val)


def microsecond2date(mircosec):
    timestamp_to_date_time = datetime.datetime.fromtimestamp(mircosec / 1000000).strftime(
        '%Y-%m-%d %H:%M:%S.%f')
    return timestamp_to_date_time


def ob_version(db):
    global version
    sql = '''select max(BUILD_VERSION) from __all_server'''
    cs = DBUtil.getValue(db, sql)
    version = cs.fetchone()[0].split('_')[0]
    return version

def cib_basic(db, metric, target_id, pg, tenant_type, tenant_name):
    global version
    vals = []
    sql = "delete from p_normal_cib where target_id='%s' and index_id=1000005 and cib_name in ('version','toolType')" % target_id
    pg.execute(sql)
    pg.conn.commit()
    sql = """insert into p_normal_cib(target_id,index_id,cib_name,cib_value,record_time) values('%s',1000005,'version','%s',now()),
    ('%s',1000005,'toolType','cluster',now())""" % (target_id, version, target_id)
    pg.execute(sql)
    pg.conn.commit()
    sql2 = '''select col2,col3,col5,col7,col8,col9,col10 from p_oracle_cib where target_id='{0}' and index_id='2801009' and col2='{1}' '''.format(
        target_id, tenant_name)
    cs2 = DBUtil.getValue(pg, sql2)
    rs2 = cs2.fetchone()
    if rs2:
        vals.append(dict(name='tenant_name', value=rs2[0]))
        vals.append(dict(name='status', value=rs2[1]))
        vals.append(dict(name='created', value=rs2[1]))
        vals.append(dict(name='read_only', value=rs2[2]))
        vals.append(dict(name='zone_list', value=rs2[3]))
        vals.append(dict(name='primary_zone', value=rs2[5]))
        vals.append(dict(name='locality', value=rs2[6]))
    vals.append(dict(name='tenant_type', value=tenant_type))
    sql3 = '''select cib_name,cib_value from p_oracle_cib where target_id='{0}' and index_id='2801015' '''.format(target_id)
    cs3 = DBUtil.getValue(pg, sql3)
    rs3 = cs3.fetchall()
    if rs3:
        for row in rs3:
            vals.append(dict(name=row[0], value=row[1]))
    if version < '4.0':
        vals.append(dict(name='version', value=version))
        sql = '''select * from v$ob_cluster'''
        cs1 = DBUtil.getValue(db, sql)
        row = cs1.fetchone()
        cluster_id = row[0]
        cluster_name = row[1]
        created = row[2]
        cluster_role = row[3]
        cluster_status = row[4]
        switchover_cnt = row[5]
        switchover_status = row[6]
        switchover_info = row[7]
        protection_mode = row[11]
        current_scn = row[8]
        redo_transport_options = row[13]
        vals.append(dict(name='cluster_id', value=cluster_id))
        vals.append(dict(name='cluster_name', value=cluster_name))
        vals.append(dict(name='created', value=created))
        vals.append(dict(name='cluster_role', value=cluster_role))
        vals.append(dict(name='cluster_status', value=cluster_status))
        vals.append(dict(name='switchover_cnt', value=switchover_cnt))
        vals.append(dict(name='switchover_status', value=switchover_status))
        vals.append(dict(name='switchover_info', value=switchover_info))
        vals.append(dict(name='protection_mode', value=protection_mode))
        vals.append(dict(name='current_scn', value=current_scn))
        vals.append(dict(name='redo_transport_options', value=redo_transport_options))
        vals.append(dict(name='role', value='cluster'))
        metric.append(dict(index_id="2801001", value=vals))
        return cluster_id
    else:
        sql = '''select distinct name,value from __all_virtual_tenant_parameter_stat t2 where name like 'cluster%' '''
        cs1 = DBUtil.getValue(db, sql)
        rs1 = cs1.fetchall()
        if rs1:
            for row in rs1:
                if row[0] == 'cluster_id':
                    cluster_id = row[1]
                elif row[0] == 'cluster':
                    cluster_name = row[1]
            vals.append(dict(name='version', value=version))
            vals.append(dict(name='cluster_id', value=cluster_id))
            vals.append(dict(name='cluster_name', value=cluster_name))
            vals.append(dict(name='role', value='cluster'))
        metric.append(dict(index_id="2801001", value=vals))
        return cluster_id


def cib_tenant_basic(db, cluster_target_id, tenant_name, tenant_type):
    vals = []
    sql1 = '''select cib_name,cib_value from p_oracle_cib where target_id='{0}' and index_id='2801001' '''.format(
        cluster_target_id)
    cs1 = DBUtil.getValue(db, sql1)
    rs1 = cs1.fetchall()
    sql2 = '''select col2,col3,col5,col7,col8,col9,col10 from p_oracle_cib where target_id='{0}' and index_id='2801009' and col2='{1}' '''.format(
        cluster_target_id, tenant_name)
    cs2 = DBUtil.getValue(db, sql2)
    rs2 = cs2.fetchone()
    if rs2:
        vals.append(dict(name='tenant_name', value=rs2[0]))
        vals.append(dict(name='status', value=rs2[1]))
        vals.append(dict(name='created', value=rs2[1]))
        vals.append(dict(name='read_only', value=rs2[2]))
        vals.append(dict(name='zone_list', value=rs2[3]))
        vals.append(dict(name='primary_zone', value=rs2[5]))
        vals.append(dict(name='locality', value=rs2[6]))
    if rs1:
        for row in rs1:
            if row[0] == 'cluster_name':
                vals.append(dict(name=row[0], value=tenant_name))
            elif row[0] == 'role':
                vals.append(dict(name=row[0], value='tenant'))
            else:
                vals.append(dict(name=row[0], value=row[1]))
    vals.append(dict(name='tenant_type', value=tenant_type))
    sql3 = '''select cib_name,cib_value from p_oracle_cib where target_id='{0}' and index_id='2801015' '''.format(cluster_target_id)
    cs3 = DBUtil.getValue(db, sql3)
    rs3 = cs3.fetchall()
    for row in rs3:
        vals.append(dict(name=row[0], value=row[1]))
    metric.append(dict(index_id="2801001", value=vals))


def cib_parameter(db, metric):
    vals = []
    kernel_vals = []
    kernel_parameters = ["audit_sys_operations", "audit_trail", "balancer_idle_time", "backup_dest",
                         "backup_dest_option", "backup_zone", "builtin_db_data_verify_cycle",
                         "bf_cache_miss_count_threshold", "bf_cache_priority", "cache_wash_threshold",
                         "clog_cache_priority", "clog_sync_time_warn_threshold", "clog_disk_usage_limit_percentage",
                         "clog_expire_days", "cpu_count", "cpu_reserved", "config_additional_dir", "data_dir",
                         "default_row_format", "data_disk_usage_limit_percentage", "enable_clog_persistence_compress",
                         "enable_pg", "enable_smooth_leader_switch", "enable_perf_event", "enable_rebalance",
                         "enable_record_trace_log", "enable_early_lock_release", "enable_rereplication",
                         "enable_rootservice_standalone", "enable_sql_audit", "enable_syslog_recycle",
                         "enable_syslog_wf", "freeze_trigger_percentage", "flush_log_at_trx_commit",
                         "fuse_row_cache_priority", "global_major_freeze_residual_memory",
                         "global_write_halt_residual_memory", "large_query_worker_percentage", "large_query_threshold",
                         "log_archive_concurrency", "major_freeze_duty_time", "max_syslog_file_count",
                         "major_compact_trigger", "memory_limit", "memory_reserved",
                         "memory_limit_percentage", "merger_completion_percentage", "max_px_worker_count",
                         "minor_freeze_times", "mysql_port", "minor_compact_trigger", "memstore_limit_percentage",
                         "rootservice_list", "rootservice_memory_limit", "system_memory", "sql_audit_memory_limit",
                         "syslog_level", "system_cpu_quota", "sys_cpu_limit_trigger", "system_trace_level",
                         "use_large_pages", "open_cursors", "enable_tcp_keepalive",
                         "data_storage_warning_tolerance_time", "__easy_memory_limit"]
    sql = '''select zone,svr_type,svr_ip,svr_port,name,value,scope,visible_level,edit_level from __all_virtual_sys_parameter_stat'''
    cs1 = DBUtil.getValue(db, sql)
    parameter_set = set()
    rs1 = cs1.fetchall()
    for row in rs1:
        parameter_set.add(row[4])
    ddir = None
    for para in parameter_set:
        values = {}
        for row in rs1:
            if row[4] == para:
                values[row[2] + ':' + str(row[3])] = row[5]
                if para == 'data_dir':
                    if ddir:
                        ddir += ',' + row[2] + ':' + str(row[3]) + '=' + row[5]
                    else:
                        ddir = row[2] + ':' + str(row[3]) + '=' + row[5]
        # value_set = set(values.values())
        # if len(value_set) == 1:
        #     para_name = para + '(all)'
        #     value = list(value_set)[0]
        #     vals.append(dict(name=para_name, value=value))
        #     if para in kernel_parameters:
        #         kernel_vals.append(dict(name=para_name, value=value))
        # else:
        for k, v in values.items():
            para_name = para + '(' + k + ')'
            vals.append(dict(name=para_name, value=v))
            if para in kernel_parameters:
                kernel_vals.append(dict(name=para_name, value=v))
    metric.append(dict(index_id="2801002", value=vals))
    metric.append(dict(index_id="2801003", value=kernel_vals))
    return ddir


def cib_tenant_parameter(db, metric, tenant_type):
    vals = []
    kernel_vals = []
    kernel_parameters = ["audit_sys_operations", "audit_trail", "balancer_idle_time", "backup_dest",
                         "backup_dest_option", "backup_zone", "builtin_db_data_verify_cycle",
                         "bf_cache_miss_count_threshold", "bf_cache_priority", "cache_wash_threshold",
                         "clog_cache_priority", "clog_sync_time_warn_threshold", "clog_disk_usage_limit_percentage",
                         "clog_expire_days", "cpu_count", "cpu_reserved", "config_additional_dir", "data_dir",
                         "default_row_format", "data_disk_usage_limit_percentage", "enable_clog_persistence_compress",
                         "enable_pg", "enable_smooth_leader_switch", "enable_perf_event", "enable_rebalance",
                         "enable_record_trace_log", "enable_early_lock_release", "enable_rereplication",
                         "enable_rootservice_standalone", "enable_sql_audit", "enable_syslog_recycle",
                         "enable_syslog_wf", "freeze_trigger_percentage", "flush_log_at_trx_commit",
                         "fuse_row_cache_priority", "global_major_freeze_residual_memory",
                         "global_write_halt_residual_memory", "large_query_worker_percentage", "large_query_threshold",
                         "log_archive_concurrency", "major_freeze_duty_time", "max_syslog_file_count",
                         "major_compact_trigger", "memory_limit", "memory_limit_percentage", "memory_reserved",
                         "memory_limit_percentage", "merger_completion_percentage", "max_px_worker_count",
                         "minor_freeze_times", "mysql_port", "minor_compact_trigger", "memstore_limit_percentage",
                         "rootservice_list", "rootservice_memory_limit", "system_memory", "sql_audit_memory_limit",
                         "syslog_level", "system_cpu_quota", "sys_cpu_limit_trigger", "system_trace_level",
                         "use_large_pages", "open_cursors", "enable_tcp_keepalive",
                         "data_storage_warning_tolerance_time", "__easy_memory_limit"]
    if tenant_type == 'mysql':
        sql = '''select zone,svr_type,svr_ip,svr_port,name,value,scope,edit_level from __all_virtual_tenant_parameter_stat'''
    else:
        sql = '''select zone,svr_type,svr_ip,svr_port,name,value,scope,edit_level from all_VIRTUAL_SYS_PARAMETER_STAT_AGENT'''
    cs1 = DBUtil.getValue(db, sql)
    parameter_set = set()
    rs1 = cs1.fetchall()
    for row in rs1:
        parameter_set.add(row[4])
    for para in parameter_set:
        values = {}
        for row in rs1:
            if row[4] == para:
                values[row[2] + ':' + str(row[3])] = row[5]
        # value_set = set(values.values())
        # if len(value_set) == 1:
        #     para_name = para + '(all)'
        #     value = list(value_set)[0]
        #     vals.append(dict(name=para_name, value=value))
        #     if para in kernel_parameters:
        #         kernel_vals.append(dict(name=para_name, value=value))
        # else:
        for k, v in values.items():
            para_name = para + '(' + k + ')'
            vals.append(dict(name=para_name, value=v))
            if para in kernel_parameters:
                kernel_vals.append(dict(name=para_name, value=v))
    metric.append(dict(index_id="2801002", value=vals))
    metric.append(dict(index_id="2801003", value=kernel_vals))


def cib_variables(db, metric):
    vals = []
    kernel_vals = []
    kernel_variables = ["autocommit", "interactive_timeout", "max_allowed_packet", "sql_mod", "time_zone",
                        "tx_isolation", "wait_timeout", "binlog_row_image", "connect_timeout", "datadir",
                        "lower_case_table_names", "read_only", "version", "max_user_connections", "query_cache_type",
                        "ob_default_replica_num", "ob_proxy_partition_hit", "ob_log_level", "ob_max_parallel_degree",
                        "ob_query_timeout", "ob_read_consistency", "ob_enable_transformation", "ob_trx_timeout",
                        "ob_enable_plan_cache", "ob_plan_cache_percentage", "recyclebin", "ob_compatibility_mode",
                        "ob_sql_work_area_percentage", "ob_enable_truncate_flashback", "auto_increment_cache_size",
                        "undo_retention", "ob_sql_audit_percentage", "ob_enable_sql_audit",
                        "optimizer_capture_sql_plan_baselines", "optimizer_use_sql_plan_baselines",
                        "parallel_max_servers", "ob_trx_idle_timeout", "nls_date_format", "nls_language",
                        "nls_characterset", "transaction_isolation", "ob_trx_lock_timeout", "performance_schema"]
    sql = '''select name,value from __all_sys_variable'''
    cs1 = DBUtil.getValue(db, sql)
    rs1 = cs1.fetchall()
    for row in rs1:
        if row[0] in kernel_variables:
            kernel_vals.append(dict(name=row[0], value=row[1]))
        vals.append(dict(name=row[0], value=row[1]))
    metric.append(dict(index_id="2801004", value=vals))
    metric.append(dict(index_id="2801005", value=kernel_vals))


def cib_tenant_variables(db, metric, tenant_type):
    vals = []
    kernel_vals = []
    kernel_variables = ["autocommit", "interactive_timeout", "max_allowed_packet", "sql_mod", "time_zone",
                        "tx_isolation", "wait_timeout", "binlog_row_image", "connect_timeout", "datadir",
                        "lower_case_table_names", "read_only", "version", "max_user_connections", "query_cache_type",
                        "ob_default_replica_num", "ob_proxy_partition_hit", "ob_log_level", "ob_max_parallel_degree",
                        "ob_query_timeout", "ob_read_consistency", "ob_enable_transformation", "ob_trx_timeout",
                        "ob_enable_plan_cache", "ob_plan_cache_percentage", "recyclebin", "ob_compatibility_mode",
                        "ob_sql_work_area_percentage", "ob_enable_truncate_flashback", "auto_increment_cache_size",
                        "undo_retention", "ob_sql_audit_percentage", "ob_enable_sql_audit",
                        "optimizer_capture_sql_plan_baselines", "optimizer_use_sql_plan_baselines",
                        "parallel_max_servers", "ob_trx_idle_timeout", "nls_date_format", "nls_language",
                        "nls_characterset", "transaction_isolation", "ob_trx_lock_timeout", "performance_schema"]
    if tenant_type == 'mysql':
        sql = '''select * from __tenant_virtual_global_variable'''
    else:
        sql = '''select * from TENANT_VIRTUAL_GLOBAL_VARIABLE'''
    cs1 = DBUtil.getValue(db, sql)
    rs1 = cs1.fetchall()
    for row in rs1:
        if row[0] in kernel_variables:
            kernel_vals.append(dict(name=row[0], value=row[1]))
        vals.append(dict(name=row[0], value=row[1]))
    metric.append(dict(index_id="2801004", value=vals))
    metric.append(dict(index_id="2801005", value=kernel_vals))


def cib_zone(db, metric):
    global version
    vals = []
    if version < '4.0':
        sql = '''select * from __all_zone where length(zone)>0'''
        sql2 = '''select * from __all_virtual_zone_stat'''
        cs1 = DBUtil.getValue(db, sql)
        rs = cs1.fetchall()
        cs2 = DBUtil.getValue(db, sql2)
        rs2 = cs2.fetchall()
        zone_lst = []
        for row in rs2:
            zone_lst.append(row[0])

        vals.append(
            dict(c1='ZONE_NAME', c2='ZONE_TYPE', c3='STORAGE_TYPE', c4='STATUS', c5='REGION', c6='RECOVERY_STATUS',
                 c7='MERGE_STATUS', c8='SERVER_COUNT', c9='RESOURCE_POOL_COUNT', c10='UNIT_COUNT'))
        for zone in zone_lst:
            zone_dict = {'zone_type': 0, 'storage_type': 0, 'storage_type': 0, 'status': 0, 'region': 0,
                         'recovery_status': 0,
                         'merge_status': 0}
            for row1 in rs:
                if row1[2] == zone:
                    zone_dict['zone_name'] = zone
                    for k, v in zone_dict.items():
                        if k == row1[3]:
                            zone_dict[k] = row1[5]
            for row2 in rs2:
                if row2[0] == zone:
                    zone_dict['server_count'] = row2[3]
                    zone_dict['resource_pool_count'] = row2[4]
                    zone_dict['unit_count'] = row2[5]
            vals.append(
                dict(c1=cs(zone_dict['zone_name']), c2=cs(zone_dict['zone_type']), c3=cs(zone_dict['storage_type']),
                     c4=cs(zone_dict['status']), c5=cs(zone_dict['region']), c6=cs(zone_dict['recovery_status']),
                     c7=cs(zone_dict['merge_status']), c8=cs(zone_dict['server_count']),
                     c9=cs(zone_dict['resource_pool_count']),
                     c10=cs(zone_dict['unit_count'])))
        metric.append(dict(index_id="2801006", content=vals))
    else:
        sql = '''select * from __all_zone where length(zone)>0'''
        sql2 = '''select * from dba_ob_zones'''
        cs1 = DBUtil.getValue(db, sql)
        rs = cs1.fetchall()
        cs2 = DBUtil.getValue(db, sql2)
        rs2 = cs2.fetchall()
        zone_lst = []
        for row in rs2:
            zone_lst.append(row[0])
        vals.append(
            dict(c1='ZONE_NAME', c2='ZONE_TYPE', c3='STORAGE_TYPE', c4='STATUS', c5='REGION', c6='RECOVERY_STATUS',
                 c7='MERGE_STATUS'))
        for zone in zone_lst:
            zone_dict = {'zone_type': 0, 'storage_type': 0, 'storage_type': 0, 'status': 0, 'region': 0,
                         'recovery_status': 0}
            for row1 in rs:
                if row1[2] == zone:
                    zone_dict['zone_name'] = zone
                    for k, v in zone_dict.items():
                        if k == row1[3]:
                            zone_dict[k] = row1[5]
            vals.append(
                dict(c1=cs(zone_dict['zone_name']), c2=cs(zone_dict['zone_type']), c3=cs(zone_dict['storage_type']),
                     c4=cs(zone_dict['status']), c5=cs(zone_dict['region']), c6=cs(zone_dict['recovery_status'])))
        metric.append(dict(index_id="2801006", content=vals))


def cib_observer1(db, metric):
    vals = []
    global version
    if version < '4.0':
        sql1 = '''select t2.id,t3.svr_ip,t3.svr_port,t3.inner_port,t3.status,t2.heartbeat_status,t3.gmt_create,t3.gmt_modified,t2.start_service_time,t2.last_heartbeat_time from  __all_virtual_zone_stat t1,__all_virtual_server_stat t2,__all_server t3 where t1.zone=t2.zone and t2.zone=t3.zone and t2.id=t3.id order by 1'''
        cs1 = DBUtil.getValue(db, sql1)
        rs1 = cs1.fetchall()
        vals.append(
            dict(c1='id', c2='svr_ip', c3='svr_port', c4='inner_port', c5='status', c6='heartbeat_status',
                 c7='create_time', c8='modified_time', c9='start_service_time', c10='last_heartbeat_time'))
        for row in rs1:
            row_lst = list(row)
            row_lst[8] = microsecond2date(row_lst[8])
            row_lst[9] = microsecond2date(row_lst[9])
            vals.append(
                dict(c1=row_lst[0], c2=cs(row_lst[1]), c3=row_lst[2], c4=row_lst[3], c5=cs(row_lst[4]), c6=row_lst[5],
                     c7=cs(row_lst[6]), c8=cs(row_lst[7]), c9=cs(row_lst[8]), c10=cs(row_lst[9])))
    
    else:
        sql1 = '''select id,svr_ip, svr_port, sql_port, status,CREATE_TIME, MODIFY_TIME , START_SERVICE_TIME ,WITH_ROOTSERVER  from DBA_OB_SERVERS'''
        cs1 = DBUtil.getValue(db, sql1)
        rs1 = cs1.fetchall()
        vals.append(
            dict(c1='id', c2='svr_ip', c3='svr_port', c4='sql_port', c5='status', c6='CREATE_TIME',
                 c7='MODIFY_TIME', c8='START_SERVICE_TIME', c9='WITH_ROOTSERVER'))
        for row in rs1:
            vals.append(
                dict(c1=row[0], c2=cs(row[1]), c3=row[2], c4=row[3], c5=cs(row[4]), c6=cs(row[5]),
                     c7=cs(row[6]), c8=cs(row[7]), c9=cs(row[8])))
    metric.append(dict(index_id="2801007", content=vals))


def cib_observer2(db, metric):
    global version
    global srvs
    vals = []
    cpu_total = 0
    cpu_assigned = 0
    if version < '4.0':
        sql1 = '''select t2.id,t2.svr_ip,t2.svr_port,t2.cpu_total,t2.cpu_assigned,round(t2.mem_total/1024/1024/1024,1) mem_total_GB,round(t2.mem_assigned/1024/1024/1024,1) mem_assigned_GB,round(t2.disk_total/1024/1024/1024,1) disk_total_GB,
    round(t2.disk_in_use/1024/1024/1024,2) disk_in_use_GB,t2.unit_num from  __all_virtual_server_stat t2'''
        cs1 = DBUtil.getValue(db, sql1)
        rs1 = cs1.fetchall()
        vals.append(
            dict(c1='id', c2='svr_ip', c3='svr_port', c4='cpu_total', c5='cpu_assigned', c6='mem_total_GB',
                 c7='mem_assigned_GB', c8='disk_total_GB', c9='disk_in_use_GB', c10='unit_num'))
        for row in rs1:
            srvs.append(row[1])
            cpu_total += float(row[3])
            cpu_assigned += float(row[4])
            vals.append(dict(c1=row[0], c2=cs(row[1]), c3=row[2], c4=row[3], c5=cs(row[4]), c6=row[5], c7=cs(row[6]),
                             c8=cs(row[7]), c9=cs(row[8]), c10=cs(row[9])))
    else:
        sql1 = '''select t2.id,
            t1.svr_ip,
            cpu_capacity,
            cpu_assigned,
            round(mem_capacity / 1024 / 1024 / 1024,2) mem_total_GB,
            round(mem_assigned / 1024 / 1024 / 1024,2) mem_assigned_GB,
            round(data_disk_capacity / 1024 / 1024 / 1024,2) data_disk_total_GB,
            round(data_disk_in_use / 1024 / 1024 / 1024,2) data_disk_in_use_GB, 
            round(log_disk_capacity / 1024 / 1024 / 1024,2) log_disk_total_GB,
            round(log_disk_in_use / 1024 / 1024 / 1024,2) log_disk_in_use_GB	
        from
            __all_virtual_server t1, DBA_OB_SERVERS t2 where t1.svr_ip = t2.SVR_IP and t1.svr_port=t2.SVR_PORT order by 1'''
        cs1 = DBUtil.getValue(db, sql1)
        rs1 = cs1.fetchall()
        vals.append(
            dict(c1='id', c2='svr_ip', c3='cpu_total', c4='cpu_assigned', c5='mem_total_GB',
                 c6='mem_assigned_GB', c7='data_disk_total_GB', c8='data_disk_in_use_GB', c9='log_disk_total_GB',
                 c10='log_disk_in_use_GB'))
        for row in rs1:
            srvs.append(row[1])
            cpu_total += float(row[2])
            cpu_assigned += float(row[3])
            vals.append(dict(c1=row[0], c2=cs(row[1]), c3=row[2], c4=row[3], c5=cs(row[4]), c6=row[5], c7=cs(row[6]),
                             c8=cs(row[7]), c9=cs(row[8]), c10=cs(row[9])))
    metric.append(dict(index_id="2801008", content=vals))
    metric.append(dict(index_id="2801015", value=[{'name': 'cpu_total', 'value': cpu_total},
                                                  {'name': 'cpu_assigned', 'value': cpu_assigned},
                                                  {'name': 'observer_numbers', 'value': len(rs1)}
                                                  ]))


def cib_tenant(db, metric):
    vals = []
    global version
    if version < '4.0':
        sql1 = '''select tenant_id,tenant_name,gmt_create,info,status,locked,read_only,zone_list,primary_zone,locality from __all_tenant'''
        cs1 = DBUtil.getValue(db, sql1)
        rs1 = cs1.fetchall()
        vals.append(
            dict(c1='tenant_id', c2='tenant_name', c3='create_time', c4='info', c5='status', c6='locked',
                 c7='read_only', c8='zone_list', c9='primary_zone', c10='locality'))
        for row in rs1:
            vals.append(dict(c1=row[0], c2=cs(row[1]), c3=row[2], c4=row[3], c5=cs(row[4]), c6=row[5], c7=cs(row[6]),
                             c8=cs(row[7]), c9=cs(row[8]), c10=cs(row[9])))
    else:
        sql1 = '''select dot.tenant_id,dot.tenant_name,create_time,t.info, dot.status, dot.LOCKED, '', zone_list, dot.PRIMARY_ZONE, dot.LOCALITY from DBA_OB_TENANTS dot, __all_tenant t where tenant_type != 'META'
and dot.tenant_id=t.tenant_id '''
        cs1 = DBUtil.getValue(db, sql1)
        rs1 = cs1.fetchall()
        vals.append(
            dict(c1='tenant_id', c2='tenant_name', c3='create_time', c4='info', c5='status', c6='locked',
                 c7='read_only', c8='zone_list', c9='primary_zone', c10='locality'))
        for row in rs1:
            vals.append(dict(c1=row[0], c2=cs(row[1]), c3=row[2], c4=row[3], c5=cs(row[4]), c6=row[5], c7=cs(row[6]),
                             c8=cs(row[7]), c9=cs(row[8]), c10=cs(row[9])))
    metric.append(dict(index_id="2801009", content=vals))


def cib_schema(db, metric):
    vals = []
    sql1 = '''select svr_ip,svr_port,tenant_id from __all_virtual_server_schema_info'''
    cs1 = DBUtil.getValue(db, sql1)
    rs1 = cs1.fetchall()
    vals.append(
        dict(c1='schema_id', c2='svr_ip', c3='svr_port', c4='tenant_id'))
    for row in rs1:
        schema_id = str(row[2]) + '_' + str(row[0]) + '_' + str(row[1])
        vals.append(dict(c1=cs(schema_id), c2=cs(row[0]), c3=row[1], c4=row[2]))
    metric.append(dict(index_id="2801010", content=vals))


def cib_resource_pool(db, metric):
    vals = []
    sql1 = '''select resource_pool_id,name,gmt_create,unit_count,unit_config_id,zone_list,tenant_id,replica_type,is_tenant_sys_pool from __all_resource_pool'''
    cs1 = DBUtil.getValue(db, sql1)
    rs1 = cs1.fetchall()
    vals.append(
        dict(c1='resource_pool_id', c2='name', c3='create_time', c4='unit_count', c5='unit_config_id', c6='zone_list',
             c7='tenant_id', c8='replica_type', c9='is_tenant_sys_pool', c10=None))
    for row in rs1:
        vals.append(dict(c1=row[0], c2=cs(row[1]), c3=row[2], c4=row[3], c5=cs(row[4]), c6=row[5], c7=cs(row[6]),
                         c8=cs(row[7]), c9=cs(row[8]), c10=None))
    metric.append(dict(index_id="2801011", content=vals))


def cib_unit(db, metric):
    vals = []
    sql1 = '''select unit_id,resource_pool_id,gmt_create,zone,svr_ip,svr_port,migrate_from_svr_ip,migrate_from_svr_port,manual_migrate,status from __all_unit'''
    cs1 = DBUtil.getValue(db, sql1)
    rs1 = cs1.fetchall()
    vals.append(
        dict(c1='unit_id', c2='resource_pool_id', c3='create_time', c4='zone', c5='svr_ip', c6='svr_port',
             c7='migrate_from_svr_ip', c8='migrate_from_svr_port', c9='manual_migrate', c10='status'))
    for row in rs1:
        vals.append(dict(c1=row[0], c2=cs(row[1]), c3=row[2], c4=row[3], c5=cs(row[4]), c6=row[5], c7=cs(row[6]),
                         c8=cs(row[7]), c9=cs(row[8]), c10=cs(row[9])))
    metric.append(dict(index_id="2801012", content=vals))


def cib_unit_config(db, metric):
    vals = []
    global version
    if version < '4.0':
        sql1 = '''select unit_config_id,name,max_cpu,min_cpu,max_memory,min_memory,max_iops,min_iops,max_disk_size,max_session_num from __all_unit_config'''
        cs1 = DBUtil.getValue(db, sql1)
        rs1 = cs1.fetchall()
        vals.append(
            dict(c1='unit_config_id', c2='name', c3='max_cpu', c4='min_cpu', c5='max_memory', c6='min_memory',
                 c7='max_iops', c8='min_iops', c9='max_disk_size', c10='max_session_num'))
        for row in rs1:
            vals.append(dict(c1=row[0], c2=cs(row[1]), c3=row[2], c4=row[3], c5=cs(row[4]), c6=row[5], c7=cs(row[6]),
                             c8=cs(row[7]), c9=cs(row[8]), c10=cs(row[9])))
    else:
        sql1 = '''select
	unit_config_id,
	name,
	max_cpu,
	min_cpu,
	memory_size,
		max_iops,
	min_iops,
	log_disk_size,
	iops_weight
from
	__all_unit_config'''
        cs1 = DBUtil.getValue(db, sql1)
        rs1 = cs1.fetchall()
        vals.append(
            dict(c1='unit_config_id', c2='name', c3='max_cpu', c4='min_cpu', c5='memory_size', c6='max_iops',
                 c7='min_iops', c8='log_disk_size', c9='iops_weight'))
        for row in rs1:
            vals.append(dict(c1=row[0], c2=cs(row[1]), c3=row[2], c4=row[3], c5=cs(row[4]), c6=row[5], c7=cs(row[6]),
                             c8=cs(row[7]), c9=cs(row[8])))
    metric.append(dict(index_id="2801013", content=vals))


def cib_resource_usage(db, metric):
    vals = []
    global version
    if version < '4.0':
        sql1 = '''
    select t1.name resource_pool_name, t2.`name` unit_config_name, t2.max_cpu, t2.min_cpu, round(t2.max_memory/1024/1024/1024) max_mem_gb, round(t2.min_memory/1024/1024/1024) min_mem_gb, t3.zone, concat(t3.svr_ip,':',t3.`svr_port`) observer,t4.tenant_id, t4.tenant_name
    from __all_resource_pool t1 join __all_unit_config t2 on (t1.unit_config_id=t2.unit_config_id)
        join __all_unit t3 on (t1.`resource_pool_id` = t3.`resource_pool_id`)
        left join __all_tenant t4 on (t1.tenant_id=t4.tenant_id)
    order by t1.`resource_pool_id`, t2.`unit_config_id`, t3.unit_id'''
        cs1 = DBUtil.getValue(db, sql1)
        rs1 = cs1.fetchall()
        vals.append(
            dict(c1='resource_pool_name', c2='unit_config_name', c3='max_cpu', c4='min_cpu', c5='max_mem_gb',
                 c6='min_mem_gb',
                 c7='zone', c8='observer', c9='tenant_id', c10='tenant_name'))
        for row in rs1:
            vals.append(dict(c1=row[0], c2=cs(row[1]), c3=row[2], c4=row[3], c5=cs(row[4]), c6=row[5], c7=cs(row[6]),
                             c8=cs(row[7]), c9=cs(row[8]), c10=cs(row[9])))
    else:
        sql1 = '''select t1.name resource_pool_name, t2.`name` unit_config_name, t2.max_cpu, t2.min_cpu, round(t2.memory_size/1024/1024/1024) mem_limit_gb,'', t3.zone, concat(t3.svr_ip,':',t3.`svr_port`) observer,t4.tenant_id, t4.tenant_name
from __all_resource_pool t1 join __all_unit_config t2 on (t1.unit_config_id=t2.unit_config_id)
    join __all_unit t3 on (t1.`resource_pool_id` = t3.`resource_pool_id`)
    left join __all_tenant t4 on (t1.tenant_id=t4.tenant_id)
order by t1.`resource_pool_id`, t2.`unit_config_id`, t3.unit_id'''
        cs1 = DBUtil.getValue(db, sql1)
        rs1 = cs1.fetchall()
        vals.append(
            dict(c1='resource_pool_name', c2='unit_config_name', c3='max_cpu', c4='min_cpu', c5='max_mem_gb',c6='min_mem_gb',
                 c7='zone', c8='observer', c9='tenant_id', c10='tenant_name'))
        for row in rs1:
            vals.append(dict(c1=row[0], c2=cs(row[1]), c3=row[2], c4=row[3], c5=cs(row[4]), c6=row[5], c7=cs(row[6]),
                             c8=cs(row[7]), c9=cs(row[8]), c10=cs(row[9])))
    metric.append(dict(index_id="2801014", content=vals))


def get_cluster_info(db, tenant_type, pg):
    global version
    if tenant_type == "oracle":
        sql = '''select distinct value from all_VIRTUAL_SYS_PARAMETER_STAT_AGENT where name='min_observer_version' '''
    else:
        sql = '''select distinct value from __all_virtual_tenant_parameter_stat where name='min_observer_version' '''
    cs = DBUtil.getValue(db, sql)
    version = cs.fetchone()[0]
    sql = "delete from p_normal_cib where target_id='%s' and index_id=1000005 and cib_name in ('version','toolType')" % target_id
    pg.execute(sql)
    sql = """insert into p_normal_cib(target_id,index_id,cib_name,cib_value,record_time) values('%s',1000005,'version','%s',now()),
    ('%s',1000005,'toolType','%s',now())""" % (target_id, version, target_id, tenant_type)
    pg.execute(sql)
    pg.conn.commit()

    if version < '4.0':
        if tenant_type == "oracle":
            sql = "select distinct name,value,TENANT_ID from ALL_VIRTUAL_SYS_PARAMETER_STAT_AGENT t1, ALL_VIRTUAL_DATABASE_AGENT t2 where name like 'cluster%'"
        else:
            sql = "select distinct name,value,tenant_id from gv$tenant t1,__all_virtual_tenant_parameter_stat t2 where t2.name like 'cluster%'"
    else:
        if tenant_type == "oracle":
            sql = "select distinct name,value,t2.TENANT_ID from V$OB_PARAMETERS t1, dba_ob_tenants t2 where name like 'cluster%'"
        else:
            sql = "select distinct name,value,t1.tenant_id from DBA_OB_TENANTS t1,__all_virtual_tenant_parameter_stat t2 where t2.name like 'cluster%'"
    cursor = DBUtil.getValue(db, sql)
    rs = cursor.fetchall()
    cluster_id = ''
    cluster_name = ''
    tenant_id = ''
    if rs:
        for row in rs:
            if row[0] == 'cluster_id':
                cluster_id = row[1]
            elif row[0] == 'cluster':
                cluster_name = row[1]
            tenant_id = row[2]
    return cluster_id, cluster_name, tenant_id


def cib_zone_tenant(db, cluster_target_id, tenant_id):
    vals = []
    global version
    if version < '4.0':
        sql = '''select t1.col1,t1.col2,t1.col3,t1.col4,t1.col5,t1.col6,t1.col7,t1.col8,t1.col9,t1.col10 from (select * from p_oracle_cib where target_id='{0}' and index_id='2801006' and seq_id>0) t1,
    (select unnest(string_to_array(col8,';')) as zn from p_oracle_cib where target_id='{0}' and index_id='2801009' and seq_id>0 and col1='{1}') t2 where t1.col1 = zn'''.format(
            cluster_target_id, tenant_id)
        cs1 = DBUtil.getValue(db, sql)
        rs1 = cs1.fetchall()
        vals.append(
            dict(c1='ZONE_NAME', c2='ZONE_TYPE', c3='STORAGE_TYPE', c4='STATUS', c5='REGION', c6='RECOVERY_STATUS',
                 c7='MERGE_STATUS', c8='SERVER_COUNT', c9='RESOURCE_POOL_COUNT', c10='UNIT_COUNT'))
        for zone in rs1:
            vals.append(dict(c1=cs(zone[0]), c2=cs(zone[1]), c3=cs(zone[2]),
                             c4=cs(zone[3]), c5=cs(zone[4]), c6=cs(zone[5]),
                             c7=cs(zone[6]), c8=cs(zone[7]),
                             c9=cs(zone[8]), c10=cs(zone[9])))
    else:
        sql = '''select t1.col1,t1.col2,t1.col3,t1.col4,t1.col5,t1.col6 from (select * from p_oracle_cib where target_id='{0}' and index_id='2801006' and seq_id>0) t1,
        (select unnest(string_to_array(col8,';')) as zn from p_oracle_cib where target_id='{0}' and index_id='2801009' and seq_id>0 and col1='{1}') t2 where t1.col1 = zn'''.format(
            cluster_target_id, tenant_id)
        cs1 = DBUtil.getValue(db, sql)
        rs1 = cs1.fetchall()
        vals.append(
            dict(c1='ZONE_NAME', c2='ZONE_TYPE', c3='STORAGE_TYPE', c4='STATUS', c5='REGION', c6='RECOVERY_STATUS'))
        for zone in rs1:
            vals.append(dict(c1=cs(zone[0]), c2=cs(zone[1]), c3=cs(zone[2]),
                             c4=cs(zone[3]), c5=cs(zone[4]), c6=cs(zone[5])))
    metric.append(dict(index_id="2801006", content=vals))


def cib_observer1_tenant(db, cluster_target_id, tenant_id):
    global version
    global srvs
    vals = []
    if version < '4.0':
        sql = '''select t4.col1,t4.col2,t4.col3,t4.col4,t4.col5,t4.col6,t4.col7,t4.col8,t4.col9,t4.col10 from 
    (select * from p_oracle_cib where target_id='{0}' and index_id='2801009' and seq_id>0 and col1='{1}') t1,
    (select * from p_oracle_cib where target_id='{0}' and seq_id>0 and index_id='2801011') t2,
    (select * from p_oracle_cib where target_id='{0}' and seq_id>0 and index_id='2801012') t3,
    (select * from p_oracle_cib where target_id='{0}' and seq_id>0 and index_id='2801007') t4
    where t1.col1=t2.col7 and t3.col2=t2.col1 and t3.col5=t4.col2 and t3.col6=t4.col3'''.format(cluster_target_id,
                                                                                                tenant_id)
        cs1 = DBUtil.getValue(db, sql)
        rs1 = cs1.fetchall()
        vals.append(
            dict(c1='id', c2='svr_ip', c3='svr_port', c4='sql_port', c5='status', c6='heartbeat_status',
                 c7='create_time', c8='modified_time', c9='start_service_time', c10='last_heartbeat_time'))
        for row_lst in rs1:
            srvs.append(row_lst[1])
            vals.append(
                dict(c1=row_lst[0], c2=cs(row_lst[1]), c3=row_lst[2], c4=row_lst[3], c5=cs(row_lst[4]), c6=row_lst[5],
                     c7=cs(row_lst[6]), c8=cs(row_lst[7]), c9=cs(row_lst[8]), c10=cs(row_lst[9])))
    else:
        sql = '''select t4.col1,t4.col2,t4.col3,t4.col4,t4.col5,t4.col6,t4.col7,t4.col8,t4.col9 from 
        (select * from p_oracle_cib where target_id='{0}' and index_id='2801009' and seq_id>0 and col1='{1}') t1,
        (select * from p_oracle_cib where target_id='{0}' and seq_id>0 and index_id='2801011') t2,
        (select * from p_oracle_cib where target_id='{0}' and seq_id>0 and index_id='2801012') t3,
        (select * from p_oracle_cib where target_id='{0}' and seq_id>0 and index_id='2801007') t4
        where t1.col1=t2.col7 and t3.col2=t2.col1 and t3.col5=t4.col2 and t3.col6=t4.col3'''.format(cluster_target_id,
                                                                                                    tenant_id)
        cs1 = DBUtil.getValue(db, sql)
        rs1 = cs1.fetchall()
        vals.append(
            dict(c1='id', c2='svr_ip', c3='svr_port', c4='sql_port', c5='status', c6='CREATE_TIME',
                 c7='MODIFY_TIME', c8='START_SERVICE_TIME', c9='WITH_ROOTSERVER'))
        for row_lst in rs1:
            srvs.append(row_lst[1])
            vals.append(
                dict(c1=row_lst[0], c2=cs(row_lst[1]), c3=row_lst[2], c4=row_lst[3], c5=cs(row_lst[4]), c6=row_lst[5],
                     c7=cs(row_lst[6]), c8=cs(row_lst[7]), c9=cs(row_lst[8])))
    metric.append(dict(index_id="2801007", content=vals))


def cib_observer2_tenant(db, cluster_target_id, tenant_id):
    global version
    vals = []
    if version < '4.0':
        sql = '''select t4.col1,t4.col2,t4.col3,t4.col4,t4.col5,t4.col6,t4.col7,t4.col8,t4.col9,t4.col10 from 
    (select * from p_oracle_cib where target_id='{0}' and index_id='2801009' and seq_id>0 and col1='{1}') t1,
    (select * from p_oracle_cib where target_id='{0}' and seq_id>0 and index_id='2801011') t2,
    (select * from p_oracle_cib where target_id='{0}' and seq_id>0 and index_id='2801012') t3,
    (select * from p_oracle_cib where target_id='{0}' and seq_id>0 and index_id='2801008') t4
    where t1.col1=t2.col7 and t3.col2=t2.col1 and t3.col5=t4.col2 and t3.col6=t4.col3'''.format(cluster_target_id,
                                                                                                tenant_id)
        cs1 = DBUtil.getValue(db, sql)
        rs1 = cs1.fetchall()
        vals.append(
            dict(c1='id', c2='svr_ip', c3='svr_port', c4='cpu_total', c5='cpu_assigned', c6='mem_total_GB',
                 c7='mem_assigned_GB', c8='disk_total_GB', c9='disk_in_use_GB', c10='unit_num'))
        for row_lst in rs1:
            vals.append(
                dict(c1=row_lst[0], c2=cs(row_lst[1]), c3=row_lst[2], c4=row_lst[3], c5=cs(row_lst[4]), c6=row_lst[5],
                     c7=cs(row_lst[6]), c8=cs(row_lst[7]), c9=cs(row_lst[8]), c10=cs(row_lst[9])))
    else:
        sql = '''select t5.col1,t5.col2,t5.col3,t5.col4,t5.col5,t5.col6,t5.col7,t5.col8,t5.col9,t5.col10 from 
        (select * from p_oracle_cib where target_id='{0}' and index_id='2801009' and seq_id>0 and col1='{1}') t1,
        (select * from p_oracle_cib where target_id='{0}' and seq_id>0 and index_id='2801011') t2,
        (select * from p_oracle_cib where target_id='{0}' and seq_id>0 and index_id='2801012') t3,
        (select * from p_oracle_cib where target_id='{0}' and seq_id>0 and index_id='2801007') t4,
				(select * from p_oracle_cib where target_id='{0}' and seq_id>0 and index_id='2801008') t5
        where t1.col1=t2.col7 and t3.col2=t2.col1 and t3.col5=t4.col2 and t3.col6=t4.col3 and t4.col1=t5.col1
'''.format(cluster_target_id, tenant_id)
        cs1 = DBUtil.getValue(db, sql)
        rs1 = cs1.fetchall()
        vals.append(
            dict(c1='id', c2='svr_ip', c3='cpu_total', c4='cpu_assigned', c5='mem_total_GB',
                 c6='mem_assigned_GB', c7='data_disk_total_GB', c8='data_disk_in_use_GB', c9='log_disk_total_GB',
                 c10='log_disk_in_use_GB'))
        for row_lst in rs1:
            vals.append(
                dict(c1=row_lst[0], c2=cs(row_lst[1]), c3=row_lst[2], c4=row_lst[3], c5=cs(row_lst[4]), c6=row_lst[5],
                     c7=cs(row_lst[6]), c8=cs(row_lst[7]), c9=cs(row_lst[8]), c10=cs(row_lst[9])))
    metric.append(dict(index_id="2801008", content=vals))


def cib_tenant_info(db, cluster_target_id, tenant_id):
    vals = []
    global version
    if version < '4.0':
        sql = '''select t4.col1,t4.col2,t4.col3,t4.col4,t4.col5,t4.col6,t4.col7,t4.col8,t4.col9,t4.col10 from 
        p_oracle_cib t4 where target_id='{0}' and index_id='2801009' and seq_id>0 and col1='{1}' '''.format(
            cluster_target_id,
            tenant_id)
        cs1 = DBUtil.getValue(db, sql)
        rs1 = cs1.fetchall()
        vals.append(
            dict(c1='tenant_id', c2='tenant_name', c3='create_time', c4='info', c5='status', c6='locked',
                 c7='read_only', c8='zone_list', c9='primary_zone', c10='locality'))
        for row in rs1:
            vals.append(dict(c1=row[0], c2=cs(row[1]), c3=row[2], c4=row[3], c5=cs(row[4]), c6=row[5], c7=cs(row[6]),
                             c8=cs(row[7]), c9=cs(row[8]), c10=cs(row[9])))
    else:
        sql = '''select t4.col1,t4.col2,t4.col3,t4.col4,t4.col5,t4.col6,t4.col7,t4.col8,t4.col9,t4.col10 from 
        p_oracle_cib t4 where target_id='{0}' and index_id='2801009' and seq_id>0 and col1='{1}' '''.format(
            cluster_target_id,
            tenant_id)
        cs1 = DBUtil.getValue(db, sql)
        rs1 = cs1.fetchall()
        vals.append(
            dict(c1='tenant_id', c2='tenant_name', c3='create_time', c4='info', c5='status', c6='locked',
                 c7='read_only', c8='zone_list', c9='primary_zone', c10='locality'))
        for row in rs1:
            vals.append(dict(c1=row[0], c2=cs(row[1]), c3=row[2], c4=row[3], c5=cs(row[4]), c6=row[5], c7=cs(row[6]),
                             c8=cs(row[7]), c9=cs(row[8]), c10=cs(row[9])))
    metric.append(dict(index_id="2801009", content=vals))


def cib_resource_pool_tenant(db, cluster_target_id, tenant_id):
    vals = []
    sql = '''select t4.col1,t4.col2,t4.col3,t4.col4,t4.col5,t4.col6,t4.col7,t4.col8,t4.col9 from 
(select * from p_oracle_cib where target_id='{0}' and index_id='2801009' and seq_id>0 and col1='{1}') t1,
(select * from p_oracle_cib where target_id='{0}' and seq_id>0 and index_id='2801011') t4
where t1.col1=t4.col7'''.format(cluster_target_id, tenant_id)
    cs1 = DBUtil.getValue(db, sql)
    rs1 = cs1.fetchall()
    vals.append(
        dict(c1='resource_pool_id', c2='name', c3='create_time', c4='unit_count', c5='unit_config_id', c6='zone_list',
             c7='tenant_id', c8='replica_type', c9='is_tenant_sys_pool', c10=None))
    for row in rs1:
        vals.append(dict(c1=row[0], c2=cs(row[1]), c3=row[2], c4=row[3], c5=cs(row[4]), c6=row[5], c7=cs(row[6]),
                         c8=cs(row[7]), c9=cs(row[8]), c10=None))
    metric.append(dict(index_id="2801011", content=vals))


def cib_unit_tenant(db, cluster_target_id, tenant_id):
    vals = []
    sql = '''select t4.col1,t4.col2,t4.col3,t4.col4,t4.col5,t4.col6,t4.col7,t4.col8,t4.col9,t4.col10 from 
(select * from p_oracle_cib where target_id='{0}' and index_id='2801009' and seq_id>0 and col1='{1}') t1,
(select * from p_oracle_cib where target_id='{0}' and seq_id>0 and index_id='2801011') t2,
(select * from p_oracle_cib where target_id='{0}' and seq_id>0 and index_id='2801012') t4
where t1.col1=t2.col7 and t4.col2=t2.col1'''.format(cluster_target_id, tenant_id)
    cs1 = DBUtil.getValue(db, sql)
    rs1 = cs1.fetchall()
    vals.append(
        dict(c1='unit_id', c2='resource_pool_id', c3='create_time', c4='zone', c5='svr_ip', c6='svr_port',
             c7='migrate_from_svr_ip', c8='migrate_from_svr_port', c9='manual_migrate', c10='status'))
    for row in rs1:
        vals.append(dict(c1=row[0], c2=cs(row[1]), c3=row[2], c4=row[3], c5=cs(row[4]), c6=row[5], c7=cs(row[6]),
                         c8=cs(row[7]), c9=cs(row[8]), c10=cs(row[9])))
    metric.append(dict(index_id="2801012", content=vals))


def cib_unit_config_tenant(db, cluster_target_id, tenant_id):
    vals = []
    global version
    if version < '4.0':
        sql = '''select t4.col1,t4.col2,t4.col3,t4.col4,t4.col5,t4.col6,t4.col7,t4.col8,t4.col9,t4.col10 from 
    (select * from p_oracle_cib where target_id='{0}' and index_id='2801009' and seq_id>0 and col1='{1}') t1,
    (select * from p_oracle_cib where target_id='{0}' and seq_id>0 and index_id='2801011') t2,
    (select * from p_oracle_cib where target_id='{0}' and seq_id>0 and index_id='2801013') t4
    where t1.col1=t2.col7 and t4.col1=t2.col5'''.format(cluster_target_id, tenant_id)
        cs1 = DBUtil.getValue(db, sql)
        rs1 = cs1.fetchall()
        vals.append(
            dict(c1='unit_config_id', c2='name', c3='max_cpu', c4='min_cpu', c5='max_memory', c6='min_memory',
                 c7='max_iops', c8='min_iops', c9='max_disk_size', c10='max_session_num'))
        for row in rs1:
            vals.append(dict(c1=row[0], c2=cs(row[1]), c3=row[2], c4=row[3], c5=cs(row[4]), c6=row[5], c7=cs(row[6]),
                             c8=cs(row[7]), c9=cs(row[8]), c10=cs(row[9])))
    else:
        sql = '''select t4.col1,t4.col2,t4.col3,t4.col4,t4.col5,t4.col6,t4.col7,t4.col8,t4.col9 from 
        (select * from p_oracle_cib where target_id='{0}' and index_id='2801009' and seq_id>0 and col1='{1}') t1,
        (select * from p_oracle_cib where target_id='{0}' and seq_id>0 and index_id='2801011') t2,
        (select * from p_oracle_cib where target_id='{0}' and seq_id>0 and index_id='2801013') t4
        where t1.col1=t2.col7 and t4.col1=t2.col5'''.format(cluster_target_id, tenant_id)
        cs1 = DBUtil.getValue(db, sql)
        rs1 = cs1.fetchall()
        vals.append(
            dict(c1='unit_config_id', c2='name', c3='max_cpu', c4='min_cpu', c5='memory_size', c6='max_iops',
                 c7='min_iops', c8='log_disk_size', c9='iops_weight'))
        for row in rs1:
            vals.append(dict(c1=row[0], c2=cs(row[1]), c3=row[2], c4=row[3], c5=cs(row[4]), c6=row[5], c7=cs(row[6]),
                             c8=cs(row[7]), c9=cs(row[8])))
    metric.append(dict(index_id="2801013", content=vals))


def cib_resource_usage_tenant(db, cluster_target_id, tenant_id):
    vals = []
    global version
    if version < '4.0':
        sql = '''select t4.col1,t4.col2,t4.col3,t4.col4,t4.col5,t4.col7,t4.col8,t4.col9,t4.col10,t1.col9 from 
    (select * from p_oracle_cib where target_id='{0}' and index_id='2801009' and seq_id>0 and col1='{1}') t1,
    (select * from p_oracle_cib where target_id='{0}' and seq_id>0 and index_id='2801014') t4
    where t1.col1=t4.col9'''.format(cluster_target_id, tenant_id)
        cs1 = DBUtil.getValue(db, sql)
        rs1 = cs1.fetchall()
        if rs1:
            vals.append(
                dict(c1='resource_pool_name', c2='unit_config_name', c3='max_cpu', c4='min_cpu', c5='max_mem_gb',
                    c6='zone',
                    c7='observer', c8='tenant_id', c9='tenant_name', c10='primary_zone'))
            cpu_total = 0
            primary_zone = set()
            for row in rs1:
                primary_zone.update(row[9].split(','))
                vals.append(dict(c1=row[0], c2=cs(row[1]), c3=row[2], c4=row[3], c5=cs(row[4]), c6=row[5], c7=cs(row[6]),
                                c8=cs(row[7]), c9=cs(row[8]), c10=cs(row[9])))
            primary_zone_lst = list(primary_zone)
            if primary_zone_lst[0] == 'RANDOM':
                for row in rs1:
                    cpu_total += float(row[2])
            else:
                for row in rs1:
                    if row[5] in primary_zone_lst:
                        cpu_total = float(row[2])
    else:
        sql = '''select t4.col1,t4.col2,t4.col3,t4.col4,t4.col5,t4.col7,t4.col8,t4.col9,t4.col10, t1.col9 from 
        (select * from p_oracle_cib where target_id='{0}' and index_id='2801009' and seq_id>0 and col1='{1}') t1,
        (select * from p_oracle_cib where target_id='{0}' and seq_id>0 and index_id='2801014') t4
        where t1.col1=t4.col9'''.format(cluster_target_id, tenant_id)
        cs1 = DBUtil.getValue(db, sql)
        rs1 = cs1.fetchall()
        if rs1:
            vals.append(
                dict(c1='resource_pool_name', c2='unit_config_name', c3='max_cpu', c4='min_cpu', c5='max_mem_gb',
                    c6='zone', c7='observer', c8='tenant_id', c9='tenant_name', c10='primary_zone'))
            cpu_total = 0
            primary_zone = set()
            for row in rs1:
                primary_zone.update(row[9].split(','))
                vals.append(dict(c1=row[0], c2=cs(row[1]), c3=row[2], c4=row[3], c5=cs(row[4]), c6=row[5], c7=cs(row[6]),
                                c8=cs(row[7]), c9=cs(row[8]), c10=cs(row[9])))
            primary_zone_lst = list(primary_zone)
            if primary_zone_lst[0] == 'RANDOM':
                for row in rs1:
                    cpu_total += float(row[2])
            else:
                for row in rs1:
                    if row[5] in primary_zone_lst:
                        cpu_total = float(row[2])
    if vals:
        metric.append(dict(index_id="2801014", content=vals))
        metric.append(dict(index_id="2801015", value=[{'name': 'cpu_total', 'value': cpu_total},
                                                    {'name': 'cpu_assigned', 'value': cpu_total}]))


def tuple2(arr, f=False):
    s = ''
    for v in arr:
        if s:
            if f:
                s += ",'%s'" % str(v)
            else:
                s += ",%s" % str(v)
        else:
            if f:
                s = "'%s'" % str(v)
            else:
                s = "%s" % str(v)
    if s and f:
        s = '(%s)' % s
    return s


def getsshinfo(db, in_ip, rs):
    in_ostype = ssh = None
    if rs:
        in_usr = rs[1]
        in_passwd = rs[2]
        in_port = rs[3]
        protocol = rs[4]
        life = rs[5]
        in_ostype = rs[6]
        if protocol == '1':
            proto = "SSH"
        elif protocol == '2':
            proto = "RSH"
        else:
            proto = "SSH"
        ssh_user, ssh_path = DBUtil.get_sshkey_info(db)
        ssh = sshSession.sshSession(in_ip, in_usr, in_passwd, in_port, proto, life, ssh_user, ssh_path)
    return in_ostype, ssh


def findPath(ddir, path):
    t = path.find('->')
    if t >= 0:
        p = path[0:t].strip()
        d = path[t+2:].strip()
        if d[0] != '/':
            d = ddir + '/' + d
    else:
        p = path.strip()
        d = ddir + '/' + p
    return p,d


def getDirs(db, in_ip, row, ddir):
    ostype,ssh = getsshinfo(db, in_ip.split(':')[0], row)
    ds = {}
    if ssh:
        cmd = os_svc.ls_cmd(ostype, ddir, 0)
        kvs = {}
        ret = os_svc.proc(ostype, ssh, cmd, kvs, None, 'd')
        val = kvs.get('ls')
        if val:
            for d in val:
                if d[0].find('clog') == 0:
                    s,p = findPath(ddir, d[0])
                    if s == 'clog':
                        ds['clog'] = p
                elif d[0].find('slog') == 0:
                    s,p = findPath(ddir, d[0])
                    if s == 'slog':
                        ds['slog'] = p
                elif d[0].find('sstable') == 0:
                    s,p = findPath(ddir, d[0])
                    if s == 'sstable':
                        ds['sstable'] = p
    return ds


def ob_os(db, uid, srvs, ddir=None):
    if srvs:
        sql = "select cib_name,cib_value from p_normal_cib where target_id='%s' and index_id=1000001 and cib_name in ('_ips','_ddir','_clog','_slog','_sstable')" % uid
        cs1 = DBUtil.getValue(db, sql)
        rs1 = cs1.fetchall()
        ips = set()
        dirs = {}
        dd = None
        if rs1:
            for row in rs1:
                if row[0] == '_ips':
                    if not ips and row[1]:
                        t = row[1].find(':')
                        if t > 0:
                            arr = row[1][0:t].split(',')
                            dd = row[1][t+1:]
                        else:
                            arr = row[1].split(',')
                        for ip in arr:
                            ips.add(ip)
                elif row[0] == '_ddir':
                    dd = row[1]
                else:
                    dirs[row[0]] = row[1]
        vs = set()
        for row in srvs:
            vs.add(row)
        f = False
        if ddir:
            if not dirs.get('_clog'):
                f = True
            if not dirs.get('_slog'):
                f = True
            if not dirs.get('_sstable'):
                f = True
        if vs != ips or dd != ddir or f:
            sql = """select b.in_ip,b.uid,b.in_username,b.in_password,b.port,b.position,b.life,d.name from mgt_device b,sys_dict d
where d.type='device_opersys' and b.opersys=d.value::numeric and in_ip in %s and b.use_flag""" % tuple2(vs.union(ips), True)
            cs2 = DBUtil.getValue(db, sql)
            rs2 = cs2.fetchall()
            if rs2:
                hosts = {}
                for row in rs2:
                    hosts[row[0]] = [row[1],row[2],row[3],row[4],row[5],row[6],row[7]]
                try:
                    cur = db.conn.cursor()
                    if vs.union(ips):
                        for ip in vs.union(ips):
                            row = hosts.get(ip)
                            if row:
                                sql = "delete from p_normal_cib where target_id='%s' and index_id=1000001 and cib_name='_ping'" % row[0]
                                cur.execute(sql)
                    f = True
                    ss = ''
                    for ip in vs:
                        row = hosts.get(ip)
                        if row:
                            vs2 = vs.copy()
                            if len(vs2) > 1:
                                vs2.remove(ip)
                            if f:
                                s = '+' + tuple2(vs2)
                                f = False
                                ss = ip
                            else:
                                s = tuple2(vs2)
                                ss += ',' + ip
                            if vs2:
                                sql = "delete from p_normal_cib where target_id='%s' and index_id=1000001 and cib_name='_ping'" % row[0]
                                cur.execute(sql)
                                sql = "insert into p_normal_cib(target_id,index_id,cib_name,cib_value,record_time) values('%s',1000001,'_ping','%s',now())" % (row[0], s)
                                cur.execute(sql)
                    sql = "delete from p_normal_cib where target_id='%s' and index_id=1000001 and cib_name in ('_ips','_ddir','_clog','_slog','_sstable')" % uid
                    cur.execute(sql)
                    if ddir is not None:
                        d1 = ''
                        d2 = ''
                        d3 = ''
                        dirs = ddir.split(',')
                        for it in dirs:
                            arr = it.split('=')
                            if len(arr) != 2:
                                continue
                            row = hosts.get(arr[0].split(':')[0])
                            if row:
                                ds = getDirs(db, arr[0], row, arr[1])
                                if ds:
                                    if ds.get('clog'):
                                        if d1:
                                            d1 += ',' + arr[0] + '=' + ds['clog']
                                        else:
                                            d1 = arr[0] + '=' + ds['clog']
                                    if ds.get('slog'):
                                        if d2:
                                            d2 += ',' + arr[0] + '=' + ds['slog']
                                        else:
                                            d2 = arr[0] + '=' + ds['slog']
                                    if ds.get('sstable'):
                                        if d3:
                                            d3 += ',' + arr[0] + '=' + ds['sstable']
                                        else:
                                            d3 = arr[0] + '=' + ds['sstable']
                        sql = """insert into p_normal_cib(target_id,index_id,cib_name,cib_value,record_time) values('%s',1000001,'_ips','%s',now()),('%s',1000001,'_ddir','%s',now()),
('%s',1000001,'_clog','%s',now()),('%s',1000001,'_slog','%s',now()),('%s',1000001,'_sstable','%s',now())""" % (uid, ss, uid, ddir, uid, d1, uid, d2, uid, d3)
                        cur.execute(sql)
                    else:
                        sql = "insert into p_normal_cib(target_id,index_id,cib_name,cib_value,record_time) values('%s',1000001,'_ips','%s',now())" % (uid, ss)
                        cur.execute(sql)
                    db.conn.commit()
                except Exception as e:
                    db.conn.rollback()


def cib_clockSource(pg, target_id, metric):
    servers = DBUtil.get_obsrv_ips(pg, target_id)
    vals = []
    for server in servers:
        server_ip = server[0]
        ostype, ssh, device_id = DBUtil.getsshinfo(pg, server_ip)
        cmd = '''cat /sys/devices/system/clocksource/clocksource0/current_clocksource'''
        rs = ssh.exec_cmd(cmd)
        if rs:
            vals.append(dict(name=server_ip, value=rs))
        else:
            vals.append(dict(name=server_ip, value=""))
    metric.append(dict(index_id="2801016", value=vals))


if __name__ == '__main__':
    ob, subtype, tenant_name, tenant_type, cluster_name = DBUtil.get_ob_env()
    target_id, pg = DBUtil.get_pg_env()
    try:
        metric = []
        if subtype == 'cluster':
            # 更新OCP连接密码
            DBUtil.get_ocp_connect_info(pg, target_id, subtype, cluster_name)
            ob_version(ob)
            ddir = cib_parameter(ob, metric)
            cib_variables(ob, metric)
            cib_zone(ob, metric)
            cib_observer1(ob, metric)
            cib_observer2(ob, metric)
            cib_tenant(ob, metric)
            cib_schema(ob, metric)
            cib_resource_pool(ob, metric)
            cib_unit(ob, metric)
            cib_unit_config(ob, metric)
            cib_resource_usage(ob, metric)
            cib_clockSource(pg, target_id, metric)
            cluster_id = cib_basic(ob, metric, target_id, pg,tenant_type, tenant_name)
            print('{"cib":' + json.dumps(metric) + '}')
            sql = "update mgt_system set subuid='{0}' where uid='{1}' and use_flag=true".format(cluster_id, target_id)
            pg.execute(sql)
            pg.conn.commit()
            ob_os(pg, target_id, srvs, ddir)
        else:
            cluster_id, cluster_name, tenant_id = get_cluster_info(ob, tenant_type, pg)
            if cluster_id:
                cluster_target_id = DBUtil.get_cluster_target_id(pg, target_id)
                cib_tenant_basic(pg, cluster_target_id, tenant_name, tenant_type)
                cib_tenant_parameter(ob, metric, tenant_type)
                cib_tenant_variables(ob, metric, tenant_type)
                cib_zone_tenant(pg, cluster_target_id, tenant_id)
                cib_observer1_tenant(pg, cluster_target_id, tenant_id)
                cib_observer2_tenant(pg, cluster_target_id, tenant_id)
                cib_tenant_info(pg, cluster_target_id, tenant_id)
                cib_resource_pool_tenant(pg, cluster_target_id, tenant_id)
                cib_unit_tenant(pg, cluster_target_id, tenant_id)
                cib_unit_config_tenant(pg, cluster_target_id, tenant_id)
                cib_resource_usage_tenant(pg, cluster_target_id, tenant_id)
            print('{"cib":' + json.dumps(metric) + '}')
            sql = "update mgt_system set subuid='{0}' where uid='{1}' and use_flag=true".format(cluster_id, target_id)
            pg.execute(sql)
            pg.conn.commit()
            #if cluster_id:
            #    ob_os(pg, target_id, srvs, ddir)
    except Exception as e:
        errorInfo = str(e)
        raise Exception(errorInfo)

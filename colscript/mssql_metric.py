# encoding: utf-8

# Author	: xxxx

import json
import sys
sys.path.append('/usr/software/knowl')
import DBUtil
import CommUtil
from datetime import datetime


def db_version(mssql):
    """
    获取数据库的版本号
    :param mssql:
    :return:
    """
    sql_version = "SELECT SUBSTRING(convert(varchar(50),SERVERPROPERTY('ProductVersion')),1,14) AS Edition"
    out_version, _ = mssql.execute(sql_version)
    db_vinfo = [i for i in out_version.msg]
    main_version = db_vinfo[0][0].split('.')[0]
    db_vinfo = db_vinfo[0][0]
    return main_version,db_vinfo


def db_platform(mssql):
    """
    查看数据库运行平台
    :param mssql:
    :return:
    """
    sql = "SELECT @@VERSION AS 'SQL Server Version';"
    result, _ = mssql.execute(sql)
    if result.code == 0:
        for row in result.msg:
            os_v = row[0]
            if str(os_v).lower().find('linux') == -1:
                return 'windows'
            else:
                return 'linux'


def get_dbname(mssql):
    """
    获取SqlServer实例中所有数据库名
    :return:
    """
    sql = "SELECT name,state_desc FROM [master].[sys].[databases] where name != 'model'"
    result, _ = mssql.execute(sql)
    temp = []
    if result.code == 0:
        for row in result.msg:
            db_name = row[0]
            temp.append([db_name,row[1]])
    return temp


def cs(val, dt=False):
    if val is None:
        return ''
    else:
        if dt:
            return val.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return str(val)


def one_result(mssql, sql, index_id, metric):
    """
    获取值对类型的指标且只有一行
    :param mssql:
    :param metric:
    :return:
    """
    result, _ = mssql.execute(sql)
    if result.code == 0:
        for row in result.msg:
            metric.append(dict(index_id=cs(index_id), value=cs(row[0])))


METRIC_BASIC = {
    'FREE SPACE IN TEMPDB (KB)':2150003,                      # 通用
    'BUFFER MANAGER:PAGE LIFE EXPECTANCY': 2151003,           # 通用
    'TRANSACTIONS/SEC': 2151014,                              # 通用
    'SQL RE-COMPILATIONS/SEC': 2151017,                       # 通用
    'SQL COMPILATIONS/SEC':2151016,                           # 通用
    'LOGINS/SEC': 2151018,                                    # 通用
    'LOGOUTS/SEC': 2151019,                                   # 通用
    'USER CONNECTIONS': 2151068,                              # 通用
    'SQL SENDS/SEC': 2151026,                                 # 通用
    'SQL SEND TOTAL': 2151027,                                # 通用
    'SQL RECEIVES/SEC': 2151028,                              # 通用
    'SQL RECEIVE TOTAL': 2151029,                             # 通用
    'LOG FLUSHES/SEC': 2151039,                               # 通用
    'LOG FLUSH WAITS/SEC': 2151040,                           # 通用
    'LOG BYTES FLUSHED/SEC': 2151041,                         # 通用
    'LOG FLUSH WAIT TIME': 2151145,                           # 通用
    'PAGE READS/SEC': 2151048,                                # 通用
    'PAGE WRITES/SEC': 2151049,                               # 通用
    'PAGE SPLITS/SEC': 2151129,                               # 通用
    'ACTIVE TEMP TABLES': 2152002,                            # 通用
    'TEMP TABLES CREATION RATE': 2152003,                     # 通用
    'PROCESSES BLOCKED': 2152030,                             # 通用
    'TEMP TABLES FOR DESTRUCTION': 2152005,                   # 通用
    'LOCK REQUESTS/SEC': 2152032,                             # 通用
    'LOCK TIMEOUTS/SEC': 2152033,                             # 通用
    'LOCK WAITS/SEC': 2152008,                                # 通用
    'NUMBER OF DEADLOCKS/SEC': 2151057,                       # 通用
    'LOCK WAIT TIME (MS)': 2152037,                           # 通用
    'FULL SCANS/SEC': 2152014,                                # 通用
    'LATCH WAITS/SEC': 2152015,                               # 通用
    'AVERAGE LATCH WAIT TIME (MS)': 2152041,                  # 通用
    'ERRORS/SEC': 2152021,                                    # 通用
    'BUFFER CACHE HIT RATIO': 2153001,                        # 通用
    'CATALOG METADATA:CACHE HIT RATIO': 2153007,              # 通用
    'CURSOR MANAGER BY TYPE:CACHE HIT RATIO': 2153002,        # 通用
    'PLAN CACHE:CACHE HIT RATIO': 2153006,                    # 通用
    'LOG CACHE HIT RATIO': 2153003,                           # 通用
    'BATCH REQUESTS/SEC': 2151131,                            # 通用
    'CONNECTION MEMORY (KB)':2151155,                         # 通用
    'GRANTED WORKSPACE MEMORY (KB)':2151156,                  # 通用
    'MAXIMUM WORKSPACE MEMORY (KB)':2151157,                  # 通用
    'MEMORY GRANTS OUTSTANDING':2151158,                      # 通用
    'OPTIMIZER MEMORY (KB)':2151159,                          # 通用
    'SQL CACHE MEMORY (KB)':2151160,                          # 通用
    'TARGET SERVER MEMORY (KB)':2151161,                      # 通用
    'TOTAL SERVER MEMORY (KB)':2151162,                       # 通用
    'INDEX SEARCHES/SEC':2150044,                             # 通用
    'PAGE DEALLOCATIONS/SEC':2150046,                         # 通用
    'PAGES ALLOCATED/SEC':2150048,                            # 通用
    'RANGE SCANS/SEC':2150050,                                # 通用
    'TABLE LOCK ESCALATIONS/SEC':2150052,                     # 通用
    'SKIPPED GHOSTED RECORDS/SEC':2150054,                    # 通用
    'MIXED PAGE ALLOCATIONS/SEC':2150056,                     # 通用
    'BUFFER MANAGER:READAHEAD PAGES/SEC':2150058,             # 通用
    'BUFFER MANAGER:STOLEN PAGES':2150063,                    # 通用
    'BUFFER MANAGER:TARGET PAGES':2150061,                    # 通用
    'BUFFER MANAGER:TOTAL PAGES':2150062,                     # 通用
    'BUFFER MANAGER:RESERVED PAGES':2150060,                  # 通用
    'CONNECTION RESET/SEC': 2151021,                         # 2005以上版本
    'WRITE TRANSACTIONS/SEC': 2151015,                        # 2005以上版本
    'SUBOPTIMAL PLANS/SEC': 2152020,                          # 2005以上版本
    'LOG BYTES RECEIVED/SEC': 2151102,                        # 2008 R2以上版本
    'LOG REMAINING FOR UNDO': 2151103,                        # 2008 R2以上版本
    'LOG SEND QUEUE': 2151104,                                # 2008 R2以上版本
    'MIRRORED WRITE TRANSACTIONS/SEC': 2151105,               # 2008 R2以上版本
    'RECOVERY QUEUE': 2151106,                                # 2008 R2以上版本
    'REDO BYTES REMAINING': 2151107,                          # 2008 R2以上版本
    'REDONE BYTES/SEC': 2151108,                              # 2008 R2以上版本
    'TOTAL LOG REQUIRING UNDO': 2151109,                      # 2008 R2以上版本
    'LOG POOL DISK READS/SEC': 2151043,                       # 2008 R2以上版本
    'LOG POOL CACHE MISSES/SEC': 2152012,                     # 2008 R2以上版本
    'REDO BLOCKED/SEC': 2152017,                              # 2008 R2以上版本
    'BYTES RECEIVED FROM REPLICA/SEC': 2151173,               # 2008 R2以上版本
    'BYTES SENT TO REPLICA/SEC': 2152019,                     # 2008 R2以上版本
    'FILE BYTES RECEIVED/SEC': 2151099,                       # 2008 R2以上版本
    'DATABASE NODE MEMORY (KB)':2151149,                      # 2008 R2以上版本
    'FREE NODE MEMORY (KB)':2151150,                          # 2008 R2以上版本
    'FOREIGN NODE MEMORY (KB)':2151151,                       # 2008 R2以上版本
    'STOLEN NODE MEMORY (KB)':2151152,                        # 2008 R2以上版本
    'TARGET NODE MEMORY (KB)':2151153,                        # 2008 R2以上版本
    'TOTAL NODE MEMORY (KB)':2151154,                         # 2008 R2以上版本
    'LOG POOL MEMORY (KB)':2151163,                           # 2008 R2以上版本
    'DATABASE CACHE MEMORY (KB)':2151164,                     # 2008 R2以上版本
    'EXTERNAL BENEFIT OF MEMORY':2151165,                     # 2008 R2以上版本
    'FREE MEMORY (KB)':2151166,                               # 2008 R2以上版本
    'RESERVED SERVER MEMORY (KB)':2151167,                    # 2008 R2以上版本
    'STOLEN SERVER MEMORY (KB)':2151168,                      # 2008 R2以上版本
    'ROWS PROCESSED/SEC': 2151023,                            # 2012以上版本
    'ROWS RETURNED/SEC': 2151024,                             # 2012以上版本
    'ROWS TOUCHED/SEC': 2151025,                              # 2012以上版本
    'TRANSACTIONS ABORTED BY USER/SEC': 2151030,              # 2012以上版本
    'TRANSACTIONS ABORTED/SEC': 2151031,                      # 2012以上版本
    'TRANSACTIONS CREATED/SEC': 2151032,                      # 2012以上版本
    'CURSOR INSERTS/SEC': 2151170,                            # 2012以上版本
    'CURSOR UPDATES/SEC': 2151171,                            # 2012以上版本
    'CURSOR DELETES/SEC': 2151172,                            # 2012以上版本
    'LOG APPLY PENDING QUEUE': 2151100,                       # 2014以上版本
    'LOG APPLY READY QUEUE': 2151101,                         # 2014以上版本
    'SEGMENT CACHE HIT RATIO': 2153004,                       # 2016以上版本
    'UPDATE CONFLICT RATIO': 2153005,                         # 2016以上版本
    'FREE LIST STALLS/SEC': 2151169,                          # 2016以上版本
    'LAZY WRITES/SEC': 2151052,                               # 2016以上版本
    'CHECKPOINT PAGES/SEC': 2151053,                          # 2016以上版本
    'RANGE SCANS/SEC': 2152048,                               # 2016以上版本
    'MEMORY GRANTS PENDING': 2151054,                         # 2016以上版本
    'BYTES SENT TO TRANSPORT/SEC': 2151124,                   # 2016以上版本
    'FLOW CONTROL TIME (MS/SEC)': 2151125,                    # 2016以上版本
    'FLOW CONTROL/SEC': 2151126,                              # 2016以上版本
    'RECEIVES FROM REPLICA/SEC': 2151095,                     # 2016以上版本
    'RESENT MESSAGES/SEC': 2151096,                           # 2016以上版本
    'SENDS TO REPLICA/SEC': 2151097,                          # 2016以上版本
    'SENDS TO TRANSPORT/SEC': 2151098                         # 2016以上版本
}


def os_performance_counters(mssql, metric):
    """
    查看数据库计数器值
    :return:
    """
    from numpy import mean
    for para_name in METRIC_BASIC.keys():
        vars = []
        idx = METRIC_BASIC.get(para_name)
        if para_name in ('BUFFER CACHE HIT RATIO','PLAN CACHE:CACHE HIT RATIO','CURSOR MANAGER BY TYPE:CACHE HIT RATIO', 'CATALOG METADATA:CACHE HIT RATIO', 'LOG CACHE HIT RATIO', 'SEGMENT CACHE HIT RATIO','UPDATE CONFLICT RATIO'):
            if para_name.find(':') == -1:
                sql_ratio = f"""
                    SELECT RTRIM(a.instance_name) ,RTRIM(a.object_name),CASE
                                WHEN CASE 
                                        WHEN b.cntr_value < 100
                                        THEN 100
                                        ELSE CONVERT(DECIMAL(18, 2), ((a.cntr_value * 1.0 / b.cntr_value) * 100.0))
                                    END IS NULL
                                THEN '100'
                                ELSE CASE 
                                        WHEN b.cntr_value < 100
                                        THEN 100
                                        ELSE CONVERT(DECIMAL(18, 2), ((a.cntr_value * 1.0 / b.cntr_value) * 100.0))
                                    END
                            END AS '命中率%'
                    FROM
                    (
                        SELECT object_name,instance_name,cntr_value
                        FROM sys.dm_os_performance_counters
                        WHERE upper(counter_name) = '{para_name}'
                    ) a
                    CROSS JOIN
                    (
                        SELECT object_name,instance_name,cntr_value
                        FROM sys.dm_os_performance_counters
                        WHERE upper(counter_name) in ('{para_name} BASE','{' '.join(para_name.split(' ')[:-1])}')
                    ) b
                    where a.instance_name = b.instance_name
                    and a.object_name = b.object_name
                    """
            else:
                obj_name = para_name.split(':')[0]
                p_name = para_name.split(':')[1]
                sql_ratio = f"""
                    SELECT RTRIM(a.instance_name) ,RTRIM(a.object_name),CASE
                                WHEN CASE 
                                        WHEN b.cntr_value < 100
                                        THEN 100
                                        ELSE CONVERT(DECIMAL(18, 2), ((a.cntr_value * 1.0 / b.cntr_value) * 100.0))
                                    END IS NULL
                                THEN '100'
                                ELSE CASE 
                                        WHEN b.cntr_value < 100
                                        THEN 100
                                        ELSE CONVERT(DECIMAL(18, 2), ((a.cntr_value * 1.0 / b.cntr_value) * 100.0))
                                    END
                            END AS '命中率%'
                    FROM
                    (
                        SELECT object_name,instance_name,cntr_value
                        FROM sys.dm_os_performance_counters
                        WHERE upper(counter_name) = '{p_name}'
                    ) a
                    CROSS JOIN
                    (
                        SELECT object_name,instance_name,cntr_value
                        FROM sys.dm_os_performance_counters
                        WHERE upper(counter_name) = '{p_name} BASE'
                    ) b
                    where a.instance_name = b.instance_name
                    and a.object_name = b.object_name
                    AND a.object_name like '%{obj_name}%'
                    """
            result, _ = mssql.execute(sql_ratio)
            if result.code == 0:
                value_temp = []
                for row in result.msg:
                    instance_name = row[0]
                    object_name = row[1]
                    value = row[2]
                    value_temp.append(value)
                    iname = instance_name + ' of ' + object_name.split(':')[1]
                    if len(instance_name.replace(' ','')) > 0:
                        vars.append(dict(name=iname, value=str(value)))
                    else:
                        metric.append(dict(index_id=cs(idx), value=cs(value)))
                if value_temp:
                    avg_value = round(mean(value_temp), 2)
                    if para_name == 'CATALOG METADATA:CACHE HIT RATIO':
                        metric.append(dict(index_id='2150007', value=cs(avg_value)))
                    elif para_name == 'CURSOR MANAGER BY TYPE:CACHE HIT RATIO':
                        metric.append(dict(index_id='2150008', value=cs(avg_value)))
                    elif para_name == 'PLAN CACHE:CACHE HIT RATIO':
                        metric.append(dict(index_id='2150009', value=cs(avg_value)))
                    elif para_name == 'LOG CACHE HIT RATIO':
                        metric.append(dict(index_id='2150023', value=cs(avg_value)))
                    elif para_name == 'SEGMENT CACHE HIT RATIO':
                        metric.append(dict(index_id='2150042', value=cs(avg_value)))
        else:
            if para_name.find(':') == -1:
                sql = f"""
                SELECT RTRIM(instance_name) ,RTRIM(object_name), cntr_value
                FROM sys.dm_os_performance_counters t
                WHERE upper(t.counter_name) = '{para_name}'
                """
            else:
                obj_name = para_name.split(':')[0]
                p_name = para_name.split(':')[1]
                sql = f"""
                SELECT RTRIM(instance_name) ,RTRIM(object_name), cntr_value
                FROM sys.dm_os_performance_counters t
                WHERE upper(t.counter_name) = '{p_name}'
                    AND upper(object_name) like '%{obj_name}%'
                """
            result, _ = mssql.execute(sql)
            if result.code == 0:
                temp_v = 0
                if len(result.msg) > 1:
                    for row in result.msg:
                        instance_name = row[0]
                        object_name = row[1]
                        value = row[2]
                        temp_v += value
                        if instance_name != '_Total':
                            if ':' in object_name:
                                iname = instance_name + ' of ' + object_name.split(':')[1]
                            else:
                                iname = instance_name + ' of ' + object_name
                            if len(instance_name.replace(' ','')) > 0:
                                vars.append(dict(name=iname, value=str(value)))
                            else:
                                metric.append(dict(index_id=cs(idx), value=cs(value)))
                else:
                    for row in result.msg:
                        value = row[2]
                        metric.append(dict(index_id=cs(idx), value=cs(value)))
                if para_name == 'ERRORS/SEC':
                    metric.append(dict(index_id='2150010', value=cs(temp_v)))
                elif para_name == 'LOCK REQUESTS/SEC':
                    metric.append(dict(index_id='2150012', value=cs(temp_v)))
                elif para_name == 'LOCK TIMEOUTS/SEC':
                    metric.append(dict(index_id='2150014', value=cs(temp_v)))
                elif para_name == 'LOCK WAIT TIME (MS)':
                    metric.append(dict(index_id='2150015', value=cs(temp_v)))
                elif para_name == 'LOCK WAITS/SEC':
                    metric.append(dict(index_id='2150017', value=cs(temp_v)))
                elif para_name == 'NUMBER OF DEADLOCKS/SEC':
                    metric.append(dict(index_id='2150019', value=cs(temp_v)))
                elif para_name == 'LOG BYTES FLUSHED/SEC':
                    metric.append(dict(index_id='2150021', value=cs(temp_v)))
                elif para_name == 'LOG FLUSH WAIT TIME':
                    metric.append(dict(index_id='2150024', value=cs(temp_v)))
                elif para_name == 'LOG FLUSH WAITS/SEC':
                    metric.append(dict(index_id='2150026', value=cs(temp_v)))
                elif para_name == 'LOG FLUSHES/SEC':
                    metric.append(dict(index_id='2150028', value=cs(temp_v)))
                elif para_name == 'LOG POOL CACHE MISSES/SEC':
                    metric.append(dict(index_id='2150030', value=cs(temp_v)))
                elif para_name == 'LOG POOL DISK READS/SEC':
                    metric.append(dict(index_id='2150032', value=cs(temp_v)))
                elif para_name == 'TRANSACTIONS/SEC':
                    metric.append(dict(index_id='2150034', value=cs(temp_v)))
                elif para_name == 'WRITE TRANSACTIONS/SEC':
                    metric.append(dict(index_id='2150036', value=cs(temp_v)))
                elif para_name == 'MIRRORED WRITE TRANSACTIONS/SEC':
                    metric.append(dict(index_id='2150038', value=cs(temp_v)))
                elif para_name == 'LOG BYTES RECEIVED/SEC':
                    metric.append(dict(index_id='2150040', value=cs(temp_v)))
        if vars:
            metric.append(dict(index_id=cs(idx), value=vars))


def server_running_time(mssql, metric, dbinfo):
    """
    获取数据库运行时间，单位：秒
    :param mssql:
    :return:
    """
    main_version = CommUtil.get_mssql_version(mssql)
    if float(main_version) > 9:  # SQLServer 2005及以上版本
        sql = "SELECT datediff(SECOND , sqlserver_start_time, GETDATE())  FROM sys.dm_os_sys_info"
    else:
        sql = "SELECT datediff(SECOND , create_date, GETDATE()) AS StartTime FROM sys.databases WHERE name = 'tempdb';"
    result, _ = mssql.execute(sql)
    seconds = result.msg[0][0]
    metric.append(dict(index_id="2150006", value=str(seconds)))
    for_t = CommUtil.FormatTime(seconds)
    target_id, pg = DBUtil.get_pg_env(dbinfo)
    sql2 = f"UPDATE  p_oracle_cib SET cib_value ='{for_t}' WHERE target_id = '{target_id}' AND index_id = 2230001 AND cib_name = 'running_time'"
    pg.execute(sql2)

def disk_usage(dbInfo, metric):
    """
    获取数据文件所在操作系统磁盘的使用率
    :param mssql:
    :param metric:
    :return:
    """
    mssql = DBUtil.get_mssql_env(dbInfo)
    db_v,db_vinfo = db_version(mssql)
    db_vinfo = str(db_vinfo)
    if float(db_v) > 10:
        db_list = get_dbname(mssql)
        temp = []
        for row in db_list:
            db = row[0]
            db_stat = row[1]
            if db_stat == 'ONLINE':
                mssql = DBUtil.get_mssql_env(dbInfo, db)
                sql = """
                SELECT DISTINCT 
                max(100 - CAST(CAST(available_bytes AS FLOAT) / CAST(total_bytes AS FLOAT) AS DECIMAL(18, 2)) * 100) AS [已使用(%)]
                FROM sys.database_files AS f
                CROSS APPLY sys.dm_os_volume_stats(DB_ID(), f.file_id);
                """
                result, col_list = mssql.execute(sql)
                if result.code == 0:
                    for row in result.msg:
                        used_p = row[0]
                        temp.append(used_p)
        max_used_per = max(temp)
    else:
        # sql_enalbe_sqlcmd = '''
        # DECLARE @sql VARCHAR(2000)
        # SET @sql ='
        # COMMIT;
        # EXEC sp_configure ''show advanced options'',1;
        # RECONFIGURE WITH OVERRIDE;
        # EXEC sp_configure ''xp_cmdshell'',1;
        # RECONFIGURE WITH OVERRIDE;
        # '
        # EXEC(@sql)
        # '''
        # sql_disalbe_sqlcmd = '''
        # DECLARE @sql VARCHAR(2000)
        # SET @sql ='
        # COMMIT;
        # EXEC sp_configure ''show advanced options'',1;
        # RECONFIGURE WITH OVERRIDE;
        # EXEC sp_configure ''xp_cmdshell'',0;
        # RECONFIGURE WITH OVERRIDE;
        # '
        # EXEC(@sql)
        # '''
        # mssql.execute_sqlcmd(sql_enalbe_sqlcmd)
        # result, col_list = mssql.execute('EXEC master.dbo.xp_fixeddrives;')
        # if result.code == 0:
        #     row_dict = []
        #     for row in result.msg:
        #         disk = row[0]
        #         row_dict.append(disk)
        # temp = []
        # for i in row_dict:
        #     sql_disk = f"EXEC sys.xp_cmdshell 'fsutil volume diskfree {i}:'"
        #     result2, col_list2 = mssql.execute(sql_disk)
        #     mssql.execute_sqlcmd(sql_disalbe_sqlcmd)
        #     if result2.code == 0:
        #         n = 0
        #         disk_avail = ''
        #         disk_total = ''
        #         for row in result2.msg:
        #             if n == 0:
        #                 disk_avail = row[0].split(':')[1]
        #             elif n == 1:
        #                 disk_total = row[0].split(':')[1]
        #             n += 1
        #         used_per = round(100 - float(disk_avail)*100/float(disk_total),2)
        #         temp.append(used_per)
        max_used_per = 'null'
    metric.append(dict(index_id="2154005", value=str(max_used_per)))


def active_session(mssql, metric):
    """
    获取活动会话数量
    :return:
    """
    sql = "SELECT count(*) FROM sys.sysprocesses where status in ('runnable','suspended')"
    result, _ = mssql.execute(sql)
    active_nums = result.msg[0][0]
    metric.append(dict(index_id="2151038", value=active_nums))
    sql2 = 'SELECT count(*) FROM sys.sysprocesses'
    result, _ = mssql.execute(sql2)
    total_session = result.msg[0][0]
    metric.append(dict(index_id="2151133", value=total_session))
    sql3 = 'SELECT count(*) FROM sys.sysprocesses where blocked >0'
    result, _ = mssql.execute(sql3)
    block_session = result.msg[0][0]
    metric.append(dict(index_id="2151143", value=block_session))


def long_sql(mssql, metric):
    """
    获取执行时间超过5秒SQL的个数
    :return:
    """
    sql = '''
    SELECT COUNT(*)
    FROM sys.dm_exec_query_stats qs
         CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) st
    WHERE total_elapsed_time / execution_count / 1000 / 1000 > 5;
    '''
    result, col_list = mssql.execute(sql)
    sqls = result.msg.fetchone()[0]
    metric.append(dict(index_id="2151122", value=sqls))


def file_io_stall(mssql, metric):
    """
    数据文件IO最大延迟时间
    :return:
    """
    sql = """
    SELECT MAX(CAST((io_stall_read_ms + io_stall_write_ms) / (1.0 + num_of_reads + num_of_writes) AS NUMERIC(10, 1))) AS [avg_io_stall_ms]
    FROM sys.dm_io_virtual_file_stats(NULL, NULL);
    """
    result, _ = mssql.execute(sql)
    io_stall = result.msg[0][0]
    metric.append(dict(index_id="2151174", value=str(io_stall)))


def alwayson_info(mssql, metric):
    """
    获取Always on集群状态信息
    :param mssql:
    :param metric:
    :return:
    """
    global sync_state, lag_seconds, redo_queue_size, sync_healthy, log_send_rate, redo_rate
    sql = """
    SELECT Sec_CommitTime.synchronization_health AS N'同步健康状态', 
        Sec_CommitTime.synchronization_state AS N'同步状态', 
        Sec_CommitTime.log_send_rate AS N'平均发送日志速率(Kb/S)', 
        Sec_CommitTime.redo_queue_size AS N'未应用日志(Kb)', 
        Sec_CommitTime.redo_rate AS N'平均应用日志速率(Kb/S)', 
        DATEDIFF(ss, Sec_CommitTime.last_commit_time, Pri_CommitTime.last_commit_time) AS [延迟时间(秒)]
    FROM
    (
        SELECT replica_server_name, 
            DBName, 
            last_commit_time
        FROM
        (
            SELECT AR.replica_server_name, 
                HARS.role_desc, 
                DB_NAME(DRS.database_id) [DBName], 
                DRS.last_commit_time
            FROM sys.dm_hadr_database_replica_states DRS
                INNER JOIN sys.availability_replicas AR ON DRS.replica_id = AR.replica_id
                INNER JOIN sys.dm_hadr_availability_replica_states HARS ON AR.group_id = HARS.group_id
                                                                            AND AR.replica_id = HARS.replica_id
        ) AG_Stats
        WHERE role_desc = 'PRIMARY'
    ) Pri_CommitTime
    INNER JOIN
    (
        SELECT replica_server_name, 
            DBName, 
            last_commit_time, 
            synchronization_health, 
            synchronization_state, 
            log_send_rate, 
            redo_queue_size, 
            redo_rate
        FROM
        (
            SELECT AR.replica_server_name, 
                HARS.role_desc, 
                DB_NAME(DRS.database_id) [DBName], 
                DRS.last_commit_time, 
                DRS.synchronization_health, 
                DRS.synchronization_state, 
                DRS.log_send_rate, 
                DRS.redo_queue_size, 
                DRS.redo_rate
            FROM sys.dm_hadr_database_replica_states DRS
                INNER JOIN sys.availability_replicas AR ON DRS.replica_id = AR.replica_id
                INNER JOIN sys.dm_hadr_availability_replica_states HARS ON AR.group_id = HARS.group_id
                                                                            AND AR.replica_id = HARS.replica_id
        ) AG_Stats
        WHERE role_desc = 'SECONDARY'
    ) Sec_CommitTime ON [Sec_CommitTime].[DBName] = [Pri_CommitTime].[DBName];
    """
    result, _ = mssql.execute(sql)
    sync_healthy_temp = -1
    sync_state_temp = -1
    log_send_rate_temp = []
    redo_queue_size_temp = []
    redo_rate_temp = []
    lag_seconds_temp = []
    sync_healthy = 2
    sync_state = 2
    log_send_rate = 0
    redo_queue_size = 0
    redo_rate = 0
    lag_seconds = 0
    flag = 0
    if result.code == 0:
        for row in result.msg:
            flag = 1
            sync_healthy = row[0]
            if sync_healthy != 2:
                sync_healthy_temp = sync_healthy
            sync_state = row[1]
            if sync_state == 0:
                sync_state_temp = 0
            log_send_rate = row[2]
            log_send_rate_temp.append(log_send_rate)
            redo_queue_size = row[3]
            redo_queue_size_temp.append(redo_queue_size)
            redo_rate = row[4]
            redo_rate_temp.append(redo_rate)
            lag_seconds = row[5]
            lag_seconds_temp.append(lag_seconds if lag_seconds else 0)
    if sync_state_temp == -1:
        metric.append(dict(index_id="2157002", value=str(sync_state)))
    else:
        metric.append(dict(index_id="2157002", value=str(sync_state_temp)))
    if flag == 1:
        metric.append(dict(index_id="2157003", value=str(max(lag_seconds_temp))))
        metric.append(dict(index_id="2157004", value=str(max(redo_queue_size_temp))))
        metric.append(dict(index_id="2157006", value=str(max(log_send_rate_temp))))
        metric.append(dict(index_id="2157007", value=str(max(redo_rate_temp))))
    else:
        metric.append(dict(index_id="2157003", value=str(lag_seconds)))
        metric.append(dict(index_id="2157004", value=str(redo_queue_size)))
        metric.append(dict(index_id="2157006", value=str(log_send_rate)))
        metric.append(dict(index_id="2157007", value=str(redo_rate)))
    if sync_healthy_temp == -1:
        metric.append(dict(index_id="2157005", value=str(sync_healthy)))
    else:
        metric.append(dict(index_id="2157005", value=str(sync_healthy_temp)))


def file_usage(dbInfo, metric):
    """
    获取数据文件最大使用率、可用大小
    :param mssql:
    :param metric:
    :return:
    """
    mssql = DBUtil.get_mssql_env(dbInfo)
    db_list = get_dbname(mssql)
    db_v,_ = db_version(mssql)
    vals = []
    vals2 = []
    vals3 = []
    vals4 = []
    vals5 = []
    vals6 = []
    for row in db_list:
        db = row[0]
        db_stat = row[1]
        if db_stat == 'ONLINE':
            mssql = DBUtil.get_mssql_env(dbInfo, db)
            if float(db_v) > 10:
                sql = """
                SELECT name,
                    size  / 128 - FILEPROPERTY(name, 'spaceused')  / 128 [未用空间(M)],
                    CASE
                        WHEN growth = 0
                                AND max_size != -1
                        THEN size / 128 - FILEPROPERTY(name, 'spaceused') / 128
                        WHEN growth != 0
                                AND max_size = -1
                        THEN available_bytes / 1024 / 1024 - FILEPROPERTY(name, 'spaceused') / 128
                        ELSE(CASE
                                    WHEN available_bytes / 1024 / 1024 > max_size / 128
                                    THEN max_size / 128 - FILEPROPERTY(name, 'spaceused') / 128
                                    ELSE available_bytes / 1024 / 1024 - FILEPROPERTY(name, 'spaceused') / 128
                                END)
                    END [最大未用空间(M)], 
                    CONVERT(DECIMAL(18, 2), FILEPROPERTY(name, 'spaceused') * 100.0 / size) [使用率(%)],
                    CASE
                        WHEN growth = 0
                        THEN CONVERT(DECIMAL(18, 2), FILEPROPERTY(name, 'spaceused') * 100.0 / size)
                        WHEN growth != 0
                                AND max_size = -1
                        THEN CONVERT(DECIMAL(18, 2), FILEPROPERTY(name, 'spaceused') / 128 * 100.0 / (available_bytes / 1024 / 1024))
                        ELSE CONVERT(DECIMAL(18, 2), FILEPROPERTY(name, 'spaceused') * 100.0 / max_size)
                    END [占最大大小使用率(%)],
                    CONVERT(DECIMAL(18, 2), available_bytes / 1073741824.0) AS [可用大小(GB)], 
                    100 - CAST(CAST(available_bytes AS FLOAT) / CAST(total_bytes AS FLOAT) AS DECIMAL(18, 2)) * 100 AS [已使用(%)]
                FROM sys.database_files AS f
                    CROSS APPLY sys.dm_os_volume_stats(DB_ID(), f.file_id);
                """
                result, _ = mssql.execute(sql)
                if result.code == 0:
                    for row in result.msg:
                        file_name = row[0]
                        vals.append(dict(name=file_name, value=cs(row[1])))
                        vals2.append(dict(name=file_name, value=cs(row[2])))
                        vals3.append(dict(name=file_name, value=cs(row[3])))
                        vals4.append(dict(name=file_name, value=cs(row[4])))
                        vals5.append(dict(name=file_name, value=cs(row[5])))
                        vals6.append(dict(name=file_name, value=cs(row[6])))
            else:
                sql = """
                    SELECT name,
                            size / 128 - FILEPROPERTY(name, 'spaceused') / 128 [未用空间(M)], 
                            CASE
                                    WHEN max_size != -1
                                        AND growth != 0
                                    THEN max_size / 128 - FILEPROPERTY(name, 'spaceused') / 128
                                    WHEN max_size = -1
                                    THEN 9999999999
                                END [最大未用空间(M)], 
                            CONVERT(DECIMAL(18, 2), FILEPROPERTY(name, 'spaceused') * 100.0 / size) [使用率(%)], 
                            CASE
                                    WHEN growth = 0
                                    THEN CONVERT(DECIMAL(18, 2), FILEPROPERTY(name, 'spaceused') * 100.0 / size)
                                    WHEN growth != 0
                                        AND max_size != -1
                                    THEN CONVERT(DECIMAL(18, 2), FILEPROPERTY(name, 'spaceused') * 100.0 / max_size)
                                    ELSE 0
                                END [占最大大小使用率(%)]
                    FROM sys.database_files AS f;
                """
                result, _ = mssql.execute(sql)
                if result.code == 0:
                    for row in result.msg:
                        file_name = row[0]
                        vals.append(dict(name=file_name, value=cs(row[1])))
                        vals2.append(dict(name=file_name, value=cs(row[2])))
                        vals3.append(dict(name=file_name, value=cs(row[3])))
                        vals4.append(dict(name=file_name, value=cs(row[4])))
    metric.append(dict(index_id="2154006", value=vals))
    metric.append(dict(index_id="2154007", value=vals2))
    metric.append(dict(index_id="2154008", value=vals3))
    metric.append(dict(index_id="2154009", value=vals4))
    metric.append(dict(index_id="2154010", value=vals5))
    metric.append(dict(index_id="2154011", value=vals6))


def wait_even(mssql, metric):
    """
    查看常见等待事件等待时间
    :param mssql:
    :param metric:
    :return:
    """
    event_basic = {
        'CXPACKET': 2152050,
        # 'AVG_CXPACKET': 2152051,
        'PAGEIOLATCH_EX': 2152054,
        # 'AVG_PAGEIOLATCH_EX': 2152055,
        'PAGEIOLATCH_DT': 2152056,
        # 'AVG_PAGEIOLATCH_DT': 2152057,
        'PAGEIOLATCH_KP': 2152058,
        # 'AVG_PAGEIOLATCH_KP': 2152059,
        'PAGEIOLATCH_SH': 2152060,
        # 'AVG_PAGEIOLATCH_SH': 2152061,
        'PAGEIOLATCH_UP': 2152062,
        # 'AVG_PAGEIOLATCH_UP': 2152063,
        'IO_COMPLETION': 2152064,
        # 'AVG_IO_COMPLETION': 2152065,
        'ASYNC_IO_COMPLETION': 2152066,
        # 'AVG_ASYNC_IO_COMPLETION': 2152067,
        'LCK_M_X': 2152068,
        # 'AVG_LCK_M_X': 2152069,
        'LCK_M_S': 2152070,
        # 'AVG_LCK_M_S': 2152071,
        'LCK_M_U': 2152072,
        # 'AVG_LCK_M_U': 2152073,
        'LCK_M_BU': 2152074,
        # 'AVG_LCK_M_BU': 2152075,
        'WRITELOG': 2152076,
        # 'AVG_WRITELOG': 2152077,
        'LOGBUFFER': 2152078,
        # 'AVG_LOGBUFFER': 2152079,
        'MSQL_XP': 2152080,
        # 'AVG_MSQL_XP': 2152081,
        'RESOURCE_SEMAPHORE': 2152082,
        # 'AVG_RESOURCE_SEMAPHORE': 2152083,
        'THREADPOOL': 2152084,
        # 'AVG_THREADPOOL': 2152085,
        'PAGELATCH_SH': 2152086,
        # 'AVG_PAGELATCH_SH': 2152087,
        'PAGELATCH_EX': 2152088,
        # 'AVG_PAGELATCH_EX': 2152089,
        'WRITE_COMPLETION': 2152090
        # 'AVG_WRITE_COMPLETION': 2152091
    }
    for para_name in event_basic.keys():
        idx = event_basic.get(para_name)
        sql = f"""
        SELECT 
            wait_time_ms 总等待时间_MS
        FROM sys.dm_os_wait_stats
        WHERE wait_type = '{para_name}';
        """
        result, col_list = mssql.execute(sql)
        if result.code == 0:
            for row in result.msg:
                value = row[0]
                metric.append(dict(index_id=cs(idx), value=cs(value)))


def log_trans(mssql, metric):
    """
    日志传输相关指标
    :param mssql:
    :param metric:
    :return:
    """
    sql = "select last_restored_latency from msdb.dbo.log_shipping_monitor_secondary;"
    result, col_list = mssql.execute(sql)
    flag = 0
    restored_latency = 0
    if result.code == 0:
        for row in result.msg:
            flag = 1
            restored_latency = row[0]
    if flag == 1:
        metric.append(dict(index_id="2157008", value=restored_latency))
    else:
        metric.append(dict(index_id="2157008", value=0))


def mirror_conn(mssql,metric):
    "采集镜像连接相关指标"
    sql = "select connection_id,total_bytes_received,total_bytes_sent,total_receives,total_sends,receives_posted,is_receive_flow_controlled,sends_posted,is_send_flow_controlled from sys.dm_db_mirroring_connections"
    result, col_list = mssql.execute(sql)
    vals = []
    vals2 = []
    vals3 = []
    vals4 = []
    vals5 = []
    vals6 = []
    vals7 = []
    vals8 = []
    if result.code == 0:
        for row in result.msg:
            name = str(row[0])
            total_bytes_received = row[1]
            total_bytes_sent = row[2]
            total_receives = row[3]
            total_sends = row[4]
            receives_posted = row[5]
            is_receive_flow_controlled = row[6]
            sends_posted = row[7]
            is_send_flow_controlled = row[8]
            vals.append(dict(name=name, value=str(total_bytes_received)))
            vals2.append(dict(name=name, value=str(total_bytes_sent)))
            vals3.append(dict(name=name, value=str(total_receives)))
            vals4.append(dict(name=name, value=str(total_sends)))
            vals5.append(dict(name=name, value=str(receives_posted)))
            vals6.append(dict(name=name, value=str(sends_posted)))
            vals7.append(dict(name=name, value=str(is_receive_flow_controlled)))
            vals8.append(dict(name=name, value=str(is_send_flow_controlled)))
    metric.append(dict(index_id="2151134", value=vals))
    metric.append(dict(index_id="2151135", value=vals2))
    metric.append(dict(index_id="2151136", value=vals3))
    metric.append(dict(index_id="2151137", value=vals4))
    metric.append(dict(index_id="2151138", value=vals5))
    metric.append(dict(index_id="2151139", value=vals6))
    metric.append(dict(index_id="2151140", value=vals7))
    metric.append(dict(index_id="2151141", value=vals8))
    sql2 = """
    SELECT t.name AS '数据库名', 
        s.mirroring_state AS '状态'
    FROM sys.database_mirroring s, 
        sys.databases t
    WHERE mirroring_guid IS NOT NULL
        AND t.database_id = s.database_id
    """
    result2, _ = mssql.execute(sql2)
    vals9 = []
    if result2.code == 0:
        for row in result2.msg:
            dbname = row[0]
            mirroring_state = row[1]
            vals9.append(dict(name=dbname, value=str(mirroring_state)))
    metric.append(dict(index_id="2151142", value=vals9))


def db_status(mssql,metric):
    # 数据库非正常状态
    sql = """
    SELECT
        state_desc AS '状态',
        COUNT(*)
    FROM
        sys.databases
    WHERE
        state_desc in ('RECOVERY_PENDING', 'SUSPECT', 'EMERGENCY', 'OFFLINE', 'OFFLINE_SECONDARY')
    GROUP BY
        state_desc
    """
    result, _ = mssql.execute(sql)
    vals = []
    if result.code == 0:
        for row in result.msg:
            state_desc = row[0]
            state_nums = row[1]
            vals.append(dict(name=state_desc, value=str(state_nums)))
    metric.append(dict(index_id="2150064", value=vals))


def ag_role(mssql,metric):
    sql = "select convert(nvarchar(36), group_id), role_desc from sys.dm_hadr_availability_replica_states where is_local=1"
    result, _ = mssql.execute(sql)
    uid, pg= DBUtil.get_pg_env()
    vals = []
    vals2 = []
    if result.code == 0:
        for row in result.msg:
            group_id = row[0]
            role_desc = row[1]
            vals.append(dict(name=group_id, value=str(role_desc)))
            sql = f"select value from mon_indexdata where uid = '{uid}' and index_id=2150065 and iname = '{group_id}'"
            curs = DBUtil.getValue(pg, sql)
            rs = curs.fetchone()
            if rs and rs[0]:
                if rs[0] != role_desc:
                    vals2.append(dict(name=group_id, value='1'))
                else:
                    vals2.append(dict(name=group_id, value='0'))
            else:
                vals2.append(dict(name=group_id, value='0'))
    metric.append(dict(index_id="2150065", value=vals))
    metric.append(dict(index_id="2150066", value=vals2))

def server_main(dbInfo, metric):
    """
    获取SqlServer CIB指标总函数
    :param mssql:
    :return:
    """
    cur_time = datetime.now()
    mssql = DBUtil.get_mssql_env(dbInfo)
    lat_time = datetime.now()
    diff_ms = (lat_time - cur_time).microseconds
    metric.append(dict(index_id="1000102", value=str(round(diff_ms/1000,0))))
    server_running_time(mssql, metric,dbInfo)
    os_performance_counters(mssql, metric)
    one_result(mssql, 'select @@total_read as 物理读', 2151008, metric)
    one_result(mssql, 'select @@total_read as 物理读', 2151036, metric)
    one_result(mssql, 'select @@total_write as 物理写', 2151009, metric)
    one_result(mssql, 'select @@pack_sent as 网络发送包', 2151011, metric)
    one_result(mssql, 'select @@pack_received as 网络接收包', 2151012, metric)
    one_result(mssql, 'select @@packet_errors as 网络包错误', 2151013, metric)
    one_result(mssql, 'select sum(total_logical_reads) as 逻辑读 FROM sys.dm_exec_query_stats ', 2151037, metric)
    db_v = CommUtil.get_mssql_version(mssql)
    if float(db_v) > 9:
        one_result(mssql,'SELECT ROUND(CONVERT(float ,PHYSICAL_MEMORY_IN_USE_KB) * 100/ CONVERT(float,TOTAL_PHYSICAL_MEMORY_KB), 2) FROM sys.dm_os_process_memory, sys.dm_os_sys_memory',2151001, metric)
        one_result(mssql,'SELECT ROUND(100- CONVERT(float ,available_physical_memory_kb) * 100/ CONVERT(float,TOTAL_PHYSICAL_MEMORY_KB), 2) FROM sys.dm_os_sys_memory',2151002, metric)
        # DB 占用CPU
        sql_db_cpu = '''
        SELECT TOP (1) SQLProcessUtilization AS [SQLServer Process CPU Utilization]
        FROM
        ( SELECT record.value('(./Record/@id)[1]', 'int') AS record_id,
                   record.value('(./Record/SchedulerMonitorEvent/SystemHealth/SystemIdle)[1]', 'int') AS [SystemIdle],
                   record.value('(./Record/SchedulerMonitorEvent/SystemHealth/ProcessUtilization)[1]', 'int') AS [SQLProcessUtilization]
            FROM
            ( SELECT CONVERT(XML, record) AS [record]
                FROM sys.dm_os_ring_buffers WITH(NOLOCK)
                WHERE ring_buffer_type = N'RING_BUFFER_SCHEDULER_MONITOR'
                      AND record LIKE N'%<SystemHealth>%'
            ) AS x
        ) AS y
        ORDER BY record_id DESC OPTION(RECOMPILE)
        '''
        # OS 占用CPU
        sql_os_cpu = '''
            SELECT TOP (1) 100 - SystemIdle AS [Total CPU Utilization]
            FROM
            ( SELECT record.value('(./Record/@id)[1]', 'int') AS record_id,
                       record.value('(./Record/SchedulerMonitorEvent/SystemHealth/SystemIdle)[1]', 'int') AS [SystemIdle],
                       record.value('(./Record/SchedulerMonitorEvent/SystemHealth/ProcessUtilization)[1]', 'int') AS [SQLProcessUtilization]
                FROM
                ( SELECT CONVERT(XML, record) AS [record]
                    FROM sys.dm_os_ring_buffers WITH(NOLOCK)
                    WHERE ring_buffer_type = N'RING_BUFFER_SCHEDULER_MONITOR'
                          AND record LIKE N'%<SystemHealth>%'
                ) AS x
            ) AS y
            ORDER BY record_id DESC OPTION(RECOMPILE)
        '''
    else:
        sql_db_cpu = '''
        SELECT TOP (1) SQLProcessUtilization AS [SQLServer Process CPU Utilization]
        FROM
        ( SELECT record.value('(./Record/@id)[1]', 'int') AS record_id,
                   record.value('(./Record/SchedulerMonitorEvent/SystemHealth/SystemIdle)[1]', 'int') AS [SystemIdle],
                   record.value('(./Record/SchedulerMonitorEvent/SystemHealth/ProcessUtilization)[1]', 'int') AS [SQLProcessUtilization]
            FROM
            ( SELECT CONVERT(XML, record) AS [record]
                FROM sys.dm_os_ring_buffers WITH(NOLOCK)
                WHERE ring_buffer_type = N'RING_BUFFER_SCHEDULER_MONITOR'
                      AND record LIKE N'%<SystemHealth>%'
            ) AS x
        ) AS y
        ORDER BY record_id DESC OPTION(RECOMPILE)
        '''
        sql_os_cpu = '''
            SELECT TOP (1) 100 - SystemIdle  AS [Total CPU Utilization]
            FROM
            ( SELECT record.value('(./Record/@id)[1]', 'int') AS record_id,
                       record.value('(./Record/SchedulerMonitorEvent/SystemHealth/SystemIdle)[1]', 'int') AS [SystemIdle],
                       record.value('(./Record/SchedulerMonitorEvent/SystemHealth/ProcessUtilization)[1]', 'int') AS [SQLProcessUtilization]
                FROM
                ( SELECT CONVERT(XML, record) AS [record]
                    FROM sys.dm_os_ring_buffers WITH(NOLOCK)
                    WHERE ring_buffer_type = N'RING_BUFFER_SCHEDULER_MONITOR'
                          AND record LIKE N'%<SystemHealth>%'
                ) AS x
            ) AS y
            ORDER BY record_id DESC OPTION(RECOMPILE)
        '''
    os_platform = db_platform(mssql)
    if os_platform== 'windows':
        one_result(mssql, sql_db_cpu, "2151007", metric)
    else:
        one_result(mssql, 'select 0', "2151007", metric)
    # OS 总CPU使用率
    if os_platform == 'windows':
        one_result(mssql, sql_os_cpu, "2151050", metric)
    else:
        one_result(mssql, 'select 0', "2151050", metric)
    # 磁盘使用率
    disk_usage(dbInfo, metric)
    # 活动会话数
    active_session(mssql, metric)
    # 数据文件IO最大延迟时间
    file_io_stall(mssql, metric)
    # Always on集群信息v
    if float(db_v) >= 11:  #从 2012开始才支持Always on集群
        alwayson_info(mssql, metric)
    # 数据文件和所在磁盘的最大使用率、可用大小
    file_usage(dbInfo, metric)
    # 常见等待事件等待时间
    wait_even(mssql, metric)
    # 日志传输、还原延迟、分钟
    log_trans(mssql, metric)
    # 镜像数据库指标采集
    mirror_conn(mssql,metric)
    # 数据库非正常状态
    db_status(mssql,metric)
    ag_role(mssql,metric)


if __name__ == '__main__':
    dbInfo = eval(sys.argv[1])
    metric = []
    db_flag = 0
    cur_time = datetime.now()
    mssql = DBUtil.get_mssql_env(dbInfo)
    metric.append(dict(index_id="1000102", value=str(round((datetime.now() - cur_time).microseconds/1000,0))))
    rs = []
    if mssql.conn:
        db_list = get_dbname(mssql)
        for row in db_list:
            db = row[0]
            db_stat = row[1]
            # if db_stat == 'OFFLINE':
            #     db_flag = 1
            #     db_temp += f'{db},'
    else:
        db_flag = 1
    if db_flag == 0:
        metric.append(dict(index_id="2150000", value="连接成功"))
        server_main(dbInfo, metric)
    else:
        metric.append(dict(index_id="2150000", value="连接失败"))
    lat_time = datetime.now()
    diff_ms = (lat_time - cur_time).microseconds
    metric.append(dict(index_id="1000101", value=str(round(diff_ms/1000,0))))
    print('{"results":' + json.dumps(metric, ensure_ascii=False) + '}')

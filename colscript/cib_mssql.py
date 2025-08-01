#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@文件    :cib_mssql.py
@说明    :SQL Server cib 信息采集
@时间    :2021/09/01 15:54:55
@作者    :xxxx
@版本    :2.0.1
'''


import datetime
import json
import sys
import re
import os
sys.path.append('/usr/software/knowl')
import DBUtil
import CommUtil

global target_ip
global main_version
global version_info

main_version = ''
target_ip = ''
version_info = ''

def db_version(mssql):
    """
    获取数据库的版本号
    :param mssql:
    :return:
    """
    global main_version
    global version_info
    sql_version = "SELECT SUBSTRING(convert(varchar(50),CAST(SERVERPROPERTY('ProductVersion') AS nvarchar(100))),1,14) AS Edition"
    out_version, col_list = mssql.execute(sql_version)
    db_v = out_version.msg[0][0].split('.')[0]
    if db_v.isdigit():
        main_version = db_v
    version_info = out_version.msg[0][0]


def cs(val, dt=False):
    if val is None:
        return ''
    else:
        if dt:
            return val.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return str(val)


def db_platform(mssql):
    """
    查看数据库运行平台
    :param mssql:
    :return:
    """
    sql_2017 = 'select host_platform from master.sys.dm_os_host_info'
    os_platform = 'Windows'
    if float(main_version) > 13:  # SQLServer 2017及以上版本
        result, col_list = mssql.execute(sql_2017)
        if result.code == 0:
            for row in result.msg:
                os_platform = row[0]
        return os_platform
    else:
        return os_platform


def server_summary(mssql, row_dict):
    """
    获取数据库概要
    :param mssql:
    :return:
    """

    sql = """
    SELECT CAST(SERVERPROPERTY('MachineName') AS nvarchar(100)) AS 'hostname', 
           CAST(SERVERPROPERTY('ServerName') AS nvarchar(100)) AS 'servername',
           CAST(CASE
               WHEN SERVERPROPERTY('InstanceName') IS NULL
               THEN @@SERVERNAME
               ELSE SERVERPROPERTY('InstanceName')
           END AS nvarchar(100)) AS 'instance_name', 
           CAST(SERVERPROPERTY('Edition') AS nvarchar(100)) AS 'db_edition', 
           CAST(SERVERPROPERTY('ProductLevel') AS nvarchar(100)) AS 'product_level', 
           CAST(SERVERPROPERTY('Collation') AS nvarchar(100)) AS 'collation', 
           physical_name AS 'data_file_path', 
           physical_name AS 'log_file_path',
           CAST(CASE SERVERPROPERTY('IsClustered')
               WHEN 0
               THEN 'Not Clustered'
               ELSE 'Clustered'
           END AS nvarchar(100)) AS 'clustered'
    FROM sys.database_files
    WHERE type_desc = 'ROWS';
      """
    result, col_list = mssql.execute(sql)
    if result.code == 0:
        for row in result.msg:
            for col, col_name in zip(range(len(col_list)), col_list):
                file_path = row[6]
                filepath, tempfilename = os.path.split(file_path.replace('\\', '/'))
                if col == 6:
                    row_dict.append(dict(name=col_name, value=filepath))
                elif col == 7:
                    row_dict.append(dict(name=col_name, value=filepath))
                else:
                    row_dict.append(dict(name=col_name, value=row[col]))
    row_dict.append(dict(name='version_num', value=version_info))
    if float(main_version) > 10:  # SQLServer 2012及以上版本
        sql2 = "SELECT [physical_memory_kb] FROM [master].[sys].[dm_os_sys_info]"
    else:
        sql2 = "SELECT round(physical_memory_in_bytes/1024,0) FROM [master].[sys].[dm_os_sys_info]"
    rs2, _ = mssql.execute(sql2)
    if rs2.code == 0:
        for row in rs2.msg:
            row_dict.append(dict(name='os_memory', value=str(row[0])))


def server_startup_time(mssql, row_dict):
    """
    获取数据库启动时间
    :param mssql:
    :return:
    """
    sql = "SELECT create_date AS StartTime FROM sys.databases WHERE name = 'tempdb';"
    result, _ = mssql.execute(sql)
    out = result.msg[0][0]
    time_str = datetime.datetime.strftime(out, '%Y-%m-%d %H:%M:%S')
    row_dict.append(dict(name='startup_time', value=time_str))


def server_running_time(mssql, row_dict):
    """
    获取数据库运行时间
    :param mssql:
    :return:
    """
    sql = "SELECT datediff(SECOND , create_date, GETDATE()) AS StartTime FROM sys.databases WHERE name = 'tempdb';"
    result, _ = mssql.execute(sql)
    out = result.msg[0][0]
    seconds = CommUtil.FormatTime(out)
    row_dict.append(dict(name='running_time', value=seconds))


def os_summary(mssql, row_dict):
    """
    各个数据库概要信息
    :param mssql:
    :return:
    """
    sql_db = "EXEC xp_msver;"
    result, _ = mssql.execute(sql_db)
    language = ''
    if result.code == 0:
        for row in result.msg:
            if row[1].lower() == 'language':
                language = row[3]
    sql_version = "SELECT @@VERSION AS 'SQL Server Version';"
    result2, col_list2 = mssql.execute(sql_version)
    if result2.code == 0:
        for row in result2.msg:
            db_version_name = str(row[0]).split(' - ')[0]
            db_version = re.search(r'[0-9]\d{0,1}.[0-9]\d{0,1}.[0-9]\d{3}.[0-9]\d{0,1}', str(row), re.M | re.I).group()
            os_arch = re.search(r'X[0-9]{2}', str(row), re.M | re.I).group()
            os_info = str(row[0]).split(' on ')[1]
            os_name = os_info.split('(')[0]
            os_release = os_info[os_info.find('(') + 1:os_info.find(')')]
            os_version = re.search(r'\d+.\d+', os_release, re.M | re.I).group()
    row_dict.append(dict(name='host_platform', value=os_name))
    row_dict.append(dict(name='host_distribution', value=os_release))
    row_dict.append(dict(name='system_info', value=os_arch))
    row_dict.append(dict(name='host_service_pack_level', value=os_version))
    row_dict.append(dict(name='alias', value=language))
    row_dict.append(dict(name='db_version', value=db_version_name + f'({db_version})'))
    row_dict.append(dict(name="host_ip", value=cs(target_ip)))
    sql_mirror = """
    SELECT t.name AS '数据库名', 
        s.mirroring_state_desc AS '状态', 
        mirroring_role_desc AS '角色', 
        mirroring_safety_level_desc AS '安全级别', 
        mirroring_witness_name AS '见证实例名', 
        mirroring_witness_state_desc AS '见证实例状态',mirroring_partner_name AS '镜像服务名',mirroring_partner_instance as '镜像实例名','null' as "null",'null' as "null"
    FROM sys.database_mirroring s, 
        sys.databases t
    WHERE mirroring_guid IS NOT NULL
        AND t.database_id = s.database_id
    """
    flag = 0
    result2, col_list2 = mssql.execute(sql_mirror)
    row_dict2 = []
    if result2.code == 0:
        data_col = {}
        n = 0
        for col_name in col_list2:
            n = n + 1
            if col_name == 'null':
                col_name = None
                data_col['c%s' % n] = str(col_name)
            else:
                data_col['c%s' % n] = str(col_name)
        row_dict2.append(data_col)
        for row in result2.msg:
            flag = 1
            data = {}
            for col in range(len(col_list2)):
                n = col + 1
                row_re = row[col]
                if str(row[col]) == 'null':
                    row_re = None
                    data['c%s' % n] = str(row_re)
                else:
                    data['c%s' % n] = str(row_re)
            row_dict2.append(data)
    metric.append(dict(index_id="2230003", content=row_dict2))
    if flag == 1:
        row_dict.append(dict(name="is_mirror", value='YES'))
    else:
        row_dict.append(dict(name="is_mirror", value='NO'))
    


def os_manufacturer(mssql):
    """
    获取服务器品牌厂商、系统类型
    :param mssql:
    :return:
    """
    os_platform = db_platform(mssql)
    if os_platform.lower() == 'windows' and float(main_version) > 9:
        sql = 'EXEC xp_readerrorlog 0,1,"Manufacturer"'
        temp = []
        result, col_list = mssql.execute(sql)
        if result.code == 0:
            for row in result.msg:
                row_dict = []
                for col in range(len(col_list)):
                    row_dict.append(row[col])
                temp.append(row_dict)
    else:
        temp = ''
    return temp


def cpu_mode(mssql):
    """
    获取CPU型号
    :param mssql:
    :return:
    """
    os_platform = db_platform(mssql)
    if os_platform.lower() == 'windows':
        sql = r"EXEC xp_instance_regread 'HKEY_LOCAL_MACHINE','HARDWARE\DESCRIPTION\System\CentralProcessor\0','ProcessorNameString'"
        result, col_list = mssql.execute(sql)
        temp = []
        if result.code == 0:
            for row in result.msg:
                for col in range(len(col_list)):
                    temp.append(row[col])
    else:
        temp = ''
    return temp


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


def db_datafile(dbInfo, row_dict3):
    """
    查看数据文件配置信息
    :return:
    """
    # 获取所有数据库名
    target_id, pg = DBUtil.get_pg_env()
    mssql = DBUtil.get_mssql_env(dbInfo)
    db_list = get_dbname(mssql)
    row_dict = []
    row_dict2 = []
    for row in db_list:
        db = row[0]
        db_stat = row[1]
        if db_stat == 'ONLINE':
            mssql = DBUtil.get_mssql_env(dbInfo, db)
            if float(main_version) > 10:
                sql = f"""
                SELECT name AS '文件名', 
                    Physical_Name AS '文件路径', 
                    type_desc AS '文件类型', 
                    State_Desc AS '状态',
                    CASE is_percent_growth
                        WHEN 1
                        THEN N'按百分比'
                        ELSE N'按固定值'
                    END 增长模式,
                    CASE is_percent_growth
                        WHEN 1
                        THEN CONVERT(VARCHAR, growth) + ' %'
                        ELSE CONVERT(VARCHAR, growth / 128) + ' MB'
                    END 增长步长,
                    CASE f.Is_Read_Only
                        WHEN 0
                        THEN N'否'
                        ELSE N'是'
                    END AS '是否只读', 
                    FILEPROPERTY(name, 'spaceused') / 128 [已用空间(M)],
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
                    CASE
                        WHEN growth = 0
                        THEN CONVERT(DECIMAL(18, 2), FILEPROPERTY(name, 'spaceused') * 100.0 / size)
                        WHEN growth != 0
                                AND max_size = -1
                        THEN CONVERT(DECIMAL(18, 2), FILEPROPERTY(name, 'spaceused') / 128 * 100.0 / (available_bytes / 1024 / 1024))
                        ELSE CONVERT(DECIMAL(18, 2), FILEPROPERTY(name, 'spaceused') * 100.0 / max_size)
                    END [占最大大小使用率(%)]
                FROM sys.database_files AS f
                    CROSS APPLY sys.dm_os_volume_stats(DB_ID(), f.file_id);
                """
            else:
                sql = """
                SELECT Name AS '文件名', 
                    Physical_Name AS '文件路径', 
                    type_desc AS '文件类型', 
                    State_Desc AS '状态',
                    CASE is_percent_growth
                        WHEN 1
                        THEN N'按百分比'
                        ELSE N'按固定值'
                    END 增长模式,
                    CASE is_percent_growth
                        WHEN 1
                        THEN CONVERT(VARCHAR, growth) + ' %'
                        ELSE CONVERT(VARCHAR, growth / 128) + ' MB'
                    END 增长步长,
                    CASE f.Is_Read_Only
                        WHEN 0
                        THEN N'否'
                        ELSE N'是'
                    END AS '是否只读', 
                    FILEPROPERTY(name, 'spaceused') / 128 [已用空间(M)],
                    CASE
                        WHEN growth = 0
                                AND max_size != -1
                        THEN CONVERT(VARCHAR, size / 128 - FILEPROPERTY(name, 'spaceused') / 128)
                        WHEN growth != 0
                                AND max_size = -1
                        THEN N'无限制'
                        WHEN growth != 0
                                AND max_size != -1
                        THEN CONVERT(VARCHAR, max_size / 128 - FILEPROPERTY(name, 'spaceused') / 128)
                    END [最大可用空间(M)],
                    CASE
                        WHEN growth = 0
                                AND max_size != -1
                        THEN CONVERT(VARCHAR, CAST((FILEPROPERTY(name, 'SpaceUsed') / (8 * 16.0)) / (size / (8 * 16.0)) * 100.0 AS DECIMAL(12, 2)))
                        WHEN growth != 0
                                AND max_size = -1
                        THEN N'无限制'
                        WHEN growth != 0
                                AND max_size != -1
                        THEN CONVERT(VARCHAR, CAST((FILEPROPERTY(name, 'SpaceUsed') / (8 * 16.0)) / (max_size / (8 * 16.0)) * 100.0 AS DECIMAL(12, 2)))
                    END [使用率(%)]
                FROM sys.database_files AS f;
                """
            result, col_list = mssql.execute(sql)
            if result.code == 0:
                data_col = {}
                n = 0
                for col_name in col_list:
                    n = n + 1
                    if col_name == 'null':
                        col_name = None
                        data_col['c%s' % n] = str(col_name)
                    else:
                        data_col['c%s' % n] = str(col_name)
                if not row_dict2:
                    row_dict2.append(data_col)
                for row in result.msg:
                    data = {}
                    for col in range(len(col_list)):
                        n = col + 1
                        row_re = row[col]
                        if str(row[col]) == 'null':
                            row_re = None
                            data['c%s' % n] = str(row_re)
                        else:
                            data['c%s' % n] = str(row_re)
                    row_dict.append(data)
    # 获取磁盘的使用率
    sql = f"""
    select iname "盘符",'','','','','','','','',round(value::numeric ,2) "使用率(%)" 
    from mon_indexdata where index_id=3000300 
    and record_time > now() - interval '4 h'
    and uid=(select distinct t.uid from mgt_device t,mgt_system s where s.ip=t.in_ip and s.uid='{target_id}'
    and s.use_flag and t.use_flag)
    """
    result2, col_list = pg.execute_col(sql)
    row_dict_pg = []
    if result2.code == 0:
        for row in result2.msg:
            data = {}
            for col2 in range(len(col_list)):
                n = col2 + 1
                row_re = row[col2]
                if str(row[col2]) == 'null':
                    row_re = None
                    data['c%s' % n] = str(row_re)
                else:
                    data['c%s' % n] = str(row_re)
            row_dict_pg.append(data)
    if row_dict2:
        for i in row_dict2:
            row_dict3.append(i)
    if row_dict_pg:
        for h in row_dict_pg:
            row_dict3.append(h)
    for k in row_dict:
        row_dict3.append(k)
    return row_dict3


def db_summary(mssql, row_dict):
    """
    各个数据库概要信息
    :param mssql:
    :return:
    """
    sql = '''
    SELECT name as '数据库名',
       create_date as '创建时间', 
       state_desc as '状态', 
       recovery_model_desc as '恢复模式', 
       case is_read_only when 0 then 'READ_WRITE'
        ELSE 'READ_ONLY' END as '读写状态', 
        collation_name as '排序规则', 
        user_access_desc as '访问模式','null' as "null",'null' as "null",'null' as "null"
FROM sys.databases
'''
    result, col_list = mssql.execute(sql)
    if result.code == 0:
        data_col = {}
        n = 0
        for col_name in col_list:
            n = n + 1
            if col_name == 'null':
                col_name = None
                data_col['c%s' % n] = str(col_name)
            else:
                data_col['c%s' % n] = str(col_name)
        row_dict.append(data_col)
        for row in result.msg:
            data = {}
            for col in range(len(col_list)):
                n = col + 1
                row_re = row[col]
                if str(row[col]) == 'null':
                    row_re = None
                    data['c%s' % n] = str(row_re)
                else:
                    data['c%s' % n] = str(row_re)
            row_dict.append(data)
    return row_dict


def instance_service(mssql, row_dict):
    """
    获取SqlServer实例服务的概要信息,(SQL Server 2008 R2 SP1 or greater)   10.0.2531
    :param mssql:
    :return:
    """

    if float(main_version) > 10:
        sql = """
        SELECT servicename as '服务名', 
               startup_type_desc as '启动类型', 
               status_desc as '状态', 
               process_id as '进程ID', 
               CONVERT(VARCHAR(100), last_startup_time, 120) AS '上次启动时间', 
               service_account as '服务账户', 
               filename as '服务可执行文件', 
               is_clustered as '集群？', 
               cluster_nodename as '集群成员','null' as "null"
        FROM sys.dm_server_services
        """
        result, col_list = mssql.execute(sql)
        if result.code == 0:
            data_col = {}
            n = 0
            for col_name in col_list:
                n = n + 1
                if col_name == 'null':
                    col_name = None
                    data_col['c%s' % n] = str(col_name)
                else:
                    data_col['c%s' % n] = str(col_name)
            row_dict.append(data_col)
            for row in result.msg:
                data = {}
                for col in range(len(col_list)):
                    n = col + 1
                    row_re = row[col]
                    if str(row[col]) == 'null':
                        row_re = None
                        data['c%s' % n] = str(row_re)
                    else:
                        data['c%s' % n] = str(row_re)
                row_dict.append(data)
        return row_dict


def server_registry(mssql, row_dict):
    """
    查看数据文件配置信息
    :return:
    """
    if float(main_version) > 10:
        sql = """
        SELECT 
        registry_key as '注册表KEY', 
        value_name as '参数名', 
        REPLACE(convert(varchar(500),value_data) COLLATE Latin1_General_BIN, CHAR(0), '') as '参数值','null' as "null",'null' as "null",'null' as "null",'null' as "null",'null' as "null",'null' as "null",'null' as "null"
        FROM sys.dm_server_registry WITH (NOLOCK) OPTION (RECOMPILE)
        """
        result, col_list = mssql.execute(sql)
        if result.code == 0:
            data_col = {}
            n = 0
            for col_name in col_list:
                n = n + 1
                if col_name == 'null':
                    col_name = None
                    data_col['c%s' % n] = str(col_name)
                else:
                    data_col['c%s' % n] = str(col_name)
            row_dict.append(data_col)
            for row in result.msg:
                data = {}
                for col in range(len(col_list)):
                    n = col + 1
                    row_re = row[col]
                    if str(row[col]) == 'null':
                        row_re = None
                        data['c%s' % n] = str(row_re)
                    else:
                        data['c%s' % n] = str(row_re)
                row_dict.append(data)


def server_config(mssql, row_dict):
    """
    获取数据库基本参数配置信息
    :param mssql:
    :return:
    """
    sql = """
    SELECT replace(name,' ','_') as '参数名', 
           CONVERT(varchar(50),value_in_use) as '当前值'
    FROM sys.configurations WITH(NOLOCK)
    ORDER BY name OPTION(RECOMPILE)
  """
    result, _ = mssql.execute(sql)
    if result.code == 0:
        for row in result.msg:
            row_dict.append(dict(name=str(row[0]), value=str(row[1])))


def database_size(dbinfo,mssql, row_dict):
    """_summary_database_size 数据库大小

    Args:
        mssql (_type_): mssql 对象
        row_dict (_type_): 返回数据 
    """
    db_list = get_dbname(mssql)
    row_dict.append(dict(c1='数据库名', c2='总大小(MB)', c3='未分配大小(MB)', c4=None, c5=None, c6=None, c7=None, c8=None, c9=None, c10=None))
    for row in db_list:
        db = row[0]
        db_stat = row[1]
        if db_stat == 'ONLINE':
            mssql2 = DBUtil.get_mssql_env(dbinfo,db)
            result, col_list = mssql2.execute('EXEC sp_spaceused')
            if result.code == 0:
                for row in result.msg:
                    db_size = ''.join(row[1].replace('MB','').split())
                    db_unlocate_size = ''.join(row[2].replace('MB','').split())
                    row_dict.append(dict(c1=db, c2=db_size, c3=db_unlocate_size, c4=None, c5=None, c6=None, c7=None, c8=None, c9=None, c10=None))


def server_main(dbInfo, metric):
    """
    获取SqlServer CIB指标总函数
    :param mssql:
    :return:
    """
    row_dict = []
    mssql = DBUtil.get_mssql_env(dbInfo)
    db_version(mssql)
    server_summary(mssql, row_dict)
    server_startup_time(mssql, row_dict)
    server_running_time(mssql, row_dict)
    os_summary(mssql, row_dict)
    manufacturer = os_manufacturer(mssql)
    mode = cpu_mode(mssql)
    if len(manufacturer) != 0:
        Manufacturer = manufacturer[0][2].split("',")[0].split(':')[1].replace("'", '')
    else:
        Manufacturer = ''
    if len(mode) != 0:
        Model = mode[1]
    else:
        Model = ''
    row_dict.append(dict(name='manufacturer', value=Manufacturer))
    row_dict.append(dict(name='cpu_model', value=Model))
    metric.append(dict(index_id="2230001", value=row_dict))
    row_dict2 = []
    db_datafile(dbInfo, row_dict2)
    metric.append(dict(index_id="2230025", content=row_dict2))
    row_dict3 = []
    db_summary(mssql, row_dict3)
    metric.append(dict(index_id="2230007", content=row_dict3))
    row_dict4 = []
    instance_service(mssql, row_dict4)
    metric.append(dict(index_id="2230015", content=row_dict4))
    row_dict5 = []
    server_config(mssql, row_dict5)
    metric.append(dict(index_id="2230014", value=row_dict5))
    row_dict6 = []
    server_registry(mssql, row_dict6)
    metric.append(dict(index_id="2230017", content=row_dict6))
    row_dict7 = []
    database_size(dbInfo,mssql, row_dict7)
    metric.append(dict(index_id="2230018", content=row_dict7))
    return metric


def set_focus(pg, uid):
    sql = "select distinct cib_value from p_oracle_cib c where c.target_id='%s' and index_id=2230001 and cib_name in ('data_file_path','log_file_path')" % uid
    result, _ = pg.execute_col(sql)
    path = ''
    if result.code == 0:
        for row in result.msg:
            if path:
                path += ',' + row[0]
            else:
                path = row[0]
    if not path:
        return
    path += ',C:\\'
    sql = "select cib_value from p_normal_cib where target_id='%s' and index_id=1000001 and cib_name='_focus_path' order by record_time desc limit 1" % uid
    result, _ = pg.execute_col(sql)
    flag = 0
    path_out = ''
    for row in result.msg:
        flag = 1
        path_out = row[0]
    if result.code == 0 and flag == 1:
        if path != path_out:
            sql = "update p_normal_cib set cib_value='%s',record_time=now() where target_id='%s' and index_id=1000001 and cib_name='_focus_path'" % (
                path, uid)
        else:
            sql = None
    else:
        sql = "insert into p_normal_cib(target_id,index_id,cib_name,cib_value,record_time) values('%s',1000001,'_focus_path','%s',now())" % (
            uid, path)
    if not sql:
        return
    pg.execute(sql)


if __name__ == '__main__':
    dbInfo = eval(sys.argv[1])
    target_id, pg = DBUtil.get_pg_env(dbInfo, 0)
    target_ip = dbInfo['target_ip']
    metric = []
    server_main(dbInfo, metric)
    set_focus(pg, target_id)
    print('{"cib":' + json.dumps(metric) + '}')

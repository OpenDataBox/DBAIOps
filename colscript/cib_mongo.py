# Author	= xxxx

import json
import sys
sys.path.append('/usr/software/knowl')
import DBUtil
import CommUtil
import datetime
import warnings
warnings.filterwarnings("ignore")

class DateEncoder(json.JSONEncoder):  
    def default(self, obj):  
        if isinstance(obj, datetime.datetime):  
            return obj.strftime('%Y-%m-%d %H:%M:%S')  
        elif isinstance(obj, date):  
            return obj.strftime("%Y-%m-%d")  
        else:  
            return json.JSONEncoder.default(self, obj) 


def is_sharding(mongo):
    """
    判断是否sharding环境且是mongos
    :return:
    """
    out = mongo.excute('listShards')
    if str(out).find('listShards') == -1:
        return True
    else:
        return False


def mongo_summary(mongo, row_dict, dbinfo):
    """
    测试MongoDB
    =param mongo=
    =param row_dict=
    =return=
    """
    # 数据库服务端信息
    sql = 'serverStatus'
    result = mongo.noitemdict_value(sql)
    out = result.msg
    out_list = dict(out)
    host = out_list['host']
    version = out_list['version']
    process = out_list['process']
    pid = out_list['pid']
    uptime = out_list['uptime']
    db_localtime = str(out_list['localTime'])
    supportsCommittedReads = ''
    readOnly = ''
    persistent = ''
    if 'storageEngine' in out_list.keys():
        storageEngine = out_list['storageEngine']['name']
        if 'supportsCommittedReads' in out_list['storageEngine'].keys():
            supportsCommittedReads = out_list['storageEngine']['supportsCommittedReads']  # 3.2
        if 'readOnly' in out_list['storageEngine'].keys():
            readOnly = out_list['storageEngine']['readOnly']
        if 'persistent' in out_list['storageEngine'].keys():
            persistent = out_list['storageEngine']['persistent']  # 3.2.6
    else:
        storageEngine = 'mongos'
    conn_user = dbinfo['target_usr']
    hostip = dbinfo['target_ip']
    dbport = dbinfo['target_port']
    row_dict.append(dict(name='host', value=host))
    row_dict.append(dict(name='version', value=version))
    row_dict.append(dict(name='process', value=process))
    row_dict.append(dict(name='pid', value=pid))
    row_dict.append(dict(name='uptime', value=uptime))
    row_dict.append(dict(name='local_time', value=db_localtime))
    row_dict.append(dict(name='ip', value=hostip))
    row_dict.append(dict(name='port', value=dbport))
    row_dict.append(dict(name='conn_user', value=conn_user))
    row_dict.append(dict(name='storageEngine', value=storageEngine))
    row_dict.append(dict(name='supportsCommittedReads', value=supportsCommittedReads))
    row_dict.append(dict(name='readOnly', value=readOnly))
    row_dict.append(dict(name='persistent', value=persistent))
    # 通过ssh读取配置文件(/etc/mongo.conf)获取日志、数据文件目录
    # mongo_out = ssh.exec_cmd(f"ps -ef|grep mongo|grep {dbport}|grep dbpath")
    # if len(mongo_out) > 1 and mongo_out.find('--dbpath') != -1:
    #     file_path = mongo_out.split('--dbpath ')[1].split(' ')[0]
    #     log_path = mongo_out.split('--logpath ')[1].split(' ')[0]
    # else:
    #     mongo_out = ssh.exec_cmd("ps -ef|grep mongo|grep '\.conf'|grep -v '\--port'|grep -v '\--dbpath'|grep -v '\--logpath'")
    #     if mongo_out.find('--config') != -1:
    #         config_path = mongo_out.split('--config ')[1].split(' ')[0]
    #     elif mongo_out.find('-f') != -1:
    #         config_path = mongo_out.split('-f ')[1].split(' ')[0]
    #     cmd = f'grep -E "path|Path|pidFilePath" {config_path}'
    #     out = ssh.exec_cmd(cmd)
    #     for i in out.split('\n'):
    #         if i.find('path') != -1 and i.find('.log') != -1:
    #             log_path = i.split(':')[1]
    #         elif i.find('dbPath') != -1:
    #             file_path = i.split(':')[1]
    # row_dict.append(dict(name='LogPath', value=log_path))
    # row_dict.append(dict(name='FilePath', value=file_path))
    # maximum log file size
    logfile_size = ''
    if 'wiredTiger' in out_list.keys():
        logfile_size = out_list['wiredTiger'].get('log').get('maximum log file size')
    row_dict.append(dict(name='max_logfile_size', value=logfile_size))

    # 主机信息
    sql = 'hostInfo'
    host_out = mongo.serverStatus_nodict(sql, 'system')
    os_arch = host_out.msg['cpuAddrSize']
    cpu_arch = host_out.msg['cpuArch']
    mem_size = host_out.msg['memSizeMB']
    cpu_cores = host_out.msg['numCores']
    numa_enabled = host_out.msg['numaEnabled']
    row_dict.append(dict(name='osArch', value=os_arch))
    row_dict.append(dict(name='cpuArch', value=cpu_arch))
    row_dict.append(dict(name='memSizeMB', value=mem_size))
    row_dict.append(dict(name='cpuCores', value=cpu_cores))
    row_dict.append(dict(name='numaEnabled', value=numa_enabled))
    host_out = mongo.serverStatus_nodict(sql, 'os')
    os_type = host_out.msg.get('type')
    os_name = host_out.msg.get('name')
    os_version = host_out.msg.get('version')
    row_dict.append(dict(name='osType', value=os_type))
    row_dict.append(dict(name='osName', value=os_name))
    row_dict.append(dict(name='osVersion', value=os_version))
    host_out = mongo.serverStatus_nodict(sql, 'extra')
    os_kernel = host_out.msg.get('kernelVersion')
    cpu_krequency = host_out.msg.get('cpuFrequencyMHz')
    os_pageSize = host_out.msg.get('pageSize')
    os_pages = host_out.msg.get('numPages')
    os_maxOpenFiles = host_out.msg.get('maxOpenFiles')
    row_dict.append(dict(name='OSkernelVersion', value=os_kernel))
    row_dict.append(dict(name='CpuFrequencyMHz', value=cpu_krequency))
    row_dict.append(dict(name='OSpageSize', value=os_pageSize))
    row_dict.append(dict(name='OSnumPages', value=os_pages))
    row_dict.append(dict(name='OSmaxOpenFiles', value=os_maxOpenFiles))


def mongo_config(mongo, row_dict):
    """
    获取MongoDB 参数
    :param mongo:
    :param row_dict:
    :return:
    """
    para_list = {
        'AlwaysRecordTraffic',
        'KeysRotationIntervalSec',
        'TransactionRecordMinimumLifetimeMinutes',
        'authenticationMechanisms',
        'allowRolesFromX509Certificates',
        'authorizationManagerCacheSize',
        'awsEC2InstanceMetadataUrl',
        'awsECSInstanceMetadataUrl',
        'bgSyncOplogFetcherBatchSize',
        'cachePressureThreshold',
        'checkCachePressurePeriodSeconds',
        'clientCursorMonitorFrequencySecs',
        'clusterAuthMode',
        'connPoolMaxConnsPerHost',
        'connPoolMaxInUseConnsPerHost',
        'connPoolMaxShardedConnsPerHost',
        'connPoolMaxShardedInUseConnsPerHost',
        'connectTimeoutMs',
        'createRollbackDataFiles',
        'cursorTimeoutMillis',
        'diagnosticDataCollectionDirectoryPath',
        'diagnosticDataCollectionDirectorySizeMB',
        'diagnosticDataCollectionEnabled',
        'diagnosticDataCollectionFileSizeMB',
        'diagnosticDataCollectionPeriodMillis',
        'disabledSecureAllocatorDomains',
        'enableFlowControl',
        'enableHybridIndexBuilds',
        'enableIndexBuildCommitQuorum',
        'enableLocalhostAuthBypass',
        'enableTwoPhaseIndexBuild',
        'featureCompatibilityVersion',
        'forceRollbackViaRefetch',
        'globalConnPoolIdleTimeoutMinutes',
        'heapProfilingEnabled',
        'loadRoutingTableOnStartup',
        'localLogicalSessionTimeoutMinutes',
        'localThresholdMs',
        'logLevel',
        'logicalSessionRefreshMillis',
        'maxIndexBuildDrainBatchSize',
        'maxIndexBuildDrainMemoryUsageMegabytes',
        'maxIndexBuildMemoryUsageMegabytes',
        'maxLogSizeKB',
        'maxNumActiveUserIndexBuilds',
        'maxNumberOfTransactionOperationsInSingleOplogEntry',
        'maxSessions',
        'maxSyncSourceLagSecs',
        'maxTransactionLockRequestTimeoutMillis',
        'maxValidateMBperSec',
        'replBatchLimitBytes',
        'replBatchLimitOperations',
        'replElectionTimeoutOffsetLimitFraction',
        'replWriterThreadCount',
        'sslMode',
        'startupAuthSchemaValidation',
        'syncdelay',
        'tlsMode',
        'traceWriteConflictExceptions',
        'transactionLifetimeLimitSeconds',
        'watchdogPeriodSeconds',
        'wiredTigerCursorCacheSize'
    }
    result = mongo.getparameters()
    out = dict(result.msg)
    for para in para_list:
        if para in out.keys():
            value = out.get(para)
            row_dict.append(dict(name=para, value=value))


def mongo_db(mongo, row_dict):
    """
    获取所有数据库及其大小
    :param mongo:
    :param row_dict:
    :return:
    """
    out = is_sharding(mongo)
    out_db = mongo.list_dbname()
    value_dict = []
    if not out:
        para_list = ['db', 'collections', 'views', 'objects', 'dataSize', 'storageSize', 'indexes', 'indexSize', 'fsUsedSize', 'fsTotalSize']
        for db in out_db.msg:
            data = []
            dbstat = mongo.dbstats(db).msg
            for para in para_list:
                if para in dict(dbstat).keys():
                    if para in ('dataSize', 'storageSize', 'indexSize', 'fsUsedSize', 'fsTotalSize'):
                        para_value = round(float(dict(dbstat).get(f'{para}'))/1024/1024,2)  # 单位换算为MB
                    else:
                        para_value = dict(dbstat).get(f'{para}')
                    data.append(para_value)
                else:
                    data.append('')
            value_dict.append(data)
    else:
        para_list = ['db', 'collections', 'views', 'objects', 'dataSize', 'storageSize', 'indexes', 'indexSize', 'fsUsedSize', 'fsTotalSize']
        for db in out_db.msg:
            dbstat = mongo.dbstats(db).msg['raw']
            for key in dict(dbstat).keys():
                host_dict = dict(dbstat)[f'{key}']
                data = []
                for para in para_list:
                    if para in host_dict.keys():
                        if para == 'db':
                            para_value = str(key) + '-' + str(dict(host_dict)[f'{para}'])
                        elif para in ('dataSize', 'storageSize', 'indexSize', 'fsUsedSize', 'fsTotalSize'):
                            para_value = round(float(dict(host_dict).get(f'{para}'))/1024/1024,2)  # 单位换算为MB
                        else:
                            para_value = dict(host_dict).get(f'{para}')
                        data.append(para_value)
                    else:
                        data.append('')
                value_dict.append(data)
    n = 1
    data_col = {}
    key = ['数据库', '集合数', '视图数', '对象数', '数据大小(MB)', '实际存储大小(MB)', '索引数', '索引大小(MB)', '所在文件系统已用(MB)', '所在文件系统总大小(MB)']
    for i in key:
        data_col['c%s' % n] = i
        n = n + 1
    row_dict.append(data_col)
    for i in value_dict:
        m = 1
        data = {}
        for j in i:
            data['c%s' % m] = j
            m = m + 1
        row_dict.append(data)


def mongo_rep(mongo, row_dict):
    """
    查看MongoDB复制集成员信息
    :param mongo:
    :param row_dict:
    :return:
    """
    result = mongo.serverStatus_nodict('replSetGetStatus', 'members')
    if result.code == 0:
        member_list = list(result.msg)
        pingMs = ''
        syncSourceHost = ''
        infoMessage = ''
        configTerm = ''
        value_dict = []
        data = []
        if member_list:
            for i in member_list:
                host = i.get('name')
                health = i.get('health')
                stateStr = i.get('stateStr')
                uptime = i.get('uptime')
                optimeDate = ''
                if 'optimeDate' in i .keys():
                    optimeDate = i['optimeDate']
                if 'electionDate' not in i.keys():
                    electionDate = ''
                else:
                    electionDate = i['electionDate']
                if 'pingMs' not in i.keys():
                    pingMs = ''
                else:
                    pingMs = i['pingMs']
                if 'syncSourceHost' in i.keys():
                    syncSourceHost = i['syncSourceHost']
                if 'infoMessage' in i.keys():
                    infoMessage = i['infoMessage']
                if 'configTerm' in i.keys():
                    configTerm = i['configTerm']
                if health == 1:
                    health = 'UP'
                else:
                    health = 'DOWN'
                data.append(host)
                data.append(health)
                data.append(stateStr)
                data.append(CommUtil.FormatTime(uptime))
                if optimeDate:
                    data.append(optimeDate.strftime('%Y-%m-%d %H:%M:%S'))
                else:
                    data.append('')
                if electionDate:
                    data.append(electionDate.strftime('%Y-%m-%d %H:%M:%S'))
                else:
                    data.append('')
                data.append(pingMs)
                data.append(syncSourceHost)
                data.append(infoMessage)
                data.append(configTerm)
                value_dict.append(data)
                data = []
            n = 1
            data_col = {}
            key = ['节点', '健康状态', '成员状态', '运行时间', '应用日志最新时间', '选取为主节点日期', '主和从的PING时间(MS)', '主节点', '详细信息', '当前Term']
            for i in key:
                data_col['c%s' % n] = i
                n = n + 1
            row_dict.append(data_col)
            for i in value_dict:
                m = 1
                data = {}
                for j in i:
                    data['c%s' % m] = j
                    m = m + 1
                row_dict.append(data)


def mongo_rep_conf(mongo, row_dict):
    """
    查看MongoDB 副本集配置
    :param mongo:
    :param row_dict:
    :return:
    """
    result = mongo.noitemdict_value('replSetGetConfig')
    if result.code == 0:
        member_list = dict(result.msg).get('config').get('members')
        value_dict = []
        for i in member_list:
            data = []
            id = i.get('_id')
            host = i.get('host')
            arbiterOnly = i.get('arbiterOnly')
            buildIndexes = i.get('buildIndexes')
            hidden = i.get('hidden')
            priority = i.get('priority')
            tags = i.get('tags')
            slaveDelay = i.get('slaveDelay')
            votes = i.get('votes')
            data.append(id)
            data.append(host)
            data.append(arbiterOnly)
            data.append(buildIndexes)
            data.append(hidden)
            data.append(priority)
            data.append(tags)
            data.append(slaveDelay)
            data.append(votes)
            data.append('')
            value_dict.append(data)
        n = 1
        data_col = {}
        key = ['ID', '节点', '是否是仲裁节点', '是否允许创建索引', '是否隐藏', '优先级', '标签', '从库延迟(S)', '投票数', '']
        for i in key:
            data_col['c%s' % n] = i
            n = n + 1
        row_dict.append(data_col)
        for i in value_dict:
            m = 1
            data = {}
            for j in i:
                data['c%s' % m] = j
                m = m + 1
            row_dict.append(data)


def mongo_sharding(mongo, row_dict):
    """
    获取sharding状态信息
    :return:
    """
    issh = is_sharding(mongo)
    if issh:
        out = mongo.serverStatus_nodict('getShardMap', 'map')
        sh_dict = out.msg
        value_dict = []
        for key in sh_dict.keys():
            data = []
            map_name = key
            map_host = sh_dict[f'{key}']
            data.append(map_name)
            data.append(map_host)
            data.append('')
            data.append('')
            data.append('')
            data.append('')
            data.append('')
            data.append('')
            data.append('')
            data.append('')
            value_dict.append(data)
        n = 1
        data_col = {}
        key = ['节点类型', '详细配置', '', '', '', '', '', '', '', '']
        for i in key:
            data_col['c%s' % n] = i
            n = n + 1
        row_dict.append(data_col)
        for i in value_dict:
            m = 1
            data = {}
            for j in i:
                data['c%s' % m] = j
                m = m + 1
            row_dict.append(data)


def server_main(dbinfo, metric):
    """
    获取MongoDB cib指标总函数
    =param mssql=
    =return=
    """
    row_dict = []
    mongo = DBUtil.get_mongo_env(dbinfo)
    mongo_summary(mongo, row_dict, dbinfo)
    metric.append(dict(index_id="2110001", value=row_dict))  # 基本信息
    row_dict2 = []
    mongo_config(mongo, row_dict2)
    metric.append(dict(index_id="2110002", value=row_dict2))
    row_dict3 = []
    mongo_db(mongo, row_dict3)
    metric.append(dict(index_id="2110003", content=row_dict3))
    row_dict4 = []
    mongo_rep(mongo, row_dict4)
    if row_dict4:
        metric.append(dict(index_id="2110004", content=row_dict4))
    row_dict5 = []
    mongo_rep_conf(mongo, row_dict5)
    if row_dict5:
        metric.append(dict(index_id="2110005", content=row_dict5))
    row_dict6 = []
    mongo_sharding(mongo, row_dict6)
    if row_dict6:
        metric.append(dict(index_id="2110006", content=row_dict6))


def set_focus(pg, uid):
    sql = "select distinct cib_value from p_oracle_cib c where c.target_id='%s' and index_id=2110001 and cib_name in ('LogPath','FilePath')" % uid
    result, collist = pg.execute_col(sql)
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
    sql = "select cib_value from p_normal_cib where target_id='%s' and index_id=1000001 and cib_name='_focus_path' order by record_time desc limit 1" % uid
    result, collist = pg.execute_col(sql)
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
    metric = []
    mongo = DBUtil.get_mongo_env(dbInfo)
    result = mongo.excute('serverStatus')
    if result.code == 0:
        server_main(dbInfo, metric)
    else:
        metric.append(dict(index_id="2110000", value='连接异常'))
    set_focus(pg, target_id)
    print('{"cib":' + json.dumps(metric, cls=DateEncoder,ensure_ascii=False) + '}')

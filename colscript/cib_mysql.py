# coding=utf-8

import sys

sys.path.append('/usr/software/knowl')

import DBUtil
import CommUtil
import MySQLUtil
import json
import re
import mysql.connector
import psycopg2

import warnings
warnings.filterwarnings("ignore")

target_id = None
version = ""
branch = ""
datadir = ""
ibdir = ""
ibdata = ""
ibtmp = ""
ibtbs = 0
uid = None


CIB_BASIC = set([
    'VERSION',
    'VERSION_COMMENT',
    'COLLATION_SERVER',
    'CHARACTER_SET_SERVER',
    'BASEDIR',
    'DATADIR',
    'HOSTNAME',
    'PORT',
    'SERVER_ID',
    'SERVER_UUID',
    'LOG_ERROR',
    'TMPDIR',
    'SOCKET'
])
CIB_PARAM = set([
    'INNODB_BUFFER_POOL_SIZE',
    'SYNC_BINLOG',
    'BINLOG_FORMAT',
    'INNODB_FLUSH_LOG_AT_TRX_COMMIT',
    'READ_ONLY',
    'LOG_SLAVE_UPDATES',
    'INNODB_IO_CAPACITY',
    'QUERY_CACHE_TYPE',
    'QUERY_CACHE_SIZE',
    'MAX_CONNECTIONS',
    'MAX_CONNECT_ERRORS',
    'WAIT_TIMEOUT',
    'TMP_TABLE_SIZE',
    'SORT_BUFFER_SIZE',
    'MAX_ALLOWED_PACKET',
    'INNODB_LOCK_WAIT_TIMEOUT',
    'KEY_BUFFER_SIZE',
    'READ_BUFFER_SIZE',
    'INNODB_LOG_FILE_SIZE',
    'INNODB_LOG_BUFFER_SIZE',
    'INNODB_FILE_PER_TABLE',
    'PERFORMANCE_SCHEMA',
    'INNODB_PAGE_SIZE',
    'TABLE_DEFINITION_CACHE',
    'TABLE_OPEN_CACHE',
    'TABLE_OPEN_CACHE_INSTANCES',
    'OPEN_FILES_LIMIT',
    'INNODB_OPEN_FILES',
    'THREAD_CACHE_SIZE',
    'HOST_CACHE_SIZE',
    'INNODB_LOG_FILES_IN_GROUP',
    'INNODB_LOG_GROUP_HOME_DIR',
    'INNODB_DATA_FILE_PATH',
    'INNODB_TEMP_DATA_FILE_PATH',
    'INNODB_BUFFER_POOL_FILENAME',
    'INNODB_DATA_HOME_DIR',
    'INNODB_UNDO_TABLESPACES',
    'INNODB_UNDO_DIRECTORY',
    'LOG_BIN',
    'LOG_BIN_BASENAME',
    'LONG_QUERY_TIME',
    'BINLOG_CACHE_SIZE',
    'MAX_HEAP_TABLE_SIZE',
    'KEY_CACHE_BLOCK_SIZE',
    'BINLOG_STMT_CACHE_SIZE',
    'DEFAULT_STORAGE_ENGINE',
    'PERFORMANCE_SCHEMA_HOSTS_SIZE',
    'LOG_WARNINGS',
    'FLUSH_TIME',
    'GENERAL_LOG',
    'LOCK_WAIT_TIMEOUT',
    'SKIP_NAME_RESOLVE',
    'SLOW_QUERY_LOG',
    'INNODB_READ_IO_THREADS',
    'INNODB_WRITE_IO_THREADS',
    'INNODB_PAGE_CLEANERS',
    'INNODB_MAX_DIRTY_PAGES_PCT',
    'INNODB_STATS_PERSISTENT',
    'INNODB_STATS_AUTO_RECALC',
    'INNODB_THREAD_CONCURRENCY',
    'INNODB_BUFFER_POOL_INSTANCES',
    'INNODB_FLUSH_METHOD',
    'INNODB_FLUSH_NEIGHBORS',
    'INNODB_LRU_SCAN_DEPTH',
    'FLUSH_LOG_AT_TRX_COMMIT',
    'CONNECT_TIMEOUT',
    'JOIN_BUFFER_SIZE',
    'READ_RND_BUFFER_SIZE',
    'THREAD_STACK',
    'EXPIRE_LOGS_DAYS'
])


class Result(object):
    # pass
    def __str__(self):
        return "\n".join("{}={}".format(k, getattr(self, k))
                         for k in self.__dict__.keys())


def relate_mysql(db, sql):
    result = Result()
    rs = db.execute(sql)
    if rs.code == 0:
        result.code = rs.code
        result.msg = rs.msg.fetchall()
    else:
        result.code = 1
        result.msg = ''
    return result


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
    except psycopg2.ProgrammingError:
        result.code = 2
        result.msg = "SQL Error"
    except psycopg2.OperationalError:
        result.code = 1
        result.msg = "Connect Error"
    return result


def parseURL(url):
    pattern = r'(\w+):(\w+)([thin:@/]+)([0-9.]+):(\d+)([:/])(\w+)'
    matchObj = re.match(pattern, url, re.I)
    return matchObj.group(2), matchObj.group(4), matchObj.group(5), matchObj.group(7)


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


def get_os_base(ssh,ostype,vals):
    cmd = "uname -n;uname -r;uname -v;uname -s;getconf PAGESIZE"
    result = ssh.exec_cmd(cmd)
    if isinstance(result, tuple):
        raise Exception(result[1])
    node_name, kernel_release, kernel_version, kernel_name, page_size = result.splitlines()
    vals.append(dict(name="node_name", value=node_name))
    vals.append(dict(name="kernel_release", value=kernel_release))
    vals.append(dict(name="kernel_version", value=kernel_version))
    vals.append(dict(name="kernel_name",value= kernel_name))
    vals.append(dict(name="page_size", value=page_size))
    os_version = 'unkown'
    if ostype.lower() in ('redhat','centos'):
        cmd = "cat /etc/redhat-release"
    elif ostype == 'SUSE':
        cmd = "cat /etc/os-release |grep VERSION_ID |awk -F'=' '{print $NF}'"
    result = ssh.exec_cmd(cmd)
    if isinstance(result, tuple):
        cmd = "cat /etc/os-release |grep VERSION_ID |awk -F'=' '{print $NF}'"
        result = ssh.exec_cmd(cmd)
        if isinstance(result, tuple):
            result = 'unkown'
        else:
            os_version = result
    else:
        os_version = result
    vals.append(dict(name="os_version", value=os_version.strip()))
    cmd_mem = "cat /proc/meminfo |grep MemTotal|awk '{print $2}'"
    vres_mem = ssh.exec_cmd(cmd_mem).strip()
    vals.append(dict(name="mem_total", value=vres_mem))
    # cpu
    cmd_cpu = """ cat /proc/cpuinfo| grep "physical id"| sort| uniq| wc -l;cat /proc/cpuinfo| grep "processor"| wc -l;cat /proc/cpuinfo | grep name | cut -f2 -d:| awk 'NR<=1 {print $0}' """
    result2 = ssh.exec_cmd(cmd_cpu)
    cpus,cpu_cores,cup_model = result2.splitlines()
    vals.append(dict(name="cpu_nums", value=cpus))
    vals.append(dict(name="cpu_cores", value=cpu_cores))
    vals.append(dict(name="cpu_model", value=cup_model))

def getTdsqlDir(dbInfo):
    datadir=''
    basedir=''
    tmpdir=''
    logdir=''
    cnfPath=''
    socktPath=''
    ostype, device_id, helper = DBUtil.get_ssh_session(dbInfo)
    port=dbInfo['mysql_port']
    cmd=f"""ps -ef | grep 'mysqld --defaults-file' | grep {port} | grep -v grep"""
    status, res = helper.execCmd(cmd, 1, None, 'ignore')
    if not status and res:
        pid=res.split()[1]
        basedir_cmd = f'ls -lsa /proc/{pid}/exe'
        status0, basedir_res = helper.execCmd(basedir_cmd, 1, None, 'ignore')
        if not status0:
            basedir = basedir_res.split()[-1].split('/bin/mysqld')[0]
        for item in res.split():
            if '--defaults-file' in item:
                cnfPath=item.split('=')[1]
            elif '--socket=' in item:
                socktPath=item.split('=')[1]
        if cnfPath:
            datadir_cmd=f"""cat {cnfPath} | grep datadir |sed -e '/#/d'"""
            tmpdir_cmd=f"""cat {cnfPath} | grep tmpdir |sed -e '/#/d'"""
            logdir_cmd=f"""cat {cnfPath} | grep -E "log-error|log_error" |sed -e '/#/d'"""
            status1, datadir_res = helper.execCmd(datadir_cmd, 1, None, 'ignore')
            status2, tmpdir_res = helper.execCmd(tmpdir_cmd, 1, None, 'ignore')
            status3, logdir_res = helper.execCmd(logdir_cmd, 1, None, 'ignore')
            if datadir_res and not status1:
                datadir=datadir_res.split('=')[1].strip()
            if not status2:
                if not tmpdir_res:
                    tmpdir='/tmp'
                else:
                    tmpdir=tmpdir_res.split('=')[1].strip()
            if logdir_res and not status3:
                logdir=logdir_res.split('=')[1].strip()
        # else:
    res={}
    dir_res=[basedir,datadir,tmpdir,logdir,socktPath]
    dir_name=['basedir','datadir','tmpdir','log_error','socket']
    for i,item in enumerate(dir_res):
        res[dir_name[i]]=dir_res[i]
    return res

def cib1(db, metric,dbInfo):
    global version
    global branch
    global ibdata
    global ibtmp
    global datadir
    sql = 'select @@innodb_version,@@version'
    result = relate_mysql(db, sql)
    version = ''
    if result.code == 0 and len(result.msg) > 0:
        version = result.msg[0][0]
        branch = result.msg[0][1]
    vals = []
    vals2 = []
    if ver_cmp(version, '5.7') >= 0 and branch.find('MariaDB') < 0:
        sql = "select * from performance_schema.global_variables"
    else:
        sql = "select * from information_schema.global_variables"
    result = relate_mysql(db, sql)
    if result.code == 0:
        addr = ""
        for row in result.msg:
            if row[0].upper() in CIB_BASIC:
                vals.append(dict(name=row[0].lower(), value=cs(row[1])))
                vals2.append(dict(name=row[0].lower(), value=cs(row[1])))
                if row[0].upper() == 'HOSTNAME':
                    if addr == "":
                        addr = cs(row[1])
                    else:
                        addr = cs(row[1]) + addr
                elif row[0].upper() == 'PORT':
                    if addr == "":
                        addr = ':' + cs(row[1])
                    else:
                        addr += ':' + cs(row[1])
                elif row[0].upper() == 'DATADIR':
                    datadir = row[1]
            elif row[0].upper() in CIB_PARAM:
                vals2.append(dict(name=row[0].lower(), value=cs(row[1])))
                if row[0].upper() == 'INNODB_DATA_FILE_PATH':
                    ibdata = row[1]
                elif row[0].upper() == 'INNODB_TEMP_DATA_FILE_PATH':
                    ibtmp = row[1]
                elif row[0].upper() == 'INNODB_UNDO_TABLESPACES':
                    if cs(row[1]) != '':
                        ibtbs = int(row[1])
                elif row[0].upper() == 'INNODB_UNDO_DIRECTORY':
                    ibdir = row[1]
        if addr != "":
            vals.append(dict(name="address", value=addr))
    if 'datadir' not in vals:
        dir_dict_res = getTdsqlDir(dbInfo)
        for item in dir_dict_res:
            vals.append(dict(name=item, value=dir_dict_res[item]))

    # print(vals)
    sql = 'show databases'
    result = relate_mysql(db, sql)
    dbs = None
    if result.code == 0:
        for row in result.msg:
            if dbs is None:
                dbs = row[0]
            else:
                dbs += ',' + row[0]
    vals.append(dict(name='databases', value=cs(dbs)))
    is_rds = CommUtil.is_rds_pg(pg,target_id)
    if not is_rds:
        ostype, ssh = DBUtil.getsshinfo_byuid(pg, target_id)
        if ostype.lower() in ['redhat', 'suse', 'centos']:
            get_os_base(ssh,ostype,vals)
    metric.append(dict(index_id="2210001", value=vals))
    metric.append(dict(index_id="2210002", value=vals2))
    sql = 'show slave status'
    result = relate_mysql(db, sql)
    if result.code == 0 and len(result.msg) > 0:
        vals3 = []
        vals3.append(dict(c1='主库地址', c2='主库端口', c3='复制用户', c4='主库ID', c5='主库UUID', c6=None, c7=None, c8=None, c9=None, c10=None))
        for row in result.msg:
            if len(row) > 40:
                vals3.append(dict(c1=cs(row[1]), c2=row[3], c3=cs(row[2]), c4=cs(row[39]), c5=cs(row[40]), c6=None, c7=None, c8=None,c9=None, c10=None))
            else:
                vals3.append(dict(c1=cs(row[1]), c2=row[3], c3=cs(row[2]), c4=cs(row[39]), c5='UNKOWN', c6=None, c7=None, c8=None,c9=None, c10=None))
        metric.append(dict(index_id="2210005", content=vals3))


def getfiles(ts, sstr, arr):
    isize = None
    xsize = None
    ibs = sstr.split(';')
    cnt = 0
    for row in ibs:
        cols = row.split(':')
        if len(cols) > 1:
            t = len(cols[1])
            if cols[1][t - 1].lower() == 'k':
                isize = int(cols[1][0:t - 1]) * 1024
            elif cols[1][t - 1].lower() == 'm':
                isize = int(cols[1][0:t - 1]) * 1024 * 1024
            elif cols[1][t - 1].lower() == 'g':
                isize = int(cols[1][0:t - 1]) * 1024 * 1024 * 1024
            if len(cols) > 2 and cols[2].lower() == 'autoextend':
                if len(cols) > 4:
                    t = len(cols[4])
                    if cols[4][t - 1].lower() == 'k':
                        xsize = int(cols[4][0:t - 1]) * 1024
                    elif cols[4][t - 1].lower() == 'm':
                        xsize = int(cols[4][0:t - 1]) * 1024 * 1024
                    elif cols[4][t - 1].lower() == 'g':
                        xsize = int(cols[4][0:t - 1]) * 1024 * 1024 * 1024
            arr.append(
                dict(c1='InnoDB', c2=datadir + '/' + cols[0], c3=ts, c4=cs(isize), c5=cs(xsize), c6=None, c7=None,
                     c8=None, c9=None, c10=None))
            cnt += 1
    return cnt


def cib2(db, metric):
    global version

    vals = []
    vals2 = []
    if ver_cmp(version, '8.0') >= 0:
        vals.append(dict(c1='引擎', c2='文件名', c3='表空间', c4='初始大小', c5='最大长度', c6=None, c7=None, c8=None, c9=None, c10=None))
        vals2.append(dict(c1='表空间', c2='类型', c3='行格式', c4='页大小',c5=None, c6=None, c7=None, c8=None, c9=None, c10=None))
        t1 = 0
        t2 = 0
        if ibdata:
            t = getfiles('innodb_system', ibdata, vals)
            if t > 0:
                vals2.append(dict(c1='innodb_system', c2='', c3='', c4='', c5=None, c6=None, c7=None, c8=None, c9=None,
                                  c10=None))
                t1 = t
        if ibtmp:
            t = getfiles('innodb_temporary', ibtmp, vals)
            if t > 0:
                vals2.append(
                    dict(c1='innodb_temporary', c2='', c3='', c4='', c5=None, c6=None, c7=None, c8=None, c9=None,
                         c10=None))
                t2 = t
        for i in range(ibtbs):
            fname = ibdir + '/ibundo' + str(i + 1)
            vals.append(
                dict(c1='InnoDB', c2=fname, c3='innodb_undo', c4=cs(10 * 1024 * 1024), c5='', c6=None, c7=None, c8=None,
                     c9=None, c10=None))
        if ibtbs > 0:
            vals2.append(
                dict(c1='innodb_undo', c2='', c3='', c4='', c5=None, c6=None, c7=None, c8=None, c9=None, c10=None))
        sql = "select a.ENGINE,FILE_NAME,a.TABLESPACE_NAME,a.INITIAL_SIZE,a.MAXIMUM_SIZE from information_schema.files a,information_schema.INNODB_TABLESPACES b where a.TABLESPACE_NAME=b.NAME and b.space_type<>'Single'"
        result = relate_mysql(db, sql)
        if result.code == 0 and len(result.msg) > 0:
            for row in result.msg:
                if (t1 > 0 and row[2] == 'innodb_system') or (t2 > 0 and row[2] == 'innodb_temporary'):
                    continue
                vals.append(
                    dict(c1=cs(row[0]), c2=row[1], c3=cs(row[2]), c4=cs(row[3]), c5=cs(row[4]), c6=None, c7=None,
                         c8=None, c9=None, c10=None))
            sql = "select NAME,SPACE_TYPE,ROW_FORMAT,PAGE_SIZE from information_schema.INNODB_SYS_TABLESPACES where SPACE_TYPE<>'Single'"
            result = relate_mysql(db, sql)
            if result.code == 0:
                for row in result.msg:
                    if (t1 > 0 and row[0] == 'innodb_system') or (t2 > 0 and row[0] == 'innodb_temporary'):
                        continue
                    vals2.append(
                        dict(c1=cs(row[0]), c2=row[1], c3=cs(row[2]), c4=cs(row[3]), c5=None, c6=None, c7=None, c8=None,
                             c9=None, c10=None))
    elif ver_cmp(version, '5.7') >= 0:
        vals.append(
            dict(c1='引擎', c2='文件名', c3='表空间', c4='初始大小', c5='最大长度', c6=None, c7=None, c8=None, c9=None, c10=None))
        vals2.append(dict(c1='表空间', c2='类型', c3='行格式', c4='页大小',
                          c5=None, c6=None, c7=None, c8=None, c9=None, c10=None))
        t1 = 0
        t2 = 0
        if ibdata:
            t = getfiles('innodb_system', ibdata, vals)
            if t > 0:
                vals2.append(dict(c1='innodb_system', c2='', c3='', c4='', c5=None, c6=None, c7=None, c8=None, c9=None,
                                  c10=None))
                t1 = t
        if ibtmp:
            t = getfiles('innodb_temporary', ibtmp, vals)
            if t > 0:
                vals2.append(
                    dict(c1='innodb_temporary', c2='', c3='', c4='', c5=None, c6=None, c7=None, c8=None, c9=None,
                         c10=None))
                t2 = t
        for i in range(ibtbs):
            fname = ibdir + '/ibundo' + str(i + 1)
            vals.append(
                dict(c1='InnoDB', c2=fname, c3='innodb_undo', c4=cs(10 * 1024 * 1024), c5='', c6=None, c7=None, c8=None,
                     c9=None, c10=None))
        if ibtbs > 0:
            vals2.append(
                dict(c1='innodb_undo', c2='', c3='', c4='', c5=None, c6=None, c7=None, c8=None, c9=None, c10=None))
        sql = "select ENGINE,FILE_NAME,TABLESPACE_NAME,INITIAL_SIZE,MAXIMUM_SIZE from information_schema.files where TABLESPACE_NAME not like 'innodb_file_per_table_%'"
        result = relate_mysql(db, sql)
        if result.code == 0 and len(result.msg) > 0:
            for row in result.msg:
                if (t1 > 0 and row[2] == 'innodb_system') or (t2 > 0 and row[2] == 'innodb_temporary'):
                    continue
                vals.append(
                    dict(c1=cs(row[0]), c2=row[1], c3=cs(row[2]), c4=cs(row[3]), c5=cs(row[4]), c6=None, c7=None,
                         c8=None, c9=None, c10=None))
            # vals2.append(dict(c1='表空间',c2='文件格式',c3='行格式',c4='页大小',c5=None,c6=None,c7=None,c8=None,c9=None,c10=None))
            # sql = "select NAME,FILE_FORMAT,ROW_FORMAT,PAGE_SIZE from information_schema.INNODB_SYS_TABLESPACES where SPACE_TYPE<>'Single'"
            sql = "select NAME,SPACE_TYPE,ROW_FORMAT,PAGE_SIZE from information_schema.INNODB_SYS_TABLESPACES where SPACE_TYPE<>'Single'"
            result = relate_mysql(db, sql)
            if result.code == 0:
                for row in result.msg:
                    if (t1 > 0 and row[0] == 'innodb_system') or (t2 > 0 and row[0] == 'innodb_temporary'):
                        continue
                    vals2.append(
                        dict(c1=cs(row[0]), c2=row[1], c3=cs(row[2]), c4=cs(row[3]), c5=None, c6=None, c7=None, c8=None,
                             c9=None, c10=None))
    else:
        vals.append(
            dict(c1='引擎', c2='文件名', c3='表空间', c4='初始大小', c5='最大长度', c6=None, c7=None, c8=None, c9=None, c10=None))
        vals2.append(dict(c1='表空间', c2='类型', c3='行格式', c4='页大小',
                          c5=None, c6=None, c7=None, c8=None, c9=None, c10=None))
        if ibdata:
            t = getfiles('innodb_system', ibdata, vals)
            if t > 0:
                vals2.append(dict(c1='innodb_system', c2='', c3='', c4='', c5=None, c6=None, c7=None, c8=None, c9=None,
                                  c10=None))
        if ibtmp:
            t = getfiles('innodb_temporary', ibtmp, vals)
            if t > 0:
                vals2.append(
                    dict(c1='innodb_temporary', c2='', c3='', c4='', c5=None, c6=None, c7=None, c8=None, c9=None,
                         c10=None))
        for i in range(ibtbs):
            fname = ibdir + '/ibundo' + str(i + 1)
            vals.append(
                dict(c1='InnoDB', c2=fname, c3='innodb_undo', c4=cs(10 * 1024 * 1024), c5='', c6=None, c7=None, c8=None,
                     c9=None, c10=None))
        if ibtbs > 0:
            vals2.append(
                dict(c1='innodb_undo', c2='', c3='', c4='', c5=None, c6=None, c7=None, c8=None, c9=None, c10=None))
    if len(vals) > 1:
        metric.append(dict(index_id="2210004", content=vals))
    if len(vals2) > 1:
        metric.append(dict(index_id="2210003", content=vals2))


def cib_ha(dbInfo, db, metric):
    vals = []
    if ver_cmp(version, '8.0') >= 0:
        sql = "select * from performance_schema.replication_group_members"
        result = relate_mysql(db, sql)
        if result.code == 0 and len(result.msg) > 0:
            vals.append(dict(c1='通道', c2='UUID', c3='主机名', c4='端口', c5='状态', c6='角色', c7='版本', c8=None, c9=None, c10=None))
            for row in result.msg:
                vals.append(dict(c1=row[0], c2=row[1], c3=row[2], c4=cs(row[3]), c5=row[4], c6=row[5], c7=row[6], c8=None,c9=None, c10=None))
    if len(vals) > 1:
        metric.append(dict(index_id="2210006", content=vals))


def cib_db(db, metric):
    """获取各个数据库信息

    Args:
        dbInfo ([type]): [description]
        db ([type]): [description]
        metric ([type]): [description]
    """
    vals = []
    flag_v = CommUtil.check_mysql_proc(db)
    if flag_v == 1:
        proc_name = 'monitor_information_proc'
        col_str = '''table_schema ,
            sum(table_rows) ,
            round(sum(data_length / 1024 / 1024 / 1024), 2) as tab_size,
            round(sum(index_length / 1024 / 1024 / 1024), 2) as index_size ,
            round(sum(DATA_LENGTH + INDEX_LENGTH)/ 1024 / 1024 / 1024, 2) as total_size,
            count(*) table_nums'''
        where_str = f'''group by
            table_schema
        order by
            sum(data_length + INDEX_LENGTH) desc'''
        proc_args = (col_str,'tables',where_str)
        result = db.execute_proc(proc_name,proc_args)
    else:
        sql = """
        select
            table_schema ,
            sum(table_rows) ,
            round(sum(data_length / 1024 / 1024 / 1024), 2) as tab_size,
            round(sum(index_length / 1024 / 1024 / 1024), 2) as index_size ,
            round(sum(DATA_LENGTH + INDEX_LENGTH)/ 1024 / 1024 / 1024, 2) as total_size,
            count(*) table_nums
        from
            information_schema.tables
        group by
            table_schema
        order by
            sum(data_length + INDEX_LENGTH) desc
        """
        result = relate_mysql(db, sql)
    if result.code == 0 and len(result.msg) > 0:
        vals.append(dict(c1='数据库名', c2='总数据行', c3='数据大小(GB)', c4='索引大小(GB)', c5='总大小(GB)', c6='表数量', c7=None, c8=None, c9=None, c10=None))
        for row in result.msg:
            vals.append(dict(c1=row[0], c2=cs(row[1]), c3=cs(row[2]), c4=cs(row[3]), c5=cs(
                row[4]), c6=cs(row[5]), c7=None, c8=None, c9=None, c10=None))
    if len(vals) > 1:
        metric.append(dict(index_id="2210007", content=vals))


def cib_table(db, metric):
    """获取TOP 20大小表

    Args:
        db ([type]): [description]
        metric ([type]): [description]
    """
    vals = []
    flag_v = CommUtil.check_mysql_proc(db)
    if flag_v == 1:
        proc_name = 'monitor_information_proc'
        col_str = '''TABLE_SCHEMA ,
            TABLE_NAME ,
            round(data_length / 1024 / 1024 / 1024, 2) data_size_gb,
            round(index_length / 1024 / 1024 / 1024, 2) index_size_gb,
            round((data_length + index_length) / 1024 / 1024 / 1024, 2) total_size,
            round(DATA_FREE*100 /(DATA_LENGTH + INDEX_LENGTH), 2) frag_ratio,
            ENGINE'''
        where_str = f'''order by
            5 desc
        limit 20'''
        proc_args = (col_str,'tables',where_str)
        result = db.execute_proc(proc_name,proc_args)
    else:
        sql = """
        select
            TABLE_SCHEMA ,
            TABLE_NAME ,
            round(data_length / 1024 / 1024 / 1024, 2) data_size_gb,
            round(index_length / 1024 / 1024 / 1024, 2) index_size_gb,
            round((data_length + index_length) / 1024 / 1024 / 1024, 2) total_size,
            round(DATA_FREE*100 /(DATA_LENGTH + INDEX_LENGTH), 2) frag_ratio,
            ENGINE
        from
            information_schema.tables
        order by
            5 desc
        limit 20
        """
        result = relate_mysql(db, sql)
    if result.code == 0 and len(result.msg) > 0:
        vals.append(dict(c1='数据库名', c2='表名', c3='数据大小(GB)', c4='索引大小(GB)', c5='总大小(GB)', c6='碎片率', c7='存储引擎', c8=None, c9=None, c10=None))
        for row in result.msg:
            vals.append(dict(c1=row[0], c2=cs(row[1]), c3=cs(row[2]), c4=cs(row[3]), c5=cs(
                row[4]), c6=cs(row[5]), c7=row[6], c8=None, c9=None, c10=None))
    if len(vals) > 1:
        metric.append(dict(index_id="2210008", content=vals))


def cib_index(db, metric):
    """获取TOP 20 索引大小

    Args:
        b ([type]): [description]
        metric ([type]): [description]
    """
    vals = []
    sql = """
    select
        database_name,
        table_name,
        index_name,
        round((stat_value*@@innodb_page_size)/ 1024 / 1024/ 1024, 2) SizeGB
    from
        mysql.innodb_index_stats iis
    where
        stat_name = 'size'
        and index_name  not in('GEN_CLUST_INDEX','PRIMARY')
        order by 4 desc
    limit 20;
    """
    result = relate_mysql(db, sql)
    if result.code == 0 and len(result.msg) > 0:
        vals.append(dict(c1='数据库名', c2='表名', c3='索引名', c4='索引大小(GB)', c5=None, c6=None, c7=None, c8=None, c9=None, c10=None))
        for row in result.msg:
            vals.append(dict(c1=row[0], c2=cs(row[1]), c3=cs(row[2]), c4=cs(
                row[3]), c5=None, c6=None, c7=None, c8=None, c9=None, c10=None))
    if len(vals) > 1:
        metric.append(dict(index_id="2210009", content=vals))


def set_focus(pg, uid):
    sql = "select distinct cib_value from p_oracle_cib c where c.target_id='%s' and index_id=2210001 and cib_name in ('log_error','socket','datadir','basedir','tmpdir')" % uid
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
    uid = dbInfo['targetId']
    db = None
    try:
        db = MySQLUtil.MySQL(dbInfo['mysql_ip'], dbInfo['mysql_usr'], dbInfo['mysql_pwd'], dbInfo['mysql_port'], dbInfo['mysql_db'])
        metric = []
        cib1(db, metric, dbInfo)
        cib2(db, metric)
        cib_ha(dbInfo, db, metric)
        cib_db(db, metric)
        cib_table(db, metric)
        cib_index(db, metric)
        set_focus(pg, target_id)
        print('{"cib":' + json.dumps(metric) + '}')
    except mysql.connector.Error as e:
        if not db is None:
            db.close()
        metric = []
        metric.append(dict(index_id="2210000", value="连接失败"))
        print('{"cib":' + json.dumps(metric) + '}')

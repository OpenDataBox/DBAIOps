import sys
import json
import dmPython
import warnings

sys.path.append('/usr/software/knowl')
import DBUtil
import os_svc
import CommUtil

warnings.filterwarnings("ignore")

# coding=utf-8

dsc = None
dbv = 8

def fetchOne(db, sql):
    result = db.execute(sql)
    if result.code == 0:
        result.msg = result.msg.fetchone()
    return result

def fetchAll(db, sql):
    result = db.execute(sql)
    if result.code == 0:
        result.msg = result.msg.fetchall()
    return result

def cs(val, dt=False):
    if val is None:
        return ''
    else:
        if dt:
            return val.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return str(val)

def cib_basic(db, metric):
    global dsc

    vals = []
    sql = """
    select 
        name,
        create_time,
        DECODE(arch_mode, 'Y', '归档', 'N', '未归档') arch_mode,
        DECODE( status$,1, '启动',2,'启动,redo完成',3,'mount',4,'打开',5,'挂起',6,'关闭' ) db_status,
        DECODE(role$, 0, '普通', 1, '主库', 2, '备库') role,
        open_count,
        startup_count, 
        CASE to_char(last_startup_time,'YYYY-MM-DD HH24:MI:SS') WHEN '0000-00-00 00:00:00' THEN '1970-01-01 00:00:00' ELSE to_char(last_startup_time,'YYYY-MM-DD HH24:MI:SS') end
    FROM v$database
    """
    cursor = DBUtil.getValue(db, sql)
    rs = cursor.fetchone()
    vals.append(dict(name="db_port", value=cs(db_port)))
    vals.append(dict(name="db_name", value=cs(rs[0])))
    vals.append(dict(name="create_time", value=cs(rs[1])))
    vals.append(dict(name="arch_mode", value=cs(rs[2])))
    vals.append(dict(name="db_status", value=cs(rs[3])))
    vals.append(dict(name="db_role", value=cs(rs[4])))
    vals.append(dict(name="open_count", value=cs(rs[5])))
    vals.append(dict(name="startup_count", value=cs(rs[6])))
    vals.append(dict(name="last_startup_time", value=cs(rs[7])))
    if dbv > '8.0':
        sql = """
        SELECT
            instance_name,
            instance_number,
            host_name,
            svr_version,
            db_version,
            status$,
            mode$,
            dsc_role,
            permanent_magic
        FROM
            v$instance
        """
    else:
        sql = """
        SELECT
            instance_name,
            instance_number,
            host_name,
            svr_version,
            db_version,
            status$,
            mode$,
            '',
            permanent_magic
        FROM
            v$instance
        """
    cursor = DBUtil.getValue(db, sql)
    rs = cursor.fetchone()
    vals.append(dict(name="instance_name", value=cs(rs[0])))
    vals.append(dict(name="instance_number", value=cs(rs[1])))
    vals.append(dict(name="host_name", value=cs(rs[2])))
    vals.append(dict(name="srv_version", value=cs(rs[3])))
    vals.append(dict(name="db_version", value=cs(dbv)))
    vals.append(dict(name="instance_status", value=cs(rs[5])))
    vals.append(dict(name="instance_mode", value=cs(rs[6])))
    vals.append(dict(name="dsc_role", value=cs(rs[7])))
    vals.append(dict(name="permanent_magic", value=cs(rs[8])))
    inst = rs[0]
    dsc = rs[7]
    sql = """
    SELECT
    n_cpu,
    round(total_phy_size / 1024 / 1024 / 1024, 2) mem_total,
    round(free_phy_size / 1024 / 1024 / 1024, 2) mem_free,
    round((total_phy_size-free_phy_size) / total_phy_size * 100,2) mem_pct,
    round(total_vir_size / 1024 / 1024 / 1024, 2) swap_total,
    round(free_vir_size / 1024 / 1024 / 1024, 2) swap_free,
    round((total_vir_size - free_vir_size) /decode(total_vir_size,0,1,total_vir_size) * 100, 2) swap_pct,
    round(cpu_user_rate,2) user_cpu,
    round(cpu_system_rate,2) system_cpu,
    round(cpu_idLE_rate,2) idle_cpu,
    SEND_BYTES_PER_SECOND,
    RECEIVE_BYTES_PER_SECOND,
    SEND_PACKAGES_PER_SECOND,
    RECEIVE_PACKAGES_PER_SECOND
FROM
    v$systeminfo
    """
    cursor = DBUtil.getValue(db, sql)
    rs = cursor.fetchone()
    vals.append(dict(name="cpu_count", value=cs(rs[0])))
    vals.append(dict(name="mem_total", value=cs(rs[1])))
    vals.append(dict(name="swap_total", value=cs(rs[4])))
    arch_sql = "select arch_dest,arch_file_size,ARCH_SPACE_LIMIT from v$dm_arch_ini"
    cs2 = DBUtil.getValue(db, arch_sql)
    rs2 = cs2.fetchone()
    if rs2:
        vals.append(dict(name="arch_dest", value=cs(rs2[0])))
        vals.append(dict(name="arch_file_size", value=cs(rs2[1])))
        vals.append(dict(name="ARCH_SPACE_LIMIT", value=cs(rs2[2])))
    if dbv > '8.0':
        sql = f"select mal_host,mal_port from v$dm_mal_ini where MAL_INST_NAME='{inst}'"
    else:
        sql = f"select ip,mal_port from v$dm_mal_ini where INST_NAME='{inst}'"
    cs2 = DBUtil.getValue(db, sql)
    rs2 = cs2.fetchone()
    if rs2:
        vals.append(dict(name="mal", value=cs(rs2[0]) + ':' + cs(rs2[1]) + '/' + inst))
    sql = "select check_code from v$license"
    cs2 = DBUtil.getValue(db, sql)
    rs2 = cs2.fetchone()
    if rs2:
        vals.append(dict(name="check_code", value=cs(rs2[0])))
    metric.append(dict(index_id="2260001", value=vals))

def cib_parameters(db, metric):
    vals = []
    sql = """
    select name,value from v$parameter 
where isdefault = 0 or name in 
(   'CTL_PATH',
    'CTL_BAK_PATH',
    'CTL_BAK_NUM',
    'BAK_PATH',
    'BAK_POLICY',
    'SYSTEM_PATH',
    'CONFIG_PATH',
    'TEMP_PATH',
    'AUD_PATH',
    'LENGTH_IN_CHAR',
    'GLOBAL_STR_CASE_SENSITIVE',
    'GLOBAL_PAGE_SIZE',
    'GLOBAL_CHARSET',
    'GLOBAL_LOG_PAGE_SIZE',
    'GLOBAL_EXTENT_SIZE',
    'CASE_COMPATIBLE_MODE',
    'CALC_AS_DECIMAL',
    'MAX_OS_MEMORY',
    'MEMORY_POOL',
    'MEMORY_TARGET',
    'MEMORY_EXTENT_SIZE',
    'MEMORY_BAK_POOL',
    'HUGE_BUFFER',
    'BUFFER',
    'BUFFER_POOLS',
    'FAST_POOL_PAGES',
    'FAST_ROLL_PAGES',
    'KEEP', 'RECYCLE',
    'RECYCLE_POOLS',
    'ROLLSEG',
    'ROLLSEG_POOLS',
    'SORT_BUF_SIZE',
    'SORT_BLK_SIZE',
    'SORT_BUF_GLOBAL_SIZE',
    'SORT_FLAG',
    'DICT_BUF_SIZE',
    'HFS_CACHE_SIZE',
    'VM_STACK_SIZE',
    'VM_POOL_SIZE',
    'VM_POOL_TARGET',
    'SESS_POOL_SIZE',
    'SESS_POOL_TARGET',
    'WORKER_THREADS',
    'TASK_THREADS',
    'OPTIMIZER_MODE',
    'MAX_SESSIONS',
    'FILE_TRACE',
    'COMM_TRACE',
    'RLOG_BUF_SIZE',
    'RLOG_POOL_SIZE',
    'TRANSACTIONS',
    'ENABLE_FLASHBACK',
    'UNDO_RETENTION',
    'SVR_LOG',
    'SVR_LOG_FILE_PATH',
    'HUGE_MEMORY_PERCENTAGE',
    'HAGR_BUF_GLOBAL_SIZE','DIRECT_IO')
    """
    cursor = DBUtil.getValue(db, sql)
    rs = cursor.fetchall()
    for row in rs:
        vals.append(dict(name=row[0], value=cs(row[1])))
    metric.append(dict(index_id="2260002", value=vals))

def cib_tablespace(db, metric):
    vals = []
    sql = """
    SELECT
        id,
        name,
        cache,
        DECODE(type$, 1, 'DB', 2, 'TEMP') type,
        DECODE(status$, 0, 'ONLINE', 1, 'OFFLINE', 2, 'RES_OFFLINE', 3, 'CORRUPT') status,
        max_size,
        total_size*sf_get_page_size()/1024/1024 MB,
        file_num
    FROM
        v$tablespace
    """
    cursor = DBUtil.getValue(db, sql)
    rs = cursor.fetchall()
    vals.append(
        dict(c1="ID", c2="表空间名称", c3="缓冲池名称", c4="类型", c5="状态", c6="最大大小MB", c7="总大小MB", c8="文件个数", c9=None, c10=None))
    for row in rs:
        vals.append(dict(c1=cs(row[0]), c2=cs(row[1]), c3=cs(row[2]), c4=cs(row[3]), c5=cs(row[4]), c6=cs(row[5]),
                         c7=cs(row[6]), c8=cs(row[7]), c9=None, c10=None))
    metric.append(dict(index_id="2260003", content=vals))

def cib_tablespace_size(db, metric):
    vals = []
    sql = """
    SELECT TABLESPACE_NAME AS "TABLESPACE NAME 表空间名",
            DECODE(STATUS,
                            0, 'ONLINE',
                            'OFFLINE') AS "STATUS 表空间状态 ",
            TS_TYPE "TS_TYPE 表空间类型",
            TRUNC(TS_TOTAL) AS "TS_MAX_SIZE(IN M) 表空间最大值",
            TRUNC(TS_CURR_TOTAL)AS "TS_CURR_SIZE(IN M) 表空间当前大小",
            TRUNC(TS_TOTAL-USED) AS "FREE (IN M) 总空闲大小",
            TRUNC(TS_CURR_TOTAL-USED) AS "CURR_FREE(IN M) 当前空闲大小",
            TRUNC(USED) AS "USED (IN M) 已使用大小",
            TRUNC(PCT_CURR_USED) AS "PCT.CURR_USED 当前实际使用率",
            TRUNC(PCT_USED) AS "PCT. USED 总使用率"
        FROM ( SELECT DF.NAME AS TABLESPACE_NAME,
                    'PERMANENT' AS TS_TYPE,
                    STATUS$ AS STATUS,
                    MAX_SIZE AS TS_TOTAL,
                    CURR_MAX_SIZE AS TS_CURR_TOTAL,
                    DECODE((MAX_SIZE - USED_SIZE_T),
                                        NULL, 0,
                                        MAX_SIZE - USED_SIZE_T) AS FREE,
                    DECODE((CURR_MAX_SIZE - USED_SIZE_T),
                                        NULL, 0,
                                        CURR_MAX_SIZE - USED_SIZE_T) AS CURR_FREE,
                    DECODE(USED_SIZE_T,
                                        NULL, 0,
                                        USED_SIZE_T) AS USED,
                    DECODE(USED_SIZE_T,
                                        NULL, 0,
                                        ROUND(CAST(USED_SIZE_T / CURR_MAX_SIZE AS DECIMAL) * 100)) AS PCT_CURR_USED,
                    DECODE(USED_SIZE_T,
                                        NULL, 0,
                                        ROUND(CAST(USED_SIZE_T / MAX_SIZE AS DECIMAL) * 100)) AS PCT_USED
                FROM (SELECT A.NAME,
                                A.ID,
                                A.STATUS$,
                                SUM(CAST(B.TOTAL_SIZE - B.FREE_SIZE AS                DECIMAL) * PAGE() / 1024 / 1024) AS USED_SIZE_P,
                                SUM(CASE AUTO_EXTEND WHEN 0 THEN CAST(B.TOTAL_SIZE AS DECIMAL) * PAGE() / 1024 / 1024 WHEN 1 THEN B.MAX_SIZE END) AS MAX_SIZE,
                                SUM(CAST(B.TOTAL_SIZE AS                              DECIMAL) * PAGE() / 1024 / 1024) AS CURR_MAX_SIZE
                        FROM V$DATAFILE B,
                                V$TABLESPACE A
                        WHERE B.GROUP_ID = A.ID AND A.NAME NOT IN ('TEMP',
                                                                    'ROLL')
                    GROUP BY A.NAME,
                                A.ID,
                                A.STATUS$) DF
            LEFT JOIN (SELECT TS_ID,
                                SUM(N_FULL_EXTENT + N_FREE_EXTENT + N_FRAG_EXTENT) * SF_GET_EXTENT_SIZE() * PAGE() / 1024 / 1024 AS USED_SIZE_T
                        FROM V$SEGMENT_INFOS
                    GROUP BY TS_ID) SEG
                    ON SEG.TS_ID = DF.ID
            UNION ALL
            SELECT TABLESPACE_NAME,
                    'UNDO' AS TS_TYPE,
                    STATUS,
                    TS_TOTAL,
                    TOTAL AS TS_CURR_TOTAL,
                    FREE,
                    FREE AS CURR_FREE,
                    (TOTAL - FREE) AS USED,
                    ROUND(CAST((TOTAL - FREE) AS DECIMAL) * 100 / TOTAL) PCT_CURR_USED,
                    ROUND(CAST((TOTAL - FREE) AS DECIMAL) * 100 / TS_TOTAL) PCT_USED
            FROM (SELECT T.NAME TABLESPACE_NAME,
                            T.STATUS$ STATUS,
                            SUM(CAST(FREE_SIZE AS                                 DECIMAL) * PAGE() / 1024 / 1024) AS FREE,
                            SUM(CAST(D.TOTAL_SIZE AS                              DECIMAL) * PAGE() / 1024 / 1024) AS TOTAL,
                            SUM(CASE AUTO_EXTEND WHEN 0 THEN CAST(D.TOTAL_SIZE AS DECIMAL) * PAGE() / 1024 / 1024 WHEN 1 THEN D.MAX_SIZE END) AS TS_TOTAL
                        FROM V$TABLESPACE T,
                            V$DATAFILE D
                    WHERE T.ID = D.GROUP_ID AND T.NAME IN ('ROLL')
                    GROUP BY T.NAME,
                            T.STATUS$)
            UNION ALL
            SELECT TABLESPACE_NAME,
                    'TEMPORARY' AS TS_TYPE,
                    STATUS,
                    TS_TOTAL,
                    TOTAL AS TS_CURR_TOTAL,
                    FREE,
                    FREE AS CURR_FREE,
                    (TOTAL - FREE) USED,
                    ROUND(CAST((TOTAL - FREE) AS DECIMAL) * 100 / TOTAL) PCT_CURR_USED,
                    ROUND(CAST((TOTAL - FREE) AS DECIMAL) * 100 / TS_TOTAL) PCT_USED
            FROM (SELECT T.NAME TABLESPACE_NAME,
                            T.STATUS$ STATUS,
                            CAST(FREE_SIZE AS    DECIMAL) * PAGE() / 1024 / 1024 AS FREE,
                            CAST(D.TOTAL_SIZE AS DECIMAL) * PAGE() / 1024 / 1024 AS TOTAL,
                            CASE (SELECT SYS_VALUE
                                    FROM V$PARAMETER
                                    WHERE NAME = 'TEMP_SPACE_LIMIT') WHEN 0 THEN 99999999 ELSE (SELECT SYS_VALUE
                                                                                                FROM V$PARAMETER
                                                                                                WHERE NAME = 'TEMP_SPACE_LIMIT') END AS TS_TOTAL
                    FROM V$TABLESPACE T,
                            V$DATAFILE D
                    WHERE T.ID = D.GROUP_ID AND T.NAME IN ('TEMP')) )
    ORDER BY TS_TYPE,
            PCT_CURR_USED DESC;
    """
    cursor = DBUtil.getValue(db, sql)
    rs = cursor.fetchall()
    vals.append(dict(c1='表空间名', c2='已使用(MB)', c3='类型', c4='最大大小(MB)', c5='总使用率', c6='总空闲(MB)', c7='当前空闲(MB)', c8='状态',c9='当前大小(MB)', c10='当前使用率'))
    for row in rs:
        vals.append(dict(c1=cs(row[0]), c2=cs(row[7]), c3=cs(row[2]), c4=cs(row[3]), c5=cs(row[9]), c6=cs(row[5]),
                         c7=cs(row[6]), c8=cs(row[1]), c9=cs(row[4]), c10=cs(row[8])))
    metric.append(dict(index_id="2260006", content=vals))

def cib_datafiles(db, metric):
    vals = []
    sql = """
    SELECT
        file_name,
        file_id,
        tablespace_name,
        round(bytes / 1024 / 1024 / 1024, 2) cur_gb,
        status,AUTOEXTENSIBLE,
        round(MAXBYTES / 1024/1024 / 1024,2) max_gb,
        round(user_bytes/1024 / 1024 / 1024, 2) user_GB,
        ONLINE_STATUS
    FROM
        dba_data_files
    """
    cursor = DBUtil.getValue(db, sql)
    rs = cursor.fetchall()
    vals.append(dict(c1="文件名称", c2="文件ID", c3="表空间名称", c4="当前大小GB", c5="可用状态", c6="是否自动扩展", c7="最大大小GB", c8="已使用空间GB",
                     c9="在线状态", c10=None))
    for row in rs:
        vals.append(dict(c1=cs(row[0]), c2=cs(row[1]), c3=cs(row[2]), c4=cs(row[3]), c5=cs(row[4]), c6=cs(row[5]),
                         c7=cs(row[6]), c8=cs(row[7]), c9=cs(row[8]), c10=None))
    metric.append(dict(index_id="2260004", content=vals))

def cib_rlogfile(db, metric):
    vals = []
    sql = """
    SELECT
        file_id,
        path,
        create_time,
        round(rlog_size / 1024 / 1024, 2) mb
    FROM
        v$rlogfile
    """
    cursor = DBUtil.getValue(db, sql)
    rs = cursor.fetchall()
    vals.append(
        dict(c1="文件ID", c2="文件路径", c3="创建时间", c4="文件大小MB", c5=None, c6=None, c7=None, c8=None, c9=None, c10=None))
    for row in rs:
        vals.append(dict(c1=cs(row[0]), c2=cs(row[1]), c3=cs(row[2]), c4=cs(row[3]), c5=None, c6=None, c7=None, c8=None,
                         c9=None, c10=None))
    metric.append(dict(index_id="2260005", content=vals))


def cib_asmgroup(db, metric):
    vals = []
    sql = """
    SELECT GROUP_ID,
        GROUP_NAME,
        N_DISK,
        round(AU_SIZE/1024/1024,2) AU_SIZE_MB,
        TOTAL_FILE_NUM,
        TYPE,
        RBL_STAT,
        RBL_PWR,
        TOTAL_MB,
        FREE_MB
    FROM
        v$ASMGROUP 
    """
    result = db.execute(sql)
    if result.code != 0:
        sql = """
        SELECT GROUP_ID,
            GROUP_NAME,
            N_DISK,
            round(AU_SIZE/1024/1024,2) AU_SIZE_MB,
            TOTAL_FILE_NUM,
            'N/A',
            'N/A',
            'N/A',
            total_size TOTAL_MB,
            free_size FREE_MB
        FROM
            v$ASMGROUP 
        """
        cursor = DBUtil.getValue(db, sql)
        rs = cursor.fetchall()
    else:
        cursor = result.msg
        rs = cursor.fetchall()
    if rs:
        vals.append(dict(c1="磁盘组ID", c2="磁盘组名称", c3="包含磁盘个数", c4="AU大小MB", c5="包含文件个数", c6="副本数", c7="重平衡状态", c8="重平衡并行度", c9="总大小MB", c10="空闲大小MB"))
        for row in rs:
            vals.append(dict(c1=cs(row[0]), c2=cs(row[1]), c3=cs(row[2]), c4=cs(row[3]), c5=cs(row[4]), c6=cs(row[5]), c7=cs(row[6]), c8=cs(row[7]),c9=cs(row[8]), c10=cs(row[9])))
        metric.append(dict(index_id="2260008", content=vals))


def cib_asmdisk(db, metric):
    vals = []
    sql = """
    SELECT GROUP_ID,
        DISK_NAME,
        DISK_PATH,
        SIZE,
        CREATE_TIME,
        MODIFY_TIME,
        FAILGROUP_NAME,
        FREE_MB,
        STATUS,
        is_destroyed
    FROM
        v$ASMDISK 
    """
        
    result = db.execute(sql)
    if result.code != 0:
        sql = """
        SELECT GROUP_ID,
            DISK_NAME,
            DISK_PATH,
            SIZE,
            CREATE_TIME,
            MODIFY_TIME,
            'N/A',
            'N/A',
            'N/A',
            'N/A'
        FROM
            v$ASMDISK 
        """
        cursor = DBUtil.getValue(db, sql)
        rs = cursor.fetchall()
    else:
        cursor = result.msg
        rs = cursor.fetchall()
    if rs:
        vals.append(dict(c1="磁盘组ID", c2="磁盘名称", c3="磁盘路径", c4="大小MB", c5="创建时间", c6="修改时间", c7="故障磁盘组", c8="剩余空间MB", c9="状态", c10="是否损坏"))
        for row in rs:
            vals.append(dict(c1=cs(row[0]), c2=cs(row[1]), c3=cs(row[2]), c4=cs(row[3]), c5=cs(row[4]), c6=cs(row[5]), c7=cs(row[6]), c8=cs(row[7]),c9=cs(row[8]), c10=cs(row[9])))
        metric.append(dict(index_id="2260007", content=vals))


def cib_usersize(db, metric):
    """
    获取各个用户的数据量总大小
    """
    sql = "select owner,round(sum(bytes)/1024/1024,2) AS size_mb from dba_segments GROUP BY owner"
    cursor = DBUtil.getValue(db, sql)
    rs = cursor.fetchall()
    vals = []
    vals.append(
        dict(c1='用户名', c2='总大小_MB', c3=None, c4=None, c5=None, c6=None, c7=None, c8=None, c9=None, c10=None))
    for row in rs:
        vals.append(
            dict(c1=cs(row[0]), c2=cs(row[1]), c3=None, c4=None, c5=None, c6=None, c7=None, c8=None, c9=None, c10=None))
    metric.append(dict(index_id="2260009", content=vals))


def ls_ret(ostype, lines, start, stop, par):
    val = None
    cmd = None
    cnt = 0
    for i in range(start, stop):
        cnt += 1
        line, cmd = os_svc.getOsline(lines[i])
        if not line is None:
            t = line.find("->")
            if t > 0:
                val = line[t + 2:].strip()
        if not cmd is None:
            break
    return val, cmd, start + cnt - 1


def dm_env(conn, db, targetId):
    sql = "select pid from v$process where pname='dmserver' limit 1"
    result = fetchOne(db, sql)
    if result.code == 0 and result.msg:
        pid = result.msg[0]
        ostype, helper, device_id = DBUtil.getsshinfo(conn, targetId)
    else:
        pid = 0
        ostype = None
        helper = None
    if pid and helper:
        cmd = os_svc.os_cmd(ostype, 'ls2', 'ls -l /proc/%d/exe' % (pid))
        kvs = {}
        ret = os_svc.proc(ostype, helper, cmd, kvs, {'ls2': ls_ret})
        val = kvs.get('ls2')
        if val:
            p = val.rfind('/bin/')
            if p > 0:
                home = val[0:p]
                sql = "select cib_name,cib_value from p_normal_cib where target_id='%s' and index_id=1000001 and cib_name='_DM_HOME' limit 1" % (targetId)
                result = fetchOne(conn, sql)
                sql = None
                if result.code == 0 and result.msg:
                    dmhome = result.msg[0]
                    if dmhome != home:
                        sql = "update p_normal_cib set cib_value='%s',record_time=now() where target_id='%s' and index_id=1000001 and cib_name='_DM_HOME'" % (home, targetId)
                else:
                    sql = "insert into p_normal_cib(target_id,index_id,cib_name,cib_value,record_time) values('%s',1000001,'_DM_HOME','%s',now())" % (targetId, home)
                if sql:
                    try:
                        cur = conn.conn.cursor()
                        cur.execute(sql)
                        conn.conn.commit()
                    except dmPython.Error as e:
                        conn.conn.rollback()



def update_subuid(dm, pg, targetId):
    sql = "SELECT check_code FROM v$license"
    cs = DBUtil.getValue(dm, sql)
    rs = cs.fetchone()
    if rs:
        check_code = rs[0]
        sql2 = f"begin;update mgt_system set subuid='{check_code}' where uid='{targetId}';end;commit;"
        DBUtil.getValue(pg, sql2)

if __name__ == '__main__':
    dbInfo = eval(sys.argv[1])
    db_port = dbInfo["ora_port"]
    uid, pg = DBUtil.get_pg_env()
    dm = DBUtil.get_dm_env()
    metric = []
    if dm.conn:
        dbv = CommUtil.get_dm_version(dm)
        cib_basic(dm, metric)
        cib_parameters(dm, metric)
        cib_tablespace(dm, metric)
        cib_datafiles(dm, metric)
        cib_rlogfile(dm, metric)
        cib_tablespace_size(dm,metric)
        cib_usersize(dm, metric)
        dm_env(pg, dm, uid)
        if dsc:
            cib_asmgroup(dm, metric)
            cib_asmdisk(dm, metric)
            update_subuid(dm, pg, uid)
    print('{"cib":' + json.dumps(metric) + '}')

# coding=utf-8

import sys
sys.path.append('/usr/software/knowl')
import DBUtil
import psycopg2
import cx_Oracle as oracle
import decimal
import re
import os
import json
import time, datetime
from datetime import datetime, timedelta
import timeout_decorator
import tags
from JavaRsa import decrypt
import DBAIOps_logger

log = DBAIOps_logger.Logger()

version = ""
cdb = ""
pdb = ""
dbid = 0
root_id = 0
inc = 0
dbname = ""
role = "PRIMARY"
uid = None
target_id = None
arch = None
rac = None
oracle_home = None


class Result(object):
    # pass
    def __str__(self):
        return "\n".join("{}={}".format(k, getattr(self, k))
                         for k in self.__dict__.keys())


def relate_oracle2(db, sql):
    result = Result()
    try:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close()
        msg = []
        for row in rows:
            msg.append(row)
        result.code = 0
        result.msg = msg
    except oracle.DatabaseError as e:
        # print(e)
        result.code = 1
        result.msg = "Execute Error"
    return result


def relate_pg2(conn, sql, nrow=0):
    result = Result()
    try:
        cur = conn.conn.cursor()
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


def getTsUsage(conn, tss):
    sql = "select cib_name,cib_value from p_normal_cib where target_id='%s' and index_id='1000002' and record_time>(now()-interval '36:00:00')" % (
        uid)
    res = relate_pg2(conn, sql)
    if res.code == 0:
        for row in res.msg:
            if row[0] and row[1]:
                tss[row[0]] = row[1].split(',')


def cib_db(conn, db, metric):
    global uid
    if root_id > 0:
        uid = tags.oradb(conn, target_id, dbid, inc, dbname + '_' + pdb, role)
    else:
        uid = tags.oradb(conn, target_id, dbid, inc, dbname, role)
    if uid is None:
        return
    tm = datetime.fromtimestamp(int(time.time())).timetuple()
    mi = int(tm.tm_min / 5)
    ms = tm.tm_min % 5
    if ms > 2:
        sdate = datetime.strptime('%04d-%02d-%02d %02d:%02d:00' % (tm.tm_year, tm.tm_mon, tm.tm_mday, tm.tm_hour, mi*5),
                                  '%Y-%m-%d %H:%M:%S') + timedelta(minutes=5)
    else:
        sdate = datetime.strptime('%04d-%02d-%02d %02d:%02d:00' % (tm.tm_year, tm.tm_mon, tm.tm_mday, tm.tm_hour, mi*5),
                                  '%Y-%m-%d %H:%M:%S')
    bdate = tags.getWindow(conn, uid, sdate, 'DB', 0.02)
    if not bdate is None:
        ct = time.time()
        if cdb == 'YES':
            log.info('start cib2')
            cib2(db, metric)
        log.info('start cib3')
        cib3(db, metric)
        log.info('start cib4')
        cib4(db, metric)
        log.info('start cib5')
        cib5(db, metric)
        log.info('start cib6')
        cib6(db, metric)
        log.info('start cib7')
        cib7(conn, db, metric)
        log.info('start cib8')
        cib8(db, metric)
        log.info('start cib9')
        cib9(db, metric)
        log.info('start asm_diskgroup')
        asm_diskgroup(db, metric)
        log.info('start asm_disk')
        asm_disk(db, metric)
        tags.setDone(conn, uid, sdate, 'DB', '2', int(time.time() - ct))
    else:
        cib3(db, metric, False)
        cib4(db, metric, False)
        cib8(db, metric, False)
        cib9(db, metric, False)


def cib1(conn, db, metric):
    global version
    global cdb
    global pdb
    global dbid
    global root_id
    global inc
    global dbname
    global role
    global arch
    global rac
    global oracle_home

    sql = 'select host_name,instance_name,instance_number,version,parallel,log_count from v$instance i, (select thread#,count(*) log_count from v$log group by thread#) l where i.thread#=l.thread#'
    result = relate_oracle2(db, sql)
    psu = "no patch"
    vals = []
    inst = 1
    rac = 'NO'
    if result.code == 0:
        if len(result.msg) > 0 and int(result.msg[0][3].split('.')[0]) > 12:
            sql = 'select host_name,instance_name,instance_number,version_full,parallel, log_count from v$instance i, (select thread#,count(*) log_count from v$log group by thread#) l where i.thread#=l.thread#'
            result = relate_oracle2(db, sql)
    if result.code == 0:
        for row in result.msg:
            version = row[3]
            vals.append(dict(name="host_name", value=row[0]))
            vals.append(dict(name="instance_name", value=row[1]))
            vals.append(dict(name="instance_number", value=row[2]))
            vals.append(dict(name="version", value=row[3]))
            vals.append(dict(name="parallel", value=row[4]))
            vals.append(dict(name="log_count", value=row[5]))
            inst = row[2]
            rac = row[4]
    if ver_cmp(version, '12') >= 0:
        #sql = "select COMMENTS from dba_registry_history where ACTION in ('APPLY','BOOTSTRAP') and NAMESPACE in('SERVER','DATAPATCH') and nvl(ACTION_TIME,trunc(sysdate-1000))=(select max(nvl(ACTION_TIME,trunc(sysdate-1000))) from dba_registry_history where ACTION in ('APPLY','BOOTSTRAP') and NAMESPACE in ('SERVER','DATAPATCH'))"
        sql = "select COMMENTS from dba_registry_history where COMMENTS not like 'OJVM%' and ACTION in ('APPLY','BOOTSTRAP','RU_APPLY') and NAMESPACE in('SERVER','DATAPATCH') and nvl(ACTION_TIME,trunc(sysdate-1000))=(select max(nvl(ACTION_TIME,trunc(sysdate-1000))) from dba_registry_history where COMMENTS not like 'OJVM%' and ACTION in ('BOOTSTRAP','RU_APPLY') and NAMESPACE in ('SERVER','DATAPATCH'))"
    else:
        sql = "select COMMENTS from dba_registry_history where ACTION='APPLY' and NAMESPACE='SERVER' and BUNDLE_SERIES='PSU' and ACTION_TIME=(select max(ACTION_TIME) from dba_registry_history where ACTION='APPLY' and NAMESPACE='SERVER' and BUNDLE_SERIES='PSU' and ID>0)"
    result = relate_oracle2(db, sql)
    if result.code == 0:
        for row in result.msg:
            psu = row[0]
    if rac == 'YES':
        ic = 1
        sql = "select count(*) from V$CLUSTER_INTERCONNECTS"
        result = relate_oracle2(db, sql)
        if result.code == 0:
            for row in result.msg:
                ic = row[0]
    else:
        ic = 0
    if version != '':
        vals.append(dict(name="psu", value=psu))
        vals.append(dict(name="cluster_interconnects", value=str(ic)))
        vals.append(dict(name="apply_delay", value=str(0)))
    metric.append(dict(index_id="2201001", value=vals))
    vals = []
    if ver_cmp(version, '12') >= 0:
        sql = 'select dbid,name,resetlogs_change#,log_mode,database_role,force_logging,supplemental_log_data_min,DB_UNIQUE_NAME,platform_name,cdb,created,open_mode from v$database'
    else:
        sql = 'select dbid,name,resetlogs_change#,log_mode,database_role,force_logging,supplemental_log_data_min,DB_UNIQUE_NAME,platform_name,\'\',created,open_mode from v$database'
    result = relate_oracle2(db, sql)
    if result.code == 0:
        for row in result.msg:
            cdb = row[9]
            if cdb is None:
                cdb = ""
                pdb = ""
            if cdb == 'YES':
                sql = 'select con_id,dbid,name,create_scn from v$containers order by con_id'
                result2 = relate_oracle2(db, sql)
                if result2.code == 0:
                    for row2 in result2.msg:
                        if row2[0] > 1:
                            dbid = row2[1]
                            inc = row2[3]
                        pdb = row2[2]
                        cid = row2[0]
                        break
                # sql = "select listagg(r.name, ',') within group (order by  r.name) from v$containers r order by con_id"
                sql = "select name from v$containers where CON_ID=sys_context('userenv','con_id')"
                result3 = relate_oracle2(db, sql)
                if result3.code == 0:
                    for row3 in result3.msg:
                        pdbs = row3[0]
            if dbid > 0:
                root_id = row[0]
            else:
                dbid = row[0]
                inc = row[2]
            dbname = row[7]
            role = row[4]
            arch = row[3]
            vals.append(dict(name="dbid", value=dbid))
            vals.append(dict(name="cluster_database", value=rac))
            vals.append(dict(name="db_name", value=row[1]))
            vals.append(dict(name="resetlogs_change", value=inc))
            vals.append(dict(name="log_mode", value=row[3]))
            vals.append(dict(name="database_role", value=row[4]))
            vals.append(dict(name="force_logging", value=row[5]))
            vals.append(dict(name="supplemental_log_data_min", value=row[6]))
            vals.append(dict(name="db_unique_name", value=row[7]))
            vals.append(dict(name="platform_name", value=row[8]))
            vals.append(dict(name="cdb", value=cdb))
            vals.append(dict(name="version", value=version))
            vals.append(dict(name="psu", value=psu))
            vals.append(dict(name="created", value=row[10]))
            vals.append(dict(name="open_mode", value=row[11]))
            if cdb == 'YES':
                vals.append(dict(name="pdb", value=pdbs))
                vals.append(dict(name="cdb_root", value=('%d.%d' % (row[0], row[2]))))
                vals.append(dict(name="pdb_inst", value=('%d.%d.%d.%d' % (row[0], row[2], cid, inst))))
                if row[0] == dbid:
                    vals.append(dict(name="cdb_uid", value=target_id))
                else:
                    s = '%d.%d.1.%d' % (row[0], row[2], inst)
                    sql = "select TARGET_ID from p_oracle_cib where index_id=2201000 and cib_name='pdb_inst' and cib_value='%s'" % (
                        s)
                    result2 = relate_pg2(conn, sql)
                    if result2.code == 0 and len(result2.msg) > 0:
                        vals.append(dict(name="cdb_uid", value=result2.msg[0][0]))
            break
    sql = "select sum(decode(substr(name,1,1),'+',1,0)) ft1,sum(decode(substr(name,1,4),'/dev',1,0)) ft2,count(1) fts from v$datafile"
    result = relate_oracle2(db, sql)
    if result.code == 0:
        for row in result.msg:
            if row[0] == row[2]:
                typ = 'ASM文件'
            elif row[1] == row[2]:
                typ = '裸设备'
            elif (row[0] == 0) and (row[1] == 0):
                typ = '普通文件'
            else:
                typ = '混合'
            vals.append(dict(name="file_type", value=typ))
    sql = "select value from v$nls_parameters where parameter='NLS_CHARACTERSET'"
    result = relate_oracle2(db, sql)
    if result.code == 0:
        for row in result.msg:
            vals.append(dict(name='nls_characterset', value=row[0]))
    # 归档路径
    sql = "SELECT t.DESTINATION FROM V$ARCHIVE_DEST t WHERE t.STATUS = 'VALID' AND t.TARGET = 'PRIMARY'"
    result = relate_oracle2(db, sql)
    arch_path = ''
    if result.code == 0:
        if result.msg:
            arch_path = result.msg[0][0]
            if arch_path == 'USE_DB_RECOVERY_FILE_DEST':
                sql = "SELECT value FROM V$PARAMETER vp WHERE vp.name = 'db_recovery_file_dest'"
                result = relate_oracle2(db, sql)
                if result.code == 0:
                    if result.msg:
                        arch_path = result.msg[0][0]
            else:
                arch_path = arch_path
        else:
            sql = "SELECT value FROM V$PARAMETER vp WHERE vp.name = 'db_recovery_file_dest'"
            result = relate_oracle2(db, sql)
            if result.code == 0:
                if result.msg:
                    arch_path = result.msg[0][0]
        vals.append(dict(name="pathvalue", value=arch_path))
    sql = 'select min(bytes) from v$log'
    result = relate_oracle2(db, sql)
    if result.code == 0:
        if result.msg:
            redo_file_size = result.msg[0][0]
            vals.append(dict(name="redo_size", value=redo_file_size))
    try:
        cs = db.cursor()
        msg = cs.var(oracle.STRING)
        cs.callproc('sys.dbms_system.get_env', ['ORACLE_HOME', msg])
        oracle_home = msg.getvalue()
        vals.append(dict(name="oracle_home", value=oracle_home))
    except:
        oracle_home = ''
    if ver_cmp(version, '12') >= 0:
        l_sql = """SELECT value ||'/alert_'||(SELECT instance_name FROM v$instance)||'.log' FROM "V$DIAG_INFO" WHERE name = 'Diag Trace'"""
    else:
        l_sql = """SELECT value ||'/alert_'||(SELECT instance_name FROM v$instance)||'.log' FROM "V$SYSTEM_PARAMETER" WHERE name = 'background_dump_dest'"""
    result1 = relate_oracle2(db, l_sql)
    if result1.code == 0:
        for row in result1.msg:
            vals.append(dict(name='log_path', value=row[0]))
    if cdb == 'yes':
        sql = "SELECT round(SUM(bytes)/1024/1024/1024,2) FROM cdb_segments"
    else:
        sql = "SELECT round(SUM(bytes)/1024/1024/1024,2) FROM dba_segments"
    result2 = relate_oracle2(db, sql)
    if result2.code == 0:
        for row in result2.msg:
            vals.append(dict(name='database_size', value=row[0]))
    metric.append(dict(index_id="2201000", value=vals))


def cib2(db, metric):
    sql = 'select CON_ID,NAME,round(TOTAL_SIZE/1024/1024/1024,3),BLOCK_SIZE,RECOVERY_STATUS,DBID,CREATE_SCN from v$containers order by CON_ID'
    result = relate_oracle2(db, sql)
    if result.code == 0:
        vals = []
        vals.append(
            dict(c1='编号', c2='名称', c3='总大小(G)', c4='块大小', c5='恢复状态', c6='DBID', c7='创建SCN', c8=None, c9=None, c10=None))
        # vals.append(dict(c1='1',c2='CDB$ROOT',c3='',c4='',c5='',c6=None,c7=None,c8=None,c9=None,c10=None))
        for row in result.msg:
            if row[0] == 1:
                vals.append(dict(c1=cs(row[0]), c2=row[1], c3=cs(row[2]), c4=cs(row[3]), c5=cs(row[4]), c6=cs(row[5]),
                                 c7=cs(inc), c8=None, c9=None, c10=None))
            else:
                vals.append(dict(c1=cs(row[0]), c2=row[1], c3=cs(row[2]), c4=cs(row[3]), c5=cs(row[4]), c6=cs(row[5]),
                                 c7=cs(row[6]), c8=None, c9=None, c10=None))
        metric.append(dict(index_id="2201002", content=vals))
        metric.append(dict(index_id="2201002", uid=uid, content=vals))


def cib3(db, metric, flag=True):
    sql = 'select group#,status,type,member,IS_RECOVERY_DEST_FILE from v$logfile order by group#'
    result = relate_oracle2(db, sql)
    if result.code == 0:
        vals = []
        vals.append(dict(c1='组号', c2='状态', c3='类型', c4='成员', c5='恢复区', c6=None, c7=None, c8=None, c9=None, c10=None))
        for row in result.msg:
            vals.append(
                dict(c1=cs(row[0]), c2=row[1], c3=row[2], c4=row[3], c5=cs(row[4]), c6=None, c7=None, c8=None, c9=None,
                     c10=None))
        metric.append(dict(index_id="2201008", content=vals))
        if flag:
            metric.append(dict(index_id="2201008", uid=uid, content=vals))


def cib4(db, metric, flag=True):
    sql = 'select thread#,group#,sequence#,members,round(bytes/1024/1024),status,archived from v$log order by thread#,group#'
    result = relate_oracle2(db, sql)
    if result.code == 0:
        vals = []
        vals2 = []
        # 初始化变量用于计算新增指标
        log_group_count = 0
        log_file_min_size = float('inf')
        max_members_per_group = 0
        min_members_per_group = float('inf')
        vals.append(dict(c1='线程号', c2='组号', c3='序列号', c4='成员数', c5='文件大小(M)', c6='状态', c7='归档', c8=None, c9=None, c10=None))
        for row in result.msg:
            vals.append(
                dict(c1=cs(row[0]), c2=cs(row[1]), c3=cs(row[2]), c4=cs(row[3]), c5=row[4], c6=row[5], c7=cs(row[6]),c8=None, c9=None, c10=None))
                        # 计算日志组数量
            
            log_group_count += 1
            # 计算日志文件最小大小
            log_file_size = row[4]
            if log_file_size < log_file_min_size:
                log_file_min_size = log_file_size
            
            # 计算每组日志文件的最大个数和最小个数
            members = row[3]
            if members > max_members_per_group:
                max_members_per_group = members
            if members < min_members_per_group:
                min_members_per_group = members
        
        # 添加新增指标到vals中
        vals2.append(dict(name="log_group_count", value=log_group_count))
        vals2.append(dict(name="logfile_minsize", value=log_file_min_size))
        vals2.append(dict(name="max_members_per_group", value=max_members_per_group))
        vals2.append(dict(name="min_members_per_group", value=min_members_per_group))
        metric.append(dict(index_id="2201000", value=vals2))
        
        
        metric.append(dict(index_id="2201003", content=vals))
        if flag:
            metric.append(dict(index_id="2201003", uid=uid, content=vals))


def cib5(db, metric):
    if cdb == 'YES':
        sql = 'select file_name,file_id,tablespace_name,round(bytes/1024/1024,2),status,autoextensible,con_id,round(MAXBYTES/1024/1024,2) from cdb_data_files order by con_id,file_id'
    else:
        sql = 'select file_name,file_id,tablespace_name,round(bytes/1024/1024,2),status,autoextensible,\'\',round(MAXBYTES/1024/1024,2) from dba_data_files order by file_id'
    result = relate_oracle2(db, sql)
    if result.code == 0:
        vals = []
        vals.append(
            dict(c1='文件名', c2='文件编号', c3='表空间名', c4='文件大小(MB)', c5='状态', c6='是否自动扩展', c7='容器ID', c8='最大大小(MB)', c9=None,
                 c10=None))
        for row in result.msg:
            vals.append(
                dict(c1=row[0], c2=cs(row[1]), c3=row[2], c4=cs(row[3]), c5=row[4], c6=row[5], c7=cs(row[6]), c8=row[7],
                     c9=None, c10=None))
        metric.append(dict(index_id="2201004", uid=uid, content=vals))


def cib6(db, metric):
    if cdb == 'YES':
        sql = 'select file_name,file_id,tablespace_name,round(bytes/1024/1024,2),status,autoextensible,con_id,round(MAXBYTES/1024/1024,2) from cdb_temp_files order by con_id,file_id'
    else:
        sql = 'select file_name,file_id,tablespace_name,round(bytes/1024/1024,2),status,autoextensible,\'\',round(MAXBYTES/1024/1024,2) from dba_temp_files order by file_id'
    result = relate_oracle2(db, sql)
    if result.code == 0:
        vals = []
        vals.append(
            dict(c1='文件名', c2='文件编号', c3='表空间名', c4='文件大小(MB)', c5='状态', c6='是否自动扩展', c7='容器ID', c8='最大大小(MB)', c9=None,
                 c10=None))
        for row in result.msg:
            vals.append(
                dict(c1=row[0], c2=cs(row[1]), c3=row[2], c4=cs(row[3]), c5=row[4], c6=row[5], c7=cs(row[6]), c8=row[7],
                     c9=None, c10=None))
        metric.append(dict(index_id="2201005", uid=uid, content=vals))


def cib7(conn, db, metric):
    tss = {}
    if cdb == 'YES':
        sql = 'select tablespace_name,status,contents,extent_management,allocation_type,segment_space_management,bigfile,con_id from cdb_tablespaces order by con_id,tablespace_name'
    else:
        sql = 'select tablespace_name,status,contents,extent_management,allocation_type,segment_space_management,bigfile,null from dba_tablespaces order by tablespace_name'
    result = relate_oracle2(db, sql)
    if result.code == 0:
        vals = []
        vals.append(
            dict(c1='表空间名', c2='状态', c3='类型', c4='空间管理方式', c5='分配类型', c6='段空间管理方式', c7='是否为大文件', c8='容器ID',
                 c9='当前大小(MB)',
                 c10='使用率'))
        for row in result.msg:
            if not row[7] is None:
                ts = tss.get(str(row[7]) + '.' + row[0])
            else:
                ts = tss.get(row[0])
            if ts:
                sz = ts[3]
                pct = ts[0]
            else:
                sz = None
                pct = None
            vals.append(
                dict(c1=row[0], c2=row[1], c3=row[2], c4=row[3], c5=row[4], c6=row[5], c7=cs(row[6]), c8=cs(row[7]),
                     c9=sz, c10=pct))
        metric.append(dict(index_id="2201006", uid=uid, content=vals))


def cib8(db, metric, flag=True):
    sql = 'select name,status,BLOCK_SIZE,FILE_SIZE_BLKS,IS_RECOVERY_DEST_FILE from v$controlfile'
    result = relate_oracle2(db, sql)
    if result.code == 0:
        vals = []
        vals.append(dict(c1='文件名', c2='状态', c3='块大小', c4='块数', c5='恢复区', c6=None, c7=None, c8=None, c9=None, c10=None))
        for row in result.msg:
            vals.append(
                dict(c1=row[0], c2=cs(row[1]), c3=cs(row[2]), c4=cs(row[3]), c5=cs(row[4]), c6=None, c7=None, c8=None,
                     c9=None, c10=None))
        metric.append(dict(index_id="2201007", content=vals))
        if flag:
            metric.append(dict(index_id="2201007", uid=uid, content=vals))


def cib9(db, metric, flag=True):
    sql = "select comp_name,version,status from dba_registry"
    result = relate_oracle2(db, sql)
    if result.code == 0:
        vals = []
        vals.append(dict(c1='组件', c2='版本', c3='状态', c4=None, c5=None, c6=None, c7=None, c8=None, c9=None, c10=None))
        for row in result.msg:
            vals.append(
                dict(c1=row[0], c2=row[1], c3=row[2], c4=None, c5=None, c6=None, c7=None, c8=None, c9=None, c10=None))
        metric.append(dict(index_id="2201009", content=vals))
        if flag:
            metric.append(dict(index_id="2201009", uid=uid, content=vals))


def cib10(db, metric):
    dest = None
    if ver_cmp(version, '12') >= 0:
        sql = "SELECT value FROM V$DIAG_INFO WHERE name = 'Diag Trace'"
        result = relate_oracle2(db, sql)
        if result.code == 0 and len(result.msg) > 0:
            dest = result.msg[0][0]
    where_str = """
(
'processes',
'db_flashback_retention_target',
'recyclebin',
'undo_retention',
'sessions',
'nls_language',
'nls_territory',
'sga_target',
'control_files',
'db_block_size',
'compatible',
'log_archive_dest_1',
'log_archive_dest_2',
'log_archive_dest_state_1',
'log_archive_dest_state_2',
'cluster_database',
'db_create_file_dest',
'db_create_online_log_dest_1',
'db_create_online_log_dest_2',
'db_recovery_file_dest',
'db_recovery_file_dest_size',
'undo_tablespace',
'instance_number',
'ldap_directory_sysauth',
'remote_login_passwordfile',
'db_domain',
'shared_servers',
'remote_listener',
'db_name',
'db_unique_name',
'open_cursors',
'star_transformation_enabled',
'log_buffer',
'cpu_count',
'session_cached_cursors',
'pga_aggregate_target',
'archive_lag_target','memory_target','background_dump_dest','workarea_size_policy','max_shared_servers','shared_server_sesions','parallel_max_servers','shared_pool_size')
    """
    if version.find('10') == 0:
        sql = f'''select name,value from v$system_parameter where isdefault='FALSE' or name in {where_str}'''
    else:
        if cdb == 'YES':
            sql = f"select name,value from v$system_parameter where isdefault='FALSE' or isbasic='TRUE' or name in {where_str} and con_id in (0,sys_context('userenv','con_id'))"
        else:
            sql = f"select name,value from v$system_parameter where isdefault='FALSE' or isbasic='TRUE' or name in {where_str}"
    result = relate_oracle2(db, sql)
    vals = []
    if result.code == 0:
        for row in result.msg:
            if row[0] == 'background_dump_dest' and dest:
                vals.append(dict(name=row[0], value=dest))
            else:
                vals.append(dict(name=row[0], value=cs(row[1])))
    sql_extra = """
    SELECT x.ksppinm NAME, y.ksppstvl VALUE
      FROM SYS.x_$ksppi x, SYS.x_$ksppcv y
     where x.indx = y.indx
       AND x.ksppinm in ('_small_table_threshold','_log_parallelism_dynamic')
    """
    result2 = relate_oracle2(db, sql_extra)
    if result2.code == 0:
        for row in result2.msg:
            vals.append(dict(name=row[0], value=cs(row[1])))
    metric.append(dict(index_id="2201010", value=vals))


def cib11(db, metric):
    sql = "select stat_name,value from v$OSSTAT where stat_name in ('NUM_CPUS','PHYSICAL_MEMORY_BYTES')"
    result = relate_oracle2(db, sql)
    vals = []
    if result.code == 0:
        for row in result.msg:
            if row[0] == 'NUM_CPUS':
                vals.append(dict(name='NUM_CPUS', value=cs(row[1])))
            else:
                mem_size = round(float(row[1]) / 1024 / 1024 / 1024, 2)
                vals.append(dict(name='PHYSICAL_MEMORY_BYTES', value=cs(mem_size) + "GB"))
    if len(vals) > 0:
        metric.append(dict(index_id="2201012", value=vals))


def cib12(db, metric):
    if arch == 'ARCHIVELOG':
        sql = "select dest_id,DESTINATION,binding from v$archive_dest where status='VALID' and target='PRIMARY' order by decode(binding,'MANDATORY',0,1),dest_id"
        result = relate_oracle2(db, sql)
        if result.code == 0:
            vals = []
            vals.append(
                dict(c1='目标id', c2='路径', c3=None, c4=None, c5=None, c6=None, c7=None, c8=None, c9=None, c10=None))
            for row in result.msg:
                if row[2] == 'MANDATORY':
                    vals.append(
                        dict(c1=cs(row[0]), c2=row[1], c3=None, c4=None, c5=None, c6=None, c7=None, c8=None, c9=None,
                             c10=None))
                else:
                    if len(vals) > 1:
                        break
                    else:
                        vals.append(dict(c1=cs(row[0]), c2=row[1], c3=None, c4=None, c5=None, c6=None, c7=None, c8=None,
                                         c9=None, c10=None))
            metric.append(dict(index_id="2201013", content=vals))


def cib2202001(db, metric):
    sql = """select grantee,granted_role,'' as note from dba_role_privs where granted_role='DBA' AND 
grantEE not in ('SYS','SYSTEM','MONITOR','GOLDENGATE')"""
    result = relate_oracle2(db, sql)
    if result.code == 0:
        vals = []
        vals.append(dict(c1='用户名', c2='权限路径', c3='备注', c4=None, c5=None, c6=None, c7=None, c8=None, c9=None, c10=None))
        for row in result.msg:
            vals.append(dict(c1=row[0], c2=row[1], c3=cs(row[2]), c4=None, c5=None, c6=None, c7=None, c8=None, c9=None,
                             c10=None))
        metric.append(dict(index_id="2202001", content=vals))


def cib2202002(db, metric):
    sql = "SELECT NAME,VALUE FROM V$PARAMETER WHERE NAME= 'audit_trail'"
    result = relate_oracle2(db, sql)
    if result.code == 0:
        vals = []
        vals.append(dict(c1='审计类型', c2='值', c3=None, c4=None, c5=None, c6=None, c7=None, c8=None, c9=None, c10=None))
        for row in result.msg:
            vals.append(
                dict(c1=row[0], c2=cs(row[1]), c3=None, c4=None, c5=None, c6=None, c7=None, c8=None, c9=None, c10=None))
        metric.append(dict(index_id="2202002", content=vals))


def cib2202003(db, metric):
    sql = """
select username,account_status,to_char(created,'yyyy-mm-dd hh24:mi:ss') created,profile
  from dba_users
 where account_status = 'OPEN'
   and profile not in
       (select profile from dba_profiles where resource_type = 'PASSWORD')"""

    result = relate_oracle2(db, sql)
    if result.code == 0:
        vals = []
        vals.append(
            dict(c1='用户名', c2='账户状态', c3='创建日期', c4='Profile', c5=None, c6=None, c7=None, c8=None, c9=None, c10=None))
        for row in result.msg:
            vals.append(
                dict(c1=row[0], c2=row[1], c3=row[2], c4=row[3], c5=None, c6=None, c7=None, c8=None, c9=None, c10=None))
        metric.append(dict(index_id="2202003", content=vals))


def cib2202004(conn, db, target_id, metric):
    vals = []
    sql = "select value from v$parameter2 where name = 'user_dump_dest'"
    cmd = ""
    cmd_cnt = ""
    rv = None
    result = relate_oracle2(db, sql)
    if result.code == 0:
        for row in result.msg:
            rv = row[0]
    in_ostype, helper = DBUtil.getsshinfo_byuid(conn, target_id)
    if not helper or in_ostype.lower() == 'windows':
        return
    if in_ostype in ['RedHat', 'SUSE','CentOS']:
        cmd = "\"df -iP " + rv + "|awk '{print \\$5}'|tail -1\""
        cmd_cnt = "\"ls " + rv + "|wc -l\""
    elif in_ostype == "AiX":
        cmd = "\"df -i " + rv + "|awk '{print \\$6}'|tail -1\""
        cmd_cnt = "\"ls " + rv + "|wc -l\""
    elif "HP" in in_ostype:
        cmd = "\"df -i " + rv + "|tail -1|awk '{print \\$1\\$2}'\""
        cmd_cnt = "\"ls " + rv + "|wc -l\""
    status,res_cmd = helper.openCmd(cmd,ef=False)
    if status != 0:
        res_cmd = None
    else:
        res_cmd = res_cmd.strip()
    status,res_cmd_cnt = helper.openCmd(cmd_cnt,ef=False)
    if status != 0:
        res_cmd_cnt = None
    else:
        res_cmd_cnt = res_cmd_cnt.strip()
    vals.append(
        dict(c1='Audit路径', c2='Audit路径下文件个数', c3='Audit路径文件系统inode使用比例', c4='说明', c5=None, c6=None, c7=None, c8=None,
             c9=None, c10=None))
    vals.append(
        dict(c1=rv, c2=res_cmd_cnt, c3=res_cmd, c4=cs(None), c5=None, c6=None, c7=None, c8=None, c9=None, c10=None))
    metric.append(dict(index_id="2202004", content=vals))
    if oracle_home and rac == 'YES':
        cmd = '"LANG=C ORACLE_HOME=' + oracle_home + " " + oracle_home + "/bin/srvctl config nodeapps|grep 'VIP IPv4 Address:'\""
        status,res = helper.openCmd(cmd,ef=False)
        vips = ''
        scanips = ''
        if status == 0 and res:
            lines = res.splitlines()
            for ln in lines:
                t = ln.find('Address:')
                if t > 0:
                    if vips:
                        vips += ',' + ln[t+8:].strip()
                    else:
                        vips = ln[t+8:].strip()
            cmd = '"LANC=C ORACLE_HOME=' + oracle_home + " " + oracle_home + "/bin/srvctl config scan|grep 'IPv4 VIP:'\""
            status,res = helper.openCmd(cmd,ef=False)
        if status == 0 and res:
            lines = res.splitlines()
            for ln in lines:
                t = ln.find('VIP:')
                if t > 0:
                    if scanips:
                        scanips += ',' + ln[t+4:].strip()
                    else:
                        scanips = ln[t+4:].strip()
        if vips or scanips:
            for m in metric:
                if m['index_id'] == "2201001":
                    if vips:
                        m['value'].append(dict(name="vips", value=vips))
                    if scanips:
                        m['value'].append(dict(name="scanips", value=scanips))
                    break


def cib2202005(db, metric):
    sql = """
select owner,table_name objname,'table' ttype,degree from all_tables 
where degree > 1
and  owner in (select username
                   from dba_users
                  where default_tablespace not in ('SYSTEM', 'SYSAUX')
                    and account_status = 'OPEN')
union all                    
select owner,index_name objname,'index' ttype,degree from all_indexes
where degree > 1
and  owner in (select username
                   from dba_users
                  where default_tablespace not in ('SYSTEM', 'SYSAUX')
                    and account_status = 'OPEN')  """

    result = relate_oracle2(db, sql)
    if result.code == 0:
        vals = []
        vals.append(
            dict(c1='属主', c2='对象名称', c3='对象类型', c4='并行度', c5=None, c6=None, c7=None, c8=None, c9=None, c10=None))
        for row in result.msg:
            vals.append(
                dict(c1=row[0], c2=row[1], c3=row[2], c4=row[3], c5=None, c6=None, c7=None, c8=None, c9=None, c10=None))
        metric.append(dict(index_id="2202005", content=vals))


@timeout_decorator.timeout(100)
def cib_seg(db, metric):
    log.info("start cib2202007")
    cib2202007(db, metric)
    log.info("start cib2202008")
    cib2202008(db, metric)
    log.info("start cib2202009")
    cib2202009(db, metric)
    log.info("start cib2202010")
    cib2202010(db, metric)
    log.info("start cib2202011")
    cib2202011(db, metric)
    log.info("start cib_2202013")
    cib_2202013(db, metric)
    

def cib2202007(db, metric):
    sql = """
select b.owner,
       t.name,
       b.table_name,
       (select trunc(sum(bytes / 1024 / 1024))
          from dba_segments a
         where a.segment_name = t.name) indsize,
       (select trunc(sum(bytes / 1024 / 1024))
          from dba_segments a
         where a.segment_name = b.table_name) tabsize,
       trunc(t.del_lf_rows / t.lf_rows * 100) ratio
  from index_stats t, dba_indexes b
 where t.name = b.index_name
"""
    result = relate_oracle2(db, sql)
    if result.code == 0:
        vals = []
        vals.append(
            dict(c1='属主', c2='索引名称', c3='表名', c4='索引大小', c5='表大小', c6='碎片率', c7=None, c8=None, c9=None, c10=None))
        for row in result.msg:
            vals.append(
                dict(c1=row[0], c2=row[1], c3=row[2], c4=row[3], c5=row[4], c6=row[5], c7=None, c8=None, c9=None,
                     c10=None))
        metric.append(dict(index_id="2202007", content=vals))


def cib2202008(db, metric):
    sql = """
    SELECT count(1) cnt, coalesce(trunc(sum(bytes / 1024 / 1024)),0) segsize
        FROM DBA_SEGMENTS
        WHERE TABLESPACE_NAME in
            (select tablespace_name
                from dba_tablespaces
                where contents not in ('TEMPORARY', 'UNDO'))
        AND SEGMENT_TYPE = 'TEMPORARY'
    """
    result = relate_oracle2(db, sql)
    if result.code == 0:
        vals = []
        vals.append(dict(c1='数量', c2='大小', c3=None, c4=None, c5=None, c6=None, c7=None, c8=None, c9=None, c10=None))
        for row in result.msg:
            vals.append(
                dict(c1=row[0], c2=row[1], c3=None, c4=None, c5=None, c6=None, c7=None, c8=None, c9=None, c10=None))
        metric.append(dict(index_id="2202008", content=vals))


def cib2202009(db, metric):
    sql = """
    select a.*, coalesce(b.table_name,a.segment_name) table_name
    from (select owner, segment_name, segment_type, trunc(sum(bytes) / 1024 / 1024) segsize
            from dba_segments
            where tablespace_name in ('SYSTEM', 'SYSAUX')
            and owner not in
                (select username
                    from dba_users
                    where default_tablespace in ('SYSTEM', 'SYSAUX', 'USERS'))
            group by owner, segment_name, segment_type) a
    left join dba_tables b
        on a.segment_name = b.table_name
    and a.owner = b.OWNER
    """
    result = relate_oracle2(db, sql)
    if result.code == 0:
        vals = []
        vals.append(dict(c1='属主', c2='段名', c3='段类型', c4='大小', c5='所属表', c6=None, c7=None, c8=None, c9=None, c10=None))
        for row in result.msg:
            vals.append(dict(c1=row[0], c2=row[1], c3=row[2], c4=row[3], c5=row[4], c6=None, c7=None, c8=None, c9=None,
                             c10=None))
        metric.append(dict(index_id="2202009", content=vals))


def cib2202010(db, metric):
    sql = """
    select owner,segment_name table_name,round(bytes/1024/1024/1024,2) tbsize_gb,tablespace_name
    from dba_segments
    where owner in (select username
                    from dba_users
                    where default_tablespace not in ('SYSTEM', 'SYSAUX')
                        and account_status = 'OPEN')
    and bytes / 1024 / 1024 / 1024 > 10
    and segment_type = 'TABLE'
    and segment_name not in (select table_name from dba_part_tables)
    """
    result = relate_oracle2(db, sql)
    if result.code == 0:
        vals = []
        vals.append(dict(c1='属主', c2='表名', c3='表大小', c4='表空间名', c5=None, c6=None, c7=None, c8=None, c9=None, c10=None))
        for row in result.msg:
            vals.append(
                dict(c1=row[0], c2=row[1], c3=row[2], c4=row[3], c5=None, c6=None, c7=None, c8=None, c9=None, c10=None))
        metric.append(dict(index_id="2202010", content=vals))


def cib2202011(db, metric):
    sql = """
    select owner||'.'||segment_name owner,
        trunc(sum(bytes / 1024 / 1024)) rl,
        round(sum(bytes / 1024 / 1024) /
        (select sum(bytes / 1024 / 1024)
            from dba_data_files
            where tablespace_name = 'SYSAUX'),2) ratio
    from dba_segments
    where tablespace_name = 'SYSAUX'
    group by owner, segment_name
    having sum(bytes / 1024 / 1024) > 4096
    """
    result = relate_oracle2(db, sql)
    if result.code == 0:
        vals = []
        vals.append(dict(c1='使用者', c2='容量', c3='占比', c4=None, c5=None, c6=None, c7=None, c8=None, c9=None, c10=None))
        for row in result.msg:
            vals.append(
                dict(c1=row[0], c2=row[1], c3=row[2], c4=None, c5=None, c6=None, c7=None, c8=None, c9=None, c10=None))
        metric.append(dict(index_id="2202011", content=vals))


def cib_2202013(db, metric):
    """
    获取各个用户的数据量总大小
    """
    if cdb == 'YES':
        sql = """
        SELECT
            vc.name ,
            vc.name || '-' ||owner,
            round(sum(bytes)/ 1024 / 1024, 2) AS size_mb
        FROM
            cdb_segments e,
            V$CONTAINERS vc
        WHERE
            e.CON_ID = vc.CON_ID
        GROUP BY
            vc.NAME,
            owner
        ORDER BY
            3 DESC
        """
    else:
        sql = """
        SELECT
            '' ,
            owner,
            round(sum(bytes)/ 1024 / 1024, 2) AS size_mb
        FROM
            dba_segments
        GROUP BY
            owner
        ORDER BY
            3 DESC
        """
    result = relate_oracle2(db, sql)
    if result.code == 0:
        vals = []
        vals.append(
            dict(c1='CDB', c2='用户名', c3='总大小_MB', c4=None, c5=None, c6=None, c7=None, c8=None, c9=None, c10=None))
        for row in result.msg:
            vals.append(
                dict(c1=row[0], c2=row[1], c3=row[2], c4=None, c5=None, c6=None, c7=None, c8=None, c9=None, c10=None))
        metric.append(dict(index_id="2202013", content=vals))


def dc_control(db):
    sql = "SELECT set_config('idle_in_transaction_session_timeout', '0', false)"
    result = relate_pg2(db, sql)


def set_focus(db, conn, uid):
    try:
        sql = "select distinct cib_value from p_oracle_cib c where c.target_id='%s' and cib_name in ('audit_file_dest','diagnostic_dest') and index_id='2201010'" % uid
        cs = DBUtil.getValue(conn, sql)
        rs = cs.fetchall()
        dir_list = []
        if rs:
            dir_list = [row[0] for row in rs if os.path.abspath(row[0])]
        if not dir_list:
            return
        if oracle_home:
            path = ','.join(dir_list + ['/', '/tmp', oracle_home])
        else:
            path = ','.join(dir_list + ['/', '/tmp'])
        # 增加数据文件路径
        sql = f"""
    select
        p.col1 file_path
    from
        mgt_oradb m,
        mgt_system s,
        p_oracle_cib p
    where
        m.id = s.subuid
        and m.id = p.target_id
        and p.index_id in(2201004,2201005)
        and s.uid = '{uid}'
        and p.col1 != N'文件名'
    """
        cs = DBUtil.getValue(conn, sql)
        rs = cs.fetchall()
        if rs:
            path_list = [os.path.dirname(row[0]) for row in rs if not row[0].startswith('+')]
            path = ','.join(set(path_list))
        sql = "select cib_value from p_normal_cib where target_id='%s' and index_id=1000001 and cib_name='_focus_path' order by record_time desc limit 1" % uid
        cs = DBUtil.getValue(conn, sql)
        rs = cs.fetchall()
        if rs and len(rs) == 1:
            if path != rs[0][0]:
                sql = "update p_normal_cib set cib_value='%s',record_time=now() where target_id='%s' and index_id=1000001 and cib_name='_focus_path'" % (
                    path, uid)
            else:
                sql = None
        else:
            sql = "insert into p_normal_cib(target_id,index_id,cib_name,cib_value,record_time) values('%s',1000001,'_focus_path','%s',now())" % (
                uid, path)
        if not sql:
            return
        try:
            cur = conn.conn.cursor()
            cur.execute(sql)
            conn.conn.commit()
        except psycopg2.ProgrammingError:
            conn.conn.rollback()
    except Exception:
        return


def tspace(pg, targetId, racid):
    sql = f"select record_time from mon_indexdata where uid='{targetId}' and index_id=2180516 limit 1"
    cursor = DBUtil.getValue(pg, sql)
    rs = cursor.fetchone()
    if rs:
        return
    sql = f"select cib_value,record_time from p_normal_cib where target_id='{targetId}' and index_id=1000002 and cib_name='2180516' limit 1"
    cursor = DBUtil.getValue(pg, sql)
    rs = cursor.fetchone()
    if rs:
        uid = rs[0]
        if uid == racid:
            return
    sql = f"select record_time from p_normal_cib where target_id='{racid}' and index_id=1000002 limit 1"
    cursor = DBUtil.getValue(pg, sql)
    rs = cursor.fetchone()
    if rs:
        cur = pg.conn.cursor()
        cur.execute("delete from p_normal_cib where target_id='{targetId}' and index_id=1000002")
        sql = "insert into p_normal_cib(target_id,index_id,cib_name,cib_value,record_time) values('%s',1000002,'%s','%s',now())" % (targetId, '2180516', racid)
        cur.execute(sql)
        pg.conn.commit()


def asm_diskgroup(db, metric):
    """
    获取 ASM 磁盘组信息
    """
    sql = """
    SELECT s.GROUP_NUMBER ,s.NAME ,s.BLOCK_SIZE ,s.STATE ,s."TYPE" ,s.TOTAL_MB ,s.FREE_MB,s.REQUIRED_MIRROR_FREE_MB ,s.OFFLINE_DISKS ,s.VOTING_FILES FROM v$asm_diskgroup_stat s
    """
    result = relate_oracle2(db, sql)
    if result.code == 0:
        vals = []
        vals2 = []
        vals.append(dict(c1='磁盘组号', c2='名称', c3='块大小', c4='状态', c5='冗余级别', c6='总大小(MB)', c7='剩余大小(MB)', c8='RMF(MB)',
                         c9='离线磁盘数', c10='VOTING_FILES'))
        for row in result.msg:
            vals.append(
                dict(c1=cs(row[0]), c2=row[1], c3=cs(row[2]), c4=row[3], c5=row[4], c6=row[5], c7=row[6], c8=row[7],
                     c9=row[8], c10=row[9]))
        metric.append(dict(index_id="2201014", uid=uid, content=vals))


def asm_disk(db, metric):
    """
    获取 ASM 磁盘信息
    """
    sql = """
SELECT t.GROUP_NUMBER ,t.NAME ,t.MODE_STATUS ,t.STATE,t.TOTAL_MB ,t.FREE_MB ,t.FAILGROUP ,t."PATH",t.CREATE_DATE ,t.MOUNT_DATE FROM V$ASM_DISK_STAT t
    """
    result = relate_oracle2(db, sql)
    if result.code == 0:
        vals = []
        vals.append(
            dict(c1='磁盘组号', c2='名称', c3='MODE_STATUS', c4='STATE', c5='总大小(MB)', c6='剩余大小(MB)', c7='故障组', c8='路径',
                 c9='创建日期', c10='挂载日期'))
        for row in result.msg:
            vals.append(
                dict(c1=row[0], c2=row[1], c3=cs(row[2]), c4=cs(row[3]), c5=row[4], c6=row[5], c7=row[6], c8=row[7],
                     c9=cs(row[8]), c10=cs(row[9])))
        metric.append(dict(index_id="2201015", uid=uid, content=vals))

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj,bytes):
            return str(int.from_bytes(obj, byteorder='big', signed=False))
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        else:
            if len(str(type(obj))) >= 41:
                return str(obj)
            else:
                return json.JSONEncoder.default(self,obj)

if __name__ == '__main__':
    dbInfo = eval(sys.argv[1])
    usr = dbInfo['orausr']
    # pwd = dbInfo['orapwd']
    pwd = decrypt(dbInfo['orapwd'])
    host = dbInfo['oraIp']
    port = dbInfo['oraPort']
    target_id, pg = DBUtil.get_pg_env(None, 0)
    bt = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
    et = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if len(str(dbInfo['oraSid'])) > 0:
        tns = oracle.makedsn(host, port, str(dbInfo['oraSid']))
    else:
        tns = oracle.makedsn(host, port, service_name=str(dbInfo['oraServiceName']))
    try:
        db = oracle.connect(usr, pwd, tns)
    except Exception as e:
        print('{"error":' + str(e) + '}')
        sys.exit()
    metric = []
    log.info('start to collect cib data')
    dc_control(pg)
    log.info('start to collect cib1')
    cib1(pg, db, metric)
    log.info('start to collect cib10')
    cib10(db, metric)
    log.info('start to collect cib11')
    cib11(db, metric)
    log.info('start to collect cib12')
    cib12(db, metric)
    log.info('start to collect cib_db')
    cib_db(pg, db, metric)
    log.info('start to collect cib2202001')
    cib2202001(db, metric)
    log.info('start to collect cib2202002')
    cib2202002(db, metric)
    log.info('start to collect cib2202003')
    cib2202003(db, metric)
    log.info('start to collect cib2202004')
    cib2202004(pg, db, target_id, metric)
    cib2202005(db, metric)
    try:
        log.info('start to collect cib_seg')
        cib_seg(db, metric)
    except timeout_decorator.timeout_decorator.TimeoutError:
        pass
    print('{"cib":' + json.dumps(metric,cls=DateEncoder) + '}')
    set_focus(db, pg, target_id)
    tspace(pg, target_id, uid)
    db.close()

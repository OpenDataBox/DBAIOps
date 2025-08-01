import sys
sys.path.append('/usr/software/knowl')
import json
import DBUtil
import sql_pg
from os_svc import getOsline, proc, concat, os_cmd
from CommUtil import is_pg

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

def cib_basic(db, metric, pg_flag):
    vals = []
    if pg_flag not in (2,5,14):
        if pg_flag == 8:
            dbv = '120000'
        elif pg_flag in [4,15,16,9,12] : # opengauss
            dbv = '092000'
        else:
            dbv = db.conn.server_version
            if len(str(dbv)) == 5:
                dbv = '0' + str(dbv)
            else:
                dbv = str(dbv)
        sql2 = "select count(*) from pg_proc where proname = 'list_settings';"
        cs2 = DBUtil.getValue(db, sql2)
        rs2 = cs2.fetchone()
        if rs2 and rs2[0]:
            sql = """
            select name,setting from public.list_settings() where name in ('server_version','server_encoding','lc_collate','port','data_directory',
            'log_destination','log_directory','log_filename','TimeZone','config_file','archive_mode')
            """
        else:
            sql = """
            select name,setting from pg_settings where name in ('server_version','server_encoding','lc_collate','port','data_directory',
            'log_destination','log_directory','log_filename','TimeZone','config_file','archive_mode')
            """
        cursor = DBUtil.getValue(db, sql)
        rs = cursor.fetchall()
        data_dir = ''
        for row in rs:
            if row[0] == 'server_version':
                vals.append(dict(name="version", value=cs(row[1])))
            elif row[0] == 'server_encoding':
                vals.append(dict(name="character_set", value=cs(row[1])))
            elif row[0] == 'lc_collate':
                vals.append(dict(name="collation", value=cs(row[1])))
            elif row[0] == 'port':
                vals.append(dict(name="port", value=cs(row[1])))
            elif row[0] == 'data_directory':
                data_dir = cs(row[1])
                vals.append(dict(name="pgdata", value=cs(row[1])))
                if float(dbv[:2]) >= 10:
                    vals.append(dict(name="wal_directory", value=cs(row[1]) + '/pg_wal'))
                else:
                    vals.append(dict(name="wal_directory", value=cs(row[1]) + '/pg_xlog'))
            elif row[0] == 'log_destination':
                vals.append(dict(name="log_destination", value=cs(row[1])))
            elif row[0] == 'log_directory':
                if row[1].find('/') == -1:
                    log_directory = data_dir + '/' + cs(row[1])
                else:
                    log_directory = cs(row[1])
                vals.append(dict(name="log_directory", value=log_directory))
            elif row[0] == 'log_filename':
                vals.append(dict(name="log_filename", value=cs(row[1])))
            elif row[0] == 'TimeZone':
                vals.append(dict(name="timezone", value=cs(row[1])))
            elif row[0] == 'config_file':
                vals.append(dict(name="config_file", value=cs(row[1])))
            elif row[0] == 'archive_mode':
                vals.append(dict(name="archive_mode", value=cs(row[1])))
        if float(dbv) >= 90200:
            sql = "select proname from pg_proc where proname='kernel_version'"
            cursor = DBUtil.getValue(db, sql)
            proname = cursor.fetchone()
            if proname:
                sql = """
                select timeline_id,system_identifier,kernel_version() from pg_control_checkpoint(),pg_control_system()
                """
            else:
                sql = """
                select timeline_id,system_identifier,version() from pg_control_checkpoint(),pg_control_system()
                """
            cursor = DBUtil.getValue(db, sql)
            rs = cursor.fetchone()
            vals.append(dict(name="timeline", value=cs(rs[0])))
            vals.append(dict(name="systemid", value=cs(rs[1])))
            sql = f"SELECT to_timestamp((({rs[1]}>>32) & (2^32 -1)::bigint));"
            cursor = DBUtil.getValue(db, sql)
            crt_rs = cursor.fetchone()
            vals.append(dict(name="version_comment", value=cs(rs[2])))
            vals.append(dict(name="created_date", value=cs(crt_rs[0])))
            # 数据库角色，主库/从库
        if float(dbv) >= 90000:
            sql = "select pg_is_in_recovery()"
            cursor = DBUtil.getValue(db, sql)
            crt_rs = cursor.fetchone()
            if crt_rs[0]:
                db_role = 'Slave'
            else:
                db_role = 'Master'
            vals.append(dict(name="db_role", value=cs(db_role)))
        if pg_flag in (4, 12, 15, 16,9,12):
            sql_a = "select max(age(datfrozenxid64)) from pg_database"
        else:
            sql_a = "select max(age(datfrozenxid)) from pg_database"
        cursor = DBUtil.getValue(db, sql_a)
        crt_rs = cursor.fetchone()
        if crt_rs and crt_rs[0]:
            db_age = crt_rs[0]
        vals.append(dict(name="db_age", value=cs(db_age)))
    elif pg_flag == 14: # uxdb
        sql2 = "select count(*) from ux_proc where proname = 'list_settings'"
        cs2 = DBUtil.getValue(db, sql2)
        rs2 = cs2.fetchone()
        if rs2 and rs2[0]:
            sql = """
            select name,setting from public.list_settings() where name in ('server_version','server_encoding','lc_collate','port','data_directory',
            'log_destination','log_directory','log_filename','TimeZone','config_file','archive_mode')
            """
        else:
            sql = """
            select name,setting from ux_settings where name in ('server_version','server_encoding','lc_collate','port','data_directory',
            'log_destination','log_directory','log_filename','TimeZone','config_file','archive_mode')
            """
        cursor = DBUtil.getValue(db, sql)
        rs = cursor.fetchall()
        data_dir = ''
        for row in rs:
            if row[0] == 'server_version':
                vals.append(dict(name="version", value=cs(row[1])))
            elif row[0] == 'server_encoding':
                vals.append(dict(name="character_set", value=cs(row[1])))
            elif row[0] == 'lc_collate':
                vals.append(dict(name="collation", value=cs(row[1])))
            elif row[0] == 'port':
                vals.append(dict(name="port", value=cs(row[1])))
            elif row[0] == 'data_directory':
                data_dir = cs(row[1])
                vals.append(dict(name="pgdata", value=cs(row[1])))
                vals.append(dict(name="wal_directory", value=cs(row[1])+'/pg_xlog'))
            elif row[0] == 'log_destination':
                vals.append(dict(name="log_destination", value=cs(row[1])))
            elif row[0] == 'log_directory':
                if row[1].find('/') == -1:
                    log_directory = data_dir + '/' + cs(row[1])
                else:
                    log_directory = cs(row[1])
                vals.append(dict(name="log_directory", value=log_directory))
            elif row[0] == 'log_filename':
                vals.append(dict(name="log_filename", value=cs(row[1])))
            elif row[0] == 'TimeZone':
                vals.append(dict(name="timezone", value=cs(row[1])))
            elif row[0] == 'config_file':
                vals.append(dict(name="config_file", value=cs(row[1])))
            elif row[0] == 'archive_mode':
                vals.append(dict(name="archive_mode", value=cs(row[1])))
        sql = """
        select timeline_id,system_identifier,version() from ux_control_checkpoint(),ux_control_system()
        """
        cursor = DBUtil.getValue(db, sql)
        rs = cursor.fetchone()
        vals.append(dict(name="timeline", value=cs(rs[0])))
        vals.append(dict(name="systemid", value=cs(rs[1])))
        sql = f"SELECT to_timestamp((({rs[1]}>>32) & (2^32 -1)::bigint));"
        cursor = DBUtil.getValue(db, sql)
        crt_rs = cursor.fetchone()
        vals.append(dict(name="version_comment", value=cs(rs[2])))
        vals.append(dict(name="created_date", value=cs(crt_rs[0])))
        # 数据库角色，主库/从库
        sql = "select ux_is_in_recovery()"
        cursor = DBUtil.getValue(db, sql)
        crt_rs = cursor.fetchone()
        if crt_rs[0]:
            db_role = 'Slave'
        else:
            db_role = 'Master'
        vals.append(dict(name="db_role", value=cs(db_role)))
    else:
        sql2 = "select count(*) from sys_proc where proname = 'list_settings'"
        cs2 = DBUtil.getValue(db, sql2)
        rs2 = cs2.fetchone()
        if rs2 and rs2[0]:
            sql = """
            select name,setting from public.list_settings() where name in ('server_version','server_encoding','lc_collate','port','data_directory',
            'log_destination','log_directory','log_filename','TimeZone','config_file','archive_mode')
            """
        else:
            sql = """
            select name,setting from sys_settings where name in ('server_version','server_encoding','lc_collate','port','data_directory',
            'log_destination','log_directory','log_filename','TimeZone','config_file','archive_mode')
            """
        cursor = DBUtil.getValue(db, sql)
        rs = cursor.fetchall()
        data_dir = ''
        for row in rs:
            if row[0] == 'server_version':
                vals.append(dict(name="version", value=cs(row[1])))
            elif row[0] == 'server_encoding':
                vals.append(dict(name="character_set", value=cs(row[1])))
            elif row[0] == 'lc_collate':
                vals.append(dict(name="collation", value=cs(row[1])))
            elif row[0] == 'port':
                vals.append(dict(name="port", value=cs(row[1])))
            elif row[0] == 'data_directory':
                data_dir = cs(row[1])
                vals.append(dict(name="pgdata", value=cs(row[1])))
                vals.append(dict(name="wal_directory", value=cs(row[1])+'/pg_xlog'))
            elif row[0] == 'log_destination':
                vals.append(dict(name="log_destination", value=cs(row[1])))
            elif row[0] == 'log_directory':
                if row[1].find('/') == -1:
                    log_directory = data_dir + '/' + cs(row[1])
                else:
                    log_directory = cs(row[1])
                vals.append(dict(name="log_directory", value=log_directory))
            elif row[0] == 'log_filename':
                vals.append(dict(name="log_filename", value=cs(row[1])))
            elif row[0] == 'TimeZone':
                vals.append(dict(name="timezone", value=cs(row[1])))
            elif row[0] == 'config_file':
                vals.append(dict(name="config_file", value=cs(row[1])))
            elif row[0] == 'archive_mode':
                vals.append(dict(name="archive_mode", value=cs(row[1])))
        sql = """
        select timeline_id,system_identifier,version() from sys_control_checkpoint(),sys_control_system()
        """
        cursor = DBUtil.getValue(db, sql)
        rs = cursor.fetchone()
        vals.append(dict(name="timeline", value=cs(rs[0])))
        vals.append(dict(name="systemid", value=cs(rs[1])))
        sql = f"SELECT to_timestamp((({rs[1]}>>32) & (2^32 -1)::bigint));"
        cursor = DBUtil.getValue(db, sql)
        crt_rs = cursor.fetchone()
        vals.append(dict(name="version_comment", value=cs(rs[2])))
        vals.append(dict(name="created_date", value=cs(crt_rs[0])))
        # 数据库角色，主库/从库
        sql = "select sys_is_in_recovery()"
        cursor = DBUtil.getValue(db, sql)
        crt_rs = cursor.fetchone()
        if crt_rs[0]:
            db_role = 'Slave'
        else:
            db_role = 'Master'
        vals.append(dict(name="db_role", value=cs(db_role)))
    vals.append(dict(name="db_type", value=cs(pg_flag)))
    vals.append(dict(name="host_ip", value=cs(pg_ip)))
    metric.append(dict(index_id="2220001", value=vals))

def cib_parameters(db, metric, pg_flag):
    vals = []
    if pg_flag not in (2,5,14):
        sql2 = "select count(*) from pg_proc where proname = 'list_settings'"
        cs2 = DBUtil.getValue(db, sql2)
        rs2 = cs2.fetchone()
        if rs2 and rs2[0]:
            sql = """
            select name,setting,unit from public.list_settings()
            """
        else:
            sql = """
            select name,setting,unit from pg_settings
            """
    elif pg_flag == 14: # uxdb
        sql2 = "select count(*) from ux_proc where proname = 'list_settings'"
        cs2 = DBUtil.getValue(db, sql2)
        rs2 = cs2.fetchone()
        if rs2 and rs2[0]:
            sql = """
            select name,setting,unit from public.list_settings()
            """
        else:
            sql = """
            select name,setting,unit from ux_settings
            """
    else:
        sql2 = "select count(*) from sys_proc where proname = 'list_settings'"
        cs2 = DBUtil.getValue(db, sql2)
        rs2 = cs2.fetchone()
        if rs2 and rs2[0]:
            sql = """
            select name,setting,unit from public.list_settings()
            """
        else:
            sql = """
            select name,setting,unit from sys_settings
            """
    cursor = DBUtil.getValue(db, sql)
    rs = cursor.fetchall()
    for row in rs:
        name, value, unit = row
        if value and (value.isdigit() or value == '-1'):
            vals.append(dict(name=name, value=cs(sql_pg.standard_units(value, unit))))
        else:
            if not unit or unit == 'None':
                vals.append(dict(name=name, value=cs(value)))
            else:
                vals.append(dict(name=name, value=str(value) + ' ' + str(unit)))
    metric.append(dict(index_id="2220002", value=vals))

def cib_extension(db, metric, pg_flag):
    vals = []
    if pg_flag not in (2,5,14):
        if pg_flag == 8:
            dbv = 120000
        elif pg_flag in [4,15,16,9,12] : # opengauss系列
            dbv = '092000'
        else:
            dbv = db.conn.server_version
        if float(dbv) >= 90100:
            sql = """
            select extname, 
                    nspname, 
                    extversion, 
                    comment
                    from pg_extension a,
                        pg_available_extensions b,
                        pg_namespace c
                    where a.extname = b.name
                    and a.extnamespace = c.oid
            """
            cursor = DBUtil.getValue(db, sql)
            rs = cursor.fetchall()
            vals.append(
                dict(c1="插件名称", c2="名称空间", c3="插件版本", c4='描述', c5=None, c6=None, c7=None, c8=None, c9=None, c10=None))
            for row in rs:
                vals.append(
                    dict(c1=cs(row[0]), c2=cs(row[1]), c3=cs(row[2]), c4=cs(row[3]), c5=None, c6=None, c7=None, c8=None,
                         c9=None, c10=None))
            metric.append(dict(index_id="2220003", content=vals))
    elif pg_flag == 14: # uxdb
        sql = """
        select extname, 
                nspname, 
                extversion, 
                comment
                from ux_extension a,
                    ux_available_extensions b,
                    ux_namespace c
                where a.extname = b.name
                and a.extnamespace = c.oid
        """
        cursor = DBUtil.getValue(db, sql)
        rs = cursor.fetchall()
        vals.append(
            dict(c1="插件名称", c2="名称空间", c3="插件版本", c4='描述', c5=None, c6=None, c7=None, c8=None, c9=None, c10=None))
        for row in rs:
            vals.append(
                dict(c1=cs(row[0]), c2=cs(row[1]), c3=cs(row[2]), c4=cs(row[3]), c5=None, c6=None, c7=None, c8=None,
                     c9=None, c10=None))
        metric.append(dict(index_id="2220003", content=vals))
    else:
        sql = """
        select extname, 
                nspname, 
                extversion, 
                comment
                from sys_extension a,
                    sys_available_extensions b,
                    sys_namespace c
                where a.extname = b.name
                and a.extnamespace = c.oid
        """
        cursor = DBUtil.getValue(db, sql)
        rs = cursor.fetchall()
        vals.append(
            dict(c1="插件名称", c2="名称空间", c3="插件版本", c4='描述', c5=None, c6=None, c7=None, c8=None, c9=None, c10=None))
        for row in rs:
            vals.append(
                dict(c1=cs(row[0]), c2=cs(row[1]), c3=cs(row[2]), c4=cs(row[3]), c5=None, c6=None, c7=None, c8=None,
                     c9=None, c10=None))
        metric.append(dict(index_id="2220003", content=vals))

def cib_db(db, metric, pg_flag):
    vals = []
    if pg_flag not in (2,5,14):
        sql = """
        select datname,
            pg_get_userbyid(datdba),
            t.spcname,
            round(pg_database_size(d.oid)/1024/1024) as size,
            pg_encoding_to_char(encoding),
            datcollate,
            datctype,
            datistemplate,
            datallowconn,
            datconnlimit
        from pg_database d,
            pg_tablespace t
        where d.dattablespace = t.oid
        """
    elif pg_flag == 14: # uxdb
        sql = """
        select datname,
            ux_get_userbyid(datdba),
            t.spcname,
            round(ux_database_size(d.oid)/1024/1024) as size,
            ux_encoding_to_char(encoding),
            datcollate,
            datctype,
            datistemplate,
            datallowconn,
            datconnlimit
        from ux_database d,
            ux_tablespace t
        where d.dattablespace = t.oid
        """
    else:
        sql = """
        select datname,
            sys_get_userbyid(datdba),
            t.spcname,
            round(sys_database_size(d.oid)/1024/1024) as size,
            sys_encoding_to_char(encoding),
            datcollate,
            datctype,
            datistemplate,
            datallowconn,
            datconnlimit
        from sys_database d,
            sys_tablespace t
        where d.dattablespace = t.oid
        """
    cursor = DBUtil.getValue(db, sql)
    rs = cursor.fetchall()
    vals.append(
        dict(c1="数据库名称", c2="属主", c3="表空间名称", c4="数据库大小(MB)", c5="编码", c6="语言符号及其分类编码", c7="比较和排序编码", c8="是否模板",
             c9="是否允许连接",
             c10="连接限制"))
    for row in rs:
        vals.append(dict(c1=cs(row[0]), c2=cs(row[1]), c3=cs(row[2]), c4=cs(row[3]), c5=cs(row[4]), c6=cs(row[5]),
                         c7=cs(row[6]), c8=cs(row[7]), c9=cs(row[8]), c10=cs(row[9])))
    metric.append(dict(index_id="2220004", content=vals))

def cib_tablespace(db, metric, pg_flag):
    vals = []
    if pg_flag not in (2,5,14):
        sql = """
        select
            spcname,
            pg_get_userbyid(spcowner) as owner ,
            pg_tablespace_location(oid) as location,
            pg_size_pretty(pg_tablespace_size(oid)) as dbsize
        from pg_tablespace
        """
    elif pg_flag == 14: # uxdb
        sql = """
        select
            spcname,
            ux_get_userbyid(spcowner) as owner ,
            ux_tablespace_location(oid) as location,
            ux_size_pretty(ux_tablespace_size(oid)) as dbsize
        from ux_tablespace
        """
    else:
        sql = """
        select
            spcname,
            sys_get_userbyid(spcowner) as owner ,
            sys_tablespace_location(oid) as location,
            sys_size_pretty(sys_tablespace_size(oid)) as dbsize
        from sys_tablespace
        where spcname != 'sysaudit'
        """
    cursor = DBUtil.getValue(db, sql)
    rs = cursor.fetchall()
    vals.append(
        dict(c1="表空间名称", c2="属主", c3="表空间路径", c4="表空间大小", c5=None, c6=None, c7=None, c8=None, c9=None, c10=None))
    for row in rs:
        vals.append(
            dict(c1=cs(row[0]), c2=cs(row[1]), c3=cs(row[2]), c4=cs(row[3]), c5=None, c6=None, c7=None, c8=None,
                 c9=None, c10=None))
    metric.append(dict(index_id="2220005", content=vals))

def cib_replication(db, metric, pg_flag):
    vals = []
    if pg_flag not in (2,5,14):
        if pg_flag == 8:
            dbv = 120000
        elif pg_flag in [4,15,16,9,12] : # opengauss
            dbv = '092000'
        else:
            dbv = db.conn.server_version
        if float(dbv) >= 90100:
            sql = """
            select usename,application_name,client_hostname,client_addr,client_port,state,sync_state from pg_stat_replication
            """
        else:
            return
    elif pg_flag == 14: # uxdb
        sql = """
        select usename,application_name,client_hostname,client_addr,client_port,state,sync_state from ux_stat_replication
        """
    else:
        sql = """
        select usename,application_name,client_hostname,client_addr,client_port,state,sync_state from sys_stat_replication
        """
    cursor = DBUtil.getValue(db, sql)
    rs = cursor.fetchall()
    vals.append(
        dict(c1="名称", c2="应用名", c3="客户主机名", c4="客户地址", c5="客户端口", c6="状态", c7="同步状态", c8=None, c9=None, c10=None))
    for row in rs:
        vals.append(
            dict(c1=cs(row[0]), c2=cs(row[1]), c3=cs(row[2]), c4=cs(row[3]), c5=cs(row[4]), c6=cs(row[5]),
                    c7=cs(row[6]), c8=None, c9=None, c10=None))
    metric.append(dict(index_id="2220006", content=vals))

def set_focus(conn, uid):
    sql = "select distinct cib_value from p_oracle_cib c where c.target_id='%s' and index_id=2220001 and cib_name in ('pgdata','log_directory')" % uid
    cs = DBUtil.getValue(conn, sql)
    rs = cs.fetchall()
    path = ''
    if rs:
        for row in rs:
            if row[0].startswith('/'):
                if path:
                    path += ',' + row[0]
                else:
                    path = row[0]
    if not path:
        return
    path += ',/,/tmp'
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
    except Exception as e:
        conn.conn.rollback()

def checkDocker(conn, targetId):
    sql = "select cib_value from p_normal_cib where target_id='%s' and index_id=1000001 and cib_name='docker' limit 1" % (targetId)
    result = fetchOne(conn, sql)
    if result.code == 0 and result.msg:
        dock = result.msg[0]
    else:
        dock = None
    return dock


def ls_ret(ostype, lines, start, stop, par):
    val = None
    cmd = None
    cnt = 0
    for i in range(start, stop):
        cnt += 1
        line, cmd = getOsline(lines[i])
        if not line is None:
            t = line.find("->")
            if t > 0:
                val = line[t + 2:].strip()
        if not cmd is None:
            break
    return val, cmd, start + cnt - 1


def pg_env(conn, db, targetId, pg_flag=0):
    ostype, helper,device_id = DBUtil.getsshinfo(conn, targetId)
    if not helper:
        return
    user = None
    home = None
    ddir = None
    pid = 0
    dock = checkDocker(conn, targetId)
    if dock:
        cmd = os_cmd(ostype, "docker_top", 'docker top %s -o pid|grep -v \\"PID\\"' % dock)
        kvs = {}
        ret = proc(ostype, helper, cmd, kvs)
        pid = kvs.get('docker_top')
    else:
        if pg_flag in (1, 3, 4, 6, 8):
            sql = "select pg_backend_pid()"
        elif pg_flag == 14: # uxdb
            sql = "select ux_backend_pid()"
        else:
            sql = "select sys_backend_pid()"
        result = fetchOne(db, sql)
        if result.code == 0 and result.msg:
            myid = result.msg[0]
            cmd = os_cmd(ostype, 'ps', 'ps -o pid,ppid,user,pcpu,vsz,rssize,state,time,etime,comm --pid %d' % (myid))
            kvs = {}
            ret = proc(ostype, helper, cmd, kvs)
            vals = kvs.get('ps')
            if vals and vals[myid][1]:
                pid = vals[myid][1]
                user = vals[myid][2]
    if pid and (dock or (not dock and user != 'polkitd')):
        cmd = os_cmd(ostype, 'ls2[1]', 'ls -l /proc/%d/exe' % (pid))
        ls = os_cmd(ostype, 'ls2[2]', 'ls -l /proc/%d/cwd' % (pid))
        cmd = concat(cmd, ls)
        kvs = {}
        ret = proc(ostype, helper, cmd, kvs, {'ls2': ls_ret})
        val = kvs.get('ls2_1')
        if val:
            p = val.rfind('/bin/')
            if p > 0:
                home = val[0:p]
        ddir = kvs.get('ls2_2')
        if not (ddir and home):
            return
        pghome = None
        pguser = None
        pgddir = None
        sql = "select cib_name,cib_value from p_normal_cib where target_id='%s' and index_id=1000001 and cib_name in ('pghome','pguser','pgdata')" % (targetId)
        result = fetchAll(conn, sql)
        if result.code == 0:
            for row in result.msg:
                if row[0] == 'pghome':
                    pghome = row[1]
                    if pghome is None:
                        pghome = ''
                elif row[0] == 'pguser':
                    pguser = row[1]
                    if pguser is None:
                        pguser = ''
                else:
                    pgddir = row[1]
                    if pgddir is None:
                        pgddir = ''
        try:
            if pghome is None or pghome != home:
                if pghome is None:
                    sql = "insert into p_normal_cib(target_id,index_id,cib_name,cib_value,record_time) values('%s',1000001,'pghome','%s',now())" % (targetId, home)
                else:
                    sql = "update p_normal_cib set cib_value='%s',record_time=now() where target_id='%s' and index_id=1000001 and cib_name='pghome'" % (home, targetId)
                cur = conn.conn.cursor()
                cur.execute(sql)
            else:
                cur = None
            if pguser is None or pguser != user:
                if pguser is None:
                    sql = "insert into p_normal_cib(target_id,index_id,cib_name,cib_value,record_time) values('%s',1000001,'pguser','%s',now())" % (targetId, cs(user))
                else:
                    sql = "update p_normal_cib set cib_value='%s',record_time=now() where target_id='%s' and index_id=1000001 and cib_name='pguser'" % (cs(user), targetId)
                cur = conn.conn.cursor()
                cur.execute(sql)
            if ddir and (pgddir is None or pgddir != ddir):
                if pgddir is None:
                    sql = "insert into p_normal_cib(target_id,index_id,cib_name,cib_value,record_time) values('%s',1000001,'pgdata','%s',now())" % (targetId, ddir)
                else:
                    sql = "update p_normal_cib set cib_value='%s',record_time=now() where target_id='%s' and index_id=1000001 and cib_name='pgdata'" % (ddir, targetId)
                cur = conn.conn.cursor()
                cur.execute(sql)
            if not cur is None:
                conn.conn.commit()
        except Exception as e:
            conn.conn.rollback()


if __name__ == '__main__':
    dbInfo = eval(sys.argv[1])
    target_id, pg = DBUtil.get_pg_env(None, 1)
    pg_flag = is_pg(pg, target_id)
    if pg_flag in [4,7,15,16,9,12]:
        conn = DBUtil.get_gaussdb_env()
    else:
        conn = DBUtil.get_pg_env_target()
    pg_ip = dbInfo['target_ip']
    metric = []
    if conn.conn:
        cib_basic(conn, metric, pg_flag)
        cib_parameters(conn, metric, pg_flag)
        cib_extension(conn, metric, pg_flag)
        cib_db(conn, metric, pg_flag)
        cib_tablespace(conn, metric, pg_flag)
        cib_replication(conn, metric, pg_flag)
        pg_env(pg, conn, target_id, pg_flag)
        set_focus(pg, target_id)
    print('{"cib":' + json.dumps(metric) + '}') 
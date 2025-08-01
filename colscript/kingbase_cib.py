import sys

sys.path.append('/usr/software/knowl')
import json
import DBUtil


def cs(val, dt=False):
    if val is None:
        return ''
    else:
        if dt:
            return val.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return str(val)


def cib_basic(db, metric,dbinfo):
    target_ip = dbinfo['target_ip']
    vals = []
    vals.append(dict(name="host_ip", value=cs(target_ip)))
    sql = """
select name,setting from sys_settings where name in ('server_version','server_encoding','lc_collate','port','data_directory',
'log_destination','log_directory','log_filename')
"""
    cursor = DBUtil.getValue(db, sql)
    rs = cursor.fetchall()
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
            vals.append(dict(name="pgdata", value=cs(row[1])))
        elif row[0] == 'log_destination':
            vals.append(dict(name="log_destination", value=cs(row[1])))
        elif row[0] == 'log_directory':
            vals.append(dict(name="log_directory", value=cs(row[1])))
        elif row[0] == 'log_filename':
            vals.append(dict(name="log_filename", value=cs(row[1])))
    sql = """
select timeline_id,system_identifier,version() from sys_control_checkpoint(),sys_control_system()
    """
    cursor = DBUtil.getValue(db, sql)
    rs = cursor.fetchone()
    vals.append(dict(name="timeline", value=cs(rs[0])))
    vals.append(dict(name="systemid", value=cs(rs[1])))
    vals.append(dict(name="version_comment", value=cs(rs[2])))
    # cmd1 = "ps -ef|grep 'bin/postgres'|grep -v grep|awk '{print $8}'"
    # res_cmd1 = ssh.opencmd(cmd1).strip()
    # pghome = res_cmd1.split('/bin')[0]
    # vals.append(dict(name="pghome", value=cs(pghome)))
    # cmd2 = "hostname"
    # hostname = ssh.opencmd(cmd2).strip()
    # vals.append(dict(name="hostname", value=cs(hostname)))
    metric.append(dict(index_id="2370001", value=vals))


def cib_parameters(db, metric):
    vals = []
    sql = """
select name,setting from sys_settings
    """
    cursor = DBUtil.getValue(db, sql)
    rs = cursor.fetchall()
    for row in rs:
        vals.append(dict(name=row[0], value=cs(row[1])))
    metric.append(dict(index_id="2370002", value=vals))


def cib_extension(db, metric):
    vals = []
    sql = """
select extname,usename,extversion,'Online' state from sys_extension, sys_user where usesysid=extowner
"""
    cursor = DBUtil.getValue(db, sql)
    rs = cursor.fetchall()
    vals.append(
        dict(c1="扩展名称", c2="扩展属主", c3="扩展版本", c4='状态', c5=None, c6=None, c7=None, c8=None, c9=None, c10=None))
    for row in rs:
        vals.append(dict(c1=cs(row[0]), c2=cs(row[1]), c3=cs(row[2]), c4=cs(row[3]), c5=None, c6=None, c7=None, c8=None,
                         c9=None, c10=None))
    metric.append(dict(index_id="2370003", content=vals))


def cib_db(db, metric):
    vals = []
    sql = """
SELECT datname,usename,sys_encoding_to_char ( ENCODING ),
	datcollate,
	datistemplate,
	datallowconn,
	datlastsysoid,
	datfrozenxid,
	spcname 
FROM
	sys_database,
	sys_user,
	sys_tablespace P 
WHERE
	usesysid = datdba 
	AND dattablespace = P.oid
"""
    cursor = DBUtil.getValue(db, sql)
    rs = cursor.fetchall()
    vals.append(
        dict(c1="数据库", c2="管理用户", c3="编码", c4="排序码", c5="是否模板", c6="是否允许连接", c7="系统OID", c8="冻结XID", c9="表空间",
             c10=None))
    for row in rs:
        vals.append(dict(c1=cs(row[0]), c2=cs(row[1]), c3=cs(row[2]), c4=cs(row[3]), c5=cs(row[4]), c6=cs(row[5]),
                         c7=cs(row[6]), c8=cs(row[7]), c9=cs(row[8]), c10=None))
    metric.append(dict(index_id="2370004", content=vals))


def cib_tablespace(db, metric):
    vals = []
    sql = """
select spcname,usename from sys_tablespace,sys_user where spcowner=usesysid
"""
    cursor = DBUtil.getValue(db, sql)
    rs = cursor.fetchall()
    vals.append(dict(c1="表空间名称", c2="表空间属主", c3=None, c4=None, c5=None, c6=None, c7=None, c8=None, c9=None, c10=None))
    for row in rs:
        vals.append(
            dict(c1=cs(row[0]), c2=cs(row[1]), c3=None, c4=None, c5=None, c6=None, c7=None, c8=None, c9=None, c10=None))
    metric.append(dict(index_id="2370005", content=vals))


def cib_replication(db, metric):
    vals = []
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
    metric.append(dict(index_id="2370006", content=vals))


if __name__ == '__main__':
    dbInfo = eval(sys.argv[1])
    pg = DBUtil.get_pg_env_target()
    conn = None
    metric = []
    if pg.conn:
        # metric.append(dict(index_id="2370000", value="连接成功"))
        cib_basic(pg, metric,dbInfo)
        cib_parameters(pg, metric)
        cib_extension(pg, metric)
        cib_db(pg, metric)
        cib_tablespace(pg, metric)
        cib_replication(pg, metric)
    # else:
    # metric.append(dict(index_id="2370000", value="连接失败"))
    print('{"cib":' + json.dumps(metric) + '}')

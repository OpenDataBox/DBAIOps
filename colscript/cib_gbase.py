import sys
sys.path.append('/usr/software/knowl')
import DBUtil
import sql_gauss
from collections import defaultdict
from DBAIOps_logger import Logger

log = Logger()
dirs = {}

def get_dict(d_dict, item):
    value = d_dict.get(item)
    if value is None:
        value = 0
    return str(value)


def insert_if_not_exists(target_id, index_id, value):
    if target_id == 'ALL' and role == 'Primary':
        if cluster_type == 'distributed':
            sql2 = f"select node_host,node_port1 from pgxc_node where node_type in ('D','C','S')"
            cursor = DBUtil.getValue(gs_conn, sql2)
            result = cursor.fetchall()
            for row in result:
                host_ip = row[0]
                port = row[1]
                sql = f"select uid from mgt_system ms where ip = '{host_ip}' and port= '{port}' and use_flag and subuid is not null"
                cursor = DBUtil.getValue(pg, sql)
                result = cursor.fetchone()
                if result is not None:
                    uid = result[0]
                    target_id = uid
                    if target_id[:4] == '2202':
                        index_type = '283'
                    else:
                        index_type = '222'
                    for item in global_metric:
                        if item["targetId"] == target_id:
                            if isinstance(value, list) and 'c1' in value[0].keys():
                                item["results"].append({"index_id": index_type + str(str(index_id)[3:]), "content": value})
                            else:
                                item["results"].append({"index_id": index_type + str(str(index_id)[3:]), "value": cs(value)})
                            break
                    else:
                        if isinstance(value, list) and 'c1' in value[0].keys():
                            new_entry = {
                            "targetId": target_id,
                            "indexType": index_type,
                            "results": [{"index_id": index_type + str(str(index_id)[3:]), "content": cs(value)}]
                        }
                        else:
                            new_entry = {
                            "targetId": target_id,
                            "indexType": index_type,
                            "results": [{"index_id": index_type + str(str(index_id)[3:]), "value": cs(value)}]
                        }
                        global_metric.append(new_entry)
    else:
        if target_id and role == 'Primary':
            if target_id[:4] == '2202':
                index_type = '283'
            else:
                index_type = '222'
            for item in global_metric:
                if item["targetId"] == target_id:
                    if isinstance(value, list) and 'c1' in value[0].keys():
                        item["results"].append({"index_id": index_type + str(str(index_id)[3:]), "content": value})
                    else:
                        item["results"].append({"index_id": index_type + str(str(index_id)[3:]), "value": cs(value)})
                    break
            else:
                if isinstance(value, list) and 'c1' in value[0].keys():
                    new_entry = {
                    "targetId": target_id,
                    "indexType": index_type,
                    "results": [{"index_id": index_type + str(str(index_id)[3:]), "content": cs(value)}]
                }
                else:
                    new_entry = {
                    "targetId": target_id,
                    "indexType": index_type,
                    "results": [{"index_id": index_type + str(str(index_id)[3:]), "value": cs(value)}]
                }
                global_metric.append(new_entry)


def get_uid_by_nodename(node_name=None, uids=None):
    if uids:
        uid = uids
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
        uid = target_id
    return uid


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
            if isinstance(val, list):
                return val
            else:
                return str(val)


def cib_basic(db, uid=None):
    vals = []
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
        # elif row[0] == 'data_directory':
        #     data_dir = cs(row[1])
        #     vals.append(dict(name="pgdata", value=cs(row[1])))
        #     vals.append(dict(name="wal_directory", value=cs(row[1]) + '/pg_xlog'))
        elif row[0] == 'log_destination':
            vals.append(dict(name="log_destination", value=cs(row[1])))
        # elif row[0] == 'log_directory':
        #     if row[1].find('/') == -1:
        #         log_directory = data_dir + '/' + cs(row[1])
        #     else:
        #         log_directory = cs(row[1])
        #     vals.append(dict(name="log_directory", value=log_directory))
        elif row[0] == 'TimeZone':
            vals.append(dict(name="timezone", value=cs(row[1])))
        # elif row[0] == 'config_file':
        #     vals.append(dict(name="config_file", value=cs(row[1])))
        elif row[0] == 'archive_mode':
            vals.append(dict(name="archive_mode", value=cs(row[1])))
        elif row[0] == 'log_filename':
            vals.append(dict(name="log_filename", value=cs(row[1])))
    vals.append(dict(name="log_filename", value='postgresql-%Y-%m-%d_%H%M%S.log'))
    sql2 = "select datapath,log_directory from pg_node_env"
    cursor2 = DBUtil.getValue(db, sql2)
    rs2 = cursor2.fetchone()
    if rs2:
        data_dir = cs(rs2[0])
        vals.append(dict(name="pgdata", value=cs(rs2[0])))
        vals.append(dict(name="wal_directory", value=cs(rs2[0]) + '/pg_xlog'))
        vals.append(dict(name="datapath", value=cs(rs2[0])))
        if rs2[1].find('/') == -1:
            log_directory = data_dir + '/' + cs(rs2[1])
        else:
            log_directory = cs(rs2[1])
        vals.append(dict(name="log_directory", value=log_directory))
        vals.append(dict(name="config_file", value=cs(rs2[0]) + '/postgresql.conf'))
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
    sql = "select pg_is_in_recovery()"
    cursor = DBUtil.getValue(db, sql)
    crt_rs = cursor.fetchone()
    if crt_rs[0]:
        db_role = 'Slave'
    else:
        db_role = 'Master'
    vals.append(dict(name="db_role", value=cs(db_role)))
    sql_a = "select max(age(datfrozenxid64)) from pg_database"
    cursor = DBUtil.getValue(db, sql_a)
    crt_rs = cursor.fetchone()
    if crt_rs and crt_rs[0]:
        db_age = crt_rs[0]
        vals.append(dict(name="db_age", value=cs(db_age)))
    vals.append(dict(name="host_ip", value=cs(gauss_ip)))
    # dn,cn CPU核数
    sql = "select node_name ,value from dbe_perf.GLOBAL_OS_RUNTIME where name in ('NUM_CPU_CORES')"
    cursor = DBUtil.getValue(db, sql)
    rs = cursor.fetchall()
    dn_cpus = 0
    cn_cpus = 0
    cns = 0
    dns = 0
    for row in rs:
        node_name = row[0]
        cpu_cores = row[1]
        if node_name.startswith('cn'):
            cn_cpus += int(cpu_cores)
            cns += 1
        else:
            dn_cpus += int(cpu_cores)
            dns += 1
        uid = get_uid_by_nodename(node_name, uid)
        if uid:
            insert_if_not_exists(uid, index_id="2870001", value=[dict(name='cpu_cores',value=cs(cpu_cores))])
    vals.append(dict(name="cn_nodes", value=cs(cns)))
    vals.append(dict(name="dn_nodes", value=cs(dns)))
    vals.append(dict(name="cn_cpu_total", value=cs(cn_cpus)))
    vals.append(dict(name="dn_cpu_total", value=cs(dn_cpus)))
    if uid:
        insert_if_not_exists(uid, index_id="2870001", value=cs(vals))
    insert_if_not_exists(target_id, index_id="2870001", value=cs(vals))
    insert_if_not_exists('ALL', index_id="2870001", value=cs(vals))


def cib_parameters(db, uid=None):
    vals = []
    sql = """
    select name,setting,unit from pg_settings
    """
    cursor = DBUtil.getValue(db, sql)
    rs = cursor.fetchall()
    for row in rs:
        name, value, unit = row
        if value and (value.isdigit() or value == '-1'):
            vals.append(dict(name=name, value=cs(sql_gauss.standard_units(value, unit))))
        else:
            if not unit or unit == 'None':
                vals.append(dict(name=name, value=cs(value)))
            else:
                vals.append(dict(name=name, value=str(value) + ' ' + str(unit)))
    vals.append(dict(name="log_filename", value='postgresql-%Y-%m-%d_%H%M%S.log'))
    sql2 = "select datapath,log_directory from pg_node_env"
    cursor2 = DBUtil.getValue(db, sql2)
    rs2 = cursor2.fetchone()
    if rs2:
        data_dir = cs(rs2[0])
        vals.append(dict(name="data_directory", value=cs(rs2[0])))
        if rs2[1].find('/') == -1:
            log_directory = data_dir + '/' + cs(rs2[1])
        else:
            log_directory = cs(rs2[1])
        vals.append(dict(name="log_directory", value=log_directory))
    insert_if_not_exists(target_id, index_id="2870002", value=cs(vals))
    insert_if_not_exists('ALL', index_id="2870002", value=cs(vals))
    # dn,cn CPU核数
    sql = "select node_name ,value from dbe_perf.GLOBAL_OS_RUNTIME where name in ('NUM_CPU_CORES')"
    cursor = DBUtil.getValue(db, sql)
    rs = cursor.fetchall()
    dn_total = defaultdict(int)
    cn_total = defaultdict(int)
    for row in rs:
        node_name = row[0]
        cpu_cores = row[1]
        if node_name.startswith('cn'):
            cn_total['_cn_cpu_total'] += int(cpu_cores)
        else:
            dn_total['_dn_cpu_total'] += int(cpu_cores)
        uid = get_uid_by_nodename(node_name, uid)
        if uid:
            insert_if_not_exists(uid, index_id="2870002", value=[dict(name='cpu_cores',value=cs(cpu_cores))])
    for k, v in dn_total.items():
        insert_if_not_exists(target_id, index_id="2870002", value=[dict(name=k,value=cs(v))])
    for k, v in cn_total.items():
        insert_if_not_exists(target_id, index_id="2870002", value=[dict(name=k,value=cs(v))])


def cib_extension(db, uid=None):
    vals = []
    if cluster_type == 'distributed':
        sql = """
        EXECUTE DIRECT ON ALL 'select  pgxc_node_str() as node_name ,
        extname, 
                    nspname, 
                    extversion, 
                    comment
                    from pg_extension a,
                        pg_available_extensions b,
                        pg_namespace c
                    where a.extname = b.name
                    and a.extnamespace = c.oid'
        """
    else:
        sql = """
        select pgxc_node_str() as node_name ,extname, 
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
        dict(c1="节点",c2="插件名称", c3="名称空间", c4="插件版本", c5='描述'))
    for row in rs:
        vals.append(dict(c1=cs(row[0]), c2=cs(row[1]), c3=cs(row[2]), c4=cs(row[3]),c5=cs(row[4])))
    if uid:
        insert_if_not_exists(uid, index_id="2870003", value=cs(vals))
    insert_if_not_exists('ALL', index_id="2870003", value=cs(vals))
    insert_if_not_exists(target_id, index_id="2870003", value=cs(vals))


def cib_db(db, uid=None):
    vals = []
    if cluster_type == 'distributed':
        sql = """
        EXECUTE DIRECT ON ALL 'select 
            datname,
            pg_get_userbyid(datdba),
            t.spcname,
            round(pg_database_size(d.oid)/1024/1024) as size,
            pg_encoding_to_char(encoding),
            datcollate,
            datctype,
            datistemplate,
            datallowconn,
            pgxc_node_str() as node_name
        from pg_database d,
            pg_tablespace t
        where d.dattablespace = t.oid'
        """
    else:
        sql = """
        select 
            datname,
            pg_get_userbyid(datdba),
            t.spcname,
            round(pg_database_size(d.oid)/1024/1024) as size,
            pg_encoding_to_char(encoding),
            datcollate,
            datctype,
            datistemplate,
            datallowconn,
            pgxc_node_str() as node_name
        from pg_database d,
            pg_tablespace t
        where d.dattablespace = t.oid
        """
    cursor = DBUtil.getValue(db, sql)
    rs = cursor.fetchall()
    vals.append(
        dict(c1="数据库名称", c2="属主", c3="表空间名称", c4="数据库大小(MB)", c5="编码", c6="语言符号及其分类编码", c7="比较和排序编码", c8="是否模板",
             c9="是否允许连接",c10="节点"))
    for row in rs:
        vals.append(dict(c1=cs(row[0]) + f"({cs(row[9])})", c2=cs(row[1]), c3=cs(row[2]), c4=cs(row[3]), c5=cs(row[4]), c6=cs(row[5]),
                         c7=cs(row[6]), c8=cs(row[7]), c9=cs(row[8]), c10=cs(row[9])))
    if uid:
        insert_if_not_exists(uid, index_id="2870004", value=cs(vals))
    insert_if_not_exists('ALL', index_id="2870004", value=cs(vals))
    insert_if_not_exists(target_id, index_id="2870004", value=cs(vals))


def cib_tablespace(db, uid=None):
    vals = []
    if cluster_type == 'distributed':
        sql = """
        EXECUTE DIRECT ON ALL 'select 
            spcname,
            pg_get_userbyid(spcowner) as owner ,
            pg_tablespace_location(oid) as location,
            pg_size_pretty(pg_tablespace_size(oid)) as dbsize,
            pgxc_node_str() as node_name
        from pg_tablespace'
        """
    else:
        sql = """
        select
            spcname,
            pg_get_userbyid(spcowner) as owner ,
            pg_tablespace_location(oid) as location,
            pg_size_pretty(pg_tablespace_size(oid)) as dbsize,
             pgxc_node_str() as node_name
        from pg_tablespace
        """
    cursor = DBUtil.getValue(db, sql)
    rs = cursor.fetchall()
    vals.append(
        dict(c1="表空间名称", c2="属主", c3="表空间路径", c4="表空间大小",c5="节点"))
    for row in rs:
        vals.append(
            dict(c1=cs(row[0]), c2=cs(row[1]), c3=cs(row[2]), c4=cs(row[3]),c5=cs(row[4])))
    if uid:
        insert_if_not_exists(uid, index_id="2870005", value=cs(vals))
    insert_if_not_exists('ALL', index_id="2870005", value=cs(vals))
    insert_if_not_exists(target_id, index_id="2870005", value=cs(vals))


def set_focus(conn, uid):
    sql = "select distinct cib_value from p_oracle_cib c where c.target_id='%s' and index_id=2830001 and cib_name in ('pgdata','log_directory')" % uid
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
    except Exception:
        conn.conn.rollback()


def get_pgxc_node(db):
    """获取pgxc_node信息"""
    vals = []
    sql = "select node_name,decode(node_type,'C','协调节点','D','数据节点','S','备份节点'),node_port,node_host,node_port1,node_host1,hostis_primary,node_id,nodeis_central from pg_catalog.pgxc_node"
    cursor = DBUtil.getValue(db, sql)
    rs = cursor.fetchall()
    vals.append(
        dict(c1="节点名称", c2="节点类型", c3="端口号", c4="IP", c5="复制节点的端口号", c6="复制节点的IP", c7="是否发生主备切换", c8="节点标志符", c9="是否控制节点"))
    for row in rs:
        vals.append(
            dict(c1=cs(row[0]), c2=cs(row[1]), c3=cs(row[2]), c4=cs(row[3]), c5=cs(row[4]), c6=cs(row[5]),c7=cs(row[6]), c8=cs(row[7]), c9=cs(row[8])))
    insert_if_not_exists(target_id, index_id="2870007", value=cs(vals))


def gauss_cluster_info(pg, target_id, gauss_ip,dcs):
    ostype, ssh, os_user = DBUtil.getsshinfo_user(pg, gauss_ip)
    if os_user == 'root':
        cmd = "su - $(ps -ef|grep gaussdb|grep gbase|awk 'NR <=1 {print$1}') -c 'gha_ctl monitor all -l %s'" % dcs
    else:
        cmd = "gha_ctl monitor all -l %s" % dcs
    result  = ssh.exec_cmd(cmd)
    if isinstance(result, tuple):
        print("查询集群状态失败，Error: %s" % result[1])
        return
    data = {}
    # 逐行解析文本
    lines = result.split('\n')

    current_section = ''
    node_num = 1
    srvs = set()
    cnsrvs = set()
    dnsrvs = set()
    cluster_info = {'cluster_state': None,
                    'redistributing': None,
                    'balanced': None,
                    'current_az': None,
                    }
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 判断是否为新的组件部分
        if '[' in line and ']' in line:
            current_section = line[1:-1].strip()
            data[current_section] = []
        elif ':' in line:
            # 处理键值对部分
            key, value = map(str.strip, line.split(':', 1))
            if current_section:
                if 'cluster_state' in key:
                    cluster_info['cluster_state'] = value
                elif 'redistributing' in key:
                    cluster_info['redistributing'] = value
                elif 'balanced' in key:
                    cluster_info['balanced'] = value
                elif 'current_az' in key:
                    cluster_info['current_az'] = value
        elif '  ' in line:
            # 处理表格部分
            if '|' not in line:
                columns = line.split()
            else:
                columns = line
            if 'CMServer' in current_section and 'instance' not in line:
                # 处理CMServer部分
                data[current_section].append({
                    'node': columns[0],
                    'node_ip': columns[2],
                    'host_ip': columns[3],
                    'path': columns[5],
                    'state': columns[6],
                })
                srvs.add(columns[3])
            elif 'ETCD' in current_section and 'instance' not in line:
                # 处理ETCD部分
                data[current_section].append({
                    'node': columns[0],
                    'node_ip': columns[2],
                    'host_ip': columns[3],
                    'port': columns[4],
                    'path': columns[5],
                    'state': columns[6],
                })
                srvs.add(columns[3])
            elif  'Coordinator' in current_section and 'instance' not in line:
                # 处理Coordinator部分
                if len(columns) == 8:
                    data[current_section].append({
                    'node': columns[0],
                    'node_ip': columns[2],
                    'host_ip': columns[3],
                    'port': columns[5],
                    'path': columns[6],
                    'state': columns[7],
                })
                srvs.add(columns[3])
                cnsrvs.add(columns[3])
            elif 'GTM' in current_section and 'instance' not in line:
                # 处理GTM部分
                if len(columns) == 11:
                    data[current_section].append({
                        'node': columns[0],
                        'node_ip': columns[2],
                        'host_ip': columns[3],
                        'port': columns[4],
                        'path': columns[5],
                        'role': columns[7],
                        'conn_state': columns[9],
                        'state': columns[10],
                    })
                else:
                    data[current_section].append({
                        'node': columns[0],
                        'node_ip': columns[2],
                        'host_ip': columns[3],
                        'port': columns[4],
                        'path': columns[5],
                        'role': columns[7],
                        'conn_state': 'shutdown',
                        'state': columns[9],
                    })
                srvs.add(columns[3])
            elif 'Datanode' in current_section and 'instance' not in line:
                # 处理Datanode部分
                one_group = {}
                one_group['node_%d' % node_num] = []
                for row in columns.split('|'):
                    columns = row.split()
                    one_group['node_%d' % node_num].append({
                            'node': columns[0],
                            'node_ip': columns[2],
                            'host_ip': columns[3],
                            'port': columns[5],
                            'path': columns[6],
                            'role': columns[8],
                            'state': columns[9],
                        })
                    srvs.add(columns[3])
                    dnsrvs.add(columns[3])
                node_num += 1
                data[current_section].append(one_group)

    data['Cluster State'].append(cluster_info)
    # CMServer
    cms_info = data['CMServer State']
    vals = []
    vals.append(dict(c1="节点", c2="节点IP", c3="主机物理IP", c4="路径", c5="状态"))
    for row in cms_info:
        node = row['node']
        node_ip = row['node_ip']
        host_ip = row['host_ip']
        path = row['path']
        state = row['state']
        vals.append(dict(c1=cs(node), c2=cs(node_ip), c3=cs(host_ip), c4=cs(path), c5=cs(state)))
    insert_if_not_exists(target_id, index_id="2870013", value=cs(vals))
    insert_if_not_exists('ALL', index_id="2870013", value=cs(vals))
    # ETCD State
    etcd_info = data['ETCD State']
    vals2 = []
    vals2.append(dict(c1="节点", c2="节点IP", c3="主机物理IP", c4="路径", c5="状态"))
    for row in etcd_info:
        node = row['node']
        node_ip = row['node_ip']
        host_ip = row['host_ip']
        path = row['path']
        state = row['state']
        vals2.append(dict(c1=cs(node), c2=cs(node_ip), c3=cs(host_ip), c4=cs(path), c5=cs(state)))
    insert_if_not_exists(target_id, index_id="2870008", value=cs(vals2))
    insert_if_not_exists('ALL', index_id="2870008", value=cs(vals))
    if cluster_type == 'distributed':
        # Coordinator State
        coordinator_info = data['Coordinator State']
        vals4 = [] 
        vals4.append(dict(c1="节点", c2="节点IP", c3="主机物理IP", c4="端口", c5="状态", c6="路径"))
        for row in coordinator_info:
            node = row['node']
            node_ip = row['node_ip']
            host_ip = row['host_ip']
            port = row['port']
            path = row['path']
            state = row['state']
            vals4.append(dict(c1=cs(node), c2=cs(node_ip), c3=cs(host_ip), c4=cs(port), c5=cs(state), c6=cs(path)))
        insert_if_not_exists(target_id, index_id="2870010", value=cs(vals4))
        insert_if_not_exists('ALL', index_id="2870010", value=cs(vals))
        # GTM State
        gtm_info = data['GTM State']
        vals5 = []
        vals5.append(dict(c1="节点", c2="节点IP", c3="主机物理IP", c4="节点ID", c5="路径", c6="角色", c7="连接状态", c8="状态"))
        for row in gtm_info:
            node = row['node']
            node_ip = row['node_ip']
            host_ip = row['host_ip']
            port = row['port']
            path = row['path']
            role = row['role']
            conn_state = row['conn_state']
            state = row['state']
            vals5.append(dict(c1=cs(node), c2=cs(node_ip), c3=cs(host_ip), c4=cs(port), c5=cs(path), c6=cs(role), c7=cs(conn_state), c8=cs(state)))
        insert_if_not_exists(target_id, index_id="2870011", value=cs(vals5))
        insert_if_not_exists('ALL', index_id="2870011", value=cs(vals))
    # Datanode State
    datanode_info = data['Datanode State']
    vals6 = []
    vals6.append(dict(c1="节点", c2="节点IP", c3="主机物理IP", c4="端口", c5="路径", c6="角色", c7="状态", c8='DN组名(自定义)'))
    vals = []
    vals.append(dict(c1="节点名称", c2="节点类型", c3="端口号", c4="IP", c5="状态"))
    for row in datanode_info:
        for key, value in row.items():
            for dn_r in value:
                node = dn_r['node']
                node_ip = dn_r['node_ip']
                host_ip = dn_r['host_ip']
                port = dn_r['port']
                path = dn_r['path']
                role = dn_r['role']
                state = dn_r['state']
                vals6.append(dict(c1=cs(node), c2=cs(node_ip), c3=cs(host_ip), c4=cs(port), c5=cs(path), c6=cs(role), c7=cs(state), c8=cs(key)))
                vals.append(dict(c1=cs(node), c2=cs(role), c3=cs(port), c4=cs(host_ip), c5=cs(state)))
    insert_if_not_exists(target_id, index_id="2870007", value=cs(vals))
    insert_if_not_exists(target_id, index_id="2870012", value=cs(vals6))
    insert_if_not_exists('ALL', index_id="2870007", value=cs(vals))
    insert_if_not_exists('ALL', index_id="2870012", value=cs(vals))
    if srvs and dnsrvs:
        gs_os(pg, target_id, srvs, cnsrvs, dnsrvs)
    return datanode_info


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


def gs_path(db, dirs):
    cur = db.conn.cursor()
    chg = False
    for uid in dirs.keys():
        if uid[0:4] != '2104':
            continue
        sql = "select cib_name,cib_value from p_normal_cib where target_id='%s' and index_id=1000001 and cib_name in ('_data_path','_log_path')" % uid
        cs = DBUtil.getValue(db, sql)
        rs = cs.fetchall()
        paths = [None, None]
        if rs:
            for row in rs:
                if row[0] == '_data_path':
                    paths[0] = row[1]
                else:
                    paths[1] = row[1]
        if paths[0] != dirs[uid][0] or paths[1] != dirs[uid][1]:
            try:
                sql = "delete from p_normal_cib where target_id='%s' and index_id=1000001 and cib_name in ('_data_path','_log_path')" % uid
                cur.execute(sql)
                if dirs[uid][0]:
                    sql = "insert into p_normal_cib(target_id,index_id,cib_name,cib_value,record_time) values('%s',1000001,'_data_path','%s',now())" % (uid, dirs[uid][0])
                    cur.execute(sql)
                if dirs[uid][1]:
                    sql = "insert into p_normal_cib(target_id,index_id,cib_name,cib_value,record_time) values('%s',1000001,'_log_path','%s',now())" % (uid, dirs[uid][1])
                    cur.execute(sql)
                chg = True
            except Exception as e:
                log.info('cib[' + uid + ']:' + str(e))
                db.conn.rollback()
                return
    if chg:
        db.conn.commit()


def gs_os(db, uid, srvs, cnsrvs, dnsrvs):
    if srvs:
        sql = "select cib_name,cib_value from p_normal_cib where target_id='%s' and index_id=1000001 and cib_name in ('_ips','_cnips','_dnips')" % uid
        cs1 = DBUtil.getValue(db, sql)
        rs1 = cs1.fetchall()
        ips = set()
        cnips = set()
        dnips = set()
        if rs1:
            for row in rs1:
                if row[0] == '_ips':
                    arr = row[1].split(',')
                    for ip in arr:
                        ips.add(ip)
                elif row[0] == '_cnips':
                    arr = row[1].split(',')
                    for ip in arr:
                        cnips.add(ip)
                else:
                    arr = row[1].split(',')
                    for ip in arr:
                        dnips.add(ip)
        vs = set()
        for row in srvs:
            vs.add(row)
        cnvs = set()
        for row in cnsrvs:
            cnvs.add(row)
        dnvs = set()
        for row in dnsrvs:
            dnvs.add(row)
        if vs != ips or cnvs != cnips or dnvs != dnips:
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
                    ss = ''
                    ss2 = ''
                    ss3 = ''
                    f = True
                    for ip in vs:
                        if ss:
                            ss += ',' + ip
                        else:
                            ss = ip
                        if ip in cnvs:
                            if ss2:
                                ss2 += ',' + ip
                            else:
                                ss2 = ip
                        if ip in dnvs:
                            if ss3:
                                ss3 += ',' + ip
                            else:
                                ss3 = ip
                        row = hosts.get(ip)
                        if row:
                            vs2 = vs.copy()
                            if len(vs2) > 1:
                                vs2.remove(ip)
                            if f:
                                s = '+' + tuple2(vs2)
                                f = False
                            else:
                                s = tuple2(vs2)
                            if vs2:
                                sql = "insert into p_normal_cib(target_id,index_id,cib_name,cib_value,record_time) values('%s',1000001,'_ping','%s',now())" % (row[0], s)
                                cur.execute(sql)
                    sql = "delete from p_normal_cib where target_id='%s' and index_id=1000001 and cib_name in ('_ips','_cnips','_dnips')" % uid
                    cur.execute(sql)
                    sql = "insert into p_normal_cib(target_id,index_id,cib_name,cib_value,record_time) values('%s',1000001,'_ips','%s',now())" % (uid, ss)
                    cur.execute(sql)
                    sql = "insert into p_normal_cib(target_id,index_id,cib_name,cib_value,record_time) values('%s',1000001,'_cnips','%s',now())" % (uid, ss2)
                    cur.execute(sql)
                    sql = "insert into p_normal_cib(target_id,index_id,cib_name,cib_value,record_time) values('%s',1000001,'_dnips','%s',now())" % (uid, ss3)
                    cur.execute(sql)
                    db.conn.commit()
                except Exception as e:
                    log.info('cib[' + target_id + ']:' + str(e))
                    db.conn.rollback()
        gs_path(db, dirs)

def global_config_settings(gs_conn, uid=None):
    global dirs
    """获取cn，dn的参数配置"""
    sql = "select node_name,name,setting,unit FROM dbe_perf.GLOBAL_CONFIG_SETTINGS order by node_name"
    cursor = DBUtil.getValue(gs_conn, sql)
    rs = cursor.fetchall()
    node_name = None
    vals = []
    vals2 = []
    vals2.append(dict(c1="节点名称", c2="参数名称", c3="值", c4="单位"))
    for row in rs:
        vals2.append(dict(c1=cs(row[0]), c2=cs(row[1]), c3=cs(row[2]), c4=cs(row[3])))
        if node_name != row[0]:
            if uid and vals:
                insert_if_not_exists(uid, index_id="2870002", value=cs(vals))
            node_name = row[0]
            uid = get_uid_by_nodename(node_name, uid)
            vals = []
        name = row[1]
        if row[3]:
            setting = row[2] + ' ' + row[3]
        else:
            setting = row[2]
        vals.append(dict(name=name, value=cs(setting)))
        if uid:
            if name in ['data_directory','log_directory']:
                ds = dirs.get(uid)
                if ds is None:
                    ds = [None, None]
                    dirs[uid] = ds
                if name == 'data_directory':
                    ds[0] = row[2]
                else:
                    ds[1] = row[2]
    if uid:
        insert_if_not_exists(uid, index_id="2870002", value=cs(vals))
    insert_if_not_exists(target_id, index_id="2870014", value=cs(vals2))

def pgxc_node_env(gs_conn):
    if cluster_type == 'distributed':
        sql = "select * from pg_catalog.pgxc_node_env"
    else:
        sql = "select * from pg_catalog.pg_node_env"
    cursor = DBUtil.getValue(gs_conn, sql)
    rs = cursor.fetchall()
    vals = []
    vals.append(dict(c1="节点", c2="主机", c3="进程号", c4="端口", c5="安装目录", c6="数据目录", c7="日志目录"))
    for row in rs:
        vals.append(dict(c1=cs(row[0]), c2=cs(row[1]), c3=cs(row[2]), c4=cs(row[3]), c5=cs(row[4]), c6=cs(row[5]), c7=cs(row[6])))
    insert_if_not_exists(target_id, index_id="2870015", value=cs(vals))
    return vals


def get_uid_by_ip(pg, ip, port):
    sql = f"select uid from mgt_system ms where ip = '{ip}' and port='{port}' and use_flag and subuid is not null"
    cursor = DBUtil.getValue(pg, sql)
    result = cursor.fetchone()
    uid = None
    if result is not None:
        uid = result[0]
    return uid   


if __name__ == '__main__':
    global_metric = []
    dbInfo = eval(sys.argv[1])
    gs_conn = DBUtil.get_gaussdb_env(exflag=2)
    gb_ip = dbInfo['target_ip']
    target_id, pg = DBUtil.get_pg_env(None, 0)
    cluster_type = DBUtil.get_gauss_type(pg, target_id)     # centralized, distributed
    dsc = DBUtil.get_gbase_dcs(pg, target_id) 
    # 打印操作系统环境变量
    role = 'Primary'
    if gs_conn.conn:
        set_focus(pg, target_id)
        is_cloud = DBUtil.gauss_is_cloud(pg, target_id)
        if cluster_type == 'distributed':
            global_config_settings(gs_conn)
            cib_basic(gs_conn)
            cib_parameters(gs_conn)
            cib_extension(gs_conn)
            cib_db(gs_conn)
            cib_tablespace(gs_conn)
            if not is_cloud:
                gauss_cluster_info(pg, target_id, gb_ip,dsc)
            get_pgxc_node(gs_conn)
            pgxc_node_env(gs_conn)
        else:
            # 获取所有节点连接信息
            if not is_cloud:
                nodes_info = gauss_cluster_info(pg, target_id, gb_ip,dsc)
                if nodes_info:
                    for row in nodes_info:
                        for key, value in row.items():
                            for dn_r in value:  # 同一个组的datanode
                                ip = dn_r['host_ip']
                                port = dn_r['port']
                                role = dn_r['role']
                                if role in ('Primary', 'Standby'):
                                    read_only = False if role == 'Primary' else True
                                    uid = get_uid_by_ip(pg, ip, port)
                                    dn_conn = DBUtil.get_dn_conn(target_id, ip, port, read_only)
                                    global_config_settings(gs_conn, uid)
                                    cib_basic(gs_conn,uid)
                                    cib_parameters(gs_conn,uid)
                                    cib_extension(gs_conn,uid)
                                    cib_db(gs_conn,uid)
                                    cib_tablespace(gs_conn,uid)
                                    pgxc_node_env(gs_conn)
            else:
                ip = dbInfo['target_ip']
                port = dbInfo['target_port']
                uid = get_uid_by_ip(pg, ip, port)
                global_config_settings(gs_conn, uid)
                cib_basic(gs_conn,uid)
                cib_parameters(gs_conn,uid)
                cib_extension(gs_conn,uid)
                cib_db(gs_conn,uid)
                cib_tablespace(gs_conn,uid)
                pgxc_node_env(gs_conn)
    print(global_metric)

#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@文件    :cib_shentong.py
@说明    :神通数据库CIB采集
@时间    :2023/09/14 09:46:47
@作者    :xxxx
@版本    :2.0.1
'''
import os
import sys
import json
sys.path.append('/usr/software/knowl')
import DBUtil


def cs(val, dt=False):
    if val is None:
        return ''
    else:
        if dt:
            return val.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return str(val)
        

def cib_database(st, metric):
    sql = "select dbid,name,resetlogs_change#,log_mode,database_role,force_logging,supplemental_log_data_min,DB_UNIQUE_NAME,platform_name,to_char(created,'yyyy-mm-dd hh24:mi:ss'),ROUND(TOTAL_SIZE/1024/1024,2) from v$database"
    vals = []
    cursor = DBUtil.getValue(st, sql)
    rs = cursor.fetchall()
    for row in rs:
        dbid = row[0]
        inc = row[2]
        dbname = row[7]
        role = row[4]
        arch = row[3]
        vals.append(dict(name="dbid", value=dbid))
        vals.append(dict(name="db_name", value=row[1]))
        vals.append(dict(name="resetlogs_change", value=inc))
        vals.append(dict(name="log_mode", value=arch))
        vals.append(dict(name="database_role", value=role))
        vals.append(dict(name="force_logging", value=row[5]))
        vals.append(dict(name="supplemental_log_data_min", value=row[6]))
        vals.append(dict(name="db_unique_name", value=dbname))
        vals.append(dict(name="platform_name", value=row[8]))
        vals.append(dict(name="created_time", value=row[9]))
        vals.append(dict(name="total_size", value=row[10]))
    sql2 = "select host_name,instance_name,instance_number,VERSION, parallel,to_char(startup_time,'yyyy-mm-dd hh24:mi:ss') from v$instance"
    cursor2 = DBUtil.getValue(st, sql2)
    rs2 = cursor2.fetchall()
    for row in rs2:
        vals.append(dict(name="host_name", value=row[0]))
        vals.append(dict(name="instance_name", value=row[1]))
        vals.append(dict(name="instance_number", value=row[2]))
        vals.append(dict(name="version", value=row[3]))
        vals.append(dict(name="parallel", value=row[4]))
        vals.append(dict(name="startup_time", value=row[5]))
    # 归档目录
    sql3 = "select archivepath from v_sys_database_info"
    cursor3 = DBUtil.getValue(st, sql3)
    rs3 = cursor3.fetchall()
    for row in rs3:
        vals.append(dict(name="archivepath", value=row[0]))
    metric.append(dict(index_id="2370001", value=vals))


def cib_logfile(st, metric):
    sql = 'select group#,status,type,member,IS_RECOVERY_DEST_FILE from v$logfile order by group#'
    cursor = DBUtil.getValue(st, sql)
    rs = cursor.fetchall()
    vals = []
    vals.append(dict(c1='组号', c2='状态', c3='类型', c4='成员', c5='恢复区', c6=None, c7=None, c8=None, c9=None, c10=None))
    for row in rs:
        vals.append(
            dict(c1=cs(row[0]), c2=row[1], c3=row[2], c4=row[3], c5=cs(row[4]), c6=None, c7=None, c8=None, c9=None,
                    c10=None))
    metric.append(dict(index_id="2370002",  content=vals))

        
def cib_datafile(st, metric):
    sql = 'select file_name,file_id,tablespace_name,round(bytes/1024/1024,2),status,autoextensible,round(MAXBYTES/1024/1024,2) from dba_data_files order by file_id'
    vals = []
    vals.append(
        dict(c1='文件名', c2='文件编号', c3='表空间名', c4='文件大小(MB)', c5='状态', c6='是否自动扩展', c7='最大大小(MB)', c8=None, c9=None,
                c10=None))
    cursor = DBUtil.getValue(st, sql)
    rs = cursor.fetchall()
    for row in rs:
        vals.append(
            dict(c1=row[0], c2=cs(row[1]), c3=row[2], c4=cs(row[3]), c5=row[4], c6=row[5], c7=cs(row[6]), c8=None,
                    c9=None, c10=None))
    metric.append(dict(index_id="2370003", content=vals))


def cib_tbs(st, metric):
    tss = {}
    sql = 'select tablespace_name,status,contents,extent_management,allocation_type,segment_space_management,bigfile from dba_tablespaces order by tablespace_name'
    cursor = DBUtil.getValue(st, sql)
    rs = cursor.fetchall()
    vals = []
    vals.append(
        dict(c1='表空间名', c2='状态', c3='类型', c4='空间管理方式', c5='分配类型', c6='段空间管理方式', c7='是否为大文件', c8='当前大小(MB)', c9='使用率', c10=''))
    for row in rs:
        ts = tss.get(row[0])
        if ts:
            sz = ts[3]
            pct = ts[0]
        else:
            sz = None
            pct = None
        vals.append(dict(c1=row[0], c2=row[1], c3=row[2], c4=row[3], c5=row[4], c6=row[5], c7=cs(row[6]), c8=sz, c9=pct, c10=None))
    metric.append(dict(index_id="2370004", content=vals))


def cib_param(st, metric):
    sql = "select name,value from v$parameter where isdefault='FALSE' or isbasic='TRUE'"
    cursor = DBUtil.getValue(st, sql)
    rs = cursor.fetchall()
    vals = []
    for row in rs:
        vals.append(dict(name=row[0], value=cs(row[1])))
    metric.append(dict(index_id="2370005", value=vals))


def cib_schema(st, metric):
    sql = """
    select USENAME, sum(size) / 1024.0 / 1024 total_MB
    from sys_class, v_segment_info, sys_shadow
    where relid = oid
    and USESYSID = RELOWNER
    group by RELOWNER, USENAME
    """
    vals = []
    vals.append(
        dict(c1='用户名', c2='数据大小(MB)', c3=None, c4=None, c5=None, c6=None, c7=None, c8=None, c9=None,
                c10=None))
    cursor = DBUtil.getValue(st, sql)
    rs = cursor.fetchall()
    for row in rs:
        vals.append(
            dict(c1=row[0], c2=cs(row[1]), c3=None, c4=None, c5=None, c6=None, c7=None, c8=None,
                    c9=None, c10=None))
    metric.append(dict(index_id="2370006", content=vals))


def set_focus(conn, uid):
    try:
        # 增加数据文件路径
        sql = f"""
        select
            p.col1 file_path
        from
            mgt_system s,
            p_oracle_cib p
        where p.target_id = '{uid}'
            and p.index_id = 2370003
            and p.target_id = s.uid 
            and p.seq_id > 0
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
        except Exception:
            conn.conn.rollback()
    except Exception:
        return
    

if __name__ == '__main__':
    dbInfo = eval(sys.argv[1])
    target_id, pg = DBUtil.get_pg_env(dbInfo, 0)
    st = DBUtil.get_shentong_env(exflag=3)
    target_ip = dbInfo['target_ip']
    metric = []
    if st.conn:
        cib_database(st, metric)
        cib_logfile(st, metric)
        cib_datafile(st, metric)
        cib_tbs(st, metric)
        cib_param(st, metric)
        cib_schema(st, metric)
        set_focus(pg, target_id)
    print('{"cib":' + json.dumps(metric) + '}')
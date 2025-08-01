#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@文件    :cib_yashan.py
@说明    :神通数据库CIB采集
@时间    :2023/11/02 11:11:06
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
    sql = """
    SELECT
        database_id,
        database_name,
        to_char(create_time, 'yyyy-mm-dd hh24:mi:ss') ,
        log_mode,
        protection_mode,
        database_role,
        block_size,
        reset_point,
        platform_name
    FROM
        v$database
        """
    vals = []
    cursor = DBUtil.getValue(st, sql)
    rs = cursor.fetchall()
    for row in rs:
        database_id,database_name,create_time ,log_mode,protection_mode,database_role,block_size,reset_point,platform_name = row
        vals.append(dict(name="dbid", value=database_id))
        vals.append(dict(name="db_name", value=database_name))
        vals.append(dict(name="reset_point", value=reset_point))
        vals.append(dict(name="log_mode", value=log_mode))
        vals.append(dict(name="database_role", value=database_role))
        vals.append(dict(name="protection_mode", value=protection_mode))
        vals.append(dict(name="block_size", value=block_size))
        vals.append(dict(name="platform_name", value=platform_name))
        vals.append(dict(name="created_time", value=create_time))
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
    metric.append(dict(index_id="2410001", value=vals))


def cib_logfile(st, metric):
    sql = 'SELECT * FROM v$logfile'
    cursor = DBUtil.getValue(st, sql)
    rs = cursor.fetchall()
    vals = []
    vals.append(dict(c1='线程号', c2='序号', c3='名称', c4='块大小', c5='总块数', c6='已使用块数', c7='序列号', c8='状态', c9=None, c10=None))
    for row in rs:
        vals.append(
                dict(c1=cs(row[0]), c2=row[1], c3=row[2], c4=row[3], c5=cs(row[4]), c6=cs(row[5]), c7=cs(row[6]), c8=cs(row[7]), c9=None,
                    c10=None))
    metric.append(dict(index_id="2410002",  content=vals))

        
def cib_datafile(st, metric):
    sql = 'select file_name,file_id,tablespace_name,round(bytes/1024/1024,2),status,AUTO_EXTEND,round(MAXBYTES/1024/1024,2) from dba_data_files order by file_id'
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
    metric.append(dict(index_id="2410003", content=vals))


def cib_tbs(st, metric):
    tss = {}
    sql = 'select tablespace_name,status,contents,LOGGING,allocation_type,segment_space_management,COMPRESSED from dba_tablespaces order by tablespace_name'
    cursor = DBUtil.getValue(st, sql)
    rs = cursor.fetchall()
    vals = []
    vals.append(
        dict(c1='表空间名', c2='状态', c3='类型', c4='是否记录日志', c5='分配方式', c6='段空间管理方式', c7='是否压缩', c8='当前大小(MB)', c9='使用率', c10=''))
    for row in rs:
        ts = tss.get(row[0])
        if ts:
            sz = ts[3]
            pct = ts[0]
        else:
            sz = None
            pct = None
        vals.append(dict(c1=row[0], c2=row[1], c3=row[2], c4=row[3], c5=row[4], c6=row[5], c7=cs(row[6]), c8=sz, c9=pct, c10=None))
    metric.append(dict(index_id="2410004", content=vals))


def cib_param(st, metric):
    sql = "select name,value from v$parameter"
    cursor = DBUtil.getValue(st, sql)
    rs = cursor.fetchall()
    vals = []
    for row in rs:
        vals.append(dict(name=row[0], value=cs(row[1])))
    metric.append(dict(index_id="2410005", value=vals))


def cib_schema(st, metric):
    sql = """
    SELECT
        owner,
        round(sum(bytes)/ 1024 / 1024, 2) AS size_mb
    FROM
        dba_segments
    GROUP BY
        owner
    ORDER BY
        2 DESC
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
    metric.append(dict(index_id="2410006", content=vals))


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
            and p.index_id = 2410003
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
    st = DBUtil.get_yashan_env(exflag=3)
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
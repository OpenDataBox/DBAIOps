#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys

sys.path.append('/usr/software/knowl')
import DBUtil
import re


def robust(actual_do):
    def add_robust(*args, **keyargs):
        try:
            return actual_do(*args, **keyargs)
        except Exception as e:
            print('Error execute: %s' % actual_do.__name__)
            print(e)
            upthcrunstastus(pg, checkId, 1, 1)

    return add_robust


@robust
def checkuserpass(conn, conn_pg, check_id):
    sql = '''
select r.username, r.account_status, r.profile
  from dba_users r
 where r.account_status = 'OPEN' and r.profile <> 'DICT_PROFILE' and r.username not in ('SYS','SYSTEM')'''
    cursor = DBUtil.getValue(conn, sql)
    res = cursor.fetchall()
    adds = ''
    # print(res)
    if res:
        adds += "用户名%a%用户状态%a%用户PROFILE文件#"
        for row in res:
            adds += row[0] + '%a%' + row[1] + '%a%' + row[2] + "#"
    # print(adds)
    if adds:
        result = '异常'
    else:
        result = '正常'
        if "'" in sql:
            sql = sql.replace("'", "''")
        adds = sql.strip() + '\n' + '-' * 50 + '\nno rows selected%a%'
    sql = '''
insert into hd_check_log_detail(hd_check_id,tab_no,item_seq,item_desc,item_result,item_err) 
values('{0}',1,1,'账号密码检查','{1}','{2}')'''.format(check_id, result, adds)
    conn_pg.execute(sql)


@robust
def checklock(conn, conn_pg, check_id):
    sql = '''
    select to_char(y.sample_time,'yyyy-mm-dd hh24:mi:ssxff') sample_time, count(1) from dba_hist_active_sess_history y where y.event in (
    select d.NAME from v$event_name d where d.NAME like '%contention'
    ) and y.sample_time > trunc(sysdate)
    group by y.sample_time
    having count(1)>30'''
    cursor = DBUtil.getValue(conn, sql)
    res = cursor.fetchall()
    adds = ''
    # print(res)
    if res:
        adds += "采样时间%a%锁数量#"
        for row in res:
            adds += row[0] + '%a%' + str(row[1]) + "#"
    # print(adds)
    if adds:
        result = '异常'
    else:
        result = '正常'
        if "'" in sql:
            sql = sql.replace("'", "''")
        adds = sql.strip() + '\n' + '-' * 50 + '\nno rows selected%a%'
    sql = '''
    insert into hd_check_log_detail(hd_check_id,tab_no,item_seq,item_desc,item_result,item_err) 
    values('{0}',1,2,'数据库锁检查','{1}','{2}')'''.format(check_id, result, adds)
    conn_pg.execute(sql)


@robust
def checkfileio(conn, conn_pg, check_id):
    sql = '''
select tsname,atpr "Av Rd(ms)" from (
select e.tsname tsname,
       decode(sum(e.phyrds - nvl(b.phyrds, 0)),
              0,
              0,
              10 * (sum(e.readtim - nvl(b.readtim, 0)) /
              sum(e.phyrds - nvl(b.phyrds, 0)))) atpr
  from dba_hist_filestatxs e, dba_hist_filestatxs b,( select 
 (select max(t.snap_id)   from dba_hist_snapshot t where t.begin_interval_time<=trunc(sysdate-1)+10.1/24 ) snap_id,(select dbid from v$database where rownum=1) dbid,
 (select instance_number from v$instance where rownum=1) inst_id
from dual) c
 where b.snap_id(+) = e.snap_id-1
   and e.snap_id = c.snap_id
   and b.dbid = e.dbid
   and e.dbid = c.dbid
   and b.dbid(+) = e.dbid
   and b.instance_number = e.instance_number
   and e.instance_number = c.inst_id
   and b.instance_number = e.instance_number
   and b.tsname(+) = e.tsname
   and b.file#(+) = e.file#
   and b.creation_change#(+) = e.creation_change#
   and ((e.phyrds - nvl(b.phyrds, 0)) + (e.phywrts - nvl(b.phywrts, 0))) > 0
 group by e.tsname
 ) where atpr>20'''
    cursor = DBUtil.getValue(conn, sql)
    res = cursor.fetchall()

    adds = ''
    # print(res)
    if res:
        adds += "表空间%a%平均读时间(ms)#"
        for row in res:
            adds += row[0] + '%a%' + str(row[1]) + "#"
    # print(adds)
    if adds:
        result = '异常'
    else:
        result = '正常'
        if "'" in sql:
            sql = sql.replace("'", "''")
        adds = sql.strip() + '\n' + '-' * 50 + '\nno rows selected%a%'
    sql = '''
    insert into hd_check_log_detail(hd_check_id,tab_no,item_seq,item_desc,item_result,item_err) 
    values('{0}',1,3,'系统读性能检查','{1}','{2}')'''.format(check_id, result, adds)
    conn_pg.execute(sql)


@robust
def checkdiagused(ssh, location, conn, check_id, hd_cc):
    cmd = '"' + hd_cc + " " + location + '"'
    res = ssh.openCmd(cmd).strip().split('\n')
    adds = ''

    if "No such file or directory" in res[0]:
        adds = res[0]
    for row in res:
        if "Filesystem" not in row:
            row = row.split()
            if row[5] in location:
                used = row[4].replace('%', '')
                if int(used) > 90:
                    adds = row + "#"

    if adds:
        result = '异常'
        if "No such file or directory" not in adds:
            adds = "Filesystem%a%Size%a%Used%a%Avail%a%Use%%a%Mounted on#" + adds
    else:
        for row in res:
            adds += row + '\n'
        adds = adds.strip()
        result = '正常'
    sql = '''
       insert into hd_check_log_detail(hd_check_id,tab_no,item_seq,item_desc,item_result,item_err) 
       values('{0}',1,4,'oracle trace目录空间检查','{1}','{2}')'''.format(check_id, result, adds)
    conn.execute(sql)


@robust
def checktsused(conn, conn_pg, check_id):
    sql = '''
SELECT A.TABLESPACE_NAME "表空间名称",
       100 - ROUND((NVL(B.BYTES_FREE, 0) / A.BYTES_ALLOC) * 100, 2) || '%' "使用率(%)",
       ROUND(NVL(B.BYTES_FREE, 0) / 1024 / 1024 / 1024, 2) "空闲(G)",
       ROUND(A.BYTES_ALLOC / 1024 / 1024 / 1024, 2) "容量(G)",
       ROUND((A.BYTES_ALLOC - NVL(B.BYTES_FREE, 0)) / 1024 / 1024 / 1024, 2) "使用(G)",
       ROUND((NVL(B.BYTES_FREE, 0) / A.BYTES_ALLOC) * 100, 2) "空闲率(%)",
       TO_CHAR(SYSDATE, 'YYYY-MM-DD HH24:MI:SS') "采样时间"
  FROM (SELECT F.TABLESPACE_NAME, SUM(F.BYTES) BYTES_ALLOC
          FROM DBA_DATA_FILES F
         GROUP BY TABLESPACE_NAME) A,
       (SELECT F.TABLESPACE_NAME, SUM(F.BYTES) BYTES_FREE
          FROM DBA_FREE_SPACE F
         GROUP BY TABLESPACE_NAME) B
 WHERE A.TABLESPACE_NAME = B.TABLESPACE_NAME(+) and 100 - ROUND((NVL(B.BYTES_FREE, 0) / A.BYTES_ALLOC) * 100, 2)>=95'''
    cursor = DBUtil.getValue(conn, sql)
    res = cursor.fetchall()

    adds = ''
    # print(res)
    if res:
        for row in res:
            if float(row[1].replace('%', '')) > 95:
                adds += row[0] + '%a%' + row[1] + '%a%' + str(row[2]) + '%a%' + str(row[3]) + '%a%' + str(
                    row[4]) + '%a%' + str(row[5]) + '%a%' + row[6] + "#"
    # print(adds)
    if adds:
        result = '异常'
        adds = "表空间%a%使用率(%)%a%空闲(G)%a%容量(G)%a%使用(G)%a%空闲率(%)%a%采样时间#" + adds
    else:
        if "'" in sql:
            sql = sql.replace("'", "''")
        adds = sql.strip() + '\n' + '-' * 50 + '\nno rows selected%a%'
        result = '正常'
    sql = '''
    insert into hd_check_log_detail(hd_check_id,tab_no,item_seq,item_desc,item_result,item_err) 
    values('{0}',1,5,'表空间使用率检查','{1}','{2}')'''.format(check_id, result, adds)
    conn_pg.execute(sql)


@robust
def checktabused(conn, conn_pg, check_id):
    sql = '''
select "OWNER",
       "TABLE_NAME" 表名,
       "PARTITIONED" 是否分区表,
       round("SPACE_PCT", 3) 空间利用率,
       round("SIZEG", 3) 实际大小GB,
       "NUM_ROWS" 记录数,
       "ROW_NUMPG" 每G存放记录数,
       "AVG_ROW_LEN" 每条记录长度,
       "LAST_ANALYZED" 最后分析时间
  from (select a.owner, --用户名
               a.table_name, --表名
               a.num_rows * a.avg_row_len / 1024 / 1024 / 1024 mabesizeg,
               a.blocks * 8 / 1024 / 1024 sizeg, --表大小
               a.num_rows, --表中记录数
               trunc(a.num_rows / (a.blocks * 8 / 1024 / 1024)) row_numpg, --平均每g空间存放记录数
               a.avg_row_len,
               a.num_rows * a.avg_row_len / (a.blocks * 8 * 1024) * 100 space_pct,
               a.empty_blocks,
               a.partitioned,
               a.last_analyzed
          from dba_tables a
         where a.num_rows > 0
           and partitioned= 'NO'
           and a.blocks > 64000
           and owner not in ('SYS', 'SYSTEM', 'SYSMAN'))
 where space_pct <= 20
 order by space_pct'''
    cursor = DBUtil.getValue(conn, sql)
    res = cursor.fetchall()

    adds = ''
    # print(res)
    if res:
        adds += "用户名%a%表名%a%是否分区表%a%空间利率率%a%实际大小(GB)%a%记录数%a%每G存放记录数%a%每条记录长度%a%最后分析时间#"
        for row in res:
            adds += row[0] + '%a%' + row[1] + '%a%' + str(row[2]) + '%a%' + str(row[3]) + '%a%' + str(
                row[4]) + '%a%' + str(row[5]) + '%a%' + \
                    str(row[6]) + '%a%' + str(row[7]) + '%a%' + str(row[8]) + "#"
    # print(adds)
    if adds:
        result = '异常'
    else:
        if "'" in sql:
            sql = sql.replace("'", "''")
        adds = sql.strip() + '\n' + '-' * 50 + '\nno rows selected%a%'
        result = '正常'
    sql = '''
    insert into hd_check_log_detail(hd_check_id,tab_no,item_seq,item_desc,item_result,item_err) 
    values('{0}',1,6,'普通表碎片检查','{1}','{2}')'''.format(check_id, result, adds)
    conn_pg.execute(sql)

    sql1 = '''
select "TABLE_OWNER",
       "TABLE_NAME" 表名,
       "PARTITION_NAME" 分区名,
       round("SPACE_PCT", 3) 空间利用率,
       round("SIZEG", 3) 实际大小GB,
       "NUM_ROWS" 记录数,
       "ROW_NUMPG" 每G存放记录数,
       "AVG_ROW_LEN" 每条记录长度,
       "LAST_ANALYZED" 最后分析时间
  from (select a.table_owner, --用户名
               a.table_name, --表名
               a.partition_name, --分区名
               a.num_rows * a.avg_row_len / 1024 / 1024 / 1024 mabesizeg,
               a.blocks * 8 / 1024 / 1024 sizeg, --表大小
               a.num_rows, --表中记录数
               trunc(a.num_rows / (a.blocks * 8 / 1024 / 1024)) row_numpg, --平均每g空间存放记录数
               a.avg_row_len,
               a.num_rows * a.avg_row_len / (a.blocks * 8 * 1024) * 100 space_pct,
               a.empty_blocks,
               a.last_analyzed
          from dba_tab_partitions a 
         where a.num_rows > 0
          and subpartition_count=0 
           and a.blocks > 25000
           and subpartition_count =0
           and table_owner not in ('SYS', 'SYSTEM', 'SYSMAN'))           
 where space_pct <= 20
 order by space_pct'''
    cursor1 = DBUtil.getValue(conn, sql1)
    res1 = cursor1.fetchall()

    adds = ''
    # print(res)
    if res1:
        adds += "用户名%a%表名%a%是否分区表%a%空间利率率%a%实际大小(GB)%a%记录数%a%每G存放记录数%a%每条记录长度%a%最后分析时间#"
        for row in res1:
            adds += row[0] + '%a%' + row[1] + '%a%' + str(row[2]) + '%a%' + str(row[3]) + '%a%' + str(
                row[4]) + '%a%' + str(row[5]) + '%a%' + \
                    str(row[6]) + '%a%' + str(row[7]) + '%a%' + str(row[8]) + "#"
    # print(adds)
    if adds:
        result = '异常'
    else:
        result = '正常'
    sql1 = '''
    insert into hd_check_log_detail(hd_check_id,tab_no,item_seq,item_desc,item_result,item_err) 
    values('{0}',1,7,'一级分区表碎片检查','{1}','{2}')'''.format(check_id, result, adds)
    conn_pg.execute(sql1)

    sql2 = '''
select "TABLE_OWNER",
       "TABLE_NAME" 表名,
       "SUBPARTITION_NAME" 分区名,
       round("SPACE_PCT", 3) 空间利用率,
       round("SIZEG", 3) 实际大小GB,
       "NUM_ROWS" 记录数,
       "ROW_NUMPG" 每G存放记录数,
       "AVG_ROW_LEN" 每条记录长度,
       "LAST_ANALYZED" 最后分析时间
  from (select a.table_owner, --用户名
               a.table_name, --表名
               a.subpartition_name, --分区名
               a.num_rows * a.avg_row_len / 1024 / 1024 / 1024 mabesizeg,
               a.blocks * 8 / 1024 / 1024 sizeg, --表大小
               a.num_rows, --表中记录数
               trunc(a.num_rows / (a.blocks * 8 / 1024 / 1024)) row_numpg, --平均每g空间存放记录数
               a.avg_row_len,
               a.num_rows * a.avg_row_len / (a.blocks * 8 * 1024) * 100 space_pct,
               a.empty_blocks,
               a.last_analyzed
          from dba_tab_subpartitions a 
         where a.num_rows > 0
           and a.blocks > 12500
           and table_owner not in ('SYS', 'SYSTEM', 'SYSMAN'))           
 where space_pct <= 20
 order by space_pct'''
    cursor2 = DBUtil.getValue(conn, sql2)
    res2 = cursor2.fetchall()

    adds = ''
    # print(res)
    if res2:
        adds += "用户名%a%表名%a%是否分区表%a%空间利率率%a%实际大小(GB)%a%记录数%a%每G存放记录数%a%每条记录长度%a%最后分析时间#"
        for row in res2:
            adds += row[0] + '%a%' + row[1] + '%a%' + str(row[2]) + '%a%' + str(row[3]) + '%a%' + str(
                row[4]) + '%a%' + str(row[5]) + '%a%' + \
                    str(row[6]) + '%a%' + str(row[7]) + '%a%' + str(row[8]) + "#"
    # print(adds)
    if adds:
        result = '异常'
    else:
        result = '正常'
    sql2 = '''
    insert into hd_check_log_detail(hd_check_id,tab_no,item_seq,item_desc,item_result,item_err) 
    values('{0}',1,8,'二级分区表碎片检查','{1}','{2}')'''.format(check_id, result, adds)
    conn_pg.execute(sql2)


@robust
def checkuserpriv(conn, conn_pg, check_id):
    sql = '''
 select grantee,granted_role,admin_option,default_role from dba_role_privs t where t.GRANTED_ROLE='DBA' and t.GRANTEE not in('SYSTEM','SYSODM','SYS','SYSMAN')
and exists(
select 1 from dba_users r where r.username = t.GRANTEE and r.account_status='OPEN')'''
    cursor = DBUtil.getValue(conn, sql)
    res = cursor.fetchall()

    adds = ''
    # print(res)
    if res:
        adds += "用户%a%被授权角色%a%是否可继承%a%是否为默认角色#"
        for row in res:
            adds += row[0] + '%a%' + row[1] + '%a%' + str(row[2]) + '%a%' + str(row[3]) + "#"
    # print(adds)
    if adds:
        result = '异常'
    else:
        if "'" in sql:
            sql = sql.replace("'", "''")
        adds = sql.strip() + '\n' + '-' * 50 + '\nno rows selected%a%'
        result = '正常'
    sql = '''
    insert into hd_check_log_detail(hd_check_id,tab_no,item_seq,item_desc,item_result,item_err) 
    values('{0}',1,6,'用户业务权限检查','{1}','{2}')'''.format(check_id, result, adds)
    conn_pg.execute(sql)


@robust
def checkarchinuse(conn, conn_pg, check_id):
    sql = '''
select LOG_MODE from v$database where log_mode<>'ARCHIVELOG' '''
    cursor = DBUtil.getValue(conn, sql)
    res = cursor.fetchone()

    adds = ''
    # print(res)
    if res:
        adds += "归档模式#"
        adds += res[0] + "#"
    # print(adds)
    if adds:
        result = '异常'
    else:
        result = '正常'
        if "'" in sql:
            sql = sql.replace("'", "''")
        adds = sql.strip() + '\n' + '-' * 50 + '\nno rows selected%a%'
    sql = '''
    insert into hd_check_log_detail(hd_check_id,tab_no,item_seq,item_desc,item_result,item_err) 
    values('{0}',1,7,'数据库归档模式检查','{1}','{2}')'''.format(check_id, result, adds)
    conn_pg.execute(sql)


@robust
def checkactivesess(conn, conn_pg, check_id):
    sql = '''
select to_char(y.sample_time, 'yyyy-mm-dd hh24:mi:ssxff') s_time, count(1) s_cnt
  from dba_hist_active_sess_history y
 where y.sample_time > trunc(sysdate)
 group by y.sample_time
having count(1) > 100'''
    cursor = DBUtil.getValue(conn, sql)
    res = cursor.fetchall()

    adds = ''
    # print(res)
    if res:
        adds += "采样时间%a%会话数量#"
        for row in res:
            adds += row[0] + '%a%' + str(row[1]) + "#"
    # print(adds)
    if adds:
        result = '异常'
    else:
        result = '正常'
        if "'" in sql:
            sql = sql.replace("'", "''")
        adds = sql.strip() + '\n' + '-' * 50 + '\nno rows selected%a%'
    sql = '''
    insert into hd_check_log_detail(hd_check_id,tab_no,item_seq,item_desc,item_result,item_err) 
    values('{0}',1,8,'在线活动进程检查','{1}','{2}')'''.format(check_id, result, adds)
    conn_pg.execute(sql)


@robust
def checkredolog(conn, conn_pg, check_id):
    sql = '''
select g.THREAD#,count(1) from v$log g group by g.THREAD# having count(1) <6'''
    cursor = DBUtil.getValue(conn, sql)
    res = cursor.fetchall()

    adds = ''
    # print(res)
    if res:
        adds += "线程号%a%日志组数量#"
        for row in res:
            adds += str(row[0]) + '%a%' + str(row[1]) + "#"
    # print(adds)
    if adds:
        result = '异常'
    else:
        result = '正常'
        if "'" in sql:
            sql = sql.replace("'", "''")
        adds = sql.strip() + '\n' + '-' * 50 + '\nno rows selected%a%'
    sql = '''
    insert into hd_check_log_detail(hd_check_id,tab_no,item_seq,item_desc,item_result,item_err) 
    values('{0}',1,12,'线程日志组数量检查','{1}','{2}')'''.format(check_id, result, adds)
    conn_pg.execute(sql)

    sql1 = '''
select group#,thread#,round(bytes/1024/1204,2) suze_m,members,ARCHIVED,STATUS from v$log g where bytes/1024/1204<500'''
    cursor1 = DBUtil.getValue(conn, sql1)
    res1 = cursor1.fetchall()

    adds = ''
    # print(res)
    if res1:
        adds += "日志组号%a%线程号%a%日志大小(M)%a%成员数量%a%是否归档%a%日志状态#"
        for row in res1:
            # print(row)
            adds += str(row[0]) + '%a%' + str(row[1]) + '%a%' + str(row[2]) + '%a%' + str(row[3]) + '%a%' + row[
                4] + '%a%' + row[5] + "#"
    # print(adds)
    if adds:
        result = '异常'
    else:
        result = '正常'
        if "'" in sql1:
            sql1 = sql1.replace("'", "''")
        adds = sql1.strip() + '\n' + '-' * 50 + '\nno rows selected%a%'
    sql1 = '''
    insert into hd_check_log_detail(hd_check_id,tab_no,item_seq,item_desc,item_result,item_err) 
    values('{0}',1,9,'重做日志大小检查','{1}','{2}')'''.format(check_id, result, adds)
    print(sql1)
    conn_pg.execute(sql1)


@robust
def checkmemorymanager(conn, conn_pg, check_id):
    sql = '''
select name,value from v$parameter where name='memory_target' and value<>'0' '''
    cursor = DBUtil.getValue(conn, sql)
    res = cursor.fetchall()

    adds = ''
    # print(res)
    if res:
        adds += "参数名称%a%参数值#"
        for row in res:
            adds += row[0] + +row[1] + "#"
    # print(adds)
    if adds:
        result = '异常'
    else:
        result = '正常'
        if "'" in sql:
            sql = sql.replace("'", "''")
        adds = sql.strip() + '\n' + '-' * 50 + '\nno rows selected%a%'
    sql = '''
    insert into hd_check_log_detail(hd_check_id,tab_no,item_seq,item_desc,item_result,item_err) 
    values('{0}',1,10,'数据库内存管理方式检查','{1}','{2}')'''.format(check_id, result, adds)
    conn_pg.execute(sql)


@robust
def checkcursorpara(conn, conn_pg, check_id):
    alertlist = []
    sql = '''
select t.NAME,t.VALUE,'正常:>=200'  from v$parameter t where t.NAME ='session_cached_cursors'
union
select t.NAME,t.VALUE,'正常:>=200'  from v$parameter t where t.NAME ='open_cursors'
union
select t.NAME,t.VALUE,'正常:>=500'  from v$parameter t where t.NAME ='processes'
union
select t.NAME,t.VALUE,'正常:>=2000'  from v$parameter t where t.NAME ='db_files'
union
select t.NAME,t.VALUE,'正常:>=10800' from v$parameter t where t.NAME ='undo_retention' '''
    cursor = DBUtil.getValue(conn, sql)
    res = cursor.fetchall()

    adds = ''
    for row in res:
        if row[0] == "db_files":
            if int(row[1]) < 2000:
                adds += row[0] + '%a%' + row[1] + "#"
        if row[0] == "open_cursors":
            if int(row[1]) < 200:
                adds += row[0] + '%a%' + row[1] + "#"
        if row[0] == "processes":
            if int(row[1]) < 500:
                adds += row[0] + '%a%' + row[1] + "#"
        if row[0] == "session_cached_cursors":
            if int(row[1]) < 200:
                adds += row[0] + '%a%' + row[1] + "#"
        if row[0] == "undo_retention":
            if int(row[1]) < 10800:
                adds += row[0] + '%a%' + row[1] + "#"

    if adds:
        result = '异常'
        adds = "参数名%a%参数值#" + adds
    else:
        result = '正常'
        if "'" in sql:
            sql = sql.replace("'", "''")
        adds = sql.strip() + '\n' + '-' * 50 + '\nno rows selected%a%'
    sql = '''
    insert into hd_check_log_detail(hd_check_id,tab_no,item_seq,item_desc,item_result,item_err) 
    values('{0}',1,11,'会话缓存游标参数检查','{1}','{2}')'''.format(check_id, result, adds)
    conn_pg.execute(sql)


@robust
def checkautospaceadv(conn, conn_pg, check_id):
    sql = '''
select client_name,status from dba_autotask_client where client_name='auto space advisor' and status='ENABLED' '''
    cursor = DBUtil.getValue(conn, sql)
    res = cursor.fetchall()

    adds = ''
    # print(res)
    if res:
        adds += "自动任务名称%a%是否启用#"
        for row in res:
            adds += row[0] + '%a%' + row[1] + "#"
    # print(adds)
    if adds:
        result = '异常'
    else:
        result = '正常'
        if "'" in sql:
            sql = sql.replace("'", "''")
        adds = sql.strip() + '\n' + '-' * 50 + '\nno rows selected%a%'
    sql = '''
    insert into hd_check_log_detail(hd_check_id,tab_no,item_seq,item_desc,item_result,item_err) 
    values('{0}',1,12,'停用自动维护任务检查','{1}','{2}')'''.format(check_id, result, adds)
    conn_pg.execute(sql)


@robust
def checkhiddenpara(conn, conn_pg, check_id):
    sql = '''
select nam.ksppinm name,val.ksppstvl value from sys.x_$ksppi nam,sys.x_$ksppcv val where nam.indx=val.indx and nam.ksppinm = '_gc_undo_affinity' and val.ksppstvl<>'FALSE'
union 
select nam.ksppinm name,val.ksppstvl value from sys.x_$ksppi nam,sys.x_$ksppcv val where nam.indx=val.indx and nam.ksppinm = '_gc_policy_time' and val.ksppstvl<>'0'
union 
select nam.ksppinm name,val.ksppstvl value from sys.x_$ksppi nam,sys.x_$ksppcv val where nam.indx=val.indx and nam.ksppinm = '_optimizer_extended_cursor_sharing' and val.ksppstvl<>'NONE'
union 
select nam.ksppinm name,val.ksppstvl value from sys.x_$ksppi nam,sys.x_$ksppcv val where nam.indx=val.indx and nam.ksppinm = '_optimizer_extended_cursor_sharing_rel' and val.ksppstvl<>'NONE'
union 
select nam.ksppinm name,val.ksppstvl value from sys.x_$ksppi nam,sys.x_$ksppcv val where nam.indx=val.indx and nam.ksppinm = '_serial_direct_read' and val.ksppstvl not in ('NEVER','never')
'''
    cursor = DBUtil.getValue(conn, sql)
    res = cursor.fetchall()

    adds = ''
    # print(res)
    if res:
        adds += "参数名%a%参数值#"
        for row in res:
            adds += row[0] + '%a%' + row[1] + "#"
    # print(adds)
    if adds:
        result = '异常'
    else:
        result = '正常'
        if "'" in sql:
            sql = sql.replace("'", "''")
        adds = sql.strip() + '\n' + '-' * 50 + '\nno rows selected%a%'
    sql = '''
    insert into hd_check_log_detail(hd_check_id,tab_no,item_seq,item_desc,item_result,item_err) 
    values('{0}',1,13,'数据库隐含参数检查','{1}','{2}')'''.format(check_id, result, adds)
    conn_pg.execute(sql)


@robust
def checknormalpara(conn, conn_pg, check_id):
    sql = '''
select t.NAME,t.VALUE from v$parameter t where t.NAME ='parallel_force_local' and t.VALUE<>'TRUE'
union
select t.NAME,t.VALUE from v$parameter t where t.NAME ='recyclebin' and t.VALUE<>'OFF'
union
select t.NAME,t.VALUE from v$parameter t where t.NAME ='audit_trail' and t.VALUE<>'NONE' '''
    cursor = DBUtil.getValue(conn, sql)
    res = cursor.fetchall()

    adds = ''
    # print(res)
    if res:
        adds += "参数名%a%参数值#"
        for row in res:
            adds += row[0] + '%a%' + row[1] + "#"
    # print(adds)
    if adds:
        result = '异常'
    else:
        result = '正常'
        if "'" in sql:
            sql = sql.replace("'", "''")
        adds = sql.strip() + '\n' + '-' * 50 + '\nno rows selected%a%'
    sql = '''
    insert into hd_check_log_detail(hd_check_id,tab_no,item_seq,item_desc,item_result,item_err) 
    values('{0}',1,14,'并行参数、回收站、审计参数检查','{1}','{2}')'''.format(check_id, result, adds)
    conn_pg.execute(sql)


@robust
def checkoggkeeptime(ssh, location, conn, check_id, profile):
    cmd = ''' 'source ~/''' + profile + ''';echo "view param mgr"|''' + location + "/ggsci'"
    # print(cmd)
    res = ssh.openCmd(cmd).split('\n')
    adds = ''
    for row in res:
        if 'minkeep' in row:
            row = row.split(',')
            for item in row:
                if 'minkeep' in item:
                    item = item.split()
                    if item[0] == 'minkeephours':
                        if int(item[1]) < 72:
                            adds = ','.join(row) + "#"
                    if item[0] == 'minkeepdays':
                        if int(item[1]) < 3:
                            adds += row + "#"
    if adds:
        result = '异常'
    else:
        result = '正常'
    sql = '''
    insert into hd_check_log_detail(hd_check_id,tab_no,item_seq,item_desc,item_result,item_err) 
    values('{0}',2,1,'ogg队列空间大小检查','{1}','{2}')'''.format(check_id, result, adds)
    conn.execute(sql)


@robust
def checkogglocused(ssh, location, conn, check_id, hd_cc):
    cmd = '"' + hd_cc + " " + location + '"'
    res = ssh.openCmd(cmd).strip().split('\n')
    adds = ''

    if "No such file or directory" in res[0]:
        adds = res[0]
    for row in res:
        if "Filesystem" not in row:
            row = row.split()
            if row[5] in location:
                used = row[4].replace('%', '')
                if int(used) > 90:
                    adds = row + "#"

    if adds:
        result = '异常'
        if "No such file or directory" not in adds:
            adds = "Filesystem%a%Size%a%Used%a%Avail%a%Use%%a%Mounted on#" + adds
    else:
        result = '正常'
    sql = '''
       insert into hd_check_log_detail(hd_check_id,tab_no,item_seq,item_desc,item_result,item_err) 
       values('{0}',2,2,'ogg部署目录空间检查','{1}','{2}')'''.format(check_id, result, adds)
    conn.execute(sql)


@robust
def checkoggprocstat(ssh, location, conn, check_id, profile, role="src"):
    cmd = ''' 'source ~/''' + profile + ''';echo "info all"|''' + location + "/ggsci'"
    res = ssh.openCmd(cmd)
    res = re.sub('\n\n', '\n', res).strip()
    pattern = r'(Program[\s\S]*)GGSCI'
    systemlist = ''.join(re.findall(pattern, res)).strip().split('\n')
    # print(systemlist)
    flag = 0
    adds = ''
    for row in systemlist:
        if "Program" not in row:
            row = row.split()
            if row[1] != "RUNNING":
                adds += "   ".join(row) + "#"
                flag = 1
    if flag == 0:
        if role == "src":
            result = "源端ogg进程运行正常"
        else:
            result = "目标端ogg进程运行正常"
    else:
        if role == "src":
            result = "源端ogg进程运行异常"
        else:
            result = "目标端ogg进程运行异常"
        adds = "Program%a%Status%a%Group%a%Lag at Chkpt%a%Time Since Chkpt#" + adds

    if role == "src":
        desc = "源端ogg进程状态检查"
        seq_id = 3
    else:
        desc = "目标端ogg进程状态检查"
        seq_id = 4

    sql = '''
       insert into hd_check_log_detail(hd_check_id,tab_no,item_seq,item_desc,item_result,item_err) 
       values('{0}',2,{1},'{2}','{3}','{4}')'''.format(check_id, seq_id, desc, result, adds)
    conn.execute(sql)


@robust
def checkoggdelay(ssh, location, conn, check_id, profile, role="src"):
    cmd = ''' 'source ~/''' + profile + ''';echo "info all"|''' + location + "/ggsci'"
    res = ssh.openCmd(cmd)
    res = re.sub('\n\n', '\n', res).strip()
    pattern = r'(Program[\s\S]*)GGSCI'
    systemlist = ''.join(re.findall(pattern, res)).strip().split('\n')
    # print(systemlist)
    flag = 0
    adds = ''
    for row in systemlist:
        if "Program" not in row:
            row = row.split()
            if row[0] != "MANAGER":
                time = row[4].split(':')
                if int(time[0]) > 0 or int(time[1]) >= 15:
                    adds += "  ".join(row) + "#"
                    flag = 1

    if flag == 0:
        if role == "src":
            result = "源端ogg进程同步正常"
        else:
            result = "目标端ogg进程同步正常"
    else:
        if role == "src":
            result = "源端ogg进程同步异常"
        else:
            result = "目标端ogg进程同步异常"
        adds = "Program%a%Status%a%Group%a%Lag at Chkpt%a%Time Since Chkpt#" + adds
    if role == "src":
        desc = "源端ogg进程延迟检查"
        seq_id = 5
    else:
        desc = "目标端ogg进程延迟检查"
        seq_id = 6

    sql = '''
       insert into hd_check_log_detail(hd_check_id,tab_no,item_seq,item_desc,item_result,item_err) 
       values('{0}',2,{1},'{2}','{3}','{4}')'''.format(check_id, seq_id, desc, result, adds)
    conn.execute(sql)


@robust
def upthcrunstastus(conn, check_id, runrs, chkrs):
    sql = '''update hd_check_log set run_status={0},check_result={1} where hd_check_id='{2}' '''.format(runrs, chkrs,
                                                                                                        check_id)
    conn.execute(sql)


# @robust
def uptcheckresult(conn, check_id):
    sql = ''' select count(*) from hd_check_log_detail where hd_check_id='{0}' and item_result like '%异常%'
'''.format(check_id)
    cursor = DBUtil.getValue(conn, sql)
    res = cursor.fetchone()
    if res[0] > 0:
        ckres = 1
    else:
        ckres = 0
    sql1 = '''update hd_check_log set check_result={0} where hd_check_id='{1}' '''.format(ckres, check_id)
    conn.execute(sql1)


if __name__ == "__main__":
    targetId, pg, bt, sz = DBUtil.get_env_resource()
    ostype, device_id, helper = DBUtil.get_ssh_help()
    ora = DBUtil.get_ora_env()

    srcloc, srcoggssh, tgtloc, tgtoggssh = DBUtil.getsshogg()
    checkId, triggerTime, baseloc = DBUtil.gethdinfo()
    if ostype == 'AiX':
        pf = '.profile'
        cc = 'df -g'
    elif ostype == 'HPUNIX':
        pf = '.profile'
        cc = 'bdf'
    elif ostype == 'RedHat':
        pf = '.bash_profile'
        cc = 'df -h'
    elif ostype == 'SUSE':
        pf = '.profile'
        cc = 'df -h'
    # print("debug")
    checkuserpass(ora, pg, checkId)
    checklock(ora, pg, checkId)
    checkfileio(ora, pg, checkId)
    checkdiagused(helper, baseloc, pg, checkId, cc)
    checktsused(ora, pg, checkId)
    # checktabused(ora, pg, checkId)
    checkuserpriv(ora, pg, checkId)
    checkarchinuse(ora, pg, checkId)
    checkactivesess(ora, pg, checkId)
    checkredolog(ora, pg, checkId)
    checkmemorymanager(ora, pg, checkId)
    checkcursorpara(ora, pg, checkId)
    checkautospaceadv(ora, pg, checkId)
    checkhiddenpara(ora, pg, checkId)
    checknormalpara(ora, pg, checkId)
    if srcloc:
        checkoggkeeptime(srcoggssh, srcloc, pg, checkId, pf)
        checkogglocused(srcoggssh, srcloc, pg, checkId, cc)
        checkoggprocstat(srcoggssh, srcloc, pg, checkId, pf)
        checkoggprocstat(tgtoggssh, tgtloc, pg, checkId, pf, "tgt")
        checkoggdelay(srcoggssh, srcloc, pg, checkId, pf)
        checkoggdelay(tgtoggssh, tgtloc, pg, checkId, pf, "tgt")
    upthcrunstastus(pg, checkId, 0, 1)
    uptcheckresult(pg, checkId)
    print("msg=" + checkId + "%a%" + targetId)

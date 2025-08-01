#!/usr/bin/env python3
# -*- encoding:utf-8 -*-
import sys



sys.path.append('/usr/software/knowl')
import PGUtil
import ResultCode
import DBUtil
import psycopg2
import io
import DBUtil as dbu

##import ash_db_io_ana as adia
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def getValue(db, sql):
    result = db.execute(sql)
    if (result.code != 0):
        msg = result.msg
        print("msg=WORD_BEGIN" + msg + "WORD_END")
        sys.exit()
    return result.msg


def _get_result(iops, mbps, pg, targetId):
    result = ""
    std_mbps = round(dbu.get_upper_limit(pg, targetId, 2189124) / 1024 / 1024, 2) + round(
        dbu.get_upper_limit(pg, targetId, 2189093) / 1024 / 1024, 2)
    std_iops = dbu.get_upper_limit(pg, targetId, 2189100) + dbu.get_upper_limit(pg, targetId, 2189092)
    msg1 = _estimate_std(mbps, std_mbps)
    msg2 = _estimate_std(iops, std_iops)
    result += f"当前数据库的物理写MBPS的大小为{mbps}MB/s,其基线指标为{std_mbps}MB/s,当前系统的负载{msg1}\n"
    result += f"当前数据库的物理写IOPS的大小为{iops}次,其基线指标为{std_iops}次，当前系统的负载{msg2}"
    return result


def _estimate_std(value, std_value):
    if value is None:
        msg = '数据库的基线指标未采集'
    elif value < std_value * 0.4:
        msg = '不大'
    elif std_value * 0.4 < value < std_value:
        msg = '中等'
    elif std_value < value < std_value * 1.5:
        msg = '较大'
    else:
        msg = '巨大'
    return msg


def DatabaseIO10(ora, pg, targetId):
    mbps_sql = 'select trunc(sum(value/1024/1024)) MB from V$METRIC where  METRIC_ID IN (2126, 2128)'
    iops_sql = 'select trunc(sum(value)) as iops  from V$METRIC where  METRIC_ID IN (2125, 2127)'
    cursor = getValue(ora, mbps_sql)
    mbps = cursor.fetchone()[0]
    cursor = getValue(ora, iops_sql)
    iops = cursor.fetchone()[0]
    return _get_result(iops, mbps, pg, targetId)


def DatabaseIO11(ora, pg, targetId):
    mbpssql = "select round(value,2) from v$metric where metric_id =2145"
    iopssql = "select round(sum(value),2) from v$metric where metric_id in (2092,2100)"
    curmbps = getValue(ora, mbpssql)
    curiops = getValue(ora, iopssql)
    mbps = curmbps.fetchone()[0]
    iops = curiops.fetchone()[0]
    return _get_result(iops, mbps, pg, targetId)


def getcpu():
    ostype, deviceId, helper = dbu.get_ssh_session()
    cpu = []
    cpun = 0

    if "RedHat" in ostype:
        r = b = us = sys = id = wa = 0
        cmd = "vmstat -w 1 10 | awk '{print $1,$2,$13,$14,$15,$16}'"
        result = helper.exec_cmd(cmd)
        tempList = result.split("\n")
        for item in tempList[2:-1]:
            data = item.split(" ")
            r += int(data[0])
            b += int(data[1])
            us += int(data[2])
            sys += int(data[3])
            id += int(data[4])
            wa += int(data[5])

        r = round(r / 10, 2)
        b = round(b / 10, 2)
        us = round(us / 10, 2)
        sys = round(sys / 10, 2)
        id = round(id / 10, 2)
        wa = round(wa / 10, 2)
        cpu.append(dict(r=r, b=b, us=us, sys=sys, id=id, wa=wa))

        cmd_cpu = "cat /proc/cpuinfo |grep processor|wc -l"
        res_cpu = helper.exec_cmd(cmd_cpu).strip()
        cpun = res_cpu

    elif "AiX" in ostype:
        r = b = p = us = sys = id = wa = 0
        cmd = "vmstat -I 1 9 | awk '{print $1,$2,$3,$15,$16,$17,$18}'"
        result = helper.exec_cmd(cmd)
        tempList = result.split("\n")
        for item in tempList[6:-1]:
            data = item.split(" ")
            r += int(data[0])
            b += int(data[1])
            p += int(data[2])
            us += int(data[3])
            sys += int(data[4])
            id += int(data[5])
            wa += int(data[6])

        r = round(r / 9, 2)
        b = round(b / 9, 2)
        p = round(p / 9, 2)
        us = round(us / 9, 2)
        sys = round(sys / 9, 2)
        id = round(id / 9, 2)
        wa = round(wa / 9, 2)
        cpu.append(dict(r=r, b=b, p=p, us=us, sys=sys, id=id, wa=wa))

        cmd_cpu = "pmcycles -m|wc -l"
        res_cpu = helper.exec_cmd(cmd_cpu).strip()
        cpun = res_cpu

    elif "HP" in ostype:
        r = b = us = sys = id = 0
        cmd = "vmstat 1 10 | awk '{print $1,$2,$16,$17,$18}'"
        result = helper.exec_cmd(cmd)
        tempList = result.split("\n")
        for item in tempList[3:-1]:
            data = item.split(" ")
            r += int(data[0])
            b += int(data[1])
            us += int(data[2])
            sys += int(data[3])
            id += int(data[4])

        r = round(r / 10, 2)
        b = round(b / 10, 2)
        us = round(us / 10, 2)
        sys = round(sys / 10, 2)
        id = round(id / 10, 2)
        cpu.append(dict(r=r, b=b, us=us, sys=sys, id=id))

        cmd_cpu = "dmesg | grep processor|wc -l"
        res_cpu = helper.openCmd(cmd_cpu).strip()
        cpun = res_cpu

    return cpu, cpun


def getltmem(pg, bt, et, ti):
    ltmem = 100
    sql = '''

select coalesce(
(
SELECT round(avg(s.value::numeric),2)
        FROM mon_indexdata_his s 
        WHERE index_id = '3000004' 
        AND uid in(select b.uid from mgt_system_device a,
mgt_device b,mgt_system c
where  b.id =a.dev_id 
and c.id = a.sys_id
and a.use_flag=True and b.use_flag=True and c.use_flag=True
and c.uid = '{0}')
        and record_time between '{1}' and '{2}'
				),(SELECT round(avg(s.value::numeric),2)
        FROM mon_indexdata s 
        WHERE index_id = '3000004' 
        AND uid in(select b.uid from mgt_system_device a,
mgt_device b,mgt_system c
where  b.id =a.dev_id 
and c.id = a.sys_id 
and a.use_flag=True and b.use_flag=True and c.use_flag=True
and c.uid = '{0}'))
)
'''.format(ti, bt, et)
    cursor = getValue(pg, sql)
    result = cursor.fetchone()
    if result:
        ltmem = result[0]

    return ltmem


def getmem():
    ostype, deviceId, helper = dbu.get_ssh_session()
    mem = []
    mem_usage = 0
    swap_usage = 0

    if "RedHat" in ostype:
        HugeTotal = HugeFree = SwapToal = SwapFree = MemTotal = MemFree = 0
        cmd = "cat /proc/meminfo | awk '{print $1,$2,$3}' "
        result = helper.exec_cmd(cmd)
        tempList = result.split("\n")
        for item in tempList[:-1]:
            data = item.split(" ")
            mem_size = round(float(data[1]) / 1024, 2)
            if "MemTotal:" == data[0]:
                MemTotal = mem_size
            elif "MemFree:" == data[0]:
                MemFree = mem_size
                mem_usage = round((MemTotal - MemFree) / MemTotal * 100, 2)
            elif "SwapTotal:" == data[0]:
                SwapTotal = mem_size
            elif "SwapFree:" == data[0]:
                SwapFree = mem_size
                swap_usage = round(((SwapTotal - SwapFree) / SwapTotal * 100), 2)
        mem.append(dict(mt=MemTotal, mf=MemFree, mu=mem_usage, st=SwapTotal, sf=SwapFree, su=swap_usage))

    elif "AiX" in ostype:
        cmd = "svmon -G | sed 1d |  awk '{print $1,$2,$3,$4}'"
        result = helper.exec_cmd(cmd)
        tempList = result.split("\n")
        for row in tempList[0:2]:
            item = row.split(' ')
            if item[0] == 'memory':
                MemTotal = round(int(item[1]) * 4 / 1024, 2)
                MemFree = round(int(item[3]) * 4 / 1024, 2)
                mem_usage = round(float(item[2]) / float(item[1]) * 100, 2)
            elif item[0] == 'pg':
                SwapTotal = round(int(item[2]) * 4 / 1024, 2)
                SwapFree = round((int(item[2]) - int(item[3])) * 4 / 1024, 2)
                swap_usage = round((int(item[3]) * 4 / 1024) / (int(item[2]) * 4 / 1024) * 100, 2)
        mem.append(dict(mt=MemTotal, mf=MemFree, mu=mem_usage, st=SwapTotal, sf=SwapFree, su=swap_usage))

    elif "HP" in ostype:
        cmd = "swapinfo -m |awk '{print $1,$2,$3,$4,$5}'"
        result = helper.exec_cmd(cmd)
        tempList = result.split("\n")
        for row in tempList:
            item = row.split(" ")
            if item[0] == "memory":
                MemTotal = item[1]
                MemFree = item[3]
                mem_usage = item[4].replace('%', '')
            if item[0] == "dev":
                SwapTotal = item[1]
                SwapFree = item[3]
                swap_usage = item[4].replace('%', '')
        mem.append(dict(mt=MemTotal, mf=MemFree, mu=mem_usage, st=SwapTotal, sf=SwapFree, su=swap_usage))

    return mem


def getIO(conn, targetid, bt=None, et=None):
    ostype, deviceId, helper = dbu.get_ssh_help()
    io = []
    targetid = deviceId
    if bt and et:
        sql = """select 
        coalesce((SELECT round(avg(s.value::numeric),2)
        FROM mon_indexdata_his s 
        WHERE index_id = '3000006' 
        AND uid = '{0}' 
        and record_time between '{1}'and '{2}'
        ),0) iolantcy,
        coalesce((SELECT round(avg(s.value::numeric),2)
        FROM mon_indexdata_his s 
        WHERE index_id = '3000008' 
        AND uid = '{0}' 
        and record_time between '{1}' and '{2}'
        ),0) iowait,
        coalesce((SELECT round(avg(s.value::numeric),2)
        FROM mon_indexdata_his s 
        WHERE index_id = '3000100' 
        AND uid = '{0}' 
        and record_time between '{1}' and '{2}'
	),0) iops,coalesce((SELECT round(avg(s.value::numeric),2)
        FROM mon_indexdata_his s 
        WHERE index_id = '3000101' 
        AND uid = '{0}' 
        and record_time between '{1}' and '{2}'
        ),0) iombps""".format(targetid, bt, et)
    else:
        sql = f"""select
	coalesce((select round(value::numeric,2) from mon_indexdata where index_id = '3000006' and uid = '{targetid}'),0) iolantcy,
	coalesce((select round(value::numeric,2) from mon_indexdata where index_id = '3000008' and uid = '{targetid}'),0) iowait,
	coalesce((select round(value::numeric,2) from mon_indexdata where index_id = '3000100' and uid = '{targetid}'),0) iops,
	coalesce((select round(value::numeric,2) from mon_indexdata where index_id = '3000101' and uid = '{targetid}'),0) iombps"""
    cursor = getValue(conn, sql)
    result = cursor.fetchone()
    if result:
        iolantcy = result[0]
        iowait = result[1]
        iops = result[2]
        iombps = result[3]

    io.append(dict(iol=iolantcy, iow=iowait, iops=iops, iombps=iombps))

    return io


def getfs():
    ostype, deviceId, helper = dbu.get_ssh_help()
    fs = []

    if "RedHat" in ostype:
        cmd = "\"df -m -P|grep -v \\\"tmpfs\\\"|grep -v \\\"Filesystem\\\"|grep -v \\\"/dev/loop\\\"|grep -v \\\"挂载点\\\"|awk '{print \\$6\\\" \\\"\\$5\\\" \\\"\\$4}'\""
        result = helper.openCmd(cmd)
        tempList = result.strip().split("\n")
        for row in tempList:
            fs.append(dict(fsmp=row.split(" ")[0], fspct=row.split(" ")[1].replace('%', ''), fsres=row.split(" ")[2]))

    elif "AiX" in ostype:
        cmd = "\"df -m|grep -v \\\"Filesystem\\\"|grep -v \\\"proc\\\"|awk '{print \\$7\\\" \\\"\\$4\\\" \\\"\\$3}'\""
        result = helper.openCmd(cmd)
        tempList = result.strip().split("\n")
        for row in tempList:
            fs.append(dict(fsmp=row.split(" ")[0], fspct=row.split(" ")[1].replace('%', ''), fsres=row.split(" ")[2]))

    elif "HP" in ostype:
        cmd = "\"bdf|grep -v \\\"Filesystem\\\"|awk '{print \\$6\\\" \\\"\\$5\\\" \\\"\\$4/1024}'\""
        result = helper.openCmd(cmd)
        tempList = result.strip().split("\n")
        for row in tempList:
            fs.append(dict(fsmp=row.split(" ")[0], fspct=row.split(" ")[1].replace('%', ''), fsres=row.split(" ")[2]))

    return fs


def getdg(conn):
    dgpct = []

    sql = '''select NAME, round(100 - FREE_MB * 100 / TOTAL_MB, 2) pct,free_mb
	   from v$asm_diskgroup
           where TOTAL_MB > 0
           order by 2 desc'''
    cursor = getValue(conn, sql)
    result = cursor.fetchall()
    if result:
        for row in result:
            dgpct.append(dict(dgname=row[0], dgpct=row[1], dgfree=row[2]))

    return dgpct


def gettbs(conn):
    tbspct = []
    sql = '''
select a.tablespace_name,
       round((nvl(b.tot_used, 0) / a.bytes_alloc) * 100) "PCT_USED1",
       round((nvl(b.tot_used, 0) / a.physical_bytes) * 100) "PCT_USED2",
       a.bytes_alloc / (1024 * 1024) "TOTAL ALLOC (MB)",
       a.physical_bytes / (1024 * 1024) "TOTAL PHYS ALLOC (MB)",
       nvl(b.tot_used, 0) / (1024 * 1024) "USED (MB)",
case when round((nvl(b.tot_used, 0) / a.bytes_alloc) * 100) >90 then '使用率过高'
         else '使用率正常' end remark
  from (select tablespace_name,
               sum(bytes) physical_bytes,
               sum(decode(autoextensible, 'NO', bytes, 'YES', maxbytes)) bytes_alloc
          from dba_data_files
         group by tablespace_name) a,
       (select tablespace_name, sum(bytes) tot_used
          from dba_segments
         group by tablespace_name) b
 where a.tablespace_name = b.tablespace_name(+)
   and a.tablespace_name not in
       (select distinct tablespace_name from dba_temp_files)
 order by 1
        '''
    cursor = getValue(conn, sql)
    result = cursor.fetchall()
    if result:
        for row in result:
            tbspct.append(dict(tbsname=row[0], tbspct=row[1], tbsremark=row[6]))

    return tbspct


def gettmptbs(conn):
    tmppct = []
    sql = '''
	Select 
	f.tablespace_name
	,sum(f.bytes_free + f.bytes_used) 
	/1024/1024/1024 Total_GB
	,sum((f.bytes_free + f.bytes_used) - nvl(p.bytes_used, 0))
	/1024/1024/1024 Free_GB
	,sum(nvl(p.bytes_used, 0))
	/1024/1024/1024 Used_GB
	,(sum(nvl(p.bytes_used, 0))/1024/1024/1024)/(sum(f.bytes_free + f.bytes_used) 
	/1024/1024/1024) pct
	from sys.v_$temp_space_header f, dba_temp_files d, sys.v_$temp_extent_pool p
	where f.tablespace_name(+) = d.tablespace_name
	  and f.file_id(+) = d.file_id
	  and p.file_id(+) = d.file_id
	group by f.tablespace_name
	'''
    cursor = getValue(conn, sql)
    result = cursor.fetchall()
    if result:
        for row in result:
            tmppct.append(dict(tmpname=row[0], tmppct=row[4]))

    return tmppct


def getprocess(conn):
    procpct = []
    sql = '''
        select (select count(1) from v$process) proc_num,
               (select value from v$parameter where name = 'processes') proc_param,
	     round((select count(1) from v$process) /
             (select value from v$parameter where name = 'processes') * 100,
             2) pct
	  from dual
	'''
    cursor = getValue(conn, sql)
    result = cursor.fetchall()
    if result:
        for row in result:
            procpct.append(dict(procnum=row[0], procparam=row[1], procpct=row[2]))

    return procpct


def getsession(conn):
    sesspct = []
    sql = '''
        select (select count(1) from v$session) sess_num,
               (select value from v$parameter where name = 'sessions') sess_param,
		round((select count(1) from v$session) /
             (select value from v$parameter where name = 'sessions') * 100,
             2) pct
	  from dual
	'''
    cursor = getValue(conn, sql)
    result = cursor.fetchall()
    if result:
        for row in result:
            sesspct.append(dict(sessnum=row[0], sessparam=row[1], sesspct=row[2]))

    return sesspct


def getblocking(conn):
    blkinfo = []
    # head = ['阻塞者SID', 'SERIAL#', '状态', 'PROGRAM', 'USERNAME', 'EVENT', '被阻塞者SID', '被阻塞者EVENT', '影响对象', '被阻塞SQL']
    sql = """
    SELECT
    s.sid   blocker_sid,
    s.serial# blocker_serial#,
    s.status ,
    substr(s.program,1,40) program,
    s.username,
    s.event,
    w.sid   blocked,
    w.event,
    decode(w.row_wait_obj#,-1,NULL,(select owner || '.' ||object_name from dba_objects o where o.object_id = w.row_wait_obj#)) object_name
    ,q.SQL_TEXT
    FROM
    v$session s,
    v$session w,
    v$sql q
    WHERE
    w.blocking_session = s.sid
    AND w.blocking_session_status = 'VALID'
    and w.sql_id = q.sql_id(+)
    """
    cursor = getValue(conn, sql)
    result = cursor.fetchall()
    if result:
        for row in result:
            blkinfo.append(
                dict(bsid=row[0], bserial=row[1], status=row[2], program=row[3], username=row[4], event=row[5],
                     blksid=row[6], blkevent=row[7], objname=row[8], sqltext=row[9]))

    return blkinfo


def val1(val):
    if val == None:
        return 0
    else:
        return val


if __name__ == '__main__':
    dbInfo = eval(sys.argv[1])
    ##pg info
    dbip = dbInfo['pg_ip']
    dbname = dbInfo['pg_dbname']
    username = dbInfo['pg_usr']
    password = dbInfo['pg_pwd']
    pgport = dbInfo['pg_port']
    ##ora info
    usr = dbInfo['ora_usr']
    pwd = dbInfo['ora_pwd']
    host = dbInfo['ora_ip']
    port = dbInfo['ora_port']
    database = dbInfo['ora_sid']

    targetid = dbInfo['targetId']
    begintime = dbInfo['start_time']
    endtime = dbInfo['end_time']
    rpt_id = dbInfo['rptid']

    pg = PGUtil.Postgre(dbip, username, password, pgport, dbname)
    ora = dbu.get_ora_env()

    try:
        cpu, cpun = getcpu()
        sql_cpu = ""
        flag_cpu = 0
        cpuinfo = "1. R队列分析"

        for res in cpu:
            sql_cpu += "select " + str(val1(res.get('r'))) + " c1," + str(val1(res.get('b'))) + " c2," + str(
                val1(res.get('p'))) + " c3," + str(val1(res.get('us'))) + " c4," + str(
                val1(res.get('sys'))) + " c5," + str(val1(res.get('id'))) + " c6," + str(
                val1(res.get('wa'))) + " c7 union all "

            if val1(res.get('r')) <= int(cpun):
                cpuinfo += '''
R队列长度小于CPU线程数，CPU负载不高；'''
            elif val1(res.get('r')) > cpun and val1(res.get('r')) <= cpun * 2:
                cpuinfo += '''
R队列长度小于CPU线程数2倍且大于1倍，CPU负载较高；'''
                flag_cpu += 1
            else:
                cpuinfo += '''
R队列长度大于CPU线程数2倍，CPU负载很高，存在风险；'''
                flag_cpu += 1

            if val1(res.get('b')) < 10:
                cpuinfo += '''
2. 阻塞队列分析
B队列小于10，B队列正常；'''
            elif val1(res.get('b')) >= 10 and val1(res.get('b')) < 20:
                cpuinfo += '''
2. 阻塞队列分析
B队列小于20，大于10，B队列出现轻微等待，可能IO存在轻微问题；'''
                flag_cpu += 1
            elif val1(res.get('b')) >= 20 and val1(res.get('b')) < 50:
                cpuinfo += '''
2. 阻塞队列分析
B队列大于20，小于50，IO存在性能隐患；'''
                flag_cpu += 1
            else:
                cpuinfo += '''
2. 阻塞队列分析
B队列大于50，IO存在较为严重的问题；'''
                flag_cpu += 1

            if val1(res.get('us')) < 20:
                cpuinfo += '''
3. CPU_USR
小于20，CPU使用率不高；'''
            elif val1(res.get('us')) >= 20 and val1(res.get('us')) < 80:
                cpuinfo += '''
3. CPU_USR
大于20，小于80，CPU使用率正常；'''
            elif val1(res.get('us')) >= 80 and val1(res.get('us')) < 95:
                cpuinfo += '''
3. CPU_USR
大于80，小于95，CPU使用率较高；'''
                flag_cpu += 1
            elif val1(res.get('us')) >= 95 and val1(res.get('r')) > cpun * 2:
                cpuinfo += '''
3. CPU_USR
大于95，CPU使用率很高，并且R队列高于CPU线程数2倍，CPU存在瓶颈；'''
                flag_cpu += 1
            else:
                cpuinfo += '''
3. CPU_USR
CPU暂时无性能瓶颈；'''

            if val1(res.get('sys')) < 15:
                cpuinfo += '''
4. CPU_SYS
小于15，SYS CPU正常；'''
            elif val1(res.get('sys')) >= 15 and val1(res.get('sys')) < 30:
                cpuinfo += '''
4. CPU_SYS
大于15，小于30，SYS CPU使用率较高，需要关注是否系统存在问题；'''
                flag_cpu += 1
            else:
                cpuinfo += '''
4. CPU_SYS
大于30，SYS CPU使用率过高，系统可能存在较为严重的隐患；'''
                flag_cpu += 1

            if val1(res.get('wa')) < 20:
                cpuinfo += '''
5. CPU_IO_WAIT
小于20，CPU IO WAIT正常；'''
            elif val1(res.get('wa')) >= 20 and val1(res.get('wa')) < 40:
                cpuinfo += '''
5. CPU_IO_WAIT
大于20，小于40，CPU IO WAIT较高，检查IO性能和IO负载是否存在问题；'''
                flag_cpu += 1
            else:
                cpuinfo += '''
5. CPU_IO_WAIT
大于40，IO性能存在较为严重的问题；'''
                flag_cpu += 1

            if res.get('p') != None:
                if val1(res.get('p')) < 10:
                    cpuinfo += '''
6. 裸设备IO等待队列长度分析（AiX） 
P队列小于10，P队列正常；'''
                elif val1(res.get('p')) >= 10 and val1(res.get('p')) < 20:
                    cpuinfo += '''
6. 裸设备IO等待队列长度分析（AiX） 
P队列小于20，大于10，P队列出现轻微等待，可能IO存在轻微问题；'''
                    flag_cpu += 1
                elif val1(res.get('p')) >= 20 and val1(res.get('p')) < 50:
                    cpuinfo += '''
6. 裸设备IO等待队列长度分析（AiX） 
P队列大于20，小于50，IO存在性能隐患；'''
                    flag_cpu += 1
                else:
                    cpuinfo += '''
6. 裸设备IO等待队列长度分析（AiX） 
P队列大于50，IO存在较为严重的问题；'''
                    flag_cpu += 1

        sql_cpu = sql_cpu[0:-10]

        sqlf = """
begin;
delete from rpt_res_cpu_ri where rpt_id='{0}' and target_id='{1}';

insert into rpt_res_cpu_ri (rpt_id,target_id,r,b,p,us,sys,id,wa)
select '{0}' rptid,'{1}' target_id,
res.c1,res.c2,res.c3,res.c4,res.c5,res.c6,res.c7
from ({2}) res;
end;""".format(rpt_id, targetid, sql_cpu)
        if sql_cpu != "":
            pg.execute(sqlf)

        if flag_cpu == 0:
            ismf = '''
begin;
delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module='rpt_res_cpu_ri';

insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'rpt_res_cpu_ri' rpt_finding_module,
0 rpt_finding_type,'' rpt_sub_id,'' iname,
'CPU使用率分析' rpt_finding_label,
'信息' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
0 rpt_finding_level;
end;
'''.format(rpt_id, targetid, cpuinfo)
            pg.execute(ismf)
        else:
            ismf = '''
begin;
delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module='rpt_res_cpu_ri';

insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'rpt_res_cpu_ri' rpt_finding_module,
0 rpt_finding_type,'' rpt_sub_id,'' iname,
'CPU使用率分析' rpt_finding_label,
'信息' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level;
end;
'''.format(rpt_id, targetid, cpuinfo)
            pg.execute(ismf)

        mem = getmem()
        mem_lt = getltmem(pg, begintime, endtime, targetid)
        mem_info = ""
        swap_info = ""
        flag_mem = 0
        flag_swap = 0

        sql_mem = ""
        for res in mem:
            sql_mem += "select " + str(res.get('mt')) + " c1," + str(res.get('mf')) + " c2," + str(
                res.get('mu')) + " c3," + str(res.get('st')) + " c4," + str(res.get('sf')) + " c5," + str(
                res.get('su')) + " c6 union all "

            if res.get('mu') > 90 and res.get('mf') < 200 and res.get('mf') > 100:
                mem_info += '''
物理内存使用率超过90%：
空闲内存小于200M，物理内存使用率过高，空闲内存过低；'''
                flag_mem += 1
            elif res.get('mu') > 90 and res.get('mf') <= 100:
                mem_info += '''
物理内存使用率超过90%：
空闲内存小于100M，物理内存使用率过高，空闲内存过低，存在性能风险；'''
                flag_mem += 1
            else:
                mem_info += '''
物理内存使用正常；'''
            if res.get('mu') > float(mem_lt) * 1.2:
                mem_info += '''
物理内存使用率超过最近平均值的20%，建议进行检查；'''
                flag_mem += 1

            if res.get('su') > 50 and res.get('su') < 80:
                swap_info += '''
SWAP使用率超过50%，SWAP使用率过高，建议检查；'''
                flag_swap += 1
            elif res.get('su') >= 80:
                swap_info += '''
SWAP使用率超过80%，SWAP使用率太高，系统存在风险，建议尽快排查；'''
                flag_swap += 1
            else:
                swap_info += '''
SWAP使用率正常；'''
        sql_mem = sql_mem[0:-10]

        sqlf = """
begin;
delete from rpt_res_mem_ri where rpt_id='{0}' and target_id='{1}';

insert into rpt_res_mem_ri(rpt_id,target_id,mem_total,mem_free,mem_pct,swap_total,swap_free,swap_pct)
select '{0}' rptid,'{1}' target_id,
res.c1,res.c2,res.c3,res.c4,res.c5,res.c6
from ({2}) res;
end;""".format(rpt_id, targetid, sql_mem)
        if sql_mem != "":
            pg.execute(sqlf)

        if flag_mem == 0:
            ismf = '''
begin;
delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module='rpt_res_mem_ri';

insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'rpt_res_mem_ri' rpt_finding_module,
0 rpt_finding_type,'' rpt_sub_id,'' iname,
'内存使用率分析' rpt_finding_label,
'信息' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
0 rpt_finding_level;
end;
'''.format(rpt_id, targetid, mem_info)
            pg.execute(ismf)
        else:
            ismf = '''
begin;
delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module='rpt_res_mem_ri';

insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'rpt_res_mem_ri' rpt_finding_module,
0 rpt_finding_type,'' rpt_sub_id,'' iname,
'内存使用率分析' rpt_finding_label,
'信息' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level;
end;
'''.format(rpt_id, targetid, mem_info)
            pg.execute(ismf)

        if flag_swap == 0:
            ismf = '''
begin;
delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module='rpt_res_swap_ri';

insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'rpt_res_swap_ri' rpt_finding_module,
0 rpt_finding_type,'' rpt_sub_id,'' iname,
'SWAP使用率分析' rpt_finding_label,
'信息' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
0 rpt_finding_level;
end;
'''.format(rpt_id, targetid, swap_info)
            pg.execute(ismf)
        else:
            ismf = '''
begin;
delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module='rpt_res_swap_ri';

insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'rpt_res_swap_ri' rpt_finding_module,
0 rpt_finding_type,'' rpt_sub_id,'' iname,
'SWAP使用率分析' rpt_finding_label,
'信息' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level;
end;
'''.format(rpt_id, targetid, swap_info)
            pg.execute(ismf)

        io = getIO(pg, targetid, begintime, endtime)
        io_info = ""
        flag_io = 0

        if ora.conn.version.startswith('10'):
            io_info += DatabaseIO10(ora, pg, targetid)
        else:
            io_info += DatabaseIO11(ora, pg, targetid)

        sql_io = ""
        for res in io:
            sql_io += "select " + str(res.get('iol')) + " c1," + str(res.get('iow')) + " c2," + str(
                res.get('iops')) + " c3," + str(res.get('iombps')) + " c4 union all "

            if res.get('iol') > 10:
                io_info += '''
IO延时超过10毫秒，存在性能问题；'''
                flag_io += 1
            else:
                io_info += '''
IO延时正常；'''

        sql_io = sql_io[0:-10]

        sqlf = """
begin;
delete from rpt_res_io_ri where rpt_id='{0}' and target_id='{1}';

insert into rpt_res_io_ri(rpt_id,target_id,iolantcy,iowait,iops,iombps)
select '{0}' rptid,'{1}' target_id,
res.c1,res.c2,res.c3,res.c4
from ({2}) res;
end;""".format(rpt_id, targetid, sql_io)
        if sql_io != "":
            pg.execute(sqlf)

        if flag_io == 0:
            ismf = '''
begin;
delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module='rpt_res_io_ri';

insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'rpt_res_io_ri' rpt_finding_module,
0 rpt_finding_type,'' rpt_sub_id,'' iname,
'IO情况分析' rpt_finding_label,
'信息' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
0 rpt_finding_level;
end;
'''.format(rpt_id, targetid, io_info)
            pg.execute(ismf)
        else:
            ismf = '''
begin;
delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module='rpt_res_io_ri';

insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'rpt_res_io_ri' rpt_finding_module,
0 rpt_finding_type,'' rpt_sub_id,'' iname,
'IO情况分析' rpt_finding_label,
'信息' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level;
end;
'''.format(rpt_id, targetid, io_info)
            pg.execute(ismf)

        fs = getfs()
        fs_info = ""
        flag_fs = 0

        sql_fs = ""
        for res in fs:
            sql_fs += "select '" + str(res.get('fsmp')) + "' c1," + str(res.get('fspct')) + " c2 union all "

            if float(res.get('fspct')) > 80 and float(res.get('fspct')) < 95 and float(res.get('fsres')) < 500:
                fs_info += res.get('fsmp') + "使用率超过80%，空闲空间小于500M，该目录使用率过高\n"
                flag_fs += 1
            elif float(res.get('fspct')) > 80 and float(res.get('fspct')) < 95 and float(res.get('fsres')) > 2500:
                fs_info += res.get('fsmp') + "使用率不高于95%，空闲空间大于5G，该目录使用率较高\n"
                flag_fs += 1
            elif float(res.get('fspct')) >= 95:
                fs_info += res.get('fsmp') + "使用率超过95%，该文件系统使用率严重超出预警值\n"
                flag_fs += 1
            else:
                fs_info += res.get('fsmp') + "文件系统使用率正常\n"

        sql_fs = sql_fs[0:-10]
        sqlf = """
begin;
delete from rpt_res_fs_ri where rpt_id='{0}' and target_id='{1}';

insert into rpt_res_fs_ri(rpt_id,target_id,fsmp,fspct)
select '{0}' rptid,'{1}' target_id,
res.c1,res.c2
from ({2}) res;
end;""".format(rpt_id, targetid, sql_fs)
        if sql_fs != "":
            pg.execute(sqlf)

        if flag_fs == 0:
            ismf = '''
begin;
delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module='rpt_res_fs_ri';

insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'rpt_res_fs_ri' rpt_finding_module,
0 rpt_finding_type,'' rpt_sub_id,'' iname,
'文件系统使用率分析' rpt_finding_label,
'信息' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
0 rpt_finding_level;
end;
'''.format(rpt_id, targetid, fs_info)
            pg.execute(ismf)
        else:
            ismf = '''
begin;
delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module='rpt_res_fs_ri';

insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'rpt_res_fs_ri' rpt_finding_module,
0 rpt_finding_type,'' rpt_sub_id,'' iname,
'文件系统使用率分析' rpt_finding_label,
'信息' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level;
end;
'''.format(rpt_id, targetid, fs_info)
            pg.execute(ismf)

        dg = getdg(ora)
        dg_info = ""
        flag_dg = 0

        sql_dg = ""
        for res in dg:
            sql_dg += "select '" + str(res.get('dgname')) + "' c1," + str(res.get('dgpct')) + " c2 union all "

            if int(res.get('dgpct')) > 80 and int(res.get('dgpct')) < 95 and int(res.get('dgfree')) < 2048:
                dg_info += res.get('dgname') + "使用率超过80%，空闲空间小于2G，该磁盘组使用率过高\n"
                flag_dg += 1
            elif int(res.get('dgpct')) > 80 and int(res.get('dgpct')) < 95 and int(res.get('dgfree')) > 10240:
                dg_info += res.get('dgname') + "使用率不高于95%，空闲空间大于10G，该磁盘组使用率较高\n"
                flag_dg += 1
            elif int(res.get('dgpct')) >= 95:
                dg_info += res.get('dgname') + "使用率超过95%，该磁盘组使用率严重超出预警值\n"
                flag_dg += 1
            else:
                dg_info += res.get('dgname') + "磁盘组使用率正常\n"

        sql_dg = sql_dg[0:-10]

        sqlf = """
begin;
delete from rpt_res_dg_ri where rpt_id='{0}' and target_id='{1}';

insert into rpt_res_dg_ri(rpt_id,target_id,dgname,dgpct)
select '{0}' rptid,'{1}' target_id,
res.c1,res.c2
from ({2}) res;
end;""".format(rpt_id, targetid, sql_dg)
        if sql_dg != "":
            pg.execute(sqlf)

        if flag_dg == 0:
            ismf = '''
begin;
delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module='rpt_res_dg_ri';

insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'rpt_res_dg_ri' rpt_finding_module,
0 rpt_finding_type,'' rpt_sub_id,'' iname,
'磁盘组使用率分析' rpt_finding_label,
'信息' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
0 rpt_finding_level;
end;
'''.format(rpt_id, targetid, dg_info)
            pg.execute(ismf)
        else:
            ismf = '''
begin;
delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module='rpt_res_dg_ri';

insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'rpt_res_dg_ri' rpt_finding_module,
0 rpt_finding_type,'' rpt_sub_id,'' iname,
'磁盘组使用率分析' rpt_finding_label,
'信息' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level;
end;
'''.format(rpt_id, targetid, dg_info)
            pg.execute(ismf)

        tbs = gettbs(ora)
        sql_tbs = ""
        for res in tbs:
            sql_tbs += "select '" + str(res.get('tbsname')) + "' c1," + str(res.get('tbspct')) + " c2,'" + str(
                res.get('tbsremark')) + "' c3 union all "
        sql_tbs = sql_tbs[0:-10]

        sqlf = """
begin;
delete from rpt_res_tbs_ri where rpt_id='{0}' and target_id='{1}';

insert into rpt_res_tbs_ri(rpt_id,target_id,tbsname,tbspct,remark)
select '{0}' rptid,'{1}' target_id,
res.c1,res.c2,res.c3
from ({2}) res;
end;""".format(rpt_id, targetid, sql_tbs)
        if sql_tbs != "":
            pg.execute(sqlf)

        tmptbs = gettmptbs(ora)
        sql_tmp = ""
        for res in tmptbs:
            sql_tmp += "select '" + str(res.get('tmpname')) + "' c1," + str(res.get('tmppct')) + " c2 union all "
        sql_tmp = sql_tmp[0:-10]

        sqlf = """
begin;
delete from rpt_res_tmptbs_ri where rpt_id='{0}' and target_id='{1}';

insert into rpt_res_tmptbs_ri(rpt_id,target_id,tmptbsname,tmptbspct)
select '{0}' rptid,'{1}' target_id,
res.c1,res.c2
from ({2}) res;
end;""".format(rpt_id, targetid, sql_tmp)
        if sql_tmp != "":
            pg.execute(sqlf)

        procpct = getprocess(ora)
        proc_info = ""
        flag_proc = 0

        sql_proc = ""
        for res in procpct:
            sql_proc += "select " + str(res.get('procparam')) + " c1," + str(res.get('procnum')) + " c2 ," + str(
                res.get('procpct')) + " c3 union all "
            if res.get('procpct') > 90:
                proc_info += '''
进程数占比超过90%，进程占比过高，需要关注；'''
                flag_proc += 1
            else:
                proc_info += '''
进程数占比正常；'''

        sql_proc = sql_proc[0:-10]

        sqlf = """
begin;
delete from rpt_res_procpct_ri where rpt_id='{0}' and target_id='{1}';

insert into rpt_res_procpct_ri(rpt_id,target_id,proc_param, proc_num, proc_pct)
select '{0}' rptid,'{1}' target_id,
res.c1,res.c2,res.c3
from ({2}) res;
end;""".format(rpt_id, targetid, sql_proc)
        if sql_proc != "":
            pg.execute(sqlf)

        if flag_proc == 0:
            ismf = '''
begin;
delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module='rpt_res_procpct_ri';

insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'rpt_res_procpct_ri' rpt_finding_module,
0 rpt_finding_type,'' rpt_sub_id,'' iname,
'进程数占比分析' rpt_finding_label,
'信息' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
0 rpt_finding_level;
end;
'''.format(rpt_id, targetid, proc_info)
            pg.execute(ismf)
        else:
            ismf = '''
begin;
delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module='rpt_res_procpct_ri';

insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'rpt_res_procpct_ri' rpt_finding_module,
0 rpt_finding_type,'' rpt_sub_id,'' iname,
'进程数占比分析' rpt_finding_label,
'信息' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level;
end;
'''.format(rpt_id, targetid, proc_info)
            pg.execute(ismf)

        sesspct = getsession(ora)
        sess_info = ""
        flag_sess = 0

        sql_sess = ""
        for res in sesspct:
            sql_sess += "select " + str(res.get('sessparam')) + " c1," + str(res.get('sessnum')) + " c2 ," + str(
                res.get('sesspct')) + " c3 union all "
            if res.get('sesspct') > 90:
                sess_info += '''
会话数占比超过90%，会话占比过高，需要关注；'''
                flag_sess += 1
            else:
                sess_info += '''
会话数占比正常；'''

        sql_sess = sql_sess[0:-10]

        sqlf = """
begin;
delete from rpt_res_sesspct_ri where rpt_id='{0}' and target_id='{1}';

insert into rpt_res_sesspct_ri(rpt_id,target_id,sess_param, sess_num, sess_pct)
select '{0}' rptid,'{1}' target_id,
res.c1,res.c2,res.c3
from ({2}) res;
end;""".format(rpt_id, targetid, sql_sess)
        if sql_sess != "":
            pg.execute(sqlf)

        if flag_sess == 0:
            ismf = '''
begin;
delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module='rpt_res_sesspct_ri';

insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'rpt_res_sesspct_ri' rpt_finding_module,
0 rpt_finding_type,'' rpt_sub_id,'' iname,
'会话数占比分析' rpt_finding_label,
'信息' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
0 rpt_finding_level;
end;
'''.format(rpt_id, targetid, sess_info)
            pg.execute(ismf)
        else:
            ismf = '''
begin;
delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module='rpt_res_sesspct_ri';

insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'rpt_res_sesspct_ri' rpt_finding_module,
0 rpt_finding_type,'' rpt_sub_id,'' iname,
'会话数占比分析' rpt_finding_label,
'信息' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level;
end;
'''.format(rpt_id, targetid, sess_info)
            pg.execute(ismf)

        blkinfo = getblocking(ora)
        sql_blk = ""
        for res in blkinfo:
            sql_blk += "select " + str(res.get('bsid')) + " c1," + str(res.get('bserial')) + " c2 ,'" + str(
                res.get('status')) + "' c3 ,'" + str(res.get('program')) + "' c4 ,'" + str(
                res.get('username')) + "' c5 ,'" + str(res.get('event')) + "' c6 ," + str(
                res.get('blksid')) + " c7 ,'" + str(res.get('blkevent')) + "' c8 ,'" + str(
                res.get('objname')) + "' c9 ,'" + str(res.get('sqltext')).replace("'", "") + "' c10 union all "
        sql_blk = sql_blk[0:-10]

        sqlf = """
begin;
delete from rpt_res_blkinfo_ri where rpt_id='{0}' and target_id='{1}';

insert into rpt_res_blkinfo_ri(rpt_id,target_id,blocker_sid, blocker_serial, status, program, username, event, blocked_sid, blocked_event, obj_name, blocked_sql)
select '{0}' rptid,'{1}' target_id,
res.c1,res.c2,res.c3,res.c4,res.c5,res.c6,res.c7,res.c8,res.c9,res.c10
from ({2}) res;
end;""".format(rpt_id, targetid, sql_blk)
        if sql_blk != "":
            pg.execute(sqlf)

    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

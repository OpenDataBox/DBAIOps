#!/usr/bin/env python3
# -*- encoding:utf-8 -*-
import sys

sys.path.append('/usr/software/knowl')
import PGUtil
import CommUtil
import ResultCode
import DBUtil
import psycopg2
import io
import subprocess

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def getValue(db, sql):
    result = db.execute(sql)
    if (result.code != 0):
        msg = result.msg
        print("msg=WORD_BEGIN" + msg + "WORD_END")
        sys.exit()
    return result.msg


def getoraerrinfo(errorType, version, errcode):
    errorCause = ""
    errorAction = ""
    errorDesc = ""
    errorCode = ""
    flag = 0
    oerr = "/usr/software/knowl/msg/oerr.pl"
    MsgPath = "/usr/software/knowl/msg/" + errorType + version + ".msg"
    cmd = oerr + " " + MsgPath + " " + str(errcode)
    cmd_result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    cmd_stdout = cmd_result.stdout.readlines()
    for line in cmd_stdout:
        raw_line = line.decode("utf-8").strip()
        if raw_line[0:2].isdigit():
            errorCode = raw_line.split(",")[0]
            errorDesc = raw_line.split(",")[2].replace("'", "''")
        elif raw_line.startswith("// *Cause"):
            errorCause += raw_line[5:].split(":")[1].strip()
            flag = 1
        elif raw_line.startswith("// *Action"):
            errorAction += raw_line[5:].split(":")[1].strip()
            flag = 2
        elif raw_line.startswith("//"):
            if flag == 1:
                errorCause += raw_line[2:].strip()
            elif flag == 2:
                errorAction += raw_line[2:].strip()

    return errorDesc, errorCause


def getmaxsnap(pg, targetid, begin_time, end_time):
    maxsnapid = ""
    sql = '''select max(snap_id::numeric ) from p_oracle_cib where target_id='{0}'
    and (
     (record_time > to_date('{1}','yyyy-mm-dd hh24:mi:ss')
    and record_time < to_date('{2}','yyyy-mm-dd hh24:mi:ss')) 
    or to_char(record_time,'yyyy-mm-dd') <= to_char(to_date('{2}' ,'yyyy-mm-dd') ,'yyyy-mm-dd'))
     '''.format(targetid, begin_time, end_time)
    sqlcursor = getValue(pg, sql)
    sqlrersult = sqlcursor.fetchall()

    if sqlrersult:
        for row in sqlrersult:
            if not row[0] is None:
                maxsnapid = row[0]
            else:
                maxsnapid = -1
    else:
        maxsnapid = -1

    return maxsnapid


def getlogana(pg, targetid, begin_time, end_time):
    dbv = ""
    errcode = ""
    errType = ""
    ana = ""
    des = "日志分析"
    head = ['错误代码', '报错次数', '错误说明']
    maxsnapid = getmaxsnap(pg, targetid, begin_time, end_time)
    sqllogana = '''
select log_code,count(*),' ' as note from log_detail where begin_time between '{0}' and '{1}'
 and target_id='{2}' and lower(log_code) not like 'evt%'group by log_code order by 
 case when log_code in ('ORA-00600','ORA-07445','ORA-00603') then 1 else 10000 end,2 desc
 '''.format(begin_time, end_time, targetid)
    # print(sqllogana)
    sqlloganacursor = getValue(pg, sqllogana)
    sqlloganaresult = sqlloganacursor.fetchall()
    sqldbv = '''
select cib_value from p_oracle_cib where target_id='{0}' and index_id='2201001' and cib_name='version'
and snap_id='{1}' '''.format(targetid, maxsnapid)
    # print(sqldbv)
    sqldbvcursor = getValue(pg, sqldbv)
    sqldbvresult = sqldbvcursor.fetchall()
    for row in sqldbvresult:
        dbv = ''.join(row[0].split('.')[0:2])
        # print(dbv)

    for resulttolist in sqlloganaresult:
        sqlloganaresult[sqlloganaresult.index(resulttolist)] = list(resulttolist)

    for row in sqlloganaresult:
        if row[0].strip().split('-')[0].lower() == 'ora' or row[0].strip().split('-')[0].lower() == 'tns':
            errType = row[0].split('-')[0].lower()
            errcode = row[0].split('-')[1].lower()
            if errType in ('ora', 'tns'):
                errorDesc, errorcause = getoraerrinfo(errType, dbv, errcode)
                row[2] = errorDesc + '\n' + errorcause
        # print(dbv)
        if row[0].strip().upper() == 'SCN-00001':
            row[2] = "SCN跃变"
        if row[0].strip().upper() == 'DGD-00001':
            row[2] = "dataguard日志传输失败"
        if row[0].strip().upper() == 'ERR-00001':
            row[2] = "其他错误"
        if row[0].strip().upper() == 'ERR-00002':
            row[2] = "旧的UNDO表空间仍存在活跃事务"
        if row[0].strip().upper() == 'ERR-00003':
            row[2] = "pmon无法获取latch"
        if row[0].strip().upper() == 'ERR-00004':
            row[2] = "实例非正常关闭"
        if row[0].strip().upper() == 'SWP-00001':
            row[2] = "发生内存换页"

    sqlresult = CommUtil.createTable(head, sqlloganaresult, des)

    return sqlresult


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
    try:
        loganaresult = getlogana(pg, targetid, begintime, endtime)
        if loganaresult:
            # print("msg=" + loganaresult)
            sqllr = '''
begin;
delete from rpt_log_info where rpt_id='{0}' and target_id='{1}';
insert into rpt_log_info (rpt_id,target_id,rpt_log_code,rpt_times,rpt_error_note)
select '{0}' rptid,'{1}' target_id,a.log_code, count(*), 
case when a.log_code='SCN-00001' then 'SCN跃变'
  when a.log_code='DGD-00001' then 'dataguard日志传输失败'
  when a.log_code='ERR-00001' then '其他错误'
  when a.log_code='ERR-00002' then '旧的UNDO表空间仍存在活跃事务'
  when a.log_code='ERR-00003' then 'pmon无法获取latch'
  when a.log_code='ERR-00004' then '实例非正常关闭'
  when a.log_code='SWP-00001' then '发生内存换页'
  else b.msg end as note
  from log_detail a
  left join (select a.log_code,a.msg from (		  
select log_type||'-'||code log_code,msg,
	row_number() over(partition by log_type,code order by version desc ) as rn from ora_error 		
	) a where rn=1) b on a.log_code=b.log_code
 where a.begin_time between '{2}' and '{3}'
   and a.target_id = '{1}'
   and lower(a.log_code) not like 'evt%'
 group by a.log_code,b.msg
 order by case
            when a.log_code in ('ORA-00600', 'ORA-07445', 'ORA-00603') then
             1
            else
             10000
          end,
          2 desc;
end;
'''.format(rpt_id, targetid, begintime, endtime)
            pg.execute(sqllr)

    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

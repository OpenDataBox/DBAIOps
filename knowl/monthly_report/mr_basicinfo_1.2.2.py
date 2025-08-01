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

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def getValue(db, sql):
    result = db.execute(sql)
    if (result.code != 0):
        msg = result.msg
        print("msg=WORD_BEGIN" + msg + "WORD_END")
        sys.exit()
    return result.msg


def getdbid(pg, targetid):
    dbid = ""
    sql = "select subuid from mgt_system where uid='{0}'".format(targetid)
    sqlcursor = getValue(pg, sql)
    sqlresult = sqlcursor.fetchall()
    for row in sqlresult:
        dbid = row[0]
    return dbid


def getsgaresize(pg, targetid, begin_time, end_time):
    ana = ''
    head = ["内存组件", "操作类型", "操作模式", "目标值", "最终值", "状态", "开始时间", "结束时间"]
    des = "SGA RESIZE信息"
    dbid = getdbid(pg, targetid)
    sqlsgaresize = '''
select * from (SELECT PARAMETER,OPER_TYPE,OPER_MODE,TARGET_SIZE,FINAL_SIZE,STATUS,START_TIME,END_TIME 
FROM SGA_RESIZE_OPS where oper_mode <>'STATIC' and target_id='{0}' and start_time between '{1}' and '{2}' 
order by start_time desc) as foo '''.format(targetid, begin_time, end_time)
    # print(sqlsgaresize)
    sqlsgaresizecursor = getValue(pg, sqlsgaresize)
    sqlsgaresizeresults = sqlsgaresizecursor.fetchall()

    if len(sqlsgaresizeresults) > 10:
        ana = "建议关注SGA设置，可能存在SGA设置偏小的问题。\n"
    tmp = []
    for row in sqlsgaresizeresults:
        if row[3] != row[4]:
            tmp.append("SGA RESIZE出现过无法满足系统需求的情况，可能是SGA配置过低或者系统并发过高导致，建议深入排查。\n")
        # if row[7]-1/1440 > row[6]
        if (row[7] - row[6]).seconds > 60:
            tmp.append("SGA RESIZE完成时间出现超过1分钟的情况，说明SGA配置过低或者系统并发过大或者系统SGA管理存在性能问题，建议深入排查。\n")

    ana += ''.join(set(tmp))
    sqlresult = CommUtil.createTable(head, sqlsgaresizeresults, des)
    return sqlresult, ana


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
        logsgaresizeresult, logsgaresizenote = getsgaresize(pg, targetid, begintime, endtime)
        if logsgaresizeresult:
            # print("msg=" + logsgaresizeresult)
            sqlls = '''
begin;
delete from rpt_sga_resize where rpt_id='{0}' and target_id='{1}' ;
insert into rpt_sga_resize(rpt_id,target_id,snap_time,component,oper_type,oper_mode,parameter,initial_size,target_size,
						  final_size,status,start_time,end_time)
select '{0}' rptid,'{1}' target_id,snap_time,component,OPER_TYPE,OPER_MODE,PARAMETER,initial_size,target_size,
final_size,status,start_time,end_time   
          FROM SGA_RESIZE_OPS
         where oper_mode <> 'STATIC'
           and target_id = '{1}'
           and start_time between '{2}' and '{3}'
         order by start_time desc;
end;
'''.format(rpt_id, targetid, begintime, endtime)
            pg.execute(sqlls)

        if logsgaresizenote:
            # print("SCREEN_BEGIN问题与发现:\\n" + logsgaresizenote+"SCREEN_END")
            logsgaresizenote = """问题与发现：
""" + logsgaresizenote
            ismf = '''
begin;
delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module='basic_sga_resize';
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'basic_sga_resize' rpt_finding_module,
0 rpt_finding_type,'' rpt_sub_id,'' iname,
'SGA_RESIZE分析' rpt_finding_label,
'信息' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level;
end;
'''.format(rpt_id, targetid, logsgaresizenote)
            pg.execute(ismf)

    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

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
        print(sql)
        print("msg=WORD_BEGIN" + result.msg + "WORD_END")
        sys.exit()
    return result.msg


def getlevel(score):
    level = ""
    if score >= 90:
        level = "优秀"
    elif score >= 75 and score < 90:
        level = "良好"
    elif score >= 50 and score < 75:
        level = "中等"
    elif score < 50:
        level = "较差"
    return level


def getloadlevel(score):
    level = ""
    if score >= 90:
        level = "超高"
    elif score >= 75 and score < 90:
        level = "较高"
    elif score >= 50 and score < 75:
        level = "一般"
    elif score < 50:
        level = "较低"
    return level


def runinfo(pg, targetid, begin_time, end_time):
    ana = ""
    head = ['指标名称', '最高值', '最低值', '平均值']
    des = "运行概况"
    runinforesults = []
    sqllogfilesync = '''
select cm.index_name,
	coalesce(cm.maxscore,0) cmas,
	coalesce(cm.minscore,0) cmis,
	coalesce(cm.avgscore,0) cavs from 
(
select 'log file sync' as index_name,
           round(max(metric_value::numeric),2) maxscore,
       round(min(metric_value::numeric),2) minscore,
           round(avg(metric_value::numeric),2) avgscore 
  from h_health_check_detail 
 where metric_id = 2184301
 and metric_value != '周期内无有效采样记录'
   and record_time between '{1}' and '{2}'
   and target_id ='{0}'
) cm
'''.format(targetid, begin_time, end_time)
    sqllogfilesynccursor = getValue(pg, sqllogfilesync)
    sqllogfilesyncresult = sqllogfilesynccursor.fetchall()

    sqlactivesesscnt = '''
select cm.index_name,
	coalesce(cm.maxscore,0) cmas,
	coalesce(cm.minscore,0) cmis,
	coalesce(cm.avgscore,0) cavs
	from  
(
select '活跃会话数' as index_name,
       round(max(metric_value::numeric),2) maxscore,
       round(min(metric_value::numeric),2) minscore,
       round(avg(metric_value::numeric),2) avgscore 
  from h_health_check_detail 
 where metric_id = 2189147
 and metric_value != '周期内无有效采样记录'
   and record_time between '{1}' and '{2}'
   and target_id ='{0}'
) cm 
'''.format(targetid, begin_time, end_time)

    sqlactivesesscntcursor = getValue(pg, sqlactivesesscnt)
    sqlactivesesscntresult = sqlactivesesscntcursor.fetchall()

    sqlloadperf = '''
select cm.index_name,
        coalesce(cm.maxscore,0) cmas,
        coalesce(cm.minscore,0) cmis,
        coalesce(cm.avgscore,0) cavs
 from
(
select '负载分' index_name,
       round(max(b.load_score),2) maxscore,
	   round(min(b.load_score),2) minscore,
	   round(avg(b.load_score),2) avgscore
  from p_perf_eva a,p_perf_eva_his b
 where a.target_id = '{0}'
   and a.eva_id = b.eva_id 
   and b.record_time between '{1}' and '{2}'
   union all
select '性能分' index_name,
       round(max(b.perf_score),2) maxscore,
	   round(min(b.perf_score),2) minscore,
	   round(avg(b.perf_score),2) avgscore
  from p_perf_eva a,p_perf_eva_his b
 where a.target_id = '{0}'
   and a.eva_id = b.eva_id 
   and b.record_time between '{1}' and '{2}'
) cm
'''.format(targetid, begin_time, end_time)
    sqlloadperfcursor = getValue(pg, sqlloadperf)
    sqlloadperfresult = sqlloadperfcursor.fetchall()

    sqlhealth = '''
select cm.index_name,coalesce(cm.maxscore,0) cmas,coalesce(cm.minscore,0) cmis,coalesce(cm.avgscore,0) cavs
  from 
(
select '健康分' as index_name,
	round(max(value::numeric),2) maxscore,
	round(min(value::numeric),2) minscore,
	round(avg(value::numeric),2) avgscore
  from mon_indexdata_his
 where index_id = 2180400 
   and uid = '{0}' 
   and record_time between '{1}' and '{2}'
) cm
'''.format(targetid, begin_time, end_time)

    sqlhealthcursor = getValue(pg, sqlhealth)
    sqlhealthresult = sqlhealthcursor.fetchall()

    for row in sqlhealthresult:
        runinforesults.append(row)
    for row in sqlloadperfresult:
        runinforesults.append(row)
    for row in sqlactivesesscntresult:
        runinforesults.append(row)
    for row in sqllogfilesyncresult:
        runinforesults.append(row)

    for row in runinforesults:
        if row[0] == "健康分":
            ana += "健康值的平均分为%s,属于%s范围;健康值的最低分为%s,属于%s范围。\\n" % (row[3], getlevel(row[3]), row[2], getlevel(row[2]))
            if row[2] < 75:
                ana += "健康值最低分进入中等或者以下范围，说明系统存在健康隐患，建议进行深入分析。\\n"
        if row[0] == "负载分":
            ana += "负载值的平均分为%s,属于%s范围;负载的最高值为%s,属于%s范围。\\n" % (
            row[3], getloadlevel(row[3]), row[1], getloadlevel(row[2]))
            if row[1] > 75:
                ana += "负载值最高分进入较高或者以上范围，说明系统存在负载过高隐患，建议进行深入分析。\\n"
        if row[0] == "性能分":
            ana += "性能值的平均分为%s,属于%s范围;性能值的最低分为%s,属于%s范围。\\n" % (row[3], getlevel(row[3]), row[2], getlevel(row[2]))
            if row[2] < 75:
                ana += "性能值最低分进入中等或者以下范围，说明系统存在性能隐患，建议进行深入分析。\\n"
        if row[0] == "活跃会话数":
            ana += "活跃会话数的平均值为%s,最高值为%s。\\n" % (row[3], row[1])
            if row[3] > 100:
                ana += "活跃会话数一般来说会较为稳定，在本次统计期间内，活跃会话数异常增长,数据库系统可能存在性能问题或者存在运行安全隐患，建议进行排查。\\n"
        if row[0] == "log file sync":
            ana += "LOG FILE SYNC延时的平均值为%s,最高值为%s。\\n" % (row[3], row[1])
            if row[3] > 8:
                ana += "LOG FILE SYNC等待一般较为稳定，但是当数据库系统出现一些问题，比如REDO量突增、遇到BUG、写IO性能不佳或者其他隐患的时候，LOG FILE SYNC指标会有较大波动。在本月内，出现了LOG FILE SYNC性能下降的问题，建议进行深入排查。\\n"

    sqlresult = CommUtil.createTable(head, runinforesults, des)

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
        runinforesult, runinfonote = runinfo(pg, targetid, begintime, endtime)
        if runinforesult:
            # print("msg=" + runinforesult)
            sqlrr = '''
begin;
delete from rpt_sys_baseline where rpt_id='{0}' and target_id='{1}';
insert into rpt_sys_baseline (rpt_id,target_id,rpt_metric_name,
  rpt_metric_value_high,rpt_metric_value_avg,rpt_metric_value_low)
select distinct '{0}' rptid,'{1}' target_id,res.index_name,res.cmas,res.cavs,res.cmis
from (
select cm.index_name,
	coalesce(cm.maxscore,0) cmas,
	coalesce(cm.minscore,0) cmis,
	coalesce(cm.avgscore,0) cavs from 
(
select 'log file sync' as index_name,
 	   round(max(metric_value::numeric),2) maxscore,
       round(min(metric_value::numeric),2) minscore,
	   round(avg(metric_value::numeric),2) avgscore 
  from h_health_check_detail 
 where metric_id = 2184301
 and metric_value != '周期内无有效采样记录'
   and record_time between '{2}' and '{3}'
   and target_id ='{1}'
) cm
union all
select cm.index_name,
	coalesce(cm.maxscore,0) cmas,
	coalesce(cm.minscore,0) cmis,
	coalesce(cm.avgscore,0) cavs
	from  
(
select '活跃会话数' as index_name,
 		round(max(metric_value::numeric),2) maxscore,
       round(min(metric_value::numeric),2) minscore,
	   round(avg(metric_value::numeric),2) avgscore 
  from h_health_check_detail 
 where metric_id = 2189147
 and metric_value != '周期内无有效采样记录'
   and record_time between '{2}' and '{3}'
   and target_id ='{1}'
) cm 
union all
select cm.index_name,
        coalesce(cm.maxscore,0) cmas,
        coalesce(cm.minscore,0) cmis,
        coalesce(cm.avgscore,0) cavs
        from  
(
select '负载分' index_name,
       round(max(b.load_score),2) maxscore,
	   round(min(b.load_score),2) minscore,
	   round(avg(b.load_score),2) avgscore
  from p_perf_eva a,p_perf_eva_his b
 where a.target_id = '{1}'
   and a.eva_id = b.eva_id 
   and b.record_time between '{2}' and '{3}'
   union all
select '性能分' index_name,
       round(max(b.perf_score),2) maxscore,
	   round(min(b.perf_score),2) minscore,
	   round(avg(b.perf_score),2) avgscore
  from p_perf_eva a,p_perf_eva_his b
 where a.target_id = '{1}'
   and a.eva_id = b.eva_id 
   and b.record_time between '{2}' and '{3}'
) cm
union all
select cm.index_name,coalesce(cm.maxscore,0) cmas,coalesce(cm.minscore,0) cmis,coalesce(cm.avgscore,0) cavs
  from 
(
select '健康分' as index_name,
	round(max(value::numeric),2) maxscore,
	round(min(value::numeric),2) minscore,
	round(avg(value::numeric),2) avgscore
  from mon_indexdata_his
 where index_id = 2180400 
   and uid = '{1}' 
   and record_time between '{2}' and '{3}'
) cm
)  res;

end;
'''.format(rpt_id, targetid, begintime, endtime)
            pg.execute(sqlrr)

        if runinfonote:
            # print("SCREEN_BEGIN问题与发现:\\n" + runinfonote + "SCREEN_END")
            runinfonote = """问题与发现：
""" + runinfonote
            ismf = '''
begin;
delete from rpt_finding where rpt_finding_module='basic_runinfo_ri' and rpt_id='{0}' and target_id='{1}';

insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'basic_runinfo_ri' rpt_finding_module,
0 rpt_finding_type,'' rpt_sub_id,'' iname,
'运行概况' rpt_finding_label,
'信息' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
0 rpt_finding_level;
end;
'''.format(rpt_id, targetid, runinfonote)
            pg.execute(ismf)

    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

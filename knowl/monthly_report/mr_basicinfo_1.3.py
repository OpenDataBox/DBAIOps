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


def comparelevel(score1, score2):
    change = ""
    if score1 > score2:
        change = "有所提高"
    elif score1 == score2:
        change = "持平"
    elif score1 < score2:
        change = "有所降低"
    return change


def comparescore(score1, score2):
    change = ""
    if score1 > score2:
        change = "有所上升"
    elif score1 == score2:
        change = "基本持平"
    elif score1 < score2:
        change = "有所下降"
    return change


def runinfo(pg, targetid, begin_time, end_time):
    ana = ""
    head = ['指标名称', '本月最高值', '本月最低值', '本月平均值', '上月最高值', '上月最低值', '上月平均值']
    des = "运行概况"
    runinforesults = []
    sqllogfilesync = '''
select distinct coalesce(cm.index_name,lm.index_name) index_name,coalesce(cm.maxscore,0)cmas,coalesce(cm.minscore,0)cmis,coalesce(cm.avgscore,0)cavs,
coalesce(lm.maxscore,0)lmas,coalesce(lm.minscore,0)lmis,coalesce(lm.maxscore,0)lavs from 
(select 'log file sync' as index_name,r."maxScore" maxscore,r."minScore" minscore,r."avgScore" avgscore 
from r_m_indexdata r where  r.uid='{0}' and 
r.index_id=2184301 and r.begin_time + interval '1 month' between '{1}' and '{2}') lm full join
(select 'log file sync' as index_name,r."maxScore" maxscore,r."minScore" minscore,r."avgScore" avgscore 
from r_m_indexdata r where r.uid='{0}' and 
r.index_id=2184301 and r.begin_time between '{1}' and '{2}') cm
on lm.index_name=cm.index_name'''.format(targetid, begin_time, end_time)
    # print(sqllogfilesync)
    sqllogfilesynccursor = getValue(pg, sqllogfilesync)
    sqllogfilesyncresult = sqllogfilesynccursor.fetchall()

    sqlactivesesscnt = '''
select distinct coalesce(cm.index_name,lm.index_name) index_name,coalesce(cm.maxscore,0)cmas,coalesce(cm.minscore,0)cmis,coalesce(cm.avgscore,0)cavs,
coalesce(lm.maxscore,0)lmas,coalesce(lm.minscore,0)lmis,coalesce(lm.maxscore,0)lavs from 
(select '活跃会话数' as index_name,r."maxScore" maxscore,r."minScore" minscore,r."avgScore" avgscore 
from r_m_indexdata r where  r.uid='{0}' and 
r.index_id=2189147 and r.begin_time + interval '1 month' between '{1}' and '{2}') lm full join
(select '活跃会话数' as index_name,r."maxScore" maxscore,r."minScore" minscore,r."avgScore" avgscore 
from r_m_indexdata r where r.uid='{0}' and 
r.index_id=2189147 and r.begin_time between '{1}' and '{2}') cm
on lm.index_name=cm.index_name'''.format(targetid, begin_time, end_time)
    # print(sqlactivesesscnt)

    sqlactivesesscntcursor = getValue(pg, sqlactivesesscnt)
    sqlactivesesscntresult = sqlactivesesscntcursor.fetchall()

    sqlloadperf = '''
select distinct coalesce(cm.index_name,lm.index_name) index_name,coalesce(cm.maxscore,0)cmas,coalesce(cm.minscore,0)cmis,coalesce(cm.avgscore,0)cavs,
coalesce(lm.maxscore,0)lmas,coalesce(lm.minscore,0)lmis,coalesce(lm.maxscore,0)lavs from 
(select case when r.type=1 then '负载分' when r.type=2 then '性能分' end as index_name,r."maxScore" as  maxscore,
r."minScore" as minscore,r."avgScore" as  avgscore from r_m_perf_eva r,p_perf_eva p where p.target_id='{0}'
and r.eva_id=p.eva_id and use_flag=true and r.begin_time + interval '1 month' between '{1}' and '{2}') lm full join
(select case when r.type=1 then '负载分' when r.type=2 then '性能分' end as index_name,r."maxScore" as  maxscore,
r."minScore" as minscore,r."avgScore" as  avgscore from r_m_perf_eva r,p_perf_eva p where p.target_id='{0}'
and r.eva_id=p.eva_id and use_flag=true and r.begin_time between '{1}' and '{2}') cm 
on cm.index_name=lm.index_name'''.format(targetid, begin_time, end_time)
    # print(sqlloadperf)
    sqlloadperfcursor = getValue(pg, sqlloadperf)
    sqlloadperfresult = sqlloadperfcursor.fetchall()

    sqlhealth = '''
select distinct coalesce(cm.index_name,lm.index_name) index_name,coalesce(cm.maxscore,0)cmas,coalesce(cm.minscore,0)cmis,coalesce(cm.avgscore,0)cavs,
coalesce(lm.maxscore,0)lmas,coalesce(lm.minscore,0)lmis,coalesce(lm.maxscore,0)lavs from 
(select '健康分' as index_name,r."maxScore" maxscore,r."minScore" minscore,r."avgScore" avgscore from r_m_indexdata r where 
 r.index_id=2180400 and uid='{0}' and r.begin_time + interval '1 month' between '{1}' and '{2}') lm full join
(select '健康分' as index_name,r."maxScore" maxscore,r."minScore" minscore,r."avgScore" avgscore from r_m_indexdata r where 
 r.index_id=2180400 and uid='{0}' and r.begin_time between '{1}' and '{2}') cm
on lm.index_name=cm.index_name'''.format(targetid, begin_time, end_time)
    # print(sqlhealth)

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
            ana += "健康值的平均分为%s,属于%s范围,较上个月%s;健康值的最低分为%s,属于%s范围,较上个月%s。\\n" % (
            row[3], getlevel(row[3]), comparelevel(row[3], row[6]), row[2], getlevel(row[2]),
            comparelevel(row[2], row[5]))
            if row[2] < 75:
                ana += "健康值最低分进入中等或者以下范围，说明系统存在健康隐患，建议进行深入分析。\\n"
        if row[0] == "负载分":
            ana += "负载值的平均分为%s,属于%s范围,较上个月,系统负载%s;负载的最高值为%s,属于%s范围,较上个月%s。\\n" % (
            row[3], getloadlevel(row[3]), comparelevel(row[3], row[6]), row[1], getloadlevel(row[2]),
            comparelevel(row[1], row[4]))
            if row[1] > 75:
                ana += "负载值最高分进入较高或者以上范围，说明系统存在负载过高隐患，建议进行深入分析。\\n"
        if row[0] == "性能分":
            ana += "性能值的平均分为%s,属于%s范围,较上个月%s;性能值的最低分为%s,属于%s范围,较上个月%s。\\n" % (
            row[3], getlevel(row[3]), comparelevel(row[3], row[6]), row[2], getlevel(row[2]),
            comparelevel(row[2], row[5]))
            if row[2] < 75:
                ana += "性能值最低分进入中等或者以下范围，说明系统存在性能隐患，建议进行深入分析。\\n"
        if row[0] == "活跃会话数":
            ana += "活跃会话数的平均值为%s,最高值为%s,上个月活跃会话数平均值为%s,最高值为%s,与上个月相比，活跃会话数平均值%s。\\n" % (
            row[3], row[1], row[6], row[4], comparescore(row[3], row[6]))
            if row[3] > 100 or row[3] > row[6] * 2:
                ana += "活跃会话数一般来说会较为稳定，在本月内，活跃会话数异常增长,数据库系统可能存在性能问题或者存在运行安全隐患，建议进行排查。\\n"
        if row[0] == "log file sync":
            ana += "LOG FILE SYNC延时的平均值为%s,最高值为%s。上个月活跃会话平均值为%s,最高值为%s,与上个月相比,LOG FILE SYNC平均延时%s。\\n" % (
            row[3], row[1], row[6], row[4], comparescore(row[3], row[6]))
            if row[3] > 8 or row[3] > float(row[6]) * 1.5:
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
  rpt_metric_value_high,rpt_metric_value_avg,rpt_metric_value_low,
  rpt_metric_value_high_l,rpt_metric_value_avg_l,rpt_metric_value_low_l)
select distinct '{0}' rptid,'{1}' target_id,res.index_name,res.cmas,res.cmis,res.cavs,res.lmas,res.lmis,res.lavs
from (
select coalesce(cm.index_name,lm.index_name) index_name,coalesce(cm.maxscore,0) cmas,
coalesce(cm.minscore,0) cmis,
coalesce(cm.avgscore,0) cavs,
coalesce(lm.maxscore,0) lmas,
coalesce(lm.minscore,0) lmis,
coalesce(lm.avgscore,0) lavs from 
(select 'log file sync' as index_name,r."maxScore" maxscore,r."minScore" minscore,r."avgScore" avgscore 
from r_m_indexdata r where  r.uid='{1}' and 
r.index_id=2184301 and r.begin_time + interval '1 month' between '{2}' and
               '{3}') lm full join
(select 'log file sync' as index_name,r."maxScore" maxscore,r."minScore" minscore,r."avgScore" avgscore 
from r_m_indexdata r where r.uid='{1}' and 
r.index_id=2184301 and r.begin_time between '{2}' and
               '{3}') cm
on lm.index_name=cm.index_name		
union all
select coalesce(cm.index_name,lm.index_name) index_name,coalesce(cm.maxscore,0) cmas,
coalesce(cm.minscore,0) cmis,
coalesce(cm.avgscore,0) cavs,
coalesce(lm.maxscore,0) lmas,
coalesce(lm.minscore,0) lmis,
coalesce(lm.avgscore,0) lavs from 
(select '活跃会话数' as index_name,r."maxScore" maxscore,r."minScore" minscore,r."avgScore" avgscore 
from r_m_indexdata r where  r.uid='{1}' and 
r.index_id=2189147 and r.begin_time + interval '1 month' between '{2}' and
               '{3}') lm
			   full join 
(select '活跃会话数' as index_name,r."maxScore" maxscore,r."minScore" minscore,r."avgScore" avgscore 
from r_m_indexdata r where r.uid='{1}' and 
r.index_id=2189147 and r.begin_time between '{2}' and
               '{3}') cm
on lm.index_name=cm.index_name
union all
select coalesce(cm.index_name,lm.index_name) index_name,coalesce(cm.maxscore,0)cmas,coalesce(cm.minscore,0)cmis,coalesce(cm.avgscore,0)cavs,
coalesce(lm.maxscore,0)lmas,coalesce(lm.minscore,0)lmis,coalesce(lm.maxscore,0)lavs from 
(select case when r.type=1 then '负载分' when r.type=2 then '性能分' end as index_name,avg(r."maxScore") as  maxscore,
avg(r."minScore") as minscore,avg(r."avgScore") as avgscore from r_m_perf_eva r,p_perf_eva p where p.target_id='{1}'
and r.eva_id=p.eva_id /*and use_flag=true*/ and r.begin_time + interval '1 month' between '{2}' and
               '{3}'
group by case when r.type=1 then '负载分' when r.type=2 then '性能分' end) lm full join
(select case when r.type=1 then '负载分' when r.type=2 then '性能分' end as index_name,avg(r."maxScore") as  maxscore,
avg(r."minScore") as minscore,avg(r."avgScore") as avgscore from r_m_perf_eva r,p_perf_eva p where p.target_id='{1}'
and r.eva_id=p.eva_id /*and use_flag=true*/ and r.begin_time between '{2}' and
               '{3}'
group by case when r.type=1 then '负载分' when r.type=2 then '性能分' end
) cm 
on cm.index_name=lm.index_name
union all
select coalesce(cm.index_name,lm.index_name) index_name,coalesce(cm.maxscore,0)cmas,coalesce(cm.minscore,0)cmis,coalesce(cm.avgscore,0)cavs,
coalesce(lm.maxscore,0)lmas,coalesce(lm.minscore,0)lmis,coalesce(lm.maxscore,0)lavs
from 
(select '健康分' as index_name,r."maxScore" maxscore,r."minScore" minscore,r."avgScore" avgscore from r_m_indexdata r where 
 r.index_id=2180400 and uid='{1}' and r.begin_time + interval '1 month' between '{2}' and
               '{3}') lm
 full join
(select '健康分' as index_name,r."maxScore" maxscore,r."minScore" minscore,r."avgScore" avgscore from r_m_indexdata r where 
 r.index_id=2180400 and uid='{1}' and r.begin_time between '{2}' and
               '{3}') cm
on lm.index_name=cm.index_name
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
delete from rpt_finding where rpt_finding_module='basic_runinfo' and rpt_id='{0}' and target_id='{1}';

insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'basic_runinfo' rpt_finding_module,
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

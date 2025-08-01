#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

sys.path.append('/usr/software/knowl')
import DBUtil
import psycopg2
import re
import CommUtil
import PGUtil
import FormatUtil
import ResultCode
import tags


def register(file_name):
    ltag = ['2.2.2', 'DB']
    return tags.register(ltag, file_name)


class Result(object):
    def __str__(self):
        return "\n".join("{}={}".format(k, getattr(self, k))
                         for k in self.__dict__.keys())


def getValue(ora, sql):
    result = ora.execute(sql)
    if (result.code != 0):
        print("msg=" + result.msg)
        sys.exit()
    return result.msg


def parseURL(url):
    pattern = r'(\w+):(\w+)([thin:@/]+)([0-9.]+):(\d+)([:/])(\w+)'
    matchObj = re.match(pattern, url, re.I)
    return matchObj.group(2), matchObj.group(4), matchObj.group(5), matchObj.group(7)


def getOSVal(conn, target_id, bt, et):
    p1 = ""
    result = []
    sql = '''
with res as (
select a.metric_id,a.deduct,a.record_time,a.metric_value,b.target_id,b.total_score
 from h_health_check_detail a,h_health_check b
where a.metric_id in (2189002,2189055,2189112,2189000,2180200,2189001)
  and a.health_check_id = b.health_check_id
  and a.metric_value <> '周期内无有效采样记录'
  /*and b.use_flag = true*/
  and b.target_id = '%s'
  and a.record_time between '%s' and '%s'
) 
select mi.description,
       case when position('，' in mi.remark)=0 then mi.remark 
       else substring(mi.remark,1,position('，' in mi.remark)-1) end remark,
       count(case when res.deduct >0 then res.deduct else null end) cnt,
       coalesce(round(avg(case when res.deduct >0 then res.deduct::numeric else null end),2),0) amv,
       coalesce(max(res.deduct::numeric),0) maxv
  from res,mon_index mi
 where res.metric_id=mi.index_id
   and mi.use_flag =true 
 group by mi.description,case when position('，' in mi.remark)=0 then mi.remark 
       else substring(mi.remark,1,position('，' in mi.remark)-1) end
''' % (target_id, bt, et)

    cursor = getValue(conn, sql)
    results = cursor.fetchall()

    if (len(results) > 0):
        head = ["指标名称（名称）", "指标描述", "扣分次数", "扣分平均值", "扣分最大值"]
        desc = "数据库命中率扣分详情"
        table = CommUtil.createTable(head, results, desc)
        title = "数据库命中率扣分详情分析"
        p1 = FormatUtil.sectionRes(title, table=table)

        result = results

    return p1, result


def getIndVal(conn, index_id, target_id, bt, et):
    pres = ""
    sql = '''
select a.record_time,c.description,a.metric_value,a.deduct
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (%s)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   /*and b.use_flag = true*/
   and b.target_id = '%s'
   and a.record_time between '%s' and '%s'
   and a.metric_id = c.index_id
 order by a.deduct desc,a.record_time desc 
 limit 5
''' % (index_id, target_id, bt, et)

    sql_des = '''
select description
  from mon_index 
 where use_flag = true 
   and index_id = %s
 limit 1
''' % (index_id)

    cursor_des = getValue(conn, sql_des)
    results_des = cursor_des.fetchone()
    if (len(results_des) > 0):
        desname = results_des[0]
    else:
        desname = str(index_id)

    cursor = getValue(conn, sql)
    results = cursor.fetchall()

    if (len(results) > 0):
        head = ["时间", "指标", "值", "扣分"]
        desc = desname + "扣分情况"
        table = CommUtil.createTable(head, results, desc)
        title = desname + "扣分情况"
        pres = FormatUtil.sectionRes(title, table=table)

    return pres


def getSeriousDis(conn, target_id, bt, et):
    psd = ""
    sql = '''
with res as (
select a.record_time,c.description,a.metric_value,a.deduct,d.total_score
  from h_health_check_detail a,h_health_check b,mon_index c,h_model_item_metric d,h_model_item e
 where a.metric_id in (2189002,2189055,2189112,2189000,2180200,2189001)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   /*and b.use_flag = true*/
   and b.target_id = '%s'
   and a.record_time between '%s' and '%s'
   and a.metric_id = c.index_id
   and a.metric_id = d.metric_id
   and d.use_flag = true
   and b.model_id = e.model_id
   and e.use_flag = true
   and d.model_item_id = e.model_item_id
),
resa as
 (select row_number() over(partition by description order by deduct desc,record_time desc) as rn,
         record_time,
         description,
         metric_value,
         deduct
    from res
   where total_score - deduct <= 0
      or deduct > 10)
select record_time, description, metric_value, deduct
  from resa
 where rn <= 5
''' % (target_id, bt, et)

    cursor = getValue(conn, sql)
    results = cursor.fetchall()

    if (len(results) > 0):
        head = ["时间", "指标", "值", "扣分"]
        desc = "严重扣分情况"
        table = CommUtil.createTable(head, results, desc)
        title = "严重扣分情况分析"
        psd = FormatUtil.sectionRes(title, table=table)

    return psd


def getVal(index_id, conn, target_id, bt, et):
    sql = '''
select coalesce(max(a.metric_value::numeric),0)
  from h_health_check_detail a,h_health_check b 
 where a.metric_id in (%s)
   and a.health_check_id = b.health_check_id
   /*and b.use_flag = true*/
   and b.target_id = '%s'
   and a.record_time between '%s' and '%s'
   and a.metric_value !='周期内无有效采样记录'
''' % (index_id, target_id, bt, et)
    cursor = getValue(conn, sql)
    results = cursor.fetchone()
    pval = results[0]
    return pval


def getCibVal(conn, target_id, bt, et):
    pcval = 0
    sql = '''
    select cib_value 
      from p_oracle_cib
     where cib_name='log_buffer'
       and target_id = '%s'
       and record_time between '%s' and '%s' 
       and index_id = 2201010
     order by record_time desc limit 1
''' % (target_id, bt, et)

    cursor = getValue(conn, sql)
    results = cursor.fetchone()
    if not results is None:
        pcval = results[0]

    return pcval


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
    ##os info

    targetid = dbInfo['targetId']
    begintime = dbInfo['start_time']
    endtime = dbInfo['end_time']

    rpt_id = dbInfo['rptid']

    pg = PGUtil.Postgre(dbip, username, password, pgport, dbname)

    try:
        result = ""
        # ora = orautil.Oracle(host, usr, pwd, port, database)

        ##删除已有数据
        sqldel1 = """delete from rpt_scope_detail where rpt_id='{0}' and target_id='{1}' and rpt_scope_category='H_HITE'
""".format(rpt_id, targetid)
        pg.execute(sqldel1)
        sqldel2 = """delete from rpt_scope_ded_history where rpt_id='{0}' and target_id='{1}' and rpt_scope_category='H_HITE'
""".format(rpt_id, targetid)
        pg.execute(sqldel2)
        sqldel3 = """delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module in ('health_hite_metric','health_hite_score')
""".format(rpt_id, targetid)
        pg.execute(sqldel3)

        ##数据库命中率入库
        insql = '''
insert into rpt_scope_detail(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_note,
                                                        rpt_scope_count,rpt_scope_ded_avg,rpt_scope_ded_max)    
with res as (
select a.metric_id,a.deduct,a.record_time,a.metric_value,b.target_id,b.total_score,a.iname
 from h_health_check_detail a,h_health_check b
where 
  a.metric_id in (2189002,2189055,2189112,2189000,2180200,2189001)
  and a.health_check_id = b.health_check_id
  and a.metric_value <> '周期内无有效采样记录'
  /*and b.use_flag = true*/
  and b.target_id = '{0}'
  and a.deduct<>0
  and a.record_time between '{1}' and '{2}'
) 
select '{3}' rptid,res.target_id target_id,'H_HITE' rsc,mi.index_id,res.iname,
       mi.description,
       mi.remark,          
       count(case when res.deduct >0 then res.deduct else null end) cnt,
       coalesce(round(avg(case when res.deduct >0 then res.deduct::numeric else null end),2),0) amv,
       coalesce(max(res.deduct::numeric),0) maxv
  from res,mon_index mi
 where res.metric_id=mi.index_id
   and mi.use_flag =true 
 group by res.target_id,mi.index_id,res.iname,mi.description,mi.remark
'''.format(targetid, begintime, endtime, rpt_id)
        pg.execute(insql)

        res_p1, res_list = getOSVal(pg, targetid, begintime, endtime)

        for res in res_list:
            if res[0].startswith("Redo Allocation Hit Ratio"):
                if res[2] > 0:
                    r1 = round(getVal(2189016, pg, targetid, begintime, endtime) / 1024 / 1024, 2)
                    if r1 > 4:
                        r1rs = "REDO量特大，建议检查应用系统是否存在批量操作数据的情况，如果经常性出现REDO量超大的情况，建议优化应用系统，减少REDO量"
                    elif r1 > 2 and r1 <= 4:
                        r1rs = "REDO量较大"
                    elif r1 > 1 and r1 <= 2:
                        r1rs = "REDO量正常"
                    else:
                        r1rs = "REDO量较小"

                    result = '''
说明REDO的性能存在问题，如果该现象比较严重会导致系统性能严重下降，甚至引起系统不稳定、宕机。
分析内容：
1、本系统的每秒REDO量的最高值为：''' + str(r1) + '''M/秒，''' + r1rs + "\\n"

                    r2 = round(getVal(2184005, pg, targetid, begintime, endtime), 2)
                    if r2 > 10:
                        r2rs = "日志写性能存在较为严重的问题，REDO LOG写性能存在问题"
                    elif r2 > 4 and r2 <= 10:
                        r2rs = "日志写性能不佳，REDO LOG写性能存在问题"
                    elif r2 > 2 and r2 <= 4:
                        r2rs = "日志写性能一般，REDO LOG写性能存在问题"
                    else:
                        r2rs = "日志写性能较好，REDO LOG写性能不存在问题"

                    result += '''
2、本系统的LOG FILE PARALLEL WRITE的响应时间的最大值为：''' + str(r2) + '''ms，''' + r2rs + "\\n"

                    r3 = round(getVal(2189022, pg, targetid, begintime, endtime), 2)
                    if r3 > 10000:
                        r3rs = "超大，建议优化应用，使用批量提交等手段减少每秒提交的数量"
                    elif r3 > 5000 and r3 <= 10000:
                        r3rs = "较大，建议优化应用，使用批量提交等手段减少每秒提交的数量"
                    elif r3 > 1000 and r3 <= 5000:
                        r3rs = "中等"
                    else:
                        r3rs = "较小"

                    result += '''
3、每秒用户提交数的最大值为：''' + str(r3) + '''，该指标''' + r3rs + "\\n"

                    r4 = round(float(getCibVal(pg, targetid, begintime, endtime)) / 1024 / 1024, 2)
                    if r4 < 100 and r3 > 1000:
                        r4rs = "建议分析LOG BUFFER，加大LOG_BUFFER参数值有助于改善REDO 命中率不高的问题"
                    else:
                        r4rs = "LOG_BUFFER参数设置合理"

                    result += '''
4、本系统的LOG_BUFFER大小为：''' + str(r4) + '''M，''' + r4rs + "\\n"

                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'health_hite_metric' rpt_finding_module,
0 rpt_finding_type,'2189002' rpt_sub_id,'' iname,
'Redo分配命中率出现扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)

                    ##result += getIndVal(pg, 2189002, targetid, begintime, endtime)
                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_HITE' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2189002)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.record_time between '{2}' and '{3}'
   and a.metric_id = c.index_id
 order by a.deduct desc,a.metric_value::numeric asc 
 limit 20
'''.format(rpt_id, targetid, begintime, endtime)
                    pg.execute(insql_mf)

            elif res[0].startswith("Soft Parse Ratio"):
                if res[2] > 0:
                    result = '''
软解析比例过低会导致该项扣分，软解析比例过低一般情况下有两种可能：
一、应用软件没有使用绑定变量，导致SQL共享比例过低，需要通过优化应用来解决该问题；
二、可能是共享池设置偏小，可以通过加大共享池进行改善，如果SGA设置为自动管理，则SGA不存在不足的情况下，系统会自动扩展共享池满足系统需求。如果当前系统没有出现过多共享池闩锁争用，则该问题可以暂时忽略。
'''
                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,2 rpt_finding_id,'health_hite_metric' rpt_finding_module,
0 rpt_finding_type,'2189055' rpt_sub_id,'' iname,
'Soft Parse Ratio命中率出现扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)
                    ##result += getIndVal(pg, 2189055, targetid, begintime, endtime)
                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_HITE' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2189055)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.record_time between '{2}' and '{3}'
   and a.metric_id = c.index_id
 order by a.deduct desc,a.metric_value::numeric asc
 limit 20
'''.format(rpt_id, targetid, begintime, endtime)
                    pg.execute(insql_mf)

            elif res[0].startswith("Library Cache Hit Ratio"):
                if res[2] > 0:
                    result = '''
共享池命中率过低导致该扣分，库缓冲命中率过低一般情况下有两种可能：
一、应用软件没有使用绑定变量，导致SQL共享比例过低，需要通过优化应用来解决该问题；
二、可能是共享池设置偏小，可以通过加大共享池进行改善，如果SGA设置为自动管理，则SGA不存在不足的情况下，系统会自动扩展共享池满足系统需求。如果当前系统没有出现过多共享池闩锁争用，则该问题可以暂时忽略。
'''
                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,3 rpt_finding_id,'health_hite_metric' rpt_finding_module,
0 rpt_finding_type,'2189112' rpt_sub_id,'' iname,
'Library Cache Hit Ratio命中率出现扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)
                    ##result += getIndVal(pg, 2189112, targetid, begintime, endtime)
                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_HITE' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2189112)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.record_time between '{2}' and '{3}'
   and a.metric_id = c.index_id
 order by a.deduct desc,a.metric_value::numeric asc
 limit 20
'''.format(rpt_id, targetid, begintime, endtime)
                    pg.execute(insql_mf)

            elif res[0].startswith("Buffer Cache Hit Ratio"):
                if res[2] > 0:
                    result = '''
数据库缓冲命中率过低导致该扣分，数据库缓冲命中率过低往往由于应用频繁扫描数据库表或者DB CACHE设置过低导致。
对于OLTP系统来说，数据库库缓冲命中率高于95%是可以接受的，对于OLAP系统来说，数据库缓冲命中率高于80%是可以接受的。
提高数据库缓冲命中率，建议分析与优化物理读较高的SQL。
'''
                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,4 rpt_finding_id,'health_hite_metric' rpt_finding_module,
0 rpt_finding_type,'2189000' rpt_sub_id,'' iname,
'Buffer Cache Hit Ratio命中率出现扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    # print(ismf)
                    pg.execute(ismf)
                    ##result += getIndVal(pg, 2189000, targetid, begintime, endtime)
                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_HITE' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2189000)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.record_time between '{2}' and '{3}'
   and a.metric_id = c.index_id
 order by a.deduct desc,a.metric_value::numeric asc
 limit 20
'''.format(rpt_id, targetid, begintime, endtime)
                    # print(insql_mf)
                    pg.execute(insql_mf)

            elif res[0].startswith("Latch hit ratio"):
                if res[2] > 0:
                    result = '''
是由于闩锁命中率较低导致的，一般来说数据库的闩锁命中率低于99%是不可接受的。
闩锁是Oracle内部数据结构的串行锁，闩锁命中率过低会导致数据库运行性能下降，严重时会导致数据库出现较为严重的性能问题，甚至宕机。
如果闩锁命中率<99%：建议进行闩锁专项分析，查找闩锁命中率过低的原因。
'''
                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,5 rpt_finding_id,'health_hite_metric' rpt_finding_module,
0 rpt_finding_type,'2180200' rpt_sub_id,'' iname,
'Buffer Cache Hit Ratio命中率出现扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)
                    ##result += getIndVal(pg, 2180200, targetid, begintime, endtime)
                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_HITE' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2180200)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.record_time between '{2}' and '{3}'
   and a.metric_id = c.index_id
 order by a.deduct desc,a.metric_value::numeric asc
 limit 20
'''.format(rpt_id, targetid, begintime, endtime)
                    pg.execute(insql_mf)

            elif res[0].startswith("Memory Sorts Ratio"):
                if res[2] > 0:
                    result += '''
是由于内存排序的比例过低导致。Oracle通过pga_aggregate_target参数来管理排序内存，当出现了特大型的排序无法满足内存排序的需求的时候，会出现磁盘排序操作，通过临时表空间存储排序的临时数据。出现磁盘排序会导致该类操作的SQL执行性能下降，因此需要尽可能减少磁盘排序的数量。
建议通过V_$PGA_TARGET_ADVICE查看PGA_AGGREGATE_TARGET的建议值，如果物理内存足够的情况下加大该参数，也可以通过AWR报告的相关章节查看参数建议。
'''
                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,6 rpt_finding_id,'health_hite_metric' rpt_finding_module,
0 rpt_finding_type,'2189001' rpt_sub_id,'' iname,
'Memory Sorts Ratio命中率出现扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)
                    ##result += getIndVal(pg, 2189001, targetid, begintime, endtime)
                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_HITE' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2189001)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.record_time between '{2}' and '{3}'
   and a.metric_id = c.index_id
 order by a.deduct desc,a.metric_value::numeric
 limit 20
'''.format(rpt_id, targetid, begintime, endtime)
                    pg.execute(insql_mf)

        """ppsd = getSeriousDis(pg, targetid, begintime, endtime)
        if ppsd != "":
            result = "严重问题发现（存在一次性扣分超过10分或者全扣光的情况）"
            ismf='''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,7 rpt_finding_id,'health_hite_score' rpt_finding_module,
0 rpt_finding_type,'' rpt_sub_id,'' iname,
'严重问题发现（存在一次性扣分超过10分或者全扣光的情况）' rpt_finding_label,
'致命' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id,targetid,result)
            pg.execute(ismf)"""

    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

    # except Exception as e:
    #    errorInfo = str(e)
    #    print("异常：" + errorInfo)

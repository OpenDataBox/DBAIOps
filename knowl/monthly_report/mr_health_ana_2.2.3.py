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
    ltag = ['2.2.3', 'DB']
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
where a.metric_id in (2189092,2189006,2189003,2189046,2189044,2189016,2189018,2189026,2189004,2189058,2189100,2189159,2189121,2189030)
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
    # print(sql)

    cursor = getValue(conn, sql)
    results = cursor.fetchall()

    if (len(results) > 0):
        head = ["指标名称（名称）", "指标描述", "扣分次数", "扣分平均值", "扣分最大值"]
        desc = "数据库负载扣分详情"
        table = CommUtil.createTable(head, results, desc)
        title = "数据库负载扣分详情分析"
        p1 = FormatUtil.sectionRes(title, table=table)

        result = results

    return p1, result


def getIndValmv(conn, index_id, target_id, bt, et, mv):
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
   and a.metric_value::numeric >= %s*3
 order by a.deduct desc,a.record_time desc 
 limit 5
''' % (index_id, target_id, bt, et, mv)

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


def getIndVal(conn, index_id, target_id, bt, et):
    pres = ""
    sql = '''
select a.record_time,c.description,a.metric_value,a.deduct
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2189006)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   /*and b.use_flag = true*/
   and b.target_id = '%s'
   and a.record_time between '%s' and '%s'
   and a.metric_id = c.index_id
 order by a.deduct desc,a.record_time desc 
 limit 5
''' % (target_id, bt, et)

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
 where a.metric_id in (2189092,2189006,2189003,2189046,2189044,2189016,2189018,2189026,2189004,2189058,2189100,2189159,2189121,2189030)
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
        desc = "数据库负载严重扣分情况"
        table = CommUtil.createTable(head, results, desc)
        title = "数据库负载严重扣分情况分析"
        psd = FormatUtil.sectionRes(title, table=table)

    return psd


def getVal(index_id, conn, target_id, bt, et):
    pval = 0
    sql = '''
    select coalesce(round(avg(a.metric_value::numeric),2),0)
  from h_health_check_detail a,h_health_check b 
 where a.metric_id in (%s)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   /*and b.use_flag = true*/
   and b.target_id = '%s'
   and a.record_time between '%s' and '%s'
''' % (index_id, target_id, bt, et)

    cursor = getValue(conn, sql)
    results = cursor.fetchone()
    pval = results[0]
    return pval


def getCibVal(cib_name, conn, target_id, bt, et):
    pcval = 0
    sql = '''
    select cib_value
      from p_oracle_cib 
     where target_id = '%s' 
       and cib_name = '%s'
       /*and record_time between '%s' and '%s' */
     order by record_time desc 
     limit 1
''' % (target_id, cib_name, bt, et)

    cursor = getValue(conn, sql)
    results = cursor.fetchone()
    if not results is None:
        pcval = results[0]

    return pcval


def getlastdt(conn, bt, et):
    pldt = []
    sql = '''
    select to_date('%s','yyyy-mm-dd hh24:mi:ss') - interval '1 months' as bt,
    to_date('%s','yyyy-mm-dd hh24:mi:ss') - interval '1 months' as et
''' % (bt, et)

    cursor = getValue(conn, sql)
    results = cursor.fetchone()

    pldt = results

    return pldt


def getOraCur(conn, target_id, bt, et):
    poc = ""
    sql = """
select
  'session_cached_cursors'  parameter,
  cib_value  val,
  case when cib_value=0 then 'n/a'
  else 100 * round(used / cib_value,2)||'%' end  usage
from
(select value::numeric used from mon_indexdata 
where index_id = 2187002
and uid = '{0}' 
and record_time between '{1}' and '{2}' 
order by record_time desc limit 1) a,
(
select cib_value::numeric cib_value
      from p_oracle_cib
     where cib_name='session_cached_cursors'
       and target_id = '{0}'
       and record_time between '{1}' and '{2}' 
       and index_id = 2201010
     order by record_time desc limit 1	 ) b

union all 

select
  'open_cursors'  parameter,
  cib_value  val,
  case when cib_value=0 then 'n/a'
  else 100 * round(used / cib_value,2)||'%' end  usage
from (	
select  value::numeric used from mon_indexdata_his 
where index_id = 2187001
and uid = '{0}'
and record_time between '{1}' and '{2}' 
order by record_time desc limit 1)a,
(
select cib_value::numeric cib_value 
      from p_oracle_cib
     where cib_name='open_cursors'
       and target_id = '{0}'
       --and record_time between '{1}' and '{2}' 
       and index_id = 2201010
     order by record_time desc limit 1) b
""".format(target_id, bt, et)

    cursor = getValue(conn, sql)
    results = cursor.fetchall()

    if (len(results) > 0):
        head = ["参数", "值", "使用率"]
        desc = "数据库Cursor设置分析"
        table = CommUtil.createTable(head, results, desc)
        title = "数据库Cursor设置分析"
        poc = FormatUtil.sectionRes(title, table=table)

    return poc


def getTopTime(conn, index_id, target_id, bt, et):
    ptt = ""
    sql = '''
with res as (
select a.record_time,c.description,a.metric_value
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (%s)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   /*and b.use_flag = true*/
   and b.target_id = '%s'
   and a.record_time between '%s' and '%s'
   and a.metric_id = c.index_id
),res1 as (
select to_char(record_time,'yyyy-mm-dd hh24:00:00') rtime,
	   round(avg(metric_value::numeric),2) mv
  from res 
 group by to_char(record_time,'yyyy-mm-dd hh24:00:00')
),res2 as (
select extract(hour from rtime::timestamp) ht,mv 
  from res1
 order by 1
),res3 as (
select ht,sum(mv) over(partition by ht)/sum(mv) over() dd
  from res2),res4 as (
  select ht,sum(dd) dd
  from res3
  group by ht
  order by 2 desc  
  limit 5
)
select concat(ht,':00') ht from res4
''' % (index_id, target_id, bt, et)

    cursor = getValue(conn, sql)
    results = cursor.fetchall()

    if (len(results) > 0):
        head = ["时间段"]
        desc = "每秒物理写过高时间段规律性分析"
        table = CommUtil.createTable(head, results, desc)
        title = "每秒物理写过高时间段规律性分析"
        ptt = FormatUtil.sectionRes(title, table=table)

    return ptt


def getLessTime(conn, index_id, target_id, bt, et):
    plt = ""
    sql = '''
with res as (
select a.record_time,c.description,a.metric_value
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (%s)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   /*and b.use_flag = true*/
   and b.target_id = '%s'
   and a.record_time between '%s' and '%s'
   and a.metric_id = c.index_id
),res1 as (
select to_char(record_time,'yyyy-mm-dd hh24:00:00') rtime,
           round(avg(metric_value::numeric),2) mv
  from res 
 group by to_char(record_time,'yyyy-mm-dd hh24:00:00')
),res2 as (
select extract(hour from rtime::timestamp) ht,mv 
  from res1
 order by 1
),res3 as (
select ht,sum(mv) over(partition by ht)/sum(mv) over() dd
  from res2),res4 as (
  select ht,sum(dd) dd
  from res3
  group by ht
  order by 2 asc
  limit 5
)
select concat(ht,':00') ht from res4
''' % (index_id, target_id, bt, et)

    cursor = getValue(conn, sql)
    results = cursor.fetchall()

    if (len(results) > 0):
        head = ["时间段"]
        desc = "每秒物理写过高时间段偶然性分析"
        table = CommUtil.createTable(head, results, desc)
        title = "每秒物理写过高时间段偶然性分析"
        plt = FormatUtil.sectionRes(title, table=table)

    return plt


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

    lmbegintime, lmendtime = getlastdt(pg, begintime, endtime)

    try:
        ##result = "SCREEN_BEGIN问题与发现：SCREEN_END"
        result = ""
        ##删除已有数据
        sqldel1 = """delete from rpt_scope_detail where rpt_id='{0}' and target_id='{1}' and rpt_scope_category='H_LOAD'
""".format(rpt_id, targetid)
        pg.execute(sqldel1)
        sqldel2 = """delete from rpt_scope_ded_history where rpt_id='{0}' and target_id='{1}' and rpt_scope_category='H_LOAD'
""".format(rpt_id, targetid)
        pg.execute(sqldel2)
        sqldel3 = """delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module in ('health_load_metric','health_load_score')
""".format(rpt_id, targetid)
        pg.execute(sqldel3)
        ##数据库负载入库
        insql = '''
insert into rpt_scope_detail(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_note,
                                                        rpt_scope_count,rpt_scope_ded_avg,rpt_scope_ded_max)    
with res as (
select a.metric_id,a.deduct,a.record_time,a.metric_value,b.target_id,b.total_score,a.iname
 from h_health_check_detail a,h_health_check b
where 
  a.metric_id in (2189092,2189006,2189003,2189046,2189044,2189016,2189018,2189026,2189004,2189058,2189100,2189159,2189121,2189030)
  and a.health_check_id = b.health_check_id
  and a.metric_value <> '周期内无有效采样记录'
  /*and b.use_flag = true*/
  and b.target_id = '{0}'
  and a.deduct<>0
  and a.record_time between '{1}' and '{2}'
) 
select '{3}' rptid,res.target_id target_id,'H_LOAD' rsc,mi.index_id,res.iname,
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

        # ora = orautil.Oracle(host, usr, pwd, port, database)
        res_p1, res_list = getOSVal(pg, targetid, begintime, endtime)

        for res in res_list:
            # print(res)
            if res[0].startswith("Physical Read Total IO Requests Per Sec"):
                if res[2] > 0:
                    lm = getVal(2189092, pg, targetid, lmbegintime, lmendtime)
                    bm = getVal(2189092, pg, targetid, begintime, endtime)
                    if lm > bm:
                        rlb = "有所下降"
                    elif lm < bm:
                        rlb = "有所上升"
                    else:
                        rlb = "基本持平"

                    result = '''
存在大量的物理读存在。上月该指标的平均值为：''' + str(lm) + '''，本月该指标的平均值为：''' + str(bm) + '''，本月与上月该指标''' + rlb + '''。如果该指标在某些时间段出现了超过平均水平3倍以上的情况，建议与开发商共同检查，分析原因。
出现问题的时间段如下：
'''

                    ##result += getIndValmv(pg, 2189092, targetid, begintime, endtime, bm)
                    result += '''
建议进行下列检查：
A) SGA是否配置不足，建议通过AWR报告分析是否可以通过加大DB CACHE来减少物理读的总量，或者通过设置KEEP POOL等减少热点数据的物理读
B) 可能存在一些未优化好的高开销SQL，进行了大量的全表扫描或者全索引扫描，建议检查执行时间较长和物理读较大的SQL，并进行分析与优化
'''
                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'health_load_metric' rpt_finding_module,
0 rpt_finding_type,'2189092' rpt_sub_id,'' iname,
'Physical Read Total IO Requests Per Sec存在扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)

                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_LOAD' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2189092)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.record_time between '{2}' and '{3}'
   and a.metric_id = c.index_id
   --and a.metric_value::numeric >= {4}*3
 order by a.deduct desc,a.metric_value::numeric desc
 limit 20
'''.format(rpt_id, targetid, begintime, endtime, bm)
                    pg.execute(insql_mf)

            elif res[0].startswith("Physical Reads Per Sec"):
                if res[2] > 0:
                    lm = getVal(2189004, pg, targetid, lmbegintime, lmendtime)
                    bm = getVal(2189004, pg, targetid, begintime, endtime)
                    if lm > bm:
                        rlb = "有所下降"
                    elif lm < bm:
                        rlb = "有所上升"
                    else:
                        rlb = "基本持平"

                    result = '''
存在大量的物理读存在。上月该指标的平均值为：''' + str(lm) + '''，本月该指标的平均值为：''' + str(bm) + '''，本月与上月该指标''' + rlb + '''。如果该指标在某些时>间段出现了超过平均水平3倍以上的情况，建议与开发商共同检查，分析原因。
出现问题的时间段如下：
'''
                    ##result += getIndValmv(pg, 2189004, targetid, begintime, endtime, bm)
                    result += '''
建议进行下列检查：
A) SGA是否配置不足，建议通过AWR报告分析是否可以通过加大DB CACHE来减少物理读的总量，或者通过设置KEEP POOL等减少热点数据的物理读
B) 可能存在一些未优化好的高开销SQL，进行了大量的全表扫描或者全索引扫描，建议检查执行时间较长和物理读较大的SQL，并进行分析与优化
'''

                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,2 rpt_finding_id,'health_load_metric' rpt_finding_module,
0 rpt_finding_type,'2189004' rpt_sub_id,'' iname,
'Physical Reads Per Sec存在扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)

                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_LOAD' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2189004)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.record_time between '{2}' and '{3}'
   and a.metric_id = c.index_id
   --and a.metric_value::numeric >= {4}*3
 order by a.deduct desc,a.metric_value::numeric desc 
 limit 20
'''.format(rpt_id, targetid, begintime, endtime, bm)
                    pg.execute(insql_mf)

            elif res[0].startswith("Physical Writes Per Sec"):
                if res[2] > 0:
                    result = '''
在某些时段，系统存在较多的物理写操作，可能由于下面原因导致，建议进行后续分析排查：
A) 如果规律性的存在：系统本身在某些时段存在大量规律性的写操作，比如做数据归档、数据批量导入、数据批量修改等操作，建议从应用角度予以确认。存在规律性物理写较高的时间段如下：
'''

                    result += \
                    getTopTime(pg, 2189006, targetid, begintime, endtime).split("TNAME_END")[1].split("TABLE_END")[
                        0].replace("</td></tr><tr><td>", "\n").replace("<table><tr><td>", "").replace(
                        "</td></tr></table>", "")
                    result += '''
B) 偶然性发生:可能存在偶发性的数据批量归档、数据导入、数据批量修改等操作，出现该问题的时间为：
'''

                    result += \
                    getLessTime(pg, 2189006, targetid, begintime, endtime).split("TNAME_END")[1].split("TABLE_END")[
                        0].replace("</td></tr><tr><td>", "\n").replace("<table><tr><td>", "").replace(
                        "</td></tr></table>", "")
                    result += '''
建议排查相关时间段是否存在类似操作。如果无法确认，可以通过LOGMINER工具进行相关分析（需要数据库处于归档模式）
C) 建议排查SGA设置情况，通过AWR分析是否可以通过加到DB CACHE减少高峰期物理写的数量
'''
                    # result += getIndVal(pg, 2189006, targetid, begintime, endtime)

                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,3 rpt_finding_id,'health_load_metric' rpt_finding_module,
0 rpt_finding_type,'2189006' rpt_sub_id,'' iname,
'Physical Writes Per Sec存在扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)

                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_LOAD' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2189006)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.record_time between '{2}' and '{3}'
   and a.metric_id = c.index_id
 order by a.deduct desc,a.metric_value::numeric desc
 limit 20
'''.format(rpt_id, targetid, begintime, endtime)
                    pg.execute(insql_mf)

            elif res[0].startswith("Physical Write Total IO Requests Per Sec"):
                if res[2] > 0:
                    result = '''
在某些时段，系统存在较多的物理写操作，可能由于下面原因导致，建议进行后续分析排查：
A) 如果规律性的存在：系统本身在某些时段存在大量规律性的写操作，比如做数据归档、数据批量导入、数据批量修改等操作，建议从应用角度予以确认。存在规律性>物理写较高的时间段如下：
'''
                    result += \
                    getTopTime(pg, 2189100, targetid, begintime, endtime).split("TNAME_END")[1].split("TABLE_END")[
                        0].replace("</td></tr><tr><td>", "\n").replace("<table><tr><td>", "").replace(
                        "</td></tr></table>", "")
                    result += '''
B) 偶然性发生：可能存在偶发性的数据批量归档、数据导入、数据批量修改等操作，出现该问题的时间为：
'''
                    result += \
                    getLessTime(pg, 2189100, targetid, begintime, endtime).split("TNAME_END")[1].split("TABLE_END")[
                        0].replace("</td></tr><tr><td>", "\n").replace("<table><tr><td>", "").replace(
                        "</td></tr></table>", "")
                    result += '''
建议排查相关时间段是否存在类似操作。如果无法确认，可以通过LOGMINER工具进行相关分析（需要数据库处于归档模式）
C) 建议排查SGA设置情况，通过AWR分析是否可以通过加到DB CACHE减少高峰期物理写的数量
'''
                    ##result += getIndVal(pg, 2189100, targetid, begintime, endtime)

                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,4 rpt_finding_id,'health_load_metric' rpt_finding_module,
0 rpt_finding_type,'2189100' rpt_sub_id,'' iname,
'Physical Write Total IO Requests Per Sec存在扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)

                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_LOAD' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2189100)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.record_time between '{2}' and '{3}'
   and a.metric_id = c.index_id
 order by a.deduct desc,a.metric_value::numeric desc 
 limit 20
'''.format(rpt_id, targetid, begintime, endtime)
                    pg.execute(insql_mf)

            elif res[0].startswith("User Transaction Per Sec"):
                if res[2] > 0:
                    lm = getVal(2189003, pg, targetid, lmbegintime, lmendtime)
                    bm = getVal(2189003, pg, targetid, begintime, endtime)
                    if lm > bm:
                        rlb = "有所下降"
                    elif lm < bm:
                        rlb = "有所上升"
                    else:
                        rlb = "基本持平"

                    result = '''
系统可能存在较大量的并发事务。上月该指标的平均值为：''' + str(lm) + '''，本月该指标的平均值为：''' + str(bm) + '''，本月与上月该指标''' + str(rlb) + '''。如果该指标在某些时间段出现了超过平均水平3倍以上的情况，建议与开发商共同检查，分析原因。
出现问题的时间段如下：
'''
                    ##result += getIndValmv(pg, 2189003, targetid, begintime, endtime, bm)
                    result += '''
建议进行后续分析：
A) 如果问题出现是规律性的：应用系统可能存在规律性的并发交易量较大的情况，建议和应用开发商确认。
B) 如果问题出现是非规律性的：应用系统可能出现非规律性的并发交易量较大情况，建议与应用开发商确认是正常现象还是由于软件BUG导致，或者数据维护操作导致，排除软件BUG的可能性。
'''

                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,5 rpt_finding_id,'health_load_metric' rpt_finding_module,
0 rpt_finding_type,'2189003' rpt_sub_id,'' iname,
'User Transaction Per Sec存在扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    # print(ismf)
                    pg.execute(ismf)

                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_LOAD' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2189003)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.record_time between '{2}' and '{3}'
   and a.metric_id = c.index_id
   --and a.metric_value::numeric >= {4}*3
 order by a.deduct desc,a.metric_value::numeric desc 
 limit 20
'''.format(rpt_id, targetid, begintime, endtime, bm)
                    # print(insql_mf)
                    pg.execute(insql_mf)

            elif res[0].startswith("Hard Parse Count Per Sec"):
                if res[2] > 0:
                    lm = getVal(2189046, pg, targetid, lmbegintime, lmendtime)
                    bm = getVal(2189046, pg, targetid, begintime, endtime)
                    if lm > bm:
                        rlb = "有所下降"
                    elif lm < bm:
                        rlb = "有所上升"
                    else:
                        rlb = "基本持平"
                    result = '''
系统中的SQL解析数量过多，导致共享池争用的可能性较大，如果特别严重将严重影响数据库性，甚至导致数据库出现不稳定情况。
上月该指标的平均值为：''' + str(lm) + '''，本月该指标的平均值为：''' + str(bm) + '''，本月与上月该指标''' + rlb + '''。
如果该指标在某些时间段出现了超过平均水平3倍以上的情况，建议与开发商共同检查，分析原因。
出现问题的时间段如下：
'''
                    ##result += getIndValmv(pg, 2189046, targetid, begintime, endtime, bm)

                    result += '''
如果问题较为严重，可进行下列分析：
A) 分析共享池是否充足，确保共享池被设置为足够大，长期保留10%以上的空闲空间。并且不存在较为严重的LIBRARY CACHE/ROW CACHE相关等待。
B) OPEN_CURSORS参数与SESSION_CACHED_CURSORS参数设置过低，导致并发量较大的时候CURSOR共享不足 。'''

                    pcrc = getOraCur(pg, targetid, begintime, endtime)
                    if pcrc != "":
                        result += pcrc
                        result += '''
如果OPEN_CURSORS或者SESSION_CACHED_CURSORS参数的使用比例大于等于99%,则建议加大这两个参数
C) 应用系统可能存在不够优化的现象，大量SQL没有使用绑定变量或者由于某个数据库BUG而没有共享。建议通过AWR报告检查执行次数较多和解析次数较多的SQL，分析是否存在类似问题
'''
                    else:
                        result += '''
C) 应用系统可能存在不够优化的现象，大量SQL没有使用绑定变量或者由于某个数据库BUG而没有共享。建议通过AWR报告检查执行次数较多和解析次数较多的SQL，分析>是否存在类似问题
'''

                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,6 rpt_finding_id,'health_load_metric' rpt_finding_module,
0 rpt_finding_type,'2189046' rpt_sub_id,'' iname,
'User Transaction Per Sec存在扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)

                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_LOAD' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2189046)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.record_time between '{2}' and '{3}'
   and a.metric_id = c.index_id
   --and a.metric_value::numeric >= {4}*3
 order by a.deduct desc,a.metric_value::numeric desc 
 limit 20
'''.format(rpt_id, targetid, begintime, endtime, bm)
                    pg.execute(insql_mf)

            elif res[0].startswith("Total Parse Count Per Sec"):
                if res[2] > 0:
                    lm = getVal(2189044, pg, targetid, lmbegintime, lmendtime)
                    bm = getVal(2189044, pg, targetid, begintime, endtime)
                    if lm > bm:
                        rlb = "有所下降"
                    elif lm < bm:
                        rlb = "有所上升"
                    else:
                        rlb = "基本持平"

                    result = '''
系统中的SQL解析数量过多，导致共享池争用的可能性较大，如果特别严重将严重影响数据库性，甚至导致数据库出现不稳定情况。
上月该指标的平均值为：''' + str(lm) + '''，本月该指标的平均值为：''' + str(bm) + '''，本月与上月该指标''' + rlb + '''。
如果该指标在某些时间段出现了超过平均水平3倍以上的情况，建议与开发商共同检查，分析原因。
出现问题的时间段如下：
'''
                    ##result += getIndValmv(pg, 2189044, targetid, begintime, endtime, bm)

                    result += '''SCREEN_BEGIN
如果问题较为严重，可进行下列分析：
A) 分析共享池是否充足，确保共享池被设置为足够大，长期保留10%以上的空闲空间。并且不存在较为严重的LIBRARY CACHE/ROW CACHE相关等待
B) OPEN_CURSORS参数与SESSION_CACHED_CURSORS参数设置过低，导致并发量较大的时候CURSOR共享不足 。'''
                    pcrc = getOraCur(pg, targetid, begintime, endtime)
                    if pcrc != "":
                        result += pcrc
                        result += '''
如果OPEN_CURSORS或者SESSION_CACHED_CURSORS参数的使用比例大于等于99%,则建议加大这两个参数
C) 应用系统可能存在不够优化的现象，大量SQL没有使用绑定变量或者由于某个数据库BUG而没有共享。建议通过AWR报告检查执行次数较多和解析次数较多的SQL，分析>是否存在类似问题
'''
                    else:
                        result += '''
C) 应用系统可能存在不够优化的现象，大量SQL没有使用绑定变量或者由于某个数据库BUG而没有共享。建议通过AWR报告检查执行次数较多和解析次数较多的SQL，分析>是否存在类似问题
'''

                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,7 rpt_finding_id,'health_load_metric' rpt_finding_module,
0 rpt_finding_type,'2189044' rpt_sub_id,'' iname,
'User Transaction Per Sec存在扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)

                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_LOAD' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2189044)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.record_time between '{2}' and '{3}'
   and a.metric_id = c.index_id
   --and a.metric_value::numeric >= {4}*3
 order by a.deduct desc,a.metric_value::numeric desc 
 limit 20
'''.format(rpt_id, targetid, begintime, endtime, bm)
                    pg.execute(insql_mf)

            elif res[0].startswith("Redo Generated Per Sec"):
                if res[2] > 0:
                    lm = getVal(2189016, pg, targetid, lmbegintime, lmendtime)
                    bm = getVal(2189016, pg, targetid, begintime, endtime)
                    if lm > bm:
                        rlb = "有所下降"
                    elif lm < bm:
                        rlb = "有所上升"
                    else:
                        rlb = "基本持平"

                    result = '''
系统存在REDO LOG产生量过大的现象。上月该指标的平均值为：''' + str(lm) + '''，本月该指标的平均值为：''' + str(bm) + '''，本月与上月该指标''' + rlb + '''。如果该指标在某些时间段出现了超过平均水平3倍以上的情况，建议与开发商共同检查，分析原因。
出现问题的时间段如下：
'''
                    ##result += getIndValmv(pg, 2189016, targetid, begintime, endtime, bm)

                    result += '''
如果问题比较严重，建议通过下面的方式进行分析:
A) 数据库管理相关的自动作业可能会产生较大的REDO，比如表分析、段自动优化等，可以通过出现问题的时间段去进一步确认。这些操作往往发生在晚上的系统运维窗口中。
B) 如果存在规律性：可能应用软件或者某些定时任务产生了较多的REDO，建议与应用开发商确认是否属于正常
C) 如果不存在规律性：可能某些手工数据维护操作或者应用软件出现特殊情况或BUG导致产生了大量的REDO，建议与开发商确认是否属于正常。必要时可以通过LOGMINER去做进一步分析。
'''

                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,8 rpt_finding_id,'health_load_metric' rpt_finding_module,
0 rpt_finding_type,'2189016' rpt_sub_id,'' iname,
'Redo Generated Per Sec存在扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)

                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_LOAD' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2189016)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.record_time between '{2}' and '{3}'
   and a.metric_id = c.index_id
   --and a.metric_value::numeric >= {4}*3
 order by a.deduct desc,a.metric_value::numeric desc 
 limit 20
'''.format(rpt_id, targetid, begintime, endtime, bm)
                    pg.execute(insql_mf)

            elif res[0].startswith("Logons Per Sec"):
                if res[2] > 0:
                    lm = getVal(2189018, pg, targetid, lmbegintime, lmendtime)
                    bm = getVal(2189018, pg, targetid, begintime, endtime)
                    if lm > bm:
                        rlb = "有所下降，数据库长连接数减少"
                    elif lm < bm:
                        rlb = "有所上升，数据库长连接数增加"
                    else:
                        rlb = "基本持平"

                    result = '''
Oracle数据库的应用一般应该使用长连接的方式连接数据库，平均每秒登录数超过1次说明应用连接数据库的方式存在隐患，建议进行排查。
上月该指标的平均值为：''' + str(lm) + '''，本月该指标的平均值为：''' + str(bm) + '''，本月与上月该指标值''' + rlb + '''。
如果该指标在某些时间段出现了超过平均水平3倍以上的情况，建议与开发商共同检查，分析原因。
出现问题的时间段如下：
'''
                    ##result += getIndValmv(pg, 2189018, targetid, begintime, endtimei,bm)
                    result += '''
如果该问题持续多次出现，建议进行如下分析：
A) 和应用开发商应用系统中是否存在短连接的应用模块，通过listener.log监听日志也可以查看到哪个服务器或者客户端存在频繁连接数据库的行为
B) 检查数据库连接池的配置是否合理，是否会出现抖动的现象
'''

                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,9 rpt_finding_id,'health_load_metric' rpt_finding_module,
0 rpt_finding_type,'2189018' rpt_sub_id,'' iname,
'Logons Per Sec存在扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)

                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_LOAD' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2189018)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.record_time between '{2}' and '{3}'
   and a.metric_id = c.index_id
   --and a.metric_value::numeric >= {4}*3
 order by a.deduct desc,a.metric_value::numeric desc 
 limit 20
'''.format(rpt_id, targetid, begintime, endtime, bm)
                    pg.execute(insql_mf)

            elif res[0].startswith("User Calls Per Sec"):
                if res[2] > 0:
                    lm = getVal(2189026, pg, targetid, lmbegintime, lmendtime)
                    bm = getVal(2189026, pg, targetid, begintime, endtime)
                    if lm > bm:
                        rlb = "有所下降"
                    elif lm < bm:
                        rlb = "有所上升"
                    else:
                        rlb = "基本持平"

                    result = '''
应用系统中可能存在某个时段SQL执行数量出现异常，上月该指标的平均值为：''' + str(lm) + '''，本月该指标的平均值为：''' + str(bm) + '''，本月较上月指标值''' + rlb + '''。
如果这两个指标中的某个指标出现过超过平均值3倍以上的时间段，则需要通过应用开发商确认该现象是否合理。
出现异常的时间段如下：
'''
                    ##result += getIndValmv(pg, 2189026, targetid, begintime, endtime, bm)
                    result += '''
如果问题比较严重，建议进行如下分析：
A) 与应用开发商确认业务量是否在所列时间段内出现超出正常水平的异常，排除应用软件BUG导致该问题
B) 相关时间段是否存在定时任务或者后台操作或者人工运维操作
C) 数据库系统是否存在系统作业或者BUG导致类该问题
'''

                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,10 rpt_finding_id,'health_load_metric' rpt_finding_module,
0 rpt_finding_type,'2189026' rpt_sub_id,'' iname,
'User Calls Per Sec存在扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)

                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_LOAD' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2189026)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.record_time between '{2}' and '{3}'
   and a.metric_id = c.index_id
   --and a.metric_value::numeric >= {4}*3
 order by a.deduct desc,a.metric_value::numeric desc 
 limit 20
'''.format(rpt_id, targetid, begintime, endtime, bm)
                    pg.execute(insql_mf)

            elif res[0].startswith("Executions Per Sec"):
                if res[2] > 0:
                    lm = getVal(2189121, pg, targetid, lmbegintime, lmendtime)
                    bm = getVal(2189121, pg, targetid, begintime, endtime)
                    if lm > bm:
                        rlb = "有所下降"
                    elif lm < bm:
                        rlb = "有所上升"
                    else:
                        rlb = "基本持平"

                    result = '''
应用系统中可能存在某个时段SQL执行数量出现异常，上月该指标的平均值为：''' + str(lm) + '''，本月该指标的平均值为：''' + str(bm) + '''，本月较上月''' + rlb + '''。
如果这两个指标中的某个指标出现过超过平均值3倍以上的时间段，则需要通过应用开发商确认该现象是否合理。
出现异常的时间段如下：
'''
                    ##result += getIndValmv(pg, 2189121, targetid, begintime, endtime, bm)
                    result += '''
如果问题比较严重，建议进行如下分析：
A) 与应用开发商确认业务量是否在所列时间段内出现超出正常水平的异常，排除应用软件BUG导致该问题
B) 相关时间段是否存在定时任务或者后台操作或者人工运维操作
C) 数据库系统是否存在系统作业或者BUG导致类该问题
'''

                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,11 rpt_finding_id,'health_load_metric' rpt_finding_module,
0 rpt_finding_type,'2189121' rpt_sub_id,'' iname,
'Executions Per Sec存在扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)

                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_LOAD' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2189121)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.record_time between '{2}' and '{3}'
   and a.metric_id = c.index_id
   --and a.metric_value::numeric >= {4}*3
 order by a.deduct desc,a.metric_value::numeric desc 
 limit 20
'''.format(rpt_id, targetid, begintime, endtime, bm)
                    pg.execute(insql_mf)

            elif res[0].startswith("Total PGA Used by SQL Workareas"):
                if res[2] > 0:
                    lm = getVal(2189159, pg, targetid, lmbegintime, lmendtime)
                    bm = getVal(2189159, pg, targetid, begintime, endtime)
                    if lm > bm:
                        rlb = "有所下降"
                    elif lm < bm:
                        rlb = "有所上升"
                    else:
                        rlb = "基本持平"

                    result = '''
应用系统中可能存在某个时段内排序所使用的物理内存总量出现异常，上月该指标的平均值为：''' + str(lm) + '''，本月该指标的平均值为：''' + str(bm) + '''，本月较上月指标值''' + rlb + '''。
如果这两个指标中的某个指标出现过超过平均值3倍以上的时间段，则需要通过应用开发商确认该现象是否合理。
出现异常的时间段如下：
'''
                    ##result += getValmv(pg, 2189159, targetid, begintime, endtime, bm)
                    result += '''
如果问题比较严重，建议进行如下分析：
A) 应用软件中可能存在一些sql的执行开销过大，导致了排序内存使用过大
'''

                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,12 rpt_finding_id,'health_load_metric' rpt_finding_module,
0 rpt_finding_type,'2189159' rpt_sub_id,'' iname,
'Total PGA Used by SQL Workareas存在扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)

                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_LOAD' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2189159)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.record_time between '{2}' and '{3}'
   and a.metric_id = c.index_id
   --and a.metric_value::numeric >= {4}*3
 order by a.deduct desc,a.metric_value::numeric desc 
 limit 20
'''.format(rpt_id, targetid, begintime, endtime, bm)
                    pg.execute(insql_mf)

            elif res[0].startswith("Logical Reads Per Sec"):
                if res[2] > 0:
                    lm = getVal(2189030, pg, targetid, lmbegintime, lmendtime)
                    bm = getVal(2189030, pg, targetid, begintime, endtime)
                    if lm > bm:
                        rlb = "有所下降"
                    elif lm < bm:
                        rlb = "有所上升"
                    else:
                        rlb = "基本持平"

                    result = '''
应用系统中可能存在某个时段SQL执行数量出现异常或者某些SQL执行开销过大导致该问题。上月该指标的平均值为：''' + str(lm) + '''，本月该指标的平均值为：''' + str(
                        bm) + '''，本月较上月指标值''' + rlb + '''。
如果这两个指标中的某个指标出现过超过平均值3倍以上的时间段，则需要通过应用开发商确认该现象是否合理。
出现异常的时间段如下：
'''
                    ##result += getIndValmv(pg, 2189030, targetid, begintime, endtime, bm)
                    result += '''
如果问题比较严重，建议进行下面的分析：
A) 检查AWR报告中的逻辑读较多的SQL，与开发商共同分析，确认是否存在问题
B) 与开发商确认业务负载是否在出现问题的时间段内存在异常
'''

                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,13 rpt_finding_id,'health_load_metric' rpt_finding_module,
0 rpt_finding_type,'2189030' rpt_sub_id,'' iname,
'Logical Reads Per Sec存在扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)

                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_LOAD' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2189030)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.record_time between '{2}' and '{3}'
   and a.metric_id = c.index_id
   --and a.metric_value::numeric >= {4}*3
 order by a.deduct desc,a.metric_value::numeric desc 
 limit 20
'''.format(rpt_id, targetid, begintime, endtime, bm)
                    pg.execute(insql_mf)
            elif res[0].startswith("Network Traffic Volume Per Sec"):
                if res[2] > 0:
                    lm = getVal(2189058, pg, targetid, lmbegintime, lmendtime)
                    bm = getVal(2189058, pg, targetid, begintime, endtime)
                    if lm > bm:
                        rlb = "有所下降"
                    elif lm < bm:
                        rlb = "有所上升"
                    else:
                        rlb = "基本持平"

                    result = '''
                    应用系统中可能存在获取大量记录的SQL或者获取了不必要的列。上月该指标的平均值为：''' + str(lm) + '''，本月该指标的平均值为：''' + str(
                            bm) + '''，本月较上月指标值''' + rlb + '''。
                    如果这两个指标中的某个指标出现过超过平均值3倍以上的时间段，则需要通过应用开发商确认该现象是否合理。
                    出现异常的时间段如下：
                    '''
                    result += '''
                    如果问题比较严重，建议进行下面的分析：
                    A) 检查问题时间段存在的获取大量记录的SQL，找到并与开发商共同分析，确认是否存在问题
                    B) 与开发商确认业务负载是否在出现问题的时间段内存在异常
                    '''
                    ismf = '''
        insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
        select '{0}' rpt_id,'{1}' target_id,13 rpt_finding_id,'health_load_metric' rpt_finding_module,
        0 rpt_finding_type,'2189058' rpt_sub_id,'' iname,
        'Network Traffic Volume Per Sec存在扣分' rpt_finding_label,
        '告警' rpt_finding_alarm_level,
        '{2}' rpt_finding_text,
        1 rpt_finding_level
        '''.format(rpt_id, targetid, result)
                    # print(ismf)
                    pg.execute(ismf)

                    insql_mf = '''
        insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                         rpt_scope_ded,rpt_ded_datetime,rpt_serious)
        select '{0}' rpt_id,b.target_id,'H_LOAD' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
                   a.deduct,a.record_time,1 rpt_serious
          from h_health_check_detail a,h_health_check b,mon_index c
         where a.metric_id in (2189058)
           and a.health_check_id = b.health_check_id
           and a.metric_value <> '周期内无有效采样记录'
           /*and b.use_flag = true*/   
           and b.target_id = '{1}'
           and a.deduct <> 0
           and a.record_time between '{2}' and '{3}'
           and a.metric_id = c.index_id
           --and a.metric_value::numeric >= {4}*3
         order by a.deduct desc,a.metric_value::numeric desc 
         limit 20
        '''.format(rpt_id, targetid, begintime, endtime, bm)
                    # print(insql_mf)
                    pg.execute(insql_mf)


        """ppsd = getSeriousDis(pg, targetid, begintime, endtime)
        if ppsd != "":
            result = "严重问题发现（存在一次性扣分超过10分或者全扣光的情况）"
            ismf='''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,14 rpt_finding_id,'health_load_score' rpt_finding_module,
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

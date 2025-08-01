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
    ltag = ['2.2.5', 'DB']
    return tags.register(ltag, file_name)


class Result(object):
    def __str__(self):
        return "\n".join("{}={}".format(k, getattr(self, k))
                         for k in self.__dict__.keys())


def getValue(ora, sql):
    result = ora.execute(sql)
    if (result.code != 0):
        print(sql)
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
select a.metric_id metric_id,a.deduct,
       a.record_time,a.metric_value,b.target_id,b.total_score
  from h_health_check_detail a,h_health_check b
 where a.metric_id in (2180509, 2184316,2184312,2184314,2184313,2184315,2184319,2184323,2184322,2184318)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   /*and b.use_flag = true*/
   and b.target_id = '%s'
   and a.record_time between '%s' and '%s'
)  
select mi.description description,
       mi.remark remark,
       count(case when res.deduct >0 then res.deduct else null end) cnt,
       coalesce(round(avg(case when res.deduct >0 then res.deduct::numeric else null end),2),0) amv,
       coalesce(max(res.deduct::numeric),0) maxv
  from res
  left join mon_index mi on res.metric_id=mi.index_id
   and mi.use_flag =true
 group by mi.description,mi.remark  
''' % (target_id, bt, et)

    cursor = getValue(conn, sql)
    results = cursor.fetchall()

    if (len(results) > 0):
        head = ["指标名称（名称）", "指标描述", "扣分次数", "扣分平均值", "扣分最大值"]
        desc = "数据库并发扣分详情"
        table = CommUtil.createTable(head, results, desc)
        title = "数据库并发扣分详情分析"
        p1 = FormatUtil.sectionRes(title, table=table)

        result = results

    return p1, result


def getSeriousDis(conn, target_id, bt, et):
    psd = ""
    sql = """
with res as (
select a.record_time,c.description,a.metric_value,a.deduct,d.total_score
  from h_health_check_detail a,h_health_check b,mon_index c,h_model_item_metric d,h_model_item e
 where a.metric_id in (2180509, 2184316,2184312,2184314,2184313,2184315,2184319,2184323,2184322,2184318)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   and b.target_id = '{0}'
   and a.record_time between '{1}' and '{2}'
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
select distinct record_time, description, metric_value, deduct
  from resa
 where rn <= 5
""".format(target_id, bt, et)

    cursor = getValue(conn, sql)
    results = cursor.fetchall()

    if (len(results) > 0):
        head = ["时间", "指标", "值", "扣分"]
        desc = "数据库并发严重扣分情况"
        table = CommUtil.createTable(head, results, desc)
        title = "数据库并发严重扣分情况分析"
        psd = FormatUtil.sectionRes(title, table=table)

    return psd


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
        result = ""
        ##ora = orautil.Oracle(host, usr, pwd, port, database)
        ##数据库并发入库
        ##删除已有数据
        sqldel1 = """delete from rpt_scope_detail where rpt_id='{0}' and target_id='{1}' and rpt_scope_category='H_CUR'
""".format(rpt_id, targetid)
        pg.execute(sqldel1)
        sqldel2 = """delete from rpt_scope_ded_history where rpt_id='{0}' and target_id='{1}' and rpt_scope_category='H_CUR'
""".format(rpt_id, targetid)
        pg.execute(sqldel2)
        sqldel3 = """delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module in ('health_cur_metric','health_cur_score')
""".format(rpt_id, targetid)
        pg.execute(sqldel3)

        insql = '''
insert into rpt_scope_detail(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_note,
                                                        rpt_scope_count,rpt_scope_ded_avg,rpt_scope_ded_max)    
with res as (
select a.metric_id,a.deduct,a.record_time,a.metric_value,b.target_id,b.total_score,a.iname
 from h_health_check_detail a,h_health_check b
where 
  a.metric_id in (2180509, 2184316,2184312,2184314,2184313,2184315,2184319,2184323,2184322,2184318)
  and a.health_check_id = b.health_check_id
  and a.metric_value <> '周期内无有效采样记录'
  /*and b.use_flag = true*/
  and b.target_id = '{0}'
  and a.deduct<>0
  and a.record_time between '{1}' and '{2}'
) 
select '{3}' rptid,res.target_id target_id,'H_CUR' rsc,mi.index_id,res.iname,
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
            if res[0].startswith("library cache lock") or res[0].startswith("latch: row cache objects") or res[
                0].startswith("row cache lock"):
                if res[2] > 0:

                    result = '''
说明共享池的性能存在问题，可能的原因如下：
A) SGA频繁出现RESIZE现象，可以通过V$SGA_RESIZE_OPS视图分析确认
B) 共享池设置偏小，通过加大共享池配置改善该问题
C) 应用软件的SQL未使用绑定变量，导致SQL共享不足
D) 某些表或者索引做了DDL操作导致SQL执行计划失效
E) 某些表或者索引更新了统计数据，导致SQL执行计划失效
'''

                    if res[0].startswith("library cache lock"):
                        res_id = "2184316"
                        rfid = 1
                    elif res[0].startswith("latch: row cache objects"):
                        res_id = "2184319"
                        rfid = 2
                    elif res[0].startswith("row cache lock"):
                        res_id = "2184318"
                        rfid = 3

                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,{2} rpt_finding_id,'health_cur_metric' rpt_finding_module,
0 rpt_finding_type,'{3}' rpt_sub_id,'' iname,
'{4}出现扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{5}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, rfid, res_id, res[0], result)
                    pg.execute(ismf)

                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_CUR' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in ({4})
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.record_time between '{2}' and '{3}'
   and a.metric_id = c.index_id
 order by a.deduct desc,a.metric_value::numeric desc 
 limit 20
'''.format(rpt_id, targetid, begintime, endtime, res_id)
                    pg.execute(insql_mf)

            elif (res[0].startswith("cursor: pin S") and "wait on X" not in res[0]) or res[0].startswith(
                    "cursor: pin S wait on X") or res[0].startswith("library cache: mutex X"):
                if res[2] > 0:
                    result = '''
这是CURSOR执行过程中争用导致，可能原因如下：
A) 针对某些表或者某条SQL执行频率过高,导致CURSOR争用
B) SQL未使用绑定变量
C) 共享池存在性能问题
D) SGA频繁出现RESIZE现象
E) 某些ORACLE BUG导致
当问题发生时，通过下列SQL可以找出存在该等待事件的SQL：
SELECT s.sid, t.sql_text
  FROM v$session s, v$sql t
 WHERE s.event LIKE ''%cursor: pin S wait on X%''
   AND t.sql_id = s.sql_id
'''

                    if res[0].startswith("cursor: pin S") and "wait on X" not in res[0]:
                        res_id = "2184314"
                        rfid = 4
                    elif res[0].startswith("cursor: pin S wait on X"):
                        res_id = "2184315"
                        rfid = 5
                    elif res[0].startswith("library cache: mutex X"):
                        res_id = "2184323"
                        rfid = 6

                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,{2} rpt_finding_id,'health_cur_metric' rpt_finding_module,
0 rpt_finding_type,'{3}' rpt_sub_id,'' iname,
'{4}出现扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{5}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, rfid, res_id, res[0], result)
                    pg.execute(ismf)

                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_CUR' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in ({4})
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.record_time between '{2}' and '{3}'
   and a.metric_id = c.index_id
 order by a.deduct desc,a.metric_value::numeric desc 
 limit 20
'''.format(rpt_id, targetid, begintime, endtime, res_id)
                    pg.execute(insql_mf)

            elif res[0].startswith("latch: cache buffers chains"):
                if res[2] > 0:
                    result = '''
DB CACHE的CBC链出现过争用较为严重争用的现象，该现象一般是由于过多的DB CACHE逻辑读/物理读操作导致。可能存在的原因如下：
A) 应用系统的SQL不够优化，产生了过多的全表扫描或者全索引扫描操作，导致过多的逻辑读
B) DB CACHE配置过小
C) 存在大量的热块争用
D) 数据库存在BUG
'''
                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,7 rpt_finding_id,'health_cur_metric' rpt_finding_module,
0 rpt_finding_type,'2184312' rpt_sub_id,'' iname,
'latch: cache buffers chains出现扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)

                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_CUR' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2184312)
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

            elif res[0].startswith("buffer busy waits"):
                if res[2] > 0:
                    result = '''
数据库出现过大量热块冲突，热块冲突产生的原因如下：
A) SQL存在性能问题，产生了不必要的全表扫描
B) 部分数据的并发访问量过大
C) DB CACHE设置不合理
'''
                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,8 rpt_finding_id,'health_cur_metric' rpt_finding_module,
0 rpt_finding_type,'2184313' rpt_sub_id,'' iname,
'buffer busy waits出现扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)

                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_CUR' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2184313)
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

            elif res[0].startswith("latch free"):
                if res[2] > 0:
                    result = '''
数据库出现过闩锁争用过于严重的问题，需要进一步分析LATCH FREE产生的具体原因，分析哪些闩锁存在问题。
'''
                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,9 rpt_finding_id,'health_cur_metric' rpt_finding_module,
0 rpt_finding_type,'2184322' rpt_sub_id,'' iname,
'latch free出现扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)

                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_CUR' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2184322)
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

            elif res[0].startswith("enq CF - contention event wait time"):
                if res[2] > 0:
                    result = '''
控制文件访问锁存在超时现象，一般产生该问题的原因如下：
A) 控制文件所在的文件系统存在性能问题
B) 过多的日志切换、备份等访问控制文件的操作并行执行导致问题
C) 数据库存在BUG导致控制文件死锁现象
'''
                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,10 rpt_finding_id,'health_cur_metric' rpt_finding_module,
0 rpt_finding_type,'2180509' rpt_sub_id,'' iname,
'enq CF - contention event wait time出现扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)

                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_CUR' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2180509)
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

        """ppsd = getSeriousDis(pg, targetid, begintime, endtime)
        if ppsd != "":
            result = "严重问题发现（存在一次性扣分超过10分或者全扣光的情况）"
            ismf='''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,11 rpt_finding_id,'health_cur_score' rpt_finding_module,
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

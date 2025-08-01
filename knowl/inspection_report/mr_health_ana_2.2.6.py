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
    ltag = ['2.2.6', 'DB']
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
select a.metric_id metric_id,a.deduct,
       a.record_time,a.metric_value,b.target_id,b.total_score
  from h_health_check_detail a,h_health_check b
 where a.metric_id in (2189118,2189119,2189999,2189123,2180514,2180501,2189106,2189108,2180513, 2184301)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   and a.metric_value <> '最近1小时无有效采样记录'
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
        desc = "数据库总体状况扣分详情"
        table = CommUtil.createTable(head, results, desc)
        title = "数据库总体状况扣分详情分析"
        p1 = FormatUtil.sectionRes(title, table=table)

        result = results

    return p1, result


def getSeriousDis(conn, target_id, bt, et):
    psd = ""
    sql = '''
with res as (
select a.record_time,c.description,a.metric_value,a.deduct,d.total_score
  from h_health_check_detail a,h_health_check b,mon_index c,h_model_item_metric d,h_model_item e
 where a.metric_id in (2189118,2189119,2189999,2189123,2180514,2180501,2189106,2189108,2180513, 2184301)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   and a.metric_value <> '最近1小时无有效采样记录'
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
        desc = "数据库总体状况严重扣分情况"
        table = CommUtil.createTable(head, results, desc)
        title = "数据库总体状况严重扣分情况分析"
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
        ##删除已有数据
        sqldel1 = """delete from rpt_scope_detail where rpt_id='{0}' and target_id='{1}' and rpt_scope_category='H_SUM_RI'
""".format(rpt_id, targetid)
        pg.execute(sqldel1)
        sqldel2 = """delete from rpt_scope_ded_history where rpt_id='{0}' and target_id='{1}' and rpt_scope_category='H_SUM_RI'
""".format(rpt_id, targetid)
        pg.execute(sqldel2)
        sqldel3 = """delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module in ('health_sum_metric_ri','health_sum_score_ri')
""".format(rpt_id, targetid)
        pg.execute(sqldel3)

        ##数据库IO入库
        insql = '''
insert into rpt_scope_detail(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_note,
                                                        rpt_scope_count,rpt_scope_ded_avg,rpt_scope_ded_max)    
with res as (
select a.metric_id,a.deduct,a.record_time,a.metric_value,b.target_id,b.total_score,a.iname
 from h_health_check_detail a,h_health_check b
where 
  a.metric_id in (2189118,2189119,2189999,2189123,2180514,2180501,2189106,2189108,2180513,2184301)
  and a.health_check_id = b.health_check_id
  and a.metric_value <> '周期内无有效采样记录'
   and a.metric_value <> '最近1小时无有效采样记录'
  /*and b.use_flag = true*/
  and b.target_id = '{0}'
  and a.deduct<>0
  and a.record_time between '{1}' and '{2}'
) 
select '{3}' rptid,res.target_id target_id,'H_SUM_RI' rsc,mi.index_id,res.iname,
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
            # print(res)
            if res[0].startswith("Process Limit"):
                if res[2] > 0:
                    result = '''
数据库的processes参数设置过低，无法满足目前的负载需要。建议加大该参数。
'''
                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'health_sum_metric_ri' rpt_finding_module,
0 rpt_finding_type,'2189118' rpt_sub_id,'' iname,
'Process Limit出现扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)

                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_SUM_RI' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2189118)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   and a.metric_value <> '最近1小时无有效采样记录'
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.record_time between '{2}' and '{3}'
   and a.metric_id = c.index_id
 order by a.deduct desc,a.metric_value::numeric asc
 limit 20
'''.format(rpt_id, targetid, begintime, endtime)
                    pg.execute(insql_mf)

            elif res[0].startswith("Session Limit"):
                if res[2] > 0:
                    result += '''
数据库的session参数设置过低，无法满足目前的负载需要。建议加大该参数。
'''
                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,2 rpt_finding_id,'health_sum_metric_ri' rpt_finding_module,
0 rpt_finding_type,'2189119' rpt_sub_id,'' iname,
'Session Limit出现扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)

                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_SUM_RI' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2189119)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   and a.metric_value <> '最近1小时无有效采样记录'
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.record_time between '{2}' and '{3}'
   and a.metric_id = c.index_id
 order by a.deduct desc,a.metric_value::numeric asc
 limit 20
'''.format(rpt_id, targetid, begintime, endtime)
                    pg.execute(insql_mf)

            elif res[0].startswith("active redo log count"):
                if res[2] > 0:
                    result += '''
数据库CHECKPOINT的速度过慢导致了活跃REDO LOG组的数量过大，严重时会引起数据库性能下降，甚至HANG住。
可能产生的原因如下：
A) 数据库的写IO性能不足，导致脏块刷新过慢
B) 应用系统出现了异常，导致大量的REDO被产生
C) 数据库中存在DROP TABLE/TRUNCATE TABLE等操作
D) REDO LOG文件设置过小
E) CHECKPOINT相关参数设置不合理
F) 操作系统性能不佳
'''
                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,3 rpt_finding_id,'health_sum_metric_ri' rpt_finding_module,
0 rpt_finding_type,'2180514' rpt_sub_id,'' iname,
'active redo log count出现扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)

                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_SUM_RI' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2180514)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   and a.metric_value <> '最近1小时无有效采样记录'
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.record_time between '{2}' and '{3}'
   and a.metric_id = c.index_id
 order by a.deduct desc,a.metric_value::numeric asc
 limit 20
'''.format(rpt_id, targetid, begintime, endtime)
                    pg.execute(insql_mf)

            elif res[0].startswith("scn rate"):
                if res[2] > 0:
                    result += '''
SCN增值速度超过正常水平，如果长期出现类似现象，可能会导致SCN HEADROOM持续下降。建议进行SCN专项检查。
'''
                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,4 rpt_finding_id,'health_sum_metric_ri' rpt_finding_module,
0 rpt_finding_type,'2180510' rpt_sub_id,'' iname,
'scn rate出现扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)

                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_SUM_RI' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2180510)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   and a.metric_value <> '最近1小时无有效采样记录'
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.record_time between '{2}' and '{3}'
   and a.metric_id = c.index_id
 order by a.deduct desc,a.metric_value::numeric asc
 limit 20
'''.format(rpt_id, targetid, begintime, endtime)
                    pg.execute(insql_mf)

            elif res[0].startswith("noarchive redo log file count"):
                if res[2] > 0:
                    result += '''
数据库归档存在性能问题或者无法正常归档导致该问题出现。
一般产生的原因如下：
A) 产生的REDO量过大，导致日志切换过于频繁
B) 归档日志所在文件系统存在性能问题，导致归档过慢
C) 归档目录满或者无法正常写入导致归档失败
D) 归档进程故障导致归档停止
E) 数据库BUG导致
'''
                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,5 rpt_finding_id,'health_sum_metric_ri' rpt_finding_module,
0 rpt_finding_type,'2180513' rpt_sub_id,'' iname,
'noarchive redo log file count出现扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)

                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_SUM_RI' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2180513)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   and a.metric_value <> '最近1小时无有效采样记录'
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.record_time between '{2}' and '{3}'
   and a.metric_id = c.index_id
 order by a.deduct desc,a.metric_value::numeric asc
 limit 20
'''.format(rpt_id, targetid, begintime, endtime)
                    pg.execute(insql_mf)
            elif res[0].startswith("Database CPU Time Ratio"):
                if res[2] > 0:
                    result += '''
数据库可能存在逻辑读过高的SQL或者排序量较大的SQL消耗大量的CPU.建议做SQL专项检查。
'''
                    ismf = '''
                    insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                                    rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
                    select '{0}' rpt_id,'{1}' target_id,5 rpt_finding_id,'health_sum_metric_ri' rpt_finding_module,
                    0 rpt_finding_type,'2189108' rpt_sub_id,'' iname,
                    'Database CPU Time Ratio出现扣分' rpt_finding_label,
                    '告警' rpt_finding_alarm_level,
                    '{2}' rpt_finding_text,
                    1 rpt_finding_level
                    '''.format(rpt_id, targetid, result)
                    # print(ismf)
                    pg.execute(ismf)

                    insql_mf = '''
                    insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                                     rpt_scope_ded,rpt_ded_datetime,rpt_serious)
                    select '{0}' rpt_id,b.target_id,'H_SUM_RI' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
                               a.deduct,a.record_time,1 rpt_serious
                      from h_health_check_detail a,h_health_check b,mon_index c
                     where a.metric_id in (2189108)
                       and a.health_check_id = b.health_check_id
                       and a.metric_value <> '周期内无有效采样记录'
                        and a.metric_value <> '最近1小时无有效采样记录'
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


        """ppsd = getSeriousDis(pg, targetid, begintime, endtime)
        if ppsd != "":
            result = "严重问题发现（存在一次性扣分超过10分或者全扣光的情况）"
            ismf='''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,6 rpt_finding_id,'health_sum_score_ri' rpt_finding_module,
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

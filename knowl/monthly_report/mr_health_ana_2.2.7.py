#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

sys.path.append('/usr/software/knowl')
import CommUtil
import DBUtil
import psycopg2
import PGUtil
import FormatUtil
import DBUtil
import tags


def register(file_name):
    ltag = ['2.2.7', 'DB']
    return tags.register(ltag, file_name)


def getOSVal(conn, target_id, bt, et):
    p1 = ""
    sql = '''
with res as (
select a.metric_id||coalesce(a.iname,'') metric_id,a.deduct,
       a.record_time,a.metric_value,a.iname,b.target_id,b.total_score
  from h_health_check_detail a,h_health_check b
 where a.metric_id in (2180205,2189098,2189099,2180209,2180210,2180211,2189101,2189102)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   /*and b.use_flag = true*/
   and b.target_id = '%s'
   and a.record_time between '%s' and '%s'
)  
select coalesce(mi.description,res.iname) description,
       coalesce(mi.remark,res.iname) remark,
       count(case when res.deduct >0 then res.deduct else null end) cnt,
       coalesce(round(avg(case when res.deduct >0 then res.deduct::numeric else null end),2),0) amv,
       coalesce(max(res.deduct::numeric),0) maxv
  from res
  left join mon_index mi on res.metric_id=mi.index_id::varchar
   and mi.use_flag =true
 group by coalesce(mi.description,res.iname), coalesce(mi.remark,res.iname)  
''' % (target_id, bt, et)
    cursor = DBUtil.getValue(conn, sql)
    results = cursor.fetchall()
    if results:
        head = ["指标名称（名称）", "指标描述", "扣分次数", "扣分平均值", "扣分最大值"]
        desc = "数据库RAC健康扣分详情"
        table = CommUtil.createTable(head, results, desc)
        title = "数据库RAC健康扣分详情分析"
        p1 = FormatUtil.sectionRes(title, table=table)
    return p1, results


def getdfVal(conn, index_id, target_id, bt, et):
    pdf = ""
    sql = f'''
select a.record_time,c.description,a.metric_value,a.deduct
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in ({index_id})
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   and b.use_flag = true
   and b.target_id = '{target_id}'
   and a.record_time between '{bt}' and '{et}'
   and a.metric_id = c.index_id
 order by a.deduct desc,a.record_time desc 
 limit 5
'''
    sql_des = f'''
select description
  from mon_index 
 where use_flag = true 
   and index_id = '{index_id}'
 limit 1
'''
    cursor_des = DBUtil.getValue(conn, sql_des)
    results_des = cursor_des.fetchone()
    if results_des:
        desname = results_des[0]
    else:
        desname = str(index_id)

    cursor = DBUtil.getValue(conn, sql)
    results = cursor.fetchall()

    if results:
        head = ["时间", "指标", "值", "扣分"]
        desc = desname + "扣分情况"
        table = CommUtil.createTable(head, results, desc)
        title = desname + "扣分情况"
        pdf = FormatUtil.sectionRes(title, table=table)
    return pdf


def getSeriousDis(conn, target_id, bt, et):
    psd = ""
    sql = '''
with res as (
select a.record_time,c.description,a.metric_value,a.deduct,d.total_score
  from h_health_check_detail a,h_health_check b,mon_index c,h_model_item_metric d,h_model_item e
 where a.metric_id in (2180205,2189098,2189099,2180209,2180210,2180211,2189101,2189102)
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

    cursor = DBUtil.getValue(conn, sql)
    results = cursor.fetchall()

    if (len(results) > 0):
        head = ["时间", "指标", "值", "扣分"]
        desc = "数据库RAC健康严重扣分情况"
        table = CommUtil.createTable(head, results, desc)
        title = "数据库RAC健康严重扣分情况分析"
        psd = FormatUtil.sectionRes(title, table=table)

    return psd


def getVal(index_id, conn, target_id, bt, et):
    pval1 = 0
    sql = '''
    select coalesce(round(avg(a.metric_value::numeric),2),0)
  from h_health_check_detail a,h_health_check b 
 where a.metric_id in (%s)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   and b.use_flag = true
   and b.target_id = '%s'
   and a.metric_value != '周期内无有效采样记录'
   and a.record_time between '%s' and '%s'
''' % (index_id, target_id, bt, et)

    cursor = DBUtil.getValue(conn, sql)
    results = cursor.fetchone()
    pval1 = results[0]
    return pval1


def getlastdt(conn, bt, et):
    pldt = []
    sql = '''
    select to_date('%s','yyyy-mm-dd hh24:mi:ss') - interval '1 months' as bt,
    to_date('%s','yyyy-mm-dd hh24:mi:ss') - interval '1 months' as et
''' % (bt, et)

    cursor = DBUtil.getValue(conn, sql)
    results = cursor.fetchone()

    pldt = results

    return pldt


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
        result = ""
        ##删除已有数据
        sqldel1 = """delete from rpt_scope_detail where rpt_id='{0}' and target_id='{1}' and rpt_scope_category='H_RAC'
""".format(rpt_id, targetid)
        pg.execute(sqldel1)
        sqldel2 = """delete from rpt_scope_ded_history where rpt_id='{0}' and target_id='{1}' and rpt_scope_category='H_RAC'
""".format(rpt_id, targetid)
        pg.execute(sqldel2)
        sqldel3 = """delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module in ('health_rac_metric','health_rac_score')
""".format(rpt_id, targetid)
        pg.execute(sqldel3)
        ##ora = orautil.Oracle(host, usr, pwd, port, database)
        ##数据库RAC入库
        insql = '''
insert into rpt_scope_detail(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_note,
                                                        rpt_scope_count,rpt_scope_ded_avg,rpt_scope_ded_max)    
with res as (
select a.metric_id,a.deduct,a.record_time,a.metric_value,b.target_id,b.total_score,a.iname
 from h_health_check_detail a,h_health_check b
where 
  a.metric_id in (2180205,2189098,2189099,2180209,2180210,2180211,2189101,2189102)
  and a.health_check_id = b.health_check_id
  and a.metric_value <> '周期内无有效采样记录'
  /*and b.use_flag = true*/
  and b.target_id = '{0}'
  and a.deduct<>0
  and a.record_time between '{1}' and '{2}'
) 
select '{3}' rptid,res.target_id target_id,'H_RAC' rsc,mi.index_id,res.iname,
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
            if res[0].startswith("Avg global enqueue get time"):
                if res[2] > 0:
                    lm = getVal(2180205, pg, targetid, lmbegintime, lmendtime)
                    bm = getVal(2180205, pg, targetid, begintime, endtime)
                    if lm > bm:
                        rlb = "延时有所降低"
                    elif lm < bm:
                        rlb = "延时有所增加"
                    else:
                        rlb = "延时基本持平"

                    result = '''
出现过集群全局锁的获取时间延时超过正常水平的现象。
上月该指标的平均值为：''' + str(lm) + '''，本月该指标的平均值为''' + str(bm) + '''，本月与上月该指标''' + str(rlb) + '''。
如果该指标在某些时间段出现了超过正常水平3倍以上或者延时值超过20毫秒的情况，建议与开发商共同检查，分析原因。
当集群网络出现性能问题、应用索冲突争用严重、集群通讯流量过大、RAC集群出现其他性能问题的情况下，可能会出现该指标延时增加。
出现问题的时间段如下：
'''
                    ##result += getdfVal(pg, 2180205, targetid, begintime, endtime)
                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'health_rac_metric' rpt_finding_module,
0 rpt_finding_type,'2180205' rpt_sub_id,'' iname,
'Avg global enqueue get time存在扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)

                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_RAC' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2180205)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.record_time between '{2}' and '{3}'
   and a.metric_value != '周期内无有效采样记录'
   and a.metric_id = c.index_id
 order by a.deduct desc,a.metric_value::numeric desc 
 limit 20
'''.format(rpt_id, targetid, begintime, endtime)
                    pg.execute(insql_mf)

            elif res[0].startswith("Global Cache Average CR Get Time"):
                if res[2] > 0:
                    result = '''
全局缓冲CR块获取时间，一般来说这个指标的延时应该小于5毫秒，超过5毫秒都属于不正常，该指标超过20毫秒将对系统性能产生较大影响。
出现扣分时间段如下：
'''
                    ##result += getdfVal(pg, 2189098, targetid, begintime, endtime)
                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                      
                          rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,2 rpt_finding_id,'health_rac_metric' rpt_finding_module,
0 rpt_finding_type,'2189098' rpt_sub_id,'' iname,
'Global Cache Average CR Get Time存在扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)

                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_RAC' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2189098)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.record_time between '{2}' and '{3}'
      and a.metric_value != '周期内无有效采样记录'
   and a.metric_id = c.index_id
 order by a.deduct desc,a.metric_value::numeric desc 
 limit 20
'''.format(rpt_id, targetid, begintime, endtime)
                    pg.execute(insql_mf)

            elif res[0].startswith("Global Cache Average Current Get Time"):
                if res[2] > 0:
                    result = '''
全局缓冲当前块获取时间，一般来说这个指标的延时应该小于5毫秒，超过5毫秒都属于不正常，该指标超过20毫秒将对系统性能产生较大影响。
出现扣分时间段如下：
'''
                    ##result += getdfVal(pg, 2189099, targetid, begintime, endtime)
                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,3 rpt_finding_id,'health_rac_metric' rpt_finding_module,
0 rpt_finding_type,'2189099' rpt_sub_id,'' iname,
'Global Cache Average Current Get Time存在扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)

                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_RAC' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2189099)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.record_time between '{2}' and '{3}'
      and a.metric_value != '周期内无有效采样记录'
   and a.metric_id = c.index_id
 order by a.deduct desc,a.metric_value::numeric desc
 limit 20
'''.format(rpt_id, targetid, begintime, endtime)
                    pg.execute(insql_mf)

            elif res[0].startswith("Avg message sent queue time"):
                if res[2] > 0:
                    result = '''
集群消息在队列中的等待事件，一般来说这个指标的延时应该小于1毫秒，超过1毫秒都属于不正常，该指标超过10毫秒将对系统性能产生较大影响。
出现扣分时间段如下：
'''
                    ##result += getdfVal(pg, 2180209, targetid, begintime, endtime)
                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,4 rpt_finding_id,'health_rac_metric' rpt_finding_module,
0 rpt_finding_type,'2180209' rpt_sub_id,'' iname,
'Avg message sent queue time存在扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)

                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_RAC' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2180209)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.record_time between '{2}' and '{3}'
      and a.metric_value != '周期内无有效采样记录'
   and a.metric_id = c.index_id
 order by a.deduct desc,a.metric_value::numeric
 limit 20
'''.format(rpt_id, targetid, begintime, endtime)
                    pg.execute(insql_mf)

            elif res[0].startswith("Avg GCS message process time"):
                if res[2] > 0:
                    result = '''
集群消息处理消耗的时间，一般来说这个指标的延时应该小于5毫秒，超过5毫秒都属于不正常，该指标超过20毫秒将对系统性能产生较大影响。
出现扣分时间段如下：
'''
                    ##result += getdfVal(pg, 2180210, targetid, begintime, endtime)
                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,5 rpt_finding_id,'health_rac_metric' rpt_finding_module,
0 rpt_finding_type,'2180210' rpt_sub_id,'' iname,
'Avg GCS message process time存在扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)

                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_RAC' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2180210)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.record_time between '{2}' and '{3}'
      and a.metric_value != '周期内无有效采样记录'
   and a.metric_id = c.index_id
 order by a.deduct desc,a.metric_value::numeric desc
 limit 20
'''.format(rpt_id, targetid, begintime, endtime)
                    pg.execute(insql_mf)

            elif res[0].startswith("Global Cache Blocks Corrupted"):
                if res[2] > 0:
                    result = '''
全局块损坏，一般来说这个指标应该为0，任何大于0的值都是不正常的。
出现扣分时间段如下：
'''
                    ##result += getdfVal(pg, 2189101, targetid, begintime, endtime)
                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,6 rpt_finding_id,'health_rac_metric' rpt_finding_module,
0 rpt_finding_type,'2189101' rpt_sub_id,'' iname,
'Global Cache Blocks Corrupted存在扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)

                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_RAC' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2189101)
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

            elif res[0].startswith("Global Cache Blocks Lost"):
                if res[2] > 0:
                    result = '''
全局块损丢失，一般来说这个指标应该为0，任何大于0的值都是不正常的。该指标超过5个时候，健康评分系统会进行扣分。
全局块丢失是数据库集群通讯异常导致，造成通讯异常的原因可能是网络故障或者ORACLE BUG。
出现扣分时间段如下：
'''
                    ##result += getdfVal(pg, 2189102, targetid, begintime, endtime)
                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,7 rpt_finding_id,'health_rac_metric' rpt_finding_module,
0 rpt_finding_type,'2189102' rpt_sub_id,'' iname,
'Global Cache Blocks Lost存在扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)

                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_RAC' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2189102)
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

        ##add for update 
        dosql = """
update rpt_scope_ded_history t
set rpt_serious=0 
from (select d.target_id,c.metric_id,c.total_score
from 
h_health_model a,
h_model_item b,
h_model_item_metric c,
h_health_check d
where a.use_flag=true
and a.model_id=b.model_id
and b.use_flag=true
and b.model_item_id=c.model_item_id 
and c.use_flag=true
and a.model_id=d.model_id
and d.use_flag=true
and d.target_id ='{1}' ) tmp
where t.rpt_id='{0}'
and t.target_id ='{1}'
and t.target_id=tmp.target_id and t.rpt_metric_id=tmp.metric_id
and tmp.total_score-t.rpt_scope_ded>0
""".format(rpt_id, targetid)
        pg.execute(dosql)

    except psycopg2.DatabaseError as e:
        if pg:
            pg.close()

    # except Exception as e:
    #    errorInfo = str(e)
    #    print("异常：" + errorInfo)

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
    ltag = ['2.2.1', 'OS']
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
select a.metric_id,a.deduct,a.record_time,a.metric_value,b.target_id,b.total_score
 from h_health_check_detail a,h_health_check b
where a.metric_id in (3000007,3000005,3000200,3000003,3000008,3000006)
  and a.health_check_id = b.health_check_id
  and a.metric_value <> '周期内无有效采样记录'
  /*and b.use_flag = true*/
  and b.target_id = '%s'
  and a.record_time between '%s' and '%s'
) 
select mi.description,
       mi.remark,
       count(case when res.deduct >0 then res.deduct else null end) cnt,
       coalesce(round(avg(case when res.deduct >0 then res.deduct::numeric else null end),2),0) amv,
       coalesce(max(res.deduct::numeric),0) maxv
  from res,mon_index mi
 where res.metric_id=mi.index_id
   and mi.use_flag =true 
 group by mi.description,mi.remark
''' % (target_id, bt, et)
    # print(sql)
    cursor = getValue(conn, sql)
    results = cursor.fetchall()

    if (len(results) > 0):
        head = ["指标名称（名称）", "指标描述", "扣分次数", "扣分平均值", "扣分最大值"]
        desc = "操作系统扣分详情"
        table = CommUtil.createTable(head, results, desc)
        title = "操作系统扣分详情分析"
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
 where a.metric_id in (3000007,3000005,3000200,3000003,3000008,3000006)
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

    # conn_pg = psycopg2.connect(database=dbname,user=username,password=CommUtil.decrypt(password),host=dbip,port=pgport)
    try:
        result = ""
        # cur_pg = conn_pg.cursor()

        ##删除已有数据
        sqldel1 = """delete from rpt_scope_detail where rpt_id='{0}' and target_id='{1}' and rpt_scope_category='H_OS'
""".format(rpt_id, targetid)
        # cur_pg.execute(sqldel1)
        pg.execute(sqldel1)
        sqldel2 = """delete from rpt_scope_ded_history where rpt_id='{0}' and target_id='{1}' and rpt_scope_category='H_OS'
""".format(rpt_id, targetid)
        # cur_pg.execute(sqldel2)
        pg.execute(sqldel2)
        sqldel3 = """delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module in ('health_os_metric','health_os_score')
""".format(rpt_id, targetid)
        pg.execute(sqldel3)
        # cur_pg.execute(sqldel3)
        ##操作系统扣分详情入库
        insql = '''
insert into rpt_scope_detail(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_note,
			rpt_scope_count,rpt_scope_ded_avg,rpt_scope_ded_max)	
with res as (
select a.metric_id,a.deduct,a.record_time,a.metric_value,b.target_id,b.total_score,a.iname
 from h_health_check_detail a,h_health_check b
where a.metric_id in (3000007,3000005,3000200,3000003,3000008,3000006)
  and a.health_check_id = b.health_check_id
  /*and b.use_flag = true*/
  and b.target_id = '{0}'
  and a.deduct<>0
  and a.metric_value <> '周期内无有效采样记录'
  and a.record_time between '{1}' and '{2}'
) 
select '{3}' rptid,res.target_id target_id,'H_OS' rsc,mi.index_id,res.iname,
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
        # cur_pg.execute(insql)
        pg.execute(insql)
        # conn_pg.commit()
        # cur_pg.close()
        # conn_pg.close()

        res_p1, res_list = getOSVal(pg, targetid, begintime, endtime)

        for res in res_list:
            if res[0].startswith("Mem Free"):
                if res[2] > 0:
                    result = '''系统物理内存存在不足的现象。建议检查
1、虚拟内存相关设置是否合理，是否存在文件缓冲占用过多物理内存
2、建议检查是否存在某些进程占用过多的内存空间
3、检查是否存在内存泄露的情况
'''
                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
			rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'health_os_metric' rpt_finding_module,
0 rpt_finding_type,'3000007' rpt_sub_id,'' iname,
'Mem Free出现过扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    # print(ismf)
                    pg.execute(ismf)

                    # result += getIndVal(pg, 3000007, targetid, begintime, endtime)
                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
				 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_OS' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
	   a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (3000007)
   and a.health_check_id = b.health_check_id
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.metric_value <> '周期内无有效采样记录'
   and a.record_time between '{2}' and '{3}'
   and a.metric_id = c.index_id
 order by a.deduct desc,a.metric_value::numeric asc
limit 20
'''.format(rpt_id, targetid, begintime, endtime)
                    # print(insql_mf)
                    pg.execute(insql_mf)

            elif res[0].startswith("root fss usage"):
                if res[2] > 0:
                    result = '''系统出现过文件系统满的情况，建议通过df检查哪个文件系统满了，并及时清理文件系统。
1、如果Oracle安装目录满，建议清理Oracle相关日志（数据库trace，监听日志等）
2、如果归档目录满，建议检查归档日志备份与删除策略，如果当前文件系统无法满足归档备份删除策略所需的空间，建议扩容相关文件系统
'''
                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,2 rpt_finding_id,'health_os_metric' rpt_finding_module,
0 rpt_finding_type,'3000005' rpt_sub_id,'' iname,
'root fss usage出现过扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)
                    ##result += getIndVal(pg, 3000005, targetid, begintime, endtime)
                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                  rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_OS' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (3000005)
   and a.health_check_id = b.health_check_id
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.metric_value <> '周期内无有效采样记录'
   and a.record_time between '{2}' and '{3}'
   and a.metric_id = c.index_id
 order by a.deduct desc,a.metric_value::numeric desc 
limit 20
'''.format(rpt_id, targetid, begintime, endtime)
                    # print(insql_mf)
                    pg.execute(insql_mf)
            elif res[0].startswith("RX ERR DRP"):
                if res[2] > 0:
                    result = '''建议检查网络情况，包括网卡、网线、交换机等情况。通过netstat -in确认是否网卡存在丢包现象，并找出丢包的网卡，并进行解决。'''
                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,3 rpt_finding_id,'health_os_metric' rpt_finding_module,
0 rpt_finding_type,'3000200' rpt_sub_id,'' iname,
'RX ERR DRP出现过扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)
                    ##result += getIndVal(pg, 3000200, targetid, begintime, endtime)
                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                  rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_OS' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (3000200)
   and a.health_check_id = b.health_check_id
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.metric_value <> '周期内无有效采样记录'
   and a.record_time between '{2}' and '{3}'
   and a.metric_id = c.index_id
 order by a.deduct desc,a.metric_value::numeric desc 
limit 20
'''.format(rpt_id, targetid, begintime, endtime)
                    pg.execute(insql_mf)
            elif res[0].startswith("CPU used"):
                if res[2] > 0:
                    result = '''建议检查系统负载情况，确保CPU能力能够满足系统要求。并检查应用系统是否存在大开销应用。'''
                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,4 rpt_finding_id,'health_os_metric' rpt_finding_module,
0 rpt_finding_type,'3000003' rpt_sub_id,'' iname,
'CPU used出现过扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)
                    ##result += getIndVal(pg, 3000003, targetid, begintime, endtime)
                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                  rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_OS' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (3000003)
   and a.health_check_id = b.health_check_id
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.metric_value <> '周期内无有效采样记录'
   and a.record_time between '{2}' and '{3}'
   and a.metric_id = c.index_id
 order by a.deduct desc,a.metric_value::numeric desc 
limit 20
'''.format(rpt_id, targetid, begintime, endtime)
                    pg.execute(insql_mf)

            elif res[0].startswith("Ioawait"):
                if res[2] > 0:
                    result = '''系统的IO能力出现了不足的现象，建议分析系统总体IO能力是否满足高峰期需求。同时检查应用系统中是否存在高IO开销的SQL，并进行针对性优化。'''
                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,5 rpt_finding_id,'health_os_metric' rpt_finding_module,
0 rpt_finding_type,'3000008' rpt_sub_id,'' iname,
'Ioawait出现过扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)

                    ##result += getIndVal(pg, 3000008, targetid, begintime, endtime)
                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                  rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_OS' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (3000008)
   and a.health_check_id = b.health_check_id
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.metric_value <> '周期内无有效采样记录'
   and a.record_time between '{2}' and '{3}'
   and a.metric_id = c.index_id
 order by a.deduct desc,a.metric_value::numeric desc 
limit 20
'''.format(rpt_id, targetid, begintime, endtime)
                    pg.execute(insql_mf)
            elif res[0].startswith("IO Latency"):
                if res[2] > 0:
                    result = '''系统的IO延时存在问题，需要检查是由于后端存储IO延时过高还是操作系统层面的等待队列过大导致的IO延时问题。'''
                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,6 rpt_finding_id,'health_os_metric' rpt_finding_module,
0 rpt_finding_type,'3000006' rpt_sub_id,'' iname,
'IO Latency出现过扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    # print(ismf)
                    pg.execute(ismf)
                    ##result += getIndVal(pg, 3000006, targetid, begintime, endtime)
                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                  rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_OS' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (3000006)
   and a.health_check_id = b.health_check_id
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.metric_value <> '周期内无有效采样记录'
   and a.record_time between '{2}' and '{3}'
   and a.metric_id = c.index_id
 order by a.deduct desc,a.metric_value::numeric desc 
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
select '{0}' rpt_id,'{1}' target_id,7 rpt_finding_id,'health_os_score' rpt_finding_module,
0 rpt_finding_type,'' rpt_sub_id,'' iname,
'严重问题发现（存在一次性扣分超过10分或者全扣光的情况）' rpt_finding_label,
'致命' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id,targetid,result)
            pg.execute(ismf)"""

    except psycopg2.DatabaseError as e:
        print(e)
        if not pg is None:
            pg.close()

    # except Exception as e:
    #    errorInfo = str(e)
    #    print("异常：" + errorInfo)

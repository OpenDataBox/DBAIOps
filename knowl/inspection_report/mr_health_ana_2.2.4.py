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
    ltag = ['2.2.4', 'DB']
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
 where a.metric_id in (2189144,2189010,2189008, 2184304,2184305,2184302,2184303,2184306)
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
        desc = "数据库IO扣分详情"
        table = CommUtil.createTable(head, results, desc)
        title = "数据库IO扣分详情分析"
        p1 = FormatUtil.sectionRes(title, table=table)

        result = results

    return p1, result


def getdfVal(conn, index_id, target_id, bt, et, iname):
    pdf = ""
    sql = '''
select a.record_time,c.description,a.metric_value,a.deduct
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (%s)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   and a.metric_value <> '最近1小时无有效采样记录'
   /*and b.use_flag = true*/
   and b.target_id = '%s'
   and a.record_time between '%s' and '%s'
   and a.metric_id = c.index_id
 order by a.deduct desc,a.record_time desc 
 limit 5
''' % (index_id, target_id, bt, et)

    cursor = getValue(conn, sql)
    results = cursor.fetchall()

    if (len(results) > 0):
        head = ["时间", "指标", "值", "扣分"]
        desc = iname + "扣分情况"
        table = CommUtil.createTable(head, results, desc)
        title = iname + "扣分情况"
        pdf = FormatUtil.sectionRes(title, table=table)

    return pdf


def getpwdpsVal(conn, target_id, bt, et):
    pdf = ""
    sql = '''
select a.record_time,c.description,a.metric_value,a.deduct
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2189010)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   and a.metric_value <> '最近1小时无有效采样记录'
   /*and b.use_flag = true*/
   and b.target_id = '%s'
   and a.record_time between '%s' and '%s'
   and a.metric_id = c.index_id
 order by a.deduct desc,a.record_time desc 
 limit 5
''' % (target_id, bt, et)

    cursor = getValue(conn, sql)
    results = cursor.fetchall()

    if (len(results) > 0):
        head = ["时间", "指标", "值", "扣分"]
        desc = "Physical Writes Direct Per Sec扣分情况"
        table = CommUtil.createTable(head, results, desc)
        title = "Physical Writes Direct Per Sec扣分情况"
        pdf = FormatUtil.sectionRes(title, table=table)

    return pdf


def getprdpsVal(conn, target_id, bt, et):
    pdf = ""
    sql = '''
select a.record_time,c.description,a.metric_value,a.deduct
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2189008)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   and a.metric_value <> '最近1小时无有效采样记录'
   /*and b.use_flag = true*/
   and b.target_id = '%s'
   and a.record_time between '%s' and '%s'
   and a.metric_id = c.index_id
 order by a.deduct desc,a.record_time desc 
 limit 5
''' % (target_id, bt, et)

    cursor = getValue(conn, sql)
    results = cursor.fetchall()

    if (len(results) > 0):
        head = ["时间", "指标", "值", "扣分"]
        desc = "Physical Reads Direct Per Sec扣分情况"
        table = CommUtil.createTable(head, results, desc)
        title = "Physical Reads Direct Per Sec扣分情况"
        pdf = FormatUtil.sectionRes(title, table=table)

    return pdf


def getSeriousDis(conn, target_id, bt, et):
    psd = ""
    sql = '''
with res as (
select a.record_time,c.description,a.metric_value,a.deduct,d.total_score
  from h_health_check_detail a,h_health_check b,mon_index c,h_model_item_metric d,h_model_item e
 where a.metric_id in (2189144,2189010,2189008, 2184304,2184305,2184302,2184303,2184306) 
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
        desc = "数据库IO严重扣分情况"
        table = CommUtil.createTable(head, results, desc)
        title = "数据库IO严重扣分情况分析"
        psd = FormatUtil.sectionRes(title, table=table)

    return psd


def getVal(index_id, conn, target_id, bt, et):
    pval = 0
    sql = '''
    select coalesce(round(avg(a.metric_value::numeric),2),0)
  from h_health_check_detail a,h_health_check b 
 where a.metric_id in (%s)
   and a.health_check_id = b.health_check_id
   /*and b.use_flag = true*/
   and b.target_id = '%s'
   and a.record_time between '%s' and '%s'
   and a.metric_value != '周期内无有效采样记录'
   and a.metric_value <> '最近1小时无有效采样记录'
''' % (index_id, target_id, bt, et)

    cursor = getValue(conn, sql)
    results = cursor.fetchone()
    pval = results[0]
    return pval


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
        sqldel1 = """delete from rpt_scope_detail where rpt_id='{0}' and target_id='{1}' and rpt_scope_category='H_IO_RI'
""".format(rpt_id, targetid)
        pg.execute(sqldel1)
        sqldel2 = """delete from rpt_scope_ded_history where rpt_id='{0}' and target_id='{1}' and rpt_scope_category='H_IO_RI'
""".format(rpt_id, targetid)
        pg.execute(sqldel2)
        sqldel3 = """delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module in ('health_io_metric_ri','health_io_score_ri')
""".format(rpt_id, targetid)
        pg.execute(sqldel3)

        ##ora = orautil.Oracle(host, usr, pwd, port, database)
        ##数据库IO入库
        insql = '''
insert into rpt_scope_detail(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_note,
                                                        rpt_scope_count,rpt_scope_ded_avg,rpt_scope_ded_max)    
with res as (
select a.metric_id,a.deduct,a.record_time,a.metric_value,b.target_id,b.total_score,a.iname
 from h_health_check_detail a,h_health_check b
where 
  a.metric_id in (2189144,2189010,2189008, 2184304,2184305,2184302,2184303,2184306)
  and a.health_check_id = b.health_check_id
  and a.metric_value <> '周期内无有效采样记录'
   and a.metric_value <> '最近1小时无有效采样记录'
  /*and b.use_flag = true*/
  and b.target_id = '{0}'
  and a.deduct<>0
  and a.record_time between '{1}' and '{2}'
) 
select '{3}' rptid,res.target_id target_id,'H_IO_RI' rsc,mi.index_id,res.iname,
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
            if res[0].startswith("db file parallel write"):
                if res[2] > 0:
                    lm = getVal(2184304, pg, targetid, lmbegintime, lmendtime)
                    bm = getVal(2184304, pg, targetid, begintime, endtime)
                    if lm > bm:
                        rlb = "有所下降"
                    elif lm < bm:
                        rlb = "有所上升"
                    else:
                        rlb = "基本持平"

                    result = '''
数据文件写延时存在超过正常水平的现象，说明数据库及服务器的数据文件写IO存在过高现象。
数据文件写IO延时超出正常范围会影响数据库的性能，严重时会出现数据库不稳定的问题。
该指标上个月的平均值为：''' + str(lm) + '''，本月平均值为：''' + str(bm) + '''，本月较上月''' + rlb + '''。
出现问题的时间段为：
'''
                    ##result += getdfVal(pg, 2184304, targetid, begintime, endtime, 'db file parallel write')
                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'health_io_metric_ri' rpt_finding_module,
0 rpt_finding_type,'2184304' rpt_sub_id,'' iname,
'db file parallel write存在扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)

                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_IO_RI' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2184304)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   and a.metric_value <> '最近1小时无有效采样记录'
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.record_time between '{2}' and '{3}'
   and a.metric_id = c.index_id
 order by a.deduct desc,a.metric_value::numeric desc 
 limit 20
'''.format(rpt_id, targetid, begintime, endtime)
                    pg.execute(insql_mf)

            elif res[0].startswith("db file scattered read"):
                if res[2] > 0:
                    lm = getVal(2184303, pg, targetid, lmbegintime, lmendtime)
                    bm = getVal(2184303, pg, targetid, begintime, endtime)
                    if lm > bm:
                        rlb = "有所上升"
                    elif lm < bm:
                        rlb = "有所下降"
                    else:
                        rlb = "基本持平"

                    result = '''
出现过数据文件多块读延时存在超过正常水平的现象，说明数据库及服务器的IO存在延时过高的现象。
数据文件多块读一般是全表扫描或者全索引扫描引起，IO延时超出正常范围会影响数据库的性能，严重时会出现数据库不稳定的问题。
该指标上个月的平均值为：''' + str(lm) + '''，本月平均值为：''' + str(bm) + '''，本月较上月''' + rlb + '''。
出现问题的时间段为：
'''
                    ##result += getdfVal(pg, 2184303, targetid, begintime, endtime, 'db file scattered read')

                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,2 rpt_finding_id,'health_io_metric_ri' rpt_finding_module,
0 rpt_finding_type,'2184303' rpt_sub_id,'' iname,
'db file scattered read存在扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)

                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_IO_RI' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2184303)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   and a.metric_value <> '最近1小时无有效采样记录'
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.record_time between '{2}' and '{3}'
   and a.metric_id = c.index_id
 order by a.deduct desc,a.metric_value::numeric desc 
 limit 20
'''.format(rpt_id, targetid, begintime, endtime)
                    pg.execute(insql_mf)

            elif res[0].startswith("db file sequential read"):
                if res[2] > 0:
                    lm = getVal(2184302, pg, targetid, lmbegintime, lmendtime)
                    bm = getVal(2184302, pg, targetid, begintime, endtime)
                    if lm > bm:
                        rlb = "有所上升"
                    elif lm < bm:
                        rlb = "有所下降"
                    else:
                        rlb = "基本持平"

                    result = '''
出现过数据文件单块读延时存在超过正常水平的现象，说明数据库及服务器的IO存在延时过高的现象。
数据文件单块读一般是通过索引访问数据的操作引起，IO延时超出正常范围会影响数据库的性能，严重时会出现数据库不稳定的问题。
该指标上个月的平均值为：''' + str(lm) + '''，本月平均值为：''' + str(bm) + '''，本月较上月''' + rlb + '''。
出现问题的时间段为：
'''
                    ##result += getdfVal(pg, 2184302, targetid, begintime, endtime, 'db file sequential read')
                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,3 rpt_finding_id,'health_io_metric_ri' rpt_finding_module,
0 rpt_finding_type,'2184302' rpt_sub_id,'' iname,
'db file sequential read存在扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)

                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_IO_RI' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2184302)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   and a.metric_value <> '最近1小时无有效采样记录'
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.record_time between '{2}' and '{3}'
   and a.metric_id = c.index_id
 order by a.deduct desc,a.metric_value::numeric desc 
 limit 20
'''.format(rpt_id, targetid, begintime, endtime)
                    pg.execute(insql_mf)

            elif res[0].startswith("control file parallel write"):
                if res[2] > 0:
                    lm = getVal(2184306, pg, targetid, lmbegintime, lmendtime)
                    bm = getVal(2184306, pg, targetid, begintime, endtime)
                    if lm > bm:
                        rlb = "有所上升"
                    elif lm < bm:
                        rlb = "有所下降"
                    else:
                        rlb = "基本持平"

                    result = '''
出现过控制文件并行写延时存在超过正常水平的现象，说明数据库及服务器的IO存在延时过高的现象。
控制文件并行写一般更新控制文件引起，IO延时超出正常范围会影响数据库的性能，严重时会出现数据库不稳定的问题，甚至导致数据库宕机。
该指标上个月的平均值为：''' + str(lm) + '''，本月平均值为：''' + str(bm) + '''，本月较上月''' + rlb + '''。
出现问题的时间段为：
'''
                    ##result += getdfVal(pg, 2184306, targetid, begintime, endtime, 'control file parallel write')
                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,4 rpt_finding_id,'health_io_metric_ri' rpt_finding_module,
0 rpt_finding_type,'2184306' rpt_sub_id,'' iname,
'control file parallel write存在扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)

                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_IO_RI' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2184306)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   and a.metric_value <> '最近1小时无有效采样记录'
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.record_time between '{2}' and '{3}'
   and a.metric_id = c.index_id
 order by a.deduct desc,a.metric_value::numeric desc 
 limit 20
'''.format(rpt_id, targetid, begintime, endtime)
                    pg.execute(insql_mf)

            elif res[0].startswith("log file parallel write"):
                if res[2] > 0:
                    lm = getVal(2184305, pg, targetid, lmbegintime, lmendtime)
                    bm = getVal(2184305, pg, targetid, begintime, endtime)
                    if lm > bm:
                        rlb = "有所上升"
                    elif lm < bm:
                        rlb = "有所下降"
                    else:
                        rlb = "基本持平"

                    result = '''
存在日志文件并行写延时存在超过正常水平的现象，说明数据库及服务器些日志文件的操作存在IO存在延时过高的现象。
日志文件并行写一般是LGWR写入在线日志引起，IO延时超出正常范围会影响数据库的性能，严重时会出现数据库不稳定的问题。
该指标上个月的平均值为：''' + str(lm) + '''，本月平均值为：''' + str(bm) + '''，本月较上月''' + rlb + '''。
出现问题的时间段为：
'''
                    ##result += getdfVal(pg, 2184305, targetid, begintime, endtime, 'log file parallel write')
                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,5 rpt_finding_id,'health_io_metric_ri' rpt_finding_module,
0 rpt_finding_type,'2184305' rpt_sub_id,'' iname,
'log file parallel write存在扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)

                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_IO_RI' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2184305)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   and a.metric_value <> '最近1小时无有效采样记录'
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.record_time between '{2}' and '{3}'
   and a.metric_id = c.index_id
 order by a.deduct desc,a.metric_value::numeric desc 
 limit 20
'''.format(rpt_id, targetid, begintime, endtime)
                    pg.execute(insql_mf)

            elif res[0].startswith("Physical Writes Direct Per Sec"):
                if res[2] > 0:
                    lm = getVal(2189010, pg, targetid, lmbegintime, lmendtime)
                    bm = getVal(2189010, pg, targetid, begintime, endtime)
                    if lm > bm:
                        rlb = "有所下降"
                    elif lm < bm:
                        rlb = "有所上升"
                    else:
                        rlb = "基本持平"

                    result = '''
存在物理直接写总量过大的问题，说明数据库中存在部分应用进行了直接路径装载操作。
建议与开发商确认出现问题时间段的直接路径装载是否合理。
该指标上个月平均值为：''' + str(lm) + '''，本月平均值为：''' + str(bm) + '''，本月较上月''' + rlb + '''。
出现问题的时间段如下：
'''
                    ##result += getpwdpsVal(pg, targetid, begintime, endtime)
                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,6 rpt_finding_id,'health_io_metric_ri' rpt_finding_module,
0 rpt_finding_type,'2189010' rpt_sub_id,'' iname,
'Physical Writes Direct Per Sec存在扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)

                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_IO_RI' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2189010)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   and a.metric_value <> '最近1小时无有效采样记录'
   /*and b.use_flag = true*/   
   and b.target_id = '{1}'
   and a.deduct <> 0
   and a.record_time between '{2}' and '{3}'
   and a.metric_id = c.index_id
 order by a.deduct desc,a.metric_value::numeric desc 
 limit 20
'''.format(rpt_id, targetid, begintime, endtime)
                    pg.execute(insql_mf)

            elif res[0].startswith("Physical Reads Direct Per Sec"):
                if res[2] > 0:
                    lm = getVal(2189008, pg, targetid, lmbegintime, lmendtime)
                    bm = getVal(2189008, pg, targetid, begintime, endtime)
                    if lm > bm:
                        rlb = "有所下降"
                    elif lm < bm:
                        rlb = "有所上升"
                    else:
                        rlb = "基本持平"

                    result = '''
存在物理直接读总量过大的问题，说明数据库中存在部分应用进行了直接路径读操作，该操作一般是由于频繁的小表全表扫描或者数据直接路径导出产生。
建议与开发商确认出现问题时间段的直接路径读是否合理。
该指标上个月平均值为：''' + str(lm) + '''，本月平均值为：''' + str(bm) + '''，本月较上月''' + rlb + '''。
出现问题的时间段如下：
'''
                    ##result += getprdpsVal(pg, targetid, begintime, endtime)
                    ismf = '''
insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                                                rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,6 rpt_finding_id,'health_io_metric_ri' rpt_finding_module,
0 rpt_finding_type,'2189008' rpt_sub_id,'' iname,
'Physical Reads Direct Per Sec存在扣分' rpt_finding_label,
'告警' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level
'''.format(rpt_id, targetid, result)
                    pg.execute(ismf)

                    insql_mf = '''
insert into rpt_scope_ded_history(rpt_id,target_id,rpt_scope_category,rpt_metric_id,iname,rpt_metric_name,rpt_metric_value,
                                                                 rpt_scope_ded,rpt_ded_datetime,rpt_serious)
select '{0}' rpt_id,b.target_id,'H_IO_RI' rpt_scope_category,a.metric_id,a.iname,c.description,a.metric_value::numeric,
           a.deduct,a.record_time,1 rpt_serious
  from h_health_check_detail a,h_health_check b,mon_index c
 where a.metric_id in (2189008)
   and a.health_check_id = b.health_check_id
   and a.metric_value <> '周期内无有效采样记录'
   and a.metric_value <> '最近1小时无有效采样记录'
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
select '{0}' rpt_id,'{1}' target_id,8 rpt_finding_id,'health_io_score_ri' rpt_finding_module,
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

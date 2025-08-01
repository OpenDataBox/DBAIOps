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
    ltag = ['9.0', '表空间']
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


def getdbid(pg, targetid):
    dbid = ""
    sql = "select subuid from mgt_system where uid='{0}'".format(targetid)
    sqlresult = getValue(pg, sql)
    for row in sqlresult:
        dbid = row[0]
    return dbid


def gettbsusage(conn, target_id, bt, et):
    p1 = ""
    sql = '''
with a as (
select col3 tbs,sum(col4::numeric) tbssize
  from p_oracle_cib 
 where index_id in (2201004)
   and target_id = '%s'
   and record_time between '%s' and '%s'
   and seq_id <> 0
   and record_time =
   (select max(record_time) from p_oracle_cib 
 where index_id in (2201004,2201005)
   and target_id = '%s'
   and record_time between '%s' and '%s'
   and seq_id <> 0)
   group by col3
), b as (
select distinct col1 tbs,col3 tbstype
  from p_oracle_cib 
 where index_id in (2201006)
   and target_id = '%s'
   and record_time between '%s' and '%s'
   and seq_id <> 0
   and record_time =
   (select max(record_time) from p_oracle_cib 
 where index_id in (2201006)
   and target_id = '%s'
   and record_time between '%s' and '%s'
   and seq_id <> 0) 
),aa as (
select col3 tbs,sum(col4::numeric) tbssize
  from p_oracle_cib 
 where index_id in (2201004)
   and target_id = '%s'
   and record_time between '%s'::timestamp - interval '1 month' and '%s'::timestamp - interval '1 month'
   and seq_id <> 0
   and record_time =
   (select max(record_time) from p_oracle_cib 
 where index_id in (2201004,2201005)
   and target_id = '%s'
   and record_time between '%s'::timestamp - interval '1 month' and '%s'::timestamp - interval '1 month'
   and seq_id <> 0)
   group by col3
)
select 
b.tbs,b.tbstype,coalesce(aa.tbssize,0) lm,coalesce(a.tbssize,0) bm,
case when coalesce(aa.tbssize,0)=0 or coalesce(a.tbssize,0)= coalesce(aa.tbssize,0) then 0
     when coalesce(a.tbssize,0)=0 then 0
     else round((a.tbssize-coalesce(aa.tbssize,0))/coalesce(aa.tbssize,0),0)
	 end ratio
  from b 
  left join a on b.tbs=a.tbs
  left join aa on b.tbs=aa.tbs
''' % (target_id, bt, et, target_id, bt, et, target_id, bt, et, target_id, bt, et, target_id, bt, et, target_id, bt, et)

    cursor = getValue(conn, sql)
    results = cursor.fetchall()
    if (len(results) > 0):
        head = ["表空间", "类型", "上月容量(MB)", "本月容量(MB)", "增长率"]
        desc = "表空间使用率分析"
        table = CommUtil.createTable(head, results, desc)
        title = "表空间使用率分析"
        p1 = FormatUtil.sectionRes(title, table=table)

    return p1


def getsysaux(conn, targetid, bt, et):
    p1 = ""
    sql = '''
select distinct col1,col2,col3
from p_oracle_cib where  record_time =
(select max(record_time) from p_oracle_cib 
where target_id = '{0}'
and index_id = 2202011
and record_time between '{1}' and '{2}'
) and index_id = 2202011
and target_id = '{0}'
and seq_id <> 0
'''.format(targetid, bt, et)

    cursor = getValue(conn, sql)
    results = cursor.fetchall()
    resld = []

    if (len(results) > 0):
        for x in results:
            resld.append(dict(owner=x[0], rl=x[1], ratio=x[2]))

        sql = ""
        for res in resld:
            sql += "select '" + res.get('owner') + "' c1," + str(res.get('rl')) + " c2," + str(
                res.get('ratio')) + " c3 union all "
        sql = sql[0:-10]
        p1 = sql

    return p1


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
        ##ora = orautil.Oracle(host, usr, pwd, port, database)
        ##result = "SCREEN_BEGIN9 表空间与数据文件分析SCREEN_END\n"
        result = ""
        # result += "SCREEN_BEGIN检查表空间使用率，是否存在表空间满的隐患\nSCREEN_END"

        target_id = getdbid(pg, targetid)
        res = gettbsusage(pg, target_id, begintime, endtime)

        if (len(res) > 0):
            ##result += res
            insql_mf = '''
begin;
delete from rpt_ts_size where rpt_id='%s' and target_id='%s';

insert into rpt_ts_size(rpt_id,rpt_name,rpt_type,rpt_size,rpt_size_l,rpt_ratio,target_id)
with a as (
select col3 tbs,sum(col4::numeric) tbssize
  from p_oracle_cib 
 where index_id in (2201004)
   and target_id = '%s'
   and record_time between '%s' and '%s'
   and seq_id <> 0
   and record_time =
   (select max(record_time) from p_oracle_cib 
 where index_id in (2201004,2201005)
   and target_id = '%s'
   and record_time between '%s' and '%s'
   and seq_id <> 0)
   group by col3
), b as (
select distinct col1 tbs,col3 tbstype
  from p_oracle_cib 
 where index_id in (2201006)
   and target_id = '%s'
   and record_time between '%s' and '%s'
   and seq_id <> 0
   and record_time =
   (select max(record_time) from p_oracle_cib 
 where index_id in (2201006)
   and target_id = '%s'
   and record_time between '%s' and '%s'
   and seq_id <> 0) 
),aa as (
select col3 tbs,sum(col4::numeric) tbssize
  from p_oracle_cib 
 where index_id in (2201004)
   and target_id = '%s'
   and record_time between '%s'::timestamp - interval '1 month' and '%s'::timestamp - interval '1 month'
   and seq_id <> 0
   and record_time =
   (select max(record_time) from p_oracle_cib 
 where index_id in (2201004,2201005)
   and target_id = '%s'
   and record_time between '%s'::timestamp - interval '1 month' and '%s'::timestamp - interval '1 month'
   and seq_id <> 0)
   group by col3
)
select '%s' rptid,
b.tbs,b.tbstype,coalesce(trunc(a.tbssize),0) bm,coalesce(trunc(aa.tbssize),0) lm,
case when coalesce(aa.tbssize,0)=0 or coalesce(a.tbssize,0)= coalesce(aa.tbssize,0) then 0
     when coalesce(a.tbssize,0)=0 then 0
     else round((a.tbssize-coalesce(aa.tbssize,0))/coalesce(aa.tbssize,0)*100,0)
	 end ratio,'%s' target_id
  from b 
  left join a on b.tbs=a.tbs
  left join aa on b.tbs=aa.tbs;
end;
''' % (rpt_id, targetid, target_id, begintime, endtime, target_id, begintime, endtime, target_id, begintime, endtime,
       target_id, begintime, endtime, target_id, begintime, endtime, target_id, begintime, endtime, rpt_id, targetid)
            pg.execute(insql_mf)

        ##result += "SCREEN_BEGIN\\nSYSAUX表空间使用情况进一步分析\nSCREEN_END"
        res_sysaux = getsysaux(pg, targetid, begintime, endtime)
        if (len(res_sysaux) > 0):
            # result += res_sysaux
            result = '''
清除建议：
请参考Oracle MOS (文档 ID 1965061.1)执行相关清理操作
1、AWR信息历史数据
2、统计信息历史数据
3、Advisor历史数据
'''
            ismf = '''
begin;
delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module='ts_size';

insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'ts_size' rpt_finding_module,
0 rpt_finding_type,'' rpt_sub_id,'' iname,
'SYSAUX表空间使用情况进一步分析' rpt_finding_label,
'信息' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
0 rpt_finding_level;
end;
'''.format(rpt_id, targetid, result)
            pg.execute(ismf)

            sqlf = """
begin;
delete from rpt_sysaux_obj where rpt_id='{0}' and target_id='{2}';
insert into rpt_sysaux_obj(rpt_id,rpt_name,rpt_size,rpt_ratio,target_id)
select '{0}' rptid,res.c1,res.c2,res.c3,'{2}' target_id
from ({1}) res;
end;""".format(rpt_id, res_sysaux, targetid)
            pg.execute(sqlf)

    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

    # except Exception as e:
    #    errorInfo = str(e)
    #    print("异常：" + errorInfo)

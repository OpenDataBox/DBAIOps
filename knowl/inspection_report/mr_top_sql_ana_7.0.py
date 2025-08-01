#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

sys.path.append('/usr/software/knowl')
import DBUtil
import psycopg2
import re
import PGUtil
import ResultCode
import tags
import top_sql


def register(file_name):
    ltag = ['7.0', 'SQL']
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

    ana = ""
    table = ""
    pg = PGUtil.Postgre(dbip, username, password, pgport, dbname)

    try:
        ##逻辑读
        flag = False
        ana, table = top_sql.get_buffer_gets(pg, targetid, begintime, endtime, flag)
        sqlljd = '''
begin;
delete from rpt_top_sql_ri where rpt_id='{0}' and target_id='{1}' and rpt_type='逻辑读';

insert into rpt_top_sql_ri(rpt_id,target_id,rpt_c1,rpt_c2,rpt_c3,rpt_c4,rpt_c5,rpt_c6,rpt_type)
 select distinct '{0}' rptid,'{1}' targetid,sql_id,sqltext,
  buffer_get_delta,
  executions_delta,
  gets_per_exec,
  elapsed_time_seconds,
  '逻辑读' rpt_type
from (select
        buffer_get_delta,
        executions_delta,
        round(case when executions_delta = 0 then 0
              else buffer_get_delta / executions_delta end) gets_per_exec,
        elapsed_time_delta / 1000000                        elapsed_time_seconds,
        s.sql_id,
        substring(t.sqltext, 1, 100)                        sqltext
      from (select
              max(buffer_gets) - min(buffer_gets)   buffer_get_delta,
              max(executions) - min(executions)     executions_delta,
              max(elapsed_time) - min(elapsed_time) elapsed_time_delta,
              target_id,
              sql_id
            from sqlstat s
            where target_id = '{1}'
              and s.type=2
              and s.record_time between '{2}' and '{3}'
            group by target_id, sql_id) s, sqltext t
      where s.sql_id = t.sql_id and s.target_id = t.target_id and s.buffer_get_delta > 0
      order by 1 desc) as foo
limit 100;
end;
'''.format(rpt_id, targetid, begintime, endtime)
        pg.execute(sqlljd)

        if ana and ana != "RED_BOLD_BEGINRED_BOLD_END":
            ismf = '''
begin;
delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module='top_sql_ri' and rpt_finding_label='逻辑读高SQL分析';

insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'top_sql_ri' rpt_finding_module,
0 rpt_finding_type,'' rpt_sub_id,'' iname,
'逻辑读高SQL分析' rpt_finding_label,
'信息' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level;

end;
'''.format(rpt_id, targetid, ana)
            pg.execute(ismf)

        ##物理读
        ana, table = top_sql.get_disk_reads(pg, targetid, begintime, endtime, flag)
        sqlwld = '''
begin;
delete from rpt_top_sql_ri where rpt_id='{0}' and target_id='{1}' and rpt_type='物理读';

insert into rpt_top_sql_ri(rpt_id,target_id,rpt_c1,rpt_c2,rpt_c3,rpt_c4,rpt_c5,rpt_c6,rpt_type)
SELECT distinct '{0}' rptid,'{1}' targetid,sql_id,sqltext,
    disk_reads_delta,
    executions_delta,
    reads_per_exec,
    elapsed_time_seconds,
    '物理读' rpt_type
FROM ( SELECT
    disk_reads_delta,
    executions_delta,
    round(CASE
        WHEN executions_delta = 0   THEN 0
        ELSE disk_reads_delta / executions_delta
    END) reads_per_exec,
    round(elapsed_time_delta / 1000000,2) elapsed_time_seconds,
    s.sql_id,
    substring(t.sqltext,1,100) sqltext
FROM ( SELECT
    MAX(disk_reads) - MIN(disk_reads) disk_reads_delta,
    MAX(executions) - MIN(executions) executions_delta,
    MAX(elapsed_time) - MIN(elapsed_time) elapsed_time_delta,
    target_id,
    sql_id
FROM
    sqlstat s where target_id ='{1}'
AND s.type = 2
    AND s.record_time BETWEEN '{2}' AND '{3}'
     group BY target_id,sql_id) s,sqltext t
WHERE
    s.sql_id = t.sql_id and s.disk_reads_delta > 0
    AND s.target_id = t.target_id order BY 1 DESC ) as foo limit 100;
end;
'''.format(rpt_id, targetid, begintime, endtime)
        pg.execute(sqlwld)

        if ana and ana != "RED_BOLD_BEGINRED_BOLD_END":
            ismf = '''
begin;
delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module='top_sql_ri' and rpt_finding_label='物理读高SQL分析';

insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'top_sql_ri' rpt_finding_module,
0 rpt_finding_type,'' rpt_sub_id,'' iname,
'物理读高SQL分析' rpt_finding_label,
'信息' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level;

end;
'''.format(rpt_id, targetid, ana)
            pg.execute(ismf)

        ##执行次数
        ana, table = top_sql.get_exec_sql(pg, targetid, begintime, endtime, flag)
        sqlzxcs = '''
begin;
delete from rpt_top_sql_ri where rpt_id='{0}' and target_id='{1}' and rpt_type='执行次数';

insert into rpt_top_sql_ri(rpt_id,target_id,rpt_c1,rpt_c2,rpt_c3,rpt_c4,rpt_c5,rpt_c6,rpt_type)
SELECT distinct '{0}' rptid,'{1}' targetid,sql_id,sqltext,
    executions_delta,
    rows_processed_delta,
    rows_per_exec,
    elapsed_time_seconds,
    '执行次数' rpt_type
FROM ( SELECT
    executions_delta,
    rows_processed_delta,
    round(CASE
        WHEN executions_delta = 0   THEN 0
        ELSE rows_processed_delta / executions_delta
    END,2) rows_per_exec,
    round(elapsed_time_delta / 1000000,2) elapsed_time_seconds,
    s.sql_id,
    substring(t.sqltext,1,100) sqltext
FROM ( SELECT
    MAX(executions) - MIN(executions) executions_delta,
    MAX(elapsed_time) - MIN(elapsed_time) elapsed_time_delta,
    MAX(rows_processed) - MIN(rows_processed) rows_processed_delta,
    target_id,
    sql_id
FROM
    sqlstat s where target_id ='{1}'
AND s.type = 2
    AND s.record_time BETWEEN '{2}' AND '{3}'
group BY target_id, sql_id) s,
sqltext t
WHERE
    s.sql_id = t.sql_id and s.executions_delta > 0
    AND s.target_id = t.target_id order BY 1 DESC ) as foo limit 100;
end;
'''.format(rpt_id, targetid, begintime, endtime)
        pg.execute(sqlzxcs)

        if ana and ana != "RED_BOLD_BEGINRED_BOLD_END":
            ismf = '''
begin;
delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module='top_sql_ri' and rpt_finding_label='执行次数高SQL分析';

insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'top_sql_ri' rpt_finding_module,
0 rpt_finding_type,'' rpt_sub_id,'' iname,
'执行次数高SQL分析' rpt_finding_label,
'信息' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level;

end;
'''.format(rpt_id, targetid, ana)
            pg.execute(ismf)

        ##执行时间
        ana, table = top_sql.get_elapsed_time(pg, targetid, begintime, endtime, flag)
        sqlzxsj = '''
begin;
delete from rpt_top_sql_ri where rpt_id='{0}' and target_id='{1}' and rpt_type='执行时间';

insert into rpt_top_sql_ri(rpt_id,target_id,rpt_c1,rpt_c2,rpt_c3,rpt_c4,rpt_c5,rpt_type)
SELECT distinct '{0}' rptid,'{1}' targetid,sql_id,sqltext,
  elapsed_time_seconds,
  executions_delta,
  elapsed_time_per_exec,
  '执行时间' rpt_type
from (select
        round(elapsed_time_delta / 1000000, 2)                             elapsed_time_seconds,
        executions_delta,
        round(case when executions_delta = 0
          then 0
              else elapsed_time_delta / executions_delta / 1000000 end, 2) elapsed_time_per_exec,
        s.sql_id,
        substring(t.sqltext, 1, 100)                                       sqltext
      from (select
              max(elapsed_time) - min(elapsed_time) elapsed_time_delta,
              max(executions) - min(executions)     executions_delta,
              target_id,
              sql_id
            from sqlstat s
            where target_id = '{1}' and s.type=2
              and s.record_time between '{2}' and '{3}'
            group by target_id, sql_id) s, sqltext t
      where s.sql_id = t.sql_id and s.target_id = t.target_id
      order by 1 desc) as foo where elapsed_time_seconds > 0
limit 100;
end;
'''.format(rpt_id, targetid, begintime, endtime)
        pg.execute(sqlzxsj)

        if ana and ana != "RED_BOLD_BEGINRED_BOLD_END":
            ismf = '''
begin;
delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module='top_sql_ri' and rpt_finding_label='执行时间高SQL分析';

insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'top_sql_ri' rpt_finding_module,
0 rpt_finding_type,'' rpt_sub_id,'' iname,
'执行时间高SQL分析' rpt_finding_label,
'信息' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level;
end;
'''.format(rpt_id, targetid, ana)
            pg.execute(ismf)

        ##CPU时间
        ana, table = top_sql.getcputime(pg, targetid, begintime, endtime, flag)
        sqlcpusj = '''
begin;
delete from rpt_top_sql_ri where rpt_id='{0}' and target_id='{1}' and rpt_type='CPU时间';

insert into rpt_top_sql_ri(rpt_id,target_id,rpt_c1,rpt_c2,rpt_c3,rpt_c4,rpt_c5,rpt_c6,rpt_type)
SELECT distinct '{0}' rptid,'{1}' targetid,sql_id,sqltext,
  cpu_time_seconds,
  executions_delta,
  cpu_time_per_exec,
  elapsed_time_seconds,
  'CPU时间'
from (select
        round(cpu_time_delta / 1000000, 2)                             cpu_time_seconds,
        executions_delta,
        round(case when executions_delta = 0
          then 0
              else cpu_time_delta / executions_delta / 1000000 end, 2) cpu_time_per_exec,
        round(elapsed_time_delta / 1000000, 2)                         elapsed_time_seconds,
        s.sql_id,
        substring(t.sqltext, 1, 100)                                   sqltext
      from (
             select
               max(cpu_time) - min(cpu_time)         cpu_time_delta,
               max(elapsed_time) - min(elapsed_time) elapsed_time_delta,
               max(executions) - min(executions)     executions_delta,
               target_id,
               sql_id
             from sqlstat s
             where target_id = '{1}' and s.type=2
               and s.record_time between '{2}' and '{3}'
             group by target_id, sql_id) s, sqltext t
      where s.sql_id = t.sql_id and s.target_id = t.target_id
      order by 1 desc) as foo where cpu_time_seconds > 0
limit 100;
end;
'''.format(rpt_id, targetid, begintime, endtime)
        pg.execute(sqlcpusj)

        if ana and ana != "RED_BOLD_BEGINRED_BOLD_END":
            ismf = '''
begin;
delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module='top_sql_ri' and rpt_finding_label='CPU时间高SQL分析';

insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'top_sql_ri' rpt_finding_module,
0 rpt_finding_type,'' rpt_sub_id,'' iname,
'CPU时间高SQL分析' rpt_finding_label,
'信息' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level;

end;
'''.format(rpt_id, targetid, ana)
            pg.execute(ismf)

        ##解析调用
        ana, table = top_sql.get_parse_calls(pg, targetid, begintime, endtime, flag)
        sqljxdy = '''
begin;
delete from rpt_top_sql_ri where rpt_id='{0}' and target_id='{1}' and rpt_type='解析调用';

insert into rpt_top_sql_ri(rpt_id,target_id,rpt_c1,rpt_c2,rpt_c3,rpt_c4,rpt_c5,rpt_type)
SELECT distinct '{0}' rptid,'{1}' targetid,sql_id,sqltext,
    parse_calls_delta,
    executions_delta,
    case when ( SELECT
     SUM(total_parse_calls)
 FROM ( SELECT
     MAX(parse_calls) - MIN(parse_calls) total_parse_calls
 FROM
     sqlstat s where target_id ='{1}'
 AND s.record_time BETWEEN '{2}' AND '{3}'
 AND type = 2
 group BY target_id,sql_id ) as foo)=0 then 0 else
    round(parse_calls_delta/( SELECT
     SUM(total_parse_calls)
 FROM ( SELECT
     MAX(parse_calls) - MIN(parse_calls) total_parse_calls
 FROM
     sqlstat s where target_id ='{1}'
 AND s.record_time BETWEEN '{2}' AND '{3}'
 AND type = 2
 group BY target_id,sql_id ) as foo)*100,2) end perc,
    '解析调用'
FROM ( SELECT
    parse_calls_delta,
    executions_delta,
    s.sql_id,
    substring(t.sqltext,1,80) sqltext
FROM ( SELECT
    MAX(parse_calls) - MIN(parse_calls) parse_calls_delta,
    MAX(executions) - MIN(executions) executions_delta,
    target_id,
    sql_id
FROM
    sqlstat s where target_id ='{1}'
AND s.type = 2
    AND s.record_time BETWEEN '{2}' AND '{3}'
group BY target_id,sql_id) s,sqltext t
WHERE
    s.sql_id = t.sql_id and s.parse_calls_delta > 0
    AND s.target_id = t.target_id order BY 1 DESC ) as foo limit 100;
end;
'''.format(rpt_id, targetid, begintime, endtime)
        pg.execute(sqljxdy)

        if ana and ana != "RED_BOLD_BEGINRED_BOLD_END":
            ismf = '''
begin;
delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module='top_sql_ri' and rpt_finding_label='解析调用高SQL分析';

insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'top_sql_ri' rpt_finding_module,
0 rpt_finding_type,'' rpt_sub_id,'' iname,
'解析调用高SQL分析' rpt_finding_label,
'信息' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level;

end;
'''.format(rpt_id, targetid, ana)
            pg.execute(ismf)

        ##子游标数量
        ana, table = top_sql.get_version_count(pg, targetid, begintime, endtime, flag)
        sqlzybsl = '''
begin;
delete from rpt_top_sql_ri where rpt_id='{0}' and target_id='{1}' and rpt_type='子游标数量';

insert into rpt_top_sql_ri(rpt_id,target_id,rpt_c1,rpt_c2,rpt_c3,rpt_c4,rpt_type)
SELECT distinct '{0}' rptid,'{1}' targetid,sql_id,sqltext,
	version_cnt,
	executions_delta,
        '子游标数量'
from 
(select version_cnt,executions_delta,s.sql_id,substring(t.sqltext,1,100) sqltext from (
select max(child_number) version_cnt,
max(executions) - min(executions) executions_delta,target_id,
sql_id from sqlstat s where target_id = '{1}' and s.type = 2 and 
s.record_time between  '{2}' and '{3}'
group by target_id,sql_id) s,sqltext t where s.sql_id=t.sql_id 
and s.target_id=t.target_id order by 1 desc) as foo limit 100;
end;
'''.format(rpt_id, targetid, begintime, endtime)
        pg.execute(sqlzybsl)

        if ana and ana != "RED_BOLD_BEGINRED_BOLD_END":
            ismf = '''
begin;
delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module='top_sql_ri' and rpt_finding_label='子游标数量高SQL分析';

insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'top_sql_ri' rpt_finding_module,
0 rpt_finding_type,'' rpt_sub_id,'' iname,
'子游标数量高SQL分析' rpt_finding_label,
'信息' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level;

end;
'''.format(rpt_id, targetid, ana)
            pg.execute(ismf)

        ##多执行计划
        ana, table = top_sql.getmoreplan(pg, targetid, begintime, endtime, flag)
        sqldzxjh = '''
begin;
delete from rpt_top_sql_ri where rpt_id='{0}' and target_id='{1}' and rpt_type='多执行计划';

insert into rpt_top_sql_ri(rpt_id,target_id,rpt_c1,rpt_c2,rpt_c3,rpt_c4,rpt_c5,rpt_c6,rpt_c7,rpt_c8,rpt_type)
SELECT distinct '{0}' rptid,'{1}' targetid,sql_id,
       plan_hash_value,
       sum(disk_reads) disk_reads_total,
       sum(buffer_gets) buffer_gets_total,
       sum(executions) executions_total,
       round(sum(elapsed_time)/1000000,2) elapsed_time_total,
       round(sum(buffer_gets)/sum(executions),2) gets_per_exec,
       round(sum(elapsed_time)/1000000/sum(executions),2) elapsed_time_per_exec,
       '多执行计划'
  from (select sql_id,
               child_number,
               plan_hash_value,
               max(executions) executions,
               max(disk_reads) disk_reads,
               max(buffer_gets) buffer_gets,
               max(elapsed_time) elapsed_time
          from sqlstat s
         where sql_id in ( select sql_id
from (select distinct
        sql_id,
        plan_hash_value
      from sqlstat s
      where target_id ='{1}' and s.record_time between 
	 '{2}' and '{3}') as foo
group by sql_id
having count(sql_id) > 1)
           and target_id = '{1}'
           and type=1
           and s.record_time between
               '{2}' and '{3}'
         group by sql_id, child_number, plan_hash_value) s
 where executions <> 0
 group by sql_id, plan_hash_value;
end;
'''.format(rpt_id, targetid, begintime, endtime)
        pg.execute(sqldzxjh)

        if ana and ana != "RED_BOLD_BEGINRED_BOLD_END":
            ismf = '''
begin;
delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module='top_sql_ri' and rpt_finding_label='多执行计划SQL分析';

insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'top_sql_ri' rpt_finding_module,
0 rpt_finding_type,'' rpt_sub_id,'' iname,
'多执行计划SQL分析' rpt_finding_label,
'信息' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level;

end;
'''.format(rpt_id, targetid, ana)
            pg.execute(ismf)

        ##集群等待时间
        ana, table = top_sql.get_cluster_wait_time(pg, targetid, begintime, endtime, flag)
        sqljqddsj = '''
begin;
delete from rpt_top_sql_ri where rpt_id='{0}' and target_id='{1}' and rpt_type='集群等待时间';

insert into rpt_top_sql_ri(rpt_id,target_id,rpt_c1,rpt_c2,rpt_c3,rpt_c4,rpt_c5,rpt_c6,rpt_c7,rpt_type)
SELECT distinct '{0}' rptid,'{1}' targetid,sql_id,sqltext,
  cluster_wait_time_seconds,
    round(cluster_wait_time_seconds / case when elapsed_time_seconds = 0
    then 1
                                    else elapsed_time_seconds * 100 end, 2),
  elapsed_time_seconds,
  cpu_time_seconds,
  executions_delta,
  '集群等待时间'
from (select
        cluster_wait_time_delta / 10000000 cluster_wait_time_seconds,
        executions_delta,
        elapsed_time_delta / 1000000                        elapsed_time_seconds,
        cpu_time_delta / 1000000 cpu_time_seconds,
        s.sql_id,
        substring(t.sqltext, 1, 100)                        sqltext
      from (select
              max(cluster_wait_time) - min(cluster_wait_time)   cluster_wait_time_delta,
              max(executions) - min(executions)     executions_delta,
              max(elapsed_time) - min(elapsed_time) elapsed_time_delta,
              max(cpu_time) - min(cpu_time) cpu_time_delta,
              target_id,
              sql_id
            from sqlstat s
            where target_id = '{1}'
              and s.type=2
              and s.record_time between '{2}' and '{3}'
            group by target_id, sql_id) s, sqltext t
      where s.sql_id = t.sql_id and s.target_id = t.target_id
      order by 1 desc) as foo where elapsed_time_seconds > 0
limit 100;
end;
'''.format(rpt_id, targetid, begintime, endtime)
        pg.execute(sqljqddsj)

        if ana and ana != "RED_BOLD_BEGINRED_BOLD_END":
            ismf = '''
begin;
delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module='top_sql_ri' and rpt_finding_label='集群等待时间高SQL分析';

insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'top_sql_ri' rpt_finding_module,
0 rpt_finding_type,'' rpt_sub_id,'' iname,
'集群等待时间高SQL分析' rpt_finding_label,
'信息' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
1 rpt_finding_level;

end;
'''.format(rpt_id, targetid, ana)
            pg.execute(ismf)

    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

    # except Exception as e:
    #    errorInfo = str(e)
    #    print("异常：" + errorInfo)

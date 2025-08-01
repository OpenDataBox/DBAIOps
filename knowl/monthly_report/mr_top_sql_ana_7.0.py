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


def getawrsqlstat(conn, target_id, bt, et):
    p1 = ""
    sql = '''
select sql_id,executions,elapsed_time,cpu_time,buffer_gets,disk_reads,plan_char
  from ora_sqlstat 
 where snap_time between '%s' and '%s'
   and dbid::varchar in (select subuid from mgt_system where uid='%s')
''' % (bt, et, target_id)

    cursor = getValue(conn, sql)
    results = cursor.fetchall()

    if (len(results) > 0):
        head = ["SQL_ID", "执行次数", "总耗时", "CPU耗时", "逻辑读", "物理读", "执行计划特征"]
        desc = "高开销SQL分析"
        table = CommUtil.createTable(head, results, desc)
        title = "高开销SQL分析"
        p1 = FormatUtil.sectionRes(title, table=table)

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
        ##result = "SCREEN_BEGIN7 高开销SQL分析SCREEN_END"
        result = ""
        res = getawrsqlstat(pg, targetid, begintime, endtime)

        if (len(res) > 0):
            result = '''
建议：
1、对于有多个执行计划的，通过sql profile或sql baseline固定执行计划
2、调整执行计划
3、增加索引
'''
            ismf = '''
begin;
delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module='top_sql';

insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'top_sql' rpt_finding_module,
0 rpt_finding_type,'' rpt_sub_id,'' iname,
'高开销sql分析' rpt_finding_label,
'信息' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
0 rpt_finding_level;
end;
'''.format(rpt_id, targetid, result)
            pg.execute(ismf)
        insql_mf = '''
begin;
delete from rpt_top_sql where rpt_id='{0}' and target_id='{3}';

insert into rpt_top_sql(rpt_id,rpt_sql_id,rpt_executions,rpt_elapsed_time,
						rpt_cpu_time,rpt_bufferpt_gets,rpt_physical_reads,rpt_plan_char,target_id)
select '{0}' rptid,sql_id,executions,elapsed_time,cpu_time,buffer_gets,disk_reads,plan_char,'{3}' target_id
  from ora_sqlstat 
 where snap_time between '{1}' and '{2}'
   and dbid::varchar in (select subuid from mgt_system where uid='{3}');
end;
'''.format(rpt_id, begintime, endtime, targetid)
        # print(insql_mf)
        pg.execute(insql_mf)

    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

    # except Exception as e:
    #    errorInfo = str(e)
    #    print("异常：" + errorInfo)

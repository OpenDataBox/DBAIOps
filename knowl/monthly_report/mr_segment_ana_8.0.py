#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

sys.path.append('/usr/software/knowl')
import DBUtil
import psycopg2
import cx_Oracle as oracle
import re
import CommUtil
import PGUtil
import FormatUtil
import ResultCode
import tags


def register(file_name):
    ltag = ['8.0', '段管理']
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


def getawrobjstat(conn, target_id, bt, et):
    p1 = ""
    sql = '''
select owner,object_name,object_type,space_size,space_allocated,space_used
  from ora_objstat
 where snap_time between '%s' and '%s'
   and dbid::varchar in (select subuid from mgt_system where uid='%s')
''' % (bt, et, target_id)

    cursor = getValue(conn, sql)
    results = cursor.fetchall()

    if (len(results) > 0):
        head = ["属主", "段名", "类型", "大小", "分配量", "使用量"]
        desc = "空间分配/使用量较大段分析"
        table = CommUtil.createTable(head, results, desc)
        title = "空间分配/使用量较大段分析"
        p1 = FormatUtil.sectionRes(title, table=table)

    return p1


def get82(conn, targetid, bt, et):
    p1 = ""
    sql = """
select distinct col1,col2,col3,col4,col5,col6
from p_oracle_cib where  record_time =
(select max(record_time) from p_oracle_cib 
where target_id = '{0}'
and index_id = 2202006
and record_time between '{1}' and '{2}'
) and index_id = 2202006
and target_id = '{0}'
and seq_id <> 0
""".format(targetid, bt, et, targetid)

    cursor = getValue(conn, sql)
    results = cursor.fetchall()

    resld = []

    if (len(results) > 0):
        for x in results:
            resld.append(dict(owner=x[0], segname=x[1], segtype=x[2], nrext=x[3], maxext=x[4], extmb=x[5]))

        sql = ""
        for res in resld:
            sql += "select '" + res.get('owner') + "' c1,'" + res.get('segname') + "' c2,'" + res.get(
                'segtype') + "' c3," + str(res.get('nrext')) + " c4," + str(res.get('maxext')) + " c5,'" + res.get(
                'extmb') + "' c6 union all "
        sql = sql[0:-10]
        p1 = sql

    return p1


def get83(conn, targetid, bt, et):
    p1 = ""
    sql = '''
select distinct col1,col2,col3,col4,col5,col6
from p_oracle_cib where  record_time =
(select max(record_time) from p_oracle_cib 
where target_id = '{0}'
and index_id = 2202007
and record_time between '{1}' and '{2}'
) and index_id = 2202007
and target_id = '{0}'
and seq_id <> 0
'''.format(targetid, bt, et)

    cursor = getValue(conn, sql)
    results = cursor.fetchall()
    resld = []

    if (len(results) > 0):
        for x in results:
            resld.append(dict(owner=x[0], indname=x[1], tabname=x[2], indsize=x[3], tabsize=x[4], ratio=x[5]))

        sql = ""
        for res in resld:
            sql += "select '" + res.get('owner') + "' c1,'" + res.get('indname') + "' c2,'" + res.get(
                'tabname') + "' c3," + str(res.get('indsize')) + " c4," + str(res.get('tabsize')) + " c5," + str(
                res.get('ratio')) + " c6 union all "
        sql = sql[0:-10]
        p1 = sql

    return p1


def get84(conn, targetid, bt, et):
    p1 = ""
    sql = '''
select distinct col1,col2
from p_oracle_cib where  record_time =
(select max(record_time) from p_oracle_cib 
where target_id = '{0}'
and index_id = 2202008
and record_time between '{1}' and '{2}'
) and index_id = 2202008
and target_id = '{0}'
and seq_id <> 0
'''.format(targetid, bt, et)

    cursor = getValue(conn, sql)
    results = cursor.fetchall()

    resld = []

    if (len(results) > 0):
        for x in results:
            resld.append(dict(segcnt=x[0], segsize=x[1]))

        sql = ""
        for res in resld:
            sql += "select '非临时表空间中临时段数量：'||" + str(res.get('segcnt')) + " c1," + str(
                res.get('segsize')) + " c2 union all "
        sql = sql[0:-10]
        p1 = sql

    return p1


def get85(conn, targetid, bt, et):
    p1 = ""
    sql = '''
select distinct col1,col2,col3,col4,col5
from p_oracle_cib where  record_time =
(select max(record_time) from p_oracle_cib 
where target_id = '{0}'
and index_id = 2202009
and record_time between '{1}' and '{2}'
) and index_id = 2202009
and target_id = '{0}'
and seq_id <> 0
'''.format(targetid, bt, et)

    cursor = getValue(conn, sql)
    results = cursor.fetchall()

    resld = []

    if (len(results) > 0):
        for x in results:
            resld.append(dict(owner=x[0], segname=x[1], segtype=x[2], segsize=x[3], tabname=x[4]))

        sql = ""
        for res in resld:
            sql += "select '" + res.get('owner') + "' c1,'" + res.get('segname') + "' c2,'" + res.get(
                'segtype') + "' c3," + str(res.get('segsize')) + " c4,'" + res.get('tabname') + "' c5 union all "
        sql = sql[0:-10]
        p1 = sql

    return p1


def get86(conn, targetid, bt, et):
    p1 = ""
    sql = '''
select distinct col1,col2,col3,col4
from p_oracle_cib where  record_time =
(select max(record_time) from p_oracle_cib 
where target_id = '{0}'
and index_id = 2202010
and record_time between '{1}' and '{2}'
) and index_id = 2202010
and target_id = '{0}'
and seq_id <> 0
'''.format(targetid, bt, et)

    cursor = getValue(conn, sql)
    results = cursor.fetchall()

    resld = []

    if (len(results) > 0):
        for x in results:
            resld.append(dict(owner=x[0], segname=x[1], tbssize=x[2], tbsname=x[3]))

        sql = ""
        for res in resld:
            sql += "select '" + res.get('owner') + "' c1,'" + res.get('segname') + "' c2,'" + str(
                res.get('tbssize')) + "' c3,'" + res.get('tbsname') + "' c4 union all "
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
        # result = "7 段分析"
        result = ""
        res = getawrobjstat(pg, targetid, begintime, endtime)

        if (len(res) > 0):
            result = '''
建议：
1、检查表上的执行计划，并且必要时增加索引
2、如果存在较多的delete或update，定期进行碎片整理
3、检查是否属于临时使用的表，用完即删
'''

            ismf = '''
begin;
delete from rpt_finding where rpt_id='{0}' and target_id='{1}' and rpt_finding_module='seg_top';

insert into rpt_finding(rpt_id,target_id,rpt_finding_id,rpt_finding_module,rpt_finding_type,rpt_sub_id,iname,
                        rpt_finding_label,rpt_finding_alarm_level,rpt_finding_text,rpt_finding_level)
select '{0}' rpt_id,'{1}' target_id,1 rpt_finding_id,'seg_top' rpt_finding_module,
0 rpt_finding_type,'' rpt_sub_id,'' iname,
'空间分配/使用量较大段分析' rpt_finding_label,
'信息' rpt_finding_alarm_level,
'{2}' rpt_finding_text,
0 rpt_finding_level;
end;
'''.format(rpt_id, targetid, result)
            pg.execute(ismf)

        insql_mf = '''
begin;
delete from rpt_top_seg where rpt_id='{0}' and target_id='{3}';

insert into rpt_top_seg(rpt_id,rpt_owner,rpt_name,rpt_type,rpt_size,rpt_alloc,rpt_used,target_id)
select '{0}' rptid,owner,object_name,object_type,space_size,space_allocated,space_used,'{3}' target_id
  from ora_objstat
 where snap_time between '{1}' and '{2}'
   and dbid::varchar in (select subuid from mgt_system where uid='{3}');
end;
'''.format(rpt_id, begintime, endtime, targetid)
        pg.execute(insql_mf)

        # result += "7.2 可能存在空间不足的段分析"
        res82 = get82(pg, targetid, begintime, endtime)
        if (len(res82) > 0):
            # result += res82
            sqlf = """
begin;
delete from rpt_nospace_seg where rpt_id='{0}' and target_id='{2}';

insert into rpt_nospace_seg(rpt_id,rpt_owner,rpt_name,rpt_type,rpt_alloc_size,rpt_maxsize,rpt_size,target_id)
select '{0}' rptid,res.c1,res.c2,res.c3,res.c4,res.c5,res.c6,'{2}' target_id
from ({1}) res;
end;""".format(rpt_id, res82, targetid)
            pg.execute(sqlf)

        # result += "7.3 索引碎片分析"
        res83 = get83(pg, targetid, begintime, endtime)
        if (len(res83) > 0):
            # result += res83
            sqlf = """
begin;
delete from rpt_index_frag where rpt_id='{0}' and target_id='{2}';

insert into rpt_index_frag(rpt_id,target_id,rpt_owner,rpt_index,rpt_table,rpt_index_size,rpt_table_size,rpt_ratio)
select '{0}' rptid,'{2}' target_id,res.c1,res.c2,res.c3,res.c4,res.c5,res.c6
from ({1}) res;
end;""".format(rpt_id, res83, targetid)
            pg.execute(sqlf)

        # result += "7.4 非临时表空间中临时段分析"
        res84 = get84(pg, targetid, begintime, endtime)
        if (len(res84) > 0):
            # result += res84
            sqlf = """
begin;
delete from rpt_stat_item where rpt_id='{0}' and rpt_item like '非临时表空间中临时段数量%' and target_id='{2}';

insert into rpt_stat_item(rpt_id,rpt_item,rpt_value,target_id)
select '{0}' rptid,res.c1,res.c2,'{2}' target_id
from ({1}) res;
end;""".format(rpt_id, res84, targetid)
            pg.execute(sqlf)

        # result += "7.5 创建在系统表空间中的非系统用户段分析"
        res85 = get85(pg, targetid, begintime, endtime)
        if (len(res85) > 0):
            # result += res85
            sqlf = """
begin;
delete from rpt_system_seg where rpt_id='{0}' and target_id='{2}';

insert into rpt_system_seg(rpt_id,rpt_owner,rpt_name,rpt_type,rpt_size,rpt_table,target_id)
select '{0}' rptid,res.c1,res.c2,res.c3,res.c4,res.c5,'{2}' target_id
from ({1}) res;
end;""".format(rpt_id, res85, targetid)
            pg.execute(sqlf)

        res86 = get86(pg, targetid, begintime, endtime)
        if (len(res86) > 0):
            sqlf = """
begin;
delete from rpt_nonpart_table where rpt_id='{0}' and target_id='{2}';

insert into rpt_nonpart_table(rpt_id,target_id,rpt_owner,rpt_tab_name,rpt_tbssize,rpt_tbsname,rpt_note)
select '{0}' rptid,'{2}' target_id,res.c1,res.c2,res.c3,res.c4,''
from ({1}) res;
end;""".format(rpt_id, res86, targetid)
            pg.execute(sqlf)

    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

    except oracle.DatabaseError as e:
        if not ora is None:
            ora.close()

    # except Exception as e:
    #    errorInfo = str(e)
    #    print("异常：" + errorInfo)

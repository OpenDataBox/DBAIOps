#!/usr/bin/env python3
# -*- encoding:utf-8 -*-
import sys

sys.path.append('/usr/software/knowl')
import PGUtil
import CommUtil
import ResultCode
import re
import DBUtil
import psycopg2
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def getValue(db, sql):
    result = db.execute(sql)
    if (result.code != 0):
        msg = result.msg
        print("msg=WORD_BEGIN" + msg + "WORD_END")
        sys.exit()
    return result.msg


def getlogresult(pg, targetid, seqno):
    oraresult = ""
    pattern = '(错误原因[\u4E00-\u9FA5\W\S\s\w]*)解决方法'
    sqllogresult = "select result from log_result where target_id='%s' and seq_no='%s'" % (targetid, seqno)
    sqllogresultcursor = getValue(pg, sqllogresult)
    sqllogresultresult = sqllogresultcursor.fetchall()
    # print(sqllogresultresult)
    if sqllogresultresult:
        for row in sqllogresultresult:
            oraresult = ''.join(re.findall(pattern, row[0])).strip()
            if oraresult == '':
                oraresult = ' '
    else:
        oraresult = ' '

    return oraresult


def getora600list(pg, targetid, begin_time, end_time):
    ana = ""
    head = ['错误', '错误次数', '错误说明']
    des = "ORA-07445错误列表"
    sqlora7445 = '''select substr(log_signature,1,position(',' in log_signature)-1),count(*),min(seq_no) from 
log_detail where begin_time between '{0}' and '{1}'  and target_id='{2}'
and upper(log_code) in ('ORA-07445','ORA-7445') group by substr(log_signature,1,position(',' in log_signature)-1) 
order by 2 desc'''.format(begin_time, end_time, targetid)

    sqlora7445cursor = getValue(pg, sqlora7445)
    sqlora7445result = sqlora7445cursor.fetchall()
    # print(sqlora7445result)

    for resulttolist in sqlora7445result:
        sqlora7445result[sqlora7445result.index(resulttolist)] = list(resulttolist)

    for row in sqlora7445result:
        row[2] = getlogresult(pg, targetid, row[2])

    sqlresult = CommUtil.createTable(head, sqlora7445result, des)

    return sqlresult


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

        ora7445result = getora600list(pg, targetid, begintime, endtime)
        if ora7445result:
            # print("msg=" + ora7445result)
            sql6r = '''
begin;
delete from rpt_log_detail where rpt_id='{3}' and target_id='{2}' and rpt_log_code='ORA-07445';
insert into rpt_log_detail(rpt_id,target_id,rpt_log_code,rpt_log_signature,rpt_times,rpt_error_note)
with a as (
select substr(log_signature,1,position(',' in log_signature)-1) log_signature,
           count(*) cnt,min(seq_no) seq_no 
  from log_detail 
 where begin_time between '{0}' and '{1}'
   and target_id='{2}'
   and upper(log_code) in ('ORA-07445','ORA-7445') 
 group by substr(log_signature,1,position(',' in log_signature)-1) 
)
select '{3}' rptid,'{2}' target_id,'ORA-07445' log_code,a.log_signature,a.cnt,
       left(split_part(split_part(b.result,'SCREEN_BEGIN',2),'SCREEN_END',1),4000) note
  from a
left join log_result b
on a.seq_no=b.seq_no
and b.target_id='{2}';
end;
'''.format(begintime, endtime, targetid, rpt_id)
            pg.execute(sql6r)

    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

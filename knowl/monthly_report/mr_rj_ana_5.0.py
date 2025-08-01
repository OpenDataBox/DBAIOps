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


def register(file_name):
    ltag = ['5.0', 'RJ']
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


def getcheck1(conn, target_id, bt, et):
    sql = '''
  with res as (
select b.item_desc,b.item_result,b.error_msg,a.handle_time
  from dc_job_log a,dc_job_log_detail b
 where a.target_id='%s'
   and a.handle_time between '%s' and '%s'
   and a.id= b.dc_log_id 
   and b.item_result <> '正常' 
)
select res.item_desc,res.item_result,res.error_msg,res.handle_time,
       to_char(res.handle_time,'dd')::int handle_day
  from res 
  where item_desc ='表空间使用率检查'
 order by res.handle_time
''' % (target_id, bt, et)

    sql1 = '''
   with res as (
 select b.item_desc,b.item_result,b.error_msg,a.handle_time
   from dc_job_log a,dc_job_log_detail b
  where a.target_id='%s'
    and a.handle_time between '%s' and '%s'
    and a.id= b.dc_log_id 
    and b.item_result <> '正常' 
 )
 select min(to_char(res.handle_time,'dd')::int) handle_day
   from res 
   where item_desc ='表空间使用率检查'
 ''' % (target_id, bt, et)

    cursor = getValue(conn, sql)
    results = cursor.fetchall()

    tbslist = []

    if (len(results) > 0):
        for x in results:
            aa = getcheck1sp(x[2])
            if (len(aa) > 0):
                for xx in aa:
                    tbslist.append(xx)

    tbslist = list(set(tbslist))

    cursor1 = getValue(conn, sql1)
    results1 = cursor1.fetchone()
    for xy in results1:
        if xy is not None:
            rdt = results1[0]
        else:
            rdt = "0"

    totalcount = 1

    resld = []

    ljjs = 1
    rqday = int(rdt)
    rqday1 = int(rdt)
    lrpdt = ""
    res = ""

    for y in tbslist:
        templj = 0
        tempdt = ""
        if (len(results) > 0):
            for yy in results:

                if (y in yy[2]) and (yy[4] != rqday1):
                    totalcount += 1
                    rqday1 = yy[4]

                if (y in yy[2]):
                    tempdt = yy[3].strftime("%Y-%m-%d %H:%M:%S")

                if (abs(yy[4] - rqday)) == 1:
                    ljjs += 1
                    templj = ljjs
                    # lrpdt = yy[3]
                    # tempdt = lrpdt.strftime("%Y-%m-%d %H:%M:%S")
                    rqday = yy[4]
                elif (abs(yy[4] - rqday)) == 0:
                    ljjs += 0
                    templj = ljjs
                    # lrpdt = yy[3]
                    # tempdt = lrpdt.strftime("%Y-%m-%d %H:%M:%S")
                    rqday = yy[4]
                else:
                    ljjs = 0
                    # lrpdt = ""

            if templj > ljjs:
                ljjs = templj
            # if tempdt > lrpdt:
            #    lrpdt = tempdt
            lrpdt = tempdt

            res += "表空间使用率检查" + y + "出现次数:" + str(totalcount) + ";连续次数:" + str(ljjs) + "出现时间:" + lrpdt
            resld.append(
                dict(checkitem='表空间使用率检查', qushz='表空间' + y + '使用率超90%', cxcnt=totalcount, ljcxcnt=ljjs, rptdt=lrpdt))
        else:
            resld = []

    return resld


def getcheck1sp(cont):
    res = []
    # cont = "以下表空间使用率超过90%: SYSAUX(92.83%), "
    cont = cont.strip()
    if cont.endswith(","):
        cont = cont[:len(cont) - 1]
    else:
        cont = cont
    a = cont.find(":")
    b = cont[a + 2:]
    c = b.split(",")
    for x in c:
        d = x[0:x.find("(")]
        res.append(d.strip())
    return res


def getcheck3(conn, target_id, bt, et):
    sql = '''
  with res as (
select b.item_desc,b.item_result,b.error_msg,a.handle_time
  from dc_job_log a,dc_job_log_detail b
 where a.target_id='%s'
   and a.handle_time between '%s' and '%s'
   and a.id= b.dc_log_id 
   and b.item_result <> '正常' 
)
select res.item_desc,res.item_result,res.error_msg,res.handle_time,
       to_char(res.handle_time,'dd')::int handle_day
  from res 
  where item_desc ='归档目录空间使用率检查'
 order by res.handle_time
''' % (target_id, bt, et)

    sql1 = '''
   with res as (
 select b.item_desc,b.item_result,b.error_msg,a.handle_time
   from dc_job_log a,dc_job_log_detail b
  where a.target_id='%s'
    and a.handle_time between '%s' and '%s'
    and a.id= b.dc_log_id 
    and b.item_result <> '正常' 
 )
 select min(to_char(res.handle_time,'dd')::int) handle_day
   from res 
   where item_desc ='归档目录空间使用率检查'
 ''' % (target_id, bt, et)

    cursor = getValue(conn, sql)
    results = cursor.fetchall()

    tbslist = []

    if (len(results) > 0):
        for x in results:
            aa = getcheck3sp(x[2])
            if (len(aa) > 0):
                for xx in aa:
                    tbslist.append(xx)

    tbslist = list(set(tbslist))

    cursor1 = getValue(conn, sql1)
    results1 = cursor1.fetchone()
    for xy in results1:
        if xy is not None:
            rdt = results1[0]
        else:
            rdt = "0"

    totalcount = 1

    resld = []

    ljjs = 1
    rqday = int(rdt)
    rqday1 = int(rdt)
    lrpdt = ""
    res = ""

    for y in tbslist:
        templj = 0
        tempdt = ""
        if (len(results) > 0):
            for yy in results:

                if (y in yy[2]) and (yy[4] != rqday1):
                    totalcount += 1
                    rqday1 = yy[4]

                if (y in yy[2]):
                    tempdt = yy[3].strftime("%Y-%m-%d %H:%M:%S")

                if (abs(yy[4] - rqday)) == 1:
                    ljjs += 1
                    templj = ljjs
                    # lrpdt = yy[3]
                    # tempdt = lrpdt.strftime("%Y-%m-%d %H:%M:%S")
                    rqday = yy[4]
                elif (abs(yy[4] - rqday)) == 0:
                    ljjs += 0
                    templj = ljjs
                    # lrpdt = yy[3]
                    # tempdt = lrpdt.strftime("%Y-%m-%d %H:%M:%S")
                    rqday = yy[4]
                else:
                    ljjs = 0
                    # lrpdt = ""

            if templj > ljjs:
                ljjs = templj
            # if tempdt > lrpdt:
            #    lrpdt = tempdt
            lrpdt = tempdt

            res += "归档目录空间使用率检查" + y + "出现次数:" + str(totalcount) + ";连续次数:" + str(ljjs) + "出现时间:" + lrpdt
            resld.append(dict(checkitem='归档目录空间使用率检查', qushz='归档目录' + y + '使用率超90%', cxcnt=totalcount, ljcxcnt=ljjs,
                              rptdt=lrpdt))
        else:
            resld = []

    return resld


def getcheck3sp(cont):
    res = []
    # cont = "快速恢复区[%s]使用率[%.2f%%]超过90%% "
    # cont = "归档磁盘组[%s]使用率[%.2f%%]超过90%% "
    cont = cont.strip()
    a = cont[0:cont.find("使用率")]
    res.append(a)
    return res


def getcheck4(conn, target_id, bt, et):
    sql = '''
  with res as (
select b.item_desc,b.item_result,b.error_msg,a.handle_time
  from dc_job_log a,dc_job_log_detail b
 where a.target_id='%s'
   and a.handle_time between '%s' and '%s'
   and a.id= b.dc_log_id 
   and b.item_result <> '正常' 
)
select res.item_desc,res.item_result,res.error_msg,res.handle_time,
       to_char(res.handle_time,'dd')::int handle_day
  from res 
  where item_desc ='密码到期情况检查'
 order by res.handle_time
''' % (target_id, bt, et)

    sql1 = '''
   with res as (
 select b.item_desc,b.item_result,b.error_msg,a.handle_time
   from dc_job_log a,dc_job_log_detail b
  where a.target_id='%s'
    and a.handle_time between '%s' and '%s'
    and a.id= b.dc_log_id 
    and b.item_result <> '正常' 
 )
 select min(to_char(res.handle_time,'dd')::int) handle_day
   from res 
   where item_desc ='密码到期情况检查'
 ''' % (target_id, bt, et)

    cursor = getValue(conn, sql)
    results = cursor.fetchall()

    tbslist = []

    if (len(results) > 0):
        for x in results:
            aa = getcheck1sp(x[2])
            if (len(aa) > 0):
                for xx in aa:
                    tbslist.append(xx)

    tbslist = list(set(tbslist))

    cursor1 = getValue(conn, sql1)
    results1 = cursor1.fetchone()
    for xy in results1:
        if xy is not None:
            rdt = results1[0]
        else:
            rdt = "0"

    totalcount = 1

    resld = []

    ljjs = 1
    rqday = int(rdt)
    rqday1 = int(rdt)
    lrpdt = ""
    res = ""

    for y in tbslist:
        templj = 0
        tempdt = ""
        if (len(results) > 0):
            for yy in results:

                if (y in yy[2]) and (yy[4] != rqday1):
                    totalcount += 1
                    rqday1 = yy[4]

                if (y in yy[2]):
                    tempdt = yy[3].strftime("%Y-%m-%d %H:%M:%S")

                if (abs(yy[4] - rqday)) == 1:
                    ljjs += 1
                    templj = ljjs
                    # lrpdt = yy[3]
                    # tempdt = lrpdt.strftime("%Y-%m-%d %H:%M:%S")
                    rqday = yy[4]
                elif (abs(yy[4] - rqday)) == 0:
                    ljjs += 0
                    templj = ljjs
                    # lrpdt = yy[3]
                    # tempdt = lrpdt.strftime("%Y-%m-%d %H:%M:%S")
                    rqday = yy[4]
                else:
                    ljjs = 0
                    # lrpdt = ""

            if templj > ljjs:
                ljjs = templj
            # if tempdt > lrpdt:
            #    lrpdt = tempdt
            lrpdt = tempdt

            res += "密码到期情况检查" + y + "出现次数:" + str(totalcount) + ";连续次数:" + str(ljjs) + "出现时间:" + lrpdt
            resld.append(
                dict(checkitem='密码到期情况检查', qushz='以下用户口令已经或者快要到期:' + y, cxcnt=totalcount, ljcxcnt=ljjs, rptdt=lrpdt))
        else:
            resld = []

    return resld


def getcheck6(conn, target_id, bt, et):
    sql = '''
  with res as (
select b.item_desc,b.item_result,b.error_msg,a.handle_time
  from dc_job_log a,dc_job_log_detail b
 where a.target_id='%s'
   and a.handle_time between '%s' and '%s'
   and a.id= b.dc_log_id 
   and b.item_result <> '正常' 
)
select res.item_desc,res.item_result,res.error_msg,res.handle_time,
       to_char(res.handle_time,'dd')::int handle_day
  from res 
  where item_desc ='SCN Headroom检查'
 order by res.handle_time
''' % (target_id, bt, et)

    sql1 = '''
   with res as (
 select b.item_desc,b.item_result,b.error_msg,a.handle_time
   from dc_job_log a,dc_job_log_detail b
  where a.target_id='%s'
    and a.handle_time between '%s' and '%s'
    and a.id= b.dc_log_id 
    and b.item_result <> '正常' 
 )
 select min(to_char(res.handle_time,'dd')::int) handle_day
   from res 
   where item_desc ='SCN Headroom检查'
 ''' % (target_id, bt, et)

    cursor = getValue(conn, sql)
    results = cursor.fetchall()

    tbslist = ["小于10天", "小于62天"]

    cursor1 = getValue(conn, sql1)
    results1 = cursor1.fetchone()
    for xy in results1:
        if xy is not None:
            rdt = results1[0]
        else:
            rdt = "0"

    totalcount = 1

    resld = []

    ljjs = 1
    rqday = int(rdt)
    rqday1 = int(rdt)
    lrpdt = ""
    res = ""

    for y in tbslist:
        templj = 0
        tempdt = ""
        if (len(results) > 0):
            for yy in results:

                if (y in yy[2]) and (yy[4] != rqday1):
                    totalcount += 1
                    rqday1 = yy[4]

                if (y in yy[2]):
                    tempdt = yy[3].strftime("%Y-%m-%d %H:%M:%S")

                if (abs(yy[4] - rqday)) == 1:
                    ljjs += 1
                    templj = ljjs
                    # lrpdt = yy[3]
                    # tempdt = lrpdt.strftime("%Y-%m-%d %H:%M:%S")
                    rqday = yy[4]
                elif (abs(yy[4] - rqday)) == 0:
                    ljjs += 0
                    templj = ljjs
                    # lrpdt = yy[3]
                    # tempdt = lrpdt.strftime("%Y-%m-%d %H:%M:%S")
                    rqday = yy[4]
                else:
                    ljjs = 0
                    # lrpdt = ""

            if templj > ljjs:
                ljjs = templj
            # if tempdt > lrpdt:
            #    lrpdt = tempdt
            lrpdt = tempdt

            res += "SCN Headroom检查" + y + "出现次数:" + str(totalcount) + ";连续次数:" + str(ljjs) + "出现时间:" + lrpdt
            resld.append(
                dict(checkitem='SCN Headroom检查', qushz='SCN Headroom' + y, cxcnt=totalcount, ljcxcnt=ljjs, rptdt=lrpdt))
        else:
            resld = []

    return resld


def getcheck7(conn, target_id, bt, et):
    sql = '''
  with res as (
select b.item_desc,b.item_result,b.error_msg,a.handle_time
  from dc_job_log a,dc_job_log_detail b
 where a.target_id='%s'
   and a.handle_time between '%s' and '%s'
   and a.id= b.dc_log_id 
   and b.item_result <> '正常' 
)
select res.item_desc,res.item_result,res.error_msg,res.handle_time,
       to_char(res.handle_time,'dd')::int handle_day
  from res 
  where item_desc ='数据库文件个数检查'
 order by res.handle_time
''' % (target_id, bt, et)

    sql1 = '''
   with res as (
 select b.item_desc,b.item_result,b.error_msg,a.handle_time
   from dc_job_log a,dc_job_log_detail b
  where a.target_id='%s'
    and a.handle_time between '%s' and '%s'
    and a.id= b.dc_log_id 
    and b.item_result <> '正常' 
 )
 select min(to_char(res.handle_time,'dd')::int) handle_day
   from res 
   where item_desc ='数据库文件个数检查'
 ''' % (target_id, bt, et)

    cursor = getValue(conn, sql)
    results = cursor.fetchall()

    tbslist = ["参数设置太小"]

    cursor1 = getValue(conn, sql1)
    results1 = cursor1.fetchone()
    for xy in results1:
        if xy is not None:
            rdt = results1[0]
        else:
            rdt = "0"

    totalcount = 1

    resld = []

    ljjs = 1
    rqday = int(rdt)
    rqday1 = int(rdt)
    lrpdt = ""
    res = ""

    for y in tbslist:
        templj = 0
        tempdt = ""
        if (len(results) > 0):
            for yy in results:

                if (y in yy[2]) and (yy[4] != rqday1):
                    totalcount += 1
                    rqday1 = yy[4]

                if (y in yy[2]):
                    tempdt = yy[3].strftime("%Y-%m-%d %H:%M:%S")

                if (abs(yy[4] - rqday)) == 1:
                    ljjs += 1
                    templj = ljjs
                    # lrpdt = yy[3]
                    # tempdt = lrpdt.strftime("%Y-%m-%d %H:%M:%S")
                    rqday = yy[4]
                elif (abs(yy[4] - rqday)) == 0:
                    ljjs += 0
                    templj = ljjs
                    # lrpdt = yy[3]
                    # tempdt = lrpdt.strftime("%Y-%m-%d %H:%M:%S")
                    rqday = yy[4]
                else:
                    ljjs = 0
                    # lrpdt = ""

            if templj > ljjs:
                ljjs = templj
            # if tempdt > lrpdt:
            #    lrpdt = tempdt
            lrpdt = tempdt

            res += "数据库文件个数检查" + y + "出现次数:" + str(totalcount) + ";连续次数:" + str(ljjs) + "出现时间:" + lrpdt
            resld.append(dict(checkitem='数据库文件个数检查', qushz='db_files' + y, cxcnt=totalcount, ljcxcnt=ljjs, rptdt=lrpdt))
        else:
            resld = []

    return resld


def getcheck9(conn, target_id, bt, et):
    sql = '''
  with res as (
select b.item_desc,b.item_result,b.error_msg,a.handle_time
  from dc_job_log a,dc_job_log_detail b
 where a.target_id='%s'
   and a.handle_time between '%s' and '%s'
   and a.id= b.dc_log_id 
   and b.item_result <> '正常' 
)
select res.item_desc,res.item_result,res.error_msg,res.handle_time,
       to_char(res.handle_time,'dd')::int handle_day
  from res 
  where item_desc ='回收站空间使用检查'
 order by res.handle_time
''' % (target_id, bt, et)

    sql1 = '''
   with res as (
 select b.item_desc,b.item_result,b.error_msg,a.handle_time
   from dc_job_log a,dc_job_log_detail b
  where a.target_id='%s'
    and a.handle_time between '%s' and '%s'
    and a.id= b.dc_log_id 
    and b.item_result <> '正常' 
 )
 select min(to_char(res.handle_time,'dd')::int) handle_day
   from res 
   where item_desc ='回收站空间使用检查'
 ''' % (target_id, bt, et)

    cursor = getValue(conn, sql)
    results = cursor.fetchall()

    tbslist = ["超过10G"]

    cursor1 = getValue(conn, sql1)
    results1 = cursor1.fetchone()
    for xy in results1:
        if xy is not None:
            rdt = results1[0]
        else:
            rdt = "0"

    totalcount = 1

    resld = []

    ljjs = 1
    rqday = int(rdt)
    rqday1 = int(rdt)
    lrpdt = ""
    res = ""

    for y in tbslist:
        templj = 0
        tempdt = ""
        if (len(results) > 0):
            for yy in results:

                if (y in yy[2]) and (yy[4] != rqday1):
                    totalcount += 1
                    rqday1 = yy[4]

                if (y in yy[2]):
                    tempdt = yy[3].strftime("%Y-%m-%d %H:%M:%S")

                if (abs(yy[4] - rqday)) == 1:
                    ljjs += 1
                    templj = ljjs
                    # lrpdt = yy[3]
                    # tempdt = lrpdt.strftime("%Y-%m-%d %H:%M:%S")
                    rqday = yy[4]
                elif (abs(yy[4] - rqday)) == 0:
                    ljjs += 0
                    templj = ljjs
                    # lrpdt = yy[3]
                    # tempdt = lrpdt.strftime("%Y-%m-%d %H:%M:%S")
                    rqday = yy[4]
                else:
                    ljjs = 0
                    # lrpdt = ""

            if templj > ljjs:
                ljjs = templj
            # if tempdt > lrpdt:
            #    lrpdt = tempdt
            lrpdt = tempdt

            res += "回收站空间使用检查" + y + "出现次数:" + str(totalcount) + ";连续次数:" + str(ljjs) + "出现时间:" + lrpdt
            resld.append(dict(checkitem='回收站空间使用检查', qushz='回收站占用空间' + y, cxcnt=totalcount, ljcxcnt=ljjs, rptdt=lrpdt))
        else:
            resld = []

    return resld


def getcheck10(conn, target_id, bt, et):
    sql = '''
  with res as (
select b.item_desc,b.item_result,b.error_msg,a.handle_time
  from dc_job_log a,dc_job_log_detail b
 where a.target_id='%s'
   and a.handle_time between '%s' and '%s'
   and a.id= b.dc_log_id 
   and b.item_result <> '正常' 
)
select res.item_desc,res.item_result,res.error_msg,res.handle_time,
       to_char(res.handle_time,'dd')::int handle_day
  from res 
  where item_desc ='定时作业/任务运行情况检查'
 order by res.handle_time
''' % (target_id, bt, et)

    sql1 = '''
   with res as (
 select b.item_desc,b.item_result,b.error_msg,a.handle_time
   from dc_job_log a,dc_job_log_detail b
  where a.target_id='%s'
    and a.handle_time between '%s' and '%s'
    and a.id= b.dc_log_id 
    and b.item_result <> '正常' 
 )
 select min(to_char(res.handle_time,'dd')::int) handle_day
   from res 
   where item_desc ='定时作业/任务运行情况检查'
 ''' % (target_id, bt, et)

    cursor = getValue(conn, sql)
    results = cursor.fetchall()

    tbslist = ["在最近1天内失效了", "在最近1天内存在运行不成功记录"]

    cursor1 = getValue(conn, sql1)
    results1 = cursor1.fetchone()
    for xy in results1:
        if xy is not None:
            rdt = results1[0]
        else:
            rdt = "0"

    totalcount = 1

    resld = []

    ljjs = 1
    rqday = int(rdt)
    rqday1 = int(rdt)
    lrpdt = ""
    res = ""

    for y in tbslist:
        templj = 0
        tempdt = ""
        if (len(results) > 0):
            for yy in results:

                if (y in yy[2]) and (yy[4] != rqday1):
                    totalcount += 1
                    rqday1 = yy[4]

                if (y in yy[2]):
                    tempdt = yy[3].strftime("%Y-%m-%d %H:%M:%S")

                if (abs(yy[4] - rqday)) == 1:
                    ljjs += 1
                    templj = ljjs
                    # lrpdt = yy[3]
                    # tempdt = lrpdt.strftime("%Y-%m-%d %H:%M:%S")
                    rqday = yy[4]
                elif (abs(yy[4] - rqday)) == 0:
                    ljjs += 0
                    templj = ljjs
                    # lrpdt = yy[3]
                    # tempdt = lrpdt.strftime("%Y-%m-%d %H:%M:%S")
                    rqday = yy[4]
                else:
                    ljjs = 0
                    # lrpdt = ""

            if templj > ljjs:
                ljjs = templj
            # if tempdt > lrpdt:
            #    lrpdt = tempdt
            lrpdt = tempdt

            res += "定时作业/任务运行情况检查" + y + "出现次数:" + str(totalcount) + ";连续次数:" + str(ljjs) + "出现时间:" + lrpdt
            resld.append(dict(checkitem='定时作业/任务运行情况检查', qushz=y, cxcnt=totalcount, ljcxcnt=ljjs, rptdt=lrpdt))
        else:
            resld = []

    return resld


def getcheck11(conn, target_id, bt, et):
    sql = '''
  with res as (
select b.item_desc,b.item_result,b.error_msg,a.handle_time
  from dc_job_log a,dc_job_log_detail b
 where a.target_id='%s'
   and a.handle_time between '%s' and '%s'
   and a.id= b.dc_log_id 
   and b.item_result <> '正常' 
)
select res.item_desc,res.item_result,res.error_msg,res.handle_time,
       to_char(res.handle_time,'dd')::int handle_day
  from res 
  where item_desc ='失效对象检查'
 order by res.handle_time
''' % (target_id, bt, et)

    sql1 = '''
   with res as (
 select b.item_desc,b.item_result,b.error_msg,a.handle_time
   from dc_job_log a,dc_job_log_detail b
  where a.target_id='%s'
    and a.handle_time between '%s' and '%s'
    and a.id= b.dc_log_id 
    and b.item_result <> '正常' 
 )
 select min(to_char(res.handle_time,'dd')::int) handle_day
   from res 
   where item_desc ='失效对象检查'
 ''' % (target_id, bt, et)

    cursor = getValue(conn, sql)
    results = cursor.fetchall()

    tbslist = []

    if (len(results) > 0):
        for x in results:
            aa = getcheck11sp(x[2])
            if (len(aa) > 0):
                for xx in aa:
                    tbslist.append(xx)

    tbslist = list(set(tbslist))

    cursor1 = getValue(conn, sql1)
    results1 = cursor1.fetchone()
    for xy in results1:
        if xy is not None:
            rdt = results1[0]
        else:
            rdt = "0"

    totalcount = 1

    resld = []

    ljjs = 1
    rqday = int(rdt)
    rqday1 = int(rdt)
    lrpdt = ""
    res = ""

    for y in tbslist:
        templj = 0
        tempdt = ""
        if (len(results) > 0):
            for yy in results:

                if (y in yy[2]) and (yy[4] != rqday1):
                    totalcount += 1
                    rqday1 = yy[4]

                if (y in yy[2]):
                    tempdt = yy[3].strftime("%Y-%m-%d %H:%M:%S")

                if (abs(yy[4] - rqday)) == 1:
                    ljjs += 1
                    templj = ljjs
                    # lrpdt = yy[3]
                    # tempdt = lrpdt.strftime("%Y-%m-%d %H:%M:%S")
                    rqday = yy[4]
                elif (abs(yy[4] - rqday)) == 0:
                    ljjs += 0
                    templj = ljjs
                    # lrpdt = yy[3]
                    # tempdt = lrpdt.strftime("%Y-%m-%d %H:%M:%S")
                    rqday = yy[4]
                else:
                    ljjs = 0
                    # lrpdt = ""

            if templj > ljjs:
                ljjs = templj
            # if tempdt > lrpdt:
            #    lrpdt = tempdt
            lrpdt = tempdt

            res += "失效对象检查" + y + "出现次数:" + str(totalcount) + ";连续次数:" + str(ljjs) + "出现时间:" + lrpdt
            resld.append(dict(checkitem='失效对象检查', qushz=y, cxcnt=totalcount, ljcxcnt=ljjs, rptdt=lrpdt))
        else:
            resld = []

    return resld


def getcheck11sp(cont):
    res = []
    cont = cont.strip()
    if cont.endswith(","):
        cont = cont[:len(cont) - 1]
    else:
        cont = cont
    a = cont.find(":")
    b = cont[a + 2:]
    c = b.split(",")
    for x in c:
        d = x.split("-")
        e = d[0] + "-" + d[1]
        res.append(e.strip())
    return res


def getsp(cont):
    res = []
    # cont = "以下表空间使用率超过90%: SYSAUX(92.83%), "
    cont = cont.strip()
    if cont.endswith(","):
        cont = cont[:len(cont) - 1]
    else:
        cont = cont
    a = cont.find(":")
    b = cont[a + 2:]
    c = b.split(",")
    for x in c:
        d = x[0:x.find("(")]
        res.append(d)
    return res


def getitem5(cont):
    res = []
    # cont = "以下表空间使用率超过90%: SYSAUX(92.83%), "
    cont = cont.strip()
    if cont.endswith(","):
        cont = cont[:len(cont) - 1]
    else:
        cont = cont
    if cont.find('[') != -1:
        c = cont.split(",")
        for x in c:
            d = x[0:x.find("[")]
            res.append(d)
    return res


def getcheck12(conn, target_id, bt, et):
    sql = '''
  with res as (
select b.item_desc,b.item_result,b.error_msg,a.handle_time
  from dc_job_log a,dc_job_log_detail b
 where a.target_id='%s'
   and a.handle_time between '%s' and '%s'
   and a.id= b.dc_log_id 
   and b.item_result <> '正常' 
)
select res.item_desc,res.item_result,res.error_msg,res.handle_time,
       to_char(res.handle_time,'dd')::int handle_day
  from res 
  where item_desc ='非临时表空间中临时段占用空间检查'
 order by res.handle_time
''' % (target_id, bt, et)

    sql1 = '''
   with res as (
 select b.item_desc,b.item_result,b.error_msg,a.handle_time
   from dc_job_log a,dc_job_log_detail b
  where a.target_id='%s'
    and a.handle_time between '%s' and '%s'
    and a.id= b.dc_log_id 
    and b.item_result <> '正常' 
 )
 select min(to_char(res.handle_time,'dd')::int) handle_day
   from res 
   where item_desc ='非临时表空间中临时段占用空间检查'
 ''' % (target_id, bt, et)

    cursor = getValue(conn, sql)
    results = cursor.fetchall()

    tbslist = ["超过10G"]

    cursor1 = getValue(conn, sql1)
    results1 = cursor1.fetchone()
    for xy in results1:
        if xy is not None:
            rdt = results1[0]
        else:
            rdt = "0"

    totalcount = 1

    resld = []

    ljjs = 1
    rqday = int(rdt)
    rqday1 = int(rdt)
    lrpdt = ""
    res = ""

    for y in tbslist:
        templj = 0
        tempdt = ""
        if (len(results) > 0):
            for yy in results:

                if (y in yy[2]) and (yy[4] != rqday1):
                    totalcount += 1
                    rqday1 = yy[4]

                if (y in yy[2]):
                    tempdt = yy[3].strftime("%Y-%m-%d %H:%M:%S")

                if (abs(yy[4] - rqday)) == 1:
                    ljjs += 1
                    templj = ljjs
                    # lrpdt = yy[3]
                    # tempdt = lrpdt.strftime("%Y-%m-%d %H:%M:%S")
                    rqday = yy[4]
                elif (abs(yy[4] - rqday)) == 0:
                    ljjs += 0
                    templj = ljjs
                    # lrpdt = yy[3]
                    # tempdt = lrpdt.strftime("%Y-%m-%d %H:%M:%S")
                    rqday = yy[4]
                else:
                    ljjs = 0
                    # lrpdt = ""

            if templj > ljjs:
                ljjs = templj
            # if tempdt > lrpdt:
            #    lrpdt = tempdt
            lrpdt = tempdt

            res += "非临时表空间中临时段占用空间检查" + y + "出现次数:" + str(totalcount) + ";连续次数:" + str(ljjs) + "出现时间:" + lrpdt
            resld.append(dict(checkitem='非临时表空间中临时段占用空间检查', qushz=y, cxcnt=totalcount, ljcxcnt=ljjs, rptdt=lrpdt))
        else:
            resld = []

    return resld


def getcheck13(conn, target_id, bt, et):
    sql = '''
  with res as (
select b.item_desc,b.item_result,b.error_msg,a.handle_time
  from dc_job_log a,dc_job_log_detail b
 where a.target_id='%s'
   and a.handle_time between '%s' and '%s'
   and a.id= b.dc_log_id 
   and b.item_result <> '正常' 
)
select res.item_desc,res.item_result,res.error_msg,res.handle_time,
       to_char(res.handle_time,'dd')::int handle_day
  from res 
  where item_desc ='日志切换检查'
 order by res.handle_time
''' % (target_id, bt, et)

    sql1 = '''
   with res as (
 select b.item_desc,b.item_result,b.error_msg,a.handle_time
   from dc_job_log a,dc_job_log_detail b
  where a.target_id='%s'
    and a.handle_time between '%s' and '%s'
    and a.id= b.dc_log_id 
    and b.item_result <> '正常' 
 )
 select min(to_char(res.handle_time,'dd')::int) handle_day
   from res 
   where item_desc ='日志切换检查'
 ''' % (target_id, bt, et)

    cursor = getValue(conn, sql)
    results = cursor.fetchall()

    tbslist = ["日志大小不一致", "日志组数不一致", "日志组数太少", "日志文件太小", "手工切换太频繁"]

    cursor1 = getValue(conn, sql1)
    results1 = cursor1.fetchone()
    for xy in results1:
        if xy is not None:
            rdt = results1[0]
        else:
            rdt = "0"

    totalcount = 1

    resld = []

    ljjs = 1
    rqday = int(rdt)
    rqday1 = int(rdt)
    lrpdt = ""
    res = ""

    for y in tbslist:
        templj = 0
        tempdt = ""
        if (len(results) > 0):
            for yy in results:
                if (y in yy[2]):
                    if (y in yy[2]) and (yy[4] != rqday1):
                        totalcount += 1
                        rqday1 = yy[4]

                    if (y in yy[2]):
                        tempdt = yy[3].strftime("%Y-%m-%d %H:%M:%S")

                    if (abs(yy[4] - rqday)) == 1:
                        ljjs += 1
                        templj = ljjs
                        # lrpdt = yy[3]
                        # tempdt = lrpdt.strftime("%Y-%m-%d %H:%M:%S")
                        rqday = yy[4]
                    elif (abs(yy[4] - rqday)) == 0:
                        ljjs += 0
                        templj = ljjs
                        # lrpdt = yy[3]
                        # tempdt = lrpdt.strftime("%Y-%m-%d %H:%M:%S")
                        rqday = yy[4]
                    else:
                        ljjs = 0
                        # lrpdt = ""

                    if templj > ljjs:
                        ljjs = templj
                    # if tempdt > lrpdt:
                    #    lrpdt = tempdt
                    lrpdt = tempdt

                    res += "日志切换检查" + y + "出现次数:" + str(totalcount) + ";连续次数:" + str(ljjs) + "出现时间:" + lrpdt
                    resld.append(dict(checkitem='日志切换检查', qushz=y, cxcnt=totalcount, ljcxcnt=ljjs, rptdt=lrpdt))
        else:
            resld = []

    return resld


def getcheck14(conn, target_id, bt, et):
    sql = '''
  with res as (
select b.item_desc,b.item_result,b.error_msg,a.handle_time
  from dc_job_log a,dc_job_log_detail b
 where a.target_id='%s'
   and a.handle_time between '%s' and '%s'
   and a.id= b.dc_log_id 
   and b.item_result <> '正常' 
)
select res.item_desc,res.item_result,res.error_msg,res.handle_time,
       to_char(res.handle_time,'dd')::int handle_day
  from res 
  where item_desc ='数据库RMAN备份检查'
 order by res.handle_time
''' % (target_id, bt, et)

    sql1 = '''
   with res as (
 select b.item_desc,b.item_result,b.error_msg,a.handle_time
   from dc_job_log a,dc_job_log_detail b
  where a.target_id='%s'
    and a.handle_time between '%s' and '%s'
    and a.id= b.dc_log_id 
    and b.item_result <> '正常' 
 )
 select min(to_char(res.handle_time,'dd')::int) handle_day
   from res 
   where item_desc ='数据库RMAN备份检查'
 ''' % (target_id, bt, et)

    cursor = getValue(conn, sql)
    results = cursor.fetchall()

    tbslist = ["存在失败备份", "备份持续到正常工作时间", "备份耗时过长"]

    cursor1 = getValue(conn, sql1)
    results1 = cursor1.fetchone()
    for xy in results1:
        if xy is not None:
            rdt = results1[0]
        else:
            rdt = "0"

    totalcount = 1

    resld = []

    ljjs = 1
    rqday = int(rdt)
    rqday1 = int(rdt)
    lrpdt = ""
    res = ""

    for y in tbslist:
        templj = 0
        tempdt = ""
        if (len(results) > 0):
            for yy in results:

                if (y in yy[2]) and (yy[4] != rqday1):
                    totalcount += 1
                    rqday1 = yy[4]

                if (y in yy[2]):
                    tempdt = yy[3].strftime("%Y-%m-%d %H:%M:%S")

                if (abs(yy[4] - rqday)) == 1:
                    ljjs += 1
                    templj = ljjs
                    # lrpdt = yy[3]
                    # tempdt = lrpdt.strftime("%Y-%m-%d %H:%M:%S")
                    rqday = yy[4]
                elif (abs(yy[4] - rqday)) == 0:
                    ljjs += 0
                    templj = ljjs
                    # lrpdt = yy[3]
                    # tempdt = lrpdt.strftime("%Y-%m-%d %H:%M:%S")
                    rqday = yy[4]
                else:
                    ljjs = 0
                    # lrpdt = ""

            if templj > ljjs:
                ljjs = templj
            # if tempdt > lrpdt:
            #    lrpdt = tempdt
            lrpdt = tempdt

            res += "数据库RMAN备份检查" + y + "出现次数:" + str(totalcount) + ";连续次数:" + str(ljjs) + "出现时间:" + lrpdt
            resld.append(dict(checkitem='数据库RMAN备份检查', qushz=y, cxcnt=totalcount, ljcxcnt=ljjs, rptdt=lrpdt))
        else:
            resld = []

    return resld


def getcheck15(conn, target_id, bt, et):
    sql = '''
  with res as (
select b.item_desc,b.item_result,b.error_msg,a.handle_time
  from dc_job_log a,dc_job_log_detail b
 where a.target_id='%s'
   and a.handle_time between '%s' and '%s'
   and a.id= b.dc_log_id 
   and b.item_result <> '正常' 
)
select res.item_desc,res.item_result,res.error_msg,res.handle_time,
       to_char(res.handle_time,'dd')::int handle_day
  from res 
  where item_desc ='SGA RESIZE操作检查'
 order by res.handle_time
''' % (target_id, bt, et)

    sql1 = '''
   with res as (
 select b.item_desc,b.item_result,b.error_msg,a.handle_time
   from dc_job_log a,dc_job_log_detail b
  where a.target_id='%s'
    and a.handle_time between '%s' and '%s'
    and a.id= b.dc_log_id 
    and b.item_result <> '正常' 
 )
 select min(to_char(res.handle_time,'dd')::int) handle_day
   from res 
   where item_desc ='SGA RESIZE操作检查'
 ''' % (target_id, bt, et)

    cursor = getValue(conn, sql)
    results = cursor.fetchall()

    tbslist = ["存在失败RESIZE", "RESIZE时间过长"]

    cursor1 = getValue(conn, sql1)
    results1 = cursor1.fetchone()
    for xy in results1:
        if xy is not None:
            rdt = results1[0]
        else:
            rdt = "0"

    totalcount = 1

    resld = []

    ljjs = 1
    rqday = int(rdt)
    rqday1 = int(rdt)
    lrpdt = ""
    res = ""

    for y in tbslist:
        templj = 0
        tempdt = ""
        if (len(results) > 0):
            for yy in results:

                if (y in yy[2]) and (yy[4] != rqday1):
                    totalcount += 1
                    rqday1 = yy[4]

                if (y in yy[2]):
                    tempdt = yy[3].strftime("%Y-%m-%d %H:%M:%S")

                if (abs(yy[4] - rqday)) == 1:
                    ljjs += 1
                    templj = ljjs
                    # lrpdt = yy[3]
                    # tempdt = lrpdt.strftime("%Y-%m-%d %H:%M:%S")
                    rqday = yy[4]
                elif (abs(yy[4] - rqday)) == 0:
                    ljjs += 0
                    templj = ljjs
                    # lrpdt = yy[3]
                    # tempdt = lrpdt.strftime("%Y-%m-%d %H:%M:%S")
                    rqday = yy[4]
                else:
                    ljjs = 0
                    # lrpdt = ""

            if templj > ljjs:
                ljjs = templj
            # if tempdt > lrpdt:
            #    lrpdt = tempdt
            lrpdt = tempdt

            res += "SGA RESIZE操作检查" + y + "出现次数:" + str(totalcount) + ";连续次数:" + str(ljjs) + "出现时间:" + lrpdt
            resld.append(dict(checkitem='SGA RESIZE操作检查', qushz=y, cxcnt=totalcount, ljcxcnt=ljjs, rptdt=lrpdt))
        else:
            resld = []

    return resld


def getcheck2(pg, targetid, begin_time, end_time):
    itemcnt = {}
    itemmaxcnt = {}
    itemlasttime = {}
    checklist = []
    checkdict = {}
    maxcnt = 0
    cnt = 0
    incnt = 0
    record_time = None
    sqlitem2 = '''
select d.item_desc ,d.error_msg,l.handle_time from dc_job_log l,dc_job_log_detail d where d.dc_log_id=l.id
and l.target_id='{0}' and item_seq=2 and l.handle_time between '{1}' and '{2}' order by handle_time
'''.format(targetid, begin_time, end_time)
    sqlitem2cursor = getValue(pg, sqlitem2)
    sqlitem2result = sqlitem2cursor.fetchall()
    for row in sqlitem2result:
        aa = getsp(row[1])
        for x in aa:
            if x:
                if not x in itemcnt:
                    itemcnt[x] = 1
                else:
                    itemcnt[x] = itemcnt[x] + 1

    asmgrouplist = itemcnt.keys()

    for group in asmgrouplist:
        for row in sqlitem2result:
            if group in row[1]:
                record_time = row[2]
                incnt = incnt + 1
                cnt = incnt
            else:
                incnt = 0
                if cnt > maxcnt:
                    maxcnt = cnt
            if cnt > maxcnt:
                maxcnt = cnt
        itemmaxcnt[group] = maxcnt
        if record_time:
            itemlasttime[group] = record_time

    if itemcnt:
        for key in itemcnt.keys():
            checkdict = dict(checkitem='ASM磁盘组空间使用率检查', qushz='磁盘组' + key + '空间使用率超90%', cxcnt=itemcnt[key],
                             ljcxcnt=itemmaxcnt[key], rptdt=itemlasttime[key].strftime("%Y-%m-%d %H:%M:%S"))
            checklist.append(checkdict)

    return checklist


def getcheck5(pg, targetid, begin_time, end_time):
    itemcnt = {}
    itemmaxcnt = {}
    itemlasttime = {}
    itemlist = []
    checklist = []
    checkdict = {}
    record_time = None
    maxcnt = 0
    cnt = 0
    incnt = 0
    sqlitem5 = '''
    select d.item_desc ,d.error_msg,l.handle_time from dc_job_log l,dc_job_log_detail d where d.dc_log_id=l.id
    and l.target_id='{0}' and item_seq=5 and l.handle_time between '{1}' and '{2}' order by handle_time
    '''.format(targetid, begin_time, end_time)
    sqlitem5cursor = getValue(pg, sqlitem5)
    sqlitem5result = sqlitem5cursor.fetchall()

    for row in sqlitem5result:
        aa = getitem5(row[1])
        for x in aa:
            if x:
                if not x in itemcnt:
                    itemcnt[x] = 1
                else:
                    itemcnt[x] = itemcnt[x] + 1
    for item in itemcnt.keys():
        for row in sqlitem5result:
            if item in row[1]:
                record_time = row[2]
                incnt = incnt + 1
                cnt = incnt
            else:
                incnt = 0
                if cnt > maxcnt:
                    maxcnt = cnt
            if cnt > maxcnt:
                maxcnt = cnt
        itemmaxcnt[item] = maxcnt
        if record_time:
            itemlasttime[item] = record_time

    if itemcnt:
        for key in itemcnt.keys():
            checkdict = dict(checkitem='SYSAUX表空间主要使用对象大小检查', qushz=key + '超过10G', cxcnt=itemcnt[key],
                             ljcxcnt=itemmaxcnt[key], rptdt=itemlasttime[key].strftime("%Y-%m-%d %H:%M:%S"))
            checklist.append(checkdict)

    return checklist


def getcheck8(pg, targetid, begin_time, end_time):
    itemcnt = {}
    itemmaxcnt = {}
    itemlasttime = {}
    itemlist = []
    checklist = []
    checkdict = {}
    maxcnt = 0
    cnt = 0
    incnt = 0
    record_time = None
    sqlitem8 = '''
    select d.item_desc ,d.error_msg,l.handle_time from dc_job_log l,dc_job_log_detail d where d.dc_log_id=l.id
    and l.target_id='{0}' and item_seq=8 and l.handle_time between '{1}' and '{2}' order by handle_time
    '''.format(targetid, begin_time, end_time)
    sqlitem8cursor = getValue(pg, sqlitem8)
    sqlitem8result = sqlitem8cursor.fetchall()
    itemcnt = {'AWR保存的最早快照时间已超过设置的最大天数': 0, '最后一次生成AWR快照的时间距现在已超过': 0}
    for row in sqlitem8result:
        for item in itemcnt.keys():
            if item in row[1]:
                itemcnt[item] = itemcnt[item] + 1

    for item in itemcnt.keys():
        for row in sqlitem8result:
            if item in row[1]:
                record_time = row[2]
                incnt = incnt + 1
                cnt = incnt
            else:
                incnt = 0
                if cnt > maxcnt:
                    maxcnt = cnt
            if cnt > maxcnt:
                maxcnt = cnt
        itemmaxcnt[item] = maxcnt
        if record_time:
            itemlasttime[item] = record_time
    if itemlasttime:
        for key in itemcnt.keys():
            if itemcnt[key] > 0:
                if key == "最后一次生成AWR快照的时间距现在已超过":
                    itemname = "最后一次生成AWR快照的时间距现在已超过设置的最大小时数"
                    checkdict = dict(checkitem='AWR快照时间范围检查', qushz=itemname, cxcnt=itemcnt[key],
                                     ljcxcnt=itemmaxcnt[key], rptdt=itemlasttime[key].strftime("%Y-%m-%d %H:%M:%S"))
                    checklist.append(checkdict)
                else:
                    checkdict = dict(checkitem='AWR快照时间范围检查', qushz=key, cxcnt=itemcnt[key], ljcxcnt=itemmaxcnt[key],
                                     rptdt=itemlasttime[key].strftime("%Y-%m-%d %H:%M:%S"))
                    checklist.append(checkdict)
    return checklist


def getfinalsql(reslist):
    sql = ""
    for res in reslist:
        sql += "select '" + res.get('checkitem') + "' c1,'" + res.get('qushz') + "' c2," + str(
            res.get('cxcnt')) + " c3," + str(res.get('ljcxcnt')) + " c4,'" + res.get('rptdt') + "' c5 union all "
    sql = sql[0:-10]
    return sql


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
        # result = "SCREEN_BEGIN5 日检分析SCREEN_END"
        result = ""
        reslist = []
        p1 = ""
        res1 = getcheck1(pg, targetid, begintime, endtime)
        res2 = getcheck2(pg, targetid, begintime, endtime)
        res3 = getcheck3(pg, targetid, begintime, endtime)
        res4 = getcheck4(pg, targetid, begintime, endtime)
        res5 = getcheck5(pg, targetid, begintime, endtime)
        res6 = getcheck6(pg, targetid, begintime, endtime)
        res7 = getcheck7(pg, targetid, begintime, endtime)
        res8 = getcheck8(pg, targetid, begintime, endtime)
        res9 = getcheck9(pg, targetid, begintime, endtime)
        res10 = getcheck10(pg, targetid, begintime, endtime)
        res11 = getcheck11(pg, targetid, begintime, endtime)
        res12 = getcheck12(pg, targetid, begintime, endtime)
        res13 = getcheck13(pg, targetid, begintime, endtime)
        res14 = getcheck14(pg, targetid, begintime, endtime)
        res15 = getcheck15(pg, targetid, begintime, endtime)

        reslist = res1 + res2 + res3 + res4 + res5 + res6 + res7 + res8 + res9 + res10 + res11 + res12 + res13 + res14 + res15
        if (not reslist == []):
            sql = getfinalsql(reslist)
            sqlf = """
begin;
delete from rpt_day_check where rpt_id='{0}' and target_id='{1}';

insert into rpt_day_check(rpt_id,target_id,rpt_check_item,rpt_check_summary,rpt_times,rpt_repeats,rpt_final_time)
select '{0}' rptid,'{1}' target_id,
res.c1,res.c2,res.c3,res.c4,case when res.c5='' or res.c5 is null then null else res.c5::timestamp end
from ({2}) res;
end;""".format(rpt_id, targetid, sql)
            pg.execute(sqlf)

    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

    # except Exception as e:
    #    errorInfo = str(e)
    #    print("异常：" + errorInfo)

import sys
import time, datetime
from datetime import date, datetime, timedelta
import re
import traceback
import json
import psycopg2

sys.path.append('/usr/software/knowl')

import CommUtil
import DBUtil
import FormatUtil
import JavaUtil
import JavaRsa
from baseline import get_sql
ctime = None

class Result(object):
    # pass
    def __str__(self):
        return "\n".join("{}={}".format(k, getattr(self, k))
                        for k in self.__dict__.keys())

def relate_pg2(conn, sql, nrow=0):
    result = Result()
    try:
        cur = conn.conn.cursor()
        cur.execute(sql)
        msg = []
        if nrow == 0:
            rows = cur.fetchall()
            for row in rows:
                msg.append(row)
        else:
            for i in range(nrow):
                row = cur.fetchone()
                if row is None:
                    break
                msg.append(row)
        result.code = 0
        result.msg = msg
    except psycopg2.ProgrammingError:
        result.code = 2
        result.msg = "SQL Error"
    except psycopg2.OperationalError:
        result.code = 1
        result.msg = "Connect Error"
    return result

def tuple2(arr):
    s = ''
    for v in arr:
        if s:
            s += ",'%s'" % str(v)
        else:
            s = "'%s'" % str(v)
    if s:
        s = '(%s)' % s
    return s

def idx_nninfo(jmx, ns, hs, metric):
    try:
        mb = javax.management.ObjectName('Hadoop:service=NameNode,name=NameNodeInfo')
        alist = ['ClusterId',
'LiveNodes',
'DeadNodes',
'DecomNodes']
        vvv = jmx.getAttributes(mb, alist)
        for vv in vvv:
            if not vv:
                continue
            nm = str(vv.getName())
            if nm == 'LiveNodes':
                ln = json.loads(str(vv.getValue()))
                if ln:
                    for k in ln.keys():
                        n = ln[k]
                        #nodes.append([k.split(':')[0],cs(n.get('infoAddr')).split(':')[0],n.get('adminState'),n.get('capacity'),n.get('used'),n.get('nonDfsUsedSpace'),n.get('numBlocks'),n.get('blockPoolUsed'),n.get('volfails')])
                        ip = cs(n.get('infoAddr')).split(':')[0]
                        for n in ns:
                            if n[1] == ip and n[2] == '2':
                                n[4] = 1
                                hs.add(n[3])
                                break

    except javax.management.RuntimeOperationsException as e:
        bt = str(e)
        exc_type, exc_value, exc_tb = sys.exc_info()
        for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
            bt += "\n%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname)
        print(bt)
        print(exc_type)
        print(exc_value)

def initjvm():
    # print(getDefaultJVMPath())
    if not jpype.isJVMStarted():
        jpype.startJVM(jpype.getDefaultJVMPath(), "-ea",
                       "-Djava.class.path=/usr/software/knowl/wlfullclient.jar:/usr/software/knowl/RsaTool.jar",
                       convertStrings=False)

def connect(ip, port, type, user, password):
    URL = "service:jmx:rmi:///jndi/rmi://%s:%s/jmxrmi" % (ip, str(port))
    jhash = java.util.HashMap()
    # for obj in jhash.getClass().getMethods():
    jarray = jpype.JArray(java.lang.String)([user, password])
    jhash.put(javax.management.remote.JMXConnector.CREDENTIALS, jarray);
    jmxurl = javax.management.remote.JMXServiceURL(URL)
    jmxsoc = javax.management.remote.JMXConnectorFactory.connect(jmxurl, jhash)
    return jmxsoc


def get_baseline_limit(pg, target_id, idx):
    bsl = {}
    columns = 'index_id, upper_limit, lower_limit'
    tables = 'baseline_profile_detail b, mgt_system m'
    options = f""" b.profile_id = m.baseline_profile_id
     and m.uid='{target_id}' and b.index_id in ({idx}) and b.use_flag"""
    sql = get_sql(pg, target_id, columns, tables, options)
    result = relate_pg2(pg, sql)
    if result.code == 0:
        for row in result.msg:
            bsl[row[0]] = [row[1],row[2]]
    return bsl


def os_cluster(pg, hs, metric):
    mets = {}
    cnt = 0
    fail = 0
    bsl = get_baseline_limit(pg, list(hs)[0], '3000009,3000003,3000007,3001031,3000100,3000101,3000006,3000209') 
    for uid in hs:
        sql = '''select index_id,value,record_time from mon_indexdata where uid='%s' and index_id in (
3000000,3000009,3000003,3000007,3001031,3000100,3000101,3000006,3000209
)''' % uid
        result = relate_pg2(pg, sql)
        met = {}
        if result.code == 0:
            for row in result.msg:
                #ts = time.mktime(row[2].timetuple())
                if row[0] != 3000000:
                    met[row[0]] = [row[0],float(row[1]),row[2]]
                else:
                    met[row[0]] = [row[0],row[1],row[2]]
        if met.get(3000000) is None or time.mktime(met[3000000][2].timetuple()) < ctime - 600:
            continue
        if met[3000000][1] != '连接成功':
            fail += 1
            continue
        cnt += 1
        for m in met.values():
            if m[0] > 3000000 and time.mktime(m[2].timetuple()) > ctime - 600:
                if mets.get(m[0]) is not None:
                    mets[m[0]][0] += 1
                    mets[m[0]][1] += m[1]
                else:
                    mets[m[0]] = [1,m[1],0]
                if bsl.get(m[0]):
                    if bsl[m[0]][0] is not None:
                        if m[1] > bsl[m[0]][0]:
                            mets[m[0]][2] += 1
                    elif bsl[m[0]][1] is not None:
                        if m[1] < bsl[m[0]][1]:
                            mets[m[0]][2] += 1
                else:
                    mets[m[0]][2] = -1
    if cnt > 0:
        for k in mets.keys():
            metric.append(dict(index_id=str(5030000+(k%1000)),value=str(round(mets[k][1]/mets[k][0],2))))
            if mets[k][2] != -1:
                metric.append(dict(index_id=str(5031000+(k%1000)),value=str(round(mets[k][2]/mets[k][0],2))))
    metric.append(dict(index_id='5039994', value=str(cnt)))
    metric.append(dict(index_id='5039995', value=str(fail)))

def hdfs_name(pg, uid, metric):
    sql = '''select index_id,value,record_time from mon_indexdata where uid='%s' and index_id in (
5010000,5010314,5010017,5010226,5010227,5010023,5011129,5011152,5011131,5011130,5011132,5010348,5010349,5010350,5010351,5010352,5010353
)''' % uid
    result = relate_pg2(pg, sql)
    if result.code == 0:
        met = {}
        for row in result.msg:
            if row[0] != 5010000:
                met[row[0]] = [row[0],float(row[1]),row[2]]
            else:
                met[row[0]] = [row[0],row[1],row[2]]
        if met.get(5010000) is None or time.mktime(met[5010000][2].timetuple()) < ctime - 600:
            metric.append(dict(index_id='5030000', value='连接失败'))
            return -1
        if met[5010000][1] != '连接成功':
            metric.append(dict(index_id='5030000', value='连接失败'))
            return -1
        for m in met.values():
            if m[0] > 5010000 and time.mktime(m[2].timetuple()) > ctime - 600:
                k =  m[0]
                metric.append(dict(index_id=str(5032000+(k%10000)),value=str(round(met[k][1]/met[k][0],2))))
        return 0
    else:
        metric.append(dict(index_id='5030000', value='连接失败'))
        return -1

def do_hdfs(pg, dbInfo, targetId, metric):
    global ctime

    sql = "select ip,port,username,password,subuid from mgt_system where uid='%s' and use_flag" % (targetId)
    result = relate_pg2(pg, sql)
    if result.code == 0 and len(result.msg) > 0:
        host = result.msg[0][0]
        port = result.msg[0][1]
        usr = result.msg[0][2]
        pwd = result.msg[0][3]
        cid = result.msg[0][4]
        if usr and pwd:
            pwd = JavaUtil.decrypt(pwd)
    else:
        metric.append(dict(index_id='5030000', value='连接失败'))
        return
    sql = '''select a.uid,a.ip,a.reserver2,b.uid from mgt_system a,mgt_device b,mgt_system_device c
where a.subuid='%s' and a.uid like '2401%%' and a.use_flag and a.id=c.sys_id and b.id=c.dev_id and c.use_flag''' % (cid)
    result = relate_pg2(pg, sql)
    ns = []
    hs = set()
    if result.code == 0:
        for row in result.msg:
            ns.append([row[0],row[1],row[2],row[3],1])
            hs.add(row[3])
    ctime = int(time.time())
    mets = {}
    bsl = {}
    cnt = 0
    fail = 0
    for it in ns:
        if it[4] == 0:
            continue
        if it[2] == '1':
            if hdfs_name(pg, it[0], metric) < 0:
                return
            else:
                continue
        sql = '''select index_id,value,record_time from mon_indexdata where uid='%s' and index_id in (
5010000,5010511,5010017,5010226,5010227,5010023,5011602,5011600,5011636,5011638,5011665,5011666
)''' % it[0]
        result = relate_pg2(pg, sql)
        met = {}
        if result.code == 0:
            for row in result.msg:
                #ts = time.mktime(row[2].timetuple())
                if row[0] != 5010000:
                    met[row[0]] = [row[0],float(row[1]),row[2]]
                else:
                    met[row[0]] = [row[0],row[1],row[2]]
        if met.get(5010000) is None or time.mktime(met[5010000][2].timetuple()) < ctime - 600:
            continue
        if met[5010000][1] != '连接成功':
            fail += 1
            continue
        if cnt == 0:
            bsl = get_baseline_limit(pg, list(hs)[0], '5010511,5010017,5010226,5010227,5010023,5011602,5011600,5011636,5011638,5011665,5011666') 
        cnt += 1
        for m in met.values():
            if m[0] > 5010000 and time.mktime(m[2].timetuple()) > ctime - 600:
                if mets.get(m[0]) is not None:
                    mets[m[0]][0] += 1
                    mets[m[0]][1] += m[1]
                else:
                    mets[m[0]] = [1,m[1],0]
                if bsl.get(m[0]):
                    if bsl[m[0]][0] is not None:
                        if m[1] > bsl[m[0]][0]:
                            mets[m[0]][2] += 1
                    elif bsl[m[0]][1] is not None:
                        if m[1] < bsl[m[0]][1]:
                            mets[m[0]][2] += 1
                else:
                    mets[m[0]][2] = -1
    if cnt > 0:
        for k in mets.keys():
            metric.append(dict(index_id=str(5034000+(k%10000)),value=str(round(mets[k][1]/mets[k][0],2))))
            if mets[k][2] != -1:
                metric.append(dict(index_id=str(5036000+(k%10000)),value=str(round(mets[k][2]/mets[k][0],2))))
    metric.append(dict(index_id='5030000', value='连接成功'))
    metric.append(dict(index_id='5039999', value=str(ctime)))
    metric.append(dict(index_id='5039996', value=str(cnt)))
    metric.append(dict(index_id='5039997', value=str(fail)))
    if cnt > 0 and hs:
        os_cluster(pg, hs, metric)

def robust(func):
    def add_robust(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except javax.management.RuntimeOperationsException as e:
            bt = str(e)
            exc_type, exc_value, exc_tb = sys.exc_info()
            for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
                bt += "\n%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname)
            print(bt)
            print(exc_type)
            print(exc_value)

    return add_robust

if __name__ == '__main__':
    dbInfo = eval(sys.argv[1])
    usr = dbInfo['target_usr']
    host = dbInfo['target_ip']
    port = dbInfo['target_port']
    target_id = dbInfo['targetId']
    targetId, pg = DBUtil.get_pg_env(dbInfo,0)
    if pg.conn is None:
        print('无法连接本地数据库')
        sys.exit()
    metric = []
    do_hdfs(pg, dbInfo, targetId, metric)
    print('{"results":' + json.dumps(metric, ensure_ascii=False) + '}')

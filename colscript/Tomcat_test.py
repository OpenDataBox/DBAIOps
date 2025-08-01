import json
import sys
import traceback
import time
from collections import Iterable

import jpype
import psycopg2
from jpype import *

sys.path.append('/usr/software/knowl')
# import DBUtil

OLD_GC = {'MarkSweepCompact', 'PS MarkSweep', 'ConcurrentMarkSweep',
          'Garbage collection optimized for short pausetimes Old Collector',
          'Garbage collection optimized for throughput Old Collector',
          'Garbage collection optimized for deterministic pausetimes Old Collector'}


# https://tomcat.apache.org/tomcat-7.0-doc/api/org/apache/tomcat/jdbc/pool/jmx/ConnectionPool.html

def cs(val, dt=False):
    if val is None:
        return ''
    else:
        if dt:
            return val.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return str(val)


class Result(object):
    # pass
    def __str__(self):
        return "\n".join("{}={}".format(k, getattr(self, k))
                         for k in self.__dict__.keys())


def relate_pg2(conn, sql, nrow=0):
    result = Result()
    try:
        cur = conn.cursor()
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


def int2(val):
    if val is None:
        return 0
    return(int(val))


def getsub(jmx, parent, path, level, lbl, mbs, trc=False):
    arr = path[level].split('=')
    t = arr[0].find('.')
    if t > 0:
        p = arr[0][0:t]
        a = arr[0][t + 1]
    else:
        p = arr[0]
        a = 'Name'
    cnt = 0
    v2 = jmx.getAttributes(parent, [p])
    if v2:
        v = v2[0].getValue()
    else:
        v = None
    if v:
        ns = []
        if not isinstance(v, str) and isinstance(v, Iterable):
            t = 0
            for o in v:
                t += 1
                if len(arr) == 1:
                    k = str(t)
                else:
                    k = str(jmx.getAttribute(o, a))
                if len(arr) == 1 or (arr[1] == '*' or arr[1] == k):
                    if level < len(path) - 1:
                        cnt += getsub(jmx, o, path, level + 1, lbl + arr[0] + '=' + k + '/', mbs)
                    else:
                        mbs[lbl + arr[0] + '=' + k] = o
                        cnt += 1
                    if trc and (len(arr) == 1 or arr[1] == '*'):
                        ns.append(k)
        else:
            if len(arr) == 1:
                k = str(1)
            else:
                k = str(jmx.getAttribute(v, a))
            if len(arr) == 1 or arr[1] == '*' or arr[1] == k:
                if level < len(path) - 1:
                    cnt += getsub(jmx, v, path, level + 1, lbl + arr[0] + '=' + k + '/', mbs)
                else:
                    mbs[lbl + arr[0] + '=' + k] = v
                    cnt += 1
                if trc and (len(arr) == 1 or arr[1] == '*'):
                    ns.append(k)
        if ns:
            mbs['+' + lbl + arr[0]] = ns
    return cnt


def getAttributes(jmx, root, path, alist, avals, pfx=None):
    if not isinstance(root, str) and isinstance(root, Iterable):
        t = 1
        for o in root:
            t = getAttributes(jmx, o, path, alist, avals, t)
        return t
    if path:
        arr = path.split('/')
        mbs = {}
        cnt = getsub(jmx, root, arr, 0, '', mbs)
        if cnt:
            for k in mbs.keys():
                if k[0] != '+':
                    b = mbs[k]
                    vs = {}
                    a = jpype.JArray(java.lang.String)(alist)
                    vvv = jmx.getAttributes(b, a)
                    for vv in vvv:
                        v = vv.getValue()
                        if not v is None:
                            vs[str(vv.getName())] = v
                    # for a in alist:
                    #    v = jmx.getAttribute(b, a)
                    #    if v:
                    #        vs[a] = v
                    if vs:
                        if pfx:
                            avals[str(pfx) + '.' + k] = vs
                        else:
                            avals[k] = vs
    else:
        vs = {}
        a = jpype.JArray(java.lang.String)(alist)
        vvv = jmx.getAttributes(root, a)
        for vv in vvv:
            v = vv.getValue()
            if not v is None:
                # if not (str(type(v)) == "<java class 'java.lang.String'>" and v == 'none'):
                vs[str(vv.getName())] = v
        # for a in alist:
        #    v = jmx.getAttribute(root, a)
        #    if v:
        #        vs[a] = v
        if vs:
            if pfx:
                avals[str(pfx) + '.*'] = vs
            else:
                avals['*'] = vs
    if pfx:
        return pfx + 1


def idx_jvm(jmx, metric):
    gcs = []
    pools = []
    mbs = jmx.queryNames(javax.management.ObjectName('java.lang:type=GarbageCollector,name=*'), None)
    for m in mbs:
        gcs.append(m)
    mbs = jmx.queryNames(javax.management.ObjectName('java.lang:type=MemoryPool,name=*'), None)
    for m in mbs:
        pools.append(m)
    object = "java.lang:type=Threading"
    arr = jmx.getAttributes(javax.management.ObjectName(object), ['ThreadCount', 'DaemonThreadCount'])
    if arr:
        metric.append(dict(index_id="4050017", value=str(arr[0].getValue())))
        if len(arr) > 1:
            metric.append(dict(index_id="4050018", value=str(arr[1].getValue())))
            metric.append(dict(index_id="4050019", value=str(arr[0].getValue() - arr[1].getValue())))
        else:
            metric.append(dict(index_id="4050018", value=str(0)))
            metric.append(dict(index_id="4050019", value=str(arr[0].getValue())))
    object = "java.lang:type=Memory"
    arr = jmx.getAttributes(javax.management.ObjectName(object), ['HeapMemoryUsage', 'NonHeapMemoryUsage'])
    if arr:
        mem = arr[0].getValue()
        n1 = mem.get('committed')
        n2 = mem.get('used')
        n3 = mem.get('max')
        metric.append(dict(index_id="4050020", value=str(n1 - n2)))
        metric.append(dict(index_id="4050021", value=str(n1)))
        metric.append(dict(index_id="4050022", value=str(n2)))
        metric.append(dict(index_id="4050023", value=str(round(n2 * 100 / n1, 2))))
        metric.append(dict(index_id="4050033", value=str(n3)))
    object = "java.lang:type=ClassLoading"
    attribute = "LoadedClassCount"
    n = jmx.getAttribute(javax.management.ObjectName(object), attribute)
    metric.append(dict(index_id="4050024", value=str(n)))  # JVM当前装载类
    object = "java.lang:type=Compilation"
    attribute = "TotalCompilationTime"
    n = jmx.getAttribute(javax.management.ObjectName(object), attribute)
    metric.append(dict(index_id="4050025", value=str(n)))
    n1 = 0
    n2 = 0
    t1 = 0
    t2 = 0
    for gc in gcs:
        nm = gc.getCanonicalName()
        arr = jmx.getAttributes(javax.management.ObjectName(nm), ['Name', 'CollectionCount', 'CollectionTime'])
        if arr:
            if str(arr[0].getValue()) in OLD_GC:
                n2 += int2(arr[1].getValue())
                t2 += int2(arr[2].getValue())
            n1 += int2(arr[1].getValue())
            t1 += int2(arr[2].getValue())
    if gcs:
        metric.append(dict(index_id="4050026", value=str(n1)))  # 垃圾收集调用次数
        metric.append(dict(index_id="4050027", value=str(t1)))  # 垃圾收集调用时间(ms)
        metric.append(dict(index_id="4050028", value=str(n2)))  # 老生代垃圾收集调用次数
        metric.append(dict(index_id="4050029", value=str(t2)))  # 老生代垃圾收集调用时间(ms)
    for mp in pools:
        nm = mp.getCanonicalName()
        arr = jmx.getAttributes(javax.management.ObjectName(nm), ['Name', 'Usage'])
        if str(arr[0].getValue()) == 'Metaspace':
            n1 = int2(arr[1].getValue().get('committed'))
            n2 = int2(arr[1].getValue().get('used'))
            metric.append(dict(index_id="4050030", value=str(n1)))  # 已分配元数据空间
            metric.append(dict(index_id="4050031", value=str(n2)))  # 已使用元数据空间
            metric.append(dict(index_id="4050032", value=str(round(n2 * 100 / n1, 2))))
            break
    object = "java.lang:type=Runtime"
    att = jmx.getAttribute(javax.management.ObjectName(object), 'Uptime')
    t_pid = str(jmx.getAttribute(javax.management.ObjectName(object), 'Name')).split('@')[0]
    metric.append(dict(index_id="4050201", value=str(round(att / 1000))))
    if t_pid != '1':
        metric.append(dict(index_id="4050061", value=str(t_pid)))
    # print(metric)


def idx_server(jmx, metric):
    mb = None
    try:
        mbs = jmx.queryNames(javax.management.ObjectName('Catalina:type=Server,*'), None)
        for m in mbs:
            mb = m
        if mb is None:
            return
        vals = jmx.getAttributes(mb, ['stateName'])
        if vals:
            val = str(vals[0].getValue())
        else:
            val = 'STARTED'
        if val == 'STARTED':
            st = 0
        else:
            st = 2
        metric.append(dict(index_id="4050001", value=str(st)))
        # metric.append(dict(index_id="4050002", value=val))
    except javax.management.RuntimeOperationsException as e:
        bt = str(e)
        exc_type, exc_value, exc_tb = sys.exc_info()
        for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
            bt += "\n%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname)
        print(bt)
        print(exc_type)
        print(exc_value)


def idx_connector(jmx, metric):
    try:
        mbs = jmx.queryNames(javax.management.ObjectName('Catalina:type=ThreadPool,*'), None)
        ns = [0] * 10
        for m in mbs:
            mb = m
            alist = ['running', 'currentThreadCount', 'currentThreadsBusy', 'connectionCount']
            avals = {}
            getAttributes(jmx, mb, '', alist, avals)
            for av in avals.values():
                if av.get('running'):
                    ns[0] += int2(av.get('currentThreadCount'))
                    ns[1] += int2(av.get('currentThreadsBusy'))
                    ns[2] += int2(av.get('connectionCount'))
                break
        metric.append(dict(index_id="4050003", value=str(ns[0])))
        metric.append(dict(index_id="4050002", value=str(ns[1])))
        metric.append(dict(index_id="4050004", value=str(ns[2])))
        mbs = jmx.queryNames(javax.management.ObjectName('Catalina:type=Manager,*'), None)
        cnt = 0
        for m in mbs:
            mb = m
            alist = ['stateName', 'sessionAverageAliveTime', 'rejectedSessions', 'duplicates', 'processingTime',
                     'activeSessions', 'expiredSessions', 'sessionCounter']
            avals = {}
            getAttributes(jmx, mb, '', alist, avals)
            for av in avals.values():
                if str(av.get('stateName')) == 'STARTED':
                    ns[3] += int2(av.get('sessionAverageAliveTime'))
                    ns[4] += int2(av.get('rejectedSessions'))
                    ns[5] += int2(av.get('duplicates'))
                    ns[6] += int2(av.get('processingTime'))
                    ns[7] += int2(av.get('activeSessions'))
                    ns[8] += int2(av.get('expiredSessions'))
                    ns[9] += int2(av.get('sessionCounter'))
                    cnt += 1
                break
        if cnt > 0:
            ns[3] = round(ns[3] / cnt, 2)
        metric.append(dict(index_id="4050005", value=str(ns[3])))
        metric.append(dict(index_id="4050006", value=str(ns[4])))
        metric.append(dict(index_id="4050011", value=str(ns[5])))
        metric.append(dict(index_id="4050007", value=str(ns[6])))
        metric.append(dict(index_id="4050008", value=str(ns[7])))
        metric.append(dict(index_id="4050009", value=str(ns[8])))
        metric.append(dict(index_id="4050010", value=str(ns[9])))
    except javax.management.RuntimeOperationsException as e:
        bt = str(e)
        exc_type, exc_value, exc_tb = sys.exc_info()
        for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
            bt += "\n%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname)
        print(bt)
        print(exc_type)
        print(exc_value)


def idx_jdbc(jmx, metric):
    vals = [0] * 25
    vals[14] = 10
    idx_jdbc1(jmx, vals)
    idx_jdbc2(jmx, vals)
    idx_jdbc3(jmx, vals)
    metric.append(dict(index_id="4050034", value=str(vals[0])))
    metric.append(dict(index_id="4050041", value=str(vals[1])))
    metric.append(dict(index_id="4050046", value=str(vals[2])))
    metric.append(dict(index_id="4050036", value=str(vals[3])))
    metric.append(dict(index_id="4050038", value=str(vals[4])))
    metric.append(dict(index_id="4050039", value=str(vals[5])))
    metric.append(dict(index_id="4050040", value=str(vals[6])))
    metric.append(dict(index_id="4050057", value=str(vals[7])))
    metric.append(dict(index_id="4050042", value=str(vals[8])))
    metric.append(dict(index_id="4050043", value=str(vals[9])))
    metric.append(dict(index_id="4050044", value=str(vals[10])))
    metric.append(dict(index_id="4050051", value=str(vals[11])))
    metric.append(dict(index_id="4050049", value=str(vals[12])))
    metric.append(dict(index_id="4050050", value=str(vals[13])))
    metric.append(dict(index_id="4050035", value=str(vals[14])))
    metric.append(dict(index_id="4050047", value=str(vals[15])))
    metric.append(dict(index_id="4050048", value=str(vals[16])))
    metric.append(dict(index_id="4050052", value=str(vals[17])))
    metric.append(dict(index_id="4050055", value=str(vals[18])))
    metric.append(dict(index_id="4050056", value=str(vals[19])))
    metric.append(dict(index_id="4050053", value=str(vals[20])))
    metric.append(dict(index_id="4050054", value=str(vals[21])))
    metric.append(dict(index_id="4050045", value=str(vals[22])))
    metric.append(dict(index_id="4050037", value=str(vals[23])))


def idx_jdbc1(jmx, vals):
    try:
        mbs = jmx.queryNames(javax.management.ObjectName('com.alibaba.druid:type=DruidDataSourceStat'), None)
        for mb in mbs:
            ds = jmx.getAttribute(mb, 'DataSourceList')
            for av in ds.values():
                if int2(av.get('ConnectCount')) > 0:
                    vals[0] += int2(av.get('ActiveCount'))
                    vals[1] += int2(av.get('CloseCount'))
                    vals[2] += int2(av.get('CommitCount'))
                    vals[3] += int2(av.get('ConnectCount'))
                    vals[4] += int2(av.get('CreateCount'))
                    vals[5] += int2(av.get('CreateErrorCount'))
                    vals[6] += int2(av.get('CreateTimespanMillis'))
                    vals[7] += int2(av.get('WaitThreadCount'))
                    vals[8] += int2(av.get('DestroyCount'))
                    vals[9] += int2(av.get('DiscardCount'))
                    vals[10] += int2(av.get('ErrorCount'))
                    vals[11] += int2(av.get('LockQueueLength'))
                    vals[12] += int2(av.get('NotEmptyWaitCount'))
                    vals[13] += round(int2(av.get('NotEmptyWaitNanos')) / 1000000, 2)
                    n = int2(av.get('PoolingCount'))
                    if n < vals[14]:
                        vals[14] = n
                    vals[15] += int2(av.get('RollbackCount'))
                    vals[16] += int2(av.get('StartTransactionCount'))
                    vals[17] += int2(av.get('PreparedStatementCacheAccessCount'))
                    vals[18] += int2(av.get('PreparedStatementCacheCurrentCount'))
                    vals[19] += int2(av.get('PreparedStatementCacheDeleteCount'))
                    vals[20] += int2(av.get('PreparedStatementCacheHitCount'))
                    vals[21] += int2(av.get('PreparedStatementCacheMissCount'))
                    vals[22] += int2(av.get('RemoveAbandonedCount'))
                    vals[23] += int2(av.get('ConnectErrorCount'))
            break
    except javax.management.RuntimeOperationsException as e:
        bt = str(e)
        exc_type, exc_value, exc_tb = sys.exc_info()
        for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
            bt += "\n%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname)
        print(bt)
        print(exc_type)
        print(exc_value)


def idx_jdbc2(jmx, vals):
    try:
        mbs = jmx.queryNames(javax.management.ObjectName('com.mchange.v2.c3p0:type=PooledDataSource,*'), None)
        for m in mbs:
            mb = m
            alist = ['numThreadsAwaitingCheckoutDefaultUser', 'numFailedCheckoutsDefaultUser', 'numConnectionsAllUsers',
                     'numIdleConnectionsAllUsers', 'numBusyConnectionsAllUsers', 'statementCacheNumStatementsAllUsers',
                     'upTimeMillisDefaultUser']
            avals = {}
            getAttributes(jmx, mb, '', alist, avals)
            for av in avals.values():
                if int2(av.get('upTimeMillisDefaultUser')) > 0:
                    vals[0] += int2(av.get('numBusyConnectionsAllUsers'))
                    vals[7] += int2(av.get('numThreadsAwaitingCheckoutDefaultUser'))
                    n = int2(av.get('numIdleConnectionsAllUsers'))
                    if n < vals[14]:
                        vals[14] = n
                    vals[18] += int2(av.get('statementCacheNumStatementsAllUsers'))
                    vals[23] += int2(av.get('numFailedCheckoutsDefaultUser'))
                break
    except javax.management.RuntimeOperationsException as e:
        bt = str(e)
        exc_type, exc_value, exc_tb = sys.exc_info()
        for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
            bt += "\n%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname)
        print(bt)
        print(exc_type)
        print(exc_value)


def idx_jdbc3(jmx, vals):
    try:
        mbs = jmx.queryNames(javax.management.ObjectName('Catalina:type=DataSource,*'), None)
        for m in mbs:
            mb = m
            alist = ['NumActive', 'NumIdle', 'BorrowedCount', 'ReturnedCount', 'CreatedCount', 'ReleasedCount',
                     'WaitCount', 'RemoveAbandonedCount']
            avals = {}
            getAttributes(jmx, mb, '', alist, avals)
            for av in avals.values():
                if int2(av.get('BorrowedCount')) > 0:
                    vals[0] += int2(av.get('NumActive'))
                    vals[7] += int2(av.get('WaitCount'))
                    n = int2(av.get('NumIdle'))
                    if n < vals[14]:
                        vals[14] = n
                    vals[3] += int2(av.get('BorrowedCount'))
                    vals[1] += int2(av.get('ReturnedCount'))
                    vals[4] += int2(av.get('CreatedCount'))
                    vals[8] += int2(av.get('ReleasedCount'))
                break
    except javax.management.RuntimeOperationsException as e:
        bt = str(e)
        exc_type, exc_value, exc_tb = sys.exc_info()
        for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
            bt += "\n%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname)
        print(bt)
        print(exc_type)
        print(exc_value)


def idx_app(jmx, metric):
    try:
        ns = [0] * 5
        mbs = jmx.queryNames(javax.management.ObjectName('Catalina:type=GlobalRequestProcessor,*'), None)
        for m in mbs:
            mb = m
            alist = ['requestCount', 'bytesReceived', 'bytesSent', 'processingTime', 'errorCount']
            avals = {}
            getAttributes(jmx, mb, '', alist, avals)
            for av in avals.values():
                req = int2(av.get('requestCount'))
                if req > 0:
                    ns[0] += req
                    ns[1] += int2(av.get('errorCount'))
                    ns[2] += int2(av.get('bytesReceived'))
                    ns[3] += int2(av.get('bytesSent'))
                    ns[4] += int2(av.get('processingTime'))
                break
        metric.append(dict(index_id="4050014", value=str(ns[0])))
        metric.append(dict(index_id="4050016", value=str(ns[1])))
        metric.append(dict(index_id="4050012", value=str(ns[2])))
        metric.append(dict(index_id="4050013", value=str(ns[3])))
        metric.append(dict(index_id="4050015", value=str(ns[4])))
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


def decrypt(passwords):
    rsa = jpype.JClass('com.dfc.RsaTool.RsaDecryptTool')
    rso = rsa()
    res = []
    for p in passwords:
        res.append(str(rso.decrypt(p)))
    return res


def connect(ip, port, type, user, password):
    URL = "service:jmx:rmi:///jndi/rmi://%s:%s/jmxrmi" % (ip, port)
    jhash = java.util.HashMap()
    # for obj in jhash.getClass().getMethods():
    jarray = jpype.JArray(java.lang.String)([user, password])
    jhash.put(javax.management.remote.JMXConnector.CREDENTIALS, jarray);
    jmxurl = javax.management.remote.JMXServiceURL(URL)
    jmxsoc = javax.management.remote.JMXConnectorFactory.connect(jmxurl, jhash)
    return jmxsoc


if __name__ == '__main__':
    dbInfo = eval(sys.argv[1])
    usr = dbInfo['target_usr']
    host = dbInfo['target_ip']
    port = dbInfo['target_port']
    target_id = dbInfo['targetId']
    initjvm()
    pwds = decrypt([dbInfo['target_pwd'], dbInfo['pg_pwd']])
    pwd = pwds[0]
    try:
        conn = psycopg2.connect(database=dbInfo['pg_db'], user=dbInfo['pg_usr'], password=pwds[1], host=dbInfo['pg_ip'],
                                port=dbInfo['pg_port'])
    except psycopg2.OperationalError as e:
        if not conn is None:
            conn.close()
        print("msg=本地数据库连接失败")
        sys.exit(1)
    ct = time.time()
    metric = []
    try:
        jmxsoc = connect(host, port, 'rmi', usr, pwd)
        jmx = jmxsoc.getMBeanServerConnection()
    except Exception as e:
        metric.append(dict(index_id="4050000", value="连接失败"))
        print('{"results":' + json.dumps(metric) + '}')
        sys.exit(1)
    ct2 = time.time()
    metric.append(dict(index_id="1000102", value=str(int((ct2-ct)*1000))))
    metric.append(dict(index_id="4050000", value="连接成功"))
    idx_jvm(jmx, metric)
    idx_server(jmx, metric)
    idx_connector(jmx, metric)
    idx_jdbc(jmx, metric)
    idx_app(jmx, metric)
    jmxsoc.close();
    ct3 = time.time()
    metric.append(dict(index_id="1000101", value=str(int((ct3-ct2)*1000))))
    print('{"results":' + json.dumps(metric) + '}')

import json
import sys
from collections import Iterable

import jpype
import psycopg2
from jpype import *

from JavaRsa import decrypt

sys.path.append('/usr/software/knowl')
# import DBUtil

global target_id
global admin
global isAdmin

target_id = None
admin = 'Server'
isAdmin = False

OLD_GC = set([
    'MarkSweepCompact',
    'PS MarkSweep',
    'ConcurrentMarkSweep',
    'Garbage collection optimized for short pausetimes Old Collector',
    'Garbage collection optimized for throughput Old Collector',
    'Garbage collection optimized for deterministic pausetimes Old Collector'
])


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


def average(avals, att, nvl=0, ref=None, thr=0, weight=True):
    t1 = 0
    t2 = 0
    f = True
    for av in avals.values():
        if ref:
            v = av.get(ref)
            if v is None:
                continue
            else:
                if thr and int(v) < thr:
                    continue
            if weight:
                t = int(v)
            else:
                t = 1
        else:
            t = 1
        v = av.get(att)
        if not v is None:
            t1 += int(v)
            t2 += t
            f = False
    if f:
        return nvl
    return t1 / t2


def subtotal(avals, att, nvl=0):
    t = 0
    f = True
    for av in avals.values():
        v = av.get(att)
        if v:
            t += int(str(v))
            f = False
    if f:
        return nvl
    return t


def getsum(jmx, parent, path, alist, avals, ref=None, thr=0, parr=None, level=None):
    cnt = 0
    if path:
        pp = parr
        lv = level
        if pp is None:
            pp = path.split('/')
            lv = 0
        arr = pp[lv].split('=')
        t = arr[0].find('.')
        if t > 0:
            p = arr[0][0:t]
            a = arr[0][t + 1]
        else:
            p = arr[0]
            a = 'Name'
        v = jmx.getAttribute(parent, p)
        if v:
            if not isinstance(v, str) and isinstance(v, Iterable):
                for o in v:
                    if len(arr) > 1:
                        k = str(jmx.getAttribute(o, a))
                    if len(arr) <= 1 or (arr[1] == '*' or arr[1] == k):
                        if lv < len(pp) - 1:
                            cnt += getsum(jmx, o, path, alist, avals, ref, thr, pp, lv + 1)
                        else:
                            vvv = jmx.getAttributes(o, alist)
                            first = not ref is None
                            if first:
                                tt = 0
                            else:
                                tt = 1
                            for vv in vvv:
                                s = str(vv.getName())
                                if first and s != ref:
                                    break
                                v = vv.getValue()
                                if not v is None:
                                    if first:
                                        if int(v) < thr:
                                            break
                                        else:
                                            tt = 1
                                            first = False
                                    n = avals.get(s)
                                    if n is None:
                                        avals[s] = int(v)
                                    else:
                                        avals[s] = int(v) + n
                                else:
                                    if first:
                                        break
                            cnt += tt
            else:
                if len(arr) > 1:
                    k = str(jmx.getAttribute(v, a))
                if len(arr) <= 1 or arr[1] == '*' or arr[1] == k:
                    if lv < len(pp) - 1:
                        cnt += getsum(jmx, v, path, alist, avals, ref, thr, pp, lv + 1)
                    else:
                        vvv = jmx.getAttributes(v, alist)
                        first = not ref is None
                        if first:
                            tt = 0
                        else:
                            tt = 1
                        for vv in vvv:
                            s = str(vv.getName())
                            if first and s != ref:
                                break
                            v = vv.getValue()
                            if not v is None:
                                if first:
                                    if int(v) < thr:
                                        break
                                    else:
                                        tt = 1
                                        first = False
                                n = avals.get(s)
                                if n is None:
                                    avals[s] = int(v)
                                else:
                                    avals[s] = int(v) + n
                            else:
                                if first:
                                    break
                        cnt += tt
    else:
        vvv = jmx.getAttributes(parent, alist)
        first = not ref is None
        if first:
            tt = 0
        else:
            tt = 1
        for vv in vvv:
            s = str(vv.getName())
            if first and s != ref:
                break
            v = vv.getValue()
            if not v is None:
                if first:
                    if int(v) < thr:
                        break
                    else:
                        tt = 1
                        first = False
                n = avals.get(s)
                if n is None:
                    avals[s] = int(v)
                else:
                    avals[s] = int(v) + n
            else:
                if first:
                    break
        cnt += tt
    return cnt


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


def getMetaInfo(jmx, obj=None):
    if not obj:
        mbs = jmx.queryNames(javax.management.ObjectName('java.lang:Location=AdminServer,type=*'), None)
        for m in mbs:
            if str(m).find('java.lang') == 0:
                print(m)
        return
    for m in obj.getClass().getDeclaredMethods():
        print(m.getName())
    info = jmx.getMBeanInfo(obj)
    atts = info.getAttributes()
    for o in atts:
        if o.isReadable():
            print(o.getName())


def idx_jvm(db, jmx, server, loc, metric):
    if loc:
        object = "java.lang:Location=%s,type=Threading" % loc
    else:
        object = "java.lang:type=Threading"
    arr = jmx.getAttributes(javax.management.ObjectName(object), ['ThreadCount', 'DaemonThreadCount'])
    if arr:
        metric.append(dict(index_id="4010019", value=str(arr[0].getValue())))
        if len(arr) > 1:
            metric.append(dict(index_id="4010018", value=str(arr[1].getValue())))
    if loc:
        object = "java.lang:Location=%s,type=Memory" % loc
    else:
        object = "java.lang:type=Memory"
    arr = jmx.getAttributes(javax.management.ObjectName(object), ['HeapMemoryUsage', 'NonHeapMemoryUsage'])
    if arr:
        mem = arr[0].getValue()
        n1 = mem.get('committed')
        n2 = mem.get('used')
        metric.append(dict(index_id="4010301", value=str(n1 - n2)))
        metric.append(dict(index_id="4010302", value=str(n1)))
        metric.append(dict(index_id="4010303", value=str(round(n2 * 100 / n1, 2))))
        if len(arr) > 1:
            mem = arr[1].getValue()
            n1 = mem.get('committed')
            n2 = mem.get('used')
            metric.append(dict(index_id="4010304", value=str(n1 - n2)))
            metric.append(dict(index_id="4010305", value=str(n1)))
            metric.append(dict(index_id="4010306", value=str(round(n2 * 100 / n1, 2))))
    if loc:
        object = "java.lang:Location=%s,type=ClassLoading" % loc
    else:
        object = "java.lang:type=ClassLoading"
    attribute = "LoadedClassCount"
    n = jmx.getAttribute(javax.management.ObjectName(object), attribute)
    metric.append(dict(index_id="4010024", value=str(n)))
    if loc:
        object = "java.lang:Location=%s,type=Compilation" % loc
    else:
        object = "java.lang:type=Compilation"
    attribute = "TotalCompilationTime"
    n = jmx.getAttribute(javax.management.ObjectName(object), attribute)
    metric.append(dict(index_id="4010025", value=str(n)))
    n1 = 0
    n2 = 0
    t1 = 0
    t2 = 0
    for gc in gcs:
        nm = gc.getCanonicalName()
        arr = jmx.getAttributes(javax.management.ObjectName(nm), ['Name', 'CollectionCount', 'CollectionTime'])
        if arr:
            if str(arr[0].getValue()) in OLD_GC:
                n2 += int(arr[1].getValue())
                t2 += int(arr[2].getValue())
            n1 += int(arr[1].getValue())
            t1 += int(arr[2].getValue())
    if gcs:
        metric.append(dict(index_id="4010026", value=str(n1)))
        metric.append(dict(index_id="4010027", value=str(t1)))
        metric.append(dict(index_id="4010028", value=str(n2)))
        metric.append(dict(index_id="4010029", value=str(t2)))
    for mp in pools:
        nm = mp.getCanonicalName()
        arr = jmx.getAttributes(javax.management.ObjectName(nm), ['Name', 'Usage'])
        if str(arr[0].getValue()) == 'Metaspace':
            n1 = int(arr[1].getValue().get('committed'))
            n2 = int(arr[1].getValue().get('used'))
            metric.append(dict(index_id="4010030", value=str(n1)))
            metric.append(dict(index_id="4010031", value=str(n2)))
            metric.append(dict(index_id="4010032", value=str(round(n2 * 100 / n1, 2))))
            break
    # print(metric)


def idx_wm(db, jmx, server, loc, metric):
    alist = ['OverallHealthState', 'State', 'ServerChannelRuntimes', 'WorkManagerRuntimes']
    avals = {}
    getAttributes(jmx, server, '', alist, avals)
    for av in avals.values():
        att = av.get('OverallHealthState')
        if att:
            h = att.getState()
            metric.append(dict(index_id="4010001", value=str(h)))
        s = av.get('State')
        metric.append(dict(index_id="4010300", value=str(s)))
        cs = av.get('ServerChannelRuntimes')
        if cs:
            # als = ['ChannelName','PublicURL','BytesReceivedCount','BytesSentCount','AcceptCount']
            als = ['BytesReceivedCount', 'BytesSentCount', 'AcceptCount']
            avs = {}
            for c in cs:
                getsum(jmx, c, '', als, avs)
            n = avs.get('BytesReceivedCount')
            if not n is None:
                metric.append(dict(index_id="4010083", value=str(n)))
            n = avs.get('BytesSentCount')
            if not n is None:
                metric.append(dict(index_id="4010084", value=str(n)))
            n = avs.get('AcceptCount')
            if not n is None:
                metric.append(dict(index_id="4010088", value=str(n)))
        wms = av.get('WorkManagerRuntimes')
        if wms:
            als = ['PendingRequests', 'StuckThreadCount', 'CompletedRequests']
            avs = {}
            for wm in wms:
                getsum(jmx, wm, '', als, avs)
            n = avs.get('PendingRequests')
            if n is None:
                n = 0
            metric.append(dict(index_id="4010006", value=str(n)))
            n = avs.get('StuckThreadCount')
            if n is None:
                n = 0
            metric.append(dict(index_id="4010007", value=str(n)))
            n = avs.get('CompletedRequests')
            if n is None:
                n = 0
            metric.append(dict(index_id="4010008", value=str(n)))
        else:
            metric.append(dict(index_id="4010006", value=str(0)))
            metric.append(dict(index_id="4010007", value=str(0)))
            metric.append(dict(index_id="4010008", value=str(0)))
        break
    alist = ['HeapFreeCurrent', 'HeapFreePercent', 'HeapSizeCurrent', 'Uptime']
    avals = {}
    getAttributes(jmx, server, 'JVMRuntime', alist, avals)
    for av in avals.values():
        n1 = None
        n2 = None
        for a in av:
            if a == 'Uptime':
                uptime = int(av[a] / 1000)
                metric.append(dict(index_id="4010201", value=str(uptime)))
            elif a == 'HeapFreeCurrent':
                n2 = av[a]
                metric.append(dict(index_id="4010020", value=str(av[a])))
            elif a == 'HeapSizeCurrent':
                n1 = av[a]
                metric.append(dict(index_id="4010021", value=str(av[a])))
            elif a == 'HeapFreePercent':
                metric.append(dict(index_id="4010023", value=str(100 - av[a])))
        if not n1 is None and not n2 is None:
            metric.append(dict(index_id="4010022", value=str(n1 - n2)))
    alist = ['QueueLength', 'HoggingThreadCount', 'PendingUserRequestCount', 'CompletedRequestCount',
             'ExecuteThreadTotalCount', 'StandbyThreadCount', 'StuckThreadCount']
    avals = {}
    getAttributes(jmx, server, 'ThreadPoolRuntime', alist, avals)
    for av in avals.values():
        n1 = None
        n2 = None
        for a in av:
            if a == 'HoggingThreadCount':
                metric.append(dict(index_id="4010002", value=str(av[a])))
            elif a == 'PendingUserRequestCount':
                metric.append(dict(index_id="4010093", value=str(av[a])))
            elif a == 'CompletedRequestCount':
                metric.append(dict(index_id="4010004", value=str(av[a])))
            elif a == 'QueueLength':
                metric.append(dict(index_id="4010003", value=str(av[a])))
            elif a == 'StuckThreadCount':
                metric.append(dict(index_id="4010092", value=str(av[a])))
            elif a == 'ExecuteThreadTotalCount':
                n1 = av[a]
            elif a == 'StandbyThreadCount':
                n2 = av[a]
        if not n1 is None and not n2 is None:
            metric.append(dict(index_id="4010005", value=str(n1 - n2)))
    # print(metric)


def idx_svc(db, jmx, server, loc, metric):
    alist = ['JTARuntime', 'JDBCServiceRuntime', 'JMSRuntime']
    avals = {}
    getAttributes(jmx, server, '', alist, avals)
    for av in avals.values():
        jta = av.get('JTARuntime')
        if jta:
            als = ['TransactionAbandonedTotalCount', 'TransactionCommittedTotalCount',
                   'TransactionRolledBackTotalCount', 'TransactionTotalCount', 'ActiveTransactionsTotalCount',
                   'SecondsActiveTotalCount']
            arr = jmx.getAttributes(jta, als)
            if arr:
                for kv in arr:
                    s = str(kv.getName())
                    v = str(kv.getValue())
                    if s == 'TransactionAbandonedTotalCount':
                        metric.append(dict(index_id="4010011", value=v))
                    elif s == 'TransactionCommittedTotalCount':
                        metric.append(dict(index_id="4010012", value=v))
                    elif s == 'TransactionTotalCount':
                        metric.append(dict(index_id="4010013", value=v))
                    elif s == 'TransactionRolledBackTotalCount':
                        metric.append(dict(index_id="4010014", value=v))
                    elif s == 'ActiveTransactionsTotalCount':
                        metric.append(dict(index_id="4010015", value=v))
                    elif s == 'SecondsActiveTotalCount':
                        metric.append(dict(index_id="4010017", value=v))
        jdbc = av.get('JDBCServiceRuntime')
        if jdbc:
            als = ['Name', 'ActiveConnectionsCurrentCount', 'ConnectionDelayTime', 'ReserveRequestCount',
                   'WaitingForConnectionTotal', 'PrepStmtCacheAccessCount', 'NumAvailable', 'CurrCapacity',
                   'NumUnavailable', 'ConnectionsTotalCount', 'LeakedConnectionCount', 'FailedReserveRequestCount',
                   'WaitingForConnectionSuccessTotal', 'WaitingForConnectionFailureTotal', 'PrepStmtCacheHitCount',
                   'CurrCapacityHighCount']
            avs = {}
            getAttributes(jmx, jdbc, 'JDBCDataSourceRuntimeMBeans', als, avs)
            n = subtotal(avs, 'ConnectionDelayTime')
            metric.append(dict(index_id="4010053", value=str(n)))
            n = subtotal(avs, 'ReserveRequestCount')
            metric.append(dict(index_id="4010054", value=str(n)))
            n = subtotal(avs, 'WaitingForConnectionTotal')
            metric.append(dict(index_id="4010055", value=str(n)))
            n = subtotal(avs, 'PrepStmtCacheHitCount')
            metric.append(dict(index_id="4010056", value=str(n)))
            n = subtotal(avs, 'ActiveConnectionsCurrentCount')
            metric.append(dict(index_id="4010058", value=str(n)))
            n = subtotal(avs, 'NumUnavailable')
            metric.append(dict(index_id="4010059", value=str(n)))
            n = subtotal(avs, 'LeakedConnectionCount')
            metric.append(dict(index_id="4010063", value=str(n)))
            n = subtotal(avs, 'FailedReserveRequestCount')
            metric.append(dict(index_id="4010085", value=str(n)))
            n = subtotal(avs, 'WaitingForConnectionFailureTotal')
            metric.append(dict(index_id="4010086", value=str(n)))
            n = subtotal(avs, 'PrepStmtCacheAccessCount')
            metric.append(dict(index_id="4010087", value=str(n)))
            n = subtotal(avs, 'ConnectionsTotalCount')
            metric.append(dict(index_id="4010094", value=str(n)))
            val = []
            n = 20
            for v in avs.values():
                n1 = v.get('ReserveRequestCount')
                if n1 > 0:
                    s = str(v.get('Name'))
                    if s.find('@') < 0:
                        n1 = v.get('CurrCapacityHighCount')  # HighestNumAvailable
                        n2 = v.get('NumAvailable')
                        n3 = v.get('NumUnavailable')
                        val.append(dict(name=s, value=str(n2)))
                        if n1 - n3 > n2:
                            n2 = n1 - n3
                        if n2 < n:
                            n = n2
            metric.append(dict(index_id="4010057", value=str(n)))
            if val:
                metric.append(dict(index_id="4010095", value=val))
        jms = av.get('JMSRuntime')
        if jms:
            als = ['Name', 'ConnectionsTotalCount', 'JMSServersTotalCount', 'JMSServers']
            arr = jmx.getAttributes(jms, als)
            js = None
            if arr:
                for kv in arr:
                    s = str(kv.getName())
                    v = kv.getValue()
                    if s == 'ConnectionsTotalCount':
                        metric.append(dict(index_id="4010067", value=str(v)))
                    elif s == 'JMSServersTotalCount':
                        metric.append(dict(index_id="4010068", value=str(v)))
                    elif s == 'JMSServers':
                        js = v
            if js:
                als = ['BytesReceivedCount', 'MessagesReceivedCount', 'BytesPagedOutTotalCount',
                       'BytesPagedInTotalCount', 'MessagesPagedInTotalCount', 'MessagesPagedOutTotalCount',
                       'BytesPendingCount', 'MessagesPendingCount', 'MessagesCurrentCount', 'BytesCurrentCount',
                       'Destinations', 'SessionPoolRuntimes']
                avs = {}
                getAttribute(jmx, js, '', als, avs)
                n = subtotal(avs, 'BytesReceivedCount')
                if not n is None:
                    metric.append(dict(index_id="4010069", value=str(n)))
                n = subtotal(avs, 'BytesPagedInTotalCount')
                if not n is None:
                    metric.append(dict(index_id="4010072", value=str(n)))
                n = subtotal(avs, 'BytesPagedOutTotalCount')
                if not n is None:
                    metric.append(dict(index_id="4010073", value=str(n)))
                n = subtotal(avs, 'MessagesPagedInTotalCount')
                if not n is None:
                    metric.append(dict(index_id="4010074", value=str(n)))
                n = subtotal(avs, 'MessagesPagedOutTotalCount')
                if not n is None:
                    metric.append(dict(index_id="4010075", value=str(n)))
                n = subtotal(avs, 'MessagesReceivedCount')
                if not n is None:
                    metric.append(dict(index_id="4010076", value=str(n)))
                n = subtotal(avs, 'BytesCurrentCount')
                if not n is None:
                    metric.append(dict(index_id="4010077", value=str(n)))
                n = subtotal(avs, 'BytesPendingCount')
                if not n is None:
                    metric.append(dict(index_id="4010078", value=str(n)))
                n = subtotal(avs, 'MessagesPendingCount')
                if not n is None:
                    metric.append(dict(index_id="4010079", value=str(n)))
                n = subtotal(avs, 'MessagesCurrentCount')
                if not n is None:
                    metric.append(dict(index_id="4010080", value=str(n)))
                als = ['MessagesMovedCurrentCount', 'MessagesDeletedCurrentCount', 'ConsumersCurrentCount']
                ads = {}
                n1 = 0
                n2 = 0
                for av in avs.values():
                    v = av.get('SessionPoolRuntimes')
                    if v:
                        n2 += len(v)
                    ds = av.get('Destinations')
                    if ds:
                        n1 += len(ds)
                        for d in ds:
                            getsum(jmx, d, '', als, ads)
                metric.append(dict(index_id="4010081", value=str(n1)))
                metric.append(dict(index_id="4010082", value=str(n2)))
                n = ads.get('MessagesMovedCurrentCount')
                if not n is None:
                    metric.append(dict(index_id="4010070", value=str(n)))
                n = ads.get('MessagesDeletedCurrentCount')
                if not n is None:
                    metric.append(dict(index_id="4010071", value=str(n)))
            else:
                metric.append(dict(index_id="4010069", value=str(0)))
                metric.append(dict(index_id="4010072", value=str(0)))
                metric.append(dict(index_id="4010073", value=str(0)))
                metric.append(dict(index_id="4010074", value=str(0)))
                metric.append(dict(index_id="4010075", value=str(0)))
                metric.append(dict(index_id="4010076", value=str(0)))
                metric.append(dict(index_id="4010077", value=str(0)))
                metric.append(dict(index_id="4010078", value=str(0)))
                metric.append(dict(index_id="4010079", value=str(0)))
                metric.append(dict(index_id="4010080", value=str(0)))
                metric.append(dict(index_id="4010081", value=str(0)))
                metric.append(dict(index_id="4010082", value=str(0)))
                metric.append(dict(index_id="4010070", value=str(0)))
                metric.append(dict(index_id="4010071", value=str(0)))


def idx_app(db, jmx, server, loc, metric):
    apps = jmx.getAttribute(server, 'ApplicationRuntimes')
    ejbs = []
    webs = []
    cps = []
    for app in apps:
        comps = jmx.getAttribute(app, 'ComponentRuntimes')
        for comp in comps:
            typ = str(jmx.getAttribute(comp, 'Type'))
            if typ.find('EJB') >= 0:
                ejbs.append([typ, comp])
            elif typ.find('WebApp') >= 0:
                webs.append([typ, comp])
                ejbs.append(['WebApp', comp])
            elif typ.find('Connector') >= 0:
                cps.append([typ, comp])
    if ejbs:
        ns = [0] * 11
        for ejb in ejbs:
            alist = ['TransactionsCommittedTotalCount', 'TransactionsRolledBackTotalCount',
                     'TransactionsTimedOutTotalCount']
            avals = {}
            getAttributes(jmx, ejb[1], 'EJBRuntimes/TransactionRuntime', alist, avals)
            ns[1] += subtotal(avals, 'TransactionsCommittedTotalCount')
            ns[2] += subtotal(avals, 'TransactionsRolledBackTotalCount')
            ns[3] += subtotal(avals, 'TransactionsTimedOutTotalCount')
            alist = ['Type', 'CacheRuntime', 'PoolRuntime', 'ProcessedMessageCount']
            # 'EntityEJBRuntimeMBean','MessageDrivenEJBRuntimeMBean','StatefulEJBRuntimeMBean','StatelessEJBRuntimeMBean'
            avals = {}
            getAttributes(jmx, ejb[1], 'EJBRuntimes', alist, avals)
            for av in avals.values():
                typ = av.get('Type')
                cs = av.get('CacheRuntime')
                if cs:
                    als = ['ActivationCount', 'CacheAccessCount', 'CacheMissCount', 'PassivationCount']
                    avs = {}
                    getAttributes(jmx, cs, '', als, avs)
                    ns[4] += subtotal(avs, 'CacheAccessCount')
                    ns[5] += subtotal(avs, 'CacheMissCount')
                    ns[6] += subtotal(avs, 'ActivationCount')
                    ns[7] += subtotal(avs, 'PassivationCount')
                ps = av.get('PoolRuntime')
                if ps:
                    als = ['AccessTotalCount', 'PooledBeansCurrentCount', 'MissTotalCount', 'BeansInUseCurrentCount',
                           'DestroyedTotalCount', 'TimeoutTotalCount', 'WaiterCurrentCount']
                    avs = {}
                    getAttributes(jmx, ps, '', als, avs)
                    ns[8] += subtotal(avs, 'AccessTotalCount')
                    ns[9] += subtotal(avs, 'MissTotalCount')
                    ns[10] += subtotal(avs, 'BeansInUseCurrentCount')
                n = av.get('ProcessedMessageCount')
                if not n is None:
                    ns[0] += int(n)
        metric.append(dict(index_id="4010043", value=str(ns[0])))
        metric.append(dict(index_id="4010040", value=str(ns[1])))
        metric.append(dict(index_id="4010041", value=str(ns[2])))
        metric.append(dict(index_id="4010042", value=str(ns[3])))
        metric.append(dict(index_id="4010033", value=str(ns[4])))
        metric.append(dict(index_id="4010034", value=str(ns[5])))
        metric.append(dict(index_id="4010037", value=str(ns[6])))
        metric.append(dict(index_id="4010038", value=str(ns[7])))
        metric.append(dict(index_id="4010035", value=str(ns[8])))
        metric.append(dict(index_id="4010036", value=str(ns[9])))
        metric.append(dict(index_id="4010039", value=str(ns[10])))
    if webs:
        alist = ['InvocationTotalCount', 'ExecutionTimeTotal', 'ExecutionTimeAverage']
        alist2 = ['DispatchTimeTotal', 'ErrorCount', 'InvocationCount', 'ExecutionTimeTotal', 'ResponseCount',
                  'ResponseErrorCount', 'ResponseTimeTotal']
        avals = {}
        avals2 = {}
        n1 = 0
        n2 = 0
        tt = 0
        for web in webs:
            arr = jmx.getAttributes(web[1], ['OpenSessionsCurrentCount', 'SessionsOpenedTotalCount'])
            if arr:
                n1 += int(arr[0].getValue())
                n2 += int(arr[1].getValue())
            tt += getsum(jmx, web[1], 'Servlets', alist, avals, 'InvocationTotalCount', 1)
            # print(avals)
            getsum(jmx, web[1], 'WseeV2Runtimes/Ports/Operations', alist2, avals2)
        metric.append(dict(index_id="4010045", value=str(n1)))
        metric.append(dict(index_id="4010091", value=str(n2)))
        n = avals.get('InvocationTotalCount')
        if n is None:
            n = 0
        metric.append(dict(index_id="4010044", value=str(n)))
        n = avals.get('ExecutionTimeTotal')
        if n is None:
            n = 0
        metric.append(dict(index_id="4010051", value=str(n)))
        if tt > 0:
            n = avals.get('ExecutionTimeAverage')
            if not n is None:
                metric.append(dict(index_id="4010308", value=str(n / tt)))
        else:
            metric.append(dict(index_id="4010308", value=str(0)))
        n = avals2.get('DispatchTimeTotal')
        if n is None:
            n = 0
        metric.append(dict(index_id="4010046", value=str(n)))
        n = avals2.get('InvocationCount')
        if n is None:
            n = 0
        metric.append(dict(index_id="4010047", value=str(n)))
        n = avals2.get('ResponseCount')
        if n is None:
            n = 0
        metric.append(dict(index_id="4010048", value=str(n)))
        n = avals2.get('ExecutionTimeTotal')
        if n is None:
            n = 0
        metric.append(dict(index_id="4010049", value=str(n)))
        n = avals2.get('ResponseTimeTotal')
        if n is None:
            n = 0
        metric.append(dict(index_id="4010050", value=str(n)))
        n = avals2.get('ResponseErrorCount')
        if n is None:
            n = 0
        metric.append(dict(index_id="4010052", value=str(n)))
    if cps:
        alist = ['ConnectionsCreatedTotalCount', 'ConnectionsDestroyedByErrorTotalCount',
                 'ConnectionsDestroyedByShrinkingTotalCount', 'ConnectionsDestroyedTotalCount',
                 'ConnectionsRejectedTotalCount', 'ConnectionsMatchedTotalCount', 'RecycledTotal', 'CloseCount',
                 'NumWaitersCurrentCount', 'NumUnavailableCurrentCount', 'FreeConnectionsCurrentCount',
                 'ActiveConnectionsCurrentCount']
        avals = {}
        for cp in cps:
            arr = jmx.getAttributes(cp[1], ['OpenSessionsCurrentCount', 'SessionsOpenedTotalCount'])
            if arr:
                n1 += int(arr[0].getValue())
                n2 += int(arr[1].getValue())
            getsum(jmx, cp[1], 'ConnectionPools', alist, avals)
        n = avals.get('ConnectionsCreatedTotalCount')
        if not n is None:
            metric.append(dict(index_id="4010060", value=str(n)))
        n = avals.get('ConnectionsDestroyedByErrorTotalCount')
        if not n is None:
            metric.append(dict(index_id="4010061", value=str(n)))
        n = avals.get('ConnectionsDestroyedTotalCount')
        if not n is None:
            metric.append(dict(index_id="4010062", value=str(n)))
    else:
        metric.append(dict(index_id="4010060", value=str(0)))
        metric.append(dict(index_id="4010061", value=str(0)))
        metric.append(dict(index_id="4010062", value=str(0)))


def initjvm():
    # print(getDefaultJVMPath())
    if not jpype.isJVMStarted():
        jpype.startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=/usr/software/knowl/wlfullclient.jar",
                       convertStrings=False)


def connect(ip, port, type, user, password):
    if type == 'domain':
        URL = "service:jmx:t3://%s:%s/jndi/weblogic.management.mbeanservers.domainruntime" % (ip, port)
    else:
        URL = "service:jmx:t3://%s:%s/jndi/weblogic.management.mbeanservers.%s" % (ip, port, type)
    jhash = java.util.HashMap()
    # for obj in jhash.getClass().getMethods():
    jarray = jpype.JArray(java.lang.String)([user, password])
    jhash.put(javax.management.remote.JMXConnector.CREDENTIALS, jarray);
    jhash.put(javax.management.remote.JMXConnectorFactory.PROTOCOL_PROVIDER_PACKAGES, 'weblogic.management.remote');
    jmxurl = javax.management.remote.JMXServiceURL(URL)
    jmxsoc = javax.management.remote.JMXConnectorFactory.connect(jmxurl, jhash)
    return jmxsoc


if __name__ == '__main__':
    dbInfo = eval(sys.argv[1])
    usr = dbInfo['target_usr']
    host = dbInfo['target_ip']
    port = dbInfo['target_port']
    target_id = dbInfo['targetId']
    sid = dbInfo['target_inst']
    metric = []
    initjvm()
    pwd = decrypt(dbInfo['target_pwd'])
    # pwds = [dbInfo['target_pwd'],dbInfo['pg_pwd']]
    try:
        conn = psycopg2.connect(database=dbInfo['pg_db'], user=dbInfo['pg_usr'], password=pwds[1], host=dbInfo['pg_ip'],
                                port=dbInfo['pg_port'])
    except psycopg2.OperationalError as e:
        if not conn is None:
            conn.close()
        msg = "本地数据库连接失败"
        metric.append(dict(index_id="4010000", value=msg))
        sys.exit(1)
    # jmxsoc = connect('60.60.60.165', 7001, 'runtime', 'weblogic', 'weblogic1')
    jmxsoc = connect(host, port, 'runtime', usr, pwd)
    jmx = jmxsoc.getMBeanServerConnection();
    server = None
    object = "com.bea:Name=RuntimeService,Type=weblogic.management.mbeanservers.runtime.RuntimeServiceMBean"
    s = jmx.getAttribute(javax.management.ObjectName(object), 'ServerName')
    gcs = []
    pools = []
    if s != sid:
        jmxsoc.close();
        jmxsoc = connect(host, port, 'domain', usr, pwd)
        jmx = jmxsoc.getMBeanServerConnection()
        object = "com.bea:Name=DomainRuntimeService,Type=weblogic.management.mbeanservers.domainruntime.DomainRuntimeServiceMBean"
        admin = str(jmx.getAttribute(javax.management.ObjectName(object), 'ServerName'))
        srvs = jmx.getAttribute(javax.management.ObjectName(object), 'ServerRuntimes')
        for srv in srvs:
            s = str(jmx.getAttribute(srv, 'Name'))
            if s == sid:
                server = srv
                mbs = jmx.queryNames(
                    javax.management.ObjectName('java.lang:Location=%s,type=GarbageCollector,name=*' % sid), None)
                for m in mbs:
                    gcs.append(m)
                mbs = jmx.queryNames(javax.management.ObjectName('java.lang:Location=%s,type=MemoryPool,name=*' % sid),
                                     None)
                for m in mbs:
                    pools.append(m)
                break
        if not server:
            msg = "该应用服务器[%s]不存在或未运行" % sid
            metric.append(dict(index_id="4010000", value=msg))
            sys.exit(1)
        loc = sid
    else:
        object = "com.bea:Name=RuntimeService,Type=weblogic.management.mbeanservers.runtime.RuntimeServiceMBean"
        server = jmx.getAttribute(javax.management.ObjectName(object), 'ServerRuntime')
        # mbs = jmx.queryMBeans(javax.management.ObjectName('java.lang:type=GarbageCollector,name=*'),None)
        mbs = jmx.queryNames(javax.management.ObjectName('java.lang:type=GarbageCollector,name=*'), None)
        for m in mbs:
            gcs.append(m)
        mbs = jmx.queryNames(javax.management.ObjectName('java.lang:type=MemoryPool,name=*'), None)
        for m in mbs:
            pools.append(m)
        loc = None
    metric.append(dict(index_id="4010000", value="连接成功"))
    idx_jvm(conn, jmx, server, loc, metric)
    idx_wm(conn, jmx, server, loc, metric)
    idx_svc(conn, jmx, server, loc, metric)
    idx_app(conn, jmx, server, loc, metric)
    jmxsoc.close();
    # print('{"metric":' + json.dumps(metric) + '}')
    print('{"results":' + json.dumps(metric) + '}')

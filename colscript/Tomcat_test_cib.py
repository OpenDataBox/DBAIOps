import sys
import traceback
import json
from collections import Iterable
import time, datetime
from datetime import date, datetime, timedelta
from jpype import *
import jpype
sys.path.append('/usr/software/knowl')
from CommUtil import FormatTime
import DBUtil
import psycopg2

CIB_BASIC = set([
'serverInfo',
'serverNumber',
'baseDir',
'defaultHost',
'backgroundProcessorDelay',
'autoDeploy',
'deployOnStartup',
'unpackWARs',
'appBase',
'nonport',
'sslport','StartTime', 'VmName', 'VmVendor', 'VmVersion', 'Uptime', 'Name'
])

#https://tomcat.apache.org/tomcat-7.0-doc/api/org/apache/tomcat/jdbc/pool/jmx/ConnectionPool.html

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

def getsub(jmx, parent, path, level, lbl, mbs, trc=False):
    arr = path[level].split('=')
    t = arr[0].find('.')
    if t > 0:
        p = arr[0][0:t]
        a = arr[0][t+1]
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
                        cnt += getsub(jmx, o, path, level+1, lbl+arr[0]+'='+k+'/', mbs)
                    else:
                        mbs[lbl+arr[0]+'='+k] = o
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
                    cnt += getsub(jmx, v, path, level+1, lbl+arr[0]+'='+k+'/', mbs)
                else:
                    mbs[lbl+arr[0]+'='+k] = v
                    cnt += 1
                if trc and (len(arr) == 1 or arr[1] == '*'):
                    ns.append(k)
        if ns:
            mbs['+'+lbl+arr[0]] = ns
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
                    #for a in alist:
                    #    v = jmx.getAttribute(b, a)
                    #    if v:
                    #        vs[a] = v
                    if vs:
                        if pfx:
                            avals[str(pfx)+'.'+k] = vs
                        else:
                            avals[k] = vs
    else:
        vs = {}
        a = jpype.JArray(java.lang.String)(alist)
        vvv = jmx.getAttributes(root, a)
        for vv in vvv:
            v = vv.getValue()
            if not v is None:
                #if not (str(type(v)) == "<java class 'java.lang.String'>" and v == 'none'):
                vs[str(vv.getName())] = v
        #for a in alist:
        #    v = jmx.getAttribute(root, a)
        #    if v:
        #        vs[a] = v
        if vs:
            if pfx:
                avals[str(pfx)+'.*'] = vs
            else:
                avals['*'] = vs
    if pfx:
        return pfx + 1

def cib_basic(jmx, bean):
    vals = None
    mb = None
    try:
        mbs = jmx.queryNames(javax.management.ObjectName('Catalina:type=Server,*'),None)
        for m in mbs:
            mb = m
        if mb is None:
            return
        alist = ['serverInfo','stateName','serverBuilt','serverNumber']
        avals = {}
        getAttributes(jmx, mb, '', alist, avals)
        for av in avals.values():
            bean['serverInfo'] = str(av.get('serverInfo'))
            bean['serverBuilt'] = str(av.get('serverBuilt'))
            bean['serverNumber'] = str(av.get('serverNumber'))
            bean['stateName'] = str(av.get('stateName'))
            break
        mbs = jmx.queryNames(javax.management.ObjectName('Catalina:type=Engine,*'),None)
        for m in mbs:
            mb = m
        if mb is None:
            return
        alist = ['defaultHost','backgroundProcessorDelay','baseDir']
        avals = {}
        getAttributes(jmx, mb, '', alist, avals)
        host = 'localhost'
        for av in avals.values():
            host = av.get('defaultHost')
            bean['defaultHost'] = str(av.get('defaultHost'))
            bean['baseDir'] = str(av.get('baseDir'))
            bean['backgroundProcessorDelay'] = str(av.get('backgroundProcessorDelay'))
            break
        mbs = jmx.queryNames(javax.management.ObjectName('Catalina:type=Host,*'),None)
        for m in mbs:
            mb = m
            alist = ['name','autoDeploy','deployOnStartup','unpackWARs','appBase']
            avals = {}
            getAttributes(jmx, mb, '', alist, avals)
            for av in avals.values():
                if str(av.get('name')) == host:
                    bean['autoDeploy'] = str(av.get('autoDeploy'))
                    bean['deployOnStartup'] = str(av.get('deployOnStartup'))
                    bean['unpackWARs'] = str(av.get('unpackWARs'))
                    bean['appBase'] = str(av.get('appBase'))
                break
        mbs = jmx.queryNames(javax.management.ObjectName('java.lang:type=Runtime,*'),None)
        for m in mbs:
            mb = m
        if mb is None:
            return
        alist = ['StartTime', 'VmName', 'VmVendor', 'VmVersion', 'Uptime', 'Name']
        avals = {}
        getAttributes(jmx, mb, '', alist, avals)
        for av in avals.values():
            bean['StartTime'] = str(av.get('StartTime'))
            bean['VmName'] = str(av.get('VmName'))
            bean['serverNumber'] = str(av.get('serverNumber'))
            bean['VmVendor'] = str(av.get('VmVendor'))
            bean['VmVersion'] = str(av.get('VmVersion'))
            bean['Uptime'] = FormatTime(float(av.get('Uptime')/1000))
            bean['Name'] = str(av.get('Name'))
            break
    except javax.management.RuntimeOperationsException as e:
        bt = str(e)
        exc_type, exc_value, exc_tb = sys.exc_info()
        for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
            bt += "\n%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname)
        print(bt)
        print(exc_type)
        print(exc_value)

def cib_connector(jmx, metric, bean):
    try:
        vals = []
        mbs = jmx.queryNames(javax.management.ObjectName('Catalina:type=Connector,*'),None)
        for m in mbs:
            mb = m
            ss = str(m.getCanonicalKeyPropertyListString())
            ss = ss.replace('Connector','ProtocolHandler')
            alist = ['scheme','acceptCount','enableLookups','maxThreads','connectionTimeout','keepAliveTimeout','tcpNoDelay','address','port']
            avals = {}
            getAttributes(jmx, mb, '', alist, avals)
            for av in avals.values():
                schema = cs(av.get('scheme'))
                if schema == 'http':
                    bean['nonport'] = str(av.get('port'))
                elif schema == 'https':
                    bean['sslport'] = str(av.get('port'))
                addr = av.get('address')
                if addr:
                    if str(addr).find('localhost') >= 0:
                        endp = '127.0.0.1'
                    else:
                        endp = str(addr) 
                else:
                    endp = '0.0.0.0'
                endp += ':' + str(av.get('port'))
                if not vals:
                    vals.append(dict(c1='名称',c2='端口',c3='模式',c4='DNS解析',c5='接受数',c6='最大线程',c7='TCP延迟',c8='连接超时',c9='保持活动超时',c10='压缩'))
                nm = ''
                zip = ''
                ms = jmx.queryNames(javax.management.ObjectName('Catalina:'+ss),None)
                if ms:
                    arr = jmx.getAttributes(list(ms)[0], ['name','compression'])
                    if arr:
                        nm = str(arr[0].getValue())
                        if len(arr) > 1:
                            zip = str(arr[1].getValue())
                vals.append(dict(c1=nm,c2=endp,c3=schema,c4=cs(av.get('enableLookups')),c5=cs(av.get('acceptCount')),c6=cs(av.get('maxThreads')),c7=cs(av.get('tcpNoDelay')),c8=cs(av.get('connectionTimeout')),c9=cs(av.get('keepAliveTimeout')),c10=zip))
                break
        if vals:
            metric.append(dict(index_id="2430003", content=vals))
    except javax.management.RuntimeOperationsException as e:
        bt = str(e)
        exc_type, exc_value, exc_tb = sys.exc_info()
        for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
            bt += "\n%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname)
        print(bt)
        print(exc_type)
        print(exc_value)

def cib_jdbc(jmx, metric):
    vals = []
    vals.append(dict(c1='名称',c2='连接池',c3='数据库类型',c4='驱动程序',c5='URL',c6='用户',c7='初始大小',c8='最大活跃数',c9='最小空闲数',c10='连接测试'))
    cib_jdbc1(jmx, vals)
    cib_jdbc2(jmx, vals)
    cib_jdbc3(jmx, vals)
    if len(vals) > 1:
        metric.append(dict(index_id="2430004", content=vals))

def cib_jdbc1(jmx, vals):
    try:
        mbs = jmx.queryNames(javax.management.ObjectName('com.alibaba.druid:type=DruidDataSourceStat'),None)
        for mb in mbs:
            ds = jmx.getAttribute(mb,'DataSourceList')
            for av in ds.values():
                ver = av.get('Version')
                if ver:
                    pool = 'druid ' + str(ver)
                else:
                    pool = 'druid'
                if av.get('TestOnBorrow'):
                    test = '请求'
                    if av.get('TestOnReturn'):
                        test += '返回'
                elif av.get('TestOnReturn'):
                    test = '返回'
                else:
                    test = ''
                vals.append(dict(c1=cs(av.get('Name')),c2=pool,c3=cs(av.get('DbType')),c4=cs(av.get('DriverClassName')),c5=cs(av.get('URL')),c6=cs(av.get('Username')),c7=cs(av.get('InitialSize')),c8=cs(av.get('MaxActive')),c9=cs(av.get('MinIdle')),c10=test))
            break
    except javax.management.RuntimeOperationsException as e:
        bt = str(e)
        exc_type, exc_value, exc_tb = sys.exc_info()
        for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
            bt += "\n%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname)
        print(bt)
        print(exc_type)
        print(exc_value)

def cib_jdbc2(jmx, vals):
    try:
        mbs = jmx.queryNames(javax.management.ObjectName('com.mchange.v2.c3p0:type=PooledDataSource,*'),None)
        for m in mbs:
            mb = m
            alist = ['dataSourceName','driverClass','jdbcUrl','testConnectionOnCheckout','testConnectionOnCheckin','user','Version','maxPoolSize','minPoolSize','initialPoolSize']
            avals = {}
            getAttributes(jmx, mb, '', alist, avals)
            for av in avals.values():
                url = cs(av.get('jdbcUrl'))
                dbtype = ''
                if url:
                    arr = url.split(':')
                    if len(arr) > 2 and arr[0].lower() == 'jdbc':
                        dbtype = arr[1]
                if av.get('testConnectionOnCheckout'):
                    test = '请求'
                    if av.get('testConnectionOnCheckin'):
                        test += '返回'
                elif av.get('testConnectionOnCheckin'):
                    test = '返回'
                else:
                    test = ''
                vals.append(dict(c1=cs(av.get('dataSourceName')),c2='c3p0 v2',c3=dbtype,c4=cs(av.get('driverClass')),c5=url,c6=cs(av.get('user')),c7=cs(av.get('initialPoolSize')),c8=cs(av.get('maxPoolSize')),c9=cs(av.get('minPoolSize')),c10=test))
                break
    except javax.management.RuntimeOperationsException as e:
        bt = str(e)
        exc_type, exc_value, exc_tb = sys.exc_info()
        for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
            bt += "\n%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname)
        print(bt)
        print(exc_type)
        print(exc_value)

def cib_jdbc3(jmx, vals):
    try:
        mbs = jmx.queryNames(javax.management.ObjectName('Catalina:type=DataSource,*'),None)
        for m in mbs:
            mb = m
            alist = ['Name','DriverClassName','Url','TestOnBorrow','TestOnReturn','Username','MaxActive','MinIdle','InitialSize']
            avals = {}
            getAttributes(jmx, mb, '', alist, avals)
            for av in avals.values():
                url = cs(av.get('Url'))
                dbtype = ''
                if url:
                    arr = url.split(':')
                    if len(arr) > 2 and arr[0].lower() == 'jdbc':
                        dbtype = arr[1]
                if av.get('TestOnBorrow'):
                    test = '请求'
                    if av.get('TestOnReturn'):
                        test += '返回'
                elif av.get('TestOnReturn'):
                    test = '返回'
                else:
                    test = ''
                vals.append(dict(c1=cs(av.get('Name')),c2='Tomcat',c3=dbtype,c4=cs(av.get('DriverClassName')),c5=url,c6=cs(av.get('Username')),c7=cs(av.get('InitialSize')),c8=cs(av.get('MaxActive')),c9=cs(av.get('MinIdle')),c10=test))
                break
    except javax.management.RuntimeOperationsException as e:
        bt = str(e)
        exc_type, exc_value, exc_tb = sys.exc_info()
        for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
            bt += "\n%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname)
        print(bt)
        print(exc_type)
        print(exc_value)

def cib_app(jmx, metric):
    try:
        vals = []
        mgr = {}
        mbs = jmx.queryNames(javax.management.ObjectName('Catalina:type=Manager,*'),None)
        for m in mbs:
            ctx = str(m.getKeyProperty('context'))
            mgr[ctx] = m
        mbs = jmx.queryNames(javax.management.ObjectName('Catalina:j2eeType=WebModule,*'),None)
        for m in mbs:
            mb = m
            alist = ['name','path','displayName','sessionTimeout','defaultWebXml','reloadable','cookies','useHttpOnly']
            avals = {}
            getAttributes(jmx, mb, '', alist, avals)
            for av in avals.values():
                nm = str(av.get('name'))
                if av.get('cookies'):
                    if av.get('useHttpOnly'):
                        coo = 'HttpOnly'
                    else:
                        coo = '支持'
                else:
                    coo = '不支持'
                if not vals:
                    vals.append(dict(c1='名称',c2='路径',c3='显示名',c4='WebXml',c5='cookies支持',c6='会话超时',c7='可重载',c8='最大会话数',c9='最大空闲时间',c10='ID长度'))
                xas = ''
                xis = ''
                idl = ''
                if mgr.get(nm):
                    arr = jmx.getAttributes(mgr[nm], ['maxActiveSessions','maxInactiveInterval','sessionIdLength'])
                    if len(arr) == 3:
                        xas = str(arr[0].getValue())
                        xis = str(arr[1].getValue())
                        idl = str(arr[2].getValue())
                vals.append(dict(c1=nm,c2=cs(av.get('path')),c3=cs(av.get('displayName')),c4=cs(av.get('defaultWebXml')),c5=coo,c6=cs(av.get('sessionTimeout')),c7=cs(av.get('reloadable')),c8=xas,c9=xis,c10=idl))
                break
        if vals:
            metric.append(dict(index_id="2430005", content=vals))
    except javax.management.RuntimeOperationsException as e:
        bt = str(e)
        exc_type, exc_value, exc_tb = sys.exc_info()
        for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
            bt += "\n%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname)
        print(bt)
        print(exc_type)
        print(exc_value)

def initjvm():
    #print(getDefaultJVMPath())
    if not jpype.isJVMStarted():
        jpype.startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=/usr/software/knowl/wlfullclient.jar:/usr/software/knowl/RsaTool.jar", convertStrings=False)

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
    #for obj in jhash.getClass().getMethods():
    jarray = jpype.JArray(java.lang.String)([user,password])
    jhash.put (javax.management.remote.JMXConnector.CREDENTIALS, jarray);
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
    pwds = decrypt([dbInfo['target_pwd'],dbInfo['pg_pwd']])
    pwd = pwds[0]
    try:
        conn = psycopg2.connect(database=dbInfo['pg_db'], user=dbInfo['pg_usr'], password=pwds[1], host=dbInfo['pg_ip'], port=dbInfo['pg_port'])
    except psycopg2.OperationalError as e:
        if not conn is None:
            conn.close()
        print("msg=本地数据库连接失败")
        sys.exit(1)
    jmxsoc = connect(host, port, 'rmi', usr, pwd)
    jmx = jmxsoc.getMBeanServerConnection();
    gcs = ''
    mbs = jmx.queryNames(javax.management.ObjectName('java.lang:type=GarbageCollector,name=*'),None)
    for m in mbs:
        s = str(m)
        t = s.find('name=')
        if t >= 0:
            t2 = s.find(',',t)
            if t2 < 0:
                t2 = len(s)
            if gcs:
                gcs += ',' + s[t+5:t2]
            else:
                gcs = s[t+5:t2]
    metric = []
    kvs = []
    kvs2 = []
    bean = {}
    cib_basic(jmx, bean)
    cib_connector(jmx, metric, bean)
    cib_jdbc(jmx, metric)
    cib_app(jmx, metric)
    for k in bean:
        if k in CIB_BASIC:
            kvs.append(dict(name=k,value=str(bean[k])))
        if isinstance(bean[k], str):
            kvs2.append(dict(name=k,value=str(bean[k])))
    kvs.append(dict(name='GarbageCollector',value=gcs))
    metric.append(dict(index_id="2430001", value=kvs))
    metric.append(dict(index_id="2430002", value=kvs2))
    jmxsoc.close();
    print('{"cib":' + json.dumps(metric) + '}')

import sys
import traceback
import json
from collections import Iterable
import time, datetime
from datetime import date, datetime, timedelta
import psycopg2
from jpype import *
import jpype
sys.path.append('/usr/software/knowl')
import DBAIOps_logger
#import DBUtil

log = DBAIOps_logger.Logger()

target_id = None
admin = 'AdminServer'
isAdmin = False

CIB_BASIC = set([
'key',
'AdminServer',
'ServerName',
'ListenAddress',
'ListenPort',
'MiddlewareHome',
'WeblogicHome',
'WeblogicVersion',
'JavaVersion',
'JavaVMVendor',
'DomainName',
'ClusterName',
'FileName',
'AdminServerHost',
'AdminServerListenPort',
'StartupMode',
'RootDirectory',
'DomainVersion',
'LastModificationTime',
'AppDeployments',
'HeapSizeMax',
'StartupTime'
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

def getMetaInfo(jmx, obj=None):
    if not obj:
        mbs = jmx.queryNames(javax.management.ObjectName('java.lang:Location=AdminServer,type=*'),None)
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

def cib_domain(db, jmx, domain, metric, vb=True):
    vals = None
    #object = "com.bea:Name=EditService,Type=weblogic.management.mbeanservers.edit.EditServiceMBean"
    #attribute = "DomainConfiguration"
    #print(domain.getCanonicalKeyPropertyListString())
    atts = None
    try:
        alist = ['Name','AdminServerName','RootDirectory','DomainVersion','LastModificationTime','Clusters','JDBCSystemResources','JMSServers','JMSSystemResources','Servers','AppDeployments']
        avals = {}
        getAttributes(jmx, domain, '', alist, avals)
        #attribute = "ServerConfiguration"
        #srv = jmx.getAttribute(javax.management.ObjectName(object), attribute)
        if not avals:
            return None
        atts = avals['*']
        objs = atts.get('AppDeployments')
        if objs:
            ss = ''
            for app in objs:
                s = str(app.getKeyProperty('Name'))
                if ss:
                    ss += ',' + s
                else:
                    ss = s
            atts['AppDeployments'] = ss
        #if not vb:
        #    return atts
        objs = atts.get('Clusters')
        if objs:
            vals = []
            vals.append(dict(c1='名称',c2='类型',c3='地址',c4='多播地址/端口',c5='消息模式',c6='广播通道',c7='负载算法',c8='成员',c9=None,c10=None))
            for clu in objs:
                bean = {}
                cib_cluster(db, jmx, clu, bean)
                if bean:
                    s1 = bean.get('MulticastAddress')
                    s2 = bean.get('MulticastPort')
                    if s1 or s2:
                        s = str(s1) + ':' + str(s2)
                    else:
                        s = ''
                    vals.append(dict(c1=bean.get('Name'),c2=bean.get('ClusterType'),c3=bean.get('ClusterAddress'),c4=s,c5=bean.get('ClusterMessagingMode'),c6=bean.get('ClusterBroadcastChannel'),c7=bean.get('DefaultLoadAlgorithm'),c8=bean.get('ClusterServerNames'),c9=None,c10=None))
            metric.append(dict(index_id="2400003", content=vals))
        jdbs = atts.get('JDBCSystemResources')
        if jdbs:
            vals = []
            vals.append(dict(c1='名称',c2='类型',c3='驱动程序',c4='URL',c5='初始值',c6='最大值',c7='测试表',c8='测试间隔秒数',c9='全局事务',c10='JNDI名'))
            for jdbc in jdbs:
                bean = {}
                cib_jdbc(db, jmx, jdbc, bean)
                if bean:
                    vals.append(dict(c1=bean.get('Name'),c2=bean.get('DatasourceType'),c3=bean.get('DriverName'),c4=bean.get('Url'),c5=bean.get('InitialCapacity'),c6=bean.get('MaxCapacity'),c7=bean.get('TestTableName'),c8=bean.get('TestFrequencySeconds'),c9=bean.get('GlobalTransactionsProtocol'),c10=bean.get('JNDINames')))
            metric.append(dict(index_id="2400005", content=vals))
        srvs = atts.get('Servers')
        if srvs:
            vals = []
            vals.append(dict(c1='名称',c2='监听地址',c3='监听端口',c4='集群',c5='日志文件名',c6=None,c7=None,c8=None,c9=None,c10=None))
            for srv in srvs:
                bean = {}
                cib_srv(db, jmx, srv, bean)
                if bean:
                    vals.append(dict(c1=bean.get('ServerName'),c2=bean.get('ListenAddress'),c3=bean.get('ListenPort'),c4=bean.get('ClusterName'),c5=bean.get('FileName'),c6=None,c7=None,c8=None,c9=None,c10=None))
            metric.append(dict(index_id="2400004", content=vals))
        return atts
    except Exception as e:
        bt = str(e)
        exc_type, exc_value, exc_tb = sys.exc_info()
        for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
            bt += "\n%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname)
        #print(bt)
        #print(exc_type)
        #print(exc_value)
        log.error('cib_domain[%s]:%s' % (target_id,bt))
        return atts
    #object = "java.lang:type=Memory"
    #attribute = "HeapMemoryUsage"
    #attr = jmx.getAttribute(javax.management.ObjectName(object),attribute)
    #print(attr.get('committed'))

def cib_server(db, jmx, server, server2, bean):
    vals = None
    try:
        cib_srv2(db, jmx, server2, bean)
        cib_srv(db, jmx, server, bean)
    except Exception as e:
        bt = str(e)
        exc_type, exc_value, exc_tb = sys.exc_info()
        for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
            bt += "\n%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname)
        #print(bt)
        #print(exc_type)
        #print(exc_value)
        log.error('cib_server[%s]:%s' % (target_id,bt))
    metric.append(dict(index_id="2220001", value=vals))

def cib_cluster(db, jmx, cluster, bean):
    try:
        if not jmx.isRegistered(cluster):
            return
        alist = ['Name','ClusterAddress','ClusterBroadcastChannel','ClusterMessagingMode','ClusterType','DefaultLoadAlgorithm','MulticastAddress','MulticastPort','Servers']
        avals = {}
        getAttributes(jmx, cluster, '', alist, avals)
        if avals:
            atts = avals['*']
            for a in atts:
                if a == 'Servers':
                    ss = ''
                    for v in atts[a]:
                        s = str(v.getKeyProperty('Name'))
                        if ss:
                            ss += ',' + s
                        else:
                            ss = s
                    bean['ClusterServerNames'] = ss
                else: 
                    bean[a] = cs(atts[a]) 
    except Exception as e:
        bt = str(e)
        exc_type, exc_value, exc_tb = sys.exc_info()
        for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
            bt += "\n%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname)
        #print(bt)
        #print(exc_type)
        #print(exc_value)
        log.error('cib_cluster[%s]:%s' % (target_id,bt))

def cib_jdbc(db, jmx, jdbc, bean):
    if not jmx.isRegistered(jdbc):
        return
    alist = ['DescriptorFileName','JDBCResource']
    avals = {}
    getAttributes(jmx, jdbc, '', alist, avals)
    v = avals['*']
    if v:
        obj = v.get("JDBCResource")
        vs = jmx.getAttributes(obj, jpype.JArray(java.lang.String)(['Name','DatasourceType']))
        if vs and vs[0]:
            name = str(vs[0].getValue())
        else:
            name = ''
        bean['Name'] = name
        if len(vs) > 1 and vs[1]:
            typ = str(vs[1].getValue())
        else:
            typ = ''
        bean['DatasourceType'] = typ
        alist = ['Name','DriverName','Url','Properties']
        avals = {}
        getAttributes(jmx, obj, 'JDBCDriverParams', alist, avals)
        if avals:
            v = avals.get('JDBCDriverParams=1')
            if v:
                bean['DriverName'] = str(v.get('DriverName'))
                bean['Url'] = str(v.get('Url'))
                o = v.get("Properties")
                alist = ['Name','Value']
                avals = {}
                getAttributes(jmx, o, 'Properties', alist, avals)
        alist = ['ConnectionReserveTimeoutSeconds','InitialCapacity','MaxCapacity','MinCapacity','StatementCacheSize','TestTableName','InitSql','SecondsToTrustAnIdlePoolConnection','TestFrequencySeconds']
        avals = {}
        getAttributes(jmx, obj, 'JDBCConnectionPoolParams', alist, avals)
        if avals:
            atts = avals['JDBCConnectionPoolParams=1']
            for a in atts:
                bean[a] = str(atts[a])
        alist = ['JNDINames','GlobalTransactionsProtocol','RowPrefetchSize','Scope','StreamChunkSize','AlgorithmType','DataSourceList']
        avals = {}
        getAttributes(jmx, obj, 'JDBCDataSourceParams', alist, avals)
        if avals:
            atts = avals['JDBCDataSourceParams=1']
            for a in atts:
                if a == 'JNDINames':
                    ss = ''
                    #js = v.get("JNDINames")
                    js = atts[a]
                    for s in js:
                        if ss:
                            ss += ',' + str(s)
                        else:
                            ss = str(s)
                    bean['JNDINames'] = ss
                else:
                    bean[a] = str(atts[a])
        alist = ['XaTransactionTimeout']
        avals = {}
        getAttributes(jmx, obj, 'JDBCXAParams', alist, avals)
        if avals:
            v = avals.get('JDBCXAParams=1')
            if v:
                bean['XaTransactionTimeout'] = str(v.get("XaTransactionTimeout"))

def cib_app(db, jmx, app, bean):
    if not jmx.isRegistered(app):
        return
    comps = jmx.getAttribute(app, 'ComponentRuntimes')
    if comps:
        t1 = 0
        t2 = 0
        t3 = 0
        for comp in comps:
            typ = str(jmx.getAttribute(comp,'Type'))
            t = typ.find('ComponentRuntime')
            if t > 0:
                typ = typ[0:t]
            if typ != 'JDBCDataSourceRuntime' and typ != 'Connector':
                if typ == 'WebApp':
                    t1 += 1
                elif typ == 'EJB':
                    t2 += 1
                else:
                    t3 += 1
        if t1 > 0:
            ss = 'WebApp'
        else:
            ss = ''
        if t2 > 0:
            if ss:
                ss += ',EJB'
            else:
                ss = 'EJB'
        if t3 > 0:
            if ss:
                ss += ',其它'
            else:
                ss = '其它'
        if ss:
            bean['Components'] = ss
        else:
            return
    alist = ['ApplicationName','ApplicationVersion','ActiveVersionState','HealthState']
    avals = {}
    getAttributes(jmx, app, '', alist, avals)
    if avals:
        atts = avals['*']
        for a in atts:
            if a == 'HealthState':
                bean[a] = str(atts[a].getState())
            else:
                bean[a] = str(atts[a])

def cib_srv(db, jmx, server, bean):
    if not jmx.isRegistered(server):
        return
    alist = ['Name','ListenAddress','ListenPort','AcceptBacklog','Cluster','StagingDirectoryName','UploadDirectoryName','DefaultProtocol','StuckThreadMaxTime','MaxOpenSockCount','IdleConnectionTimeout','MaxMessageSize','SocketReaders','StuckThreadTimerInterval','CompleteWriteTimeout','CompleteMessageTimeout','StartupMode']
    avals = {}
    getAttributes(jmx, server, '', alist, avals)
    if avals:
        atts = avals['*']
        for a in atts:
            if a == 'Cluster':
                s = atts[a].getKeyProperty('Name')
                bean['ClusterName'] = str(s)
                if not isAdmin:
                    b = {}
                    cib_cluster(db, jmx, atts[a], b)
                    atts['Cluster'] = b
                else:
                    atts['Cluster'] = None
            else:
                if a == 'Name':
                    bean['ServerName'] = str(atts[a])
                else:
                    bean[a] = str(atts[a])
    alist = ['FileName','DateFormatPattern','LogFileRotationDir']
    avals = {}
    getAttributes(jmx, server, 'Log', alist, avals)
    if avals:
        atts = avals['Log=1']
        for a in atts:
            bean[a] = str(atts[a])
    alist = ['PostTimeoutSecs','WriteChunkBytes','DefaultWebAppContextRoot','KeepAliveSecs','MaxPostSize','MaxPostTimeSecs']
    avals = {}
    getAttributes(jmx, server, 'WebServer=%s' % bean['ServerName'], alist, avals)
    if avals:
        atts = avals['WebServer=%s' % bean['ServerName']]
        for a in atts:
            bean[a] = str(atts[a])

def cib_srv2(db, jmx, server, bean):
    if not jmx.isRegistered(server):
        return
    alist = ['CurrentDirectory','CurrentMachine','MiddlewareHome','RequestClassRuntimes','State','DefaultURL','WeblogicHome','WeblogicVersion','AdminServerHost','AdminServerListenPort','AdministrationURL']
    avals = {}
    getAttributes(jmx, server, '', alist, avals)
    if avals:
        atts = avals['*']
        for a in atts:
            #if a == 'OverallHealthStateJMX':
            #    v = atts[a].getAll(jpype.JArray(java.lang.String)(['Component','HealthState','IsCritical','MBean','ReasonCode']))
            #    bean['HealthState'] = str(v[1])
            bean[a] = str(atts[a])
    #alist = ['HeapFreeCurrent','HeapFreePercent','HeapSizeCurrent','HeapSizeMax','JavaVendor','JavaVersion','JavaVMVendor','OSName','OSVersion','Uptime']
    alist = ['HeapSizeCurrent','HeapSizeMax','JavaVendor','JavaVersion','JavaVMVendor','OSName','OSVersion','Uptime']
    avals = {}
    getAttributes(jmx, server, 'JVMRuntime', alist, avals)
    if avals:
        atts = avals['JVMRuntime=1']
        for a in atts:
            if a == 'Uptime':
                bt = datetime.fromtimestamp(time.time() - int(atts[a])/1000)
                bean['StartupTime'] = cs(bt, True)
            else:
                bean[a] = str(atts[a])
    #print(bean)

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
    if type == 'rmi':
        URL = "service:jmx:rmi:///jndi/rmi://%s:%s/jmxrmi" % (ip, port)
    elif type == 'domain':
        URL = "service:jmx:t3://%s:%s/jndi/weblogic.management.mbeanservers.domainruntime" % (ip, port)
    else:
        URL = "service:jmx:t3://%s:%s/jndi/weblogic.management.mbeanservers.%s" % (ip, port, type)
    jhash = java.util.HashMap()
    #for obj in jhash.getClass().getMethods():
    jarray = jpype.JArray(java.lang.String)([user,password])
    jhash.put (javax.management.remote.JMXConnector.CREDENTIALS, jarray);
    jhash.put (javax.management.remote.JMXConnectorFactory.PROTOCOL_PROVIDER_PACKAGES, 'weblogic.management.remote');
    jmxurl = javax.management.remote.JMXServiceURL(URL)
    jmxsoc = javax.management.remote.JMXConnectorFactory.connect(jmxurl, jhash)
    return jmxsoc 

def mgt_wls(db, sid, key, adm):
    sql = "select reserver2,subuid from mgt_system where uid='%s'" % target_id
    result = relate_pg2(db, sql)
    if result.code == 0:
        if len(result.msg) == 1 and result.msg[0][0] == sid:
            id = ''
        else:
            id = sid
        if len(result.msg) == 0:
            raise IndexError(sql)
        uid = result.msg[0][1]
    else:
        return -1
    sql = "select target_id from p_oracle_cib where index_id=2400001 and cib_name='key' and cib_value='%s' limit 1" % key
    result = relate_pg2(db, sql)
    if result.code == 0:
        if len(result.msg) == 1 and target_id != result.msg[0][0]:
            return 1
    else:
        return -1
    if key != adm:
        aid = None
        sql = "select target_id from p_oracle_cib where index_id=2400001 and cib_name='key' and cib_value='%s' limit 1" % adm
        result = relate_pg2(db, sql)
        if result.code == 0:
            if len(result.msg) == 1:
                aid = result.msg[0][0]
        else:
            return -1
    else:
        aid = target_id
    if id or (uid != aid and aid):
        if id:
            ss = "reserver2='%s'" % id
        else:
            ss = ''
        if uid != aid and aid:
            if ss:
                ss += ",subuid='%s'" % aid
            else:
                ss = "subuid='%s'" % aid
        cur = db.cursor()
        sql = "update mgt_system set %s where uid='%s'" % (ss, target_id)
        cur.execute(sql)
        db.commit()
    return 0

if __name__ == '__main__':
    dbInfo = eval(sys.argv[1])
    usr = dbInfo['target_usr']
    host = dbInfo['target_ip']
    port = dbInfo['target_port']
    target_id = dbInfo['targetId']
    sid = dbInfo['target_inst']
    initjvm()
    pwds = decrypt([dbInfo['target_pwd'],dbInfo['pg_pwd']])
    #pwds = [dbInfo['target_pwd'],dbInfo['pg_pwd']]
    pwd = pwds[0]
    conn = None
    try:
        conn = psycopg2.connect(database=dbInfo['pg_db'], user=dbInfo['pg_usr'], password=pwds[1], host=dbInfo['pg_ip'], port=dbInfo['pg_port'])
    except psycopg2.OperationalError as e:
        if not conn is None:
            conn.close()
        print("msg=本地数据库连接失败")
        sys.exit(1)
    #jmxsoc = connect('60.60.60.165', 7001, 'runtime', 'weblogic', 'weblogic1')
    if usr and usr[0] == '+':
        jmxsoc = connect(host, port, 'rmi', usr[1:], pwd)
    else:
        jmxsoc = connect(host, port, 'runtime', usr, pwd)
    jmx = jmxsoc.getMBeanServerConnection();
    server = None
    server2 = None
    domain = None
    object = "com.bea:Name=RuntimeService,Type=weblogic.management.mbeanservers.runtime.RuntimeServiceMBean"
    sn = str(jmx.getAttribute(javax.management.ObjectName(object), 'ServerName'))
    domain = jmx.getAttribute(javax.management.ObjectName(object), 'DomainConfiguration')
    if domain:
        admin = str(jmx.getAttribute(domain, 'AdminServerName'))
    else:
        admin = 'AdminServer'
    gcs = ''
    if not sid:
        sid = sn
    if sn == admin and (not usr or usr[0] != '+') and sid != admin:
        jmxsoc.close();
        jmxsoc = connect(host, port, 'domain', usr, pwd)
        jmx = jmxsoc.getMBeanServerConnection()
        object = "com.bea:Name=DomainRuntimeService,Type=weblogic.management.mbeanservers.domainruntime.DomainRuntimeServiceMBean" 
        srvs = jmx.getAttribute(javax.management.ObjectName(object), 'ServerRuntimes')
        for srv in srvs:
            s = str(jmx.getAttribute(srv, 'Name'))
            if s.upper() == sid.upper():
                if s != sid:
                     print("msg=ServerName应该是%s,大小写不一致" % s)
                     sys.exit(1)
                server = srv
                mbs = jmx.queryNames(javax.management.ObjectName('java.lang:Location=%s,type=GarbageCollector,name=*' % sid),None)
                for m in mbs:
                    s = str(m)
                    t = s.find('name=')
                    if t > 0:
                        t2 = s.find(',',t)
                        if t2 < 0:
                            t2 = len(s)
                        if gcs:
                            gcs += ',' + s[t+5:t2]
                        else:
                            gcs = s[t+5:t2]
                domain = jmx.getAttribute(javax.management.ObjectName(object), 'DomainConfiguration')
                svs = jmx.getAttribute(domain, 'Servers')
                for sv in svs:
                    s = str(jmx.getAttribute(sv, 'Name'))
                    if s == sid:
                        server2 = sv
                isAdmin = False
                break
        if not server:
            print("msg=该应用服务器[%s]不存在或未运行" % sid)
            sys.exit(1)
    else:
        if sn != sid:
            print("msg=连接的ServerName应该是%s,和配置的值[%s]不一致" % (sn,sid))
            sys.exit(1)
        object = "com.bea:Name=RuntimeService,Type=weblogic.management.mbeanservers.runtime.RuntimeServiceMBean"
        server = jmx.getAttribute(javax.management.ObjectName(object), 'ServerRuntime')
        server2 = jmx.getAttribute(javax.management.ObjectName(object), 'ServerConfiguration')
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
        #domain = jmx.getAttribute(javax.management.ObjectName(object), 'DomainConfiguration')
        isAdmin = sid == admin
    #pg = DBUtil.get_pg_env_test()
    #object = "java.lang:type=Memory"
    #object = "java.lang:Location=AdminServer,type=Memory"
    #attribute = "HeapMemoryUsage"
    #attr = jmx.getAttribute(javax.management.ObjectName(object),attribute)
    #print(attr.get('committed'))
    metric = []
    kvs = []
    kvs2 = []
    bean = {}
    cib_server(conn, jmx, server2, server, bean)
    s1 = bean.get('ListenAddress')
    s2 = bean.get('ListenPort')
    s3 = bean.get('AdminServerHost')
    s4 = bean.get('AdminServerListenPort')
    if not s1:
        s1 = host
    ss1 = cs(s1) + ':' + cs(s2) + '/' + sn
    ss2 = cs(s3) + ':' + cs(s4) + '/' + admin
    ret = mgt_wls(conn, sid, ss1, ss2)
    if ret != 0:
        if ret == 1:
            print("msg=该应用服务器对象[%s]已存在" % sid)
        else:
            print("msg=本地数据库访问失败")
        sys.exit(1)
    bean['key'] = ss1
    bean['AdminServer'] = ss2
    for k in bean:
        if k == 'Cluster' and bean[k]:
            c = bean[k]
            s1 = c.get('MulticastAddress')
            s2 = c.get('MulticastPort')
            if s1 or s2:
                s = str(s1) + ':' + str(s2)
            else:
                s = ''
            vals = []
            #vals.append(dict(c1='',c2='',c3='',c4='',c5='',c6='',c7='',c8='',c9='',c10=''))
            vals.append(dict(c1='名称',c2='类型',c3='地址',c4='多播地址/端口',c5='消息模式',c6='广播通道',c7='负载算法',c8='成员',c9=None,c10=None))
            vals.append(dict(c1=c.get('Name'),c2=c.get('ClusterType'),c3=c.get('ClusterAddress'),c4=s,c5=c.get('ClusterMessagingMode'),c6=c.get('ClusterBroadcastChannel'),c7=c.get('DefaultLoadAlgorithm'),c8=c.get('ClusterServerNames'),c9=None,c10=None))
            metric.append(dict(index_id="2400003", content=vals))
        else:
            if k in CIB_BASIC:
                kvs.append(dict(name=k,value=str(bean[k])))
            if isinstance(bean[k], str):
                kvs2.append(dict(name=k,value=str(bean[k])))
    apps = jmx.getAttribute(server, 'ApplicationRuntimes')
    if apps:
        vals = []
        vals.append(dict(c1='名称',c2='版本',c3='版本状态',c4='健康状态',c5='组件类型',c6=None,c7=None,c8=None,c9=None,c10=None))
        for v in apps:
            bean = {}
            cib_app(conn, jmx, v, bean)
            if bean:
                s = bean.get('ActiveVersionState')
                if s:
                    if int(s) < 3:
                        s1 = ['INACTIVE','ACTIVE','ACTIVE_ADMIN'][int(s)]
                    else:
                        s1 = 'STATE_%s' % s
                else:
                    s1 = None
                s = bean.get('HealthState')
                if s:
                    if int(s) < 5:
                        s2 = ['OK','WARN','CRITICAL','FAILED','OVERLOADED'][int(s)]
                    else:
                        s2 = 'STATE_%s' % s
                else:
                    s2 = None
                vals.append(dict(c1=bean.get('ApplicationName'),c2=bean.get('ApplicationVersion'),c3=s1,c4=s2,c5=bean.get('Components'),c6=None,c7=None,c8=None,c9=None,c10=None))
        metric.append(dict(index_id="2400006", content=vals))
    atts = cib_domain(conn, jmx, domain, metric, isAdmin)
    if atts:
        for k in atts:
            if k == 'Name':
                kvs.append(dict(name='DomainName',value=str(atts[k])))
                kvs2.append(dict(name='DomainName',value=str(atts[k])))
            else:
                if k in CIB_BASIC:
                    kvs.append(dict(name=k,value=str(atts[k])))
                #if isinstance(atts[k], str):
                kvs2.append(dict(name=k,value=str(atts[k])))
    kvs.append(dict(name='GarbageCollector',value=gcs))
    metric.append(dict(index_id="2400001", value=kvs))
    metric.append(dict(index_id="2400002", value=kvs2))
    jmxsoc.close();
    print('{"cib":' + json.dumps(metric) + '}')

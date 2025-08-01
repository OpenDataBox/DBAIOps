import json
import sys
import time
from datetime import datetime
import psycopg2
import jpype
from jpype import *

sys.path.append('/usr/software/knowl')
import DBUtil
import JavaUtil
import JavaRsa
from CommUtil import FormatTime

CIB_BASIC = set([
'StartTime', 'VmName', 'VmVendor', 'VmVersion', 'Name', 'SpecVersion', 'InputArguments', 'GarbageCollector',
'NNRole',
'ClusterId',
'BlockPoolId',
'Hostname',
'Endpoint',
'SoftwareVersion'
])

nsp = []
nodes = []
jour = []
dirs = {}

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

def cs(val, dt=False):
    if val is None:
        return ''
    else:
        if dt:
            return val.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return str(val)

def table_append(tab_list, vals):
    cs = {}
    l = len(vals)
    for i in range(10):
        if i < l:
            cs['c%d'%(i+1)] = vals[i]
        else:
            cs['c%d'%(i+1)] = None
    tab_list.append(cs)

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

def idx_jvm(jmx, bean):
    mbs = jmx.queryNames(javax.management.ObjectName('java.lang:type=GarbageCollector,name=*'),None)
    gcs = ''
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
    bean['GarbageCollector'] = gcs
    mb = javax.management.ObjectName('java.lang:type=Runtime')
    alist = ['StartTime', 'VmName', 'VmVendor', 'VmVersion', 'Uptime', 'Name', 'SpecVersion']
    vvv = jmx.getAttributes(mb, alist)
    for vv in vvv:
        if str(vv.getName()) == 'StartTime':
            tm = vv.getValue()
            if tm:
                bean['StartTime'] = str(datetime.fromtimestamp(int(tm/1000)))
        else:
            bean[str(vv.getName())] = cs(vv.getValue())
    bean['Uptime'] = FormatTime(float(bean['Uptime'])/1000)

def idx_nnst(jmx, bean):
    try:
        mb = javax.management.ObjectName('Hadoop:service=NameNode,name=NameNodeStatus')
        alist = ['NNRole',
'HostAndPort',
'SecurityEnabled',
'LastHATransitionTime',
'State']
        vvv = jmx.getAttributes(mb, alist)
        for vv in vvv:
            if vv:
                nm = str(vv.getName())
                if nm == 'HostAndPort':
                    vs = cs(vv.getValue()).split(':')
                    bean['Hostname'] = vs[0]
                    if vs[1]:
                        bean['RpcPort'] = vs[1]
                else:
                    bean[str(vv.getName())] = cs(vv.getValue())
    except javax.management.RuntimeOperationsException as e:
        bt = str(e)
        exc_type, exc_value, exc_tb = sys.exc_info()
        for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
            bt += "\n%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname)
        print(bt)
        print(exc_type)
        print(exc_value)

def idx_blkst(jmx, bean):
    try:
        mb = javax.management.ObjectName('Hadoop:service=NameNode,name=BlockStats')
        alist = ['StorageTypeStats']
        vvv = jmx.getAttributes(mb, alist)
        for vv in vvv:
            if vv:
                vals = vv.getValue()
                if vals:
                    #for kv in vals.entrySet():
                    for vs in vals.values():
                        if vs:
                            k = vs.get('key')
                            v = vs.get('value')
                            n1 = v.get('blockPoolUsed')
                            n2 = v.get('capacityNonDfsUsed')
                            n3 = v.get('capacityTotal')
                            n4 = v.get('capacityUsed')
                            n5 = v.get('nodesInService')
                            bean['StorageType'] = str(k)
    except javax.management.RuntimeOperationsException as e:
        bt = str(e)
        exc_type, exc_value, exc_tb = sys.exc_info()
        for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
            bt += "\n%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname)
        print(bt)
        print(exc_type)
        print(exc_value)

def idx_nninfo(jmx, bean):
    global nsp

    try:
        mb = javax.management.ObjectName('Hadoop:service=NameNode,name=NameNodeInfo')
        alist = ['ClusterId',
'Safemode',
'Total',
'Used',
'Free',
'NonDfsUsedSpace',
'PercentUsed',
'BlockPoolUsedSpace',
'PercentBlockPoolUsed',
'PercentRemaining',
'TotalBlocks',
'NumberOfMissingBlocks',
'BlockPoolId',
'NameDirSize',
'NameDirStatuses',
'NameJournalStatus',
'JournalTransactionInfo',
#'NodeUsage',
'BlockPoolUsedSpace',
'PercentBlockPoolUsed',
'NNStarted',
'NNStartedTimeInMillis',
'CompileInfo',
'LiveNodes',
#'DistinctVersionCount',
#'DeadNodes',
#'DecomNodes',
'SoftwareVersion']
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
                        nodes.append([k.split(':')[0],cs(n.get('infoAddr')).split(':')[0],n.get('adminState'),n.get('capacity'),n.get('used'),n.get('nonDfsUsedSpace'),n.get('numBlocks'),n.get('blockPoolUsed'),n.get('volfails')])
            elif nm == 'NameDirSize':
                ln = json.loads(str(vv.getValue()))
                if ln:
                    for k in ln.keys():
                        dirs[k] = [k, ln[k], None, None]
            elif nm == 'NameDirStatuses':
                ln = json.loads(str(vv.getValue()))
                if ln:
                    ls = ln.get('active')
                    if ls:
                        for k in ls.keys():
                            if dirs.get(k):
                                dirs[k][2] = ls[k]
                                dirs[k][3] = 'Active'
            elif nm == 'NameJournalStatus':
                ln = json.loads(str(vv.getValue()))
                if ln:
                    for vs in ln:
                        jour.append([vs.get('manager'),vs.get('stream'),vs.get('disabled'),vs.get('required')])
            elif nm == 'JournalTransactionInfo':
                ln = json.loads(str(vv.getValue()))
                if ln:
                    v = ln.get('MostRecentCheckpointTxId')
                    if v:
                        bean['MostRecentCheckpointTxId'] = cs(v)
                    v = ln.get('LastAppliedOrWrittenTxId')
                    if v:
                        bean['LastAppliedOrWrittenTxId'] = cs(v)
            else:
                bean[nm] = cs(vv.getValue())
        nsp = [bean.get('BlockPoolId'),bean.get('Total'),bean.get('Used'),bean.get('NonDfsUsedSpace'),bean.get('PercentUsed'),bean.get('PercentRemaining'),bean.get('BlockPoolUsedSpace'),bean.get('PercentBlockPoolUsed'),bean.get('TotalBlocks'),bean.get('NumberOfMissingBlocks')]
        del bean['Total']
        del bean['Used']
        del bean['NonDfsUsedSpace']
        del bean['PercentUsed']
        del bean['PercentRemaining']
        del bean['BlockPoolUsedSpace']
        del bean['PercentBlockPoolUsed']
        del bean['TotalBlocks']
        del bean['NumberOfMissingBlocks']
        del bean['Free']
    except javax.management.RuntimeOperationsException as e:
        bt = str(e)
        exc_type, exc_value, exc_tb = sys.exc_info()
        for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
            bt += "\n%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname)
        print(bt)
        print(exc_type)
        print(exc_value)

def idx_dninfo(jmx, bean):
    try:
        mb = javax.management.ObjectName('Hadoop:service=DataNode,name=DataNodeInfo')
        alist = ['ClusterId',
'RpcPort',
'DataPort',
'NamenodeAddresses',
'DatanodeHostname',
#'BPServiceActorInfo',
'SoftwareVersion',
'VolumeInfo']
        vvv = jmx.getAttributes(mb, alist)
        for vv in vvv:
            nm = str(vv.getName())
            if nm == 'NamenodeAddresses':
                v = json.loads(str(vv.getValue()))
                s = ''
                for k in v.values():
                    if s:
                        s += ',' + k
                    else:
                        s = k
                bean['BlockPoolId'] = s
            elif nm == 'VolumeInfo':
                v = json.loads(str(vv.getValue()))
                for k in v.keys():
                    vols.append([bean.get('Hostname'),k,v[k].get('numBlocks'),v[k].get('usedSpace'),v[k].get('freeSpace'),v[k].get('reservedSpace'),v[k].get('storageType')])
            elif nm == 'DatanodeHostname':
                bean['Hostname'] = cs(vv.getValue())
            else:
                bean[nm] = cs(vv.getValue())
    except javax.management.RuntimeOperationsException as e:
        bt = str(e)
        exc_type, exc_value, exc_tb = sys.exc_info()
        for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
            bt += "\n%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname)
        print(bt)
        print(exc_type)
        print(exc_value)

def idx_dnfsds(jmx, bean):
    try:
        mb = javax.management.ObjectName('Hadoop:service=DataNode,name=FSDatasetState')
        alist = ['Capacity',
'tag.StorageInfo',
'DfsUsed',
'Remaining',
'NumFailedVolumes']
        vvv = jmx.getAttributes(mb, alist)
        for vv in vvv:
            if vv:
                bean[str(vv.getName())] = cs(vv.getValue())
        if bean.get('RpcPort') and bean.get('DatanodeHostname'):
            bean['HostAndPort'] = bean['DatanodeHostname'] + ':' + bean['RpcPort']
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

def get_hdfs_info(pg, target_id, metric):
    #sql = "select cib_value from p_normal_cib where index_id=1000001 and cib_name='members' and target_id='%s'" % target_id
    #result = relate_pg2(pg, sql)
    #if result.code != 0 or len(result.msg) == 0 or not result.msg[0][0]:
    #    return
    #bs = set(result.msg[0][0].split(','))
    bs = set()
    bs.add(target_id)
    sql = "select uid,ip,port,username,password from mgt_system where uid in %s and use_flag" % (tuple2(bs))
    result = relate_pg2(pg, sql)
    ns = set()
    hosts = []
    usr = ''
    pwd = ''
    uid = None
    if result.code == 0:
        for row in result.msg:
            ns.add(row[0])
            if hosts:
                hosts.append([row[1],row[2]])
            else:
                uid = row[0]
                hosts.append([row[1],row[2]])
                usr = row[3]
                pwd = row[4]
                if usr and pwd:
                    pwd = JavaUtil.decrypt(pwd)
    if ns != bs:
        return

    ct = time.time()
    jmxsoc = connect(hosts[0][0], hosts[0][1], 'rmi', usr, pwd)
    jmx = jmxsoc.getMBeanServerConnection()
    typ = -1
    mbs = jmx.queryNames(javax.management.ObjectName('Hadoop:service=NameNode,name=*'),None)
    if mbs:
        typ = 0
    else:
        mbs = jmx.queryNames(javax.management.ObjectName('Hadoop:service=DataNode,name=*'),None)
        if mbs:
            typ = 1
    if typ != 0:
        print("msg=对象类型非NameNode")
        sys.exit(1)
    bean = {}
    idx_jvm(jmx, bean)
    idx_nnst(jmx, bean)
    idx_nninfo(jmx, bean)
    #idx_blkst(jmx, bean)
    jmxsoc.close()
    kvs = []
    kvs2 = []
    rpc = bean.get('RpcPort')
    if rpc:
        bean['Endpoint'] = hosts[0][0] + ':' + rpc
    for k in bean:
        if k in CIB_BASIC:
            kvs.append(dict(name=k,value=cs(bean[k])))
        if isinstance(bean[k], str):
            kvs2.append(dict(name=k,value=cs(bean[k])))
    metric.append(dict(index_id="5040001", value=kvs))
    metric.append(dict(index_id="5040002", value=kvs2))
    if nsp:
        vals = []
        table_append(vals, ['块池ID','总容量','已用容量','非dfs空间','使用率','剩余率','已用块池','块池使用率','总块数','丢失块数'])
        table_append(vals, nsp)
        metric.append(dict(index_id="5040003", content=vals))
    if nodes:
        vals = []
        table_append(vals, ['主机名','IP地址','状态','容量','已使用','非dfs空间','块数','已用块池','失败卷数'])
        for n in nodes:
            table_append(vals, n)
        metric.append(dict(index_id="5040004", content=vals))
    if dirs:
        vals = []
        table_append(vals, ['路径','大小','类型','状态'])
        for n in dirs.values():
            table_append(vals, n)
        metric.append(dict(index_id="5040006", content=vals))
    if jour:
        vals = []
        table_append(vals, ['管理','流','失效','需要'])
        for n in jour:
            table_append(vals, n)
        metric.append(dict(index_id="5040007", content=vals))
    cluster_id = bean['ClusterId']
    sql = "update mgt_system set subuid='%s' where uid in %s and (subuid is null or subuid<>'%s') and use_flag" % (cluster_id, tuple2(bs), cluster_id)
    cur = pg.conn.cursor()
    cur.execute(sql)
    pg.conn.commit()

def main(pg, target_id):
    metric = []
    get_hdfs_info(pg, target_id, metric)
    #metric.append(dict(index_id=5040001, value=vals))
    print('{"cib":' + json.dumps(metric) + '}')

if __name__ == '__main__':
    dbInfo = eval(sys.argv[1])
    initjvm()
    pg, target_id = JavaUtil.get_pg_env(dbInfo, 0)
    main(pg, target_id)

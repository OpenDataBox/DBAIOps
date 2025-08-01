import json
import sys
import traceback
import time
from datetime import datetime
import psycopg2
from jpype import *

sys.path.append('/usr/software/knowl')
# import DBUtil
import JavaUtil
import JavaRsa
from CommUtil import FormatTime
import HttpJmxUtil
from HttpJmxUtil import HttpJmx

OLD_GC = {'MarkSweepCompact', 'PS MarkSweep', 'ConcurrentMarkSweep',
          'Garbage collection optimized for short pausetimes Old Collector',
          'Garbage collection optimized for throughput Old Collector',
          'Garbage collection optimized for deterministic pausetimes Old Collector'}

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
vols = []
jour = []
dirs = {}

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

def table_append(tab_list, vals):
    cs = {}
    l = len(vals)
    for i in range(10):
        if i < l:
            cs['c%d'%(i+1)] = vals[i]
        else:
            cs['c%d'%(i+1)] = None
    tab_list.append(cs)

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

def idx_jvm(jmx, bean):
    if isinstance(jmx, HttpJmx):
        mbs = jmx.queryNames('java.lang:type=GarbageCollector,name=*',None)
    else:
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
    if isinstance(jmx, HttpJmx):
        mb = 'java.lang:type=Runtime'
    else:
        mb = javax.management.ObjectName('java.lang:type=Runtime')
    alist = ['StartTime', 'VmName', 'VmVendor', 'VmVersion', 'Uptime', 'Name', 'SpecVersion', 'SystemProperties', 'InputArguments']
    vvv = jmx.getAttributes(mb, alist)
    for vv in vvv:
        if isinstance(jmx, HttpJmx):
            nm = vv[0]
            vu = vv[1]
        else:
            nm = str(vv.getName())
            vu = vv.getValue()
        if nm == 'StartTime':
            tm = float(vu)
            if tm:
                bean['StartTime'] = str(datetime.fromtimestamp(int(tm/1000)))
        elif nm == 'SystemProperties':
            if isinstance(jmx, HttpJmx):
                vals = vu
            else:
                vals = vu.values()
            for val in vals:
                k = str(val.get('key'))
                if k in ['hadoop.log.dir', 'hadoop.log.file', 'hadoop.id.str']:
                    bean[k] = cs(val.get('value'))
        else:
            bean[nm] = cs(vu)
    bean['Uptime'] = FormatTime(float(bean['Uptime'])/1000)

def idx_nnst(jmx, bean):
    try:
        if isinstance(jmx, HttpJmx):
            mb = 'Hadoop:service=NameNode,name=NameNodeStatus'
        else:
            mb = javax.management.ObjectName('Hadoop:service=NameNode,name=NameNodeStatus')
        alist = ['NNRole',
'HostAndPort',
'SecurityEnabled',
'LastHATransitionTime',
'State']
        vvv = jmx.getAttributes(mb, alist)
        for vv in vvv:
            if vv:
                if isinstance(jmx, HttpJmx):
                    nm = vv[0]
                    ve = vv[1]
                else:
                    nm = str(vv.getName())
                    ve = vv.getValue()
                if nm == 'HostAndPort':
                    vs = cs(ve).split(':')
                    bean['Hostname'] = vs[0]
                    if vs[1]:
                        bean['RpcPort'] = vs[1]
                else:
                    bean[nm] = cs(ve)
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
        if isinstance(jmx, HttpJmx):
            mb = 'Hadoop:service=NameNode,name=BlockStats'
        else:
            mb = javax.management.ObjectName('Hadoop:service=NameNode,name=BlockStats')
        alist = ['StorageTypeStats']
        vvv = jmx.getAttributes(mb, alist)
        for vv in vvv:
            if vv:
                if isinstance(jmx, HttpJmx):
                    vals = vv[1]
                else:
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
        if isinstance(jmx, HttpJmx):
            mb = 'Hadoop:service=NameNode,name=NameNodeInfo'
        else:
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
            if isinstance(jmx, HttpJmx):
                nm = vv[0]
                ve = vv[1]
            else:
                nm = str(vv.getName())
                ve = vv.getValue()
            if nm == 'LiveNodes':
                ln = json.loads(str(ve))
                if ln:
                    for k in ln.keys():
                        n = ln[k]
                        nodes.append([k.split(':')[0],cs(n.get('infoAddr')).split(':')[0],n.get('adminState'),n.get('capacity'),n.get('used'),n.get('nonDfsUsedSpace'),n.get('numBlocks'),n.get('blockPoolUsed'),n.get('volfails')])
            elif nm == 'NameDirSize':
                ln = json.loads(str(ve))
                if ln:
                    for k in ln.keys():
                        dirs[k] = [k, ln[k], None, None]
            elif nm == 'NameDirStatuses':
                ln = json.loads(str(ve))
                if ln:
                    ls = ln.get('active')
                    if ls:
                        for k in ls.keys():
                            if dirs.get(k):
                                dirs[k][2] = ls[k]
                                dirs[k][3] = 'Active'
            elif nm == 'NameJournalStatus':
                ln = json.loads(str(ve))
                if ln:
                    for vs in ln:
                        jour.append([vs.get('manager'),vs.get('stream'),vs.get('disabled'),vs.get('required')])
            elif nm == 'JournalTransactionInfo':
                ln = json.loads(str(ve))
                if ln:
                    v = ln.get('MostRecentCheckpointTxId')
                    if v:
                        bean['MostRecentCheckpointTxId'] = cs(v)
                    v = ln.get('LastAppliedOrWrittenTxId')
                    if v:
                        bean['LastAppliedOrWrittenTxId'] = cs(v)
            else:
                bean[nm] = cs(ve)
        nsp.append([bean.get('BlockPoolId'),bean.get('Total'),bean.get('Used'),bean.get('NonDfsUsedSpace'),bean.get('PercentUsed'),bean.get('PercentRemaining'),bean.get('BlockPoolUsedSpace'),bean.get('PercentBlockPoolUsed'),bean.get('TotalBlocks'),bean.get('NumberOfMissingBlocks')])
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
        if isinstance(jmx, HttpJmx):
            mb = 'Hadoop:service=DataNode,name=DataNodeInfo'
        else:
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
            if isinstance(jmx, HttpJmx):
                nm = vv[0]
                ve = vv[1]
            else:
                nm = str(vv.getName())
                ve = vv.getValue()
            if nm == 'NamenodeAddresses':
                v = json.loads(str(ve))
                s = ''
                for k in v.values():
                    if s:
                        s += ',' + k
                    else:
                        s = k
                bean['BlockPoolId'] = s
            elif nm == 'VolumeInfo':
                v = json.loads(str(ve))
                for k in v.keys():
                    vols.append([bean.get('Hostname'),k,v[k].get('numBlocks'),v[k].get('usedSpace'),v[k].get('freeSpace'),v[k].get('reservedSpace'),v[k].get('storageType')])
            elif nm == 'DatanodeHostname':
                bean['Hostname'] = cs(ve)
            else:
                bean[nm] = cs(ve)
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
        if isinstance(jmx, HttpJmx):
            mb = 'Hadoop:service=DataNode,name=FSDatasetState'
        else:
            mb = javax.management.ObjectName('Hadoop:service=DataNode,name=FSDatasetState')
        alist = ['Capacity',
'tag.StorageInfo',
'DfsUsed',
'Remaining',
'NumFailedVolumes']
        vvv = jmx.getAttributes(mb, alist)
        for vv in vvv:
            if isinstance(jmx, HttpJmx):
                nm = vv[0]
                ve = vv[1]
            else:
                nm = str(vv.getName())
                ve = vv.getValue()
            if vv:
                bean[nm] = cs(ve)
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

def hdfs_cluster(pg, target_id, cid):
    sql = "select subuid from mgt_system where uid='%s'" % target_id
    result = relate_pg2(pg, sql)
    if result.code == 0:
        if len(result.msg) == 1 and result.msg[0][0] == cid:
            return 0
    else:
        return -1
    cur = pg.conn.cursor()
    sql = "update mgt_system set subuid='%s' where uid='%s'" % (cid, target_id)
    cur.execute(sql)
    pg.conn.commit()

if __name__ == '__main__':
    dbInfo = eval(sys.argv[1])
    pg, target_id = JavaUtil.get_pg_env(dbInfo, 0)
    host = dbInfo['target_ip']
    port = dbInfo['target_port']
    usr = dbInfo['target_usr']
    pwd = dbInfo['target_pwd']
    ct = time.time()
    if pwd:
        pwd = JavaRsa.decrypt_java(pwd)
    #jmxsoc = JMXUtil.connect(host, port, 'rmi', usr, pwd)
    #jmx = jmxsoc.getMBeanServerConnection();
    #jmxsoc = JMXUtil.Jmx(host, port, 'rmi', usr, pwd)
    #jmx = jmxsoc.jmx
    jmxsoc = None
    jmx = HttpJmxUtil.HttpJmx(host, port, usr, pwd)
    jmx.connect()
    ct2 = time.time()
    metric = []
    typ = -1
    if isinstance(jmx, HttpJmx):
        mbs = jmx.queryNames('Hadoop:service=NameNode,name=*',None)
    else:
        mbs = jmx.queryNames(javax.management.ObjectName('Hadoop:service=NameNode,name=*'),None)
    if mbs:
        typ = 0
    else:
        if isinstance(jmx, HttpJmx):
            mbs = jmx.queryNames('Hadoop:service=DataNode,name=*',None)
        else:
            mbs = jmx.queryNames(javax.management.ObjectName('Hadoop:service=DataNode,name=*'),None)
        if mbs:
            typ = 1
    if typ == -1:
        print("msg=对象类型非NameNode或DataNode")
        sys.exit(1)
    kvs = []
    kvs2 = []
    bean = {}
    if typ == 0:
        idx_jvm(jmx, bean)
        idx_nnst(jmx, bean)
        idx_nninfo(jmx, bean)
    else:
        idx_jvm(jmx, bean)
        idx_dninfo(jmx, bean)
        bean['NNRole'] = 'DataNode'
    rpc = bean.get('RpcPort')
    if rpc:
        bean['Endpoint'] = host + ':' + rpc
    for k in bean:
        if k in CIB_BASIC:
            kvs.append(dict(name=k,value=cs(bean[k])))
        if isinstance(bean[k], str) and k != 'InputArguments':
            kvs2.append(dict(name=k,value=cs(bean[k])))
    if jmxsoc:
        jmxsoc.close();
    cluster_id = bean.get('ClusterId')
    if cluster_id:
        hdfs_cluster(pg, target_id, cluster_id)
    #metric.append(dict(index_id="5020000", value="连接成功"))
    metric.append(dict(index_id="5020001", value=kvs))
    metric.append(dict(index_id="5020002", value=kvs2))
    if nsp:
        vals = []
        table_append(vals, ['块池ID','总容量','已用容量','非dfs空间','使用率','剩余率','已用块池','块池使用率','总块数','丢失块数'])
        for n in nsp:
            table_append(vals, n)
        metric.append(dict(index_id="5020003", content=vals))
    if nodes:
        vals = []
        table_append(vals, ['主机名','IP地址','状态','容量','已使用','非dfs空间','块数','已用块池','失败卷数'])
        for n in nodes:
            table_append(vals, n)
        metric.append(dict(index_id="5020004", content=vals))
    if vols:
        vals = []
        table_append(vals, ['主机名','块数','已用空间','空闲空间','保留空间','存储类型'])
        for n in vols:
            table_append(vals, n)
        metric.append(dict(index_id="5020005", content=vals))
    if dirs:
        vals = []
        table_append(vals,['路径','大小','类型','状态'])
        for n in dirs.values():
            table_append(vals, n)
        metric.append(dict(index_id="5020006", content=vals))
    if jour:
        vals = []
        table_append(vals,['管理','流','失效','需要'])
        for n in jour:
            table_append(vals, n)
        metric.append(dict(index_id="5020007", content=vals))
    print('{"cib":' + json.dumps(metric) + '}')

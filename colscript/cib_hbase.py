import json
import sys
import traceback
import time
from datetime import datetime
from collections import Iterable

import jpype
from jpype import *

sys.path.append('/usr/software/knowl')
# import DBUtil
import JavaUtil
import JavaRsa
import JMXUtil
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
'clusterId',
'zookeeperQuorum',
'Endpoint',
'Hostname',
'isActiveMaster',
'version',
'rootdir'
])

nsp = []
nodes = []

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
    except Exception as e:
        result.code = 1
        result.msg = str(e)
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
                if k in ['hbase.log.dir', 'hbase.log.file', 'hadoop.id.str']:
                    bean[k] = cs(val.get('value'))
        else:
            bean[nm] = cs(vu)
    bean['Uptime'] = FormatTime(float(bean['Uptime'])/1000)

def idx_master(jmx, bean):
    global nsp

    try:
        if isinstance(jmx, HttpJmx):
            mb = 'Hadoop:service=HBase,name=Master,sub=Server'
        else:
            mb = javax.management.ObjectName('Hadoop:service=HBase,name=Master,sub=Server')
        alist = ['tag.clusterId',
'tag.liveRegionServers',
'tag.deadRegionServers',
'tag.zookeeperQuorum',
'tag.serverName',
'tag.isActiveMaster',
'masterActiveTime']
        vvv = jmx.getAttributes(mb, alist)
        for vv in vvv:
            if not vv:
                continue
            if isinstance(jmx, HttpJmx):
                nm = vv[0]
                ve = vv[1]
            else:
                nm = str(vv.getName())
                ve = str(vv.getValue())
            if nm == 'tag.liveRegionServers':
                if ve:
                    srs = str(ve).split(';')
                    for sr in srs:
                        arr = sr.split(',')
                        s = arr[2]
                        if arr[2]:
                            tm = float(arr[2])
                            if tm:
                                s = str(datetime.fromtimestamp(int(tm/1000)))
                        nodes.append([arr[0],arr[1],s,'Active'])
            elif nm == 'tag.deadRegionServers':
                if ve:
                    srs = str(ve).split(';')
                    for sr in srs:
                        arr = sr.split(',')
                        s = arr[2]
                        if arr[2]:
                            tm = float(arr[2])
                            if tm:
                                s = str(datetime.fromtimestamp(int(tm/1000)))
                        nodes.append([arr[0],arr[1],s,'Dead'])
            elif nm == 'tag.serverName':
                arr = str(ve).split(',')
                bean['Endpoint'] = arr[0]+':'+arr[1]
                bean['Hostname'] = arr[0]
            elif nm == 'tag.zookeeperQuorum':
                bean['zookeeperQuorum'] = str(ve)
            elif nm == 'tag.clusterId':
                bean['clusterId'] = str(ve)
            elif nm == 'tag.isActiveMaster':
                bean['isActiveMaster'] = str(ve)
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

def idx_region(jmx, bean):
    try:
        if isinstance(jmx, HttpJmx):
            mb = 'Hadoop:service=HBase,name=RegionServer,sub=Server'
        else:
            mb = javax.management.ObjectName('Hadoop:service=HBase,name=RegionServer,sub=Server')
        alist = ['tag.zookeeperQuorum',
'tag.clusterId',
'tag.serverName',
'regionCount',
'storeCount',
'hlogFileCount',
'hlogFileSize',
'memStoreSize',
'storeFileCount',
'storeFileSize',
'storeFileIndexSize',
'percentFilesLocal',
'percentFilesLocalSecondaryRegions'
]
        vvv = jmx.getAttributes(mb, alist)
        for vv in vvv:
            if isinstance(jmx, HttpJmx):
                nm = vv[0]
                ve = vv[1]
            else:
                nm = str(vv.getName())
                ve = vv.getValue()
            if nm == 'tag.serverName':
                arr = str(ve).split(',')
                bean['Endpoint'] = arr[0]+':'+arr[1]
                bean['Hostname'] = arr[0]
            elif nm == 'tag.zookeeperQuorum':
                bean['zookeeperQuorum'] = str(ve)
            elif nm == 'tag.clusterId':
                bean['clusterId'] = str(ve)
            else:
                bean[nm] = cs(ve)
        nsp.append([bean.get('regionCount'),bean.get('storeCount'),bean.get('hlogFileCount'),bean.get('hlogFileSize'),bean.get('memStoreSize'),bean.get('storeFileCount'),bean.get('storeFileSize'),bean.get('storeFileIndexSize'),bean.get('percentFilesLocal'),bean.get('percentFilesLocalSecondaryRegions')])
        del bean['regionCount']
        del bean['storeCount']
        del bean['hlogFileCount']
        del bean['hlogFileSize']
        del bean['memStoreSize']
        del bean['storeFileCount']
        del bean['storeFileSize']
        del bean['storeFileIndexSize']
        del bean['percentFilesLocal']
        del bean['percentFilesLocalSecondaryRegions']
    except javax.management.RuntimeOperationsException as e:
        bt = str(e)
        exc_type, exc_value, exc_tb = sys.exc_info()
        for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
            bt += "\n%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname)
        print(bt)
        print(exc_type)
        print(exc_value)

def hbase_props(jmx, bean):
    xml = jmx.get('conf')
    if xml:
        val = HttpJmxUtil.getProp(xml, 'hbase.defaults.for.version')
        if val is not None:
            bean['version'] = val
        val = HttpJmxUtil.getProp(xml, 'hbase.rootdir')
        if val is not None:
            bean['rootdir'] = val
        val = HttpJmxUtil.getProp(xml, 'zookeeper.znode.parent')
        if val is not None:
            bean['zookeeperRoot'] = val

def hbase_cluster(pg, target_id, cid):
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

def fillInfo(pg, target_id, dbInfo):
    sql = "select ip,port,user,password from mgt_system where uid='%s' and use_flag" % target_id
    result = relate_pg2(pg, sql)
    if result.code == 0 and len(result.msg) > 0:
        dbInfo['target_ip'] = result.msg[0][0]
        dbInfo['target_port'] = result.msg[0][1]
        dbInfo['target_usr'] = result.msg[0][2]
        dbInfo['target_pwd'] = result.msg[0][3]

if __name__ == '__main__':
    dbInfo = eval(sys.argv[1])
    pg, target_id = JavaUtil.get_pg_env(dbInfo, 0)
    fillInfo(pg, target_id, dbInfo)
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
        mbs = jmx.queryNames('Hadoop:service=HBase,name=Master,sub=Server',None)
    else:
        mbs = jmx.queryNames(javax.management.ObjectName('Hadoop:service=HBase,name=Master,sub=Server'),None)
    if mbs:
        typ = 0
    else:
        if isinstance(jmx, HttpJmx):
            mbs = jmx.queryNames('Hadoop:service=HBase,name=RegionServer,sub=Server',None)
        else:
            mbs = jmx.queryNames(javax.management.ObjectName('Hadoop:service=HBase,name=RegionServer,sub=Server'),None)
        if mbs:
            typ = 1
    if typ == -1:
        print("msg=对象类型非HMaster或RegionServer")
        sys.exit(1)
    kvs = []
    kvs2 = []
    bean = {}
    if typ == 0:
        idx_jvm(jmx, bean)
        idx_master(jmx, bean)
        bean['NNRole'] = 'HMaster'
    else:
        idx_jvm(jmx, bean)
        idx_region(jmx, bean)
        bean['NNRole'] = 'RegionServer'
    hbase_props(jmx, bean)
    for k in bean:
        if k in CIB_BASIC:
            kvs.append(dict(name=k,value=cs(bean[k])))
        if isinstance(bean[k], str) and k != 'InputArguments':
            kvs2.append(dict(name=k,value=cs(bean[k])))
    if jmxsoc:
        jmxsoc.close();
    cluster_id = bean.get('clusterId')
    if cluster_id:
        hbase_cluster(pg, target_id, cluster_id)
    #metric.append(dict(index_id="5060000", value="连接成功"))
    metric.append(dict(index_id="5060001", value=kvs))
    metric.append(dict(index_id="5060002", value=kvs2))
    if nsp:
        vals = []
        table_append(vals, ['区域数','存储区数','hlog文件数','hlog文件大小','内存存储区大小','存储文件数','存储文件大小','存储索引大小','本地文件比例','本地文件副本比例'])
        for n in nsp:
            table_append(vals, n)
        metric.append(dict(index_id="5060003", content=vals))
    if nodes:
        vals = []
        table_append(vals, ['主机名','端口','启动时间','状态'])
        for n in nodes:
            table_append(vals, n)
        metric.append(dict(index_id="5060004", content=vals))
    print('{"cib":' + json.dumps(metric) + '}')

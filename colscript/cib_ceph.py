import sys

sys.path.append('/usr/software/knowl')
import json
import DBUtil
import JavaRsa
import PromeUtil
import os_svc

def fetchOne(db, sql):
    result = db.execute(sql)
    if result.code == 0:
        result.msg = result.msg.fetchone()
    return result

def fetchAll(db, sql):
    result = db.execute(sql)
    if result.code == 0:
        result.msg = result.msg.fetchall()
    return result

def cs(val, dt=False):
    if val is None:
        return ''
    else:
        if dt:
            return val.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return str(val)

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

def cib_basic(pg, target_id, mets, metric):
    props = []
    if mets.get('ceph_osd_metadata'):
        ms = mets['ceph_osd_metadata']
        osds = {}
        for k in ms.keys():
            if k[0:4] == 'met_':
                ts = ms[k].get('tags')
                if ts:
                    s1 = ts.get('cluster_addr')
                    s2 = ts.get('device_class')
                    s3 = ts.get('id')
                    s4 = ts.get('public_addr')
                    osds['osd.' + cs(s3)] = [s3,s2,s1,s4,None,None,None]
        ms = mets['ceph_osd_numpg']
        if ms:
            for k in ms.keys():
                if k[0:4] == 'met_':
                    ts = ms[k].get('tags')
                    if ts:
                        s = ts.get('ceph_daemon')
                        if osds.get(s):
                            osds[s][4] = ms[k].get('val')
        ms = mets['ceph_osd_stat_bytes']
        if ms:
            for k in ms.keys():
                if k[0:4] == 'met_':
                    ts = ms[k].get('tags')
                    if ts:
                        s = ts.get('ceph_daemon')
                        if osds.get(s):
                            osds[s][5] = ms[k].get('val')
        ms = mets['ceph_osd_stat_bytes_used']
        if ms:
            for k in ms.keys():
                if k[0:4] == 'met_':
                    ts = ms[k].get('tags')
                    if ts:
                        s = ts.get('ceph_daemon')
                        if osds.get(s):
                            osds[s][6] = ms[k].get('val')
        if osds:
            vals = []
            vals.append(
                dict(c1="ID", c2="磁盘类型", c3="集群地址", c4="公网地址", c5="放置组数", c6="容量", c7="已使用", c8=None, c9=None, c10=None))
            for row in osds.values():
                vals.append(
                    dict(c1=cs(row[0]), c2=cs(row[1]), c3=cs(row[2]), c4=cs(row[3]), c5=cs(row[4]), c6=cs(row[5]), c7=cs(row[6]), c8=None,
                         c9=None, c10=None))
            metric.append(dict(index_id="4120002", content=vals))
    if mets.get('ceph_disk_occupation'):
        ms = mets['ceph_disk_occupation']
        ns = set()
        vals = []
        for k in ms.keys():
            if k[0:4] == 'met_':
                ts = ms[k].get('tags')
                if ts:
                    s1 = ts.get('instance')
                    ns.add(s1)
                    s2 = ts.get('device')
                    s3 = ts.get('ceph_daemon')
                    if not vals:
                        vals.append(
                            dict(c1="节点", c2="磁盘", c3="OSD", c4=None, c5=None, c6=None, c7=None, c8=None, c9=None, c10=None))
                    vals.append(
                        dict(c1=cs(s1), c2=cs(s2), c3=cs(s3), c4=None, c5=None, c6=None, c7=None, c8=None,
                             c9=None, c10=None))
        if vals:
            metric.append(dict(index_id="4120003", content=vals))
        if ns:
            props.append(dict(name="osd_nodes", value=tuple2(ns)))
    if mets.get('ceph_pool_metadata'):
        ps = {}
        ms = mets['ceph_pool_metadata']
        for k in ms.keys():
            if k[0:4] == 'met_':
                ts = ms[k].get('tags')
                if ts:
                    s1 = ts.get('pool_id')
                    s2 = ts.get('name')
                    ps[s1] = [s1,s2,None,None,None,None]
        ms = mets.get('ceph_pool_objects')
        if ms:
            for k in ms.keys():
                if k[0:4] == 'met_':
                    ts = ms[k].get('tags')
                    if ts:
                        s1 = ts.get('pool_id')
                        s2 = ms[k].get('val')
                        if ps.get(s1):
                            ps[s1][2] = s2
        ms = mets.get('ceph_pool_bytes_used')
        if ms:
            for k in ms.keys():
                if k[0:4] == 'met_':
                    ts = ms[k].get('tags')
                    if ts:
                        s1 = ts.get('pool_id')
                        s2 = ms[k].get('val')
                        if ps.get(s1):
                            ps[s1][3] = s2
        ms = mets.get('ceph_pool_raw_bytes_used')
        if ms:
            for k in ms.keys():
                if k[0:4] == 'met_':
                    ts = ms[k].get('tags')
                    if ts:
                        s1 = ts.get('pool_id')
                        s2 = ms[k].get('val')
                        if ps.get(s1):
                            ps[s1][4] = s2
        ms = mets.get('ceph_pool_max_avail')
        if ms:
            for k in ms.keys():
                if k[0:4] == 'met_':
                    ts = ms[k].get('tags')
                    if ts:
                        s1 = ts.get('pool_id')
                        s2 = ms[k].get('val')
                        if ps.get(s1):
                            ps[s1][5] = s2
        if ps:
            vals = []
            vals.append(
                dict(c1="ID", c2="名称", c3="对象数", c4="已使用", c5="已使用(裸)", c6="最大可用", c7=None, c8=None, c9=None, c10=None))
            for row in ps.values():
                vals.append(
                    dict(c1=cs(row[0]), c2=cs(row[1]), c3=cs(row[2]), c4=cs(row[3]), c5=cs(row[4]), c6=cs(row[5]), c7=None, c8=None,
                         c9=None, c10=None))
            metric.append(dict(index_id="4120004", content=vals))
    if mets.get('ceph_cluster_total_bytes'):
        s1 = mets['ceph_cluster_total_bytes']['met_'].get('val')
    else:
        s1 = None
    if mets.get('ceph_cluster_total_used_bytes'):
        s2 = mets['ceph_cluster_total_used_bytes']['met_'].get('val')
    else:
        s2 = None
    if mets.get('ceph_cluster_total_objects'):
        s3 = mets['ceph_cluster_total_objects']['met_'].get('val')
    else:
        s3 = None
    if s1 and s2 and s3:
        vals = []
        vals.append(
            dict(c1="总容量", c2="已使用", c3="对象数", c4=None, c5=None, c6=None, c7=None, c8=None, c9=None, c10=None))
        vals.append(
            dict(c1=cs(s1), c2=cs(s2), c3=cs(s3), c4=None, c5=None, c6=None, c7=None, c8=None,
                 c9=None, c10=None))
        metric.append(dict(index_id="4120005", content=vals))
    if mets.get('ceph_mon_num_sessions'):
        ns = set()
        ms = mets['ceph_mon_num_sessions']
        for k in ms.keys():
            if k[0:4] == 'met_':
                ts = ms[k].get('tags')
                if ts:
                    s = ts.get('ceph_daemon')
                    if s and s[0:4] == 'mon.':
                        ns.add(s[4:])
        if ns:
            props.append(dict(name="mon_nodes", value=tuple2(ns)))
    if mets.get('ceph_pg_active'):
        props.append(dict(name="pg_active", value=cs(mets['ceph_pg_active']['met_'].get('val'))))
    if mets.get('ceph_pg_clean'):
        props.append(dict(name="pg_clean", value=cs(mets['ceph_pg_clean']['met_'].get('val'))))
    ceph_info(pg, target_id, props)
    if props:
        metric.append(dict(index_id="4120001", value=props))

def getsshinfo(pg, targetId):
    import sshSession
    sql = """select b.in_ip,b.in_username,b.in_password,b.port,b.position,b.life,d.name
from mgt_system a,mgt_device b,sys_dict d
where a.ip=b.in_ip
and a.uid = '""" + target_id + """'
and d.type='device_opersys'
and b.opersys=d.value::numeric and b.use_flag"""
    res = DBUtil.getValue(pg, sql)
    rs = res.fetchone()
    in_ostype = ssh = ''
    if rs:
        in_ip = rs[0]
        in_usr = rs[1]
        in_passwd = rs[2]
        in_port = rs[3]
        protocol = rs[4]
        life = rs[5]
        in_ostype = rs[6]
        if protocol == '1':
            proto = "SSH"
        elif protocol == '2':
            proto = "RSH"
        else:
            proto = "SSH"
        # 获取ssh免密信息
        ssh_user, ssh_path = DBUtil.get_sshkey_info(pg)
        ssh = sshSession.sshSession(in_ip, in_usr, in_passwd, in_port, proto, life, ssh_user, ssh_path)
    return in_ostype, ssh

def ceph_ret(ostype, lines, start, stop, par):
    val = None
    cmd = None
    cnt = 0
    for i in range(start, stop):
        cnt += 1
        line, cmd = os_svc.getOsline(lines[i])
        if not line is None:
            val = line
        if not cmd is None:
            break
    return val, cmd, start + cnt - 1

def ceph_info(conn, targetId, props):
    ostype, helper, device_id = getsshinfo(conn, targetId)
    if not helper:
        return
    pid = 0
    cmd = os_svc.os_cmd(ostype, 'ceph1', 'ceph -v')
    s = os_svc.os_cmd(ostype, 'ceph2', 'ceph pg stat')
    cmd = os_svc.concat(cmd, s)
    kvs = {}
    ret = os_svc.proc(ostype, helper, cmd, kvs, {'ceph1': ceph_ret,'ceph2': ceph_ret})
    val = kvs.get('ceph1')
    if val:
        props.append(dict(name="version", value=val))
    val = kvs.get('ceph2')
    if val:
        props.append(dict(name="pgs", value=val.split()[0]))

def failover(pg, target_id, host, port, mets):
    hosts = []
    ph = host
    f = False
    hs = None
    sql = "select cib_name,cib_value from p_normal_cib where index_id=1000001 and cib_name in ('mgr','_mgr') and target_id='%s'" % target_id
    result = fetchAll(pg, sql)
    if result.code == 0:
        for row in result.msg:
            if row[0] == 'mgr':
                hs = row[1]
            else:
                ph = row[1]
                f = True
    hosts.append(ph)
    if hs:
        arr = hs.split(',')
        for it in arr:
            if it:
                if it != ph:
                    hosts.append(it)
    for h in hosts:
        try:
            exptr = PromeUtil.Exporter(h,port)
            exptr.collect(mets)
            if h != ph:
                if f:
                    sql = "update p_normal_cib set cib_value='%s',record_time=now() where target_id='%s' and cib_name='_mgr' and index_id=1000001" % (h,target_id)
                else:
                    sql = "insert into p_normal_cib(target_id,index_id,cib_name,cib_value,record_time) values('%s',1000001,'_mgr','%s',now())" % (target_id,h)
                try:
                    cur = pg.conn.cursor()
                    cur.execute(sql)
                    pg.conn.commit()
                except:
                    pg.conn.rollback()
            ret = True
            break
        except:
            ret = False
    return ret

if __name__ == '__main__':
    dbInfo = eval(sys.argv[1])
    host = dbInfo['target_ip']
    port = dbInfo['target_port']
    #usr = dbInfo['target_usr']
    target_id, pg = DBUtil.get_pg_env(dbInfo, 0)
    mets = {}
    metric = []
    ret = failover(pg, target_id, host, port, mets)
    if ret:
        cib_basic(pg, target_id, mets, metric)
        print('{"cib":' + json.dumps(metric) + '}')
    else:
        raise Exception('连接失败')

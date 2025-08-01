import os
import sys
import json
import time

sys.path.append('/usr/software/knowl')
import DBUtil
import JavaRsa
import PromeUtil

map_table = [
["ceph_health_status","=",4130001],
["ceph_mon_quorum_count","=",4130002],
["ceph_osd_metadata","cnt",4130003],
#["ceph_disk_occupation","cnt",4130004],
["ceph_pool_metadata","cnt",4130005],
#["ceph_osd_numpg","sum",4130006],
["ceph_osd_in","sum",4130007],
["ceph_osd_up","sum",4130008],
["ceph_osd_op_out_bytes","sum",4130011],
["ceph_osd_op_r","sum",4130012],
["ceph_osd_op_r_out_bytes","sum",4130013],
["ceph_osd_op_in_bytes","sum",4130014],
["ceph_osd_op_w","sum",4130015],
["ceph_osd_op_w_in_bytes","sum",4130016],
["ceph_osd_op_rw_out_bytes","sum",4130017],
["ceph_osd_op_rw_in_bytes","sum",4130018],
["ceph_osd_op","sum",4130019],
["ceph_osd_op_rw","sum",4130020],
["ceph_osd_apply_latency_ms","avg",4130021],
["ceph_osd_commit_latency_ms","avg",4130022],
["ceph_cluster_total_bytes","=",4130023],
["ceph_cluster_total_used_bytes","=",4130024],
["ceph_cluster_total_objects","=",4130025],
#["ceph_pool_bytes_used","sum",4130024],
#["ceph_pool_raw_bytes_used","sum",4130025],
#["ceph_pool_max_avail","sum",4130026],
#["ceph_pool_objects","sum",4130027],
#["ceph_osd_stat_bytes","sum",4130028],
#["ceph_osd_stat_bytes_used","sum",4130029],
["ceph_pg_incomplete","=",4130101],
["ceph_pg_degraded","=",4130102],
["ceph_pg_forced_backfill","=",4130103],
["ceph_pg_stale","=",4130104],
["ceph_pg_undersized","=",4130105],
["ceph_pg_peering","=",4130106],
["ceph_pg_inconsistent","=",4130107],
["ceph_pg_forced_recovery","=",4130108],
["ceph_pg_creating","=",4130109],
["ceph_pg_wait_backfill","=",4130110],
["ceph_pg_active","=",4130111],
["ceph_pg_deep","=",4130112],
["ceph_pg_scrubbing","=",4130113],
["ceph_pg_recovering","=",4130114],
["ceph_pg_repair","=",4130115],
["ceph_pg_down","=",4130116],
["ceph_pg_peered","=",4130117],
["ceph_pg_backfill","=",4130118],
["ceph_pg_clean","=",4130119],
["ceph_pg_remapped","=",4130120],
["ceph_pg_backfill_toofull","=",4130121]
]

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

def failover(pg, target_id, host, port, mets):
    sql = "select cib_name,cib_value from p_normal_cib where index_id=1000001 and cib_name in ('mgr','_mgr') and target_id='%s'" % target_id
    result = relate_pg2(pg, sql)
    hosts = []
    ph = host
    f = False
    hs = None
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
    targetId, pg = DBUtil.get_pg_env(dbInfo,0)
    if pg.conn is None:
        print('无法连接本地数据库')
        sys.exit()
    ct = int(time.time())
    mets = {}
    metric = []
    ret = failover(pg, targetId, host, port, mets)
    if ret:
        metric.append(dict(index_id="4130000", value="连接成功"))
        PromeUtil.map(mets, map_table, metric)
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
            metric.append(dict(index_id="4130004", value=str(len(ns))))
        n1 = PromeUtil.calc(mets, 'ceph_osd_metadata', 'cnt')
        n2 = PromeUtil.calc(mets, 'ceph_osd_in', 'sum')
        n3 = PromeUtil.calc(mets, 'ceph_osd_up', 'sum')
        if n1 is not None:
            if n2 is not None:
                metric.append(dict(index_id="4130009", value=str(int(n1 - n2))))
                metric.append(dict(index_id="4130209", value=str(round((n1-n2)*100/n1,2))))
            if n3 is not None:
                metric.append(dict(index_id="4130010", value=str(int(n1 - n3))))
                metric.append(dict(index_id="4130210", value=str(round((n1-n3)*100/n1,2))))
            ps = {}
            ms = mets.get('ceph_osd_stat_bytes')
            if ms:
                for k in ms.keys():
                    if k[0:4] == 'met_':
                        ts = ms[k].get('tags')
                        if ts:
                            s1 = ts.get('ceph_daemon')
                            s2 = ms[k].get('val')
                            ps[s1] = [float(s2), None]
            ms = mets.get('ceph_osd_stat_bytes_used')
            v = 0
            if ms:
                for k in ms.keys():
                    if k[0:4] == 'met_':
                        ts = ms[k].get('tags')
                        if ts:
                            s1 = ts.get('ceph_daemon')
                            s2 = ms[k].get('val')
                            if ps.get(s1) is not None:
                                ps[s1][1] = float(s2)
                                n = round(ps[s1][1]*100/ps[s1][0],2)
                                if n > v:
                                    v = n
            metric.append(dict(index_id="4130027", value=str(v)))
        if mets.get('ceph_pool_metadata'):
            ps = {}
            ms = mets.get('ceph_pool_raw_bytes_used')
            if ms:
                for k in ms.keys():
                    if k[0:4] == 'met_':
                        ts = ms[k].get('tags')
                        if ts:
                            s1 = ts.get('pool_id')
                            s2 = ms[k].get('val')
                            ps[s1] = [float(s2), None]
            ms = mets.get('ceph_pool_max_avail')
            v = 0
            if ms:
                for k in ms.keys():
                    if k[0:4] == 'met_':
                        ts = ms[k].get('tags')
                        if ts:
                            s1 = ts.get('pool_id')
                            s2 = ms[k].get('val')
                            if ps.get(s1) is not None:
                                ps[s1][1] = float(s2)
                                n = round(ps[s1][0]*100/(ps[s1][0]+ps[s1][1]),2)
                                if n > v:
                                    v = n
            metric.append(dict(index_id="4130028", value=str(v)))
        if mets.get('ceph_cluster_total_bytes'):
            s1 = mets['ceph_cluster_total_bytes']['met_'].get('val')
            if s1 and mets.get('ceph_cluster_total_used_bytes'):
                s2 = mets['ceph_cluster_total_used_bytes']['met_'].get('val')
                if s2:
                    n = round(float(s2)*100/float(s1),2)
                    metric.append(dict(index_id="4130026", value=str(n)))
    else:
        metric.append(dict(index_id="4130000", value="连接失败"))
    metric.append(dict(index_id="4139999", value=str(ct)))
    ct2 = time.time()
    metric.append(dict(index_id="1000101", value=str(int((ct2-ct)*1000))))
    print('{"results":' + json.dumps(metric, ensure_ascii=False) + '}')

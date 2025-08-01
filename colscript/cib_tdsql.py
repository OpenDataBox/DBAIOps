import sys

sys.path.append('/usr/software/knowl')
import json
import DBUtil
import TdsqlUtil
import JavaRsa

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

def cib_basic(pg, tdsql, target_id, metric):
    props = []
    ret,res = tdsql.getInstance(pg, target_id)
    states = ['待运营', '运营中', '已下架']
    if ret == 200:
        for row in res:
            id = row['id']
            props.append(dict(name="instance_id", value=id))
            mtype = row['mtype']
            props.append(dict(name="instance_type", value=mtype))
            rstate = states[int(row['rstate'])]
            props.append(dict(name="instance_state", value=rstate))
            lst = row['mysql_list']
            vals = []
            for rs in lst:
                if not vals:
                    vals.append(
                        dict(c1="IP", c2="端口", c3="角色", c4="运营状态", c5="集合", c6=None, c7=None, c8=None, c9=None, c10=None))
                vals.append(dict(c1=cs(rs['ip']),c2=cs(rs['port']),c3=cs(rs['role']),c4=states[int(rs['rstate'])],c5=cs(rs['set_id']),c6=None,c7=None,c8=None,c9=None,c10=None))
            if vals:
                metric.append(dict(index_id="2600002", content=vals))
            lst = row['proxy_list']
            vals = []
            for rs in lst:
                if not vals:
                    vals.append(
                        dict(c1="IP", c2="端口", c3="运营状态", c4=None, c5=None, c6=None, c7=None, c8=None, c9=None, c10=None))
                vals.append(dict(c1=cs(rs['ip']),c2=cs(rs['port']),c3=states[int(rs['rstate'])],c4=None,c5=None,c6=None,c7=None,c8=None,c9=None,c10=None))
            if vals:
                metric.append(dict(index_id="2600003", content=vals))
            break
    ret,res = tdsql.getCapacity(pg, target_id)
    if ret == 200:
        vals = []
        for rs in res:
            if not vals:
                vals.append(
                    dict(c1="机型", c2="状态", c3="容灾模式", c4="设备数", c5="CPU总量", c6="内存总量", c7="磁盘总量", c8="CPU空闲率", c9="内存空闲率", c10="磁盘空闲率"))
            vals.append(dict(c1=cs(rs['machine']),c2=cs(rs['status']),c3=cs(rs['slaves']),c4=cs(rs['machine_count']),c5=cs(rs['cpu_total']),c6=cs(rs['memory_total']),c7=cs(rs['data_disk_total']),
                             c8=cs(rs['cpu_free_rate']),c9=cs(rs['memory_free_rate']),c10=cs(rs['data_disk_free_rate'])))
        if vals:
            metric.append(dict(index_id="2600004", content=vals))
    ret,res = tdsql.getCluster(pg, target_id)
    if ret == 200:
        props.append(dict(name="cluster_id", value=res.get('cluster_id')))
        props.append(dict(name="cluster_key", value=res.get('cluster_key')))
        props.append(dict(name="cluster_name", value=res.get('cluster_name')))
        props.append(dict(name="cluster_version", value=res.get('cluster_version')))
        props.append(dict(name="admin_list", value=res.get('admin_list')))
        props.append(dict(name="cluster_capacity_rate", value=res.get('cluster_capacity_rate')))
        props.append(dict(name="cluster_capacity_total", value=res.get('cluster_capacity_total')))
        props.append(dict(name="cluster_capacity_used", value=res.get('cluster_capacity_used')))
        props.append(dict(name="cluster_rstate", value=states[int(res.get('cluster_rstate'))]))
        props.append(dict(name="cluster_type", value=res.get('cluster_type')))
        props.append(dict(name="mdb_ip", value=res.get('mdb_ip')))
        props.append(dict(name="mdb_list", value=res.get('mdb_list')))
        props.append(dict(name="mdb_port", value=res.get('mdb_port')))
        props.append(dict(name="mdb_user", value=res.get('mdb_user')))
        props.append(dict(name="mdb_name", value=res.get('mdb_name')))
        props.append(dict(name="osssvr_list", value=res.get('osssvr_list')))
        props.append(dict(name="oss_version", value=res.get('oss_version')))
        props.append(dict(name="zookeeper_list", value=res.get('zookeeper_list')))
        props.append(dict(name="zookeeper_rootdir", value=res.get('zookeeper_rootdir')))
    if props:
        metric.append(dict(index_id="2600001", value=props))

def mgt(pg, tdsql, target_id):
    params = ["cluster/get_list","monitor_data/fetch","cluster/get_capacity","cluster/get_instances","install/get_db_info"]
    sql = f"select cib_name,cib_value from p_normal_cib where target_id='{target_id}' and index_id=1000001 and cib_name in {tuple2(params)}"
    result = fetchAll(pg, sql)
    auths = {}
    if result.code == 0:
        for row in result.msg:
            auths[row[0]] = row[1]
    ret = tdsql.getAuths()
    if ret == 0:
        for h in params:
            if tdsql.auths.get(h):
                if auths.get(h) != tdsql.auths[h]:
                    if h in auths.keys():
                        sql = f"update p_normal_cib set cib_value='{tdsql.auths[h]}',record_time=now() where target_id='{target_id}' and cib_name='{h}' and index_id=1000001"
                    else:
                        sql = f"insert into p_normal_cib(target_id,index_id,cib_name,cib_value,record_time) values('{target_id}',1000001,'{h}','{tdsql.auths[h]}',now())"
                    try:
                        cur = pg.conn.cursor()
                        cur.execute(sql)
                        pg.conn.commit()
                    except:
                        pg.conn.rollback()
    return ret

if __name__ == '__main__':
    dbInfo = eval(sys.argv[1])
    host = dbInfo['target_ip']
    port = dbInfo['target_port']
    #usr = dbInfo['target_usr']
    key = dbInfo['authKey']
    cid = dbInfo['clusterKey']
    iid = dbInfo['instanceId']
    target_id, pg = DBUtil.get_pg_env(dbInfo, 0)
    metric = []
    tdsql = TdsqlUtil.Tdsql(host, port, key, cid, iid)
    ret = mgt(pg, tdsql, target_id)
    if ret == 0:
        cib_basic(pg, tdsql, target_id, metric)
        print('{"cib":' + json.dumps(metric) + '}')
    else:
        raise Exception(str(dbInfo))
        raise Exception('连接失败')

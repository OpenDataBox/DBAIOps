import json
import sys
import datetime
import requests

sys.path.append('/usr/software/knowl')
import DBUtil

metric = []


def vals_append(key, value):
    metric.append(dict(index_id=str(key), value=str(value)))


def get_response(ip,port,section):
    url = f"http://{ip}:{port}/{section}"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    response = requests.request("GET", url, headers=headers).json()
    return response


def health_info(ip,port):
    """
    当前节点相关信息采集
    """
    data = get_response(ip,port,"patroni")
    vals_append(2320001, data["state"])
    start_time = data["postmaster_start_time"]
    et = datetime.datetime.now()
    bt = datetime.datetime.strptime(start_time.split('.')[0], "%Y-%m-%d %H:%M:%S")
    diff_seconds = (et - bt).seconds
    vals_append(2320006, diff_seconds)
    if data["role"] == "master":
        vals_append(2320002, data["xlog"]["location"])
    else:
        vals_append(2320003, data["xlog"]["received_location"])
        vals_append(2320004, data["xlog"]["replayed_location"])
        if data["xlog"]["paused"]:
            xlog_stat = 0
        else:
            xlog_stat = 1
        vals_append(2320005, xlog_stat)


def cluster_lag(ip,port):
    "查看集群从节点延迟"
    data = get_response(ip,port,"cluster")
    vars = []
    if data["members"]:
        for i in data["members"]:
            if "lag" in i.keys():
                mem_name = i["name"]
                mem_lag = i["lag"]
                vars.append(dict(name=mem_name, value=str(mem_lag)))
        metric.append(dict(index_id="2320007", value=vars))


def health_score(pg,ip):
    "获取该节点上PG软件对象的健康分"
    sql = f"""
    select
        total_score
    from
        h_health_check hhc,
        mgt_system ms
    where
        hhc.target_id = ms.uid
        and update_time > now() - interval '30m'
        and ms.ip = '{ip}'
        and type = '4'
    """
    cs = DBUtil.getValue(pg,sql)
    rs = cs.fetchone()
    if rs and rs[0]:
        vals_append(2320008, rs[0])
    else:
        vals_append(2320008, 100)


if __name__ == '__main__':
    dbInfo = eval(sys.argv[1])
    ip = dbInfo["target_ip"]
    port = dbInfo["target_port"]
    url = f"http://{ip}:{port}/patroni"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    try:
        response = requests.request("GET", url, headers=headers).json()
        metric.append(dict(index_id="2320000", value=str('连接成功')))
        health_info(ip,port)
        cluster_lag(ip,port)
        pg = DBUtil.get_pg_from_cfg()
        health_score(pg,ip)
    except requests.exceptions.RequestException as e:
        metric.append(dict(index_id="2320000", value=str('连接失败')))
    print('{"results":' + json.dumps(metric) + '}')

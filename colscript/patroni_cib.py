import json
import sys

import requests

vals = []
metric = []


def vals_append(key, value):
    vals.append(dict(name=key, value=str(value)))


def table_append(tab_list, c1=None, c2=None, c3=None, c4=None, c5=None, c6=None, c7=None, c8=None, c9=None, c10=None):
    tab_list.append(dict(c1=c1, c2=c2, c3=c3, c4=c4, c5=c5, c6=c6, c7=c7, c8=c8, c9=c9, c10=c10))


def get_response(section):
    dbInfo = eval(sys.argv[1])
    ip = dbInfo["target_ip"]
    port = dbInfo["target_port"]
    url = f"http://{ip}:{port}/{section}"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    response = requests.request("GET", url, headers=headers).json()
    return response


def cluster_info():
    """
    'api_url': 'http://test205:8008/patroni',
   'host': 'test205',
   'lag': 392,
   'name': 'test205',
   'port': 5432,
   'role': 'replica',
   'state': 'running',
   'timeline': 4}]
    """
    response = get_response("cluster")
    data = response["members"]
    members_list = []
    table_append(members_list, "name", "host", "port", "role", "state", "lag", "timeline", "api_url")
    for item in data:
        if item["role"] == 'leader':
            table_append(members_list, item["name"], item["host"], item["port"], item["role"], item["state"], "-1",
                         item["timeline"], item["api_url"])
        else:
            table_append(members_list, item["name"], item["host"], item["port"], item["role"], item["state"],
                         item["lag"],
                         item["timeline"], item["api_url"])
    metric.append(dict(index_id=2310003, content=members_list))


def health_info():
    """
    {
  "state": "running",
  "postmaster_start_time": "2021-08-23 08:11:33.897167+08:00",
  "role": "master",
  "server_version": 130004,
  "cluster_unlocked": false,
  "xlog": {
    "location": 83890680
  },
  "timeline": 5,
  "replication": [
    {
      "usename": "rep_user",
      "application_name": "test203",
      "client_addr": "60.60.60.203",
      "state": "streaming",
      "sync_state": "async",
      "sync_priority": 0
    },
    {
      "usename": "rep_user",
      "application_name": "test205",
      "client_addr": "60.60.60.205",
      "state": "startup",
      "sync_state": "async",
      "sync_priority": 0
    }
  ],
  "database_system_identifier": "6998110376364988695",
  "patroni": {
    "version": "2.1.0",
    "scope": "stampede"
  }
}
    """
    data = get_response("patroni")
    vals_append("state", data["state"])
    vals_append("postmaster_start_time", data["postmaster_start_time"])
    vals_append("role", data["role"])
    vals_append("server_version", data["server_version"])
    vals_append("cluster_unlocked", data["cluster_unlocked"])
    if data["role"] == "master":
        vals_append("replication_count", len(data["replication"]))
        vals_append("xlog_location", data["xlog"]["location"])
        replication_info = data["replication"]
        replication_list = []
        table_append(replication_list, "usename", "application_name", "client_addr", "state", "sync_state",
                     "sync_priority")
        for item in replication_info:
            table_append(replication_list, item["usename"], item["application_name"], item["client_addr"],
                         item["state"], item["sync_state"], item["sync_priority"])
        metric.append(dict(index_id=2310004, content=replication_list))
    else:
        vals_append("received_location", data["xlog"]["received_location"])
        vals_append("replayed_location", data["xlog"]["replayed_location"])
        vals_append("replayed_timestam", data["xlog"]["replayed_timestamp"])
        vals_append("paused", data["xlog"]["paused"])
    vals_append("timeline", data["timeline"])
    vals_append("database_system_identifier", data["database_system_identifier"])
    vals_append("patroni_version", data["patroni"]["version"])
    vals_append("patroni_scope", data["patroni"]["scope"])
    vals_append("ip", ip)
    metric.append(dict(index_id=2310001, value=vals))


def config_info():
    """
    {
  "ttl": 30,
  "loop_wait": 10,
  "retry_timeout": 10,
  "maximum_lag_on_failover": 1048576,
  "postgresql": {
    "use_pg_rewind": true,
    "use_slots": true,
    "parameters": {
      "wal_level": "logical",
      "wal_log_hints": "on"
    }
  }
}
    """
    data = get_response("config")
    vals_append("ttl", data["ttl"])
    vals_append("loop_wait",data["loop_wait"])
    vals_append("retry_timeout",data["retry_timeout"])
    vals_append("maximum_lag_on_failover",data["maximum_lag_on_failover"])
    vals_append("use_pg_rewind",data["postgresql"]["use_pg_rewind"])
    vals_append("use_slots",data["postgresql"]["use_slots"])
    para_dict = data["postgresql"]["parameters"]
    for k,v in para_dict.items():
      vals_append(k,v)
    metric.append(dict(index_id=2310002, value=vals))

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
        cluster_info()
        health_info()
        config_info()
    except requests.exceptions.RequestException as e:
        metric= {}
    print('{"cib":' + json.dumps(metric) + '}')

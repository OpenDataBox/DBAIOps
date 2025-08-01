import json
import sys
import warnings
from collections import Counter
from datetime import datetime

sys.path.append('/usr/software/knowl')
import numpy as np
from huawei_comm import request_comm, get_days

warnings.filterwarnings("ignore")


def get_huawei_storage_health():
    vals = []
    metric = []

    get_request, request_url, deviceid, url = request_comm()

    def vals_append(key, value):
        if isinstance(value, list):
            vals.append(dict(index_id=key, value=value))
        else:
            vals.append(dict(index_id=key, value=str(value)))

    def get_size(key):
        size = round(512 * int(data[key]) / 1024 / 1024, 2)
        return str(size)

    def get_info(module, extra=False):
        url = request_url(module=module, extra=extra)
        response = get_request(url=url)
        data = response.json()["data"]
        return data

    def cs(val, dt=False):
        return val.strftime('%Y-%m-%d %H:%M:%S') if dt else str(val) if val else ''

    def encap10(row, targetId):
        return dict(uid_c=targetId, recorddt_d=str(cs(datetime.now(), True)), hostid_c=str(row[0]),
                    hostname_c=str(row[1]), ip_c=str(row[2]), c1_n=str(row[3]),
                    c2_n=str(row[4]),
                    c3_n=str(row[5]), c4_n=str(row[6]), c5_n=str(row[7]), c6_n=str(row[8]))

    def encap9(row, targetId):
        return dict(uid_c=targetId, recorddt_d=str(cs(datetime.now(), True)), ctrlid_c=str(row[0]),
                    c1_n=str(row[1]), c2_n=str(row[2]), c3_n=str(row[3]), c4_n=str(row[4]), c5_n=str(row[5]),
                    c6_n=str(row[6]),
                    c7_n=str(row[7]), c8_n=str(row[8]), c9_n=str(row[9]), c10_n=str(row[10]), c11_n=str(row[11]),
                    c12_n=str(row[12]))

    def encap7(row, targetId):
        return dict(uid_c=targetId, recorddt_d=str(cs(datetime.now(), True)), ctrlid_c=str(row[0]),
                    c1_n=str(row[1]), c2_n=str(row[2]), c3_n=str(row[3]), c4_n=str(row[4]), c5_n=str(row[5]),
                    c6_n=str(row[6]))

    def encap8(row, targetId):
        return dict(uid_c=targetId, recorddt_d=str(cs(datetime.now(), True)), filesystemid_c=str(row[0]),
                    c1_n=str(row[1]), c2_n=str(row[2]), c3_n=str(row[3]), c4_n=str(row[4]), c5_n=str(row[5]),
                    c6_n=str(row[6]), c7_n=str(row[7]), c8_n=str(row[8]), c9_n=str(row[9]), c10_n=str(row[10]))

    # 系统信息
    data = get_info(module="system", extra=True)
    vals_append("4090000","连接成功")
    vals_append("4090001", data["HEALTHSTATUS"])  # 健康状态
    vals_append("4090002", data["RUNNINGSTATUS"])  # 运行状态
    vals_append("4090003", get_size("STORAGEPOOLRAWCAPACITY"))  # 存储池裸盘总容量
    vals_append("4090004", get_size("STORAGEPOOLCAPACITY"))  # 存储池总容量
    vals_append("4090005", get_size("STORAGEPOOLFREECAPACITY"))  # 存储池剩余容量
    vals_append("4090006", get_size("STORAGEPOOLUSEDCAPACITY"))  # 存储池已用容量
    vals_append("4090007", get_size("STORAGEPOOLHOSTSPARECAPACITY"))  # 存储池热备空间容量
    vals_append("4090008", get_size("FREEDISKSCAPACITY"))  # 空闲盘裸盘总容量
    vals_append("4090009", get_size("MEMBERDISKSCAPACITY"))  # 加入硬盘域的裸盘总容量
    vals_append("4090010", get_size("UNAVAILABLEDISKSCAPACITY"))  # 不可用磁盘总容量
    vals_append("4090011", get_size("THICKLUNSALLOCATECAPACITY"))  # 普通Lun已分配总容量
    vals_append("4090012", get_size("THICKLUNSUSEDCAPACITY"))  # 普通lun已写数据总量
    vals_append("4090013", get_size("THINLUNSALLOCATECAPACITY"))  # thin lun已分配总容量
    vals_append("4090014", get_size("THINLUNSMAXCAPACITY"))  # thin lun对主机可视容量
    vals_append("4090015", get_size("THINLUNSUSEDCAPACITY"))  # thin lun已写数据总量
    if 'TOTALCAPACITY' in data.keys():
        vals_append("4090016", get_size("TOTALCAPACITY"))  # 系统总容量
    if "USEDCAPACITY" in data.keys():
        vals_append("4090017", get_size("USEDCAPACITY"))  # 系统已用容量

    storagepool_used_pct = host_spare_pct = 0
    if int(data["STORAGEPOOLCAPACITY"]) > 0:
        storagepool_used_pct = round(int(data["STORAGEPOOLUSEDCAPACITY"]) / int(data["STORAGEPOOLCAPACITY"]) * 100, 2)
        host_spare_pct = round(int(data["STORAGEPOOLHOSTSPARECAPACITY"]) / int(data["STORAGEPOOLCAPACITY"]) * 100, 2)
    vals_append("4090019", storagepool_used_pct)  # 存储池使用率
    vals_append("4090020", host_spare_pct)  # 热备空间占存储池总容量百分比
    pct = round(int(data["FREEDISKSCAPACITY"]) * 100 / (
            int(data["FREEDISKSCAPACITY"]) + int(data["MEMBERDISKSCAPACITY"]) + int(
        data["UNAVAILABLEDISKSCAPACITY"])), 2)
    vals_append("4090021", pct)  # 空闲裸盘占总容量百分比
    # server status
    server_status_url = request_url(module="server/status")
    server_status_response = get_request(url=server_status_url)
    data = server_status_response.json()["data"]
    vals_append("4090018", data["status"])  # 设备状态
    # 机框

    enclosure_url = request_url(module="enclosure")
    enclosure_response = get_request(url=enclosure_url)
    data = enclosure_response.json()["data"]

    vals_append("4090119", len(data))  # 机框数量
    health_counter = Counter([item["HEALTHSTATUS"] for item in data])
    running_counter = Counter([item["RUNNINGSTATUS"] for item in data])
    vals_append("4090120", health_counter["2"])  # 故障机框数量
    vals_append("4090121", running_counter["28"])  # 离线机框数量

    # 控制器
    controller_url = request_url(module="controller")
    controller_response = get_request(url=controller_url)
    data = controller_response.json()["data"]

    ctrl_id_list = [item["ID"] for item in data]

    vals_append("4090222", len(data))  # 控制器数量

    health_counter = Counter([item["HEALTHSTATUS"] for item in data])
    vals_append("4090223", health_counter["0"])  # 未知状态控制器数量
    vals_append("4090224", health_counter["2"])  # 故障控制器数量
    vals_append("4090225", health_counter["9"])  # 不一致状态控制器数量

    # ctrl_health_list = []
    # for item in data:
    #     ctrl_health_list.append(dict(name=item["ID"],value=str(item["HEALTHSTATUS"])))
    # vals_append("4090226",ctrl_health_list) # 控制器健康状态

    vals_append("4090226", [dict(name=item["ID"], value=str(item["HEALTHSTATUS"])) for item in data])

    # expboard
    expboard_url = request_url(module="expboard")
    expboard_response = get_request(url=expboard_url)
    data = expboard_response.json()["data"]

    vals_append("4090250", len(data))  # 级联板个数
    health_counter = Counter([item["HEALTHSTATUS"] for item in data])
    vals_append("4090251", health_counter["2"])  # 故障级联板个数
    vals_append("4090252", health_counter["0"])  # 未知状态级联板个数

    # 接口模块

    intf_module_url = request_url(module="intf_module")
    intf_module_response = get_request(url=intf_module_url)
    data = intf_module_response.json()["data"]

    vals_append("4090350", len(data))  # 接口板个数
    health_counter = Counter([item["HEALTHSTATUS"] for item in data])
    vals_append("4090351", health_counter["2"])  # 故障接口板个数
    vals_append("4090352", health_counter["0"])  # 未知状态级接口个数

    # 硬盘
    disk_url = request_url(module="disk")
    disk_response = get_request(url=disk_url)
    data = disk_response.json()["data"]

    vals_append("4090326", len(data))  # 硬盘数量
    logictype_counter = Counter([item["LOGICTYPE"] for item in data])
    vals_append("4090327", logictype_counter["1"])  # 空闲盘数量
    vals_append("4090328", logictype_counter["3"])  # 热备盘数量
    health_counter = Counter([item["HEALTHSTATUS"] for item in data])
    vals_append("4090329", health_counter["2"])  # 故障盘数量
    vals_append("4090330", health_counter["3"])  # 即将故障的磁盘数量
    vals_append("4090331", health_counter["0"] + health_counter["2"] + health_counter["3"])  # 非正常运行磁盘数量
    running_counter = Counter([item["RUNNINGSTATUS"] for item in data])
    vals_append("4090332", running_counter["16"])  # 正在重构的磁盘数量
    remain_life_list = [item["REMAINLIFE"] for item in data if 0 < int(item["REMAINLIFE"]) < 100]
    vals_append("4090333", len(remain_life_list))  # 寿命小于100天的磁盘个数
    temperature = [item["TEMPERATURE"] for item in data if int(item["TEMPERATURE"]) > 58]
    vals_append("4090334", len(temperature))  # 超温磁盘个数
    health_mark_list = [item["HEALTHMARK"] for item in data if 0 < int(item["HEALTHMARK"]) < 80]
    vals_append("4090335", len(health_mark_list))  # 健康评分小于80的磁盘个数
    health_mark90_list = [item["HEALTHMARK"] for item in data if 0 < int(item["HEALTHMARK"]) < 90]
    vals_append("4090336", len(health_mark90_list))  # 健康评分小于90的磁盘个数
    health_mark_list = [item["HEALTHMARK"] for item in data if 0 < int(item["HEALTHMARK"]) < 70]
    vals_append("4090339", len(health_mark_list))  # 健康评分小于70的磁盘个数
    health_mark_list = [item["HEALTHMARK"] for item in data if 0 < int(item["HEALTHMARK"]) < 60]
    vals_append("4090340", len(health_mark_list))  # 健康评分小于60的磁盘个数
    health_mark90_list = [item["HEALTHMARK"] for item in data if 0 < int(item["HEALTHMARK"]) < 50]
    vals_append("4090341", len(health_mark90_list))  # 健康评分小于50的磁盘个数
    health_mark20_list = [item["HEALTHMARK"] for item in data if 0 < int(item["HEALTHMARK"]) < 20]
    vals_append("4090346", len(health_mark20_list))  # 健康评分小于20的磁盘个数
    runtime_list = [int(item["RUNTIME"]) for item in data]
    vals_append("4090337", max(runtime_list))  # 磁盘最大使用天数
    vals_append("4090338", int(np.mean(runtime_list)))  # 磁盘平均使用天数
    temperature = [item["TEMPERATURE"] for item in data if int(item["TEMPERATURE"]) > 35]
    vals_append("4090342", len(temperature))  # 温度超过35度的磁盘个数
    temperature = [item["TEMPERATURE"] for item in data if int(item["TEMPERATURE"]) > 40]
    vals_append("4090343", len(temperature))  # 温度超过40度的磁盘个数
    temperature = [item["TEMPERATURE"] for item in data if int(item["TEMPERATURE"]) > 45]
    vals_append("4090344", len(temperature))  # 温度超过45度的磁盘个数
    temperature = [item["TEMPERATURE"] for item in data if int(item["TEMPERATURE"]) > 50]
    vals_append("4090345", len(temperature))  # 温度超过50度的磁盘个数
    runtime_list180 = [int(item["RUNTIME"]) for item in data if 0 <= int(item["RUNTIME"]) <= 180]
    vals_append("4090347", len(runtime_list180))  # 磨合期磁盘数量
    runtime_list1095 = [int(item["RUNTIME"]) for item in data if 180 <= int(item["RUNTIME"]) <= 1095]
    vals_append("4090348", len(runtime_list1095))  # 稳定期磁盘数量
    runtime_listmax = [int(item["RUNTIME"]) for item in data if 1095 <= int(item["RUNTIME"]) ]
    vals_append("4090349", len(runtime_listmax))  # 老化期磁盘数量


    # power

    power_url = request_url(module="power")
    power_response = get_request(url=power_url)
    data = power_response.json()["data"]

    vals_append("4090434", len(data))
    health_counter = Counter([item["HEALTHSTATUS"] for item in data])
    vals_append("4090435", health_counter["2"])  # 故障电源数量
    running_counter = Counter([item["RUNNINGSTATUS"] for item in data])
    vals_append("4090436", running_counter["28"])  # 离线电源数量

    voltage = [item["OUTPUTVOLTAGE"] for item in data if item["OUTPUTVOLTAGE"] != "0"]
    vals_append("4090432", len(voltage))  # 电压不正常电源数量
    temperature = [item["TEMPERATURE"] for item in data if int(item["TEMPERATURE"]) > 45]
    vals_append("4090433", len(temperature))  # 超温电源数量

    # BBU
    backup_power_url = request_url(module="backup_power")
    backup_power_response = get_request(url=backup_power_url)
    data = backup_power_response.json()["data"]

    backup_power_vals = []

    vals_append("4090537", len(data))
    health_counter = Counter([item["HEALTHSTATUS"] for item in data])
    vals_append("4090538", health_counter["2"])  # 故障备电源数量
    vals_append("4090539", health_counter["3"])  # 即将故障备电源数量
    vals_append("4090540", health_counter["12"])  # 电量不足的备电源数量
    running_counter = Counter([item["RUNNINGSTATUS"] for item in data])
    vals_append("4090541", running_counter["28"])  # 离线备电源数量
    vals_append("4090542",
                len([item["REMAINLIFEDAYS"] for item in data if
                     0 < int(item["REMAINLIFEDAYS"]) < 100]))  # 寿命小于100天的备电源数量
    days_list = [get_days(item["MANUFACTUREDDATE"]) for item in data if get_days(item["MANUFACTUREDDATE"]) > 365 * 5]
    vals_append("4090543", len(days_list))  # 出厂时间超过5年的备电源数量
    voltage = [item["VOLTAGE"] for item in data if item["VOLTAGE"] != "110"]
    vals_append("4090545", len(voltage))  # 电压不正常备电源数量
    vals_append("4090544", "0")  # 超温备电源数量
    # fan

    fan_url = request_url(module="fan")
    fan_response = get_request(url=fan_url)
    data = fan_response.json()["data"]
    vals_append("4090644", len(data))
    health_counter = Counter([item["HEALTHSTATUS"] for item in data])
    vals_append("4090645", health_counter["2"])  # 故障风扇个数
    vals_append("4090646", health_counter["0"] + health_counter["2"])  # 非正常运行的风扇个数
    runlevel_counter = Counter([item["RUNLEVEL"] for item in data])
    vals_append("4090647", runlevel_counter["2"])  # 高档位运行风扇个数

    # fan_ctrl_module 不支持

    fan_ctrl_module_url = request_url(module="fan_ctrl_module")
    fan_ctrl_module_response = get_request(url=fan_ctrl_module_url)
    data = fan_ctrl_module_response.json()
    code = data["error"]["code"]
    if code == -1:
        vals_append("4090650", "0")
        vals_append("4090651", "0")
        vals_append("4090652", "0")
        vals_append("4090653", "0")
    else:
        data = fan_ctrl_module_response.json()["data"]
        vals_append("4090650", len(data))  # 风扇控制模块个数
        health_counter = Counter([item["HEALTHSTATUS"] for item in data])
        vals_append("4090651", health_counter["2"])  # 故障风扇控制模块
        running_counter = Counter([item["RUNNINGSTATUS"] for item in data])
        vals_append("4090653", running_counter["103"])  # 上电失败风扇控制模板
        running = [item["RUNNINGSTATUS"] for item in data if item["RUNNINGSTATUS"] not in ["1", "2"]]
        vals_append("4090652", len(running))  # 未正常运行风扇控制模块

    # sas_port
    sas_port_url = request_url(module="sas_port")
    sas_port_response = get_request(url=sas_port_url)
    data = sas_port_response.json()["data"]
    vals_append("4090748", len(data))  # sas port count
    health_counter = Counter([item["HEALTHSTATUS"] for item in data])
    vals_append("4090749", health_counter["2"])  # 故障SAS端口个数
    vals_append("4090750", health_counter["3"])  # 即将故障SAS端口个数
    # fc_port
    fc_port_url = request_url(module="fc_port")
    fc_port_response = get_request(url=fc_port_url)
    data = fc_port_response.json()["data"]
    vals_append("4090851", len(data))
    health_counter = Counter([item["HEALTHSTATUS"] for item in data])
    vals_append("4090852", health_counter["2"])  # 故障FC端口个数
    vals_append("4090853", health_counter["3"])  # 即将故障FC端口个数
    running_counter = Counter([item["RUNNINGSTATUS"] for item in data])
    vals_append("4090854", running_counter["10"])  # 已连接端口数
    vals_append("4090855", runlevel_counter["11"])  # 未连接端口数
    vals_append("4090856", round(running_counter["11"] / len(data) * 100, 2))  # FC端口空闲比例
    # FC启动器
    fc_initiator_url = request_url(module="fc_initiator")
    fc_initiator_response = get_request(url=fc_initiator_url)
    data = fc_initiator_response.json()["data"]
    vals_append("4090954", len(data))  # fc 启动器数量
    running_counter = Counter([item["RUNNINGSTATUS"] for item in data])
    vals_append("4090955", running_counter["28"])  # 离线启动器数量
    health_list = [item["HEALTHSTATUS"] for item in data if item["HEALTHSTATUS"] not in ["1"]]
    vals_append("4090956", len(health_list))  # 异常FC启动器数量

    # lun
    lun_param = {"range": "[0-100]"}
    lun_url = request_url(module="lun")
    lun_response = get_request(url=lun_url, params=lun_param)
    if "data" in lun_response.json():
        data = lun_response.json()["data"]
        vals_append("4091056", len(data))
        health_counter = Counter([item["HEALTHSTATUS"] for item in data])
        vals_append("4091057", health_counter["2"])  # 故障LUN个数

    # lungroup
    lungroup_url = request_url(module="lungroup")
    lungroup_response = get_request(url=lungroup_url)
    data = lungroup_response.json()["data"]
    vals_append("4091158", len(data))

    # 存储池
    storagepool_url = request_url(module="storagepool")
    storagepool_response = get_request(url=storagepool_url)
    data = storagepool_response.json()["data"]
    vals_append("4091259", len(data))
    health_counter = Counter([item["HEALTHSTATUS"] for item in data])
    vals_append("4091260", health_counter["2"])  # 故障存储池个数
    vals_append("4091258", health_counter["5"])  # 降级存储池个数
    running_counter = Counter([item["RUNNINGSTATUS"] for item in data])
    vals_append("4091257", running_counter["16"])  # 重构存储池个数

    # 文件系统
    filesystem_url = request_url(module="filesystem")
    filesystem_response = get_request(url=filesystem_url)
    data = filesystem_response.json()["data"]
    vals_append("4091300", len(data))
    running_counter = Counter([item["RUNNINGSTATUS"] for item in data])
    vals_append("4091301", running_counter["28"])  # 离线文件系统数量
    y = len(
        [item["AVAILABLEANDALLOCCAPACITYRATIO"] for item in data if int(item["AVAILABLEANDALLOCCAPACITYRATIO"]) > 85])
    vals_append("4091302", y)  # 文件系统已用容量占比超过85%的文件系统个数
    filesystem_id_list = [item["ID"] for item in data]

    # currentalarm
    currentalarm_url = request_url(module="alarm/currentalarm")
    currentalarm_response = get_request(url=currentalarm_url)
    data = currentalarm_response.json()["data"]
    vals_append("4091261", len(data))
    ss = ""
    stat_data_id_list_first = "21,22,68,69,110,120"
    stat_data_id_list_last = "370,371,384,385,93,95"

    # 控制器性能指标
    metric_first = []
    metric_second = []
    metric = []

    for item in ctrl_id_list:
        query_parameter = {"CMO_STATISTIC_UUID": f"207:{item}",
                           "CMO_STATISTIC_DATA_ID_LIST": stat_data_id_list_first}
        performance_url = request_url(module="performance/statdata")
        performance_response = get_request(url=performance_url, params=query_parameter)
        if performance_response.json()["error"]["code"] == 0:
            data = performance_response.json()["data"][0]["CMO_STATISTIC_DATA_LIST"].split(',')
        else:
            performance_url = request_url(module="performace_statistic/cur_statistic_data")
            performance_response = get_request(url=performance_url, params=query_parameter)
            code = performance_response.json()["error"]["code"]
            if code == 83890436:
                data = []
            else:
                data = performance_response.json()["data"][0]["CMO_STATISTIC_DATA_LIST"].split(',')
        metric_first.append([int(item) for item in data])

    for item in ctrl_id_list:
        query_parameter = {"CMO_STATISTIC_UUID": f"207:{item}",
                           "CMO_STATISTIC_DATA_ID_LIST": stat_data_id_list_last}
        performance_url = request_url(module="performance/statdata")
        performance_response = get_request(url=performance_url, params=query_parameter)
        if performance_response.json()["error"]["code"] == 0:
            data = performance_response.json()["data"][0]["CMO_STATISTIC_DATA_LIST"].split(',')
        else:
            performance_url = request_url(module="performace_statistic/cur_statistic_data")
            performance_response = get_request(url=performance_url, params=query_parameter)
            code = performance_response.json()["error"]["code"]
            if code != 0:
                data = []
            else:
                data = performance_response.json()["data"][0]["CMO_STATISTIC_DATA_LIST"].split(',')
        metric_second.append([int(item) for item in data])

    if metric_second:
        # ss = 'uid_c,recorddt_d,ctrlid_c,c1_n,c2_n,c3_n,c4_n,c5_n,c6_n,c7_n,c8_n,c9_n,c10_n,c11_n,c12_n'
        for index, item in enumerate(metric_first):
            temp = item + metric_second[index]
            metric.append(temp)
    else:
        # ss = 'uid_c,recorddt_d,ctrlid_c,c1_n,c2_n,c3_n,c4_n,c5_n,c6_n'
        metric = metric_first.copy()
    # 控制器性能指标采集入库程序开始
    rs = []
    for index, id in enumerate(ctrl_id_list):
        temp = [id] + metric[index]
        rs.append(temp)

    # rs_json = []
    # crtlstr = ss = ''
    # sprt = CommUtil.getSeparator()
    # if rs:
    #     for row in rs:
    #         if len(row) == 13:
    #             rs_json.append(encap9(row, target_id))
    #         elif len(row) == 7:
    #             rs_json.append(encap7(row, target_id))
    #     crtlstr += '%s{"tb":"h_controller_performance","colname":"%s",' % (sprt, ss)
    #     crtlstr += ('"col":' + json.dumps(rs_json) + '}')

    # 控制器性能指标采集入库程序结束
    temp_list = list(zip(*metric))
    rs_list = [max(item) for item in temp_list]
    vals_append("4098101", max(temp_list[0]))  # 控制器最大块带宽(MB/s)
    vals_append("4098102", max(temp_list[1]))  # 控制器最大平均IOPS（IO/s）
    vals_append("4098103", max(temp_list[2]))  # 控制器最大平均CPU利用率
    vals_append("4098104", max(temp_list[3]))  # 控制器最大平均Cache利用率
    vals_append("4098105", max(temp_list[4]))  # 控制器最大Cache读利用率
    vals_append("4098106", max(temp_list[5]))  # 控制器最大Cache写利用率

    vals_append("4098151", [dict(name=item[0], value=str(item[1])) for item in rs])
    vals_append("4098152", [dict(name=item[0], value=str(item[2])) for item in rs])
    vals_append("4098153", [dict(name=item[0], value=str(item[3])) for item in rs])
    vals_append("4098154", [dict(name=item[0], value=str(item[4])) for item in rs])
    vals_append("4098155", [dict(name=item[0], value=str(item[5])) for item in rs])
    vals_append("4098156", [dict(name=item[0], value=str(item[6])) for item in rs])

    if metric_second:
        vals_append("4098107", max(temp_list[6]))  # 控制器平均响应时间（us）
        vals_append("4098108", max(temp_list[7]))  # 控制器最大I/O响应时间(us)
        vals_append("4098109", max(temp_list[8]))  # 控制器最大平均读I/O响应时间(us)
        vals_append("4098110", max(temp_list[9]))  # 控制器最大平均写I/O响应时间(us)
        vals_append("4098111", min(temp_list[10]))  # 控制器最小读Cache命中率(%)
        vals_append("4098112", min(temp_list[11]))  # 控制器最小写Cache命中率(%)

        vals_append("4098157", [dict(name=item[0], value=str(item[7])) for item in rs])
        vals_append("4098158", [dict(name=item[0], value=str(item[8])) for item in rs])
        vals_append("4098159", [dict(name=item[0], value=str(item[9])) for item in rs])
        vals_append("4098160", [dict(name=item[0], value=str(item[10])) for item in rs])
        vals_append("4098161", [dict(name=item[0], value=str(item[11])) for item in rs])
        vals_append("4098162", [dict(name=item[0], value=str(item[12])) for item in rs])
    else:
        vals_append("4098107", 0)  # 控制器平均响应时间（us）
        vals_append("4098108", 0)  # 控制器最大I/O响应时间(us)
        vals_append("4098109", 0)  # 控制器最大平均读I/O响应时间(us)
        vals_append("4098110", 0)  # 控制器最大平均写I/O响应时间(us)
        vals_append("4098111", 0)  # 控制器最小读Cache命中率(%)
        vals_append("4098112", 0)  # 控制器最小写Cache命中率(%)

    # 主机
    host_param = {"range": "[0-100]"}
    host_url = request_url(module="host")
    host_response = get_request(url=host_url, params=host_param)
    if "data" in host_response.json():
        data = host_response.json()["data"]
    else:
        data = []
    host_id_list = [(item["ID"], item["NAME"], item["IP"]) for item in data]
    metric = []

    for item in host_id_list:
        query_parameter = {"CMO_STATISTIC_UUID": f"21:{item[0]}", "CMO_STATISTIC_DATA_ID_LIST": "18,19,21,22,370,307"}
        performance_url = request_url(module="performance/statdata")
        performance_response = get_request(url=performance_url, params=query_parameter)
        if performance_response.json()["error"]["code"] == 0:
            data = performance_response.json()["data"][0]["CMO_STATISTIC_DATA_LIST"].split(',')
        else:
            performance_url = request_url(module="performace_statistic/cur_statistic_data")
            performance_response = get_request(url=performance_url, params=query_parameter)
            code = performance_response.json()["error"]["code"]
            if code == 83890436:
                data = []
            else:
                data = performance_response.json()["data"][0]["CMO_STATISTIC_DATA_LIST"].split(',')
            # data = performance_response.json()["data"][0]["CMO_STATISTIC_DATA_LIST"].split(',')
        metric.append([int(item) for item in data])
    # 主机性能指标入库程序开始
    rs = []
    for index, item in enumerate(host_id_list):
        temp = list(item) + metric[index]
        rs.append(temp)

    # rs_json = []
    # outstr = ''
    # sprt = CommUtil.getSeparator()
    # if rs:
    #     for row in rs:
    #         if len(row) == 9:
    #             rs_json.append(encap10(row, target_id))
    #     ss = 'uid_c,recorddt_d,hostid_c,hostname_c,ip_c,c1_n,c2_n,c3_n,c4_n,c5_n,c6_n'
    #     outstr += '%s{"tb":"h_host_performance","colname":"%s",' % (sprt, ss)
    #     outstr += ('"col":' + json.dumps(rs_json) + '}')
    # 主机性能指标入库程序结束
    temp_list = list(zip(*metric))
    rs_list = [max(item) for item in temp_list]
    if rs:
        vals_append("4098201", max(temp_list[0]))  # 主机最大利用率(%)
        vals_append("4098202", max(temp_list[1]))  # 主机最大队列长度(个）
        vals_append("4098203", max(temp_list[2]))  # 主机最大块带宽（MB/s）
        vals_append("4098204", max(temp_list[3]))  # 主机最大平均IOPS(IO/s)
        vals_append("4098205", max(temp_list[4]))  # 主机最大平均IO响应时间(us)
        vals_append("4098206", max(temp_list[5]))  # 主机最大最大IOPS（IO/s)

        vals_append("4098251", [dict(name=item[0], value=str(item[3])) for item in rs])
        vals_append("4098252", [dict(name=item[0], value=str(item[4])) for item in rs])
        vals_append("4098253", [dict(name=item[0], value=str(item[5])) for item in rs])
        vals_append("4098254", [dict(name=item[0], value=str(item[6])) for item in rs])
        vals_append("4098255", [dict(name=item[0], value=str(item[7])) for item in rs])
        vals_append("4098256", [dict(name=item[0], value=str(item[8])) for item in rs])

    # 文件系统性能指标
    metric = []
    for item in filesystem_id_list:
        query_parameter = {"CMO_STATISTIC_UUID": f"40:{item}",
                           "CMO_STATISTIC_DATA_ID_LIST": "23,26,123,124,182,232,233,523,524,525"}
        performance_url = request_url(module="performance/statdata")
        performance_response = get_request(url=performance_url, params=query_parameter)
        if performance_response.json()["error"]["code"] == 0:
            data = performance_response.json()["data"][0]["CMO_STATISTIC_DATA_LIST"].split(',')
        else:
            performance_url = request_url(module="performace_statistic/cur_statistic_data")
            performance_response = get_request(url=performance_url, params=query_parameter)
            code = performance_response.json()["error"]["code"]
            if code == 83890436:
                data = []
            else:
                data = performance_response.json()["data"][0]["CMO_STATISTIC_DATA_LIST"].split(',')
        metric.append([int(item) for item in data])

    # 文件系统性能指标采集入库程序开始
    rs = []
    for index, id in enumerate(filesystem_id_list):
        temp = [id] + metric[index]
        rs.append(temp)

    # rs_json = []
    # filesystemstr = ''
    # sprt = CommUtil.getSeparator()
    # if rs:
    #     for row in rs:
    #         rs_json.append(encap8(row, target_id))
    #     ss = 'uid_c,recorddt_d,filesystemid_c,c1_n,c2_n,c3_n,c4_n,c5_n,c6_n,c7_n,c8_n,c9_n,c10_n'
    #     filesystemstr += '%s{"tb":"h_filesystem_performance","colname":"%s",' % (sprt, ss)
    #     filesystemstr += ('"col":' + json.dumps(rs_json) + '}')

    # 控制器性能指标采集入库程序结束
    temp_list = list(zip(*metric))
    if rs:
        vals_append("4098301", max(temp_list[0]))  # 文件系统最大读带宽(MB/s)
        vals_append("4098302", max(temp_list[1]))  # 文件系统最大写带宽(MB/s)
        vals_append("4098303", max(temp_list[2]))  # 文件系统最大读带宽(KB/s)
        vals_append("4098304", max(temp_list[3]))  # 文件系统最大写带宽(KB/s)
        vals_append("4098305", max(temp_list[4]))  # 文件系统最大OPS(个/s)
        vals_append("4098306", max(temp_list[5]))  # 文件系统最大读OPS(个/s)
        vals_append("4098307", max(temp_list[6]))  # 文件系统最大写OPS(个/s)
        vals_append("4098308", max(temp_list[7]))  # 文件系统最大服务时间(us)
        vals_append("4098309", max(temp_list[8]))  # 文件系统最大平均读OPS响应时间(us)
        vals_append("4098310", max(temp_list[9]))  # 文件系统最大平均写OPS响应时间(us)

        vals_append("4098351", [dict(name=item[0], value=str(item[1])) for item in rs])
        vals_append("4098352", [dict(name=item[0], value=str(item[2])) for item in rs])
        vals_append("4098353", [dict(name=item[0], value=str(item[3])) for item in rs])
        vals_append("4098354", [dict(name=item[0], value=str(item[4])) for item in rs])
        vals_append("4098355", [dict(name=item[0], value=str(item[5])) for item in rs])
        vals_append("4098356", [dict(name=item[0], value=str(item[6])) for item in rs])
        vals_append("4098357", [dict(name=item[0], value=str(item[7])) for item in rs])
        vals_append("4098358", [dict(name=item[0], value=str(item[8])) for item in rs])
        vals_append("4098359", [dict(name=item[0], value=str(item[9])) for item in rs])
        vals_append("4098360", [dict(name=item[0], value=str(item[10])) for item in rs])

    # loginout
    # response = requests.request("DELETE", url, headers=headers, cookies=cookie, verify=False)
    response = get_request(method="DELETE", url=url)
    msg = '{"results":' + json.dumps(vals) + '}'
    # msg = '{"metric":' + json.dumps(vals) + '}'
    return msg


if __name__ == '__main__':
    msg = get_huawei_storage_health()
    print(msg)

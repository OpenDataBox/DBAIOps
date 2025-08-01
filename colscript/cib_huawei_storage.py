import json
import sys

sys.path.append('/usr/software/knowl')
from huawei_comm import *

warnings.filterwarnings("ignore")

vals = []
metric = []


def vals_append(key, value):
    vals.append(dict(name=key, value=value))


get_request, request_url, deviceid, url = request_comm()


def get_info(module, extra=False):
    url = request_url(module=module, extra=extra)
    response = get_request(url=url)
    data = response.json()["data"]
    return data


# 系统信息
data = get_info(module="system", extra=True)


def get_size(key):
    size = int(data["SECTORSIZE"]) * int(data[key])
    return hr_bytes(size)


def get_item_size(key):
    if "SECTORSIZE" in item.keys():
        size = int(item["SECTORSIZE"]) * int(item[key])
    else:
        size = 512 * int(item[key])
    if key in ["COMPRESSIONSAVEDCAPACITY", "TOTALSAVEDCAPACITY", "AVAILABLECAPCITY"]:
        size = 512 * int(item[key])
    return hr_bytes(size)


def table_append(tab_list, c1=None, c2=None, c3=None, c4=None, c5=None, c6=None, c7=None, c8=None, c9=None, c10=None):
    tab_list.append(dict(c1=c1, c2=c2, c3=c3, c4=c4, c5=c5, c6=c6, c7=c7, c8=c8, c9=c9, c10=c10))


vals_append("id", data["ID"])  # 系统ID
vals_append("name", data["NAME"])  # 系统名称
vals_append("location", data["LOCATION"])  # 位置信息
vals_append("product_mode", get_product_mode(data["PRODUCTMODE"]))  # 产品型号
vals_append("product_version", data["PRODUCTVERSION"])  # 产品版本
vals_append("health_status", get_health_status(data["HEALTHSTATUS"]))  # 健康状态
vals_append("running_status", get_running_status(data["RUNNINGSTATUS"]))  # 运行状态
vals_append("device_id", deviceid)  # 设备ID
vals_append("storage_pool_raw_capacity", get_size("STORAGEPOOLRAWCAPACITY"))  # 存储池裸盘总容量
vals_append("storage_pool_capacity", get_size("STORAGEPOOLCAPACITY"))  # 存储池总容量
vals_append("storage_pool_free_capacity", get_size("STORAGEPOOLFREECAPACITY"))  # 存储池剩余容量
vals_append("storage_pool_used_capacity", get_size("STORAGEPOOLUSEDCAPACITY"))  # 存储池已用容量
vals_append("storage_pool_host_spare_capacity", get_size("STORAGEPOOLHOSTSPARECAPACITY"))  # 存储池热备空间容量
vals_append("free_disk_capacity", get_size("FREEDISKSCAPACITY"))  # 空闲盘裸盘总容量
vals_append("member_disk_capacity", get_size("MEMBERDISKSCAPACITY"))  # 加入硬盘域的裸盘总容量
vals_append("unavailabled_disk_capacity", get_size("UNAVAILABLEDISKSCAPACITY"))  # 不可用磁盘总容量
vals_append("vasa_support_block", data["VASA_SUPPORT_BLOCK"])  # 支持的块访问接口类型
vals_append("wwn", data["wwn"])  # wwn
vals_append("thick_luns_allocate_capacity", get_size("THICKLUNSALLOCATECAPACITY"))  # 普通Lun已分配总容量
vals_append("thick_luns_used_capacity", get_size("THICKLUNSUSEDCAPACITY"))  # 普通lun已写数据总量
vals_append("thin_luns_allocate_capacity", get_size("THINLUNSALLOCATECAPACITY"))  # thin lun已分配总容量
vals_append("thin_luns_max_capacity", get_size("THINLUNSMAXCAPACITY"))  # thin lun对主机可视容量
vals_append("thin_luns_used_capacity", get_size("THINLUNSUSEDCAPACITY"))  # thin lun已写数据总量
if 'TOTALCAPACITY' in data.keys():
    vals_append("total_capacity", get_size("TOTALCAPACITY"))  # 系统总容量
if "USEDCAPACITY" in data.keys():
    vals_append("used_capacity", get_size("USEDCAPACITY"))  # 系统已用容量

# system_timezone
system_timezone_url = request_url(module="system_timezone")
system_timezone_response = get_request(url=system_timezone_url)
data = system_timezone_response.json()["data"][0]
vals_append("system_timezone", data["CMO_SYS_TIME_ZONE_NAME"])  # 时区信息

# server status
server_status_url = request_url(module="server/status")
server_status_response = get_request(url=server_status_url)
data = server_status_response.json()["data"]
vals_append("server_status", get_server_status(data["status"]))  # 设备状态
# 机框

enclosure_url = request_url(module="enclosure")
enclosure_response = get_request(url=enclosure_url)
data = enclosure_response.json()["data"]

vals_append("enclosure_count", len(data))  # 机框数量
enclosure_vals = []

table_append(enclosure_vals, "机框编号", "机框名称", "位置", "健康状态", "运行状态")
for item in data:
    table_append(enclosure_vals, item["ID"], item["NAME"], item["LOCATION"],
                 get_health_status(item["HEALTHSTATUS"]), get_running_status(item["RUNNINGSTATUS"]))

metric.append(dict(index_id=4080002, content=enclosure_vals))
# 控制器
controller_url = request_url(module="controller")
controller_response = get_request(url=controller_url)
data = controller_response.json()["data"]

vals_append("controller_count", len(data))  # 控制器数量
controller_vals = []
table_append(controller_vals, "控制器ID", "控制器名称", "描述", "健康状态", "运行状态", "固件版本")
for item in data:
    table_append(controller_vals, item["ID"], item["NAME"], item["DESCRIPTION"],
                 get_health_status(item["HEALTHSTATUS"]), get_running_status(item["RUNNINGSTATUS"]), item["SOFTVER"])

metric.append(dict(index_id=4080003, content=controller_vals))
# expboard
expboard_url = request_url(module="expboard")
expboard_response = get_request(url=expboard_url)
data = expboard_response.json()["data"]
expboard_vals = []
if data:
    table_append(expboard_vals, "级联板ID", "级联板名称", "位置", "健康状态", "运行状态", "型号", "逻辑版本", "PCB版本", "SES版本")
    for item in data:
        table_append(expboard_vals, item["ID"], item["NAME"], item["LOCATION"], get_health_status(item["HEALTHSTATUS"]),
                     get_running_status(item["RUNNINGSTATUS"]), get_expboard_model(item["MODEL"]), item["LOGICVER"],
                     item["PCBVER"], item["SESVER"])

metric.append(dict(index_id=4080004, content=expboard_vals))
# 接口模块

intf_module_url = request_url(module="intf_module")
intf_module_response = get_request(url=intf_module_url)
data = intf_module_response.json()["data"]
intf_module_vals = []
if data:
    table_append(intf_module_vals, "接品模块ID", "名称", "位置", "健康状态", "运行状态", "型号", "逻辑版本", "PCB版本", "温度", "运行模式")
    for item in data:
        # if "RUNMODE" in item:
        #     run_mode = get_run_mode(item["RUNMODE"])
        # else:
        run_mode = ""
        table_append(intf_module_vals, item["ID"], item["NAME"], item["LOCATION"],
                     get_health_status(item["HEALTHSTATUS"]),
                     get_running_status(item["RUNNINGSTATUS"]), get_intf_module(item["MODEL"]), item["LOGICVER"],
                     item["PCBVER"],
                     item["TEMPERATURE"], run_mode)

metric.append(dict(index_id=4080005, content=intf_module_vals))
# 硬盘
disk_url = request_url(module="disk")
disk_response = get_request(url=disk_url)
data = disk_response.json()["data"]

vals_append("disk_count", len(data))  # 硬盘数量

disk_basic_vals = []
disk_run_vals = []
table_append(disk_basic_vals, "磁盘编号", "父对象编号", "位置", "健康状态", "运行状态", "硬盘类型", "硬盘接口类型", "磁盘大小", "接口带宽", "容量率")
table_append(disk_run_vals, "磁盘编号", "硬盘外形尺寸", "转速", "温度", "生产厂商", "序列号", "逻辑类型", "运行天数", "盘路径信息", "健康评分")
for item in data:
    table_append(disk_basic_vals, item["ID"], "机框" + item["PARENTID"], item["LOCATION"],
                 get_health_status(item["HEALTHSTATUS"]), get_running_status(item["RUNNINGSTATUS"]),
                 get_disk_type(item["DISKTYPE"]), get_diskif_type(item["DISKIFTYPE"]), get_item_size("SECTORS"),
                 item["BANDWIDTH"] + "Mbit/s",
                 item["CAPACITYUSAGE"])
    table_append(disk_run_vals, item["ID"], get_diskform(item["DISKFORM"]), item["SPEEDRPM"] + "RPM",
                 item["TEMPERATURE"] + "°C", item["MANUFACTURER"], item["SERIALNUMBER"],
                 get_logictype(item["LOGICTYPE"]), item["RUNTIME"] + "天", item["MULTIPATH"], item["HEALTHMARK"])

metric.append(dict(index_id=4080006, content=disk_basic_vals))
metric.append(dict(index_id=4080007, content=disk_run_vals))
# power

power_url = request_url(module="power")
power_response = get_request(url=power_url)
data = power_response.json()["data"]

vals_append("power_count", len(data))
power_vals = []
table_append(power_vals, "电源编号", "名称", "位置", "健康状态", "运行状态", "温度", "生产厂家", "型号", "生产日期", "序列号")
for item in data:
    table_append(power_vals, item["ID"], item["NAME"], item["LOCATION"], get_health_status(item["HEALTHSTATUS"]),
                 get_running_status(item["RUNNINGSTATUS"]), item["TEMPERATURE"], item["MANUFACTURER"], item["MODEL"],
                 item["PRODUCEDATE"], item["SERIALNUMBER"])

metric.append(dict(index_id=4080008, content=power_vals))
# BBU
backup_power_url = request_url(module="backup_power")
backup_power_response = get_request(url=backup_power_url)
data = backup_power_response.json()["data"]

backup_power_vals = []

vals_append("backup_power_count", len(data))

table_append(backup_power_vals, "名称", "位置", "健康状态", "运行状态", "当前电压", "剩余寿命", "放电次数", "固件版本", "生产日期", "控制器ID")
for item in data:
    table_append(backup_power_vals, item["NAME"], item["LOCATION"], get_health_status(item["HEALTHSTATUS"]),
                 get_running_status(item["RUNNINGSTATUS"]), get_voltage(item["VOLTAGE"]),
                 item["REMAINLIFEDAYS"] + "天", item["CHARGETIMES"] + "次", item["FIRMWAREVER"], item["MANUFACTUREDDATE"],
                 item["CONTROLLERID"])

metric.append(dict(index_id=4080009, content=backup_power_vals))
# fan

fan_url = request_url(module="fan")
fan_response = get_request(url=fan_url)
data = fan_response.json()["data"]

vals_append("fan_count", len(data))
fan_vals = []
table_append(fan_vals, "风扇ID", "风扇名称", "位置", "健康状态", "运行状态", "运行档位")
for item in data:
    table_append(fan_vals, item["ID"], item["NAME"], item["LOCATION"], get_health_status(item["HEALTHSTATUS"]),
                 get_running_status(item["RUNNINGSTATUS"]), get_running_level(item["RUNLEVEL"]))

metric.append(dict(index_id=4080010, content=fan_vals))
# sas_port
sas_port_url = request_url(module="sas_port")
sas_port_response = get_request(url=sas_port_url)
data = sas_port_response.json()["data"]

vals_append("sas_port_count", len(data))  # sas port count
sas_port_vals = []
table_append(sas_port_vals, "端口ID", "端口名称", "端口位置", "健康状态", "运行状态", "运行速率", "WWN", "端口类型", "端口开关")
for item in data:
    table_append(sas_port_vals, item["ID"], item["NAME"], item["LOCATION"], get_health_status(item["HEALTHSTATUS"]),
                 get_running_status(item["RUNNINGSTATUS"]), item["RUNSPEED"], item["WWN"],
                 get_iniortgt(item["INIORTGT"]), item["PORTSWITCH"])

metric.append(dict(index_id=4080011, content=sas_port_vals))
# fc_port
fc_port_url = request_url(module="fc_port")
fc_port_response = get_request(url=fc_port_url)
data = fc_port_response.json()["data"]
vals_append("fc_port_count", len(data))
fc_port_vals = []
table_append(fc_port_vals, "名称", "位置", "健康状态", "运行状态", "配置速率", "运行速率", "最大支持速率", "WWN", "光模块状态", "端口类型")
for item in data:
    table_append(fc_port_vals, item["NAME"], item["LOCATION"], get_health_status(item["HEALTHSTATUS"]),
                 get_running_status(item["RUNNINGSTATUS"]), item["CONFSPEED"] + "Mbit/s", item["RUNSPEED"] + "Mbit/s",
                 item["MAXSUPPORTSPEED"] + "Mbits/s", item["WWN"],
                 get_sfpstatus(item["SFPSTATUS"]),
                 get_iniortgt(item["INIORTGT"]))

metric.append(dict(index_id=4080012, content=fc_port_vals))
# FC启动器
fc_initiator_url = request_url(module="fc_initiator")
fc_initiator_response = get_request(url=fc_initiator_url)
data = fc_initiator_response.json()["data"]
vals_append("fc_initiator_count", len(data))  # fc 启动器数量
fc_initiator_vals = []
table_append(fc_initiator_vals, "对象ID", "健康状态", "运行状态", "是否空闲", "多路径类型", "操作系统")
for item in data:
    table_append(fc_initiator_vals, item["ID"], get_health_status(item["HEALTHSTATUS"]),
                 get_running_status(item["RUNNINGSTATUS"]), item["ISFREE"], get_multi_path_type(item["MULTIPATHTYPE"]),
                 get_operation_system(item["OPERATIONSYSTEM"])
                 )

metric.append(dict(index_id=4080013, content=fc_initiator_vals))
# lun
lun_param = {"range": "[0-100]"}
lun_url = request_url(module="lun")
lun_response = get_request(url=lun_url, params=lun_param)
if "data" in lun_response.json():
    data = lun_response.json()["data"]
else:
    data = []
vals_append("lun_count", len(data))
lun_vals = []
if data:
    table_append(lun_vals, "ID", "名称", "健康状态", "运行状态", "配置容量", "实际占用容量", "是否映射", "归属控制器", "工作控制器", "是否已添加给LUN组")
    for item in data:
        table_append(lun_vals, item["ID"], item["NAME"], get_health_status(item["HEALTHSTATUS"]),
                     get_running_status(item["RUNNINGSTATUS"]), get_item_size("CAPACITY"),
                     get_item_size("ALLOCCAPACITY"),
                     item["EXPOSEDTOINITIATOR"], item["OWNINGCONTROLLER"], item["WORKINGCONTROLLER"],
                     item["ISADD2LUNGROUP"])

metric.append(dict(index_id=4080014, content=lun_vals))
# lungroup
lungroup_url = request_url(module="lungroup")
lungroup_response = get_request(url=lungroup_url)
data = lungroup_response.json()["data"]
vals_append("lungroup_count", len(data))
lungroup_vals = []
table_append(lungroup_vals, "ID", "名称", "是否已添加给了映射视图", "应用类型", "配置容量")
for item in data:
    table_append(lungroup_vals, item["ID"], item["NAME"], item["ISADD2MAPPINGVIEW"], get_app_type(item["APPTYPE"]),
                 get_item_size("CAPCITY"))

metric.append(dict(index_id=4080015, content=lungroup_vals))
# 存储池
storagepool_url = request_url(module="storagepool")
storagepool_response = get_request(url=storagepool_url)
data = storagepool_response.json()["data"]
vals_append("storage_pool_count", len(data))
storagepool_vals = []
table_append(storagepool_vals, "ID", "名称", "描述", "健康状态", "运行状态", "总容量", "空闲容量", "已用容量", "已用容量百分比(%)", "已用容量阈值(%)")
for item in data:
    table_append(storagepool_vals, item["ID"], item["NAME"], item["DESCRIPTION"],
                 get_health_status(item["HEALTHSTATUS"]), get_running_status(item["RUNNINGSTATUS"]),
                 get_item_size("USERTOTALCAPACITY"), get_item_size("USERFREECAPACITY"),
                 get_item_size("USERCONSUMEDCAPACITY"), item["USERCONSUMEDCAPACITYPERCENTAGE"] ,
                 item["USERCONSUMEDCAPACITYTHRESHOLD"])

metric.append(dict(index_id=4080016, content=storagepool_vals))
# currentalarm
currentalarm_url = request_url(module="alarm/currentalarm")
currentalarm_response = get_request(url=currentalarm_url)
data = currentalarm_response.json()["data"]
vals_append("current_alarm_count", len(data))
current_alarm_vals = []
if data:
    table_append(current_alarm_vals, "告警发生时间", "告警名称", "告警级别", "告警描述", "告警详情", "告警恢复建议", "告警状态")
    for item in data:
        table_append(current_alarm_vals, utc2datetime(item["startTime"]), item["name"], get_alarm_level(item["level"]),
                     item["description"], item["detail"], item["suggestion"], get_alarm_level(item["alarmStatus"]))

metric.append(dict(index_id=4080017, content=current_alarm_vals))

# host
host_param = {"range": "[0-100]"}
host_url = request_url(module="host")
host_response = get_request(url=host_url, params=host_param)
if "data" in host_response.json():
    data = host_response.json()["data"]
else:
    data = []
vals_append("host_count", len(data))  # 主机个数
host_vals = []
if data:
    table_append(host_vals, "主机ID", "名称", "位置", "健康状态", "运行状态", "描述信息", "主机操作系统", "IP地址", "是否加入主机组")
    for item in data:
        if "LOCATION" in item.keys():
            table_append(host_vals, item["ID"], item["NAME"], item["LOCATION"], get_health_status(item["HEALTHSTATUS"]),
                     get_running_status(item["RUNNINGSTATUS"]), item["DESCRIPTION"],
                     get_operation_system(item["OPERATIONSYSTEM"]),
                     item["IP"], item["ISADD2HOSTGROUP"])
        else:
            table_append(host_vals, item["ID"], item["NAME"], '', get_health_status(item["HEALTHSTATUS"]),
                     get_running_status(item["RUNNINGSTATUS"]), '',
                     get_operation_system(item["OPERATIONSYSTEM"]),
                     item["IP"], item["ISADD2HOSTGROUP"])

metric.append(dict(index_id=4080018, content=host_vals))

# filesystem
filesystem_url = request_url(module="filesystem")
filesystem_response = get_request(url=filesystem_url)
if "data" in filesystem_response.json():
    data = filesystem_response.json()["data"]
else:
    data = []
vals_append("filesystem_count", len(data))  # 文件系统个数
filesystem_vals1 = []
filesystem_vals2 = []
if data:
    table_append(filesystem_vals1, "ID", "名称", "总空间容量告警阈值", "运行状态", "文件系统类型", "空间分配方式", "配置容量", "初始分配容量", "实际占用容量",
                 "块大小")
    table_append(filesystem_vals2, "ID", "归属控制器ID", "工作控制器ID", "文件系统IO优先级", "是否启用压缩", "压缩算法", "文件系统可用空间",
                 "文件系统已用容量占比(%)", "压缩节省空间", "总节省空间")
    for item in data:
        table_append(filesystem_vals1, item["ID"], item["NAME"], item["CAPACITYTHRESHOLD"],
                     get_running_status(item["RUNNINGSTATUS"]), get_sub_type(item["SUBTYPE"]),
                     get_alloc_type(item["ALLOCTYPE"]),
                     get_item_size("CAPACITY"), get_item_size("INITIALALLOCCAPACITY"), get_item_size("ALLOCCAPACITY"),
                     item["SECTORSIZE"]
                     )
        if "COMPRESSIONSAVEDCAPACITY" in item.keys():
            table_append(filesystem_vals2, item["ID"], item["OWNINGCONTROLLER"], item["WORKINGCONTROLLER"],
                     get_iopriority(item["IOPRIORITY"]),
                     item["ENABLECOMPRESSION"], get_compression(item["COMPRESSION"]), get_item_size("AVAILABLECAPCITY"),
                     item["AVAILABLEANDALLOCCAPACITYRATIO"],
                     get_item_size("COMPRESSIONSAVEDCAPACITY"), get_item_size("TOTALSAVEDCAPACITY"))
        else:
            table_append(filesystem_vals2, item["ID"], item["OWNINGCONTROLLER"], item["WORKINGCONTROLLER"],
                     get_iopriority(item["IOPRIORITY"]),
                     item["ENABLECOMPRESSION"], get_compression(item["COMPRESSION"]), get_item_size("AVAILABLECAPCITY"),
                     item["AVAILABLEANDALLOCCAPACITYRATIO"],
                     '', '')
metric.append(dict(index_id=4080019, content=filesystem_vals1))
metric.append(dict(index_id=4080020, content=filesystem_vals2))
# loginout
# response = requests.request("DELETE", url, headers=headers, cookies=cookie, verify=False)
response = get_request(method="DELETE", url=url)

metric.append(dict(index_id=4080001, value=vals))
print('{"cib":' + json.dumps(metric) + '}')

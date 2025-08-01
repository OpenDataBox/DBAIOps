
import json
import sys

sys.path.append('/usr/software/knowl')
import DBUtil
from Unity_storage_comm import Unity

import warnings
warnings.filterwarnings("ignore")

vals = []
metric = []


def vals_append(key, value):
    vals.append(dict(name=key, value=value))


# 获取storage system基本信息
def unity_storageSystemBasicinfo(unityInst):
    vals_append("id", unityInst.id)  # 系统id
    vals_append("sys_name", unityInst.name)  # 系统名称
    vals_append("model", unityInst.model)  # 模块名称
    vals_append("softwareVersion", unityInst.softwareVersion)  # 软件版本
    payload = dict()
    # 健康状态，硬件平台
    payload["fields"] = "health,platform"

    response = unityInst.unity_request("/instances/system/0", payload=payload).json()
    vals_append("systemHealth", Unity.health_status.get(response['content']['health']['value']))
    vals_append("HardwarePlatform", response['content']['platform'])
    response1 = unityInst.unity_request("/instances/systemInformation/0", payload={"fields": "locationName"}).json()
    if response1.get('content').get('locationName'):
        vals_append("locationName", response1.get('content').get('locationName'))


def unity_storagePollInfo(unityInst):
    payload = dict()
    # 存储池总大小，剩余大小，已使用大小
    payload["fields"] = "sizeTotal, sizeFree, sizeUsed"
    response = unityInst.unity_request("/types/pool/instances", payload=payload).json()
    if 'entries' in response:
        # 统计pool的数量
        vals_append("pool_count", len(response['entries']))
        pool_list = list()
        pool_list.append(dict(c1='存储池id', c2='总大小(GB)', c3='已使用大小(GB)', c4='剩余大小(GB)',
                         c5='使用率(%)', c6=None, c7=None, c8=None, c9=None, c10=None))
        # 统计所有存储池总大小，剩余大小，已使用大小
        for item in response['entries']:
            # 换算成GB
            sum_all = round(int(item['content']['sizeTotal']) / 1024 / 1024 / 1024, 2)
            sum_free = round(int(item['content']['sizeFree']) / 1024 / 1024 / 1024, 2)
            sum_used = round(int(item['content']['sizeUsed']) / 1024 / 1024 / 1024, 2)

            if sum_all > 0:
                used_pct = round(sum_used / sum_all * 100, 2)
            else:
                used_pct = 0
            pool_list.append(dict(c1=item['content']['id'], c2=sum_all, c3=sum_used, c4=sum_free,
                                  c5=used_pct, c6=None, c7=None, c8=None, c9=None, c10=None))
        metric.append(dict(index_id=4100002, content=pool_list))


def unity_DiskInfo(unityInst):
    payload = dict()
    # 磁盘健康状态，是否需要更换，裸盘大小，当前速度，最高速度, 是否有用户数据
    payload["fields"] = "health, needsReplacement, rawSize, currentSpeed, maxSpeed, isInUse"
    response = unityInst.unity_request("/types/disk/instances", payload=payload).json()
    if 'entries' in response:
        disk_list = list()
        disk_list.append(dict(c1='磁盘id', c2='健康状态', c3='是否需要更换', c4='当前速度(bytes/sec)',
                              c5='最高速度(bytes/sec)', c6='是否有用户数据', c7=None, c8=None, c9=None, c10=None))
        # 磁盘信息
        for item in response['entries']:
            disk_list.append(dict(c1=item['content']['id'], c2=Unity.health_status.get(item['content']['health']['value']),
                                  c3=item['content']['needsReplacement'], c4=item['content']['currentSpeed'],
                                  c5=item['content']['maxSpeed'], c6=item['content']['isInUse'], c7=None, c8=None, c9=None, c10=None))
        if len(disk_list) > 1:
            metric.append(dict(index_id=4100003, content=disk_list))


def unity_LunInfo(unityInst):
    payload = dict()
    # lun名称，健康状态，类型，总分配大小，所属池
    payload["fields"] = "name, health, type, sizeAllocatedTotal, pool"
    response = unityInst.unity_request("/types/lun/instances", payload=payload).json()
    if 'entries' in response:
        lun_list = list()
        lun_list.append(dict(c1='lun名称', c2='健康状态', c3='类型', c4='总分配大小(GB)', c5='所属池',
                             c6=None, c7=None, c8=None, c9=None, c10=None))
        # lun信息
        for item in response['entries']:
            sizeAllocatedTotal = round(int(item['content']['sizeAllocatedTotal']) / 1024 / 1024 / 1024, 2)
            lun_list.append(dict(c1=item['content']['name'], c2=Unity.health_status.get(item['content']['health'].get('value')),
                                 c3=item['content'].get('type'), c4=sizeAllocatedTotal, c5=item['content']['pool'].get('name'),
                                 c6=None, c7=None, c8=None, c9=None, c10=None))
        if len(lun_list) > 1:
            metric.append(dict(index_id=4100004, content=lun_list))


def unity_enclosure(unityInst):
    payload = dict()
    payload["fields"] = "name, health, needsReplacement, enclosureType, currentTemperature, maxTemperature, " \
                        "currentPower, maxPower"
    response = unityInst.unity_request("/types/dpe/instances", payload=payload).json()
    if 'entries' in response:
        # 统计所有机框数量
        vals_append("enclosure_count", len(response['entries']))
        enclosure_list = list()
        enclosure_list.append(dict(c1='名称', c2='健康状态', c3='是否需要更换', c4='当前温度(degrees C)', c5='最高温度(degrees C)',
                                   c6='当前电功率', c7='最大电功率', c8='机框类型', c9=None, c10=None))
        for item in response['entries']:
            # DPE信息
            enclosure_list.append(
                dict(c1=item['content']['name'], c2=Unity.health_status.get(item['content']['health']['value']),
                     c3=item['content']['needsReplacement'], c4=item['content'].get('currentTemperature'),
                     c5=item['content'].get('maxTemperature'), c6=item['content'].get('currentPower'),
                     c7=item['content'].get('maxPower'), c8=item['content'].get('enclosureType'), c9=None, c10=None))
        if len(enclosure_list) > 1:
            metric.append(dict(index_id=4100005, content=enclosure_list))
        # 非Virtual_DPE，才支持获取硬件信息
        if response['entries'][0]['content']['enclosureType'] != 100:
            unity_power(unityInst)
            unity_fan(unityInst)


def unity_power(unityInst):
    payload = dict()
    payload["fields"] = "name, health, needsReplacement, Manufacturer, model"
    response = unityInst.unity_request("/types/powerSupply/instances", payload=payload).json()
    if 'entries' in response:
        # 统计所有电源数量
        vals_append("power_count", len(response['entries']))
        power_list = list()
        power_list.append(dict(c1='名称', c2='健康状态', c3='是否需要更换', c4='制造商', c5='型号',
                               c6=None, c7=None, c8=None, c9=None, c10=None))
        for item in response['entries']:
            # 电源信息
            power_list.append(
                dict(c1=item['content']['name'], c2=Unity.health_status.get(item['content']['health']['value']),
                     c3=item['content']['needsReplacement'], c4=item['content']['Manufacturer'],
                     c5=item['content']['model'], c6=None, c7=None, c8=None, c9=None, c10=None))
        if len(power_list) > 1:
            metric.append(dict(index_id=4100006, content=power_list))


def unity_fan(unityInst):
    payload = dict()
    payload["fields"] = "name, health, needsReplacement, Manufacturer, model"
    response = unityInst.unity_request("/types/fan/instances", payload=payload).json()
    if 'entries' in response:
        # 统计所有风扇数量
        vals_append("fan_count", len(response['entries']))
        power_list = list()
        power_list.append(dict(c1='名称', c2='健康状态', c3='是否需要更换', c4='制造商', c5='型号',
                               c6=None, c7=None, c8=None, c9=None, c10=None))
        for item in response['entries']:
            # 风扇信息
            power_list.append(
                dict(c1=item['content']['name'], c2=Unity.health_status.get(item['content']['health']['value']),
                     c3=item['content']['needsReplacement'], c4=item['content']['Manufacturer'],
                     c5=item['content']['model'], c6=None, c7=None, c8=None, c9=None, c10=None))
        if len(power_list) > 1:
            metric.append(dict(index_id=4100007, content=power_list))


def get_hp3par_info(hp_clt):
    """获取HPE 3PAR存储信息
    :param host: HPE 3PAR主机IP
    :param
    """
    metric = []
    response, out = hp_clt.getStorageSystemInfo()
    if response.status == 200:
        metric.append(dict(name='Name', value=out['name']))
        metric.append(dict(name='Patches', value=out['patches']))
        metric.append(dict(name='Model', value=out['model']))
        metric.append(dict(name='SerialNumber', value=out['serialNumber']))
        metric.append(dict(name='timeZone', value=out['timeZone']))
        # license info
        var = []
        var.append(dict(name='LicenseDate', value=out['licenseInfo']['issueTime8601']))
        var.append(dict(name='LicensediskCount', value=out['licenseInfo']['diskCount']))
        var.append(dict(name='LicenseWWNBASE', value=out['licenseInfo']['WWNBASE']))
        li_str = ''
        for row in out['licenseInfo']['licenses']:
            li_str = li_str + row['name'] + ','
        metric.append(dict(name='LicenseFeatures', value=li_str[:-1]))
        for key,item in out['licenseInfo']['licenseState'].items():
            var.append(dict(name=key, value=item))
        # 容量总体信息
        var.append(dict(name='chunkletSizeMiB', value=out['chunkletSizeMiB']))
        var.append(dict(name='totalCapacityMiB', value=out['totalCapacityMiB']))
        var.append(dict(name='allocatedCapacityMiB', value=out['allocatedCapacityMiB']))
        var.append(dict(name='freeCapacityMiB', value=out['freeCapacityMiB']))
        var.append(dict(name='failedCapacityMiB', value=out['failedCapacityMiB']))
        metric.append(dict(index_id='4100001', value=var))
        # parameters
        var2 = []
        for key,item in out['parameters'].items():
            var2.append(dict(name=key, value=item))
        metric.append(dict(index_id='4100008', value=var2))
    return metric


def execute(p=None):
    if p:
        sub_type, client = DBUtil.get_common_storage_client(p)
    else:
        sub_type, client = DBUtil.get_common_storage_client()
    if sub_type == '4':
        # 获取storage system基本信息
        unity_storageSystemBasicinfo(client)
        # 获取storage pool信息
        unity_storagePollInfo(client)
        # 获取机框数量
        unity_enclosure(client)
        # 获取磁盘信息
        unity_DiskInfo(client)
        # 获取lun信息
        unity_LunInfo(client)
        metric.append(dict(index_id=4100001, value=vals))
    elif sub_type == '5':
        get_hp3par_info(client)


if __name__ == '__main__':
    #t = '{"target_ip": "60.60.60.177", "target_port": "443", "target_usr": "admin", "target_pwd": "Password123##", "sub_type": "4"}'
    execute()
    print('{"cib":' + json.dumps(metric) + '}')




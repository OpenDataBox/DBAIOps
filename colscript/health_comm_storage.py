
import json
import sys

sys.path.append('/usr/software/knowl')
import DBUtil
import warnings
warnings.filterwarnings("ignore")


def execute(p=None):
    if not p:
        dbInfo = eval(sys.argv[1])
    else:
        dbInfo = eval(p)

    sub_type, client = DBUtil.get_common_storage_client(dbInfo)
    if sub_type == '4':
        unity = client
        # 获取storage system基本信息
        unity.unity_storageSystemBasicinfo(vals)
        # 获取storage pool信息
        unity.unity_storagePollInfo(vals)
        # 获取lun信息
        unity.unity_LunInfo(vals)
        # 获取磁盘信息
        unity.unity_DiskInfo(vals)
        # 获取DPE信息
        unity.unity_DpeInfo(vals)
        # 获取host启动器信息
        unity.unity_hostInitiator(vals)
        # 获取系统容量信息
        unity.unity_systemCapacity(vals)
        # 获取文件系统大小
        unity.unity_filesystem(vals)
        # 获取性能指标
        unity.performance_metric(vals)
    elif sub_type == '5':
        hp3par = client
        pass


if __name__ == '__main__':
    vals = []
    #t = '{"target_ip": "60.60.60.177", "target_port": "443", "target_usr": "admin", "target_pwd": "Password123##", "sub_type": "4"}'
    execute()
    msg = '{"results":' + json.dumps(vals) + '}'
    print(msg)




#  @文件    :cib_os.py
#  @说明    :
#  @创建时间    :2021/2/7 下午1:50
#  @修改时间    :2021/2/7 下午1:50
#  @作者    :baoba
#  @版本    :1.9.4
import sys

sys.path.append('/usr/software/knowl')

import DBUtil
import json
import warnings

warnings.filterwarnings("ignore")

vals = []
metric = []


def vals_append(key, value):
    vals.append(dict(name=key, value=str(value)))


def table_append(tab_list, c1=None, c2=None, c3=None, c4=None, c5=None, c6=None, c7=None, c8=None, c9=None, c10=None):
    tab_list.append(dict(c1=c1, c2=c2, c3=c3, c4=c4, c5=c5, c6=c6, c7=c7, c8=c8, c9=c9, c10=c10))


def get_sysctl_config():
    cmd = "sysctl -a"
    params = []
    result = helper.exec_cmd(cmd)
    if not isinstance(result, tuple):
        temp_list = result.split("\n")
        for index, item in enumerate(temp_list[0:]):
            key, value = item.split("=")
            params.append(dict(name=key.strip(), value=value.strip()))
        metric.append(dict(index_id=3010002, value=params))
    else:
        print(result)


def get_blk_device():
    cmd = "lsblk -P"
    result = helper.exec_cmd(cmd)
    if not isinstance(result, tuple):
        temp_list = result.split("\n")
        disks = []
        for index, item in enumerate(temp_list[0:]):
            t = item.find('="')
            b = 0
            arr = [None]*7
            while t > 0:
                s = item[b:t].strip()
                t2 = item.find('"', t+2)
                if t2 > 0:
                    v = item[t+2:t2].strip()
                    b = t2+1
                    t = item.find('="',b)
                    i = ['NAME','MAJ:MIN','RM','TYPE','SIZE','RO','MOUNTPOINT'].index(s)
                    if i >= 0:
                        arr[i] = v 
                else:
                    break
            if arr[0]:
                table_append(disks, arr[0], arr[1], arr[2], arr[3], arr[4])
        metric.append(dict(index_id=3010003, content=disks))
    else:
        print(result)


def get_os_base():
    cmd = "uname -n;uname -r;uname -v;uname -s;getconf PAGESIZE"
    result = helper.exec_cmd(cmd)
    if not isinstance(result,tuple):
        node_name, kernel_release, kernel_version, kernel_name, *page_size = result.splitlines()
        if not page_size:
            page_size = '4096'
        else:
            page_size = page_size[0]
        vals_append("node_name", node_name)
        vals_append("kernel_release", kernel_release)
        vals_append("kernel_version", kernel_version)
        vals_append("kernel_name", kernel_name)
        vals_append("page_size", page_size)
    cmd = "cat /etc/os-release |grep VERSION_ID |awk -F'=' '{print $NF}'"
    result = helper.exec_cmd(cmd)
    if isinstance(result,tuple):
        cmd = "cat /etc/redhat-release | awk '{print $(NF-1)}'"
        result = helper.exec_cmd(cmd)
        if isinstance(result,tuple):
            vals_append("os_version", 'unkown')
        else:
            vals_append("os_version", result.strip())
    else:
        vals_append("os_version", result.strip().replace('"', ''))
    cmd_mem = "cat /proc/meminfo |grep MemTotal|awk '{print $2}'"
    result = helper.exec_cmd(cmd_mem)
    if not isinstance(result,tuple):
        vres_mem = result.strip()
        vals_append("mem_total", vres_mem)
    # cpu
    cmd_cpu = """ cat /proc/cpuinfo| grep "physical id"| sort| uniq| wc -l;cat /proc/cpuinfo| grep "processor"| wc -l;cat /proc/cpuinfo | grep name | cut -f2 -d:| awk 'NR<=1 {print $0}' """
    result2 = helper.exec_cmd(cmd_cpu)
    if not isinstance(result,tuple):
        cpus,cpu_cores,cup_model = result2.splitlines()
        vals_append("cpu_nums", cpus)
        vals_append("cpu_cores", cpu_cores)
        vals_append("cpu_model", cup_model)
        metric.append(dict(index_id=3010001, value=vals))


if __name__ == '__main__':
    ostype, device_id, helper = DBUtil.get_ssh_session_cib()
    dbInfo = eval(sys.argv[1])
    proto = dbInfo.get('protocol')
    if ostype in ['RedHat', 'SUSE', 'CentOS'] and proto in ['1','2']:
        get_os_base()
        get_sysctl_config()
        get_blk_device()
    print('{"cib":' + json.dumps(metric) + '}')

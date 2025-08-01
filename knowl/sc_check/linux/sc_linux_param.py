import sys

sys.path.append('/usr/software/knowl')
import DBUtil
import json


def register(file_name):
    res = []
    print('{"params_reg":[]}')


def getlinuxparam():
    score = 0
    fres = []

    vs = 0
    vt = []
    vtr = []
    vtn = []
    cmd_mem = "cat /proc/meminfo |grep MemTotal|awk '{print $2}'"
    vres_mem = helper.openCmd(cmd_mem).strip()

    ci = ['kernel.shmmni', 'kernel.shmall', 'kernel.shmmax', 'kernel.sem', 'fs.file-max', 'fs.aio-max-nr',
          'net.core.rmem_default', 'net.core.rmem_max', 'net.core.wmem_default', 'net.core.wmem_max',
          'net.ipv4.ip_local_port_range', 'net.ipv4.ipfrag_high_thresh', 'net.ipv4.ipfrag_low_thresh',
          'vm.min_free_kbytes', 'vm.vfs_cache_pressure', 'vm.swappiness', 'vm.nr_hugepages']
    for x in ci:
        cmd = "cat /proc/sys/" + x.replace(".", "/")
        # print(cmd)
        vres = helper.openCmd(cmd).strip()
        vtr.append(dict(name=x, value=vres))

    for x in vtr:
        if x.get("name") == "kernel.shmmni":
            if int(x.get("value")) != 4096:
                vs += 1
                vt.append(x.get("name") + "设置不合规，建议值：4096")
            else:
                vtn.append(x.get("name") + "设置合规，值为：" + str(int(x.get("value"))))

        if x.get("name") == "kernel.shmall":
            rval = int(int(vres_mem) * 0.7 / 4)
            if int(x.get("value")) - rval < 1:
                vs += 1
                vt.append(x.get("name") + "设置不合规，建议值：" + str(rval))
            else:
                vtn.append(x.get("name") + "设置合规，值为：" + str(int(x.get("value"))))

        if x.get("name") == "kernel.shmmax":
            rval = int(int(vres_mem) * 0.7 * 1024)
            if int(x.get("value")) - rval < 1:
                vs += 1
                vt.append(x.get("name") + "设置不合规，建议值：" + str(rval))
            else:
                vtn.append(x.get("name") + "设置合规，值为：" + str(int(x.get("value"))))

        if x.get("name") == "kernel.sem":
            if int(x.get("value").split("\t")[0]) != 250 or int(x.get("value").split("\t")[1]) != 32000 or int(
                    x.get("value").split("\t")[2]) != 100 or int(x.get("value").split("\t")[3]) != 128:
                vs += 1
                vt.append(x.get("name") + "设置不合规，建议值：250 32000 100 128")
            else:
                vtn.append(x.get("name") + "设置合规，值为：" + str(x.get("value")))

        if x.get("name") == "fs.file-max":
            if int(x.get("value")) < 6815744:
                vs += 1
                vt.append(x.get("name") + "设置不合规，建议值：6815744")
            else:
                vtn.append(x.get("name") + "设置合规，值为：" + str(x.get("value")))

        if x.get("name") == "fs.aio-max-nr":
            if int(x.get("value")) < 1048576:
                vs += 1
                vt.append(x.get("name") + "设置不合规，建议值：1048576")
            else:
                vtn.append(x.get("name") + "设置合规，值为：" + str(x.get("value")))

        if x.get("name") == "net.core.rmem_default":
            if int(x.get("value")) < 262144:
                vs += 1
                vt.append(x.get("name") + "设置不合规，建议值：262144")
            else:
                vtn.append(x.get("name") + "设置合规，值为：" + str(x.get("value")))

        if x.get("name") == "net.core.rmem_max":
            if int(x.get("value")) < 4194304:
                vs += 1
                vt.append(x.get("name") + "设置不合规，建议值：4194304")
            else:
                vtn.append(x.get("name") + "设置合规，值为：" + str(x.get("value")))

        if x.get("name") == "net.core.wmem_default":
            if int(x.get("value")) < 262144:
                vs += 1
                vt.append(x.get("name") + "设置不合规，建议值：262144")
            else:
                vtn.append(x.get("name") + "设置合规，值为：" + str(x.get("value")))

        if x.get("name") == "net.core.wmem_max":
            if int(x.get("value")) < 1048576:
                vs += 1
                vt.append(x.get("name") + "设置不合规，建议值：1048576")
            else:
                vtn.append(x.get("name") + "设置合规，值为：" + str(x.get("value")))

        if x.get("name") == "net.ipv4.ip_local_port_range":
            if int(x.get("value").split("\t")[0]) != 9000 or int(x.get("value").split("\t")[1]) != 65500:
                vs += 1
                vt.append(x.get("name") + "设置不合规，建议值：9000 65500")
            else:
                vtn.append(x.get("name") + "设置合规，值为：" + str(x.get("value")))

        if x.get("name") == "net.ipv4.ipfrag_high_thresh":
            if int(x.get("value")) < 4194304:
                vs += 1
                vt.append(x.get("name") + "设置不合规，建议值：4194304")
            else:
                vtn.append(x.get("name") + "设置合规，值为：" + str(x.get("value")))

        if x.get("name") == "net.ipv4.ipfrag_low_thresh":
            if int(x.get("value")) < 3145728:
                vs += 1
                vt.append(x.get("name") + "设置不合规，建议值：3145728")
            else:
                vtn.append(x.get("name") + "设置合规，值为：" + str(x.get("value")))

        if x.get("name") == "vm.min_free_kbytes":
            if int(x.get("value")) < 512000:
                vs += 1
                vt.append(x.get("name") + "设置不合规，建议值：512000")
            else:
                vtn.append(x.get("name") + "设置合规，值为：" + str(x.get("value")))

        if x.get("name") == "vm.vfs_cache_pressure":
            if int(x.get("value")) < 200:
                vs += 1
                vt.append(x.get("name") + "设置不合规，建议值：200")
            else:
                vtn.append(x.get("name") + "设置合规，值为：" + str(x.get("value")))

        if x.get("name") == "vm.swappiness":
            if int(x.get("value")) < 20:
                vs += 1
                vt.append(x.get("name") + "设置不合规，建议值：20")
            else:
                vtn.append(x.get("name") + "设置合规，值为：" + str(x.get("value")))

        if x.get("name") == "vm.nr_hugepages":
            if int(x.get("value")) == 0:
                vs += 1
                vt.append(x.get("name") + "设置不合规，建议值：DB_SGA+ASM_SGA+1GB/Hugepagesize")
            else:
                vtn.append(x.get("name") + "设置合规，值为：" + str(x.get("value")))

    if vs > 0:
        score += 1
        fres.append(dict(rkey="系统参数配置检查", rval="\n".join(str(i) for i in vt), rtype=1, rnote="系统参数配置不合规"))
    else:
        fres.append(dict(rkey="系统参数配置检查", rval="\n".join(str(i) for i in vtn), rtype=0, rnote="系统参数配置合规"))
    return score, fres


if __name__ == '__main__':
    """'{"deviceId":"110100011","in_ip":"60.60.60.116","in_os":"RedHat","in_port":"22","in_pwd":"A/uOt/N48/t8wkiYVPA9qG/U6oTl6gRIlq9x4CNbuA5tgaELSobkkEdS1EaM7Fxqj6gmwPHr0kv6HP0PytI2PCXUDfDxH0dnz88ZL94N1AuQdhLsx6e1O/McX8osfqsEhwtJCEAd/Y+XmM06vnBBgPB0PTzvJbpmTzbTG1WR61E=","in_uid":"110600001","in_username":"root","in_usr":"root"}'"""
    """'{"deviceId":"110100012","in_ip":"60.60.60.205","in_os":"RedHat","in_port":"22","in_pwd":"NQTZWN7c6qx/Mjc1LiIRl2xlPj5+5w5jsAdbpQN1E21dnqazfAImji5PIWczjMHyEuy6h8bl9O18InFiHB6D0oQiZimRSZHrgmJoEsh34DWRIpy10+82DexjWO69nJWRzDlwUJ+bGi/H5av9RESVe4EEToJsUljAHZJPcoZ5Ep4=","in_uid":"110600002","in_username":"root","in_usr":"root"}'"""
    check_item = ['系统版本检查', '系统时区检查', '系统可用磁盘空间检查', '系统内存检查', '系统字符集检查', '系统网卡个数检查', '系统文件系统检查', '系统RPM包检查', '系统服务检查',
                  '系统Selinux检查', '系统透明大页检查', '系统安全配置检查', '系统参数配置检查']
    ostype, deviceId, helper = DBUtil.get_ssh_help()
    # dbInfo = eval(sys.argv[1])

    try:
        s13, f13 = getlinuxparam()
        if f13:
            print('msg=' + json.dumps(f13[0]))


    except Exception as e:
        errorInfo = str(e)
        print("异常：" + errorInfo)

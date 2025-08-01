#!/bin/bash
#
#
#
#set -e
bin=`dirname "${BASH_SOURCE-$0}"`
bin=`cd "$bin"; pwd`
ROOT=`cd $bin;cd ..;pwd`
DBAIOps_oper_dir="/usr/software"
localnode=`hostname`
log=$DBAIOps_oper_dir/bin/logs/openoffice_install.log

# 获取主脚本中的语言设置
if [ -z "$LANGUAGE" ]; then
    LANGUAGE="en"  # 默认英文
fi


c1() {
    RED_COLOR='\E[1;31m'
    GREEN_COLOR='\E[1;32m'
    YELLOW_COLOR='\E[1;33m'
    BLUE_COLOR='\E[1;34m'
    PINK_COLOR='\E[1;35m'
    WHITE_BLUE='\E[47;34m'
    DOWN_BLUE='\E[4;36m'
    FLASH_RED='\E[5;31m'
    RES='\E[0m'

    if [ $# -ne 2 ]; then
        echo "Usage $0 content {red|yellow|blue|green|pink|wb|db|fr}"
        exit
    fi

    case "$2" in
    red | RED)
        echo -e "${RED_COLOR}$1${RES}"
        ;;
    yellow | YELLOW)
        echo -e "${YELLOW_COLOR}$1${RES}"
        ;;
    green | GREEN)
        echo -e "${GREEN_COLOR}$1${RES}"
        ;;
    blue | BLUE)
        echo -e "${BLUE_COLOR}$1${RES}"
        ;;
    pink | PINK)
        echo -e "${PINK_COLOR}$1${RES}"
        ;;
    wb | WB)
        echo -e "${WHITE_BLUE}$1${RES}"
        ;;
    db | DB)
        echo -e "${DOWN_BLUE}$1${RES}"
        ;;
    fr | FR)
        echo -e "${FLASH_RED}$1${RES}"
        ;;
    *)
        echo -e "Please enter the specified color code：{red|yellow|blue|green|pink|wb|db|fr}"
        ;;
    esac
}


print_usage(){
    echo "Usage: DBAIOps Openoffice installation"
    echo "  -install                      install DBAIOps Openoffice Package"
}


install_openoffice_rpm() {
    # 多语言提示信息
    if [ "$LANGUAGE" == "cn" ]; then
        local msg_install_openoffice="正在安装 Web openoffice..."
        local msg_local_install="本地节点安装 openoffice..."
        local msg_remote_install="远程节点 $ds_web 安装 openoffice..."
        local msg_install_success="openoffice 安装成功！"
        local msg_install_failed="openoffice 安装失败！"
    else
        local msg_install_openoffice="Installing Web openoffice..."
        local msg_local_install="Installing openoffice on local node..."
        local msg_remote_install="Installing openoffice on remote node $ds_web..."
        local msg_install_success="openoffice installation succeeded!"
        local msg_install_failed="openoffice installation failed!"
    fi

    echo "############################################################"
    if [ "$LANGUAGE" == "cn" ]; then
        echo "                  安装 Web openoffice                    "
    else
        echo "                  Install Web openoffice                 "
    fi
    echo "############################################################"

    c1 "$msg_install_openoffice" blue

    if [ "$localnode" == "$ds_web" ]; then
        # 本地节点安装
        c1 "$msg_local_install" blue
        if [ -f /etc/profile.d/java.sh ]; then
            source /etc/profile.d/java.sh
        fi
        cd $DBAIOps_oper_dir/python3
        tar --no-same-owner -xvzf Apache_OpenOffice_4.1.7_Linux_x86-64_install-rpm_zh-CN.tar.gz > /dev/null 2>&1
        cd $DBAIOps_oper_dir/python3/zh-CN/RPMS
        if [ "$os_type" == "suse" ]; then
            rpm -ivh *.rpm > $log
            cd $DBAIOps_oper_dir/python3/zh-CN/RPMS/desktop-integration
            rpm -ivh openoffice4.1.7-suse-menus-4.1.7-9800.noarch.rpm >> $log
        fi
        if [ -n "$flag_yum" ]; then
            yum localinstall -y *.rpm > $log
            cd $DBAIOps_oper_dir/python3/zh-CN/RPMS/desktop-integration
            yum localinstall -y openoffice4.1.7-redhat-menus-4.1.7-9800.noarch.rpm >> $log
        fi

        /opt/openoffice4/program/soffice -headless -accept="socket,host=127.0.0.1,port=8100;urp;" -nofirststartwizard &
        sleep 2
        proc=$(netstat -lnp | grep 8100 | awk '{print $NF}' | awk -F '/' '{print $1}')
        if [ "$proc" ]; then
            c1 "$msg_install_success" green
            kill -9 $proc > /dev/null 2>&1
        else
            c1 "$msg_install_failed" red
            exit 1
        fi
    else
        # 远程节点安装
        c1 "$msg_remote_install" blue
        ssh $ds_web "
            cd $DBAIOps_oper_dir/python3
            tar --no-same-owner -xvzf Apache_OpenOffice_4.1.7_Linux_x86-64_install-rpm_zh-CN.tar.gz > /dev/null 2>&1
            cd $DBAIOps_oper_dir/python3/zh-CN/RPMS
            if [ \"$os_type\" == \"suse\" ]; then
                zypper install -y *.rpm > $log
                cd $DBAIOps_oper_dir/python3/zh-CN/RPMS/desktop-integration
                zypper install -y openoffice4.1.7-suse-menus-4.1.7-9800.noarch.rpm >> $log
            fi
            if [ -n \"$flag_yum\" ]; then
                yum install -y *.rpm > $log
                cd $DBAIOps_oper_dir/python3/zh-CN/RPMS/desktop-integration
                yum install -y openoffice4.1.7-redhat-menus-4.1.7-9800.noarch.rpm >> $log
            fi
        "
        echo '/opt/openoffice4/program/soffice -headless -accept="socket,host=127.0.0.1,port=8100;urp;" -nofirststartwizard &' > /tmp/openoffice.sh
        chmod +x /tmp/openoffice.sh
        scp /tmp/openoffice.sh $ds_web:/tmp
        ssh $ds_web "source /etc/profile.d/java.sh; sh /tmp/openoffice.sh >/dev/null 2>&1 &"
        proc=$(ssh $ds_web "netstat -lnp | grep 8100" | awk '{print $NF}' | awk -F '/' '{print $1}')
        if [ "$proc" ]; then
            c1 "$msg_install_success" green
            ssh $ds_web "kill -9 $proc > /dev/null 2>&1"
        else
            c1 "$msg_install_failed" red
        fi
    fi
}

install_openoffice_apt() {
    # 多语言提示信息
    if [ "$LANGUAGE" == "cn" ]; then
        local msg_install_openoffice="正在安装 Web openoffice..."
        local msg_local_install="本地节点安装 openoffice..."
        local msg_remote_install="远程节点 $ds_web 安装 openoffice..."
        local msg_install_success="openoffice 安装成功！"
        local msg_install_failed="openoffice 安装失败！"
    else
        local msg_install_openoffice="Installing Web openoffice..."
        local msg_local_install="Installing openoffice on local node..."
        local msg_remote_install="Installing openoffice on remote node $ds_web..."
        local msg_install_success="openoffice installation succeeded!"
        local msg_install_failed="openoffice installation failed!"
    fi

    echo "############################################################"
    if [ "$LANGUAGE" == "cn" ]; then
        echo "                  安装 Web openoffice                    "
    else
        echo "                  Install Web openoffice                 "
    fi
    echo "############################################################"

    c1 "$msg_install_openoffice" blue

    if [ "$localnode" == "$ds_web" ]; then
        # 本地节点安装
        c1 "$msg_local_install" blue
        cd $DBAIOps_oper_dir/python3
        source /etc/profile.d/java.sh
        tar --no-same-owner -xvzf Apache_OpenOffice_4.1.7_Linux_x86-64_install-deb_zh-CN.tar.gz > /dev/null 2>&1
        cd $DBAIOps_oper_dir/python3/zh-CN/DEBS
        apt -y install ./openoffice*.deb > /dev/null 2>&1
        cd $DBAIOps_oper_dir/python3/zh-CN/DEBS/desktop-integration
        apt -y install ./openoffice4.1-debian-menus_4.1.7-9800_all.deb > /dev/null 2>&1
        /opt/openoffice4/program/soffice -headless -accept="socket,host=127.0.0.1,port=8100;urp;" -nofirststartwizard &
        sleep 2
        proc=$(netstat -lnp | grep 8100 | awk '{print $NF}' | awk -F '/' '{print $1}')
        if [ "$proc" ]; then
            c1 "$msg_install_success" green
            kill -9 $proc > /dev/null 2>&1
        else
            c1 "$msg_install_failed" red
            exit 1
        fi
    else
        # 远程节点安装
        c1 "$msg_remote_install" blue
        ssh $ds_web "
            cd $DBAIOps_oper_dir/python3
            tar --no-same-owner -xvzf Apache_OpenOffice_4.1.7_Linux_x86-64_install-deb_zh-CN.tar.gz > /dev/null 2>&1
            cd $DBAIOps_oper_dir/python3/zh-CN/DEBS
            apt -y install ./openoffice*.deb > /dev/null 2>&1
            cd $DBAIOps_oper_dir/python3/zh-CN/DEBS/desktop-integration
            apt -y install ./openoffice4.1-debian-menus_4.1.7-9800_all.deb > /dev/null 2>&1
        "
        echo '/opt/openoffice4/program/soffice -headless -accept="socket,host=127.0.0.1,port=8100;urp;" -nofirststartwizard &' > /tmp/openoffice.sh
        chmod +x /tmp/openoffice.sh
        scp /tmp/openoffice.sh $ds_web:/tmp
        ssh $ds_web "source /etc/profile.d/java.sh; sh /tmp/openoffice.sh >/dev/null 2>&1 &"
        proc=$(ssh $ds_web "netstat -lnp | grep 8100" | awk '{print $NF}' | awk -F '/' '{print $1}')
        if [ "$proc" ]; then
            c1 "$msg_install_success" green
            ssh $ds_web "kill -9 $proc > /dev/null 2>&1"
        else
            c1 "$msg_install_failed" red
        fi
    fi
}

install_openoffice_kylinV10() {
    # 多语言提示信息
    if [ "$LANGUAGE" == "cn" ]; then
        local msg_install_openoffice="正在安装 Web openoffice (KylinV10)..."
        local msg_local_install="本地节点安装 openoffice (KylinV10)..."
        local msg_remote_install="远程节点 $ds_web 安装 openoffice (KylinV10)..."
        local msg_install_success="openoffice (KylinV10) 安装成功！"
    else
        local msg_install_openoffice="Installing Web openoffice (KylinV10)..."
        local msg_local_install="Installing openoffice (KylinV10) on local node..."
        local msg_remote_install="Installing openoffice (KylinV10) on remote node $ds_web..."
        local msg_install_success="openoffice (KylinV10) installation succeeded!"
    fi

    echo "############################################################"
    if [ "$LANGUAGE" == "cn" ]; then
        echo "                  安装 Web openoffice (KylinV10)          "
    else
        echo "                  Install Web openoffice (KylinV10)       "
    fi
    echo "############################################################"

    c1 "$msg_install_openoffice" blue

    if [ "$localnode" == "$ds_web" ]; then
        # 本地节点安装
        c1 "$msg_local_install" blue
        cd $DBAIOps_oper_dir/python3
        tar zxf libreoffice7.1.8-aarch.tar.gz -C /opt/
        if [ -d /opt/openoffice4 ]; then
            rm -rf /opt/openoffice4
        fi
        mv /opt/instdir/ /opt/openoffice4/
        c1 "$msg_install_success" green
    else
        # 远程节点安装
        c1 "$msg_remote_install" blue
        ssh $ds_web "
            cd $DBAIOps_oper_dir/python3
            tar zxf libreoffice7.1.8-aarch.tar.gz -C /opt/
            mv /opt/instdir/ /opt/openoffice4/
        "
        c1 "$msg_install_success" green
    fi
}


# 根据语言设置定义提示信息
if [ "$LANGUAGE" = "cn" ]; then
    MSG_NO_ROLE_CFG="在 $CONF 中没有找到 role.cfg 文件"
    MSG_EXECUTE_DBAIOps="请先执行 DBAIOps-system-package.sh 脚本！"
    MSG_JAVA_INSTALL_FAIL="Java 安装可能未成功，请检查"
else
    MSG_NO_ROLE_CFG="There is no role.cfg in $CONF"
    MSG_EXECUTE_DBAIOps="please execute DBAIOps-system-package.sh first!"
    MSG_JAVA_INSTALL_FAIL="Java install may not successful, please check"
fi

DBAIOps_HOME=`awk -F '=' '/^DS_BASE_LOCALTION/ {print $2}' $DBAIOps_oper_dir/role.cfg`
CONF=$DBAIOps_HOME

if [ ! -f $CONF/role.cfg ]; then
    echo "$MSG_NO_ROLE_CFG"
    exit 1
else
    . $CONF/role.cfg
fi

ds_hosts=$(awk -F '=' '/^DS_Web|^DS_Collector|^DS_Monitor|^DS_Logana|^DS_Fstask|^DS_Zookeeper|^DS_Other_Executor|^DS_Redis/ {print $2}' $CONF/role.cfg | tr -s '\n' | tr ',' '\n' |sort -u)
ds_web=`awk -F '=' '/^DS_Web/ {print $2}' $CONF/role.cfg`
cmd=$1

if [ -f /usr/software/bin/logs/os_type.txt ]; then
    os_type=`cat /usr/software/bin/logs/os_type.txt`
    if [ -z "$os_type" ]; then
        echo "$MSG_EXECUTE_DBAIOps"
        exit 1
    fi
else
    echo "$MSG_EXECUTE_DBAIOps"
    exit 1
fi

flag_suse=`echo $os_type|grep -i suse`
flag_yum=`echo $os_type|grep -iE 'redhat|centos'`
flag_apt=`echo $os_type|grep -iE 'uos|kylinV4'`
flag_kylinV10=`echo $os_type|grep -i 'kylinV10'`

case $cmd in
    ("-install")
        sh $bin/DBAIOps-java.sh -install_local
        if [ $? -eq 1 ]; then
            echo "$MSG_JAVA_INSTALL_FAIL"
            exit 1
        fi
        if [ ! -z "$flag_yum" ]; then
            install_openoffice_rpm $ds_web
        elif [ ! -z "$flag_kylinV10" ]; then
            install_openoffice_kylinV10
        else
            install_openoffice_apt $ds_web
        fi
        ;;
    (*)
        print_usage
        ;;
esac
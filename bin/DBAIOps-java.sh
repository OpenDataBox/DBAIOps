#!/bin/bash
#
#
#
bin=`dirname "${BASH_SOURCE-$0}"`
bin=`cd "$bin"; pwd`
ROOT=`cd $bin;cd ..;pwd`
DBAIOps_HOME="/usr/software"
DBAIOps_oper_dir=/usr/software
CONF=$DBAIOps_HOME
localnode=`hostname`
cpu_version=`uname -a|grep aarch64`
set -e

# 获取主脚本中的语言设置
if [ -z "$LANGUAGE" ]; then
    LANGUAGE="en"  # 默认英文
fi

print_usage(){
  echo "Usage: DBAIOps java installation script"
  echo "< -install >"
  echo "  -install                       install java environment"
}

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


install() {
    # 多语言提示信息
    if [ "$LANGUAGE" == "cn" ]; then
        local msg_install_java="正在安装 Java..."
        local msg_jdk_not_found="JDK 安装文件不存在！"
        local msg_local_install="本地节点安装 Java 环境..."
        local msg_remote_install="远程节点 $ip 安装 Java 环境..."
        local msg_java_success="Java 安装成功！"
    else
        local msg_install_java="Installing Java..."
        local msg_jdk_not_found="JDK installation file not found!"
        local msg_local_install="Installing Java environment on local node..."
        local msg_remote_install="Installing Java environment on remote node $ip..."
        local msg_java_success="Java installation succeeded!"
    fi

    echo "############################################################"
    if [ "$LANGUAGE" == "cn" ]; then
        echo "                      安装 Java                          "
    else
        echo "                      Install Java                       "
    fi
    echo "############################################################"

    # 检查 JDK 安装文件是否存在
    if [ ! -f $DBAIOps_oper_dir/jdk-8u331-linux-x64.tar.gz ]; then
        c1 "$msg_jdk_not_found" red
        exit 1
    fi

    c1 "$msg_install_java" blue

    for ip in $ds_hosts; do
        if [ "$localnode" == "$ip" ]; then
            # 本地节点安装
            c1 "$msg_local_install" blue
            if [ -z "$cpu_version" ]; then
                cd $DBAIOps_oper_dir
                tar --no-same-owner -xzvf $DBAIOps_oper_dir/jdk-8u331-linux-x64.tar.gz > /dev/null 2>&1
                echo "export JAVA_HOME=$DBAIOps_oper_dir/jdk1.8.0_331" > /etc/profile.d/java.sh
            else
                cd $DBAIOps_oper_dir
                tar --no-same-owner -xzvf $DBAIOps_oper_dir/jdk-8u301-linux-aarch64.tar.gz > /dev/null 2>&1
                rm -rf $DBAIOps_oper_dir/jdk1.8.0_331
                mv jdk1.8.0_301 jdk1.8.0_331
                echo "export JAVA_HOME=$DBAIOps_oper_dir/jdk1.8.0_331" > /etc/profile.d/java.sh
                echo "export JVM_PATH=\$JAVA_HOME/jre/lib/aarch64/server/libjvm.so" >> /etc/profile.d/java.sh
            fi
            echo "export PATH=\$JAVA_HOME/bin:\$PATH" >> /etc/profile.d/java.sh
            chmod 644 /etc/profile.d/java.sh
            sed -i '/.*jdk.tls.disabledAlgorithms=SSLv3*/c\jdk.tls.disabledAlgorithms= RC4, DES, MD5withRSA, \\' $DBAIOps_oper_dir/jdk1.8.0_331/jre/lib/security/java.security
        else
            # 远程节点安装
            c1 "$msg_remote_install" blue
            if [ -z "$cpu_version" ]; then
                ssh $ip "cd $DBAIOps_oper_dir; tar --no-same-owner -xzvf $DBAIOps_oper_dir/jdk-8u331-linux-x64.tar.gz > /dev/null 2>&1; echo \"export JAVA_HOME=$DBAIOps_oper_dir/jdk1.8.0_331\" > /etc/profile.d/java.sh"
            else
                ssh $ip "cd $DBAIOps_oper_dir; tar --no-same-owner -xzvf $DBAIOps_oper_dir/jdk-8u301-linux-aarch64.tar.gz > /dev/null 2>&1; cd $DBAIOps_oper_dir; mv jdk1.8.0_301 jdk1.8.0_331; echo \"export JAVA_HOME=$DBAIOps_oper_dir/jdk1.8.0_331\" > /etc/profile.d/java.sh"
                ssh $ip 'echo "export JVM_PATH=\$JAVA_HOME/jre/lib/aarch64/server/libjvm.so" >> /etc/profile.d/java.sh'
            fi
            ssh $ip 'echo "export PATH=\$JAVA_HOME/bin:\$PATH" >> /etc/profile.d/java.sh'
            ssh $ip "chmod 644 /etc/profile.d/java.sh"
            ssh $ip "sed -i '/.*jdk.tls.disabledAlgorithms=SSLv3*/c\jdk.tls.disabledAlgorithms= RC4, DES, MD5withRSA, \\' $DBAIOps_oper_dir/jdk1.8.0_331/jre/lib/security/java.security"
        fi
    done

    c1 "$msg_java_success" green
}

install_local()
{
    cd $DBAIOps_oper_dir
    if [ -f /usr/software/jdk1.8.0_331/bin/java ];then
		echo "local node have installed java"
    else
        if [ ! -f $DBAIOps_oper_dir/jdk-8u331-linux-x64.tar.gz ];then
            echo "jdk安装文件不存在！"
            exit 1
        fi
    	if [ -z "$cpu_version" ];then
            tar --no-same-owner -xzvf $DBAIOps_oper_dir/jdk-8u331-linux-x64.tar.gz > /dev/null
            echo "export JAVA_HOME=$DBAIOps_oper_dir/jdk1.8.0_331" > /etc/profile.d/java.sh
        else
            tar --no-same-owner -xzvf $DBAIOps_oper_dir/jdk-8u301-linux-aarch64.tar.gz > /dev/null
            echo "export JAVA_HOME=$DBAIOps_oper_dir/jdk1.8.0_301" > /etc/profile.d/java.sh
            echo "export JVM_PATH=\$JAVA_HOME/jre/lib/aarch64/server/libjvm.so" >> /etc/profile.d/java.sh
        fi
        echo "export PATH=\$JAVA_HOME/bin:\$PATH" >> /etc/profile.d/java.sh
        chmod 644 /etc/profile.d/java.sh
    fi
}

if [ ! -f $CONF/role.cfg ];then
    echo "There is no role.cfg in $CONF"
    exit 1
else 
    . $CONF/role.cfg
fi

ds_hosts=$(awk -F '=' '/^DS_Web|^DS_Collector|^DS_Monitor|^DS_Logana|^DS_Fstask|^DS_Other_Executor|^DS_Zookeeper|^DS_Redis/ {print $2}' $CONF/role.cfg | tr -s '\n' | tr ',' '\n' |sort -u)

if [ -z $DBAIOps_oper_dir ];then
    echo "DBAIOps安装目录不存在！"
    exit 1
fi

case $1 in
        "-install")
                install $ds_hosts
        ;;
        "-install_local")
                install_local
        ;;
        *)
                print_usage
                exit 1
        ;;
esac

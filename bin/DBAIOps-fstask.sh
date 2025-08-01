#!/bin/bash
#
#
set -e
bin=`dirname "${BASH_SOURCE-$0}"`
bin=`cd "$bin"; pwd`
ROOT=`cd $bin;cd ..;pwd`
DBAIOps_HOME="/usr/software"
DBAIOps_oper_dir=/usr/software
fstask_home=$DBAIOps_oper_dir/fstaskpkg
CONF=$DBAIOps_HOME
localnode=`hostname`
local_ip=`hostname -i|awk '{print $1}'`

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
    echo "Usage: DBAIOps fsTask management script"
    echo "  -start                         start fstask service"
    echo "  -stop                          stop fstask service"
    echo "  -status                        check fstask service status"
    echo "  -install                       install fstask service"
    echo "  -clean			 clean fstask server"
}

install() {
    # 多语言提示信息
    if [ "$LANGUAGE" == "cn" ]; then
        local msg_install_fstask="正在安装 fsTask..."
        local msg_fstask_not_found="fstaskpkg 安装包不存在！"
        local msg_local_install="本地节点安装 fstask 管理服务和执行器服务..."
        local msg_remote_install="远程节点 $ip 安装 fstask 管理服务和执行器服务..."
        local msg_extra_executor="远程节点 $ip 安装 fstask 执行器服务..."
        local msg_fstask_success="fsTask 安装成功！"
    else
        local msg_install_fstask="Installing fsTask..."
        local msg_fstask_not_found="fstaskpkg installation package not found!"
        local msg_local_install="Installing fstask admin and executor service on local node..."
        local msg_remote_install="Installing fstask admin and executor service on remote node $ip..."
        local msg_extra_executor="Installing fstask executor service on remote node $ip..."
        local msg_fstask_success="fsTask installation succeeded!"
    fi

    echo "############################################################"
    if [ "$LANGUAGE" == "cn" ]; then
        echo "                      安装 fsTask                       "
    else
        echo "                      Install fsTask                    "
    fi
    echo "############################################################"

    c1 "$msg_install_fstask" blue

    for ip in $fstlist; do
        if [ "$localnode" == "$ip" ]; then
            # 本地节点安装
            c1 "$msg_local_install" blue
            if [ ! -f $DBAIOps_oper_dir/fstaskpkg.tar.gz ]; then
                c1 "$msg_fstask_not_found" red
                exit 1
            fi
            cd $DBAIOps_oper_dir
            tar --no-same-owner -xzvf $DBAIOps_oper_dir/fstaskpkg.tar.gz > /dev/null 2>&1
            cd $fstask_home/bin
            source /etc/profile.d/python3.sh
            source /etc/profile.d/java.sh
            sed -i "s/127.0.0.1:2181/$DFC_ZK_CONN/g" $fstask_home/bin/initZk.py
            sh $fstask_home/bin/init.sh
            sh $fstask_home/bin/fsTaskCli.sh install
        else
            # 远程节点安装
            c1 "$msg_remote_install" blue
            ssh $ip "
                if [ ! -f $DBAIOps_oper_dir/fstaskpkg.tar.gz ]; then
                    echo '$msg_fstask_not_found'
                    exit 1
                fi
                cd $DBAIOps_oper_dir
                tar --no-same-owner -xzvf $DBAIOps_oper_dir/fstaskpkg.tar.gz > /dev/null 2>&1
                cd $fstask_home/bin
                source /etc/profile.d/python3.sh
                source /etc/profile.d/java.sh
                sed -i 's/127.0.0.1:2181/$DFC_ZK_CONN/g' $fstask_home/bin/initZk.py
                sh $fstask_home/bin/init.sh
                sh $fstask_home/bin/fsTaskCli.sh install
            "
        fi
    done

    if [ -n "$extraExecutor" ]; then
        for ip in $extraExecutor; do
            # 安装额外的执行器服务
            c1 "$msg_extra_executor" blue
            ssh $ip "
                if [ ! -f $DBAIOps_oper_dir/fstaskpkg.tar.gz ]; then
                    echo '$msg_fstask_not_found'
                    exit 1
                fi
                cd $DBAIOps_oper_dir
                tar --no-same-owner -xzvf $DBAIOps_oper_dir/fstaskpkg.tar.gz > /dev/null 2>&1
                cd $fstask_home/bin
                source /etc/profile.d/python3.sh
                source /etc/profile.d/java.sh
                sed -i 's/127.0.0.1:2181/$DFC_ZK_CONN/g' $fstask_home/bin/initZk.py
                sh $fstask_home/bin/init.sh
                sh $fstask_home/bin/fsTaskCli.sh install executor
            "
        done
    fi

    c1 "$msg_fstask_success" green
}

start()
{
    echo "############################################################"
    echo "                       start fsTask                         "
    echo "############################################################"
    for ip in $fstlist
    do
        if [[ $localnode == $ip || $local_ip == $ip ]];then
        echo "local node start fstask"
        sh $fstask_home/bin/fsTaskCli.sh start admin
        else
        echo "$ip:"
        ssh $ip "sh $fstask_home/bin/fsTaskCli.sh start admin > /dev/null 2>&1"
        fi
    done

    if [ "$extraExecutor" != "" ];then
        for ip in $extraExecutor
        do
            echo "$ip:"
            ssh $ip "sh $fstask_home/bin/fsTaskCli.sh start > /dev/null 2>&1"
        done
    fi
    #if [ $? -eq 0 ];then
    #    echo "fsTask Start Successed!"
    #else
    #    echo "fsTask Start Failed!"
    #    exit 1
    #fi
}

stop()
{   echo "############################################################"
    echo "                       stop fsTask                          "
    echo "############################################################"
    for ip in $fstlist
    do
        if [[ $localnode == $ip || $local_ip == $ip ]];then
        echo "local node stop fstask"
        sh $fstask_home/bin/fsTaskCli.sh stop
        else
        echo "$ip:"
        ssh $ip "sh $fstask_home/bin/fsTaskCli.sh stop"
        fi
    done
   
    if [ "$extraExecutor" != "" ];then
        for ip in $extraExecutor
        do
            echo "$ip:"
            ssh $ip "sh $fstask_home/bin/fsTaskCli.sh stop"
        done
    fi
}

status()
{
    echo "############################################################"
    echo "                       status fsTask                        "
    echo "############################################################"
    #sh $fstask_home/bin/fsTaskCli.sh status
    for ip in $fstlist
    do
        if [ $localnode == $ip ];then
        echo "local node fstask status"
        PROC=`ps -ef | grep "fstaskpkg/lib/tomcat-apache-fstask"|grep -v grep|awk '{print $2}'`
        else
        echo "$ip:"
        PROC=`ssh $ip "ps -ef | grep fstaskpkg/lib/tomcat-apache-fstask|grep -v grep|awk '{print \\\$2}'"`
        fi
        if [ "$PROC" ]; then
            echo "fsTask is running (PID:$PROC)!"
        else
            echo "fsTask not started!"
        fi
    done
    
    if [ "$extraExecutor" != "" ];then
        for ip in $extraExecutor
        do
            echo "$ip:"
            PROC=`ssh $ip "ps -ef | grep fstaskpkg/lib/tomcat-apache-fstask|grep -v grep|awk '{print \\\$2}'"`
            if [ "$PROC" ]; then
                echo "fsTask is running (PID:$PROC)!"
            else
                echo "fsTask not started!"
            fi
        done
    fi
}

kill()
{
    echo "############################################################"
    echo "                       kill fsTask                          "
    echo "############################################################"
    for ip in $fstlist
    do
        if [[ $localnode == $ip || $local_ip == $ip ]];then
        echo "local node stop fstask"
        sh $fstask_home/bin/fsTaskCli.sh stop
        else
        echo "$ip:"
        ssh $ip "sh $fstask_home/bin/fsTaskCli.sh stop"
        fi
    done
   
    if [ "$extraExecutor" != "" ];then
        for ip in $extraExecutor
        do
            echo "$ip:"
            ssh $ip "sh $fstask_home/bin/fsTaskCli.sh stop"
        done
    fi
}

clean()
{
    echo "###########################################################"
    echo "                     clean fsTask                          "
    echo "###########################################################"
    for ip in $fstlist
    do
        if [ $localnode == $ip ];then
        echo "local node clean fstask"
        rm -rf $fstask_home
        echo "fsTask admin clean successful"
        else
        echo "$ip:"
        ssh $ip "rm -rf $fstask_home"
        echo "$ip fsTask admin clean successful"
        fi
    done

    if [ "$extraExecutor" != "" ];then
        for ip in $extraExecutor
        do
            echo "$ip:"
            ssh $ip "rm -rf $fstask_home"
            echo "$ip fsTask executor clean successful"
        done
    fi

    python3 /usr/software/bin/InitFaskTable.py

}

if [ -z $DBAIOps_oper_dir ];then
    echo "DBAIOps安装目录不存在！"
    exit 1
fi

if [ ! -f $CONF/role.cfg ];then
    echo "There is no role.cfg in $CONF"
    exit 1
else
    . $CONF/role.cfg
fi

. $DBAIOps_HOME/DBAIOps.cfg

fstl=`awk -F '=' '/^DS_Fstask/ {print $2}' $CONF/role.cfg`
fstlnum=`echo $fstl | tr ',' '\n' |wc -l`
extraExecutor=`awk -F '=' '/^DS_Other_Executor/ {print $2}' $CONF/role.cfg`

if [ $fstlnum -gt 1 ];then
    echo "Fstask服务仅支持一个节点!"
    exit 1
fi

if [ -z $2 ];then
    fstlist=`echo $fstl | tr ',' '\n'`
else
    fstlist=$2
fi

if [ "$extraExecutor" != "" ];then
    extraExecutor=`echo $extraExecutor | tr ',' '\n'`
else
    extraExecutor=""
fi


case $1 in
        "-start")
                start $fstlist $extraExecutor
        ;;
        "-stop")
                stop $fstlist $extraExecutor
        ;;
        "-kill")
                kill $fstlist $extraExecutor
        ;;
        "-status")
                status $fstlist $extraExecutor
        ;;
        "-install")
                install $fstlist $extraExecutor
        ;;
        "-clean")
                clean $fstlist $extraExecutor
        ;;
        *)
                print_usage
                exit 1
        ;;
esac

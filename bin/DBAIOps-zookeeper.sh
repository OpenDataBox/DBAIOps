#!/bin/bash
#
#
set -e
bin=`dirname "${BASH_SOURCE-$0}"`
bin=`cd "$bin"; pwd`
ROOT=`cd $bin;cd ..;pwd`
DBAIOps_HOME="/usr/software"
DBAIOps_oper_dir=/usr/software
zk_home=$DBAIOps_oper_dir/zookeeper-3.7.1
zk_data=$DBAIOps_oper_dir/zkdata
CONF=$DBAIOps_HOME
MYID_HOME=/usr/software/zkdata
localnode=`hostname`
local_ip=`hostname -i|awk '{print $1}'`

# 获取主脚本中的语言设置
if [ -z "$LANGUAGE" ]; then
    LANGUAGE="en"  # 默认英文
fi

print_usage(){
    echo "Usage: DBAIOps zookeeper management script"
    echo "< -install | -start | -stop | -status | -clean >"
    echo "  -install                       install zookeeper service"
    echo "  -start                         start zookeeper service"
    echo "  -stop                          stop zookeeper service"
    echo "  -status                        check zookeeper service status"
    echo "  -clean                         clean zookeeper service"
}

install() {
    # 日志文件路径
    LOG_FILE="/var/log/DBAIOps_install.log"

    # 函数用于记录日志并输出提示信息
    log_message() {
        local english_msg="$1"
        local chinese_msg="$2"
        local log_msg

        # 根据语言选择提示信息
        if [ "$LANGUAGE" = "en" ]; then
            echo "$english_msg"
            log_msg="$english_msg"
        else
            echo "$chinese_msg"
            log_msg="$chinese_msg"
        fi

        # 记录日志
        echo "$(date '+%Y-%m-%d %H:%M:%S') - $log_msg" >> "$LOG_FILE"
    }

    log_message "############################################################" "############################################################"
    log_message "                   Installing Zookeeper                        " "                   正在安装 Zookeeper                        "
    log_message "############################################################" "############################################################"

    # 检查 Zookeeper 安装文件是否存在
    if [ ! -f "$DBAIOps_oper_dir/zookeeper-3.7.1.tar.gz" ]; then
        log_message "Zookeeper installation file does not exist!" "Zookeeper 安装文件不存在！"
        exit 1
    fi

    # 生成服务器配置信息
    sinfo=""
    nm=1
    for ip in $zklist; do
        sinfo=$sinfo"server."$nm"="$ip":2888:3888,"
        nm=$((nm + 1))
    done
    unset nm
    serverinfo=$(echo "$sinfo" | sed 's/,$//' | tr ',' '\n')

    # 安装 Zookeeper
    myid=1
    for ip in $zklist; do
        if [ "$localnode" == "$ip" ]; then
            log_message "Installing Zookeeper on local node..." "正在本地节点安装 Zookeeper..."
            cd "$DBAIOps_oper_dir"
            tar --no-same-owner -xzvf "$DBAIOps_oper_dir/zookeeper-3.7.1.tar.gz" > /dev/null 2>&1
            echo "$serverinfo" >> "$DBAIOps_oper_dir/zookeeper-3.7.1/conf/zoo.cfg"
            mkdir -p "$MYID_HOME"
            echo "$myid" > "$MYID_HOME/myid"
        else
            log_message "Installing Zookeeper on remote node: $ip..." "正在远程节点 $ip 安装 Zookeeper..."
            ssh "$ip" "cd $DBAIOps_oper_dir; tar --no-same-owner -xzvf $DBAIOps_oper_dir/zookeeper-3.7.1.tar.gz > /dev/null 2>&1; echo \"$serverinfo\" >> $DBAIOps_oper_dir/zookeeper-3.7.1/conf/zoo.cfg"
            ssh "$ip" "mkdir -p $MYID_HOME; echo $myid > $MYID_HOME/myid"
        fi
        myid=$((myid + 1))
    done
    unset myid

    log_message "Zookeeper installation completed successfully!" "Zookeeper 安装成功完成！"
}

start()
{
    echo "############################################################"
    echo "                   start zookeeper                          "
    echo "############################################################"
    for ip in $zklist
    do
        if [[ $localnode == $ip || $local_ip == $ip ]];then
            echo "local node start zookeeper"
            source /etc/profile.d/java.sh
            # 检查 Zookeeper 是否在运行
            if ps aux | grep -v grep | grep /usr/software/zookeeper-3.7.1/bin/ > /dev/null
            then
                echo "Zookeeper is already running."
            else
                $zk_home/bin/zkServer.sh start
            fi
        else
            echo "$ip:"
            ssh $ip "source /etc/profile.d/java.sh;$zk_home/bin/zkServer.sh start"
        fi
    done
}

stop()
{
    echo "############################################################"
    echo "                   stop zookeeper                           "
    echo "############################################################"
    for ip in $zklist
    do
        if [[ $localnode == $ip || $local_ip == $ip ]];then
        echo "local node stop zookeeper"
        source /etc/profile.d/java.sh
        set +e
        $zk_home/bin/zkServer.sh stop
        else
        echo "$ip:"
        ssh $ip "source /etc/profile.d/java.sh;$zk_home/bin/zkServer.sh stop"
        fi
    done
}

kill()
{
    echo "############################################################"
    echo "                   kill zookeeper                           "
    echo "############################################################"
    for ip in $zklist
    do
        if [[ $localnode == $ip || $local_ip == $ip ]];then
        echo "local node stop zookeeper"
        source /etc/profile.d/java.sh
        set +e
        $zk_home/bin/zkServer.sh stop
        else
        echo "$ip:"
        ssh $ip "source /etc/profile.d/java.sh;$zk_home/bin/zkServer.sh stop"
        fi
    done
}

status()
{
    echo "############################################################"
    echo "                   status zookeeper                         "
    echo "############################################################"
    for ip in $zklist
    do
        if [ $localnode == $ip ];then
        echo "local node zookeeper status"
        zk_pid=`ps -ef| grep -i zookeeper-3.7.1|grep -v grep |awk '{print $2}'`
        if [ -z "$zk_pid" ];then
            echo "Zookeeper is not running!"
        else
            echo "Zookeeper is running (PID:$zk_pid)!"
        fi
        unset zkpid
        else
        echo "$ip:"
        zk_pid=`ssh $ip "ps -ef| grep -i zookeeper-3.7.1|grep -v grep |awk '{print \\$2}'"`
        if [ -z "$zk_pid" ]; then
            echo "Zookeeper is not running!"
        else 
            echo "Zookeeper is running (PID:$zk_pid)!"
        fi
        unset zkpid
        fi
    done
}

clean()
{
    echo "############################################################"
    echo "                   clean zookeeper                          "
    echo "############################################################"
    for ip in $zklist
    do
        if [ $localnode == $ip ];then
        echo "local node clean zookeeper enviroment"
        rm -rf $zk_home $zk_data
        else
        echo "$ip:"
        ssh $ip "rm -rf $zk_home $zk_data"
        fi
        echo "$ip Zookeeper clean successful"
    done
}

if [ $# = 0 ]; then
    print_usage
    exit 1
fi

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

dszk=`awk -F '=' '/^DS_Zookeeper/ {print $2}' $CONF/role.cfg`
dszknum=`echo $dszk | tr ',' '\n' |wc -l`
if ((dszknum>3));then
    echo "Please check the role.cfg, Zookeeper must be less than 3 nodes"
    exit 1
fi

if [ -z $2 ];then
    zklist=`echo $dszk | tr ',' '\n'`
else
    zklist=$2
fi

case $1 in
        "-install")
                install $zklist
        ;;
        "-start")
                start $zklist
        ;;
        "-stop")
                stop $zklist
        ;;
        "-kill")
                kill $zklist
        ;;
        "-status")
                status $zklist
        ;;
        "-clean")
                clean $zklist
        ;;
        *)
                print_usage
                exit 1
        ;;
esac

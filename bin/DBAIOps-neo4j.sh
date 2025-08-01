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
webl=`awk -F '=' '/^DS_Web/ {print $2}' $CONF/role.cfg`

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


set -e
print_usage(){
    echo "Usage: DBAIOps neo4j installation script"
    echo "< -install >"
    echo "  -install                       install neo4j environment"
    echo "< -start >"
    echo "  -start                       start neo4j environment"
    echo "< -stop >"
    echo "  -stop                       stop neo4j environment"
    echo "< -status >"
    echo "  -status                       status neo4j environment"
    echo "< -clean >"
    echo "  -clean                       clean neo4j environment"
}


install() {
    # 多语言提示信息
    if [ "$LANGUAGE" == "cn" ]; then
        local msg_neo4j_not_found="neo4j 安装文件不存在！"
        local msg_install_neo4j="正在安装 neo4j..."
        local msg_local_install="本地节点安装 neo4j 环境..."
        local msg_remote_install="远程节点 $webl 安装 neo4j 环境..."
        local msg_neo4j_success="neo4j 安装成功！"
    else
        local msg_neo4j_not_found="neo4j installation file not found!"
        local msg_install_neo4j="Installing neo4j..."
        local msg_local_install="Installing neo4j environment on local node..."
        local msg_remote_install="Installing neo4j environment on remote node $webl..."
        local msg_neo4j_success="neo4j installation succeeded!"
    fi

    # 检查 neo4j 安装文件是否存在
    if [ ! -f $DBAIOps_oper_dir/neo4j.tar ]; then
        c1 "$msg_neo4j_not_found" red
        exit 1
    fi

    echo "############################################################"
    if [ "$LANGUAGE" == "cn" ]; then
        echo "                      安装 neo4j                          "
    else
        echo "                      Install neo4j                       "
    fi
    echo "############################################################"

    c1 "$msg_install_neo4j" blue

    if [ "$localnode" == "$webl" ]; then
        # 本地节点安装
        c1 "$msg_local_install" blue
        ip=$(hostname -i | awk '{print $1}')
        cd $DBAIOps_oper_dir
        tar --no-same-owner -xvf $DBAIOps_oper_dir/neo4j.tar > /dev/null 2>&1
        echo "export NEO4J_HOME=/usr/software/neo4j/neo4j-4.4.8" > /etc/profile.d/neo4j.sh
        echo "export PATH=\$NEO4J_HOME/bin:\$PATH" >> /etc/profile.d/neo4j.sh
        chmod 644 /etc/profile.d/neo4j.sh
    else
        # 远程节点安装
        c1 "$msg_remote_install" blue
        ip=$(ssh $webl "hostname -i | awk '{print \$1}'")
        ssh $webl "cd $DBAIOps_oper_dir; tar --no-same-owner -xzvf $DBAIOps_oper_dir/neo4j.tar > /dev/null 2>&1; echo \"export NEO4J_HOME=/usr/software/neo4j/neo4j-4.4.8\" > /etc/profile.d/neo4j.sh"
        ssh $webl 'echo "export PATH=\$NEO4J_HOME/bin:\$PATH" >> /etc/profile.d/neo4j.sh'
        ssh $webl "chmod 644 /etc/profile.d/neo4j.sh"
    fi

    c1 "$msg_neo4j_success" green
}

start()
{
	echo "############################################################"
    echo "                      start neo4j                           "
	echo "############################################################"
    if [ "$localnode" == "$webl" ];then
        source /etc/profile.d/neo4j.sh
        neo4j start 
    else
        ssh $webl "source /etc/profile.d/neo4j.sh;neo4j start "
    fi
}


stop()
{
    echo "############################################################"
    echo "                      stop neo4j                           "
    echo "############################################################"
    if [ "$localnode" == "$webl" ];then
        source /etc/profile.d/neo4j.sh
        neo4j stop 
    else
        ssh $webl "source /etc/profile.d/neo4j.sh;neo4j stop"
    fi
}

clean()
{
	echo "############################################################"
    echo "                      clean neo4j                           "
    echo "############################################################"
	if [ "$localnode" == "$webl" ];then
        if [ -d /usr/software/neo4j ];then
            source /etc/profile.d/neo4j.sh
            set +e
            flag=`ps -ef|grep "/usr/software/neo4j"|grep -v grep`
            if [ ! -z "$flag" ];then
                neo4j stop
            fi
            rm -rf /usr/software/neo4j
        fi
    else
        ssh $webl "source /etc/profile.d/neo4j.sh;neo4j stop"
        ssh $webl "rm -rf /usr/software/neo4j"
    fi
}

status()
{
	echo "############################################################"
    echo "                      status neo4j                          "
    echo "############################################################"
    if [ "$localnode" == "$webl" ];then
        source /etc/profile.d/neo4j.sh
        neo4j status
    else
        ssh $webl "source /etc/profile.d/neo4j.sh;neo4j status"
    fi
}

if [ ! -f $CONF/role.cfg ];then
    echo "There is no role.cfg in $CONF"
    exit 1
else 
    . $CONF/role.cfg
fi


if [ -z $DBAIOps_oper_dir ];then
    echo "DBAIOps安装目录不存在！"
    exit 1
fi


hosts=$(awk -F '=' '/^DS_Web|^DS_Collector|^DS_Monitor|^DS_Logana|^DS_Fstask|^DS_Other_Executor|^DS_Zookeeper|^DS_Redis/ {print $2}' $CONF/role.cfg | tr -s '\n' | tr ',' '\n' |sort -u |tr '\n' ',')
hosts=${hosts%,}
hlist=`echo $hosts | tr ',' '\n'`

case $1 in
        "-install")
                install
        ;;
        "-start")
                start
        ;;
        "-stop")
                stop
        ;;
        "-clean")
                clean
        ;;
        "-status")
                status
        ;;
        *)
                print_usage
                exit 1
        ;;
esac

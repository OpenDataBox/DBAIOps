#!/bin/bash
#
# set -e
bin=`dirname "${BASH_SOURCE-$0}"`
bin=`cd "$bin"; pwd`
ROOT=`cd $bin;cd ..;pwd`
current_dir="$(dirname $(dirname $(cd "$(dirname "$0")"; pwd -P)/$(basename "$0")))"
DBAIOps_oper_dir='/usr/software'
DBAIOps_HOME=$DBAIOps_oper_dir
CONF=$DBAIOps_HOME
localnode=`hostname`
localip=`hostname -i|awk '{print $1}'`
selected_ip='127.0.0.1'


# 日志文件路径
DBAIOps_log="/usr/software/bin/logs/DBAIOps_install.log"

# 语言选择
LANGUAGE="en"

# 日志记录函数
log() {
    local log_level=$1
    local message=$2
    local timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    echo -e "[$timestamp] [$log_level] $message" | tee -a $DBAIOps_log
}


# 语言选择函数
select_language() {
    c1 "请选择安装语言 / Please select installation language:" blue
    echo "1. 中文"
    echo "2. English"
    read -p "请输入选择 / Please enter your choice (1 or 2): " lang_choice
    case $lang_choice in
        1) LANGUAGE="cn" ;;
        2) LANGUAGE="en" ;;
        *) c1 "无效的选择，默认使用英文 / Invalid choice, defaulting to English." red
        LANGUAGE="en" ;;
    esac
    export LANGUAGE # 导出为环境变量
}

# 根据语言显示提示信息
show_message() {
    local cn_message=$1
    local en_message=$2
    if [ "$LANGUAGE" == "cn" ]; then
        c1 "$cn_message" blue
    else
        c1 "$en_message" blue
    fi
}

# show_message "正在进行环境检查..." "Performing environment check..."
# log "INFO" "Environment check completed."


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

print_usage() {
    if [ "$LANGUAGE" == "cn" ]; then
        echo "用法: DBAIOps 运维脚本介绍"
        echo "< -envcheck |-install | -start | -stop | -status | -clean | -version >"
        echo "  -envcheck                     在安装 DBAIOps 前检查操作系统环境"
        echo "  -install                      安装 DBAIOps 服务"
        echo "  -start                        启动 DBAIOps 服务"
        echo "  -stop                         停止 DBAIOps 服务"
        echo "  -status                       查看 DBAIOps 服务状态"
        echo "  -reinstall                    重新安装 DBAIOps 服务"
        echo "  -restart                      重启 DBAIOps 服务"
        echo "  -clslog                       清理日志文件以释放磁盘空间"
        echo "  -version                      显示 DBAIOps 版本"
        echo "  -upgrade                      升级 DBAIOps 版本"
        echo "  -updatecomp                   更新 DBAIOps 组件"
    else
        echo "Usage: DBAIOps operation and maintenance script introduction"
        echo "< -envcheck |-install | -start | -stop | -status | -clean | -version >"
        echo "  -envcheck                     before install DBAIOps check OS environment"
        echo "  -install                      install DBAIOps Service"
        echo "  -start                        launch DBAIOps Service"
        echo "  -stop                         stop DBAIOps Service"
        echo "  -status                       show DBAIOps Service status"
        echo "  -reinstall                    reinstall DBAIOps Service"
        echo "  -restart                      restart DBAIOps Service"
        echo "  -clslog                       clean logfile release disk space"
        echo "  -version                      show DBAIOps version"
        echo "  -upgrade                      upgrade DBAIOps version"
        echo "  -updatecomp                   update DBAIOps component"
    fi
}

cmd=$1
case $cmd in
        ("-version")
        DBAIOps_version="5.1"
        if [ -z $DBAIOps_version ];then
                echo "DBAIOps Standard Edition" "Unknow"
        else
                echo "DBAIOps Standard Edition" $DBAIOps_version
        fi
        exit 0
        ;;
esac
unset cmd


install()
{
    # 安装依赖包
    c1 "第一步：安装相关RPM包" blue
    if [ -f /usr/software/bin/logs/os_type.txt ];then
        os_type=`cat /usr/software/bin/logs/os_type.txt`
        if [ -z "$os_type" ];then
            sh $bin/DBAIOps-system-package.sh -install
            if [ $? -eq 1 ];then
                c1 "系统依赖包安装失败,请检查" red
                exit 1
            fi
        fi
    else
        sh $bin/DBAIOps-system-package.sh -install
        if [ $? -eq 1 ];then
            c1 "系统依赖包安装失败,请检查" red
            exit 1
        fi
    fi
    c1 "系统依赖包安装成功" green
    set +e
    sh $bin/DBAIOps-openoffice.sh -install
    if [ $? -eq 1 ];then
        c1 'openoffice install failed,please re-execute the "DBAIOps-openoffice.sh -install" command after the execution of DBAIOps.sh is complete' red
    fi
    set -e
	if [ "$type" == "retry" ];then
		c1 "第二步：开始安装PostgreSQL(需要10~30分钟)" blue
		echo "DBAIOps retry install, skip package deploy and pg db install"
	else
        sh $bin/DBAIOps-pkg.sh -install
        c1 "第二步：开始安装PostgreSQL(需要10~30分钟)" blue
        pg_ip=`cat /usr/software/role.cfg | grep DSPG_Node|cut -d '=' -f2`
        # 是否是本机
        if [ "$localip" == "$pg_ip" ];then
            if [ -f /usr/software/bin/DBAIOps_pg.log ];then
                if grep -q "CREATE INDEX" /usr/software/bin/DBAIOps_pg.log;
                    then c1 "PostgreSQL数据库已经安装，跳过..." green
                else
                    c1 "本机安装PostgreSQL" blue
                    sh $bin/DBAIOps-pg.sh -install $localip
                fi
            else
                c1 "本机安装PostgreSQL" blue
                sh $bin/DBAIOps-pg.sh -install $localip
            fi
        else
            if ssh $pg_ip "grep -q "CREATE INDEX" /tmp/DBAIOps_pg.log";
                then c1 "PostgreSQL数据库已经安装，跳过..." green
            else
                c1 "远程安装PostgreSQL" blue
                sh $bin/DBAIOps-pg.sh -install $pg_ip
            fi
        fi
	fi
		
    c1 "第三步：开始安装Python相关模块(需要30~60分钟)" blue
    sh $bin/DBAIOps-python3.sh -install
    if [ $? -eq 1 ];then
        c1 "Python3 install may not successful,please check" red
        exit 1
    fi

    sh $bin/DBAIOps-python3.sh -install_thirdlib
    if [ $? -eq 1 ];then
        c1 "Python3 thirdlib install may not successful,please check" red
        exit 1
    fi

    c1 "第四步：开始安装Python rpm" blue
    sh $bin/DBAIOps-python3.sh -install_rpm
    if [ $? -eq 1 ];then
        c1 "Python3 rpm install may not successful,please check" red
        exit 1
    fi

    c1 "第五步：开始安装Oracle客户端" blue
    sh $bin/DBAIOps-orainst.sh -install
    if [ $? -eq 1 ];then
        c1 "Oracle python3 client install may not successful,please check" red
        exit 1
    fi

    c1 "第六步：开始安装zookeeper" blue
    sh $bin/DBAIOps-zookeeper.sh -install
    if [ $? -eq 1 ];then
        c1 "Zookeeper install may not successful,please check" red
        exit 1
    fi

    sh $bin/DBAIOps-zookeeper.sh -start
    if [ $? -eq 1 ];then
        c1 "Zookeeper install may not successful,please check" red
        exit 1
    fi

    c1 "第七步：开始安装redis" blue
    sh $bin/DBAIOps-redis-single.sh -install
    if [ $? -eq 1 ];then
        c1 "Redis install may not successful,please check" red
        exit 1
    fi

    c1 "第八步：开始安装phantomjs" blue
    sh $bin/DBAIOps-phantomjs.sh -install
    if [ $? -eq 1 ];then
        c1 "Phantomjs install may not successful,please check" red
        exit 1
    fi

    c1 "第九步：开始安装任务平台" blue
    sh $bin/DBAIOps-fstask.sh -install
    if [ $? -eq 1 ];then
        c1 "Fstask install may not successful,please check" red
        exit 1
    fi

    c1 "第十步：开始安装Neo4j" blue
    sh $bin/DBAIOps-neo4j.sh -install
    if [ $? -eq 1 ];then
        c1 "neo4j install may not successful,please check" red
        exit 1
    fi

    sh $bin/DBAIOps-fstask.sh -stop
    if [ $? -eq 1 ];then
        c1 "Fstask install may not successful,please check" red
        exit 1
    fi
    
    sh $bin/DBAIOps-zookeeper.sh -stop
    c1 "Configurations,DBAIOps install Successful!" green
}

upgrade_file(){
    for ip in $hlist
    do
        echo $ip
        dt=`date +%Y%m%d%H%M`
        dir_name=bak${dt}
        if [ "$localnode" == "$ip" ];then
            mkdir -p $DBAIOps_oper_dir/patches/$dir_name
        else
            ssh $ip "mkdir -p $DBAIOps_oper_dir/patches/$dir_name"
        fi

        if [ "$localnode" == "$ip" ];then
            flst=`ls $1`
        else
            flst=`ssh $ip "ls $1"`
        fi

        for file in $flst
        do
            if [ -e $DBAIOps_oper_dir/$file ];then
                if [ "$file" = "python3" ];then
                    echo "python3 directory not mv"
                elif [ "$file" = "patches" ];then
                    echo "patches directory not mv"
                elif [ "$file" = "role.cfg" ];then
                    echo "role.cfg not mv"
                elif [ "$file" = "DBAIOps.cfg" ];then
                    echo "DBAIOps.cfg not mv"
                else
                    echo "$file backup"
                    if [ "$localnode" == "$ip" ];then
                        if [ "$file" = "fstaskpkg" ];then
                            mkdir -p $DBAIOps_oper_dir/patches/$dir_name/fstaskpkg
                            mv $DBAIOps_oper_dir/fstaskpkg/war $DBAIOps_oper_dir/patches/$dir_name/fstaskpkg
                            cp -r $DBAIOps_oper_dir/fstaskpkg/bin $DBAIOps_oper_dir/patches/$dir_name/fstaskpkg
                        else
                            mv $DBAIOps_oper_dir/$file $DBAIOps_oper_dir/patches/$dir_name
                        fi
                    else
                        ssh $ip "if [ -e $DBAIOps_oper_dir/$file ];then if [ $file = \"fstaskpkg\" ];then mkdir -p $DBAIOps_oper_dir/patches/$dir_name/fstaskpkg;mv $DBAIOps_oper_dir/fstaskpkg/war $DBAIOps_oper_dir/patches/$dir_name/fstaskpkg;cp -r $DBAIOps_oper_dir/fstaskpkg/bin $DBAIOps_oper_dir/patches/$dir_name/fstaskpkg;else mv $DBAIOps_oper_dir/$file $DBAIOps_oper_dir/patches/$dir_name;fi;fi"
                    fi
                fi
            fi

            if [[ "$file" =~ "upgrade" ]];then
                echo "upgrade sql not mv"
            elif [[ "$file" =~ "python3" ]];then
                if [ "$localnode" == "$ip" ];then
                    cp -r $DBAIOps_oper_dir/patches/software/$file $DBAIOps_oper_dir
                else
                    ssh $ip "cp -r $DBAIOps_oper_dir/patches/software/$file $DBAIOps_oper_dir"
                fi
            elif [ "$file" = "fstaskpkg" ];then
                if [ "$localnode" == "$ip" ];then
                    mv $DBAIOps_oper_dir/patches/software/fstaskpkg/war $DBAIOps_oper_dir/fstaskpkg
                    \cp $DBAIOps_oper_dir/patches/software/fstaskpkg/bin/*.sh $DBAIOps_oper_dir/fstaskpkg/bin
                else
                    ssh $ip "if [ -e $DBAIOps_oper_dir/patches/software/fstaskpkg/war ];then mv $DBAIOps_oper_dir/patches/software/fstaskpkg/war $DBAIOps_oper_dir/fstaskpkg;fi"
                    ssh $ip "if [ -e $DBAIOps_oper_dir/patches/software/fstaskpkg/bin ];then \cp $DBAIOps_oper_dir/patches/software/fstaskpkg/bin/*.sh $DBAIOps_oper_dir/fstaskpkg/bin;fi"
                fi
            elif [ "$file" = "patches" ];then
                echo "patches not mv"
            elif [ "$file" = "role.cfg" ];then
                    echo "role.cfg not mv"
            elif [ "$file" = "DBAIOps.cfg" ];then
                    echo "DBAIOps.cfg not mv"
            else
                echo "$file move"
                if [ "$localnode" == "$ip" ];then
                    if [ -e $DBAIOps_oper_dir/patches/software/$file ];then
                        mv $DBAIOps_oper_dir/patches/software/$file $DBAIOps_oper_dir
                    fi
                else
                    ssh $ip "if [ -e $DBAIOps_oper_dir/patches/software/$file ];then mv $DBAIOps_oper_dir/patches/software/$file $DBAIOps_oper_dir;fi"
                fi
            fi

            if [[ "$file" =~ "bin" ]];then
                if [ "$localnode" == "$ip" ];then
                    cp -r $DBAIOps_oper_dir/patches/$dir_name/bin/logs $DBAIOps_oper_dir/bin
                else
                    if [ -d $DBAIOps_oper_dir/patches/$dir_name/bin/logs ];then
                        scp -r $DBAIOps_oper_dir/patches/$dir_name/bin/logs $ip:$DBAIOps_oper_dir/bin
                    else
                        scp -r $DBAIOps_oper_dir/bin/logs $ip:$DBAIOps_oper_dir/bin
                    fi
                fi
            fi
        done
    done
}

upgrade_reinstall(){
    for ip in $hlist
    do
        echo "upgrde $ip"
        if [ "$localnode" == "$ip" ];then
            sh $bin/DBAIOps-python3.sh -install_thirdlib upgrade
            if [ $? -eq 1 ];then
                echo "Python3 thirdlib install may not successful,please check"
                exit 1
            fi
        else
            ssh $ip "$bin/DBAIOps-python3.sh -install_thirdlib upgrade"
        fi
    done

    sh $bin/DBAIOps-zookeeper.sh -start

    sh $bin/DBAIOps-neo4j.sh -clean
    if [ $? -eq 1 ];then
        echo "neo4j install may not successful,please check"
        exit 1
    fi

    sh $bin/DBAIOps-neo4j.sh -install
    if [ $? -eq 1 ];then
        echo "neo4j install may not successful,please check"
        exit 1
    fi

    echo "Configurations,DBAIOps install Successful!"
}

upgrade()
{
    upgrade_file $DBAIOps_oper_dir/patches/software
    upgrade_reinstall
}


install_free()
{   
    source /etc/profile.d/java.sh
    source /etc/profile.d/python3.sh
    if [ "$localip" = "$pgnode" ];then
        source /etc/profile.d/pg.sh
    fi
    sh $bin/DBAIOps-python3.sh -install_rpm
    if [ $? -eq 1 ];then
        c1 "Python3 rpm 安装失败，查看/usr/software/bin/logs下日志" red
        exit 1
    fi
    c1 "系统依赖包安装成功" green
    set +e
    sh $bin/DBAIOps-openoffice.sh -install
    if [ $? -eq 1 ];then
        echo 'openoffice install failed,please re-execute the "DBAIOps-openoffice.sh -install" command after the execution of DBAIOps.sh is complete'
    fi
    set -e 

    sh $bin/DBAIOps-zookeeper.sh -install
    if [ $? -eq 1 ];then
        c1 "Zookeeper install may not successful,please check" red
        exit 1
    fi
    c1 "zookeeper组件安装成功" green
    
    sh /etc/profile.d/java.sh
    
    sh $bin/DBAIOps-zookeeper.sh -start
    if [ $? -eq 1 ];then
        c1 "Zookeeper install may not successful,please check" red
        exit 1
    fi

    sh $bin/DBAIOps-redis-single.sh -install_free
    if [ $? -eq 1 ];then
        c1 "Redis install may not successful,please check" red
        exit 1
    fi
    c1 "redis组件安装成功" green

    sh $bin/DBAIOps-fstask.sh -install
    if [ $? -eq 1 ];then
        c1 "Fstask install may not successful,please check" red
        exit 1
    fi
    c1 "fstask组件安装成功" green

    sh $bin/DBAIOps-neo4j.sh -install
    if [ $? -eq 1 ];then
        c1 "neo4j install may not successful,please check" red
        exit 1
    fi
    c1 "neo4j组件安装成功" green

    sh $bin/DBAIOps-fstask.sh -stop
    if [ $? -eq 1 ];then
        c1 "Fstask install may not successful,please check" red
        exit 1
    fi

    sh $bin/DBAIOps-zookeeper.sh -stop

    c1 "安装成功!" green

}

reinstall()
{
    source /etc/profile.d/python3.sh
    source /etc/profile.d/java.sh
    source /etc/profile.d/orainstclient.sh
    if [ "$localip" = "$pgnode" ];then
        source /etc/profile.d/pg.sh
    fi
    source /etc/profile.d/neo4j.sh
    sh $bin/DBAIOps-zookeeper.sh -clean
    if [ $? -eq 1 ];then
        echo "Zookeeper clean may not successful,please check"
        exit 1
    fi
    
    sh $bin/DBAIOps-redis-single.sh -clean
    if [ $? -eq 1 ];then
        echo "Redis clean may not successful,please check"
        exit 1
    fi

    sh $bin/DBAIOps-fstask.sh -clean
    if [ $? -eq 1 ];then
        echo "Fstask clean may not successful,please check"
        exit 1
    fi

    sh $bin/DBAIOps-zookeeper.sh -install
    if [ $? -eq 1 ];then
        echo "Zookeeper install may not successful,please check"
        exit 1
    fi

    sh $bin/DBAIOps-zookeeper.sh -start
    if [ $? -eq 1 ];then
        echo "Zookeeper install may not successful,please check"
        exit 1
    fi

    sh $bin/DBAIOps-redis-single.sh -install
    if [ $? -eq 1 ];then
        echo "Redis install may not successful,please check"
        exit 1
    fi

    sh $bin/DBAIOps-phantomjs.sh -install
    if [ $? -eq 1 ];then
        echo "Phantomjs install may not successful,please check"
        exit 1
    fi

    sh $bin/DBAIOps-fstask.sh -install
    if [ $? -eq 1 ];then
        echo "Fstask install may not successful,please check"
        exit 1
    fi

    sh $bin/DBAIOps-fstask.sh -stop
    if [ $? -eq 1 ];then
        echo "Fstask install may not successful,please check"
        exit 1
    fi

    echo "Configurations,DBAIOps reinstall Successful!"
}

start()
{
    source /etc/profile.d/python3.sh
    source /etc/profile.d/java.sh
    source /etc/profile.d/orainstclient.sh
    if [ "$localip" = "$pgnode" ];then
        source /etc/profile.d/pg.sh
    fi
    source /etc/profile.d/neo4j.sh
    sh $bin/DBAIOps-pg.sh -start ${pgnode}
    if [ $? -eq 1 ];then
	exit 1
    fi

    sh $bin/DBAIOps-zookeeper.sh -start
    if [ $? -eq 1 ];then
        exit 1
    fi
    sleep 2
    
    sh $bin/DBAIOps-redis-single.sh -start
    if [ $? -eq 1 ];then
        exit 1
    fi
    sleep 3

    sh $bin/DBAIOps-fstask.sh -start
    if [ $? -eq 1 ];then
        exit 1
    fi
    sleep 1
    echo "Waiting Webserver start..."
    sh $bin/DBAIOps-web.sh -start
    if [ $? -eq 1 ];then
        exit 1
    fi
    sleep 5
    sh $bin/DBAIOps-return.sh -start monitor
    if [ $? -eq 1 ];then
        exit 1
    fi
    sleep 5
    sh $bin/DBAIOps-return.sh -start collector
    if [ $? -eq 1 ];then
        exit 1
    fi
    sleep 1
    sh $bin/DBAIOps-return.sh -start logana
    if [ $? -eq 1 ];then
        exit 1
    fi
    sleep 1
        sh $bin/DBAIOps-return.sh -start dbconn
    if [ $? -eq 1 ];then
        exit 1
    fi
    sleep 1
    sh $bin/DBAIOps-neo4j.sh -start
    if [ $? -eq 1 ];then
        exit 1
    fi

}

stop()
{
    source /etc/profile.d/python3.sh
    source /etc/profile.d/java.sh
    source /etc/profile.d/orainstclient.sh
    if [ "$localip" = "$pgnode" ];then
        source /etc/profile.d/pg.sh
    fi
    source /etc/profile.d/neo4j.sh
    sh $bin/DBAIOps-web.sh -stop
    if [ $? -eq 1 ];then
        exit 1
    fi

    sh $bin/DBAIOps-return.sh -stop collector
    if [ $? -eq 1 ];then
        exit 1
    fi

    sh $bin/DBAIOps-return.sh -stop monitor
    if [ $? -eq 1 ];then
        exit 1
    fi

    sh $bin/DBAIOps-return.sh -stop logana
    if [ $? -eq 1 ];then
        exit 1
    fi

    sh $bin/DBAIOps-return.sh -stop dbconn
    if [ $? -eq 1 ];then
        exit 1
    fi

    sh $bin/DBAIOps-fstask.sh -stop
    if [ $? -eq 1 ];then
        exit 1
    fi

    sh $bin/DBAIOps-zookeeper.sh -stop
    if [ $? -eq 1 ];then
        exit 1
    fi

    sh $bin/DBAIOps-redis-single.sh -stop
    if [ $? -eq 1 ];then
        exit 1
    fi

    #sh $bin/DBAIOps-docker.sh -stop knowledge-tupu
    sh $bin/DBAIOps-neo4j.sh -stop
    if [ $? -eq 1 ];then
        exit 1
    fi

    sh $bin/DBAIOps-pg.sh -stop ${pgnode}
    if [ $? -eq 1 ];then
	exit 1
    fi

    echo "Configurations,DBAIOps stop Successfully!"
}

status()
{
    source /etc/profile.d/python3.sh
    source /etc/profile.d/java.sh
    source /etc/profile.d/orainstclient.sh
    if [ "$localip" = "$pgnode" ];then
        source /etc/profile.d/pg.sh
    fi
    source /etc/profile.d/neo4j.sh
    sh $bin/DBAIOps-web.sh -status
    if [ $? -eq 1 ];then
        exit 1
    fi
    echo -e "\n"
    sleep 1
    sh $bin/DBAIOps-return.sh -status collector
    if [ $? -eq 1 ];then
        exit 1
    fi
    echo -e "\n"
    sleep 1
    sh $bin/DBAIOps-return.sh -status dbconn
    if [ $? -eq 1 ];then
        exit 1
    fi
    echo -e "\n"
    sleep 1
    sh $bin/DBAIOps-return.sh -status monitor
    if [ $? -eq 1 ];then
        exit 1
    fi
    echo -e "\n"
    sleep 1
    sh $bin/DBAIOps-return.sh -status logana
    if [ $? -eq 1 ];then
        exit 1
    fi
    echo -e "\n"

    sleep 1
    sh $bin/DBAIOps-fstask.sh -status
    if [ $? -eq 1 ];then
        exit 1
    fi
    echo -e "\n"
    sleep 1
    sh $bin/DBAIOps-zookeeper.sh -status
    if [ $? -eq 1 ];then
        exit 1
    fi
    echo -e "\n"
    sleep 1
    sh $bin/DBAIOps-redis-single.sh -status

    if [ $? -eq 1 ];then
        exit 1
    fi
    echo -e "\n"
    sleep 1
    set +e
    sh $bin/DBAIOps-neo4j.sh -status
    set -e
    echo -e "\n"
    sh $bin/DBAIOps-pg.sh -status ${pgnode}
    set -e
    echo -e "\n"
    echo "Configurations,DBAIOps status Successfully!"
}

genecfg()
{
    ##generate DBAIOps.cfg
    dt=`date "+%Y-%m-%d-%H:%M:%S"`
    cp -f $CONF/DBAIOps.cfg $CONF/DBAIOps.cfg.$dt
    cp -f $CONF/DBAIOps.cfg.init $CONF/DBAIOps.cfg
    sed -i "s/DFC_DB_IP=127.0.0.1/DFC_DB_IP=$DSPG_Node/g" $CONF/DBAIOps.cfg
    sed -i "s/DFC_DB_PORT=5433/DFC_DB_PORT=$DSPG_Port/g" $CONF/DBAIOps.cfg
    sed -i "s#DFC_DB_USERNAME=RrC3zs1h/AqHKzChrjWzO7ZY7/fO3LYaanw+7WOpaOXcRXRGtwJLoLtSTOx+kPgFEumg+onirQkHv9zICNX5f2gbx5SFh6B4TNtbwpqloFOQm6Im5O1K+tplQIxtQhwPRzmJdw59GECrsvnJL2/UXdN+cn/Upf5sQVzasYmLrns=#DFC_DB_USERNAME=$DSPG_User#g" $CONF/DBAIOps.cfg
    sed -i "s#DFC_DB_PASSWORD=qXjHSTyexpjFapalErOu4ENrMmBaKt3oE8U4T60gIX4l0dUN17zMVV8oIxq5T9llNdPdOIKO7CFQt1QpgD74zqvPw2+y8pE5BnHqnyjioaZKrty+qA5IiH9tgsk7Dp07ZMYKATrzUzy3Kh1yjNBnKzFwQ7uMG6T/gOMZVIy+vcU=#DFC_DB_PASSWORD=$DSPG_Password#g" $CONF/DBAIOps.cfg
    sed -i "s/DFC_DB_DATABASE=DBAIOps_2018/DFC_DB_DATABASE=$DSPG_Database/g" $CONF/DBAIOps.cfg
    sed -i "s/DFC_FSTASK_DBNAME=fstask/DFC_FSTASK_DBNAME=$DSPG_FS_Database/g" $CONF/DBAIOps.cfg
    if [ $localnode == $DS_Fstask ];then
    DS_Fstask_ip=`hostname -i`
    else
    DS_Fstask_ip=`ssh $DS_Fstask "hostname -i"`
    fi

    if [ $localnode == $DS_Monitor ];then
    DFC_MONITOR_IP=`hostname -i`
    else
    DFC_MONITOR_IP=`ssh $DS_Monitor "hostname -i"`
    fi

    if [ $localnode == $DS_Web ];then
    DFC_WEB_IP=`hostname -i`
    else
    DFC_WEB_IP=`ssh $DS_Web "hostname -i"`
    fi
    sed -i "s/DFC_MONITOR_IP=127.0.0.1/DFC_MONITOR_IP=$DFC_MONITOR_IP/g" $CONF/DBAIOps.cfg
    sed -i "s/DFC_WEB_IP=127.0.0.1/DFC_WEB_IP=$DFC_WEB_IP/g" $CONF/DBAIOps.cfg
    sed -i "s/DFC_ADMIN_IP=127.0.0.1/DFC_ADMIN_IP=$DS_Fstask_ip/g" $CONF/DBAIOps.cfg
    sed -i "s/DFC_DB_SERVER_IP=127.0.0.1/DFC_DB_SERVER_IP=$DSPG_Node/g" $CONF/DBAIOps.cfg
    sed -i "s/DFC_DB_SERVER_PORT=22/DFC_DB_SERVER_PORT=$DSPG_Node_Port/g" $CONF/DBAIOps.cfg
    sed -i "s#DFC_DB_SERVER_USERNAME=Rr35X+vEqIghc6sBJuRkb63zsgYEO8UE/ZWufTFB969AKg3cgCGj7bj8+GK1KU8JQaGjbHhfNh6N7WQ4Ff13kO6mZjTjfrNRjbEVcrNHTyiCT/0jfwuqUNQ7XHEgRlSEuW4anSzWVrjSCu6Hzy6MuU5WHPDeRJ1xZKtnhJ3cM5Q=#DFC_DB_SERVER_USERNAME=$DSPG_Node_User#g" $CONF/DBAIOps.cfg
    sed -i "s#DFC_DB_SERVER_PASSWORD=FUslK0sm+Dpo3LDFRKhlbriz09uC/z5RH9R6vytHmo8EL70wLMem6PGHIMeWRRDB0NpJd3sWqCTOCi5yVPTg+alttpjhCfp64pzlQtLVQuheUmk+Hq28lxEbHh5E8fgCkxR4O44KmB2o9+ml3aK5MOp/Wti+95Tb0iCejY+j2pg=#DFC_DB_SERVER_PASSWORD=$DSPG_Node_Password#g" $CONF/DBAIOps.cfg
    zk=`echo $DS_Zookeeper|tr ',' '\n'`
    zkl=""
    for x in $zk
    do
        if [ $localnode == $x ];then
        xip=`hostname -i`
        zkl=$zkl$xip":12181,"
        else
        xip=`ssh $x "hostname -i"`
        zkl=$zkl$xip":12181,"
        fi
    done
    zklist=`echo $zkl|sed 's/,$//'`

    sed -i "s/DFC_ZK_CONN=127.0.0.1:2181/DFC_ZK_CONN=$zklist/g" $CONF/DBAIOps.cfg
    rediscnt=`echo $DS_Redis|tr ',' '\n'|sort -u|wc -l`
    if [ -z $redis_flag ];then
        if ((rediscnt=3));then
            r1=`echo $DS_Redis|tr ',' '\n'|head -1`
            r2=`echo $DS_Redis|tr ',' '\n'|head -2|tail -1`
            r3=`echo $DS_Redis|tr ',' '\n'|tail -1`
            r1=`ssh $r1 "hostname -i"`
            r2=`ssh $r2 "hostname -i"`
            r3=`ssh $r3 "hostname -i"`
            sed -i "s@DFC_REDIS_SENTINEL1=\"redis://127.0.0.1:26379\"@DFC_REDIS_SENTINEL1=\"redis://$r1:26379\"@g" $CONF/DBAIOps.cfg
            sed -i "s@DFC_REDIS_SENTINEL2=\"redis://127.0.0.1:26380\"@DFC_REDIS_SENTINEL2=\"redis://$r2:26380\"@g" $CONF/DBAIOps.cfg
            sed -i "s@DFC_REDIS_SENTINEL3=\"redis://127.0.0.1:26381\"@DFC_REDIS_SENTINEL3=\"redis://$r3:26381\"@g" $CONF/DBAIOps.cfg
        elif ((rediscnt=1));then
            rr=`echo $DS_Redis|tr ',' '\n'|sort -u|head -1`
            if [ $localnode == $rr ];then
            rr=`hostname -i`
            else
            rr=`ssh $rr "hostname -i"`
            fi
            sed -i "s@DFC_REDIS_SENTINEL1=\"redis://127.0.0.1:26379\"@DFC_REDIS_SENTINEL1=\"redis://$rr:26379\"@g" $CONF/DBAIOps.cfg
            sed -i "s@DFC_REDIS_SENTINEL2=\"redis://127.0.0.1:26380\"@DFC_REDIS_SENTINEL2=\"redis://$rr:26380\"@g" $CONF/DBAIOps.cfg
            sed -i "s@DFC_REDIS_SENTINEL3=\"redis://127.0.0.1:26381\"@DFC_REDIS_SENTINEL3=\"redis://$rr:26381\"@g" $CONF/DBAIOps.cfg
        else
            echo "Redis can only be 1 or 3 nodes!"
            exit 1
        fi
    else
        rr=`echo $DS_Redis|tr ',' '\n'|sort -u|head -1`
        if [ $localnode == $rr ];then
        rr=`hostname -i`
        else
        rr=`ssh $rr "hostname -i"`
        fi
        sed -i "s@DFC_REDIS_SINGLENODE=\"redis://127.0.0.1:16379\"@DFC_REDIS_SINGLENODE=\"redis://$rr:16379\"@g" $CONF/DBAIOps.cfg
    fi
}

genecfg_single()
{   DBAIOps_ips=`hostname -i|awk '{print $1}'`
    mv  $CONF/DBAIOps.cfg $CONF/DBAIOps.cfg.bak
    echo "DFC_JAVA_HOME=/usr/software/jdk1.8.0_331" >> $CONF/DBAIOps.cfg
    #database
    echo "DFC_DB_TYPE=postgres" >> $CONF/DBAIOps.cfg
    echo "DFC_DB_IP=$DBAIOps_ips" >> $CONF/DBAIOps.cfg
    echo "DFC_DB_PORT=15433" >> $CONF/DBAIOps.cfg
    echo "DFC_DB_USERNAME=RrC3zs1h/AqHKzChrjWzO7ZY7/fO3LYaanw+7WOpaOXcRXRGtwJLoLtSTOx+kPgFEumg+onirQkHv9zICNX5f2gbx5SFh6B4TNtbwpqloFOQm6Im5O1K+tplQIxtQhwPRzmJdw59GECrsvnJL2/UXdN+cn/Upf5sQVzasYmLrns=" >> $CONF/DBAIOps.cfg
    echo "DFC_DB_PASSWORD=qXjHSTyexpjFapalErOu4ENrMmBaKt3oE8U4T60gIX4l0dUN17zMVV8oIxq5T9llNdPdOIKO7CFQt1QpgD74zqvPw2+y8pE5BnHqnyjioaZKrty+qA5IiH9tgsk7Dp07ZMYKATrzUzy3Kh1yjNBnKzFwQ7uMG6T/gOMZVIy+vcU=" >> $CONF/DBAIOps.cfg
    echo "DFC_DB_DATABASE=DBAIOps_2022" >> $CONF/DBAIOps.cfg
    echo "DFC_DB_SERVER_IP=$DBAIOps_ips" >> $CONF/DBAIOps.cfg
    echo "DFC_DB_SERVER_PORT=" >> $CONF/DBAIOps.cfg
    echo "DFC_DB_SERVER_USERNAME=" >> $CONF/DBAIOps.cfg
    echo "DFC_DB_SERVER_PASSWORD=" >> $CONF/DBAIOps.cfg
    echo "DFC_ZK_CONN=$DBAIOps_ips:12181" >> $CONF/DBAIOps.cfg

    echo "DFC_MANAGER_IP=127.0.0.1" >> $CONF/DBAIOps.cfg
    echo "DFC_MANAGER_UID=110300126" >> $CONF/DBAIOps.cfg
    echo "DFC_NODE_UID=110300126" >> $CONF/DBAIOps.cfg
    echo "DFC_FSTASK_DBNAME=fstask" >> $CONF/DBAIOps.cfg
    echo "DFC_ADMIN_IP=$DBAIOps_ips" >> $CONF/DBAIOps.cfg
    echo "DFC_ADMIN_PORT=18090" >> $CONF/DBAIOps.cfg
    echo "DFC_EXECUTOR_PORT=19090" >> $CONF/DBAIOps.cfg
    echo "DFC_FSTASK_DB_USERNAME=hY8ey-pqLVaP73dOxAOkZlGlbT143n91vykMVW6f_hcNPo4pnvDv62JQA5rhHvQv6iS2pOfS432TeX5AeP-Hbg" >> $CONF/DBAIOps.cfg
    echo "DFC_FSTASK_DB_PASSWORD=NbQKzfLd2Cbsx3pAj4x-nW2yXRvzmyEdBHwVMIXcP9z7XE_jIH-XIFxZxpRp1Vby3rWRrWl5Rx0hk_jsmMDCQg" >> $CONF/DBAIOps.cfg
    echo "DFC_ML_SWITCH=off" >> $CONF/DBAIOps.cfg
    #REDIS
    echo "DFC_REDIS_SINGLENODE=\"redis://$DBAIOps_ips:16379\"" >> $CONF/DBAIOps.cfg

    #Monitor
    echo "DFC_MONITOR_IP=$DBAIOps_ips" >> $CONF/DBAIOps.cfg

    #WEB
    echo "DFC_WEB_IP=$DBAIOps_ips" >> $CONF/DBAIOps.cfg
}


modifyWebCfg(){
    monnode=`awk -F '=' '/^DS_Monitor/{print $2}' $CONF/role.cfg| tr -s '\n' | tr ',' '\n' |sort -u `
    if [ "$localnode" == "$monnode" ];then
        monitorip=`hostname -i|awk '{print $1}'`
    else
        monitorip=`ssh $monnode "hostname -i|awk '{print $1}'"`
    fi
    sed -i "s/60.60.60.72/$monitorip/g" /usr/software/webserver/conf/skin.json
}

do_insert()
{
    webnode=`awk -F '=' '/^DS_Web/{print $2}' $CONF/role.cfg| tr -s '\n' | tr ',' '\n' |sort -u `
    colnode=`awk -F '=' '/^DS_Collector/{print $2}' $CONF/role.cfg| tr -s '\n' | tr ',' '\n' |sort -u `
    monnode=`awk -F '=' '/^DS_Monitor/{print $2}' $CONF/role.cfg| tr -s '\n' | tr ',' '\n' |sort -u `
    lognode=`awk -F '=' '/^DS_Logana/{print $2}' $CONF/role.cfg| tr -s '\n' | tr ',' '\n' |sort -u `
    fstnode=`awk -F '=' '/^DS_Fstask/{print $2}' $CONF/role.cfg| tr -s '\n' | tr ',' '\n' |sort -u `
    fstnode_extra_executor=`awk -F '=' '/^DS_Other_Executor/{print $2}' $CONF/role.cfg| tr -s '\n' | tr ',' '\n' |sort -u `
    zknode=`awk -F '=' '/^DS_Zookeeper/{print $2}' $CONF/role.cfg| tr -s '\n' | tr ',' '\n' |sort -u `
    rdnode=`awk -F '=' '/^DS_Redis/{print $2}' $CONF/role.cfg| tr -s '\n' | tr ',' '\n' |sort -u `
    if [ -f /tmp/init_mcs.sql ];then
        cat /dev/null > /tmp/init_mcs.sql
        echo "delete from mon_comp_status;" >> /tmp/init_mcs.sql
    fi
    topnode_total=`awk -F '=' '/^DS_Collector/{print $2}' $CONF/role.cfg`','`awk -F '=' '/^DS_Fstask/{print $2}' $CONF/role.cfg`','`awk -F '=' '/^DS_Other_Executor/{print $2}' $CONF/role.cfg`
    topnode=`echo $topnode_total|tr -s '\n' | tr ',' '\n'|sort -u `
    iplist=''
    for x in $topnode
    do
        if [ $localnode == $x ];then
            xip=`hostname -i|awk '{print $1}'`
        else
            xip=`ssh $x "hostname -i|awk '{print $1}'"`
        fi
        iplist=$xip';'$iplist
    done
    iplist=`echo $iplist| sed 's/.$//'`
    echo "$iplist" > /tmp/init_domain.txt
    num=1
    for x in $colnode
    do
        if [ $localnode == $x ];then
        xip=`hostname -i|awk '{print $1}'`
        else
        xip=`ssh $x "hostname -i|awk '{print $1}'"`
        fi
        echo "insert into mon_comp_status(id,comp_name,node_ip,node_ip_addr,status,stats_dt) values($num,'Collector$num','$x','$xip','0',now());" >> /tmp/init_mcs.sql
        num=`expr $num + 1`
    done
    for x in $monnode
    do
        if [ $localnode == $x ];then
        xip=`hostname -i|awk '{print $1}'`
        else
        xip=`ssh $x "hostname -i|awk '{print $1}'"`
        fi
        echo "insert into mon_comp_status(id,comp_name,node_ip,node_ip_addr,status,stats_dt) values($num,'Monitor','$x','$xip','0',now());" >> /tmp/init_mcs.sql
        num=`expr $num + 1`
    done
    for x in $lognode
    do
        if [ $localnode == $x ];then
        xip=`hostname -i|awk '{print $1}'`
        else
        xip=`ssh $x "hostname -i|awk '{print $1}'"`
        fi
        echo "insert into mon_comp_status(id,comp_name,node_ip,node_ip_addr,status,stats_dt) values($num,'LogAna','$x','$xip','0',now());" >> /tmp/init_mcs.sql
        num=`expr $num + 1`
    done
    for x in $fstnode
    do
        if [ $localnode == $x ];then
        xip=`hostname -i|awk '{print $1}'`
        else
        xip=`ssh $x "hostname -i|awk '{print $1}'"`
        fi
        echo "insert into mon_comp_status(id,comp_name,node_ip,node_ip_addr,status,stats_dt) values($num,'Fstask','$x','$xip','0',now());" >> /tmp/init_mcs.sql
        num=`expr $num + 1`
    done
    for x in $fstnode_extra_executor
    do
        if [ $localnode == $x ];then
        xip=`hostname -i|awk '{print $1}'`
        else
        xip=`ssh $x "hostname -i|awk '{print $1}'"`
        fi
        echo "insert into mon_comp_status(id,comp_name,node_ip,node_ip_addr,status,stats_dt) values($num,'Fstask','$x','$xip','0',now());" >> /tmp/init_mcs.sql
        num=`expr $num + 1`
    done
    num_zk=1
    for x in $zknode
    do
        if [ $localnode == $x ];then
        xip=`hostname -i|awk '{print $1}'`
        else
        xip=`ssh $x "hostname -i|awk '{print $1}'"`
        fi
        echo "insert into mon_comp_status(id,comp_name,node_ip,node_ip_addr,status,stats_dt) values($num,'Zookeeper$num_zk','$x','$xip','0',now());" >> /tmp/init_mcs.sql
        num=`expr $num + 1`
        num_zk=`expr $num_zk + 1`
    done
    num_rd=1
    for x in $rdnode
    do
        if [ $localnode == $x ];then
        xip=`hostname -i|awk '{print $1}'`
        else
        xip=`ssh $x "hostname -i|awk '{print $1}'"`
        fi
        echo "insert into mon_comp_status(id,comp_name,node_ip,node_ip_addr,status,stats_dt) values($num,'Redis$num_rd','$x','$xip','0',now());" >> /tmp/init_mcs.sql
        num=`expr $num + 1`
        num_rd=`expr $num_rd + 1`
    done
    for x in $webnode
    do
        if [ $localnode == $x ];then
        xip=`hostname -i|awk '{print $1}'`
        else
        xip=`ssh $x "hostname -i|awk '{print $1}'"`
        fi
        echo "insert into mon_comp_status(id,comp_name,node_ip,node_ip_addr,status,stats_dt) values($num,'Web','$x','$xip','0',now());" >> /tmp/init_mcs.sql
        num=`expr $num + 1`
    done
    unset num
    unset num_zk
    unset num_rd
}

config_hosts() {
    # 多语言提示信息
    if [ "$LANGUAGE" == "cn" ]; then
        local msg_localhost="当前主机名为 localhost，程序将修改主机名为 dbmonitor"
        local msg_hosts_entry="当前 /etc/hosts 文件存在 127.0.0.1 $(hostname) 条目，程序将注释该行"
        local msg_hosts_backup="hosts 文件已备份：/etc/hosts.bak"
        local msg_no_ip="未找到有效的 IP 地址，退出安装。"
        local msg_select_ip="请选择一个 IP："
        local msg_invalid_choice="无效选择，请重新选择。"
        local msg_ip_exists="/etc/hosts 已存在该 IP 条目，跳过配置。"
        local msg_hosts_configured="已配置 /etc/hosts。"
        local msg_multiple_ips="当前主机存在多个 IP："
        local msg_verify_success="验证成功：hostname -i 返回的 IP 与配置的 IP 一致。"
        local msg_verify_failed="验证失败：hostname -i 返回的 IP 与配置的 IP 不一致。"
    else
        local msg_localhost="Current hostname is localhost, changing it to dbmonitor"
        local msg_hosts_entry="Found 127.0.0.1 $(hostname) entry in /etc/hosts, commenting it out"
        local msg_hosts_backup="Hosts file backed up: /etc/hosts.bak"
        local msg_no_ip="No valid IP address found, exiting installation."
        local msg_select_ip="Please select an IP:"
        local msg_invalid_choice="Invalid choice, please try again."
        local msg_ip_exists="IP entry already exists in /etc/hosts, skipping configuration."
        local msg_hosts_configured="/etc/hosts configured successfully."
        local msg_multiple_ips="Current host has multiple IPs:"
        local msg_verify_success="Verification successful: hostname -i returns the configured IP."
        local msg_verify_failed="Verification failed: hostname -i does not return the configured IP."
    fi

    # 检查主机名是否是 localhost，如果是则修改主机名为 dbmonitor
    if [ "$(hostname)" == "localhost" ]; then
        c1 "$msg_localhost" red
        hostname dbmonitor
        echo "dbmonitor" > /etc/hostname
    fi

    # 判断 /etc/hosts 文件中是否存在 127.0.0.1 主机名，如果有则提示并注释
    if grep -q "^127.0.0.1\s\+$(hostname)\s*$" /etc/hosts; then
        c1 "$msg_hosts_entry" red
        sed -i "/^127.0.0.1\s\+$(hostname)\s*$/s/^/#/" /etc/hosts
    fi

    # 备份 /etc/hosts
    if [ -f /etc/hosts.bak ]; then
        c1 "$msg_hosts_backup" blue
    else
        cp -f /etc/hosts /etc/hosts.bak
    fi

    # 获取多个 IP 地址（排除虚拟网卡）
    ip_list=$(ip -o -4 addr show | awk '{print $4}' | grep -vE '127.0.0.1|docker|virbr|veth' | cut -d/ -f1)

    # 将获取到的 IP 地址转换成数组
    IFS=$'\n' read -r -d '' -a ipv4_array <<<"$ip_list"

    # 判断 IP 数量
    if [ ${#ipv4_array[@]} -eq 0 ]; then
        c1 "$msg_no_ip" red
        exit 1
    elif [ ${#ipv4_array[@]} -eq 1 ]; then
        # 如果只有一个 IP，直接配置到 /etc/hosts
        selected_ip=${ipv4_array[0]}
        if grep -q "$selected_ip" /etc/hosts; then
            c1 "$msg_ip_exists" green
        else
            echo "$selected_ip $(hostname)" | tee -a /etc/hosts > /dev/null
            c1 "$msg_hosts_configured" green
        fi
    else
        # 如果有多个 IP，让用户选择一个并配置到 /etc/hosts
        c1 "$msg_multiple_ips" blue
        for i in "${!ipv4_array[@]}"; do
            echo "$((i+1)). ${ipv4_array[i]}"
        done

        # 提示用户选择一个 IP
        while true; do
            read -p "$msg_select_ip " choice
            if [[ $choice =~ ^[0-9]+$ ]] && [ $choice -ge 1 ] && [ $choice -le ${#ipv4_array[@]} ]; then
                selected_ip=${ipv4_array[$((choice-1))]}
                break
            else
                c1 "$msg_invalid_choice" red
            fi
        done

        # 检查选择的 IP 是否已存在并添加
        if grep -q "$selected_ip" /etc/hosts; then
            c1 "$msg_ip_exists" green
        else
            echo "$selected_ip $(hostname)" | tee -a /etc/hosts > /dev/null
            c1 "$msg_hosts_configured" green
        fi
    fi

    # 验证配置是否正确
    configured_ip=$(hostname -i)
    if [ "$configured_ip" == "$selected_ip" ]; then
        c1 "$msg_verify_success" green
    else
        c1 "$msg_verify_failed" red
        exit 1
    fi
}

setup_selinux() {
    # 多语言提示信息
    if [ "$LANGUAGE" == "cn" ]; then
        local msg_check_selinux="检查 $ip 上的 SELinux 状态..."
        local msg_selinux_enabled="$ip 上的 SELinux 当前已启用。"
        local msg_disable_selinux="正在禁用 $ip 上的 SELinux..."
        local msg_selinux_disabled="$ip 上的 SELinux 已禁用完成。"
        local msg_selinux_not_enabled="$ip 上的 SELinux 未启用，无需禁用。"
        local msg_local_selinux_enabled="本地节点的 SELinux 当前已启用。"
        local msg_local_disable_selinux="正在禁用本地节点上的 SELinux..."
        local msg_local_selinux_disabled="本地节点上的 SELinux 已禁用完成。"
        local msg_local_selinux_not_enabled="本地节点上的 SELinux 未启用，无需禁用。"
        local msg_selinux_disable_complete="SELinux 禁用完成。"
    else
        local msg_check_selinux="Checking SELinux status on $ip..."
        local msg_selinux_enabled="SELinux is currently enabled on $ip."
        local msg_disable_selinux="Disabling SELinux on $ip..."
        local msg_selinux_disabled="SELinux has been disabled on $ip."
        local msg_selinux_not_enabled="SELinux is not enabled on $ip, no need to disable."
        local msg_local_selinux_enabled="SELinux is currently enabled on local node."
        local msg_local_disable_selinux="Disabling SELinux on local node..."
        local msg_local_selinux_disabled="SELinux has been disabled on local node."
        local msg_local_selinux_not_enabled="SELinux is not enabled on local node, no need to disable."
        local msg_selinux_disable_complete="SELinux disable completed."
    fi

    for ip in $hlist; do
        if [ "$localnode" != "$ip" ]; then
            # 检查远程节点的 SELinux 状态
            c1 "$msg_check_selinux" blue
            selinux_status=$(ssh $ip "sestatus | grep 'SELinux status' | awk '{print \$3}'")

            if [ "$selinux_status" == "enabled" ]; then
                c1 "$msg_selinux_enabled" red
                c1 "$msg_disable_selinux" blue
                ssh $ip "setenforce 0 && sed -i 's/^SELINUX=.*/SELINUX=disabled/' /etc/selinux/config"
                c1 "$msg_selinux_disabled" green
            else
                c1 "$msg_selinux_not_enabled" green
            fi
        else
            # 检查本地节点的 SELinux 状态
            selinux_status=$(sestatus | grep 'SELinux status' | awk '{print $3}')

            if [ "$selinux_status" == "enabled" ]; then
                c1 "$msg_local_selinux_enabled" red
                c1 "$msg_local_disable_selinux" blue
                setenforce 0
                sed -i 's/^SELINUX=.*/SELINUX=disabled/' /etc/selinux/config
                c1 "$msg_local_selinux_disabled" green
            else
                c1 "$msg_local_selinux_not_enabled" green
            fi
        fi
    done

    c1 "$msg_selinux_disable_complete" green
}

setup_firewall() {
    # 多语言提示信息
    if [ "$LANGUAGE" == "cn" ]; then
        local msg_check_firewall="检查 $ip 上的防火墙状态..."
        local msg_firewall_enabled="$ip 上的防火墙当前已启用。"
        local msg_disable_firewall="正在禁用 $ip 上的防火墙..."
        local msg_firewall_disabled="$ip 上的防火墙已禁用。"
        local msg_firewall_not_enabled="$ip 上的防火墙未启用。"
        local msg_local_firewall_enabled="本地节点上的防火墙当前已启用。"
        local msg_local_disable_firewall="正在禁用本地节点上的防火墙..."
        local msg_local_firewall_disabled="本地节点上的防火墙已禁用。"
        local msg_local_firewall_not_enabled="本地节点上的防火墙未启用。"
        local msg_firewall_disable_complete="防火墙设置完成。"
    else
        local msg_check_firewall="Checking firewall status on $ip..."
        local msg_firewall_enabled="Firewall is currently enabled on $ip."
        local msg_disable_firewall="Disabling firewall on $ip..."
        local msg_firewall_disabled="Firewall has been disabled on $ip."
        local msg_firewall_not_enabled="Firewall is not enabled on $ip."
        local msg_local_firewall_enabled="Firewall is currently enabled on local node."
        local msg_local_disable_firewall="Disabling firewall on local node..."
        local msg_local_firewall_disabled="Firewall has been disabled on local node."
        local msg_local_firewall_not_enabled="Firewall is not enabled on local node."
        local msg_firewall_disable_complete="Firewall setup completed."
    fi

    for ip in $hlist; do
        if [ "$localnode" != "$ip" ]; then
            # 检查远程节点的防火墙状态
            c1 "$msg_check_firewall" blue
            firewall_status=$(ssh $ip "systemctl is-active firewalld")

            if [ "$firewall_status" == "active" ]; then
                c1 "$msg_firewall_enabled" red
                c1 "$msg_disable_firewall" blue
                ssh $ip "systemctl stop firewalld && systemctl disable firewalld"
                c1 "$msg_firewall_disabled" green
            else
                c1 "$msg_firewall_not_enabled" green
            fi
        else
            # 检查本地节点的防火墙状态
            c1 "$msg_check_firewall" blue
            firewall_status=$(systemctl is-active firewalld)

            if [ "$firewall_status" == "active" ]; then
                c1 "$msg_local_firewall_enabled" red
                c1 "$msg_local_disable_firewall" blue
                systemctl stop firewalld
                systemctl disable firewalld
                c1 "$msg_local_firewall_disabled" green
            else
                c1 "$msg_local_firewall_not_enabled" green
            fi
        fi
    done

    c1 "$msg_firewall_disable_complete" green
}


check_set_timezone() {
    # 多语言提示信息
    if [ "$LANGUAGE" == "cn" ]; then
        local msg_local_timezone="检查本地节点时区 ($local_timezone)..."
        local msg_remote_timezone="检查远程节点时区 ($remote_timezone)..."
        local msg_not_target_timezone="当前时区不是北京时区 (Asia/Shanghai)。"
        local msg_confirm_continue="是否继续安装？(Y/N): "
        local msg_timezone_already_set="时区已设置为 Asia/Shanghai。"
        local msg_remote_connection_failed="无法连接到远程节点。"
    else
        local msg_local_timezone="Checking local node timezone ($local_timezone)..."
        local msg_remote_timezone="Checking remote node timezone ($remote_timezone)..."
        local msg_not_target_timezone="Current timezone is not Asia/Shanghai."
        local msg_confirm_continue="Do you want to continue installation? (Y/N): "
        local msg_timezone_already_set="Timezone is already set to Asia/Shanghai."
        local msg_remote_connection_failed="Failed to connect to remote node."
    fi

    target_timezone="Asia/Shanghai"

    for ip in $hlist; do
        if [ "$localnode" == "$ip" ]; then
            # 检查本地节点时区
            local_timezone=$(timedatectl | grep "Time zone" | awk '{print $3}')
            c1 "$msg_local_timezone" blue

            if [ "$local_timezone" != "$target_timezone" ]; then
                c1 "$msg_not_target_timezone" red
                read -p "$msg_confirm_continue" confirm
                if [[ "$confirm" != "Y" && "$confirm" != "y" ]]; then
                    c1 "安装已取消。" red
                    exit 1
                fi
            else
                c1 "$msg_timezone_already_set" green
            fi
        else
            # 检查远程节点时区
            remote_timezone=$(ssh $ip "timedatectl | grep 'Time zone' | awk '{print \$3}'" 2>/dev/null)
            if [ -n "$remote_timezone" ]; then
                c1 "$msg_remote_timezone" blue

                if [ "$remote_timezone" != "$target_timezone" ]; then
                    c1 "$msg_not_target_timezone" red
                    read -p "$msg_confirm_continue" confirm
                    if [[ "$confirm" != "Y" && "$confirm" != "y" ]]; then
                        c1 "安装已取消。" red
                        exit 1
                    fi
                else
                    c1 "$msg_timezone_already_set" green
                fi
            else
                c1 "$msg_remote_connection_failed" red
            fi
        fi
    done
}


setup_characterset(){
    echo "export LANG=en_US.UTF-8" > /etc/profile.d/lang.sh
    source /etc/profile.d/lang.sh
}

config_role(){
    cp $CONF/role.cfg $CONF/role.cfg.bak
    echo "" > $CONF/role.cfg
    echo "DS_Web=$DBAIOps_hostname" > $CONF/role.cfg
    echo "DS_Collector=$DBAIOps_hostname" >> $CONF/role.cfg
    echo "DS_Monitor=$DBAIOps_hostname" >> $CONF/role.cfg
    echo "DS_Logana=$DBAIOps_hostname" >> $CONF/role.cfg
    echo "DS_Fstask=$DBAIOps_hostname" >> $CONF/role.cfg
    echo "DS_Other_Executor=" >> $CONF/role.cfg
    echo "DS_Zookeeper=$DBAIOps_hostname" >> $CONF/role.cfg
    echo "DS_Redis=$DBAIOps_hostname" >> $CONF/role.cfg
    echo "DS_BASE_LOCALTION=/usr/software" >> $CONF/role.cfg
    echo "DSPG_Node=$selected_ip" >> $CONF/role.cfg
    echo "DSPG_BASE=/usr/software/pgsql" >> $CONF/role.cfg
    echo "DSPG_DATA_LOCALTION=/usr/software/pgsql/data" >> $CONF/role.cfg
    echo "DSPG_Port=15433" >> $CONF/role.cfg
    echo "DSPG_Database=DBAIOps_2022" >> $CONF/role.cfg
    echo "DSPG_FS_Database=fstask" >> $CONF/role.cfg
    echo "DSPG_OS_USER=postgres" >> $CONF/role.cfg
    echo "DSPG_User=RrC3zs1h/AqHKzChrjWzO7ZY7/fO3LYaanw+7WOpaOXcRXRGtwJLoLtSTOx+kPgFEumg+onirQkHv9zICNX5f2gbx5SFh6B4TNtbwpqloFOQm6Im5O1K+tplQIxtQhwPRzmJdw59GECrsvnJL2/UXdN+cn/Upf5sQVzasYmLrns=" >> $CONF/role.cfg
    echo "DSPG_Password=qXjHSTyexpjFapalErOu4ENrMmBaKt3oE8U4T60gIX4l0dUN17zMVV8oIxq5T9llNdPdOIKO7CFQt1QpgD74zqvPw2+y8pE5BnHqnyjioaZKrty+qA5IiH9tgsk7Dp07ZMYKATrzUzy3Kh1yjNBnKzFwQ7uMG6T/gOMZVIy+vcU=" >> $CONF/role.cfg
}

config_yum() {
    # 多语言提示信息
    if [ "$LANGUAGE" == "cn" ]; then
        local msg_yum_configured="YUM 源已配置。"
        local msg_yum_check_failed="YUM 源配置检查失败，请手动配置 YUM 源。"
        local msg_yum_check_success="YUM 源配置检查通过。"
    else
        local msg_yum_configured="YUM repository is configured."
        local msg_yum_check_failed="YUM repository configuration check failed, please configure it manually."
        local msg_yum_check_success="YUM repository configuration check passed."
    fi

    # 检查 YUM 源是否可用
    if yum repolist > /dev/null 2>&1; then
        c1 "$msg_yum_configured" green
        c1 "$msg_yum_check_success" green
    else
        c1 "$msg_yum_check_failed" red
        exit 1
    fi
}

do_pg_insert(){
    . $CONF/role.cfg
    pgip=$DSPG_Node
    pgdbname=$DSPG_Database
    pgusername=$DSPG_User
    pgpasswd=$DSPG_Password
    pgport=$DSPG_Port
    sysarg="{\"pg_ip\": \"$pgip\", \"pg_dbname\": \"$pgdbname\", \"pg_usr\": \"$pgusername\", \"pg_pwd\": \"$pgpasswd\", \"pg_port\": \"$pgport\"}"
    if [ -f /etc/profile.d/python3.sh ];then
        source /etc/profile.d/python3.sh
    fi
    if [ -f /etc/profile.d/java.sh ];then
        source /etc/profile.d/java.sh
    fi
    if [ -f /etc/profile.d/pg.sh ];then
        source /etc/profile.d/pg.sh
    fi
    python3 $DBAIOps_HOME/bin/DBAIOps_initmcs.py "$sysarg"
}


do_crontab() {
    # 多语言提示信息
    if [ "$LANGUAGE" == "cn" ]; then
        local msg_cron_exists="DBAIOpsSelfCheckCron 定时任务已存在。"
        local msg_add_cron="添加 DBAIOpsSelfCheckCron 定时任务成功。"
    else
        local msg_cron_exists="DBAIOpsSelfCheckCron cron job already exists."
        local msg_add_cron="DBAIOpsSelfCheckCron cron job added successfully."
    fi

    # 检查定时任务是否已存在
    if grep -q "DBAIOps_restart.log" /var/spool/cron/root; then
        c1 "$msg_cron_exists" green
    else
        # 确保 crontab 文件存在
        if [ ! -f /var/spool/cron/root ]; then
            touch /var/spool/cron/root
        fi

        # 添加定时任务
        echo "0 12 * * 3 python3 /usr/software/knowl/DBAIOpsSelfCheckCron.py > /tmp/DBAIOps_restart.log" >> /var/spool/cron/root
        c1 "$msg_add_cron" green
    fi
}

pgfincore(){
    echo "python3 /usr/software/knowl/pg_load_tab_into_cache.py > /tmp/pgfincore.log 2>&1" > /usr/software/bin/pgfincore.sh
    echo "*/10  * * * * /usr/bin/sh /usr/software/bin/pgfincore.sh" >> /var/spool/cron/root
}


clslog() {
    # 多语言提示信息
    if [ "$LANGUAGE" == "cn" ]; then
        local msg_clean_start="开始清理 $ip 上的日志文件..."
        local msg_clean_return="清理 return 日志文件..."
        local msg_clean_fstask="清理 fstask 日志文件..."
        local msg_clean_web="清理 web 日志文件..."
        local msg_clean_success="日志清理完成。"
        local msg_clean_failed="日志清理失败。"
    else
        local msg_clean_start="Starting to clean log files on $ip..."
        local msg_clean_return="Cleaning return log files..."
        local msg_clean_fstask="Cleaning fstask log files..."
        local msg_clean_web="Cleaning web log files..."
        local msg_clean_success="Log cleaning completed."
        local msg_clean_failed="Log cleaning failed."
    fi

    # 清理日志文件的函数
    clean_logs() {
        local log_dir=$1
        local log_type=$2
        if [ -d "$log_dir" ]; then
            find "$log_dir" -type f -mtime +3 -exec rm -rf {} \;
            if [ $? -eq 0 ]; then
                c1 "$log_type 日志清理成功。" green
            else
                c1 "$log_type 日志清理失败。" red
            fi
        else
            c1 "$log_type 日志目录不存在，跳过清理。" yellow
        fi
    }

    for ip in $hlist; do
        c1 "$msg_clean_start" blue

        # 清理 return 日志文件
        c1 "$msg_clean_return" blue
        ssh $ip "$(typeset -f clean_logs); clean_logs /usr/software/return/logs 'return'"

        # 清理 fstask 日志文件
        c1 "$msg_clean_fstask" blue
        ssh $ip "$(typeset -f clean_logs); clean_logs /usr/software/fstaskpkg/lib/tomcat-apache-fstask/logs 'fstask'"

        # 清理 web 日志文件
        c1 "$msg_clean_web" blue
        ssh $ip "$(typeset -f clean_logs); clean_logs /usr/software/webserver/lib/apache-tomcat-9.0.86/logs 'web'"

        c1 "$msg_clean_success" green
    done
}
config_DBAIOps() {
    # 多语言提示信息
    if [ "$LANGUAGE" == "cn" ]; then
        local msg_setup_charset="修改字符集..."
        local msg_setup_charset_success="字符集修改成功。"
        local msg_setup_selinux="禁用 SELinux..."
        local msg_setup_selinux_success="SELinux 禁用成功。"
        local msg_setup_firewall="禁用防火墙..."
        local msg_setup_firewall_success="防火墙禁用成功。"
        local msg_check_timezone="检查时区设置..."
        local msg_config_hosts="配置 /etc/hosts..."
        local msg_config_hosts_success="/etc/hosts 配置成功。"
        local msg_config_role="配置 role.cfg..."
        local msg_config_role_success="role.cfg 配置成功。"
        local msg_config_yum="检查 YUM 源..."
        local msg_config_yum_success="YUM 源检查成功。"
        local msg_config_complete="KYSD 配置完成。"
    else
        local msg_setup_charset="Setting up character set..."
        local msg_setup_charset_success="Character set setup completed."
        local msg_setup_selinux="Disabling SELinux..."
        local msg_setup_selinux_success="SELinux disabled successfully."
        local msg_setup_firewall="Disabling firewall..."
        local msg_setup_firewall_success="Firewall disabled successfully."
        local msg_check_timezone="Checking timezone settings..."
        local msg_config_hosts="Configuring /etc/hosts..."
        local msg_config_hosts_success="/etc/hosts configured successfully."
        local msg_config_role="Configuring role.cfg..."
        local msg_config_role_success="role.cfg configured successfully."
        local msg_config_yum="Checking YUM repository..."
        local msg_config_yum_success="YUM repository check completed."
        local msg_config_complete="KYSD configuration completed."
    fi

    # 修改字符集
    c1 "$msg_setup_charset" blue
    setup_characterset
    if [ $? -eq 0 ]; then
        c1 "$msg_setup_charset_success" green
    else
        c1 "字符集修改失败。" red
        exit 1
    fi
    echo -e "\n"

    # 禁用 SELinux
    c1 "$msg_setup_selinux" blue
    setup_selinux
    if [ $? -eq 0 ]; then
        c1 "$msg_setup_selinux_success" green
    else
        c1 "SELinux 禁用失败。" red
        exit 1
    fi
    echo -e "\n"

    # 禁用防火墙
    c1 "$msg_setup_firewall" blue
    setup_firewall
    if [ $? -eq 0 ]; then
        c1 "$msg_setup_firewall_success" green
    else
        c1 "防火墙禁用失败。" red
        exit 1
    fi
    echo -e "\n"

    # 检查时区设置
    c1 "$msg_check_timezone" blue
    check_set_timezone
    echo -e "\n"

    # 配置 /etc/hosts
    c1 "$msg_config_hosts" blue
    config_hosts
    if [ $? -eq 0 ]; then
        c1 "$msg_config_hosts_success" green
    else
        c1 "/etc/hosts 配置失败。" red
        exit 1
    fi
    echo -e "\n"

    # 配置 role.cfg
    c1 "$msg_config_role" blue
    config_role
    if [ $? -eq 0 ]; then
        c1 "$msg_config_role_success" green
    else
        c1 "role.cfg 配置失败。" red
        exit 1
    fi
    echo -e "\n"

    # 检查 YUM 源
    c1 "$msg_config_yum" blue
    config_yum
    if [ $? -eq 0 ]; then
        c1 "$msg_config_yum_success" green
    else
        c1 "YUM 源检查失败。" red
        exit 1
    fi
    echo -e "\n"

    # 记录配置完成
    echo "config DBAIOps success" > /usr/software/bin/logs/DBAIOps_config.txt
    c1 "$msg_config_complete" green
}


check_root() {
    # 多语言提示信息
    if [ "$LANGUAGE" == "cn" ]; then
        local msg_not_root="当前用户不是 root 用户，请以 root 用户运行此脚本。"
    else
        local msg_not_root="This script must be run as root. Please switch to root user."
    fi

    # 检查当前用户是否是 root
    if [ "$(id -u)" -ne 0 ]; then
        c1 "$msg_not_root" red
        log "ERROR" "$msg_not_root"
        exit 1
    fi
}

check_root

DBAIOps_hostname=`hostname`
check_dir() {
    # 多语言提示信息
    if [ "$LANGUAGE" == "cn" ]; then
        local msg_wrong_dir="当前目录 ($current_dir) 不是安装目录，程序将自动创建软连接到 /usr 目录下。"
        local msg_dir_exists="/usr/software 目录已存在，是否删除？(Y/N): "
        local msg_skip_delete="选择了不删除 /usr/software 目录，退出安装。"
        local msg_invalid_choice="无效的选择。"
        local msg_softlink_created="软连接创建成功。"
    else
        local msg_wrong_dir="Current directory ($current_dir) is not the installation directory. A symbolic link will be created in /usr."
        local msg_dir_exists="/usr/software directory already exists. Delete it? (Y/N): "
        local msg_skip_delete="Chose not to delete /usr/software directory. Exiting installation."
        local msg_invalid_choice="Invalid choice."
        local msg_softlink_created="Symbolic link created successfully."
    fi

    if [ "$current_dir" != "$DBAIOps_oper_dir" ]; then
        c1 "$msg_wrong_dir" red

        if [ -d /usr/software ]; then
            read -p "$msg_dir_exists" choice
            case $choice in
                Y|y)
                    rm -rf /usr/software
                    ;;
                N|n)
                    c1 "$msg_skip_delete" red
                    exit 1
                    ;;
                *)
                    c1 "$msg_invalid_choice" red
                    exit 1
                    ;;
            esac
        fi

        # 创建软连接
        ln -s "$current_dir" /usr/software
        if [ $? -eq 0 ]; then
            c1 "$msg_softlink_created" green
        else
            c1 "软连接创建失败。" red
            exit 1
        fi
    fi
}

check_file() {
    # 多语言提示信息
    if [ "$LANGUAGE" == "cn" ]; then
        local msg_create_log="创建日志文件 $DBAIOps_log..."
        local msg_log_created="日志文件创建成功。"
        local msg_cfg_missing="DBAIOps.cfg 文件不存在，退出安装。"
    else
        local msg_create_log="Creating log file $DBAIOps_log..."
        local msg_log_created="Log file created successfully."
        local msg_cfg_missing="DBAIOps.cfg file does not exist. Exiting installation."
    fi

    # 检查日志文件是否存在，如果不存在则创建
    if [ ! -f "$DBAIOps_log" ]; then
        c1 "$msg_create_log" blue
        touch "$DBAIOps_log"
        if [ $? -eq 0 ]; then
            c1 "$msg_log_created" green
        else
            c1 "日志文件创建失败。" red
            exit 1
        fi
    fi

    # 检查 DBAIOps.cfg 文件是否存在
    if [ ! -f "$DBAIOps_oper_dir/DBAIOps.cfg" ]; then
        c1 "$msg_cfg_missing" red
        exit 1
    fi
}

check_config() {
    # 多语言提示信息
    if [ "$LANGUAGE" == "cn" ]; then
        local msg_config_DBAIOps="开始配置 KYSD..."
        local msg_role_missing="$CONF 目录下不存在 role.cfg 文件，退出安装。"
        local msg_config_success="KYSD 配置完成。"
    else
        local msg_config_DBAIOps="Starting KYSD configuration..."
        local msg_role_missing="role.cfg file does not exist in $CONF directory. Exiting installation."
        local msg_config_success="KYSD configuration completed."
    fi

    c1 "$msg_config_DBAIOps" blue

    # 调用 config_DBAIOps 函数
    config_DBAIOps

    # 检查 role.cfg 文件是否存在
    if [ ! -f "$CONF/role.cfg" ]; then
        c1 "$msg_role_missing" red
        exit 1
    else
        # 加载 role.cfg 文件
        . "$CONF/role.cfg"
    fi

    c1 "$msg_config_success" green
}


read_config(){
    . $CONF/role.cfg
    hosts=$(awk -F '=' '/^DS_Web|^DS_Collector|^DS_Monitor|^DS_Logana|^DS_Fstask|^DS_Other_Executor|^DS_Zookeeper|^DS_Redis/ {print $2}' $CONF/role.cfg | tr -s '\n' | tr ',' '\n' |sort -u |tr '\n' ',')
    hosts=${hosts%,}
    hlist=`echo $hosts | tr ',' '\n'`
    pgnode=`awk -F '=' '/^DSPG_Node/ {print $2}' $CONF/role.cfg`
    webip=`/usr/software/bin/DBAIOps-web.sh -getwebip`
    DBAIOps_log=/usr/software/bin/logs/DBAIOps.log
    redis_flag=`grep ^DFC_REDIS_SINGLENODE $CONF/DBAIOps.cfg`
}


# 显示安装完成后的信息
show_completion_message() {
    clear
    echo ''
    c1 "====================================================" blue
    if [ "$LANGUAGE" = "en" ]; then
        c1 "Installation completed successfully!" green
    else
        c1 "安装成功完成！" green
    fi
    echo ''
    echo ''
    c1 "====================================================" blue
    if [ "$LANGUAGE" = "en" ]; then
        c1 "Access URL: http://$webip:18081/DBAIOps" blue
        c1 "Username: admin" blue
        c1 "Password: admin@123" blue
    else
        c1 "访问地址: http://$webip:18081/DBAIOps" blue
        c1 "用户名: admin" blue
        c1 "密码: admin@123" blue
    fi
    c1 "====================================================" blue
    if [ "$LANGUAGE" = "en" ]; then
        c1 "Note: Please change the default password after first login." yellow
    else
        c1 "注意：首次登录后请修改默认密码。" yellow
    fi
    c1 "====================================================" blue
}


# 显示启动成功后的信息
show_startup_message() {
    clear
    echo ''
    c1 "====================================================" blue
    if [ "$LANGUAGE" = "en" ]; then
        c1 "StartUp successfully!" green
    else
        c1 "启动成功！" green
    fi
    echo ''
    echo ''
    c1 "====================================================" blue
    if [ "$LANGUAGE" = "en" ]; then
        c1 "Access URL: http://$webip:18081/DBAIOps" blue
    else
        c1 "访问地址: http://$webip:18081/DBAIOps" blue
    fi
    c1 "====================================================" blue
}


check_host_ssh() {
    # 多语言提示信息
    if [ "$LANGUAGE" == "cn" ]; then
        local msg_ssh_trusted="SSH 互信已配置：$ip"
        local msg_ssh_not_trusted="SSH 互信未配置：$ip，请配置 SSH 互信。"
        local msg_ssh_check_passed="SSH 互信检查通过。"
    else
        local msg_ssh_trusted="SSH trust configured for $ip"
        local msg_ssh_not_trusted="SSH trust not configured for $ip. Please configure SSH trust."
        local msg_ssh_check_passed="SSH trust check passed."
    fi

    for ip in $hlist; do
        if [ "$localnode" != "$ip" ]; then
            # 尝试在远程节点上运行一个简单的命令
            ssh -o BatchMode=yes "root@$ip" echo > /dev/null 2>&1
            if [ $? -eq 0 ]; then
                c1 "$msg_ssh_trusted" green
            else
                c1 "$msg_ssh_not_trusted" red
                log "ERROR" "$msg_ssh_not_trusted"
                exit 1
            fi
        fi
    done

    c1 "$msg_ssh_check_passed" green
}

check_time_sync() {
    # 多语言提示信息
    if [ "$LANGUAGE" == "cn" ]; then
        local msg_time_sync="远程节点 $ip 和本地节点时间同步。"
        local msg_time_not_sync="远程节点 $ip 和本地节点时间不同步，时间差为 $time_diff 秒。"
        local msg_time_check_passed="时间同步检查通过。"
    else
        local msg_time_sync="Time is synchronized between remote node $ip and local node."
        local msg_time_not_sync="Time is not synchronized between remote node $ip and local node. Time difference: $time_diff seconds."
        local msg_time_check_passed="Time synchronization check passed."
    fi

    local local_time=$(date +%s)
    for ip in $hlist; do
        if [ "$localnode" != "$ip" ]; then
            # 获取远程节点时间
            remote_time=$(ssh $ip "date +%s" 2>/dev/null)
            if [ -z "$remote_time" ]; then
                c1 "无法获取远程节点 $ip 的时间。" red
                log "ERROR" "Failed to get time from remote node $ip."
                exit 1
            fi

            # 计算时间差
            time_diff=$((remote_time - local_time))
            if [ $time_diff -gt 10 ] || [ $time_diff -lt -10 ]; then
                c1 "$msg_time_not_sync" red
                log "ERROR" "$msg_time_not_sync"
                exit 1
            else
                c1 "$msg_time_sync" green
            fi
        fi
    done

    c1 "$msg_time_check_passed" green
}

check_role() {
    # 多语言提示信息
    if [ "$LANGUAGE" == "cn" ]; then
        local msg_role_configured="role.cfg 文件已经配置。"
        local msg_role_not_configured="role.cfg 文件没有配置，请配置后重新执行安装程序。"
    else
        local msg_role_configured="role.cfg file is configured."
        local msg_role_not_configured="role.cfg file is not configured. Please configure it and rerun the installation."
    fi

    if ! grep -q "xxx.xxx" /usr/software/role.cfg; then
        c1 "$msg_role_configured" green
    else
        c1 "$msg_role_not_configured" red
        log "ERROR" "$msg_role_not_configured"
        exit 1
    fi
}
print_role() {
    # 多语言提示信息
    if [ "$LANGUAGE" == "cn" ]; then
        local msg_table_header="以下是 role.cfg 文件的内容："
        local msg_confirm_install="安装信息如上，请确认是否安装？(Y/N): "
        local msg_install_aborted="选择了不安装，退出安装。"
        local msg_invalid_choice="无效的选择。"
    else
        local msg_table_header="The content of role.cfg file is as follows:"
        local msg_confirm_install="The installation information is shown above. Confirm installation? (Y/N): "
        local msg_install_aborted="Installation aborted by user."
        local msg_invalid_choice="Invalid choice."
    fi

    # 打印表头
    c1 "$msg_table_header" blue
    printf "%-20s | %s\n" "KEY" "VALUE"
    printf "%-20s-+-%s\n" "--------------------" "--------------------"

    # 读取文件内容并打印
    while IFS='=' read -r key value; do
        if [ -n "$key" ] && [ -n "$value" ]; then
            printf "%-20s | %s\n" "$key" "$value"
        fi
    done < /usr/software/role.cfg

    # 提示用户确认是否安装
    while true; do
        read -p "$msg_confirm_install" choice
        case $choice in
            Y|y)
                c1 "继续安装..." green
                break
                ;;
            N|n)
                c1 "$msg_install_aborted" red
                log "INFO" "$msg_install_aborted"
                exit 1
                ;;
            *)
                c1 "$msg_invalid_choice" red
                ;;
        esac
    done
}


cmd=$1
type=$2


case $cmd in
    ("-envcheck")
        sh $bin/DBAIOps-env.sh -check
        ;;    
    ("-install")
        select_language
        check_dir
        check_file
        export LD_LIBRARY_PATH=/usr/lib64:/usr/lib

        # 让用户选择是单节点部署，还是分布式部署
        read_config
        if [ "$type" == "free" ]; then
            . $CONF/role.cfg
            genecfg
            install_free
        else
            if [ "$LANGUAGE" == "cn" ]; then
                c1 "请选择部署类型：" blue
                echo "  1：单节点部署"
                echo "  2：分布式部署(需手动配置role.cfg)"
                read -p "请输入部署类型(1 或 2) [1]：" choice
            else
                c1 "Please select deployment type:" blue
                echo "  1: Single-node deployment"
                echo "  2: Distributed deployment (requires manual configuration of role.cfg)"
                read -p "Please enter deployment type (1 or 2) [1]: " choice
            fi

            case $choice in
                1)
                    if [ "$LANGUAGE" == "cn" ]; then
                        c1 "选择了单节点部署。" green
                    else
                        c1 "Selected single-node deployment." green
                    fi
                    check_config
                    genecfg_single
                    print_role
                    ;;
                2)
                    if [ "$LANGUAGE" == "cn" ]; then
                        c1 "选择了分布式部署。" green
                    else
                        c1 "Selected distributed deployment." green
                    fi
                    check_role
                    print_role
                    check_host_ssh
                    setup_selinux
                    setup_firewall
                    check_set_timezone
                    check_time_sync
                    genecfg
                    ;;
                *)
                    if [ "$LANGUAGE" == "cn" ]; then
                        c1 "选择了单节点部署。" green
                    else
                        c1 "Selected single-node deployment." green
                    fi
                    check_config
                    genecfg_single
                    print_role
                    ;;
            esac

            # 环境检查
            sh $bin/DBAIOps-env.sh -check
            if [ $? -eq 1 ]; then
                exit 1
            fi

            # 安装
            install
        fi

        # 后续配置
        modifyWebCfg
        do_insert
        do_pg_insert
        do_crontab
        stop
        start
        show_completion_message
        ;;

    ("-start")
        read_config
        start
        show_startup_message
        ;;

    ("-stop")
        read_config
        stop
        ;;

    ("-status")
        read_config
        status
        ;;

    ("-clslog")
        clslog
        ;;

    ("-reinstall")
        read_config
        genecfg
        reinstall
        do_insert
        do_pg_insert
        stop
        start
        show_completion_message
        ;;

    ("-restart")
        read_config
        stop
        start
        show_startup_message
        ;;

    ("-updatecomp")
        read_config
        genecfg
        do_insert
        do_pg_insert
        ;;

    ("-genecfg")
        read_config
        . $CONF/role.cfg
        genecfg
        ;;

    ("-pgfincore")
        pgfincore
        ;;

    ("-upgrade")
        upgrade $type
        ;;

    (*)
        if [ "$LANGUAGE" == "cn" ]; then
            c1 "无效命令，请重新输入！" red
        else
            c1 "Invalid command, please try again!" red
        fi
        print_usage
        ;;
esac

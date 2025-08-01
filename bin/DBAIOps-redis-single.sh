#!/bin/bash
#
#

bin=`dirname "${BASH_SOURCE-$0}"`
bin=`cd "$bin"; pwd`
ROOT=`cd $bin;cd ..;pwd`
DBAIOps_HOME="/usr/software"
DBAIOps_oper_dir=/usr/software
redis_home=$DBAIOps_oper_dir/redis
CONF=$DBAIOps_HOME
localnode=`hostname`

# 获取主脚本中的语言设置
if [ -z "$LANGUAGE" ]; then
    LANGUAGE="en"  # 默认英文
fi

print_usage(){
    echo "Usage: DBAIOps redis management script"
    echo "< -install | -start | -stop | -status | -clean >"
    echo "  -install                       install redis service"
    echo "  -start                         start redis service"
    echo "  -stop                          stop redis service"
    echo "  -status                        check redis service status"
    echo "  -clean                         clean redis service"
}

install() {
    # 日志文件路径
    log_file="/var/log/redis_install.log"

    # 根据 LANGUAGE 变量设置提示信息
    if [[ $LANGUAGE == "cn"* ]]; then
        echo "############################################################" | tee -a $log_file
        echo "                      安装 Redis                            " | tee -a $log_file
        echo "############################################################" | tee -a $log_file
        local_node_msg="本地节点安装 Redis 环境"
        remote_node_msg="远程节点安装 Redis 环境"
        build_success_msg="Redis 编译成功！"
        install_success_msg="Redis 安装成功！"
    else
        echo "############################################################" | tee -a $log_file
        echo "                      Install Redis                         " | tee -a $log_file
        echo "############################################################" | tee -a $log_file
        local_node_msg="Local node installing Redis environment"
        remote_node_msg="Remote node installing Redis environment"
        build_success_msg="Redis build succeeded!"
        install_success_msg="Redis installed successfully!"
    fi

    # 安装 Redis
    for ip in $rdlist; do
        if [ $localnode == $ip ]; then
            echo "$local_node_msg" | tee -a $log_file
            echo "解压 Redis 安装包..." | tee -a $log_file
            cd $DBAIOps_oper_dir
            tar --no-same-owner -xzvf $DBAIOps_oper_dir/redis-7.0.2.tar.gz >>$log_file 2>&1
            echo "编译 Redis..." | tee -a $log_file
            cd $redis_home/redis-7.0.2
            make distclean >>$log_file 2>&1
            make >>$log_file 2>&1
            make install >>$log_file 2>&1
            echo "配置 Redis 环境变量..." | tee -a $log_file
            echo "export PATH=$redis_home/redis-7.0.2/src:\$PATH" >/etc/profile.d/redis.sh
        else
            echo "$ip: $remote_node_msg" | tee -a $log_file
            ssh $ip "echo '解压 Redis 安装包...' >> $log_file; cd $DBAIOps_oper_dir; tar --no-same-owner -xzvf $DBAIOps_oper_dir/redis-7.0.2.tar.gz >> $log_file 2>&1; echo '编译 Redis...' >> $log_file; cd $redis_home/redis-7.0.2; make distclean >> $log_file 2>&1; make >> $log_file 2>&1; make install >> $log_file 2>&1; echo '配置 Redis 环境变量...' >> $log_file; echo \"export PATH=$redis_home/redis-7.0.2/src:\$PATH\" > /etc/profile.d/redis.sh"
        fi
    done

    echo "$build_success_msg" | tee -a $log_file

    # 替换配置文件
    for ip in $rdlist; do
        if [ $localnode == $ip ]; then
            echo "检测系统架构..." | tee -a $log_file
            arm_flag=$(uname -r | grep aarch64)
            set -e
            if [ -n "$arm_flag" ]; then
                echo "添加 ARM64 警告忽略配置..." | tee -a $log_file
                echo "ignore-warnings ARM64-COW-BUG" >>$redis_home/redis_conf/master_slave/redis.conf
            fi
        else
            echo "$ip: 检测系统架构..." | tee -a $log_file
            arm_flag=$(ssh $ip "uname -r | grep aarch64")
            if [ -n "$arm_flag" ]; then
                echo "$ip: 添加 ARM64 警告忽略配置..." | tee -a $log_file
                ssh $ip "echo \"ignore-warnings ARM64-COW-BUG\" >> $redis_home/redis_conf/master_slave/redis.conf"
            fi
        fi
    done

    echo "$install_success_msg" | tee -a $log_file
}

install_free()
{
    echo "############################################################"
    echo "                      install redis                         "
    echo "############################################################"

    for ip in $rdlist
    do
        if [ $localnode == $ip ];then
            echo "local node install redis enviroment"
            cd $DBAIOps_oper_dir;tar --no-same-owner -xzvf $DBAIOps_oper_dir/redis-7.0.2.tar.gz > /dev/null 2>&1;
            echo "export PATH=$redis_home/redis-7.0.2/src:\$PATH" > /etc/profile.d/redis.sh
        else
            echo "$ip:"
            ssh $ip "cd $DBAIOps_oper_dir;tar --no-same-owner -xzvf $DBAIOps_oper_dir/redis-7.0.2.tar.gz > /dev/null 2>&1;echo \"export PATH=$redis_home/redis-7.0.2/src:\$PATH\" > /etc/profile.d/redis.sh"
        fi
    done


    for ip in $rdlist
    do
    if [ $localnode == $ip ];then
        # ipa=`hostname -i|awk '{print $1}'`
        # sed -i "s/bind \*/bind 0.0.0.0/g" $redis_home/redis_conf/master_slave/redis.conf
        set +e
        arm_flag=`uname -r|grep aarch64`
        set -e
        if [ -n "$arm_flag" ];then
            echo "ignore-warnings ARM64-COW-BUG" >> $redis_home/redis_conf/master_slave/redis.conf
        fi
    else
        # ipa=`ssh $ip "hostname -i|awk '{print $1}'"`
        # ssh $ip "sed -i \"s/bind \*/bind 0.0.0.0/g\" $redis_home/redis_conf/master_slave/redis.conf"
        arm_flag=`ssh $ip "uname -r|grep aarch64"`
        if [ -n "$arm_flag" ];then
            ssh $ip "echo \"ignore-warnings ARM64-COW-BUG\" >> $redis_home/redis_conf/master_slave/redis.conf"
        fi
    fi
    done
    echo "Redis install Successed!"
}


start()
{
    echo "############################################################"
    echo "                      start redis                           "
    echo "############################################################"
    for ip in $rdlist
    do
        if [ $localnode == $ip ];then
        echo "local node start redis"
        $redis_home/redis-7.0.2/src/redis-server $redis_home/redis_conf/master_slave/redis.conf
        else
        echo "$ip:"
        ssh $ip "$redis_home/redis-7.0.2/src/redis-server $redis_home/redis_conf/master_slave/redis.conf"
        fi
    done
    echo "redis start successful."
}

stop()
{
    echo "############################################################"
    echo "                      stop redis                            "
    echo "############################################################"
    for ip in $rdlist
    do
        if [ $localnode == $ip ];then
            echo "local node stop redis"
            set +e
            pkill redis-
            set -e
        else
            echo "$ip:"
            redis_sstat=`ssh $ip "ps -ef|grep redis-server|grep -v \"grep\"|awk '{print \\\$2}'"`
        fi
        if [ ! "$redis_sstat" = "" ];then
          ssh $ip 'ps -ef | grep redis- | grep -v grep | awk "{print \$2}" | xargs kill -9 && wait'
        else
            echo "Redis_Server is not running!"
        fi
    done
    echo "redis stop successful."
}

kill()
{
    echo "############################################################"
    echo "                      kill redis                            "
    echo "############################################################"
    for ip in $rdlist
    do
        if [ $localnode == $ip ];then
            echo "local node stop redis"
            pkill redis-
        else
            echo "$ip:"
            redis_sstat=`ssh $ip "ps -ef|grep redis-server|grep -v \"grep\"|awk '{print \\\$2}'"`
        fi
        if [ ! "$redis_sstat" = "" ];then
          ssh $ip 'ps -ef | grep redis- | grep -v grep | awk "{print \$2}" | xargs kill -9 && wait'
        else
            echo "Redis_Server is not running!"
        fi
    done
    echo "redis kill successful."
}

status()
{
    echo "############################################################"
    echo "                      status redis                          "
    echo "############################################################"
    for ip in $rdlist
    do
        if [ $localnode == $ip ];then
        echo "local node redis status"
        redis_sstat=`ps -ef|grep redis-server|grep -v grep|awk '{print $2}'`
        else
        echo "$ip:"
        redis_sstat=`ssh $ip "ps -ef|grep redis-server|grep -v \"grep\"|awk '{print \\\$2}'"`
        fi
        if [ ! "$redis_sstat" = "" ];then
            echo "Redis_Server is running(PID:$redis_sstat)!"
        else
            echo "Redis_Server is not running!"
        fi
    done
}

clean()
{
    echo "############################################################"
    echo "                      clean redis                           "
    echo "############################################################"   
    set +e
    stop > /dev/null 2>&1
    set -e
    for ip in $rdlist
    do
        if [ $localnode == $ip ];then
        echo "local node clean redis enviroment"
        if [ -d "$redis_home" ];then rm -rf $redis_home;fi
        else
        echo "Clean $ip:"
        ssh $ip "if [ -d "$redis_home" ];then rm -rf $redis_home;fi"
        fi
    done
}

# 检查 DBAIOps_oper_dir 是否存在
if [ -z "$DBAIOps_oper_dir" ]; then
    if [[ $LANGUAGE == "cn"* ]]; then
        echo "DBAIOps安装目录不存在！" | tee -a $log_file
    else
        echo "DBAIOps installation directory does not exist!" | tee -a $log_file
    fi
    exit 1
fi

# 检查 Redis 安装文件是否存在
if [ ! -f "$DBAIOps_oper_dir/redis-7.0.2.tar.gz" ]; then
    if [[ $LANGUAGE == "cn"* ]]; then
        echo "redis安装文件不存在！"  | tee -a $log_file
    else
        echo "Redis installation file does not exist!" | tee -a $log_file
    fi
    exit 1
fi

# 检查 role.cfg 文件是否存在
if [ ! -f "$CONF/role.cfg" ]; then
    if [[ $LANGUAGE == "cn"* ]]; then
        echo  "在 $CONF 目录中未找到 role.cfg 文件"  | tee -a $log_file
    else
        echo "There is no role.cfg in $CONF" | tee -a $log_file
    fi
    exit 1
else
    # 如果 role.cfg 存在，加载它
    . "$CONF/role.cfg"
fi

dsrd=`awk -F '=' '/^DS_Redis/ {print $2}' $CONF/role.cfg`

if [ -z $2 ] || [ $1 == "-start" ];then
    rdlist=`echo $dsrd | tr ',' '\n'`
else
    rdlist=$2
fi

case $1 in
        "-install")
                install $rdlist
        ;;
        "-install_free")
                install_free $rdlist
        ;;
        "-start")
                start $rdlist
        ;;
        "-stop")
                stop $rdlist
        ;;
        "-kill")
                kill $rdlist
        ;;
        "-status")
                status $rdlist
        ;;
        "-clean")
                clean $rdlist
        ;;
        *)
                print_usage
                exit 1
        ;;
esac

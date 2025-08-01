#!/bin/bash
#

bin=`dirname "${BASH_SOURCE-$0}"`
bin=`cd "$bin"; pwd`
ROOT=`cd $bin;cd ..;pwd`
DBAIOps_HOME="/usr/software"
DBAIOps_oper_dir=/usr/software
redis_home=$DBAIOps_oper_dir/redis
CONF=$DBAIOps_HOME
cpu_version=`uname -a|grep aarch64`
localnode=`hostname`
local_ip=`hostname -i|awk '{print $1}'`

print_usage(){
  echo "Usage: DBAIOps redis management script"
  echo "< -install | -start | -stop | -status | -clean >"
  echo "  -install                       install redis service"
  echo "  -start                         start redis service"
  echo "  -stop                          stop redis service"
  echo "  -status                        check redis service status"
  echo "  -clean                         clean redis service"
}

install()
{
    echo "############################################################"
    echo "                      install redis                         "
    echo "############################################################"
    for ip in $rdlist
    do
        echo "$ip:"
        ssh $ip "cd $DBAIOps_oper_dir;tar --no-same-owner -xzvf $DBAIOps_oper_dir/redis-7.0.2.tar.gz > /dev/null 2>&1"
    done
        ##replace conf
    if [ $dsrdnum = 3 ];then
        num=1
        cp -r $redis_home/redis_conf/master_slave $redis_home/redis_conf/master_slave_tmp
        cp -r $redis_home/redis_conf/sentinel $redis_home/redis_conf/sentinel_tmp
        for ip in $rdlist
        do
            if [ $num == 1 ];then
                ip=`ssh $ip "hostname -i|awk '{print $1}'"` 
                sed -i "s/127.0.0.1 16379/$ip 16379/g" $redis_home/redis_conf/master_slave_tmp/redis.conf 
                sed -i "s/127.0.0.1 16379/$ip 16379/g" $redis_home/redis_conf/master_slave_tmp/slave6380.conf 
                sed -i "s/127.0.0.1 16379/$ip 16379/g" $redis_home/redis_conf/master_slave_tmp/slave6381.conf 
                sed -i "s/bind \*/bind $ip/g" $redis_home/redis_conf/master_slave_tmp/redis.conf

                sed -i "s/127.0.0.1 16379/$ip 16379/g" $redis_home/redis_conf/sentinel_tmp/sentinel.conf
                sed -i "s/127.0.0.1 26379/$ip 26379/g" $redis_home/redis_conf/sentinel_tmp/sentinel.conf
                sed -i "s/127.0.0.1 16379/$ip 16379/g" $redis_home/redis_conf/sentinel_tmp/sentinel26380.conf
                sed -i "s/127.0.0.1 26379/$ip 26379/g" $redis_home/redis_conf/sentinel_tmp/sentinel26380.conf
                sed -i "s/127.0.0.1 16379/$ip 16379/g" $redis_home/redis_conf/sentinel_tmp/sentinel26381.conf
                sed -i "s/127.0.0.1 26379/$ip 26379/g" $redis_home/redis_conf/sentinel_tmp/sentinel26381.conf
            elif [ $num == 2 ];then
                ip=`ssh $ip "hostname -i|awk '{print $1}'"` 
                sed -i "s/bind \*/bind $ip/g" $redis_home/redis_conf/master_slave_tmp/slave6380.conf
                sed -i "/127.0.0.1 16380/d" $redis_home/redis_conf/sentinel_tmp/sentinel.conf
                sed -i "s/127.0.0.1 26380/$ip 26380/g" $redis_home/redis_conf/sentinel_tmp/sentinel.conf
                sed -i "/127.0.0.1 16380/d" $redis_home/redis_conf/sentinel_tmp/sentinel26380.conf
                sed -i "s/127.0.0.1 26380/$ip 26380/g" $redis_home/redis_conf/sentinel_tmp/sentinel26380.conf
                sed -i "/127.0.0.1 16380/d" $redis_home/redis_conf/sentinel_tmp/sentinel26381.conf
                sed -i "s/127.0.0.1 26380/$ip 26380/g" $redis_home/redis_conf/sentinel_tmp/sentinel26381.conf
            elif [ $num == 3 ];then 
                ip=`ssh $ip "hostname -i|awk '{print $1}'"` 
                sed -i "s/bind \*/bind $ip/g" $redis_home/redis_conf/master_slave_tmp/slave6381.conf
                sed -i "/127.0.0.1 16381/d" $redis_home/redis_conf/sentinel_tmp/sentinel.conf
                sed -i "s/127.0.0.1 26381/$ip 26381/g" $redis_home/redis_conf/sentinel_tmp/sentinel.conf
                sed -i "/127.0.0.1 16381/d" $redis_home/redis_conf/sentinel_tmp/sentinel26380.conf
                sed -i "s/127.0.0.1 26381/$ip 26381/g" $redis_home/redis_conf/sentinel_tmp/sentinel26380.conf
                sed -i "/127.0.0.1 16381/d" $redis_home/redis_conf/sentinel_tmp/sentinel26381.conf
                sed -i "s/127.0.0.1 26381/$ip 26381/g" $redis_home/redis_conf/sentinel_tmp/sentinel26381.conf
            fi
            num=`expr $num + 1`
        done

        unset num
        for ip in $rdlist
        do
            scp -r -q $redis_home/redis_conf/master_slave_tmp/* $ip:$redis_home/redis_conf/master_slave/
            scp -r -q $redis_home/redis_conf/sentinel_tmp/* $ip:$redis_home/redis_conf/sentinel/
        done
    else
        cd $DBAIOps_oper_dir;tar --no-same-owner -xzvf $DBAIOps_oper_dir/redis-7.0.2.tar.gz > /dev/null 2>&1
        for ip in $rdlist
        do
        if [ $localnode == $ip ];then
            ipa=`hostname -i|awk '{print $1}'`
        else
            ipa=`ssh $ip "hostname -i|awk '{print $1}'"`
        fi
        sed -i "s/bind \*/bind $ipa/g" $redis_home/redis_conf/master_slave/redis.conf
        sed -i "s/bind \*/bind $ipa/g" $redis_home/redis_conf/master_slave/slave6380.conf
        sed -i "s/slaveof 127.0.0.1/slaveof $ipa/g" $redis_home/redis_conf/master_slave/slave6380.conf
        sed -i "s/bind \*/bind $ipa/g" $redis_home/redis_conf/master_slave/slave6381.conf
        sed -i "s/slaveof 127.0.0.1/slaveof $ipa/g" $redis_home/redis_conf/master_slave/slave6381.conf
        sed -i "/127.0.0.1 16380/d" $redis_home/redis_conf/sentinel/sentinel.conf
        sed -i "/127.0.0.1 16381/d" $redis_home/redis_conf/sentinel/sentinel.conf
        sed -i "/127.0.0.1 16380/d" $redis_home/redis_conf/sentinel/sentinel26380.conf
        sed -i "/127.0.0.1 16381/d" $redis_home/redis_conf/sentinel/sentinel26380.conf
        sed -i "/127.0.0.1 16380/d" $redis_home/redis_conf/sentinel/sentinel26381.conf
        sed -i "/127.0.0.1 16381/d" $redis_home/redis_conf/sentinel/sentinel26381.conf
        sed -i "s/127.0.0.1/$ipa/g" $redis_home/redis_conf/sentinel/sentinel.conf
        sed -i "s/127.0.0.1/$ipa/g" $redis_home/redis_conf/sentinel/sentinel26380.conf
        sed -i "s/127.0.0.1/$ipa/g" $redis_home/redis_conf/sentinel/sentinel26381.conf
        done
        
        for ip in $rdlist
        do
            if [ $localnode != $ip ];then
                scp -r -q $redis_home/redis_conf/master_slave_tmp/* $ip:$redis_home/redis_conf/master_slave/
                scp -r -q $redis_home/redis_conf/sentinel_tmp/* $ip:$redis_home/redis_conf/sentinel/
            fi
        done
    fi
    if [ ! -z "$cpu_version"];then
      echo "ignore-warnings ARM64-COW-BUG"  >>  $redis_home/redis_conf/master_slave/redis.conf
    fi
    echo "Redis install Successed!"
}

start()
{
    echo "############################################################"
    echo "                      start redis                           "
    echo "############################################################"
    if [ $dsrdnum = 3 ];then
        num=1
        for ip in $rdlist
        do
            echo "$ip:"
            if [ $num == 1 ];then
                ssh $ip "$redis_home/redis-7.0.2/src/redis-server $redis_home/redis_conf/master_slave/redis.conf > /dev/null 2>&1"
            elif [ $num == 2 ];then
                ssh $ip "$redis_home/redis-7.0.2/src/redis-server $redis_home/redis_conf/master_slave/slave6380.conf > /dev/null 2>&1"
            elif [ $num == 3 ];then 
                ssh $ip "$redis_home/redis-7.0.2/src/redis-server $redis_home/redis_conf/master_slave/slave6381.conf > /dev/null 2>&1"
            fi
            num=`expr $num + 1`
        done
        unset num

        num=1
        for ip in $rdlist
        do
            echo "$ip:"
            if [ $num == 1 ];then
                ssh $ip "$redis_home/redis-7.0.2/src/redis-sentinel $redis_home/redis_conf/sentinel/sentinel.conf > /dev/null 2>&1"
            elif [ $num == 2 ];then
                ssh $ip "$redis_home/redis-7.0.2/src/redis-sentinel $redis_home/redis_conf/sentinel/sentinel26380.conf > /dev/null 2>&1"
            elif [ $num == 3 ];then 
                ssh $ip "$redis_home/redis-7.0.2/src/redis-sentinel $redis_home/redis_conf/sentinel/sentinel26381.conf > /dev/null 2>&1"
            fi
            num=`expr $num + 1`
        done
        unset num
    else
        for ip in $rdlist
        do
            echo "$ip:"
            ssh $ip "$redis_home/redis-7.0.2/src/redis-server $redis_home/redis_conf/master_slave/redis.conf > /dev/null 2>&1"
            ssh $ip "$redis_home/redis-7.0.2/src/redis-server $redis_home/redis_conf/master_slave/slave6380.conf > /dev/null 2>&1"
            ssh $ip "$redis_home/redis-7.0.2/src/redis-server $redis_home/redis_conf/master_slave/slave6381.conf > /dev/null 2>&1"
            ssh $ip "$redis_home/redis-7.0.2/src/redis-sentinel $redis_home/redis_conf/sentinel/sentinel.conf > /dev/null 2>&1"
            ssh $ip "$redis_home/redis-7.0.2/src/redis-sentinel $redis_home/redis_conf/sentinel/sentinel26380.conf > /dev/null 2>&1"
            ssh $ip "$redis_home/redis-7.0.2/src/redis-sentinel $redis_home/redis_conf/sentinel/sentinel26381.conf > /dev/null 2>&1"
        done
    fi
}

stop()
{
    echo "############################################################"
    echo "                      stop redis                            "
    echo "############################################################"
    if [ $dsrdnum -eq 1 ];then
        for ip in $rdlist
        do
            echo "$ip:"
            ssh $ip "pkill redis-"
        done

    else
        for ip in $rdlist
        do
            echo "$ip:"
            redis_pid=`ssh $ip "ps -ef|grep redis-sentinel|grep -v \"grep\"|awk '{print \\\$2}'"`
            if [ ! -z "$redis_pid" ]; then
                ssh $ip "kill -SIGTERM $redis_pid"
            fi
            unset redis_pid
        done
        for ip in $rdlist
        do
            echo "$ip:"
            redis_pid=`ssh $ip "ps -ef|grep redis-server|grep -v \"grep\"|awk '{print \\\$2}'"`
            if [ ! -z "$redis_pid" ]; then
                ssh $ip "kill -SIGTERM $redis_pid"
            fi
            unset redis_pid
        done
    fi
}

kill()
{
    echo "############################################################"
    echo "                      kill redis                            "
    echo "############################################################"
    if [ $dsrdnum -eq 1 ];then
        for ip in $rdlist
        do
            echo "$ip:"
            ssh $ip "pkill redis-"
        done

    else
        for ip in $rdlist
        do
            echo "$ip:"
            redis_pid=`ssh $ip "ps -ef|grep redis-sentinel|grep -v \"grep\"|awk '{print \\\$2}'"`
            if [ ! -z "$redis_pid" ]; then
                ssh $ip "kill -9 $redis_pid"
            fi
            unset redis_pid
        done
        for ip in $rdlist
        do
            echo "$ip:"
            redis_pid=`ssh $ip "ps -ef|grep redis-server|grep -v \"grep\"|awk '{print \\\$2}'"`
            if [ ! -z "$redis_pid" ]; then
                ssh $ip "kill -9 $redis_pid"
            fi
            unset redis_pid
        done
    fi
}

status()
{
    echo "############################################################"
    echo "                      status redis                          "
    echo "############################################################"
    for ip in $rdlist
    do
        echo "$ip:"
        redis_stat=`ssh $ip "ps -ef|grep redis-sentinel|grep -v \"grep\"|awk '{print \\\$2}'"`
        redis_sstat=`ssh $ip "ps -ef|grep redis-server|grep -v \"grep\"|awk '{print \\\$2}'"`
        if [ ! "$redis_stat" = "" ];then
            echo "Redis_Sentinel is running(PID:$redis_stat)!"
        else
            echo "Redis_Sentinel is not running!"
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
    stop $rdlist > /dev/null 2>&1
    for ip in $rdlist
    do
        echo "Clean $ip:"
        ssh $ip "if [ -d "$redis_home" ];then rm -rf $redis_home;fi"
        echo "$ip Redis Clean successful"
    done
}

if [ -z $DBAIOps_oper_dir ];then
    echo "DBAIOps安装目录不存在！"
    exit 1
fi

if [ ! -f $DBAIOps_oper_dir/redis-7.0.2.tar.gz ];then
    echo "redis安装文件不存在！"
    exit 1
fi

if [ ! -f $CONF/role.cfg ];then
    echo "There is no role.cfg in $CONF"
    exit 1
else
    . $CONF/role.cfg
fi

dsrd=`awk -F '=' '/^DS_Redis/ {print $2}' $CONF/role.cfg`
dsrdnum=`echo $dsrd | tr ',' '\n' |wc -l`
if [ $dsrdnum -eq 1 ];then
    echo "1 node"
elif [ $dsrdnum -eq 3 ];then
    echo "3 nodes"
else
    echo "Please check the role.cfg, Redis must be 1 node or 3 nodes"
    exit 1
fi

if [ -z $2 ] || [ $1 == "-start" ];then
    rdlist=`echo $dsrd | tr ',' '\n'`
else
    rdlist=$2
fi

case $1 in
        "-install")
                install $rdlist
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

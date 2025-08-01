#!/bin/bash
#
#
#
set -e
bin=`dirname "${BASH_SOURCE-$0}"`
bin=`cd "$bin"; pwd`
ROOT=`cd $bin;cd ..;pwd`
DBAIOps_HOME="/usr/software"
DBAIOps_oper_dir=/usr/software
web_home=$DBAIOps_oper_dir/webserver
CONF=$DBAIOps_HOME
localnode=`hostname`

print_usage(){
    echo "Usage: DBAIOps web management script"
    echo "  -start                         start web service"
    echo "  -stop                          stop web service"
    echo "  -status                        check web service status"
}


start()
{
    echo "############################################################"
    echo "                     start web service                       "
    echo "############################################################"
    for ip in $weblist
    do
        if [ $localnode == $ip ];then
        echo "local node start web service"
        sh $web_home/bin/webserver.sh start
        else
        echo "$ip:"
        ssh $ip "sh $web_home/bin/webserver.sh start"
        fi
    done
    #if [ $? -eq 0 ];then
    #    echo "webserver Start Successed!"
    #else
    #    echo "webserver Start Failed!"
    #    exit 1
    #fi
}

getwebip(){
    for ip in $weblist
    do
        if [ $localnode == $ip ];then
            webip=`hostname -i|awk '{print $1}'`
            echo $webip
        else
            webip=`ssh $ip "hostname -i|awk '{print $1}'"`
            echo $webip
        fi
    done
}

stop()
{
    echo "############################################################"
    echo "                      stop web service                      "
    echo "############################################################"
    for ip in $weblist
    do
        if [ $localnode == $ip ];then
        echo "local node stop web service"
        sh $web_home/bin/webserver.sh stop
        else
        echo "$ip:"
        ssh $ip "sh $web_home/bin/webserver.sh stop"
        fi
    done
}

kill()
{
    echo "############################################################"
    echo "                      kill web service                      "
    echo "############################################################"
    for ip in $weblist
    do
        if [ $localnode == $ip ];then
        echo "local node kill web process"
        PROC=`ps -ef | grep webserver/lib/apache-tomcat|grep -v grep|awk '{print $2}'`
        if [ "$PROC" ]; then
            kill -SIGTERM $PROC
        fi
        else
        echo "$ip:"
        PROC=`ssh $ip "ps -ef | grep webserver/lib/apache-tomcat|grep -v grep|awk '{print \\\$2}'"`
        if [ "$PROC" ]; then
            ssh $ip "kill -SIGTERM $PROC"
        fi
        fi
    done
}

status()
{
    echo "############################################################"
    echo "                     status web service                      "
    echo "############################################################"
    for ip in $weblist
    do
        if [ $localnode == $ip ];then
        echo "local node web status"
        PROC=`ps -ef | grep webserver/lib/apache-tomcat|grep -v grep|awk '{print $2}'`
        else
        echo "$ip:"
        PROC=`ssh $ip "ps -ef | grep webserver/lib/apache-tomcat|grep -v grep|awk '{print \\\$2}'"`
        fi
        if [ "$PROC" ]; then
            echo "webserver is running (PID:$PROC)!"
        else
            echo "webserver is not running!"
        fi
    done
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

webl=`awk -F '=' '/^DS_Web/ {print $2}' $CONF/role.cfg`
weblnum=`echo $webl | tr ',' '\n' |wc -l`

#if [ $weblnum -gt 1 ];then
#    echo "Web服务仅支持一个节点!"
#    exit 1
#fi

#if [ ! `hostname` == "$weblist" ];then
#    echo "Web服务必须部署在此节点上:`hostname`!"
#    exit 1
#fi
if [ -z $2 ];then
    weblist=`echo $webl | tr ',' '\n'`
else
    weblist=$2
fi


case $1 in
        "-start")
                start $weblist
        ;;
        "-stop")
                stop $weblist
        ;;
        "-status")
                status $weblist
        ;;
        "-kill")
                kill $weblist
        ;;
        "-getwebip")
                getwebip $weblist
        ;;
        *)
                print_usage
                exit 1
        ;;
esac

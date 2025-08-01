#!/bin/bash
#
#
set -e
bin=`dirname "${BASH_SOURCE-$0}"`
bin=`cd "$bin"; pwd`
ROOT=`cd $bin;cd ..;pwd`
DBAIOps_HOME="/usr/software"
DBAIOps_oper_dir=/usr/software
return_base=$DBAIOps_oper_dir/return
CONF=$DBAIOps_HOME
localnode=`hostname`
local_ip=`hostname -i|awk '{print $1}'`
print_usage(){
  echo "Usage: DBAIOps return script"
  echo "< -start [ collector|monitor|logana ] | -stop [ collector|monitor|logana|dbconn ] | -status [ collector|monitor|logana|dbconn ] | -zkinfo >"
  echo "  -start                       start collector|monitor|logana|alarm|dbconn service"
  echo "  -stop                        stop collector|monitor|logana|alarm|dbconn service"
  echo "  -status                      check collector|monitor|logana|alarm|dbconn service"
  echo "  -zkinfo                      view zookeeper info"
}

start()
{
    echo "############################################################"
    echo "                   start return service                     "
    echo "############################################################"
    case $1 in
        "dbconn")
        for ip in $collist
        do
            if [[ $localnode == $ip || $local_ip == $ip ]];then
            echo "local node start dbconn service"
            sh $return_base/bin/db-conn.sh start
            else
            echo "$ip:"
            ssh $ip "sh $return_base/bin/db-conn.sh start"
            fi
        done
        ;;
        "collector")
        for ip in $collist
        do
            if [[ $localnode == $ip || $local_ip == $ip ]];then
            echo "local node start collector service"
            sh $return_base/bin/collector.sh start
            else
            echo "$ip:"
            ssh $ip "sh $return_base/bin/collector.sh start > /dev/null 2>&1"
            fi
        done
        echo "Collector service started!"
        ;;
        "monitor")
        for ip in $monlist
        do
            if [[ $localnode == $ip || $local_ip == $ip ]];then
            echo "local node start monitor service"
            sh $return_base/bin/monitor.sh start
            else
            echo "$ip:"
            ssh $ip "sh $return_base/bin/monitor.sh start > /dev/null 2>&1"
            fi
        done
        echo "Monitor service started!"
        ;;
        "logana")
        for ip in $loglist
        do
            if [[ $localnode == $ip || $local_ip == $ip ]];then
            echo "local node start logana service"
            sh $return_base/bin/logana.sh start 
            else
            echo "$ip:"
            ssh $ip "sh $return_base/bin/logana.sh start > /dev/null 2>&1"
            fi
        done
        echo "LogAna service started!"
        ;;
        "alarm")
        for ip in $monlist
        do
            if [[ $localnode == $ip || $local_ip == $ip ]];then
            echo "local node start Monitor alarm service"
            sh $return_base/bin/monitor-alarm-center.sh start > /dev/null
            else
            echo "$ip:"
            ssh $ip "sh $return_base/bin/monitor-alarm-center.sh start > /dev/null 2>&1"
            fi
        done
        echo "Monitor alarm service started!"
        ;;
        *)
        print_usage
        exit 1
        ;;
    esac
}

stop()
{
    echo "############################################################"
    echo "                   stop return service                      "
    echo "############################################################"
    case $1 in
        "dbconn")
        for ip in $collist
        do
            if [[ $localnode == $ip || $local_ip == $ip ]];then
            echo "local node stop dbconn service"
            sh $return_base/bin/db-conn.sh stop
            else
            echo "$ip:"
            ssh $ip "sh $return_base/bin/db-conn.sh stop"
            fi
        done
        ;;
        "collector")
        for ip in $collist
        do
            if [[ $localnode == $ip || $local_ip == $ip ]];then
            echo "local node stop collector service"
            sh $return_base/bin/collector.sh stop
            else
            echo "$ip:"
            ssh $ip "sh $return_base/bin/collector.sh stop"
            fi
        done
        ;;
        "monitor")
        for ip in $monlist
        do
            if [[ $localnode == $ip || $local_ip == $ip ]];then
            echo "local node stop monitor service"
            sh $return_base/bin/monitor.sh stop
            else
            echo "$ip:"
            ssh $ip "sh $return_base/bin/monitor.sh stop"
            fi
        done
        ;;
        "logana")
        for ip in $loglist
        do
            if [[ $localnode == $ip || $local_ip == $ip ]];then
            echo "local node stop logana service"
            sh $return_base/bin/logana.sh stop
            else
            echo "$ip:"
            ssh $ip "sh $return_base/bin/logana.sh stop"
            fi
        done
        ;;
        "alarm")
        for ip in $monlist
        do
            if [[ $localnode == $ip || $local_ip == $ip ]];then
            echo "local node stop Monitor alarm service"
            sh $return_base/bin/monitor-alarm-center.sh stop
            else
            echo "$ip:"
            ssh $ip "sh $return_base/bin/monitor-alarm-center.sh stop"
            fi
        done
        ;;
        *)
        print_usage
        exit 1
        ;;
    esac
}

kill()
{
    echo "############################################################"
    echo "                   kill return service                      "
    echo "############################################################"
        case $1 in
        "dbconn")
        for ip in $collist
        do
            if [[ $localnode == $ip || $local_ip == $ip ]];then
            echo "local node stop dbconn service"
            sh $return_base/bin/db-conn.sh stop
            else
            echo "$ip:"
            ssh $ip "sh $return_base/bin/db-conn.sh stop"
            fi
        done
        ;;
        "collector")
        for ip in $collist
        do
            if [[ $localnode == $ip || $local_ip == $ip ]];then
            echo "local node stop collector service"
            sh $return_base/bin/collector.sh stop
            else
            echo "$ip:"
            ssh $ip "sh $return_base/bin/collector.sh stop"
            fi
        done
        ;;
        "monitor")
        for ip in $monlist
        do
            if [[ $localnode == $ip || $local_ip == $ip ]];then
            echo "local node stop monitor service"
            sh $return_base/bin/monitor.sh stop
            else
            echo "$ip:"
            ssh $ip "sh $return_base/bin/monitor.sh stop"
            fi
        done
        ;;
        "logana")
        for ip in $loglist
        do
            if [[ $localnode == $ip || $local_ip == $ip ]];then
            echo "local node stop logana service"
            sh $return_base/bin/logana.sh stop
            else
            echo "$ip:"
            ssh $ip "sh $return_base/bin/logana.sh stop"
            fi
        done
        ;;
        "alarm")
        for ip in $monlist
        do
            if [[ $localnode == $ip || $local_ip == $ip ]];then
            echo "local node stop Monitor alarm service"
            sh $return_base/bin/monitor-alarm-center.sh stop
            else
            echo "$ip:"
            ssh $ip "sh $return_base/bin/monitor-alarm-center.sh stop"
            fi
        done
        ;;
        *)
        print_usage
        exit 1
        ;;
    esac
}

status()
{
    echo "############################################################"
    echo "                   status return service                    "
    echo "############################################################"
    case $1 in
        "dbconn")
        for ip in $collist
        do
            if [ $localnode == $ip ];then
            echo "local node dbconn status"
            collps=`ps -ef|grep -i db-conn.jar|grep -v grep|awk '{print $2}'`
            else
            echo "$ip:"
            collps=`ssh $ip "ps -ef|grep \"db-conn.jar\"|grep -v \"grep\"|awk '{print \\\$2}'"`
            fi
            if [ "$collps" ];then
                echo "DbConn Service is running(PID:$collps)!"
            else
                echo "DbConn Service is not running!"
            fi
        done
        ;;
        "collector")
        for ip in $collist
        do
            if [ $localnode == $ip ];then
            echo "local node collector status"
            collps=`ps -ef|grep -i Collector.jar|grep -v grep|awk '{print $2}'`
            else
            echo "$ip:"
            collps=`ssh $ip "ps -ef|grep \"Collector.jar\"|grep -v \"grep\"|awk '{print \\\$2}'"`
            fi
            if [ "$collps" ];then
                echo "Collector Service is running(PID:$collps)!"
            else
                echo "Collector Service is not running!"
            fi
        done
        ;;
        "monitor")
        for ip in $monlist
        do
            if [ $localnode == $ip ];then
            echo "local node monitor status"
            monps=`ps -ef|grep -i Monitor.jar|grep -v grep|awk '{print $2}'`
            else
            echo "$ip:"
            monps=`ssh $ip "ps -ef|grep \"Monitor.jar\"|grep -v \"grep\"|awk '{print \\\$2}'"`
            fi
            if [ "$monps" ];then
                echo "Monitor Service is running(PID:$monps)!"
            else
                echo "Monitor Service is not running!"
            fi
        done
        ;;
        "logana")
        for ip in $loglist
        do
            if [ $localnode == $ip ];then
            echo "local node logana status"
            lanps=`ps -ef|grep -i LogAna.jar|grep -v grep|awk '{print $2}'`
            else
            echo "$ip:"
            lanps=`ssh $ip "ps -ef|grep \"LogAna.jar\"|grep -v \"grep\"|awk '{print \\\$2}'"`
            fi
            if [ "$lanps" ];then
                echo "LogAna Service is running(PID:$lanps)!"
            else
                echo "LogAna Service is not running!"
            fi
        done
        ;;
        "alarm")
        for ip in $loglist
        do
            if [ $localnode == $ip ];then
            echo "local node Monitor alarm status"
            lanps=`ps -ef|grep -i monitor-alarm-center.jar|grep -v grep|awk '{print $2}'`
            else
            echo "$ip:"
            lanps=`ssh $ip "ps -ef|grep \"monitor-alarm-center.jar\"|grep -v \"grep\"|awk '{print \\\$2}'"`
            fi
            if [ "$lanps" ];then
                echo "Monitor alarm Service is running(PID:$lanps)!"
            else
                echo "Monitor alarm Service is not running!"
            fi
        done
        ;; 
        *)
        print_usage
        exit 1
        ;;
    esac
}

checkZk()
{
    sh $return_base/bin/zkInfoTool.sh
}

if [ -z $DBAIOps_oper_dir ];then
    echo "DBAIOps安装目录不存在！"
    exit 1
fi

if [ ! -d $return_base ];then
    echo "return采集、监控程序不存在！"
    exit 1
fi
if [ ! -f $CONF/role.cfg ];then
    echo "There is no role.cfg in $CONF"
    exit 1
else 
    . $CONF/role.cfg
fi

logl=`awk -F '=' '/^DS_Logana/ {print $2}' $CONF/role.cfg`
loglnum=`echo $logl | tr ',' '\n' |wc -l`
monl=`awk -F '=' '/^DS_Monitor/ {print $2}' $CONF/role.cfg`
monlnum=`echo $monl | tr ',' '\n' |wc -l`
coll=`awk -F '=' '/^DS_Collector/ {print $2}' $CONF/role.cfg`
collnum=`echo $coll | tr ',' '\n' |wc -l`

if [ $loglnum -gt 1 ];then
    echo "LogAna服务只支持一个节点!"
    exit 1
fi
if [ $monlnum -gt 1 ];then
    echo "Monitor服务只支持一个节点!"
    exit 1
fi

loglist=`echo $logl | tr ',' '\n'`
monlist=`echo $monl | tr ',' '\n'`
collist=`echo $coll | tr ',' '\n'`

if [ -z $3 ];then
    loglist=`echo $logl | tr ',' '\n'`
    monlist=`echo $monl | tr ',' '\n'`
    collist=`echo $coll | tr ',' '\n'`
else
    loglist=$3
    monlist=$3
    collist=$3
fi

cmd=$1
shift
case $cmd in
        ("-start")
                start $@
        ;;
        ("-stop")
                stop $@
        ;;
        ("-kill")
                kill $@
        ;;
        ("-status")
                status $@
        ;;
        ("-zkinfo")
                checkZk
        ;;
        (*)
                print_usage
                exit 1
        ;;
esac

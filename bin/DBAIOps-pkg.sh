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
print_usage(){
  echo "Usage: DBAIOps Package installation"
  echo "  -install                      install DBAIOps Package"
}

install()
{
    echo "############################################################"
    echo "                   install DBAIOps                              "
    echo "############################################################"
    for ip in $ds_hosts
    do   
        if [ x$ip == x`hostname` ]||[ x$ip == x`hostname -i|awk '{print $1}'` ];then
            echo "Local Node"
        else
            echo "$ip:"
            ssh $ip "if [ ! -d $DBAIOps_HOME ];then mkdir -p $DBAIOps_HOME;fi"
            set +e
            scp -r $DBAIOps_HOME/* $ip:$DBAIOps_HOME > /dev/null 2>&1
            set -e
            ssh $ip "if [ ! -d $DBAIOps_oper_dir ];then ln -s $DBAIOps_HOME $DBAIOps_oper_dir;fi"
        fi
    done
    echo "Configurations,DBAIOps package deployed Successful!"
    sh $bin/DBAIOps-java.sh -install
    if [ $? -eq 1 ];then
        echo "Java install may not successful,please check"
        exit 1
    fi
}


DBAIOps_HOME=`awk -F '=' '/^DS_BASE_LOCALTION/ {print $2}' $DBAIOps_oper_dir/role.cfg`
CONF=$DBAIOps_HOME
if [ ! -f $CONF/role.cfg ];then
    echo "There is no role.cfg in $CONF"
    exit 1
else 
    . $CONF/role.cfg
fi

ds_hosts=$(awk -F '=' '/^DS_Web|^DS_Collector|^DS_Monitor|^DS_Logana|^DS_Fstask|^DS_Zookeeper|^DS_Other_Executor|^DS_Redis/ {print $2}' $CONF/role.cfg | tr -s '\n' | tr ',' '\n' |sort -u)
ds_web=`awk -F '=' '/^DS_Web/ {print $2}' $CONF/role.cfg`
os_release=`cat /etc/os-release|grep "^ID"|awk -F "=" '{print $2}'`
cmd=$1

case $cmd in
    ("-install")
        install $ds_hosts
        ;;
    (*)
        print_usage
        ;;
esac

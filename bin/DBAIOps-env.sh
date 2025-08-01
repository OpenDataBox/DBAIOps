#!/bin/bash
#
#
#
#set -e
bin=`dirname "${BASH_SOURCE-$0}"`
bin=`cd "$bin"; pwd`
ROOT=`cd $bin;cd ..;pwd`
DBAIOps_HOME="/usr/software"
DBAIOps_oper_dir=/usr/software
CONF=$DBAIOps_HOME
localnode=`hostname`

print_usage(){
  echo "Usage: DBAIOps Env Check Script"
  echo "< -check >"
  echo "  -check                       check DBAIOps install Environment"
}

check()
{
    echo "###########################################################"
    echo "                  check DBAIOps environment                 "
    echo "###########################################################"
    echo "==================Step 1 :check iptables==================="
    for ip in $ds_hosts
    do
        if [ $localnode == $ip ];then
        echo "local node enviroment check"
        else
        echo "$ip:"
        fi
        
        #set +e
        if [ $localnode == $ip ];then  
            firewall=`systemctl status firewalld.service`
        else
            firewall=`ssh $ip "systemctl status firewalld.service"`
        fi
        if [ $? -eq 3 ]; then
            echo "firewalld检查通过"
        else
            echo "firewalld检查失败"
            unset firewall
        fi
       # set -e
    done
    echo -e "\n"

    echo "==================Step 2 :check selinux===================="
    for ip in $ds_hosts
    do	
	if [ -f /etc/redhat-release ];then 
            if [ $localnode == $ip ];then
            echo "local node check selinux"
            sed -i 's/^SELINUX=.*$/SELINUX=disabled/g' /etc/selinux/config;
            #set +e
            setenforce 0 > /dev/null 2>&1
            #set -e
            else
            echo "$ip:"
            ssh $ip "sed -i 's/^SELINUX=.*$/SELINUX=disabled/g' /etc/selinux/config; setenforce 0 > /dev/null 2>&1"
            fi
        fi  
        echo "selinux检查通过"
    done
    echo -e "\n"
}

check_redhat_rpm(){
    echo "==================Step 3 :check os package================="
    for ip in $ds_hosts
    do
        if [ $localnode == $ip ];then
        echo "local node check os package"
        rpm -q gcc >/dev/null 2>&1
        if [ ! $? -eq 0 ];then
            echo 'gcc系统包未安装';
            exit 1;
        fi
        #rpm -q expect >/dev/null 2>&1
        #if [ ! $? -eq 0 ];then
        #    echo 'expect系统包未安装';
        #    exit 1;
        #fi;
        rpm -q zlib-devel >/dev/null 2>&1
        if [ ! $? -eq 0 ];then
            echo 'zlib-devel系统包未安装';
            exit 1;
        fi;
        if [ -f /etc/redhat-release ];then
        rpm -q libffi-devel >/dev/null 2>&1
        else
        rpm -q rpm -q libffi48-devel > /dev/null 2>&1
        fi
        if [ ! $? -eq 0 ];then
            echo 'libffi-devel系统包未安装';
            exit 1;
        fi;
        if [ -f /etc/redhat-release ];then
        rpm -q openssl-devel >/dev/null 2>&1
        else
        rpm -q libopenssl-devel > /dev/null 2>&1
        fi
        if [ ! $? -eq 0 ];then
            echo 'openssl-devel系统包未安装';
            exit 1;
        fi;
        rpm -q readline-devel >/dev/null 2>&1
        if [ ! $? -eq 0 ];then
            echo 'readline-level系统包未安装';
            exit 1;
        fi;
        rpm -q unzip >/dev/null 2>&1
        if [ ! $? -eq 0 ];then
            echo 'unzip系统包未安装';exit 1;
        fi;
        rpm -q bzip2 >/dev/null 2>&1
        if [ ! $? -eq 0 ];then
            echo 'bzip2系统包未安装';exit 1;
        fi;
        echo "$ip OS Package检查通过"
        else
        echo "$ip:"
        ssh $ip "rpm -q gcc >/dev/null 2>&1;"
        if [ ! $? -eq 0 ];then 
            echo 'gcc系统包未安装';
            exit 1;
        fi
        #ssh $ip "rpm -q expect >/dev/null 2>&1;"
        #if [ ! $? -eq 0 ];then 
        #    echo 'expect系统包未安装';
        #    exit 1;
        #fi;
        ssh $ip "rpm -q zlib-devel >/dev/null 2>&1;"
        if [ ! $? -eq 0 ];then 
            echo 'zlib-devel系统包未安装'; 
	    exit 1; 
        fi;
        ssh $ip "rpm -q libffi-devel >/dev/null 2>&1;"
        if [ ! $? -eq 0 ];then 
            echo 'libffi-devel系统包未安装';
            exit 1;
        fi;
        ssh $ip "rpm -q openssl-devel >/dev/null 2>&1;"
        if [ ! $? -eq 0 ];then 
            echo 'openssl-devel系统包未安装';
            exit 1;
        fi;
        ssh $ip "rpm -q readline-devel >/dev/null 2>&1;"
        if [ ! $? -eq 0 ];then 
            echo 'readline-level系统包未安装';
            exit 1;
        fi;
        ssh $ip "rpm -q unzip >/dev/null 2>&1;"
        if [ ! $? -eq 0 ];then 
            echo 'unzip系统包未安装';exit 1;
        fi;
        ssh $ip "rpm -q bzip2 >/dev/null 2>&1;"
        if [ ! $? -eq 0 ];then 
            echo 'bzip2系统包未安装';exit 1;
        fi;
        echo "$ip OS Package检查通过"
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

ds_hosts=$(awk -F '=' '/^DS_Web|^DS_Collector|^DS_Monitor|^DS_Logana|^DS_Fstask|^DS_Other_Executor|^DS_Zookeeper|^DS_Redis/ {print $2}' $CONF/role.cfg | tr -s '\n' | tr ',' '\n' |sort -u)
os_release=`cat /etc/os-release|grep "^ID"|awk -F "=" '{print $2}'`
case $1 in
        "-check")
                check $ds_hosts
	#	if [ "$(echo $os_release|grep -i uos)" == "" ];then
	#	    check_redhat_rpm $ds_hosts
#		fi
        ;;
        *)
                print_usage
                exit 1
        ;;
esac

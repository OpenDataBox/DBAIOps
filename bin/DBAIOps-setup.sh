#!/bin/bash
bin=/usr/software/bin
CONF=/usr/software
print_usage(){
    echo "Usage: DBAIOps setup script"
    echo "./DBAIOps-setup.sh 60.60.60.57"
}

DBAIOps_log=/usr/software/bin/logs/DBAIOps.log

check_ip(){
    IP=$1
    VALID_CHECK=$(echo $IP|awk -F. '$1<=255 && $2<=255 && $3<=255 && $4<=255 {print "yes"}')
    #echo $VALID_CHECK
    if echo $IP|grep -E "^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$">/dev/null; then
        if [[ $VALID_CHECK == "yes" ]]; then
            echo "$IP available."
        else
            echo "$IP not available!"
        print_usage
        exit 1
        fi
    else
        echo "请提供服务器IP地址(Please provide the server address)"
    print_usage
        exit 1
    fi
}

if [ ! -f /usr/software/bin/logs/os_type.txt ];then
    echo "please execute DBAIOps-system-package.sh first!"
    exit 1
fi

ip=$1

if [ -z $1 ];then
    echo "请提供服务器IP地址(Please provide the server address)"
    print_usage
    exit 1
fi

check_ip $ip


setup_selinux(){
    echo "......"
    sed -i 's/^SELINUX=.*$/SELINUX=disabled/g' /etc/selinux/config
    setenforce 0 > /dev/null 2>&1
}

setup_firewall(){
    echo "......"
    systemctl stop firewalld
    systemctl disable firewalld
}

setup_characterset(){
    echo "export LANG=en_US.UTF-8" > /etc/profile.d/lang.sh
    source /etc/profile.d/lang.sh
}

setup_hostname(){
    echo "......"
    hostnamectl set-hostname DBAIOps
}

setup_hosts(){
    echo "......"
    \cp /etc/hosts /etc/hosts.bak
    sed -i "s/.*DBAIOps/$ip DBAIOps/g" /usr/software/hosts
    \cp /usr/software/hosts /etc
}

setup_cfg(){
    echo "......"
    sed -i "s/DSPG_Node=.*/DSPG_Node=$ip/g" /usr/software/role.cfg
    \cp /usr/software/pg.sh /etc/profile.d
    \cp /usr/software/java.sh /etc/profile.d
    \cp /usr/software/python3.sh /etc/profile.d
    \cp /usr/software/orainstclient.sh /etc/profile.d
    chmod 644 /etc/profile.d/pg.sh
    chmod 644 /etc/profile.d/java.sh
    chmod 644 /etc/profile.d/python3.sh
    chmod 644 /etc/profile.d/orainstclient.sh
    source /etc/profile.d/java.sh
    source /etc/profile.d/python3.sh
    $bin/DBAIOps.sh -genecfg
    if [ -f /usr/share/crypto-policies/DEFAULT/opensslcnf.txt ];then
    sed -i "s/MinProtocol = TLSv1.2/MinProtocol = TLSv1.1/g" /usr/share/crypto-policies/DEFAULT/opensslcnf.txt
    fi
}


update_libpq(){
    rm -rf /lib64/libpq.so.5.16
    rm -rf /lib64/libpq.so.5
    cp /usr/software/pgsql/lib/libpq.so.5.16 /lib64
    ln -s /lib64/libpq.so.5.16 /lib64/libpq.so.5
}

setup_pg(){
    useradd postgres -m
    chown -R root:root /usr/software/pgsql
    chown -R postgres:root /usr/software/pgsql/data
    chmod -R 755 /usr/software/pgsql
    chmod -R 700 /usr/software/pgsql/data
    hostmem=`cat /proc/meminfo|grep MemTotal|awk '{print $2}'`
    sharedmem=$((hostmem/4096))
    sed -i "s/shared_buffers = .*MB/shared_buffers = ${sharedmem}MB/g" /usr/software/pgsql/data/postgresql.conf
    su - postgres -c "/usr/software/pgsql/bin/pg_ctl start -D /usr/software/pgsql/data"

}

check_pg(){
    flag=`ps -ef|grep "/usr/software/pgsql/bin/postgres"`
    if [ -z "$flag" ];then
        echo "数据库启动失败，请检查/usr/software/pgsql/data/pg_log目录下的日志，确认数据库启动失败的原因."
        exit 1
    fi
}


install_env_check(){
    flag=`ps -ef|grep -i "Collector.jar"|grep -v grep`
    if [ ! -z "$flag" ];then
        $bin/DBAIOps-return.sh -stop collector
    fi
    echo "Collector组件未运行，检查通过"
    flag=`ps -ef|grep -i "Monitor.jar"|grep -v grep`
    if [ ! -z "$flag" ];then
        $bin/DBAIOps-return.sh -stop monitor
    fi
    echo "Monitor组件未运行，检查通过"
    flag=`ps -ef|grep -i "LogAna.jar"|grep -v grep`
    if [ ! -z "$flag" ];then
        $bin/DBAIOps-return.sh -stop logana
    fi
    echo "LogAna组件未运行，检查通过"
    flag=`ps -ef|grep -i "/usr/software/neo4j"|grep -v grep`
    if [ ! -z "$flag" ];then
        $bin/DBAIOps-neo4j.sh -stop
    fi
    echo "neo4j组件未运行，检查通过"
    flag=`ps -ef|grep -i "/usr/software/fstaskpkg"|grep -v grep`
    if [ ! -z "$flag" ];then
        $bin/DBAIOps-fstask.sh -stop
    fi

    flag=`ps -ef|grep -i "/usr/software/redis"|grep -v grep`
    if [ ! -z "$flag" ];then
        if [ -z $redis_flag ];then
            sh $bin/DBAIOps-redis.sh -stop
              if [ $? -eq 1 ];then
                  echo "Redis stop may not successful,please check"
                  exit 1
            fi
        else
            sh $bin/DBAIOps-redis-single.sh -stop
            if [ $? -eq 1 ];then
                   echo "Redis stop may not successful,please check"
                exit 1
            fi
        fi
    fi
    echo "redis组件未运行，检查通过"
    flag=`ps -ef|grep -i "/usr/software/zookeeper"|grep -v grep`
    if [ ! -z "$flag" ];then
        $bin/DBAIOps-zookeeper.sh -stop
    if [ $? -eq 1 ];then
        ps -ef|grep '/usr/software/zookeeper'|grep -v grep|awk '{print $2}'|xargs kill -9
    fi
    fi
    echo "zookeeper组件未运行，检查通过"
    flag=`ps -ef|grep -i "/usr/software/webserver"|grep -v grep`
    if [ ! -z "$flag" ];then
        $bin/DBAIOps-web.sh -stop
    fi
    echo "webserver组件未运行，检查通过"
    flag=`ps -ef|grep -i "/usr/software/pgsql"|grep -v grep`
    if [ ! -z "$flag" ];then
        su - postgres -c "/usr/software/pgsql/bin/pg_ctl stop"
        if [ $? -ne 0 ];then
            echo "Redis stop may not successful,please check"
            exit 1
        fi
    fi
    echo "postgresql组件未运行，检查通过"
    sh $bin/DBAIOps-zookeeper.sh -clean
    if [ $? -eq 1 ];then
        echo "Zookeeper clean may not successful,please check"
        exit 1
    fi

    if [ -z $redis_flag ];then
        sh $bin/DBAIOps-redis.sh -clean
        if [ $? -eq 1 ];then
            echo "Redis clean may not successful,please check"
            exit 1
        fi
    else
        sh $bin/DBAIOps-redis-single.sh -clean
        if [ $? -eq 1 ];then
            echo "Redis clean may not successful,please check"
            exit 1
        fi
    fi
    sh $bin/DBAIOps-neo4j.sh -clean
    if [ $? -eq 1 ];then
        echo "neo4j clean may not successful,please check"
        exit 1
    fi

    sh $bin/DBAIOps-fstask.sh -clean
    if [ $? -eq 1 ];then
        echo "Fstask clean may not successful,please check"
        exit 1
    fi
}
echo -e "\e[31m 注意：安装本程序会关闭selinux，禁用服务器防火墙，修改/etc/hosts文件，修改主机名，修改服务器字符集，请一定要使用单独的（不和其他程序共用）服务器进行安装！！! \e[0m"
echo -e "\e[31m (Note：Installing this program will close selinux, disable the server firewall, modify the /etc/hosts file, modify the host name, modify the server character set, please be sure to use a separate (not shared with other programs) server for installation! ! ! )\e[0m"
read -p "是否继续[y/n](Whether to continue [y/n]):" go
if [ "$go" == "y" -o "$go" == "Y" ];then
    echo "" > $DBAIOps_log
    echo "安装详情日志请查看:$DBAIOps_log" | tee -a $DBAIOps_log
    echo "修改字符集" | tee -a $DBAIOps_log
    setup_characterset >> $DBAIOps_log 2>&1
    echo "字符集修改成功" | tee -a $DBAIOps_log
    echo -e "\n" | tee -a $DBAIOps_log
    echo "禁用selinux" | tee -a $DBAIOps_log
    setup_selinux >> $DBAIOps_log 2>&1
    echo "禁用selinux成功" | tee -a $DBAIOps_log
    echo -e "\n" | tee -a $DBAIOps_log
    echo "禁用防火墙" | tee -a $DBAIOps_log
    setup_firewall >> $DBAIOps_log 2>&1
    echo "禁用防火墙成功" | tee -a $DBAIOps_log
    echo -e "\n" | tee -a $DBAIOps_log
    echo "修改主机名" | tee -a $DBAIOps_log
    setup_hostname >> $DBAIOps_log 2>&1
    echo "修改主机名成功" | tee -a $DBAIOps_log
    echo -e "\n" | tee -a $DBAIOps_log
    echo "修改/etc/hosts" | tee -a $DBAIOps_log
    setup_hosts >> $DBAIOps_log 2>&1
    echo "修改/etc/hsots成功" | tee -a $DBAIOps_log
    echo -e "\n" | tee -a $DBAIOps_log
    redis_flag=`grep ^DFC_REDIS_SINGLENODE $CONF/DBAIOps.cfg`
    echo "修改DBAIOps配置文件" | tee -a $DBAIOps_log
    setup_cfg >> $DBAIOps_log 2>&1
    echo "修改DBAIOps配置文件成功" | tee -a $DBAIOps_log
    echo -e "\n" | tee -a $DBAIOps_log
    echo "更新libpq" | tee -a $DBAIOps_log
    update_libpq >> $DBAIOps_log
    echo "更新libpq成功" | tee -a $DBAIOps_log
    echo -e "\n" | tee -a $DBAIOps_log
    echo "安装前检查" | tee -a $DBAIOps_log
    install_env_check >> $DBAIOps_log 2>&1
    echo "安装前检查成功" | tee -a $DBAIOps_log
    echo -e "\n" | tee -a $DBAIOps_log
    echo "启动数据库" | tee -a $DBAIOps_log
    setup_pg >> $DBAIOps_log 2>&1
    check_pg 2>&1| tee -a $DBAIOps_log
    echo "数据库启动成功" | tee -a $DBAIOps_log
    echo -e "\n" | tee -a $DBAIOps_log
    echo "开始安装DBAIOps" | tee -a $DBAIOps_log
    sh /usr/software/bin/DBAIOps.sh -install free >> $DBAIOps_log 2>&1
    if [ $? -eq 1 ];then
        echo "DBAIOps安装失败" | tee -a $DBAIOps_log
        exit 1
    fi
    echo "DBAIOps安装成功" | tee -a $DBAIOps_log
    echo -e "\n" | tee -a $DBAIOps_log
    echo "开始启动DBAIOps" | tee -a $DBAIOps_log
    sh /usr/software/bin/DBAIOps.sh -start >> $DBAIOps_log 2>&1
    if [ $? -eq 1 ];then
        echo "DBAIOps启动失败" | tee -a $DBAIOps_log
        exit 1
    fi
    echo "DBAIOps已启动成功,请访问:"
    echo "$ip:18081/DBAIOps"
    echo "登陆用户名/密码为：administrator/p@ssw0rd#DFC_2018" | tee -a $DBAIOps_log
else
    echo "exit"
    exit 1
fi
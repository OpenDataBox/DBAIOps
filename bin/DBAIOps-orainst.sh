#!/bin/bash
#
#
#
bin=`dirname "${BASH_SOURCE-$0}"`
bin=`cd "$bin"; pwd`
ROOT=`cd $bin;cd ..;pwd`
DBAIOps_HOME="/usr/software"
DBAIOps_oper_dir=/usr/software
ora_instcli_home=$DBAIOps_oper_dir/python3/instantclient_21_3
CONF=$DBAIOps_HOME
localnode=`hostname`
cpu_version=`uname -a|grep aarch64`
set -e
if [ -z "$cpu_version" ];then
    ora_instcli_home=$DBAIOps_oper_dir/python3/instantclient_21_3
else
    ora_instcli_home=$DBAIOps_oper_dir/python3/instantclient_19_10
fi


# 获取主脚本中的语言设置
if [ -z "$LANGUAGE" ]; then
    LANGUAGE="en"  # 默认英文
fi


print_usage(){
  echo "Usage: DBAIOps oracle instantclient manage script"
  echo "< -install >"
  echo "  -install                       install oracle instantclient"
  echo "  -clean                         clean oracle instantclient"
}

install() {
    # 根据语言设置定义提示信息
    if [ "$LANGUAGE" = "cn" ]; then
        MSG_INSTALL_TITLE="正在安装 Oracle Instantclient"
        MSG_LOCAL_NODE="本地节点安装 Oracle Instantclient"
        MSG_REMOTE_NODE="远程节点 $ip:"
        MSG_INSTALL_SUCCESS="Oracle Instantclient 安装成功！"
    else
        MSG_INSTALL_TITLE="Installing Oracle Instantclient"
        MSG_LOCAL_NODE="Local node installing Oracle Instantclient"
        MSG_REMOTE_NODE="Remote node $ip:"
        MSG_INSTALL_SUCCESS="Oracle Instantclient installation succeeded!"
    fi

    echo "############################################################"
    echo "               $MSG_INSTALL_TITLE                           "
    echo "############################################################"

    for ip in $ds_hosts; do
        if [ "$localnode" == "$ip" ]; then
            echo "$MSG_LOCAL_NODE"
            cd "$DBAIOps_oper_dir/python3" || { echo "Failed to cd to $DBAIOps_oper_dir/python3"; exit 1; }

            # 清理旧目录
            if [ -d "$ora_instcli_home" ]; then
                rm -rf "$ora_instcli_home"
            fi

            # 根据 CPU 版本选择安装包
            if [ -z "$cpu_version" ]; then
                unzip -o "$DBAIOps_oper_dir/python3/instantclient-basic-linux.x64-21.3.0.0.0.zip" > /dev/null
                unzip -o "$DBAIOps_oper_dir/python3/instantclient-sqlplus-linux.x64-21.3.0.0.0.zip" > /dev/null
            else
                unzip -o "$DBAIOps_oper_dir/python3/instantclient-basic-linux.arm64-19.10.0.0.0dbru.zip" > /dev/null
                unzip -o "$DBAIOps_oper_dir/python3/instantclient-sqlplus-linux.arm64-19.10.0.0.0dbru.zip" > /dev/null
            fi

            # 配置环境变量
            echo "$ora_instcli_home" > /etc/ld.so.conf.d/oracle-instantclient.conf
            ldconfig > /dev/null
            echo "export LD_LIBRARY_PATH=$ora_instcli_home:\$LD_LIBRARY_PATH" > /etc/profile.d/orainstclient.sh
            echo "export PATH=$ora_instcli_home:\$PATH" >> /etc/profile.d/orainstclient.sh
            chmod 644 /etc/profile.d/orainstclient.sh
        else
            echo "$MSG_REMOTE_NODE"
            if [ -z "$cpu_version" ]; then
                ssh "$ip" "cd $DBAIOps_oper_dir/python3; if [ -d $ora_instcli_home ]; then rm -rf $ora_instcli_home; fi; unzip -o $DBAIOps_oper_dir/python3/instantclient-basic-linux.x64-21.3.0.0.0.zip > /dev/null; unzip -o $DBAIOps_oper_dir/python3/instantclient-sqlplus-linux.x64-21.3.0.0.0.zip > /dev/null"
            else
                ssh "$ip" "cd $DBAIOps_oper_dir/python3; if [ -d $ora_instcli_home ]; then rm -rf $ora_instcli_home; fi; unzip -o $DBAIOps_oper_dir/python3/instantclient-basic-linux.arm64-19.10.0.0.0dbru.zip > /dev/null; unzip -o $DBAIOps_oper_dir/python3/instantclient-sqlplus-linux.arm64-19.10.0.0.0dbru.zip > /dev/null"
            fi

            # 配置远程节点的环境变量
            ssh "$ip" "echo $ora_instcli_home > /etc/ld.so.conf.d/oracle-instantclient.conf; ldconfig > /dev/null"
            ssh "$ip" "echo \"export LD_LIBRARY_PATH=$ora_instcli_home:\\\$LD_LIBRARY_PATH\" > /etc/profile.d/orainstclient.sh"
            ssh "$ip" "chmod 644 /etc/profile.d/orainstclient.sh"
        fi
    done

    echo "$MSG_INSTALL_SUCCESS"
}

clean()
{
    echo "############################################################"
    echo "                clean oracle instantclient                  "
    echo "############################################################"
    for ip in $ds_hosts
    do
        if [ $localnode == $ip ];then
        echo "local node clean oracle instantclient"
        if [ -d $ora_instcli_home ];then rm -rf $ora_instcli_home;fi;
        if [ -f /etc/ld.so.conf.d/oracle-instantclient.conf ];then rm -rf /etc/ld.so.conf.d/oracle-instantclient.conf;fi;
        if [ -f /etc/profile.d/orainstclient.sh ];then rm -rf /etc/profile.d/orainstclient.sh;fi
        else
        echo "$ip:"
        ssh $ip "if [ -d $ora_instcli_home ];then rm -rf $ora_instcli_home;fi;if [ -f /etc/ld.so.conf.d/oracle-instantclient.conf ];then rm -rf /etc/ld.so.conf.d/oracle-instantclient.conf;fi;if [ -f /etc/profile.d/orainstclient.sh ];then rm -rf /etc/profile.d/orainstclient.sh;fi"
        fi
    done
    echo "Oracle Instantclient Clean Successed!"
}

if [ -z $DBAIOps_oper_dir ];then
    echo "DBAIOps安装目录不存在！"
    exit 1
fi

#if [ ! -f $DBAIOps_oper_dir/python3/instantclient-basic-linux.x64-12.2.0.1.0.zip ];then
#    echo "oracle instantclient安装文件不存在！"
#    exit 1
#fi

if [ ! -f $CONF/role.cfg ];then
    echo "There is no role.cfg in $CONF"
    exit 1
else 
    . $CONF/role.cfg
fi

ds_hosts=$(awk -F '=' '/^DS_Web|^DS_Collector|^DS_Monitor|^DS_Logana|^DS_Fstask|^DS_Other_Executor|^DS_Zookeeper|^DS_Redis/ {print $2}' $CONF/role.cfg | tr -s '\n' | tr ',' '\n' |sort -u)

case $1 in
        "-install")
                install $ds_hosts
        ;;
        "-clean")
                clean $ds_hosts
        ;;
        *)
                print_usage
                exit 1
        ;;
esac

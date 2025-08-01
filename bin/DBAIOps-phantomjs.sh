#!/bin/bash
#set -e
bin=`dirname "${BASH_SOURCE-$0}"`
bin=`cd "$bin"; pwd`
ROOT=`cd $bin;cd ..;pwd`
DBAIOps_HOME="/usr/software"
DBAIOps_oper_dir=/usr/software
phan_conf_dir=$DBAIOps_oper_dir/phantomjsconf
CONF=$DBAIOps_HOME
localnode=`hostname`

# 获取主脚本中的语言设置
if [ -z "$LANGUAGE" ]; then
    LANGUAGE="en"  # 默认英文
fi

print_usage(){
    echo "Usage: DBAIOps Phantomjs install Script"
    echo "< -install >"
    echo "  -install  install Phantomjs Env"
}

install()
{
    echo "###########################################################"
    echo "                     install Phantomjs                     "
    echo "###########################################################"
    for ip in $weblist
    do
        if [ $localnode == $ip ];then
        echo "local node install Phantomjs"
        cd $DBAIOps_oper_dir
        if [ ! -f phantomjs-2.1.1-linux-x86_64.tar.bz2 ];then echo 'phantomjs-2.1.1-linux-x86_64.tar.bz2安装包不存在'; exit 1;fi;
        if [ -d $DBAIOps_oper_dir/phantomjs-2.1.1-linux-x86_64 ];then rm -rf $DBAIOps_oper_dir/phantomjs-2.1.1-linux-x86_64;fi;
        if [ -d $DBAIOps_oper_dir/phantomjs ];then rm -rf $DBAIOps_oper_dir/phantomjs;fi;
        tar -jxvf $DBAIOps_oper_dir/phantomjs-2.1.1-linux-x86_64.tar.bz2 > /dev/null 2>&1;mv $DBAIOps_oper_dir/phantomjs-2.1.1-linux-x86_64 $DBAIOps_oper_dir/phantomjs;ln -s -f /usr/software/phantomjs/bin/phantomjs /usr/bin/;
        \cp -r $phan_conf_dir/cn_fonts $DBAIOps_oper_dir;ln -s -f /usr/software/cn_fonts /usr/share/fonts/windowsFonts;mkfontscale > /dev/null;mkfontdir > /dev/null;fc-cache -fv > /dev/null
        \cp $phan_conf_dir/phantomjs.properties /usr/software/webserver/conf
        else
        echo "$ip:"
        ssh $ip "cd $DBAIOps_oper_dir;if [ ! -f phantomjs-2.1.1-linux-x86_64.tar.bz2 ];then echo 'phantomjs-2.1.1-linux-x86_64.tar.bz2安装包不存在'; exit 1;fi;if [ -d $DBAIOps_oper_dir/phantomjs-2.1.1-linux-x86_64 ];then rm -rf $DBAIOps_oper_dir/phantomjs-2.1.1-linux-x86_64;fi;if [ -d $DBAIOps_oper_dir/phantomjs ];then rm -rf $DBAIOps_oper_dir/phantomjs;fi;tar -jxvf $DBAIOps_oper_dir/phantomjs-2.1.1-linux-x86_64.tar.bz2 > /dev/null 2>&1;mv $DBAIOps_oper_dir/phantomjs-2.1.1-linux-x86_64 $DBAIOps_oper_dir/phantomjs;ln -s -f /usr/software/phantomjs/bin/phantomjs /usr/bin/;cp -r $phan_conf_dir/cn_fonts $DBAIOps_oper_dir;ln -s -f /usr/software/cn_fonts /usr/share/fonts/windowsFonts;mkfontscale > /dev/null;mkfontdir > /dev/null;fc-cache -fv > /dev/null;cp $phan_conf_dir/phantomjs.properties /usr/software/webserver/conf"
        fi
    done
    
    echo "phantomjs安装完成"
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

if [ -z $2 ];then
    weblist=`echo $webl | tr ',' '\n'`
else
    weblist=$2
fi

case $1 in
        "-install")
                install $weblist
        ;;
        *)
                print_usage
                exit 1
        ;;
esac

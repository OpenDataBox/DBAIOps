#!/bin/bash
#
#
#
bin=`dirname "${BASH_SOURCE-$0}"`
bin=`cd "$bin"; pwd`
ROOT=`cd $bin;cd ..;pwd`
DBAIOps_HOME="/usr/software"
DBAIOps_oper_dir=/usr/software
CONF=$DBAIOps_HOME
localnode=`hostname`
localnodeip=`hostname -i`
cpu_version=`uname -a|grep aarch64`
python3_home=$DBAIOps_oper_dir/python3
os_type_file=$DBAIOps_oper_dir/bin/logs/os_type.txt

set -e
print_usage(){
    echo "Usage: DBAIOps system package installation script"
    echo "< -install >"
    echo "  -install                install system package"
    echo "current support os type as below:"
    echo "redhat
centos
uos
kylinV4
kylinV10
suse"
    echo "please chose the above os type!"
}

install()
{
    echo "############################################################"
    echo "                      install system package                "
    echo "############################################################"
    os_num=$1
    case $os_num in
        "1")
            install_yum
            echo "redhat" > $os_type_file
        ;;
        "2")
            install_yum
            echo "centos" > $os_type_file
        ;;
        "3")
            install_yum
            echo "uos" > $os_type_file
        ;;
        "4")
            install_apt
            echo "kylinV4" > $os_type_file
        ;;
        "5")
	    install_yum
	    echo "kylinV10" > $os_type_file
	;;
        "6")
            install_zypper
            echo "suse" > $os_type_file
        ;;
        *)
            print_usage
            exit 1
        ;;
    esac
    echo "System Package install Successed!"
}

install_yum_free(){
echo "local node install system package"
##yum install package
yum -y install vim
yum -y install net-tools
yum -y install gcc
yum -y install zlib-devel
yum -y install libaio
yum -y install lsof
yum -y install sysstat
yum -y install xz-devel
yum -y install gcc-c++
yum -y install rng-tools
yum -y install dmidecode
yum -y install kernel-headers
yum -y install mtr
systemctl start rngd
systemctl enable rngd
yum -y install unixODBC
yum -y install unixODBC-devel
yum -y install gcc-gfortran
yum -y install openssl*
yum -y install wget
yum -y install fontconfig
yum -y install mariadb-libs
yum -y install mariadb
set +e
#yum -y install bitmap-fonts
#yum -y groupinstall "X Window System"
yum -y install bzip2
yum -y install bitmap-fonts-cjk
yum -y install libX11-devel
yum -y install libxml2-devel
yum -y install e2fsprogs-devel
yum -y install freetds
set -e
yum -y install mkfontscale
yum -y install libjpeg-turbo-devel
yum -y install libxml2*
yum -y install freetype*
yum -y install libpng*
yum -y install libXext-devel
yum -y install libicu-devel
yum -y install libXt
yum -y install libxslt-devel
yum -y install make
}

install_yum(){
for ip in $ds_hosts
do
    if [ $localnode == $ip ] || [ $localnodeip == $ip ];then
echo "local node install system package"
##yum install package
yum -y install vim
yum -y install net-tools
yum -y install gcc
yum -y install zlib-devel
yum -y install libffi-devel
yum -y install readline-devel
yum -y install libaio
yum -y install lsof
yum -y install sysstat
yum -y install unzip
yum -y install bzip2-devel
yum -y install xz-devel
yum -y install gcc-c++
yum -y install dmidecode
yum -y install rng-tools
yum -y install kernel-headers
yum -y install mtr
systemctl start rngd
systemctl enable rngd
yum -y install unixODBC
yum -y install unixODBC-devel
yum -y install gcc-gfortran
yum -y install openssl openssl-devel  openssl-libs
yum -y install wget 
yum -y install fontconfig
set +e
#yum -y install bitmap-fonts
#yum -y groupinstall "X Window System"
yum -y install mariadb-libs
yum -y install mariadb
yum -y install bzip2
yum -y install bitmap-fonts-cjk
yum -y install libX11-devel
yum -y install libxml2-devel
yum -y install e2fsprogs-devel
yum -y install freetds
yum -y install freetds-devel
yum -y install libicu-devel
yum -y install postgresql-devel
set -e
yum -y install mkfontscale
yum -y install libjpeg-turbo-devel
yum -y install libxml2*
yum -y install freetype*
yum -y install libpng*
yum -y install libXext-devel
yum -y install libXt
yum -y install libxslt-devel
yum -y install make
else
echo "$ip install system package"
    ssh $ip "yum -y install vim mariadb-libs mariadb net-tools gcc zlib-devel libffi-devel readline-devel libaio lsof sysstat unzip bzip2-devel xz-devel gcc-c++ unixODBC unixODBC-devel gcc-gfortran wget fontconfig mkfontscale libjpeg-turbo-devel rng-tools dmidecode"
    ssh $ip "systemctl start rngd;systemctl enable rngd;yum -y install openssl*;yum -y install libxml2*;yum -y install freetype*;yum -y install libpng*"
    set +e
    ssh $ip 'yum -y install bitmap-fonts bitmap-fonts-cjk freetds libicu-devel'
    ssh $ip 'yum -y install libXext-devel libXt libxslt-devel postgresql-devel'
    set -e
fi
done
}

install_zypper(){
for ip in $ds_hosts
do
if [ $localnode == $ip ] || [ $localnodeip == $ip ];then
echo "local node install system package"
zypper install -y gcc
zypper install -y expect
zypper install -y zlib-devel
zypper install -y libopenssl-devel
zypper install -y libaio
zypper install -y lsof
zypper install -y sysstat
zypper install -y unzip
zypper install -y bzip2
zypper install -y gcc-c++
zypper install -y dmidecode
zypper install -y rng-tools
zypper install -y selinux-tools
zypper install -y bison
zypper install -y flex
zypper install -y wget
zypper install -y fontconfig
zypper install -y mkfontscale 
zypper install -y libzip2
zypper install -y libffi*
zypper install -y openssl*
systemctl start rng-tools
systemctl enable rng-tools
zypper install -y mariadb-client
zypper install -y libffi48-devel
zypper install -y postgresql-devel
zypper install -y xz-devel
zypper install -y libicu-devel
zypper install -y readline-devel
zypper install -y libXext-devel
zypper install -y libxslt-devel
else
echo "$ip install system package"
ssh $ip "zypper install -y postgresql-devel libicu-devel gcc expect zlib-devel libopenssl-devel libaio lsof sysstat unzip bzip2 gcc-c++ rng-tools selinux-tools bison flex wget fontconfig mkfontscale libzip2 dmidecode"
ssh $ip "zypper install -y libffi*;zypper install -y openssl*"
ssh $ip "systemctl start rng-tools;systemctl enable rng-tools"
ssh $ip "zypper install -y mariadb-client;zypper install -y libffi48-devel;zypper install -y xz-devel;zypper install -y readline-devel;zypper install -y libXext-devel;zypper install -y libxslt-devel"
fi
done
}

install_apt(){
for ip in $ds_hosts
do
if [ $localnode == $ip ] || [ $localnodeip == $ip ];then
echo "local node install system package"
apt install -y gcc
apt install -y zlib*
apt install -y libffi*
apt install -y openssl*
apt install -y libssl*
apt install -y readline*
apt install -y libreadline-dev*
apt install -y libaio*
apt install -y lsof
apt install -y sysstat
apt install -y unzip
apt install -y bzip2
set +e
apt install -y g++*
apt install -y bison*
apt install -y flex*
apt install -y freetds-dev
set -e
apt install -y unixODBC*
apt install -y fontconfig
apt install -y cmake
apt install -y odbcinst
apt install -y odbcinst1debian2
apt install -y libodbc1
apt install -y liblzma-dev
apt install -y gfortran
apt install -y libjpeg-dev
apt install -y zlib1g-dev
apt install -y libbz2-dev
apt install -y libopenblas-dev
apt install -y rng-tools
rngd -r /dev/urandom
apt install mysql-client
else
echo "$ip install system package"
ssh $ip "apt install -y gcc lsof sysstat unzip bzip2 fontconfig cmake odbcinst odbcinst1debian2 libodbc1 liblzma-dev gfortran libjpeg-dev zlib1g-dev libbz2-dev libopenblas-dev rng-tools"
ssh $ip "rngd -r /dev/urandom;apt install -y unixODBC*;apt install -y libaio*;apt install -y libreadline-dev*;apt install -y readline*;apt install -y libssl*;apt install -y openssl*;apt install -y libffi*;apt install -y zlib*;"
set +e
ssh $ip "apt install -y g++*;apt install -y bison*;apt install -y flex*;apt install -y freetds-dev"
set -e
ssh $ip "apt install mysql-client"
fi
done
}


ds_hosts=$(awk -F '=' '/^DS_Web|^DS_Collector|^DS_Monitor|^DS_Logana|^DS_Fstask|^DS_Other_Executor|^DS_Zookeeper|^DS_Redis|^DSPG_Node/ {print $2}' $CONF/role.cfg | tr -s '\n' | tr ',' '\n' |sort -u)

if [ -z $DBAIOps_oper_dir ];then
    echo "DBAIOps安装目录不存在！"
    exit 1
fi

flag=$2

case $1 in
        "-install")
                read -p "chose os type:
1)redhat
2)centos
3)uos
4)kylinV4
5)kylinV10
6)suse
Please enter your os type number:" number
        if [ "$flag" == "free" ];then
            install_yum_free
            case $number in
                "1")
                    echo "redhat" > $os_type_file
                ;;
                "2")
                    echo "centos" > $os_type_file
                ;;
                "3")
                    echo "uos" > $os_type_file
                ;;
                "4")
                    echo "kylinV4" > $os_type_file
                ;;
                "5")
                echo "kylinV10" > $os_type_file
                ;;
                "6")
                    echo "suse" > $os_type_file
                ;;
                *)
                    print_usage
                    exit 1
                ;;
                esac
            echo "System Package install Successed!"
		else
                    install $number
		fi
        ;;
        *)
                print_usage
                exit 1
        ;;
esac

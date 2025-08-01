#!/bin/bash
#
#
#
bin=`dirname "${BASH_SOURCE-$0}"`
bin=`cd "$bin"; pwd`
ROOT=`cd $bin;cd ..;pwd`
DBAIOps_HOME="/usr/software"
DBAIOps_oper_dir=/usr/software
python3_home=$DBAIOps_oper_dir/python3
python3_lib_dir=$DBAIOps_oper_dir/python3/python3_lib
CONF=$DBAIOps_HOME
localnode=$(hostname)
log_dir=$DBAIOps_oper_dir/bin/logs
cpu_version=$(uname -a | grep aarch64)
python3_rpm_log=${log_dir}/python3_rpm_install.log
set -e
print_usage() {
    echo "Usage: DBAIOps python3 installation script"
    echo "< -install >"
    echo "  -install                       install python3 environment"
    echo "< -install_thirdlib >"
    echo "  -install_thirdlib              install python3 third library"
    echo "< -install_rpm      >"
    echo "< -install_rpm      >            install os level rpm package"
}

install() {
    echo "############################################################"
    echo "                      install python3                       "
    echo "############################################################"
    if [ ! -f $python3_home/Python-3.8.16.tgz ]; then
        echo "python3安装文件不存在！"
        exit 1
    fi
    for ip in $ds_hosts; do
        python3_log=${log_dir}/python3_install.log
        if [ $localnode == $ip ]; then
            echo "local node install python3"
            cd $python3_home && tar --no-same-owner -xzvf $python3_home/Python-3.8.16.tgz >/dev/null 2>&1 && cd $python3_home/Python-3.8.16 && ./configure --prefix=$python3_home >$python3_log 2>&1 && make >>$python3_log 2>&1 && make install >>$python3_log 2>&1
            echo "export PYTHON3_HOME=/usr/software/python3" >/etc/profile.d/python3.sh
            echo "export PATH=\$PYTHON3_HOME/bin:\$PATH" >>/etc/profile.d/python3.sh
            echo "export DM_HOME=/usr/software/python3/python3_lib/dpi" >>/etc/profile.d/python3.sh
            echo "export PYTHONPATH=/usr/software/python3/pyzenith:/usr/software/python3/python3_lib" >>/etc/profile.d/python3.sh
            echo "export PYTHONIOENCODING=utf-8" >>/etc/profile.d/python3.sh
            chmod 644 /etc/profile.d/python3.sh
            source /etc/profile.d/python3.sh
            if [ -f /usr/share/crypto-policies/DEFAULT/opensslcnf.txt ]; then
                sed -i "s/MinProtocol = TLSv1.2/MinProtocol = TLSv1.1/g" /usr/share/crypto-policies/DEFAULT/opensslcnf.txt
            fi
            if [ -z "$cpu_version" ]; then
                echo "export LD_LIBRARY_PATH=/usr/lib64:/usr/lib:/usr/software/lib/yashan/x86:/usr/software/python3/python3_lib/dpi:/usr/software/lib/shentong/x86:\$LD_LIBRARY_PATH" >> /etc/profile.d/python3.sh
            else
                echo "export LD_LIBRARY_PATH=/usr/lib64:/usr/lib:/usr/software/lib/yashan/arm:/usr/software/python3/python3_lib/dpi:/usr/software/lib/shentong/arm:\$LD_LIBRARY_PATH" >> /etc/profile.d/python3.sh
            fi

        else
            echo "$ip:"
            ssh $ip "echo \"export PYTHON3_HOME=/usr/software/python3\" > /etc/profile.d/python3.sh"
            ssh $ip 'echo "export PATH=\$PYTHON3_HOME/bin:\$PATH" >> /etc/profile.d/python3.sh'
            ssh $ip 'echo "export DM_HOME=/usr/software/python3/python3_lib/dpi" >> /etc/profile.d/python3.sh'
            ssh $ip 'echo "export PYTHONPATH=/usr/software/python3/pyzenith:/usr/software/python3/python3_lib" >> /etc/profile.d/python3.sh'
            ssh $ip 'echo "export PYTHONIOENCODING=utf-8" >> /etc/profile.d/python3.sh'
            ssh $ip 'chmod 644 /etc/profile.d/python3.sh'
            if [ -z "$cpu_version" ]; then
                ssh $ip 'echo "export LD_LIBRARY_PATH=/usr/lib64:/usr/lib:/usr/software/lib/yashan/x86:/usr/software/python3/python3_lib/dpi:/usr/software/lib/shentong/x86:\$LD_LIBRARY_PATH" >> /etc/profile.d/python3.sh'
            else
                ssh $ip 'echo "export LD_LIBRARY_PATH=/usr/lib64:/usr/lib:/usr/software/lib/yashan/arm:/usr/software/python3/python3_lib/dpi:/usr/software/lib/shentong/arm:\$LD_LIBRARY_PATH" >> /etc/profile.d/python3.sh'
            fi
        fi
    done
    echo "Python3 install Successed!"
}

total_nums=76

chmod +x -R /usr/software/lib

install_thirdlib() {
    echo "############################################################"
    echo "                 install python3 thirdlib                   "
    echo "############################################################"
    python3_thirdlib_log=${log_dir}/python3_thirdlib_install.log
    python3_installed_hirdlib=${log_dir}/python3_installed_thirdlib.log
    if [ ! -f $python3_installed_hirdlib ]; then
        touch $python3_installed_hirdlib
    fi
    echo "local node install python3 third lib package:"
    cat /dev/null >$python3_thirdlib_log
    set -e
    source /etc/profile
    set +e
    source /etc/profile.d/java.sh
    source /etc/profile.d/python3.sh
    echo "setuptools begin install" >>$python3_thirdlib_log
    pip3 uninstall setuptools -y >>$python3_thirdlib_log
    cd $python3_lib_dir
    tar --no-same-owner -xvzf setuptools-59.6.0.tar.gz >/dev/null 2>&1
    cd setuptools-59.6.0
    python3 setup.py install >>$python3_thirdlib_log 2>&1
    echo "setuptools install successed" >>$python3_thirdlib_log
    set +e
    flag=$(grep "cx_Oracle" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "cx_Oracle begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -xvzf cx_Oracle-8.3.0.tar.gz >/dev/null 2>&1
        cd cx_Oracle-8.3.0/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'cx-Oracle install successed'
        echo "cx_Oracle install successed" >>$python3_thirdlib_log
        echo "cx_Oracle" >$python3_installed_hirdlib
    else
        echo "cx_Oracle have installed"
    fi
    echo "Have install 3rd lib package: 1/$total_nums"

    set +e
    flag=$(grep "psycopg2" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "psycopg2 begin install" >>$python3_thirdlib_log
        if [ -z "$cpu_version" ]; then
            cd $python3_lib_dir
            tar --no-same-owner -xvzf psycopg2-2.9.1.tar.gz >/dev/null 2>&1
            cd psycopg2-2.9.1/
            python3 setup.py install >>$python3_thirdlib_log 2>&1
        else
            cd $python3_lib_dir
            tar --no-same-owner -xvzf psycopg2-2.9.1.tar.gz >/dev/null 2>&1
            cd psycopg2-2.9.1/
            python3 setup.py install >>$python3_thirdlib_log 2>&1
        fi
        echo 'psycopg2 install successed'
        echo "psycopg2 install successed" >>$python3_thirdlib_log
        echo "psycopg2" >>$python3_installed_hirdlib
    else
        echo "psycopg2 have installed"
    fi
    echo "Have install 3rd lib package: 2/$total_nums"

    set +e
    flag=$(grep "timeout-decorator" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "timeout-decorator begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -xvzf timeout-decorator-0.4.0.tar.gz >/dev/null 2>&1
        cd timeout-decorator-0.4.0/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'timeout-decorator install successed'

        echo "timeout-decorator install successed" >>$python3_thirdlib_log
        echo "timeout-decorator" >>$python3_installed_hirdlib
    else
        echo "timeout-decorator have installed"
    fi
    echo "Have install 3rd lib package: 3/$total_nums"

    set +e
    flag=$(grep "six" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "six begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -xvzf six-1.11.0.tar.gz >/dev/null 2>&1
        cd six-1.11.0/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'six install successed'
        echo "six install successed" >>$python3_thirdlib_log
        echo "six" >>$python3_installed_hirdlib
    else
        echo "six have installed"
    fi
    echo "Have install 3rd lib package: 4/$total_nums"

    set +e
    flag=$(grep "pycparser" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "pycparser begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -xvzf pycparser-2.14.tar.gz >/dev/null 2>&1
        cd pycparser-2.14/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'pycparser install successed'
        echo "pycparser install successed" >>$python3_thirdlib_log
        echo "pycparser" >>$python3_installed_hirdlib
    else
        echo "pycparser have installed"
    fi
    echo "Have install 3rd lib package: 5/$total_nums"

    set +e
    flag=$(grep "cffi" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "cffi begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -xvzf cffi-1.15.1.tar.gz >/dev/null 2>&1
        cd cffi-1.15.1
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'cffi install successed'
        echo "cffi install successed" >>$python3_thirdlib_log
        echo "cffi" >>$python3_installed_hirdlib
    else
        echo "cffi have installed"
    fi
    echo "Have install 3rd lib package: 6/$total_nums"

    set +e
    flag=$(grep "bcrypt" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "bcrypt begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -xvzf bcrypt-3.2.2.tar.gz >/dev/null 2>&1
        cd bcrypt-3.2.2/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'bcrypt install successed'
        echo "bcrypt install successed" >>$python3_thirdlib_log
        echo "bcrypt" >>$python3_installed_hirdlib
    else
        echo "bcrypt have installed"
    fi
    echo "Have install 3rd lib package: 7/$total_nums"

    set +e
    flag=$(grep "Cython" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "Cython begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -xvzf Cython-0.29.35.tar.gz >/dev/null 2>&1
        cd Cython-0.29.35/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'Cython install successed'
        echo "Cython install successed" >>$python3_thirdlib_log
        echo "Cython" >>$python3_installed_hirdlib
    else
        echo "Cython have installed"
    fi
    echo "Have install 3rd lib package: 8/$total_nums"

    set +e
    flag=$(grep "PyNaCl" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "PyNaCl begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -xvzf PyNaCl-1.5.0.tar.gz >/dev/null 2>&1
        cd PyNaCl-1.5.0/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'PyNaCl install successed'
        echo "PyNaCl install successed" >>$python3_thirdlib_log
        echo "PyNaCl" >>$python3_installed_hirdlib
    else
        echo "PyNaCl have installed"
    fi
    echo "Have install 3rd lib package: 9/$total_nums"

    set +e
    flag=$(grep "asn1crypto" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "asn1crypto begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -xvzf asn1crypto-0.22.0.tar.gz >/dev/null 2>&1
        cd asn1crypto-0.22.0/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'asn1crypto install successed'
        echo "asn1crypto install successed" >>$python3_thirdlib_log
        echo "asn1crypto" >>$python3_installed_hirdlib
    else
        echo "asn1crypto have installed"
    fi
    echo "Have install 3rd lib package: 10/$total_nums"

    set +e
    flag=$(grep "idna" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "idna begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -xvzf idna-2.7.tar.gz >/dev/null 2>&1
        cd idna-2.7/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'idna install successed'
        echo "idna install successed" >>$python3_thirdlib_log
        echo "idna" >>$python3_installed_hirdlib
    else
        echo "idna have installed"
    fi
    echo "Have install 3rd lib package: 11/$total_nums"

    set +e
    flag=$(grep "cryptography" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "cryptography begin install" >>$python3_thirdlib_log
        #if [ -f /etc/redhat-release ];then
        cd $python3_lib_dir
        if [ -z "$cpu_version" ]; then
            pip3 install cryptography-41.0.3-cp37-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl >>$python3_thirdlib_log 2>&1
        else
            pip3 install cryptography-41.0.3-cp37-abi3-manylinux_2_17_aarch64.manylinux2014_aarch64.whl >>$python3_thirdlib_log 2>&1
        fi
#        tar --no-same-owner -xvzf cryptography-2.7.tar.gz >/dev/null 2>&1
#        cd cryptography-2.7/
#        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'cryptography install successed'
        #elif [ $uos_len -ne 0 ];then
        #cd $python3_lib_dir;tar --no-same-owner -xvzf cryptography-2.2.2.tar.gz > /dev/null 2>&1;cd cryptography-2.2.2/;python3 setup.py install >> $python3_thirdlib_log 2>&1;echo 'cryptography install successed'
        #else
        #cd $python3_lib_dir;tar --no-same-owner -xvzf cryptography-2.2.2.tar.gz > /dev/null 2>&1;cd cryptography-2.2.2/;\cp -f /usr/lib64/libffi.so /usr/lib64/libffi.so.6;python3 setup.py install >> $python3_thirdlib_log 2>&1;echo 'cryptography install successed'
        #fi
        echo "cryptography install successed" >>$python3_thirdlib_log
        echo "cryptography" >>$python3_installed_hirdlib
    else
        echo "cryptography have installed"
    fi
    echo "Have install 3rd lib package: 12/$total_nums"

    set +e
    flag=$(grep "pyasn1" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "pyasn1 begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -xvzf pyasn1-0.4.3.tar.gz >/dev/null 2>&1
        cd pyasn1-0.4.3/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'pyasn1 install successed'
        echo "pyasn1 install successed" >>$python3_thirdlib_log
        echo "pyasn1" >>$python3_installed_hirdlib
    else
        echo "pyasn1 have installed"
    fi
    echo "Have install 3rd lib package: 13/$total_nums"

    set +e
    flag=$(grep "paramiko" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "paramiko begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -xvzf paramiko-3.3.1.tar.gz >/dev/null 2>&1
        cd paramiko-3.3.1/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'paramiko install successed'
        echo "paramiko install successed" >>$python3_thirdlib_log
        echo "paramiko" >>$python3_installed_hirdlib
    else
        echo "paramiko have installed"
    fi
    echo "Have install 3rd lib package: 14/$total_nums"

    set +e
    flag=$(grep "kazoo" $python3_installed_hirdlib)
    set -e

    if [ -z "$flag" ]; then
        echo "kazoo begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -xvzf kazoo-2.9.0.tar.gz >/dev/null 2>&1
        cd kazoo-2.9.0/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'kazoo install successed'
        echo "kazoo install successed" >>$python3_thirdlib_log
        echo "kazoo" >>$python3_installed_hirdlib
    else
        echo "kazoo have installed"
    fi
    echo "Have install 3rd lib package: 15/$total_nums"

    set +e
    flag=$(grep "psutil" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "psutil begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -xvzf psutil-5.4.5.tar.gz >/dev/null 2>&1
        cd psutil-5.4.5/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'psutil install successed'
        echo "psutil install successed" >>$python3_thirdlib_log
        echo "psutil" >>$python3_installed_hirdlib
    else
        echo "psutil have installed"
    fi
    echo "Have install 3rd lib package: 16/$total_nums"

    set +e
    flag=$(grep "pyjnius" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "pyjnius begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -xvzf pyjnius-1.3.0.0.tar.gz >/dev/null
        cd pyjnius-1.3.0/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'pyjnius install successed'
        echo "pyjnius install successed" >>$python3_thirdlib_log
        echo "pyjnius" >>$python3_installed_hirdlib
    else
        echo "pyjnius have installed"
    fi
    echo "Have install 3rd lib package: 17/$total_nums"

    set +e
    flag=$(grep "pycrypto" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "pycrypto begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -xvzf pycrypto-2.6.1.tar.gz >/dev/null 2>&1
        cd pycrypto-2.6.1/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'pycrypto install successed'
        echo "pycrypto install successed" >>$python3_thirdlib_log
        echo "pycrypto" >>$python3_installed_hirdlib
    else
        echo "pycrypto have installed"
    fi
    echo "Have install 3rd lib package: 18/$total_nums"

    set +e
    flag=$(grep "protobuf" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "protobuf begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -xvzf protobuf-3.17.1.tar.gz >/dev/null 2>&1
        cd protobuf-3.17.1/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'protobuf install successed'
        echo "protobuf install successed" >>$python3_thirdlib_log
        echo "protobuf" >>$python3_installed_hirdlib
    else
        echo "protobuf have installed"
    fi
    echo "Have install 3rd lib package: 19/$total_nums"

    set +e
    flag=$(grep "mysql_connector_python" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "mysql_connector_python begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -xvzf mysql-connector-python-2.1.8.tar.gz >/dev/null 2>&1
        cd mysql-connector-python-2.1.8/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'mysql_connector_python install successed'
        echo "mysql_connector_python install successed" >>$python3_thirdlib_log
        #cd $python3_lib_dir;unzip -o dmPython.zip > /dev/null 2>&1;cd dmPython;python3 setup.py install > /dev/null 2>&1;echo '/usr/software/python3/dpi' > /etc/ld.so.conf.d/dmdba.conf;echo 'TIME_ZONE=(480)' > /etc/dm_svc.conf;echo 'LANGUAGE=(en)' >> /etc/dm_svc.conf;chmod 644 /etc/dm_svc.conf;echo 'dmPython install successed'
        echo "mysql_connector_python" >>$python3_installed_hirdlib
    else
        echo "mysql_connector_python have installed"
    fi
    echo "Have install 3rd lib package: 20/$total_nums"

    set +e
    flag=$(grep "dmPython" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "dmPython begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        if [ -z "$cpu_version" ]; then
            tar -xvzf dpi_x86_64.tar.gz >/dev/null
        else
            tar -xvzf dpi_aarch64.tar.gz >/dev/null
        fi
        cd $python3_lib_dir
        unzip -o dmPython.zip >/dev/null 2>&1
        cd dmPython
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'TIME_ZONE=(480)' >/etc/dm_svc.conf
        echo 'LANGUAGE=(en)' >>/etc/dm_svc.conf
        chmod 644 /etc/dm_svc.conf
        echo 'dmPython install successed'
        echo "dmPython install successed" >>$python3_thirdlib_log
        echo "dmPython" >>$python3_installed_hirdlib
    else
        echo "dmPython have installed"
    fi
    echo "Have install 3rd lib package: 21/$total_nums"

    set +e
    flag=$(grep "numpy" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "numpy begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        if [ -z "$cpu_version" ]; then
            export CFLAGS="-std=c99"
            export LAPACK=None
            export BLAS=None
            unzip -o numpy-1.22.4.zip >/dev/null 2>&1
            cd numpy-1.22.4/
            python3 setup.py install >>$python3_thirdlib_log 2>&1
            echo 'numpy install successed!'
            unset -v CFLAGS
            unset -v LAPACK
            unset -v BLAS
        else
            pip3 install numpy-1.23.2-cp38-cp38-manylinux_2_17_aarch64.manylinux2014_aarch64.whl >>$python3_thirdlib_log 2>&1
        fi
        echo "numpy install successed" >>$python3_thirdlib_log
        echo "numpy" >>$python3_installed_hirdlib
    else
        echo "numpy have installed"
    fi
    echo "Have install 3rd lib package: 22/$total_nums"

    set +e
    flag=$(grep "pytz" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "pytz begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -xvzf pytz-2019.3.tar.gz >/dev/null 2>&1
        cd pytz-2019.3/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'pytz install successed'
        echo "pytz install successed" >>$python3_thirdlib_log
        echo "pytz" >>$python3_installed_hirdlib
    else
        echo "pytz have installed"
    fi
    echo "Have install 3rd lib package: 23/$total_nums"

    set +e
    flag=$(grep "setuptools_scm" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "setuptools_scm begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -xvzf setuptools_scm-3.4.0.tar.gz >/dev/null 2>&1
        cd setuptools_scm-3.4.0/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'setuptools_scm install successed'
        echo "setuptools_scm install successed" >>$python3_thirdlib_log
        echo "setuptools_scm" >>$python3_installed_hirdlib
    else
        echo "setuptools_scm have installed"
    fi
    echo "Have install 3rd lib package: 24/$total_nums"

    set +e
    flag=$(grep "python_dateutil" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        #装python-dateutil要先装setuptools_scm
        echo "python_dateutil begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -xvzf python-dateutil-2.8.0.tar.gz >/dev/null 2>&1
        cd python-dateutil-2.8.0/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'python_dateutil install successed'
        echo "python_dateutil install successed" >>$python3_thirdlib_log
        echo "python_dateutil" >>$python3_installed_hirdlib
    else
        echo "python_dateutil have installed"
    fi
    echo "Have install 3rd lib package: 25/$total_nums"

    set +e
    flag=$(grep "pandas" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "pandas begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -xvzf pandas-1.0.5.tar.gz >/dev/null 2>&1
        cd pandas-1.0.5/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'pandas install successed'
        echo "pandas install successed" >>$python3_thirdlib_log
        echo "pandas" >>$python3_installed_hirdlib
    else
        echo "pandas have installed"
    fi
    echo "Have install 3rd lib package: 26/$total_nums"

    set +e
    flag=$(grep "pybind11" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        #装scipy要先装pybind11
        echo "pybind11 begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -xvzf pybind11-2.6.2.tar.gz >/dev/null 2>&1
        cd pybind11-2.6.2/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'pybind11 install successed'
        echo 'pybind11 install successed' >>$python3_thirdlib_log
        echo "pybind11" >>$python3_installed_hirdlib
    else
        echo "pybind11 have installed"
    fi
    echo "Have install 3rd lib package: 27/$total_nums"

    if [ -z "$cpu_version" ]; then
        set +e
        flag=$(grep "scipy" $python3_installed_hirdlib)
        set -e
        if [ -z "$flag" ]; then
            cd $python3_lib_dir
            pip3 install scipy-1.10.1-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl >>$python3_thirdlib_log 2>&1
            echo 'scipy install successed'
            echo "scipy install successed" >>$python3_thirdlib_log
            echo "scipy" >>$python3_installed_hirdlib
        else
            echo "scipy have installed"
        fi
        echo "Have install 3rd lib package: 28/$total_nums"
    else
        set +e
        flag=$(grep "blas" $python3_installed_hirdlib)
        set -e
        if [ -z "$flag" ]; then
            echo "blas begin install" >>$python3_thirdlib_log
            cd $python3_lib_dir
            tar --no-same-owner -xvzf blas-3.10.0.tgz >/dev/null 2>&1
            cd BLAS-3.10.0
            gfortran -c -O3 -fPIC *.f
            gcc -shared *.o -fPIC -o libblas.so
            cp libblas.so /usr/local/lib/
            ar rv libblas.a *.o
            cp libblas.a /usr/local/lib
            echo "blas install successed"
            echo "blas install successed" >>$python3_thirdlib_log
            echo "blas" >>$python3_installed_hirdlib
        else
            echo "blas have installed"
        fi
        echo "Have install 3rd lib package: 28/$total_nums"


        set +e
        flag=$(grep "lapack" $python3_installed_hirdlib)
        set -e
        if [ -z "$flag" ]; then
            echo "lapack begin install" >>$python3_thirdlib_log
            cd $python3_lib_dir
            tar --no-same-owner -vxzf lapack-3.10.0.tar.gz >/dev/null 2>&1
            cd lapack-3.10.0/
            cp make.inc.example make.inc
            make >>$python3_thirdlib_log 2>&1
            cp *.a /usr/local/lib
            echo "lapack install successed" >>$python3_thirdlib_log
            echo "lapack install successed"
            echo "lapack" >>$python3_installed_hirdlib
        else
            echo "lapack have installed"
        fi
        echo "Have install 3rd lib package: 29/$total_nums"


        set +e
        flag=$(grep "scipy" $python3_installed_hirdlib)
        set -e
        if [ -z "$flag" ]; then
            echo "scipy begin install" >>$python3_thirdlib_log
            cd $python3_lib_dir
            tar --no-same-owner -xvzf scipy-1.5.2.tar.gz >/dev/null 2>&1
            cd scipy-1.5.2/
            python3 setup.py install >>$python3_thirdlib_log 2>&1
            echo 'scipy install successed'
            echo "scipy install successed" >>$python3_thirdlib_log
            echo "scipy" >>$python3_installed_hirdlib
        else
            echo "scipy have installed"
        fi
        echo "Have install 3rd lib package: 30/$total_nums"
    fi

    set +e
    flag=$(grep "patsy" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "patsy begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -xvzf patsy-0.5.1.tar.gz >/dev/null 2>&1
        cd patsy-0.5.1/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'patsy install successed'
        echo "patsy install successed" >>$python3_thirdlib_log
        echo "patsy" >>$python3_installed_hirdlib
    else
        echo "patsy have installed"
    fi
    echo "Have install 3rd lib package: 31/$total_nums"

    set +e
    flag=$(grep "statsmodels" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "statsmodels begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -xvzf statsmodels-0.12.2.tar.gz >/dev/null 2>&1
        cd statsmodels-0.12.2/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'statsmodels install successed'
        echo '/usr/software/python3/pyzenith' >/etc/ld.so.conf.d/pyzenith.conf
        echo 'GaussDB T python3 install successed'
        echo "statsmodels install successed" >>$python3_thirdlib_log
        echo "statsmodels" >>$python3_installed_hirdlib
    else
        echo "statsmodels have installed"
    fi
    echo "Have install 3rd lib package: 32/$total_nums"

    set +e
    flag=$(grep "certifi" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "certifi begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -xvzf certifi-2020.4.5.tar.gz >/dev/null 2>&1
        cd certifi-2020.4.5/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'certifi install successed'
        echo "certifi install successed" >>$python3_thirdlib_log
        echo "certifi" >>$python3_installed_hirdlib
    else
        echo "certifi have installed"
    fi
    echo "Have install 3rd lib package: 33/$total_nums"

    set +e
    flag=$(grep "urllib3" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "urllib3 begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -xvzf urllib3-1.26.6.tar.gz >/dev/null 2>&1
        cd urllib3-1.26.6/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'urllib3 install successed'
        echo "urllib3 install successed" >>$python3_thirdlib_log
        echo "urllib3" >>$python3_installed_hirdlib
    else
        echo "urllib3 have installed"
    fi
    echo "Have install 3rd lib package: 34/$total_nums"

    set +e
    flag=$(grep "chardet" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "chardet begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -xvzf chardet-3.0.4.tar.gz >/dev/null 2>&1
        cd chardet-3.0.4/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'chardet install successed'
        echo "chardet install successed" >>$python3_thirdlib_log
        echo "chardet" >>$python3_installed_hirdlib
    else
        echo "chardet have installed"
    fi
    echo "Have install 3rd lib package: 35/$total_nums"

    set +e
    flag=$(grep "charset-normalizer" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "charset-normalizer begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -xvzf charset-normalizer-2.0.0.tar.gz >/dev/null 2>&1
        cd charset-normalizer-2.0.0/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'charset-normalizer install successed'
        echo "charset-normalizer install successed" >>$python3_thirdlib_log
        echo "charset-normalizer" >>$python3_installed_hirdlib
    else
        echo "charset-normalizer have installed"
    fi
    echo "Have install 3rd lib package: 36/$total_nums"

    set +e
    flag=$(grep "requests" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "requests begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -xvzf requests-2.26.0.tar.gz >/dev/null 2>&1
        cd requests-2.26.0/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'requests install successed'
        echo "requests install successed" >>$python3_thirdlib_log
        echo "requests" >>$python3_installed_hirdlib
    else
        echo "requests have installed"
    fi
    echo "Have install 3rd lib package: 37/$total_nums"

    set +e
    flag=$(grep "redis" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "redis begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -xvzf redis-3.5.3.tar.gz >/dev/null 2>&1
        cd redis-3.5.3/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'redis install successed'
        echo "redis install successed" >>$python3_thirdlib_log
        echo "redis" >>$python3_installed_hirdlib
    else
        echo "redis have installed"
    fi
    echo "Have install 3rd lib package: 38/$total_nums"

    set +e
    flag=$(grep "typing_extensions" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "typing_extensions begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -xvzf typing_extensions-3.10.0.0.tar.gz >/dev/null 2>&1
        cd typing_extensions-3.10.0.0/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'typing_extensions install successed'
        echo "typing_extensions install successed" >>$python3_thirdlib_log
        echo "typing_extensions" >>$python3_installed_hirdlib
    else
        echo "typing_extensions have installed"
    fi
    echo "Have install 3rd lib package: 39/$total_nums"

    set +e
    flag=$(grep "jpype" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        #要先装typing_extensions，然后再装JPype1
        echo "jpype begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar -xvzf JPype1-1.3.0.tar.gz >/dev/null 2>&1
        cd JPype1-1.3.0/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'jpype install successed'
        echo "jpype install successed" >>$python3_thirdlib_log
        echo "jpype" >>$python3_installed_hirdlib
    else
        echo "jpype have installed"
    fi
    echo "Have install 3rd lib package: 40/$total_nums"

    set +e
    flag=$(grep "xlrd" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "xlrd begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -xvzf xlrd-1.2.0.tar.gz >/dev/null 2>&1
        cd xlrd-1.2.0/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'xlrd install successed'
        echo "xlrd install successed" >>$python3_thirdlib_log
        echo "xlrd" >>$python3_installed_hirdlib
    else
        echo "xlrd have installed"
    fi
    echo "Have install 3rd lib package: 41/$total_nums"

    set +e
    flag=$(grep "SQLAlchemy" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "SQLAlchemy begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -xvzf SQLAlchemy-1.3.19.tar.gz >/dev/null 2>&1
        cd SQLAlchemy-1.3.19/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'sqlalchemy install successed'
        echo "SQLAlchemy install successed" >>$python3_thirdlib_log
        echo "SQLAlchemy" >>$python3_installed_hirdlib
    else
        echo "SQLAlchemy have installed"
    fi
    echo "Have install 3rd lib package: 42/$total_nums"

    set +e
    flag=$(grep "mongo-python-driver" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "mongo-python-driver begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -xvzf mongo-python-driver-3.11.1.tar.gz >/dev/null 2>&1
        cd mongo-python-driver-3.11.1/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'mongo-python-driver install successed'
        echo "mongo-python-driver install successed" >>$python3_thirdlib_log
        echo "mongo-python-driver" >>$python3_installed_hirdlib
    else
        echo "mongo-python-driver have installed"
    fi
    echo "Have install 3rd lib package: 43/$total_nums"

    set +e
    flag=$(grep "neo4j" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "neo4j begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -xvzf neo4j-4.1.1.tar.gz >/dev/null 2>&1
        cd neo4j-4.1.1/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'neo4j install successed'
        echo "neo4j install successed" >>$python3_thirdlib_log
        echo "neo4j" >>$python3_installed_hirdlib
    else
        echo "neo4j have installed"
    fi
    echo "Have install 3rd lib package: 44/$total_nums"

    set +e
    flag=$(grep "cppy" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "cppy begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -xvzf cppy-1.1.0.tar.gz >/dev/null 2>&1
        cd cppy-1.1.0/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'cppy install successed'
        echo "cppy install successed" >>$python3_thirdlib_log
        echo "cppy" >>$python3_installed_hirdlib
    else
        echo "cppy have installed"
    fi
    echo "Have install 3rd lib package: 45/$total_nums"

    set +e
    flag=$(grep "kiwisolver" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        #要先装cppy
        echo "kiwisolver begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -xvzf kiwisolver-1.3.1.tar.gz >/dev/null 2>&1
        cd kiwisolver-1.3.1/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'kiwisolver install successed'
        echo "kiwisolver install successed" >>$python3_thirdlib_log
        echo "kiwisolver" >>$python3_installed_hirdlib
    else
        echo "kiwisolver have installed"
    fi
    echo "Have install 3rd lib package: 46/$total_nums"

    set +e
    flag=$(grep "pyparsing" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "pyparsing begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -xvzf pyparsing-2.4.7.tar.gz >/dev/null 2>&1
        cd pyparsing-2.4.7/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'pyparsing install successed'
        echo "pyparsing install successed" >>$python3_thirdlib_log
        echo "pyparsing" >>$python3_installed_hirdlib
    else
        echo "pyparsing have installed"
    fi
    echo "Have install 3rd lib package: 47/$total_nums"

    set +e
    flag=$(grep "cycler" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "cycler begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -xvzf cycler-0.10.0.tar.gz >/dev/null 2>&1
        cd cycler-0.10.0/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'cycler install successed'
        echo "cycler install successed" >>$python3_thirdlib_log
        echo "cycler" >>$python3_installed_hirdlib
    else
        echo "cycler have installed"
    fi
    echo "Have install 3rd lib package: 48/$total_nums"

    set +e
    flag=$(grep "Pillow" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "Pillow begin install" >>$python3_thirdlib_log
        if [ -z "$flag_suse" ]; then
            cd $python3_lib_dir
            tar --no-same-owner -xvzf Pillow-8.1.0.tar.gz >/dev/null 2>&1
            cd Pillow-8.1.0/
            python3 setup.py install >>$python3_thirdlib_log 2>&1
            echo 'Pillow install successed'
        else
            cd $python3_lib_dir
            pip3 install Pillow-8.1.0-cp38-cp38m-manylinux1_x86_64.whl >>$python3_thirdlib_log 2>&1
            echo 'Pillow install successed'
        fi
        echo "Pillow install successed" >>$python3_thirdlib_log
        echo "Pillow" >>$python3_installed_hirdlib
    else
        echo "Pillow have installed"
    fi
    echo "Have install 3rd lib package: 49/$total_nums"

    set +e
    flag=$(grep "matplotlib" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "matplotlib begin install" >>$python3_thirdlib_log
        if [ -z "$flag_suse" ]; then
            cd $python3_lib_dir
            tar --no-same-owner -xvzf matplotlib-3.2.0.tar.gz >/dev/null 2>&1
            cd matplotlib-3.2.0/
            python3 setup.py install >>$python3_thirdlib_log 2>&1
        else
            cd $python3_lib_dir
            pip3 install matplotlib-3.2.0-cp38-cp38-manylinux1_x86_64.whl >>$python3_thirdlib_log 2>&1
        fi
        echo 'matplotlib install successed'

        if [ -z "$cpu_version" ]; then
            if [ -z "$flag_suse" ]; then
                \cp -rf $python3_home/SimHei.ttf $python3_home/lib/python3.8/site-packages/matplotlib-3.2.0-py3.8-linux-x86_64.egg/matplotlib/mpl-data/fonts/ttf
            else
                \cp -rf $python3_home/SimHei.ttf $python3_home/lib/python3.8/site-packages/matplotlib/mpl-data/fonts/ttf
            fi
        else
            \cp -rf $python3_home/SimHei.ttf $python3_home/lib/python3.8/site-packages/matplotlib-3.2.0-py3.8-linux-aarch64.egg/matplotlib/mpl-data/fonts/ttf
        fi
        rm -rf /root/.cache/matplotlib
        echo "matplotlib install successed" >>$python3_thirdlib_log
        echo "matplotlib" >>$python3_installed_hirdlib
    else
        echo "matplotlib have installed"
    fi
    echo "Have install 3rd lib package: 50/$total_nums"

    set +e
    flag=$(grep "threadpoolctl" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "threadpoolctl begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -vxzf threadpoolctl-2.1.0.tar.gz >/dev/null 2>&1
        cd threadpoolctl-2.1.0/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'threadpoolctl install successed'
        echo "threadpoolctl install successed" >>$python3_thirdlib_log
        echo "threadpoolctl" >>$python3_installed_hirdlib
    else
        echo "threadpoolctl have installed"
    fi
    echo "Have install 3rd lib package: 51/$total_nums"

    set +e
    flag=$(grep "joblib" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "joblib begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -xvzf joblib-1.0.1.tar.gz >/dev/null 2>&1
        cd joblib-1.0.1/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'joblib install successed'
        echo "joblib install successed" >>$python3_thirdlib_log
        echo "joblib" >>$python3_installed_hirdlib
    else
        echo "joblib have installed"
    fi
    echo "Have install 3rd lib package: 52/$total_nums"

    set +e
    flag=$(grep "scikit_learn" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "scikit_learn begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -xzvf scikit-learn-0.24.2.tar.gz >/dev/null 2>&1
        cd scikit-learn-0.24.2/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'scikit_learn install successed'
        echo "scikit_learn install successed" >>$python3_thirdlib_log
        echo "scikit_learn" >>$python3_installed_hirdlib
    else
        echo "scikit_learn have installed"
    fi
    echo "Have install 3rd lib package: 53/$total_nums"

    set +e
    flag=$(grep "pymssql" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "pymssql begin install" >>$python3_thirdlib_log
        if [ -z "$cpu_version" ]; then
            cd $python3_lib_dir
            pip3 install pymssql-2.1.5-cp38-cp38-manylinux1_x86_64.whl >>$python3_thirdlib_log 2>&1
        else
            if [ "$os_type" == "kylinV10" ]; then
                cd $python3_lib_dir
                tar --no-same-owner -xvzf setuptools-git-1.2.tar.gz >/dev/null 2>&1
                cd setuptools-git-1.2/
                python3 setup.py install >>$python3_thirdlib_log 2>&1
                set +e
                freetds_flag=$(rpm -qa | grep freetds-devel)
                set -e
                if [ -z "$freetds_flag" ]; then
                    cd $python3_home
                    rpm -ivh freetds-devel-1.00.38-7.ky10.aarch64.rpm >>$python3_thirdlib_log 2>&1
                fi
                cd $python3_lib_dir
                tar --no-same-owner -zxvf pymssql-2.1.5.tar.gz >/dev/null 2>&1
                cd pymssql-2.1.5/
                python3 setup.py install >>$python3_thirdlib_log 2>&1
            else
                cd $python3_lib_dir
                tar --no-same-owner -xvzf setuptools-git-1.2.tar.gz >/dev/null 2>&1
                cd setuptools-git-1.2/
                python3 setup.py install >>$python3_thirdlib_log 2>&1
                cd $python3_lib_dir
                tar --no-same-owner -zxvf pymssql-2.1.5.tar.gz >/dev/null 2>&1
                cd pymssql-2.1.5/
                python3 setup.py install >>$python3_thirdlib_log 2>&1
            fi
        fi
        echo 'pymssql install successed'
        echo 'pymssql install successed' >>$python3_thirdlib_log
        echo "pymssql" >>$python3_installed_hirdlib
    else
        echo "pymssql have installed"
    fi
    echo "Have install 3rd lib package: 54/$total_nums"

    set +e
    flag=$(grep "pyodbc" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "pyodbc begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar --no-same-owner -zxvf pyodbc-4.0.31.tar.gz >/dev/null 2>&1
        cd pyodbc-4.0.31/
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'pyodbc install successed'
        echo "pyodbc install successed" >>$python3_thirdlib_log
        echo "pyodbc" >>$python3_installed_hirdlib
    else
        echo "pyodbc have installed"
    fi
    echo "Have install 3rd lib package: 55/$total_nums"

    set +e
    flag=$(grep "psqlparse" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "psqlparse begin install" >>$python3_thirdlib_log
        if [ -z "$cpu_version" ]; then
            cd $python3_lib_dir
            unzip -o psqlparse.zip >/dev/null 2>&1
            cd psqlparse-master
            python3 setup.py install >>$python3_thirdlib_log 2>&1
        else
            cd $python3_lib_dir
            unzip -o libpg_query-13-latest.zip >/dev/null 2>&1
            cd libpg_query-13-latest
            make >>$python3_thirdlib_log 2>&1
            cd $python3_lib_dir
            unzip -o psqlparse.zip >/dev/null 2>&1
            cp $python3_lib_dir/libpg_query-13-latest/libpg_query.a $python3_lib_dir/psqlparse-master/libpg_query
            cd psqlparse-master
            python3 setup.py install >>$python3_thirdlib_log 2>&1
        fi
        echo 'psqlparse install successed'
        echo "psqlparse install successed" >>$python3_thirdlib_log
        echo "psqlparse" >>$python3_installed_hirdlib
    else
        echo "psqlparse have installed"
    fi
    echo "Have install 3rd lib package: 56/$total_nums"

    set +e
    flag=$(grep "ksycopg2" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "ksycopg2 begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        # if [ -z "$cpu_version" ]; then
        #     tar -xvf ksycopg2_x86_64.tar.gz >/dev/null
        # else
        #     tar -xvf ksycopg2_aarch64.tar.gz >/dev/null
        # fi
        echo "ksycopg2 install successed"
        echo "ksycopg2 install successed" >>$python3_thirdlib_log
        echo "ksycopg2" >>$python3_installed_hirdlib
    else
        echo "ksycopg2 have installed"
    fi
    echo "Have install 3rd lib package: 57/$total_nums"

    set +e
    flag=$(grep "lxml" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "lxml begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar -xvzf lxml-4.6.3.tar.gz > /dev/null
        cd lxml-4.6.3
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'lxml install successed'
        echo 'lxml install successed' >>$python3_thirdlib_log
        echo "lxml" >>$python3_installed_hirdlib
    else
        echo "lxml have installed"
    fi
    echo "Have install 3rd lib package: 58/$total_nums"

    set +e
    flag=$(grep "JayDeBeApi" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "JayDeBeApi begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar -xvzf JayDeBeApi-1.2.3.tar.gz > /dev/null
        cd JayDeBeApi-1.2.3
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'JayDeBeApi install successed'
        echo "JayDeBeApi install successed" >>$python3_thirdlib_log
        echo "JayDeBeApi" >>$python3_installed_hirdlib
    else
        echo "JayDeBeApi have installed"
    fi
    echo "Have install 3rd lib package: 59/$total_nums"


    set +e
    flag=$(grep "kafka-python" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "JayDeBeApi begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar -xvzf kafka-python-2.0.2.tar.gz > /dev/null
        cd kafka-python-2.0.2
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'kafka-python install successed'
        echo "kafka-python install successed" >>$python3_thirdlib_log
        echo "kafka-python" >>$python3_installed_hirdlib
    else
        echo "kafka-python have installed"
    fi
    echo "Have install 3rd lib package: 60/$total_nums"


    set +e
    flag=$(grep "rsa" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "rsa begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar -xvzf rsa-4.9.tar.gz > /dev/null
        cd rsa-4.9
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'rsa install successed'
        echo "rsa install successed" >>$python3_thirdlib_log
        echo "rsa" >>$python3_installed_hirdlib
    else
        echo "rsa have installed"
    fi
    echo "Have install 3rd lib package: 61/$total_nums"


    set +e
    flag=$(grep "jmespath" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "jmespath begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar -xvzf jmespath-0.10.0.tar.gz > /dev/null
        cd jmespath-0.10.0
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'jmespath install successed'
        echo "jmespath install successed" >>$python3_thirdlib_log
        echo "jmespath" >>$python3_installed_hirdlib
    else
        echo "jmespath have installed"
    fi
    echo "Have install 3rd lib package: 62/$total_nums"


    set +e
    flag=$(grep "aliyun-python-sdk-core-v2" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "aliyun-python-sdk-core-v2 begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar -xvzf aliyun-python-sdk-core-2.13.36.tar.gz > /dev/null
        cd aliyun-python-sdk-core-2.13.36
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'aliyun-python-sdk-core-v2 install successed'
        echo "aliyun-python-sdk-core-v2 install successed" >>$python3_thirdlib_log
        echo "aliyun-python-sdk-core-v2" >>$python3_installed_hirdlib
    else
        echo "aliyun-python-sdk-core-v2 have installed"
    fi
    echo "Have install 3rd lib package: 63/$total_nums"


    set +e
    flag=$(grep "aliyun-python-sdk-core-v3" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "aliyun-python-sdk-core-v3 begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar -xvzf aliyun-python-sdk-core-v3-2.13.33.tar.gz > /dev/null
        cd aliyun-python-sdk-core-v3-2.13.33
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'aliyun-python-sdk-core-v3 install successed'
        echo "aliyun-python-sdk-core-v3 install successed" >>$python3_thirdlib_log
        echo "aliyun-python-sdk-core-v3" >>$python3_installed_hirdlib
    else
        echo "aliyun-python-sdk-core-v3 have installed"
    fi
    echo "Have install 3rd lib package: 64/$total_nums"


    set +e
    flag=$(grep "aliyun-python-sdk-rds" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "aliyun-python-sdk-rds begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar -xvzf aliyun-python-sdk-rds-2.7.1.tar.gz > /dev/null
        cd aliyun-python-sdk-rds-2.7.1
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'aliyun-python-sdk-rds install successed'
        echo "aliyun-python-sdk-rds install successed" >>$python3_thirdlib_log
        echo "aliyun-python-sdk-rds" >>$python3_installed_hirdlib
    else
        echo "aliyun-python-sdk-rds have installed"
    fi
    echo "Have install 3rd lib package: 65/$total_nums"

    set +e
    flag=$(grep "ordered-set" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "ordered-set begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar -xvzf ordered-set-4.0.2.tar.gz > /dev/null
        cd ordered-set-4.0.2
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'ordered-set install successed'
        echo "ordered-set install successed" >>$python3_thirdlib_log
        echo "ordered-set" >>$python3_installed_hirdlib
    else
        echo "ordered-set have installed"
    fi
    echo "Have install 3rd lib package: 66/$total_nums"

    set +e
    flag=$(grep "datacompy" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "datacompy begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar -xvzf datacompy-0.8.4.tar.gz > /dev/null
        cd datacompy-0.8.4
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'datacompy install successed'
        echo "datacompy install successed" >>$python3_thirdlib_log
        echo "datacompy" >>$python3_installed_hirdlib
    else
        echo "datacompy have installed"
    fi
    echo "Have install 3rd lib package: 67/$total_nums"

    set +e
    if [ -z "$cpu_version" ]; then  #x86
        flag=$(grep "STPython" $python3_installed_hirdlib)
        set -e
        if [ -z "$flag" ]; then
            echo "STPython begin install" >>$python3_thirdlib_log
            cd $python3_lib_dir
            pip3 install STPython-2.0.16-cp38-cp38-linux_x86_64.whl >>$python3_thirdlib_log 2>&1
            echo 'STPython install successed'
            echo "STPython install successed" >>$python3_thirdlib_log
            echo "STPython" >>$python3_installed_hirdlib
        else
            echo "STPython have installed"
        fi
    else
        flag=$(grep "STPython" $python3_installed_hirdlib)
        set -e
        if [ -z "$flag" ]; then
            echo "STPython begin install" >>$python3_thirdlib_log
            cd $python3_lib_dir
            pip3 install STPython-2.0.19-cp38-cp38-linux_aarch64.whl >>$python3_thirdlib_log 2>&1
            echo 'STPython install successed'
            echo "STPython install successed" >>$python3_thirdlib_log
            echo "STPython" >>$python3_installed_hirdlib
        else
            echo "STPython have installed"
        fi
    fi
    echo "Have install 3rd lib package: 68/$total_nums"

    set +e
    flag=$(grep "aliyun-python-sdk-asapi" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "aliyun-python-sdk-asapi begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar -xvzf aliyun-python-sdk-asapi-2.4.7.1-py3.tar.gz > /dev/null
        cd aliyun-python-sdk-asapi-2.4.7.1
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'aliyun-python-sdk-asapi install successed'
        echo "aliyun-python-sdk-asapi install successed" >>$python3_thirdlib_log
        echo "aliyun-python-sdk-asapi" >>$python3_installed_hirdlib
    else
        echo "aliyun-python-sdk-asapi have installed"
    fi
    echo "Have install 3rd lib package: 69/$total_nums"

    set +e
    if [ -z "$cpu_version" ]; then  #x86
        flag=$(grep "yaspy" $python3_installed_hirdlib)
        set -e
        if [ -z "$flag" ]; then
            echo "yaspy begin install" >>$python3_thirdlib_log
            cd $python3_lib_dir
            pip3 install yaspy-1.0.0-cp38-cp38-linux_x86_64.whl >>$python3_thirdlib_log 2>&1
            echo 'yaspy install successed'
            echo "yaspy install successed" >>$python3_thirdlib_log
            echo "yaspy" >>$python3_installed_hirdlib
        else
            echo "yaspy have installed"
        fi
    else
        flag=$(grep "yaspy" $python3_installed_hirdlib)
        set -e
        if [ -z "$flag" ]; then
            echo "yaspy begin install" >>$python3_thirdlib_log
            cd $python3_lib_dir
            pip3 install yaspy-1.0.0-cp38-cp38-linux_aarch64.whl >>$python3_thirdlib_log 2>&1
            echo 'yaspy install successed'
            echo "yaspy install successed" >>$python3_thirdlib_log
            echo "yaspy" >>$python3_installed_hirdlib
        else
            echo "yaspy have installed"
        fi
    fi
    echo "Have install 3rd lib package: 70/$total_nums"
    if [ -z "$cpu_version" ]; then  #x86
        set +e
        flag=$(grep "ibm_db" $python3_installed_hirdlib)
        set -e
        if [ -z "$flag" ]; then
            echo "ibm_db begin install" >>$python3_thirdlib_log
            cd $python3_lib_dir
            pip3 install ibm_db-3.2.3-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl >>$python3_thirdlib_log 2>&1
            echo 'ibm_db install successed'
            echo "ibm_db install successed" >>$python3_thirdlib_log
            echo "ibm_db" >>$python3_installed_hirdlib
        else
            echo "ibm_db have installed"
        fi
    else
        echo "ibm_db only support x86 platform"
        echo "ibm_db only support x86 platform" >>$python3_thirdlib_log
    fi
    echo "Have install 3rd lib package: 71/$total_nums"
    

    set +e
    flag=$(grep "PyYAML" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "PyYAML begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar -xvzf PyYAML-6.0.1.tar.gz > /dev/null
        cd PyYAML-6.0.1
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'PyYAML install successed'
        echo "PyYAML install successed" >>$python3_thirdlib_log
        echo "PyYAML" >>$python3_installed_hirdlib
    else
        echo "PyYAML have installed"
    fi
    echo "Have install 3rd lib package: 72/$total_nums"

    # pymysql
    set +e
    flag=$(grep "pymysql" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "pymysql begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar -xvzf pymysql-1.1.1.tar.gz > /dev/null
        cd pymysql-1.1.1
        \cp -rf pymysql $python3_home/lib/python3.8/site-packages
        echo 'pymysql install successed'
        echo "pymysql install successed" >>$python3_thirdlib_log
        echo "pymysql" >>$python3_installed_hirdlib
    else
        echo "pymysql have installed"
    fi
    echo "Have install 3rd lib package: 73/$total_nums"
    set +e
    flag=$(grep "elasticsearch" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "elasticsearch begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        tar -xvzf elasticsearch-7.13.0.tar.gz > /dev/null
        cd elasticsearch-7.13.0
        python3 setup.py install >>$python3_thirdlib_log 2>&1
        echo 'elasticsearch install successed'
        echo "elasticsearch install successed" >>$python3_thirdlib_log
        echo "elasticsearch" >>$python3_installed_hirdlib
    else
        echo "elasticsearch have installed"
    fi
    echo "Have install 3rd lib package: 74/$total_nums"
    set +e
    flag=$(grep "openai" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "openai begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        pip3 install openai-1.75.0-py3-none-any.whl >>$python3_thirdlib_log 2>&1
        echo 'openai install successed'
        echo "openai install successed" >>$python3_thirdlib_log
        echo "openai" >>$python3_installed_hirdlib
    else
        echo "openai have installed"
    fi
    echo "Have install 3rd lib package: 75/$total_nums"
    set +e
    flag=$(grep "sqlglot" $python3_installed_hirdlib)
    set -e
    if [ -z "$flag" ]; then
        echo "sqlglot begin install" >>$python3_thirdlib_log
        cd $python3_lib_dir
        pip3 install sqlglot-26.15.0-py3-none-any.whl
        echo 'sqlglot install successed'
        echo "sqlglot install successed" >>$python3_thirdlib_log
        echo "sqlglot" >>$python3_installed_hirdlib
    else
        echo "sqlglot have installed"
    fi
    echo "Have install 3rd lib package: 76/$total_nums"
    if [ -z $upgrade ];then
        for ip in $ds_hosts
        do
            if [ "$localnode" != "$ip" ]; then
                echo "$ip:"
                ssh $ip "rm -rf /usr/software/python3"
                scp -r $python3_home $ip:/usr/software >/dev/null
                echo "$ip python3 lib install done"
            fi
        done
    fi
    echo "Python3 third lib install Successed!"
}

install_extra_yum() {
    for ip in $ds_hosts; do
        if [ $localnode == $ip ]; then
            echo "local node install DBAIOps extra package"
            cat /dev/null >$python3_rpm_log
            if [ -z "$cpu_version" ]; then
                echo "sshpass begin installl"
                echo "sshpass begin installl" >>$python3_rpm_log
                set +e
                flag=$(rpm -qa | grep sshpass)
                set -e
                if [ -z "$flag" ]; then
                    #	cd $python3_home;yum -y localinstall sshpass-1.06-2.el7.x86_64.rpm >> $python3_rpm_log 2>&1
                    cd $python3_home
                    tar --no-same-owner -xvzf sshpass-1.06.tar.gz >/dev/null 2>&1
                    cd sshpass-1.06
                    ./configure >>$python3_rpm_log 2>&1
                    make >>$python3_rpm_log 2>&1
                    make install >>$python3_rpm_log 2>&1
                    echo "sshpass install successed"
                    echo "sshpass install successed" >>$python3_rpm_log
                else
                    echo 'sshpass already installed'
                fi

                echo "mssql-tools begin install" >>$python3_rpm_log
                set +e
                cd $python3_home
                ACCEPT_EULA=Y rpm -ivh msodbcsql17-17.7.2.1-1.x86_64.rpm >>$python3_rpm_log 2>&1
                echo 'msodbcsql17 install successed'
                cd $python3_home
                ACCEPT_EULA=Y rpm -ivh mssql-tools-17.7.1.1-1.x86_64.rpm >>$python3_rpm_log 2>&1
                echo 'mssql-tools install successed'
                set -e
                sed -i "s@\$PYTHON3_HOME/bin@\$PYTHON3_HOME/bin:/opt/mssql-tools/bin@g" /etc/profile.d/python3.sh
                echo 'configure mssql-tools successed'
                echo "mssql-tools install successed" >>$python3_rpm_log
            else
                echo "sshpass begin installl" >>$python3_rpm_log
                cd $python3_home
                tar --no-same-owner -xvzf sshpass-1.06.tar.gz >/dev/null 2>&1
                cd sshpass-1.06
                ./configure >>$python3_rpm_log 2>&1
                make >>$python3_rpm_log 2>&1
                make install >>$python3_rpm_log 2>&1
                echo "sshpass install successed"
                echo "sshpass install successed" >>$python3_rpm_log
            fi
        else
            echo "$ip:"
            ssh $ip "cat /dev/null > $python3_rpm_log;cd $python3_home;tar --no-same-owner -xvzf sshpass-1.06.tar.gz > /dev/null 2>&1;cd sshpass-1.06;./configure >> $python3_rpm_log 2>&1;make >> $python3_rpm_log 2>&1;make install >> $python3_rpm_log 2>&1;echo 'sshpass install successed';echo 'sshpass install successed' >> $python3_rpm_log;echo 'mssql-tools begin install' >> $python3_rpm_log;cd $python3_home;yum -y localinstall msodbcsql17-17.7.2.1-1.x86_64.rpm >> $python3_rpm_log 2>&1;echo 'msodbcsql17 install successed';cd $python3_home;yum -y localinstall mssql-tools-17.7.1.1-1.x86_64.rpm >> $python3_rpm_log 2>&1;echo 'mssql-tools install successed';echo 'export PATH=\$PATH:/opt/mssql-tools/bin' >> /etc/profile.d/python3.sh; echo 'configure mssql-tools successed';echo 'mssql-tools install successed' >> $python3_rpm_log;"
        fi
    done
}

install_extra_apt() {
    for ip in $ds_hosts; do
        if [ $localnode == $ip ]; then
            echo "local node install DBAIOps extra package"
            cat /dev/null >$python3_rpm_log
            echo "sshpass begin installl" >>$python3_rpm_log
            cd $python3_home
            tar --no-same-owner -xvzf sshpass-1.06.tar.gz >/dev/null 2>&1
            cd sshpass-1.06
            ./configure >>$python3_rpm_log 2>&1
            make >>$python3_rpm_log 2>&1
            make install >>$python3_rpm_log 2>&1
            echo "sshpass install successed"
            echo "sshpass install successed" >>$python3_rpm_log
        else
            echo "$ip"
            ssh $ip "cat /dev/null > $python3_rpm_log;echo 'sshpass begin install' >> $python3_rpm_log;cd $python3_home;tar --no-same-owner -xvzf sshpass-1.06.tar.gz > /dev/null 2>&1;cd sshpass-1.06;./configure >> $python3_rpm_log 2>&1;make >> $python3_rpm_log 2>&1;make install >> $python3_rpm_log 2>&1;echo 'sshpass install successed';echo 'sshpass install successed' >> $python3_rpm_log"
        fi
    done
}

install_extra_zypper() {
    for ip in $ds_hosts; do
        if [ $localnode == $ip ]; then
            echo "local node install DBAIOps extra package"
            cat /dev/null >$python3_rpm_log
            echo "sshpass begin install" >>$python3_rpm_log
            cd $python3_home
            tar --no-same-owner -xvzf sshpass-1.06.tar.gz >/dev/null 2>&1
            cd sshpass-1.06
            ./configure >>$python3_rpm_log 2>&1
            make >>$python3_rpm_log 2>&1
            make install >>$python3_rpm_log 2>&1
            echo "sshpass install successed"
            echo "sshpass install successed" >>$python3_rpm_log
            cd $python3_home
            cp _bz2.cpython-34m.so $python3_home/lib/python3.8/lib-dynload/_bz2.cpython-38m-x86_64-linux-gnu.so
        else
            echo "$ip"
            ssh $ip "cat /dev/null > $python3_rpm_log;echo 'sshpass begin install' >> $python3_rpm_log;cd $python3_home;tar --no-same-owner -xvzf sshpass-1.06.tar.gz > /dev/null 2>&1;cd sshpass-1.06;./configure >> $python3_rpm_log 2>&1;make >> $python3_rpm_log 2>&1;make install >> $python3_rpm_log 2>&1;echo 'sshpass install successed';echo 'sshpass install successed' >> $python3_rpm_log"
        fi
    done
}

install_extra_package() {
    echo "############################################################"
    echo "                 install DBAIOps extra package                     "
    echo "############################################################"
    case $os_type in
    "redhat")
        install_extra_yum
        ;;
    "centos")
        install_extra_yum
        ;;
    "uos")
        install_extra_apt
        ;;
    "kylinV4")
        install_extra_apt
        ;;
    "kylinV10")
        install_extra_yum
        ;;
    "suse")
        install_extra_zypper
        ;;
    *)
        echo "invalid os type,please confirm your os type and execute again."
        exit 1
        ;;
    esac
    if [ "$ip" == "$ds_web" ]; then
        if [ $localnode == $ip ]; then
            source /etc/profile.d/python3.sh
            source /etc/profile.d/java.sh
            cd $python3_home
            python3 mustdo.py | xargs echo -n >/usr/software/webserver/conf/web.conf
        else
            ssh $ip "source /etc/profile.d/python3.sh;source /etc/profile.d/java.sh;cd $python3_home;python3 mustdo.py|xargs echo -n > /usr/software/webserver/conf/web.conf"
        fi
    fi
    echo "DBAIOps extra package install Successed!"
}

webcfg() {
    i=0
    for ip in $ds_hosts; do
        let i+=1
    done
    if [ $i -eq 1 ]; then
        rm -rf /tmp/web.conf
        cd $python3_home
        python3 mustdo.py | xargs echo -n >/tmp/web.conf
        echo -n " $i" >>/tmp/web.conf
        cat /tmp/web.conf | xargs java -jar /usr/software/return/lib/FstaskEnTool.jar >/usr/software/webserver/conf/web.conf
    else
        rm -rf /tmp/web.conf
        for ip in $ds_hosts; do
            ssh $ip "cd $python3_home;python3 mustdo.py > /tmp/do.conf"
            scp $ip:/tmp/do.conf /tmp/$ip.conf
            cat /tmp/$ip.conf | xargs echo -n >>/tmp/web.conf
            ssh $ip "echo '' > /tmp/conf"
            echo "" >/tmp/$ip.conf
        done
        echo -n " $i" >>/tmp/web.conf
        cat /tmp/web.conf | xargs java -jar /usr/software/return/lib/FstaskEnTool.jar >/usr/software/webserver/conf/web.conf
    fi
}

if [ ! -f $CONF/role.cfg ]; then
    echo "There is no role.cfg in $CONF"
    exit 1
else
    . $CONF/role.cfg
fi

ds_hosts=$(awk -F '=' '/^DS_Web|^DS_Collector|^DS_Monitor|^DS_Logana|^DS_Fstask|^DS_Other_Executor|^DS_Zookeeper|^DS_Redis/ {print $2}' $CONF/role.cfg | tr -s '\n' | tr ',' '\n' | sort -u)
ds_web=$(awk -F '=' '/^DS_Web/ {print $2}' $CONF/role.cfg)
os_release=$(cat /etc/os-release | grep "^ID=" | awk -F "=" '{print $2}')
set +e
uos_flag=$(echo $os_release | grep -i uos)
set -e
if [ -z $uos_flag ]; then
    uos_len=0
else
    uos_len=${#uos_flag}
fi

if [ -z $python3_home ]; then
    echo "python3安装目录不存在！"
    exit 1
fi

if [ -f /usr/software/bin/logs/os_type.txt ]; then
    os_type=$(cat /usr/software/bin/logs/os_type.txt)
    if [ -z "$os_type" ]; then
        echo "please execute DBAIOps-system-package.sh first!"
        exit 1
    fi
else
    echo "please execute DBAIOps-system-package.sh first!"
    exit 1
fi
set +e
flag_suse=$(echo $os_type | grep -i suse)
flag_yum=$(echo $os_type | grep -iE 'redhat|centos')
flag_apt=$(echo $os_type | grep -iE 'uos|kylinV4')
set -e

case $1 in
"-install")
    install $ds_hosts
    ;;
"-install_thirdlib")
    upgrade=$2
    install_thirdlib $ds_hosts
    ;;
"-install_rpm")
    install_extra_package $ds_hosts
    ;;
*)
    print_usage
    exit 1
    ;;
esac

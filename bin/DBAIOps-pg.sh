#!/bin/bash
# 安装数据库
#
#

bin=`dirname "${BASH_SOURCE-$0}"`
bin=`cd "$bin"; pwd`
ROOT=`cd $bin;cd ..;pwd`
DBAIOps_oper_dir=/usr/software
DBAIOps_HOME=`awk -F '=' '/^DS_BASE_LOCALTION/ {print $2}' $DBAIOps_oper_dir/role.cfg`
PG_CONF=`cd $bin;cd ../pgconf;pwd`
CONF=$DBAIOps_HOME
localips=$(hostname -I)
host=`hostname`

#如果目录不存在，则创建目录
if [ ! -d "$DBAIOps_oper_dir/bin/logs" ]; then
    mkdir -p $DBAIOps_oper_dir/bin/logs
fi
installpg_log=$DBAIOps_oper_dir/bin/logs/DBAIOps_pg.log

# 获取主脚本中的语言设置
if [ -z "$LANGUAGE" ]; then
    LANGUAGE="en"  # 默认英文
fi


c1() {
    RED_COLOR='\E[1;31m'
    GREEN_COLOR='\E[1;32m'
    YELLOW_COLOR='\E[1;33m'
    BLUE_COLOR='\E[1;34m'
    PINK_COLOR='\E[1;35m'
    WHITE_BLUE='\E[47;34m'
    DOWN_BLUE='\E[4;36m'
    FLASH_RED='\E[5;31m'
    RES='\E[0m'

    if [ $# -ne 2 ]; then
        echo "Usage $0 content {red|yellow|blue|green|pink|wb|db|fr}"
        exit
    fi

    case "$2" in
    red | RED)
        echo -e "${RED_COLOR}$1${RES}"
        ;;
    yellow | YELLOW)
        echo -e "${YELLOW_COLOR}$1${RES}"
        ;;
    green | GREEN)
        echo -e "${GREEN_COLOR}$1${RES}"
        ;;
    blue | BLUE)
        echo -e "${BLUE_COLOR}$1${RES}"
        ;;
    pink | PINK)
        echo -e "${PINK_COLOR}$1${RES}"
        ;;
    wb | WB)
        echo -e "${WHITE_BLUE}$1${RES}"
        ;;
    db | DB)
        echo -e "${DOWN_BLUE}$1${RES}"
        ;;
    fr | FR)
        echo -e "${FLASH_RED}$1${RES}"
        ;;
    *)
        echo -e "Please enter the specified color code：{red|yellow|blue|green|pink|wb|db|fr}"
        ;;
    esac
}

print_usage(){
    echo "Usage: DBAIOps postgresql installation script"
    echo "< -install nodes| -initdb | -start nodes | -stop nodes | -status nodes | -clean >"
    echo "  -install MasterNode,SlaveNode               install postgresql environment"
    echo "  -initdb                 init postgresql database"
    echo "  -start                  start postgresql service"
    echo "  -stop                   stop postgresql service"
    echo "  -status                 check postgresql service"
    echo "  -clean                  clean postgresql service"
}


# 获取主脚本中的语言设置
if [ -z "$LANGUAGE" ]; then
    LANGUAGE="en"  # 默认英文
fi

# 根据语言设置定义提示信息
if [ "$LANGUAGE" = "cn" ]; then
    MSG_INSTALL_TITLE="正在安装 CMake"
    MSG_INSTALL_SUCCESS="CMake 安装成功！"
    MSG_INSTALL_FAIL="CMake 安装失败，请查看日志文件：$installpg_log"
    MSG_LOG_PATH="日志文件路径：$installpg_log"
    MSG_ALREADY_INSTALLED="CMake 已安装，版本 $cmake_version 大于 3.15"
else
    MSG_INSTALL_TITLE="Installing CMake"
    MSG_INSTALL_SUCCESS="CMake installation succeeded!"
    MSG_INSTALL_FAIL="CMake installation failed, please check log file: $installpg_log"
    MSG_LOG_PATH="Log file path: $installpg_log"
    MSG_ALREADY_INSTALLED="CMake already installed, version $cmake_version is greater than 3.15"
fi

# 日志函数
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> $installpg_log
}

# 错误处理函数
error_exit() {
    local error_message=$1
    log "Error: $error_message"
    if [ "$LANGUAGE" = "cn" ]; then
        echo "Postgres DBAIOps 初始化失败，请查看日志文件：$installpg_log"
        echo "日志文件路径：$installpg_log"
    else
        echo "Postgres DBAIOps initialization failed, please check log file: $installpg_log"
        echo "Log file path: $installpg_log"
    fi
    exit 1
}
# 本地安装 CMake
install_cmake_local() {
    log "$MSG_INSTALL_TITLE (本地)"
    echo "$MSG_INSTALL_TITLE (本地)"

    # 复制 CMake 安装包到 /tmp
    \cp "$DBAIOps_oper_dir/cmake-3.17.3.tar.gz" /tmp || error_exit "Failed to copy CMake archive to /tmp."

    # 解压 CMake 安装包
    cd /tmp && tar --no-same-owner -xvzf /tmp/cmake-3.17.3.tar.gz > /dev/null 2>&1 || error_exit "Failed to extract CMake archive."

    # 进入 CMake 目录并编译安装
    cd /tmp/cmake-3.17.3 || error_exit "Failed to enter CMake source directory."
    ./configure --prefix=/usr >> $installpg_log 2>&1 || error_exit "Failed to configure CMake."
    make >> $installpg_log 2>&1 || error_exit "Failed to build CMake."
    make install >> $installpg_log 2>&1 || error_exit "Failed to install CMake."

    # 验证安装
    cmake --version >> $installpg_log 2>&1 || error_exit "Failed to verify CMake installation."

    log "$MSG_INSTALL_SUCCESS"
    echo "$MSG_INSTALL_SUCCESS"
}

# 远程安装 CMake
install_cmake_remote() {
    local remote_node=$1
    log "$MSG_INSTALL_TITLE (远程: $remote_node)"
    echo "$MSG_INSTALL_TITLE (远程: $remote_node)"

    # 复制 CMake 安装包到远程节点的 /tmp
    scp -q "$DBAIOps_oper_dir/cmake-3.17.3.tar.gz" "$remote_node:/tmp" || error_exit "Failed to copy CMake archive to $remote_node."

    # 在远程节点解压、编译和安装 CMake
    ssh "$remote_node" "
        cd /tmp && tar --no-same-owner -xvzf /tmp/cmake-3.17.3.tar.gz > /dev/null 2>&1 || exit 1;
        cd /tmp/cmake-3.17.3 || exit 1;
        ./configure --prefix=/usr >> $installpg_log 2>&1 || exit 1;
        make >> $installpg_log 2>&1 || exit 1;
        make install >> $installpg_log 2>&1 || exit 1;
        cmake --version >> $installpg_log 2>&1 || exit 1;
    " || error_exit "Failed to install CMake on $remote_node."

    log "$MSG_INSTALL_SUCCESS (远程: $remote_node)"
    echo "$MSG_INSTALL_SUCCESS (远程: $remote_node)"
}

# 安装 CMake（主逻辑）
install_cmake() {
    local node=$1
    if echo "$localips" | grep -wq "$node"; then
        # 本地节点
        cmake_use_flag=$(which cmake 2>/dev/null)
        if [ -z "$cmake_use_flag" ]; then
            install_cmake_local
        else
            cmake_version=$(cmake --version | grep version | awk '{print $3}')
            cmake_main_version=$(echo "$cmake_version" | awk -F "." '{print $1}')
            cmake_second_version=$(echo "$cmake_version" | awk -F "." '{print $2}')
            if [ "$cmake_main_version" -eq 3 ] && [ "$cmake_second_version" -gt 15 ]; then
                echo "$MSG_ALREADY_INSTALLED"
            else
                install_cmake_local
            fi
        fi
    else
        # 远程节点
        cmake_use_flag=$(ssh "$node" "which cmake 2>/dev/null")
        if [ -z "$cmake_use_flag" ]; then
            install_cmake_remote "$node"
        else
            cmake_version=$(ssh "$node" "cmake --version" | grep version | awk '{print $3}')
            cmake_main_version=$(echo "$cmake_version" | awk -F "." '{print $1}')
            cmake_second_version=$(echo "$cmake_version" | awk -F "." '{print $2}')
            if [ "$cmake_main_version" -eq 3 ] && [ "$cmake_second_version" -gt 15 ]; then
                echo "$node: $MSG_ALREADY_INSTALLED"
            else
                install_cmake_remote "$node"
            fi
        fi
    fi
}

# 安装 pg_cron
install_pg_cron() {
    # 提示信息
    if [ "$LANGUAGE" = "cn" ]; then
        local install_title="正在安装 pg_cron"
        local restart_pg="正在重启 PostgreSQL"
        local create_extension="正在创建 pg_cron 扩展"
        local schedule_jobs="正在配置定时任务"
        local install_success="pg_cron 安装成功！"
    else
        local install_title="Installing pg_cron"
        local restart_pg="Restarting PostgreSQL"
        local create_extension="Creating pg_cron extension"
        local schedule_jobs="Scheduling jobs"
        local install_success="pg_cron installation succeeded!"
    fi

    log "$install_title"
    echo "$install_title"

    # 创建定时任务 SQL 文件
    echo "SELECT cron.schedule('compress timescaledb hypertables before 7 days', '* 12 * * *', 'select auto_compress_chunk()');" > /tmp/pg_cron.sql
    # echo "SELECT cron.schedule('drop timescaledb hypertables before system keep time', '* 12 * * *', 'select auto_drop_chunk()');" >> /tmp/pg_cron.sql
    chmod 777 /tmp/pg_cron.sql

    if echo "$localips" | grep -wq "$mnd"; then
        # 本地节点
        log "$restart_pg"
        echo "$restart_pg"
        su - "$PG_OS_USER" -c "$PG_PATH/pg_ctl restart -D $PG_DATA_PATH" >> $installpg_log 2>&1 || error_exit "Failed to restart PostgreSQL."

        log "$create_extension"
        echo "$create_extension"
        su - "$PG_OS_USER" -c "psql -U $PG_OS_USER -d $pgDBAIOpsdb -p $pgport -c 'create extension pg_cron;'" >> $installpg_log 2>&1 || error_exit "Failed to create pg_cron extension."

        log "$schedule_jobs"
        echo "$schedule_jobs"
        su - "$PG_OS_USER" -c "psql -U $PG_OS_USER -d $pgDBAIOpsdb -p $pgport < /tmp/pg_cron.sql" >> $installpg_log 2>&1 || error_exit "Failed to schedule jobs."
    else
        # 远程节点
        log "$restart_pg (远程: $mnd)"
        echo "$restart_pg (远程: $mnd)"
        ssh "$mnd" "su - $PG_OS_USER -c \"$PG_PATH/pg_ctl restart -D $PG_DATA_PATH\" >> $installpg_log 2>&1" || error_exit "Failed to restart PostgreSQL on $mnd."

        log "$create_extension (远程: $mnd)"
        echo "$create_extension (远程: $mnd)"
        ssh "$mnd" "su - $PG_OS_USER -c \"psql -U $PG_OS_USER -d $pgDBAIOpsdb -p $pgport -c 'create extension pg_cron;'\" >> $installpg_log 2>&1" || error_exit "Failed to create pg_cron extension on $mnd."

        log "$schedule_jobs (远程: $mnd)"
        echo "$schedule_jobs (远程: $mnd)"
        scp -q /tmp/pg_cron.sql "$mnd:/tmp" || error_exit "Failed to copy pg_cron.sql to $mnd."
        ssh "$mnd" "chmod 777 /tmp/pg_cron.sql" || error_exit "Failed to set permissions on pg_cron.sql on $mnd."
        ssh "$mnd" "su - $PG_OS_USER -c \"psql -U $PG_OS_USER -d $pgDBAIOpsdb -p $pgport < /tmp/pg_cron.sql\" >> $installpg_log 2>&1" || error_exit "Failed to schedule jobs on $mnd."
    fi

    log "$install_success"
    echo "$install_success"
}

# 初始化 PostgreSQL 数据库
initdb_m() {
    # 提示信息
    if [ "$LANGUAGE" = "cn" ]; then
        local init_title="正在初始化 PostgreSQL 数据库"
        local copy_sql="正在复制 SQL 文件到 /tmp"
        local create_db="正在创建数据库"
        local execute_sql="正在执行 SQL 脚本"
        local restart_pg="正在重启 PostgreSQL"
        local init_success="Postgres DBAIOps 初始化成功！"
    else
        local init_title="Initializing PostgreSQL database"
        local copy_sql="Copying SQL files to /tmp"
        local create_db="Creating database"
        local execute_sql="Executing SQL scripts"
        local restart_pg="Restarting PostgreSQL"
        local init_success="Postgres DBAIOps initialization succeeded!"
    fi

    log "$init_title"
    echo "$init_title"

    if echo "$localips" | grep -wq "$mnd"; then
        # 本地节点
        log "$copy_sql"
        echo "$copy_sql"
        \cp "$DBAIOps_oper_dir/DBAIOps_2018.sql" /tmp || error_exit "Failed to copy DBAIOps_2018.sql to /tmp."
        \cp "$DBAIOps_oper_dir/fstask_tables_postgres.sql" /tmp || error_exit "Failed to copy fstask_tables_postgres.sql to /tmp."
        chmod 644 /tmp/DBAIOps_2018.sql || error_exit "Failed to set permissions on DBAIOps_2018.sql."
        chmod 644 /tmp/fstask_tables_postgres.sql || error_exit "Failed to set permissions on fstask_tables_postgres.sql."

        log "$create_db: $pgDBAIOpsdb"
        echo "$create_db: $pgDBAIOpsdb"
        su - "$PG_OS_USER" -c "$PG_PATH/createdb $pgDBAIOpsdb -p $pgport" >> $installpg_log 2>&1 || error_exit "Failed to create database $pgDBAIOpsdb."

        log "$execute_sql: DBAIOps_2018.sql"
        echo "$execute_sql: DBAIOps_2018.sql"
        su - "$PG_OS_USER" -c "$PG_PATH/psql -p $pgport -U $PG_OS_USER -d $pgDBAIOpsdb -f /tmp/DBAIOps_2018.sql" >> $installpg_log 2>&1 || error_exit "Failed to execute DBAIOps_2018.sql."

        log "$create_db: $pgfsdb"
        echo "$create_db: $pgfsdb"
        su - "$PG_OS_USER" -c "$PG_PATH/createdb $pgfsdb -p $pgport" >> $installpg_log 2>&1 || error_exit "Failed to create database $pgfsdb."

        log "$execute_sql: fstask_tables_postgres.sql"
        echo "$execute_sql: fstask_tables_postgres.sql"
        su - "$PG_OS_USER" -c "$PG_PATH/psql -p $pgport -U $PG_OS_USER -d $pgfsdb -f /tmp/fstask_tables_postgres.sql" >> $installpg_log 2>&1 || error_exit "Failed to execute fstask_tables_postgres.sql."

        log "$restart_pg"
        echo "$restart_pg"
        su - "$PG_OS_USER" -c "$PG_PATH/pg_ctl restart -D $PG_DATA_PATH" >> $installpg_log 2>&1 || error_exit "Failed to restart PostgreSQL."
    else
        # 远程节点
        log "$copy_sql (远程: $mnd)"
        echo "$copy_sql (远程: $mnd)"
        scp -q "$DBAIOps_oper_dir/DBAIOps_2018.sql" "$mnd:/tmp" || error_exit "Failed to copy DBAIOps_2018.sql to $mnd."
        scp -q "$DBAIOps_oper_dir/fstask_tables_postgres.sql" "$mnd:/tmp" || error_exit "Failed to copy fstask_tables_postgres.sql to $mnd."
        ssh "$mnd" "chmod 644 /tmp/DBAIOps_2018.sql" || error_exit "Failed to set permissions on DBAIOps_2018.sql on $mnd."
        ssh "$mnd" "chmod 644 /tmp/fstask_tables_postgres.sql" || error_exit "Failed to set permissions on fstask_tables_postgres.sql on $mnd."

        log "$create_db: $pgDBAIOpsdb (远程: $mnd)"
        echo "$create_db: $pgDBAIOpsdb (远程: $mnd)"
        ssh "$mnd" "su - $PG_OS_USER -c \"$PG_PATH/createdb $pgDBAIOpsdb -p $pgport\" >> $installpg_log 2>&1" || error_exit "Failed to create database $pgDBAIOpsdb on $mnd."

        log "$execute_sql: DBAIOps_2018.sql (远程: $mnd)"
        echo "$execute_sql: DBAIOps_2018.sql (远程: $mnd)"
        ssh "$mnd" "su - $PG_OS_USER -c \"$PG_PATH/psql -p $pgport -U $PG_OS_USER -d $pgDBAIOpsdb -f /tmp/DBAIOps_2018.sql\" >> $installpg_log 2>&1" || error_exit "Failed to execute DBAIOps_2018.sql on $mnd."

        log "$create_db: $pgfsdb (远程: $mnd)"
        echo "$create_db: $pgfsdb (远程: $mnd)"
        ssh "$mnd" "su - $PG_OS_USER -c \"$PG_PATH/createdb $pgfsdb -p $pgport\" >> $installpg_log 2>&1" || error_exit "Failed to create database $pgfsdb on $mnd."

        log "$execute_sql: fstask_tables_postgres.sql (远程: $mnd)"
        echo "$execute_sql: fstask_tables_postgres.sql (远程: $mnd)"
        ssh "$mnd" "su - $PG_OS_USER -c \"$PG_PATH/psql -p $pgport -U $PG_OS_USER -d $pgfsdb -f /tmp/fstask_tables_postgres.sql\" >> $installpg_log 2>&1" || error_exit "Failed to execute fstask_tables_postgres.sql on $mnd."

        log "$restart_pg (远程: $mnd)"
        echo "$restart_pg (远程: $mnd)"
        ssh "$mnd" "su - $PG_OS_USER -c \"$PG_PATH/pg_ctl restart -D $PG_DATA_PATH\" >> $installpg_log 2>&1" || error_exit "Failed to restart PostgreSQL on $mnd."
    fi

    log "$init_success"
    echo "$init_success"
}


# 安装 PostgreSQL 扩展
install_extension_m() {
    # 提示信息
    if [ "$LANGUAGE" = "cn" ]; then
        local install_title="正在安装 PostgreSQL 扩展"
        local install_cmake="正在安装 CMake"
        local copy_files="正在复制扩展文件到 /tmp"
        local build_timescaledb="正在编译和安装 TimescaleDB"
        local build_pgfincore="正在编译和安装 pgfincore"
        local restart_pg="正在重启 PostgreSQL"
        local create_timescaledb="正在创建 TimescaleDB 扩展"
        local create_pgfincore="正在创建 pgfincore 扩展"
        local install_success="PostgreSQL 扩展安装成功！"
    else
        local install_title="Installing PostgreSQL extensions"
        local install_cmake="Installing CMake"
        local copy_files="Copying extension files to /tmp"
        local build_timescaledb="Building and installing TimescaleDB"
        local build_pgfincore="Building and installing pgfincore"
        local restart_pg="Restarting PostgreSQL"
        local create_timescaledb="Creating TimescaleDB extension"
        local create_pgfincore="Creating pgfincore extension"
        local install_success="PostgreSQL extensions installation succeeded!"
    fi

    log "$install_title"
    echo "$install_title"

    # 安装 CMake
    log "$install_cmake"
    echo "$install_cmake"
    export LD_LIBRARY_PATH=""
    install_cmake "$mnd" || error_exit "Failed to install CMake."

    if echo "$localips" | grep -wq "$mnd"; then
        # 本地节点
        log "$copy_files"
        echo "$copy_files"
        \cp "$DBAIOps_oper_dir/timescaledb-2.14.2.zip" /tmp || error_exit "Failed to copy timescaledb-2.14.2.zip to /tmp."
        \cp "$DBAIOps_oper_dir/pg_cron-1.6.2.zip" /tmp || error_exit "Failed to copy pg_cron-1.6.2.zip to /tmp."
        \cp "$DBAIOps_oper_dir/pgfincore-1.3.1.zip" /tmp || error_exit "Failed to copy pgfincore-1.3.1.zip to /tmp."

        # 编译和安装 TimescaleDB
        log "$build_timescaledb"
        echo "$build_timescaledb"
        cd /tmp && if [ -d /tmp/timescaledb-2.14.2 ]; then rm -rf /tmp/timescaledb-2.14.2; fi
        unzip -o /tmp/timescaledb-2.14.2.zip > /dev/null 2>&1 || error_exit "Failed to unzip timescaledb-2.14.2.zip."
        cd /tmp/timescaledb-2.14.2 || error_exit "Failed to enter timescaledb-2.14.2 directory."
        ./bootstrap -DUSE_OPENSSL=0 -DREGRESS_CHECKS=OFF >> $installpg_log 2>&1 || error_exit "Failed to bootstrap TimescaleDB."
        cd /tmp/timescaledb-2.14.2/build && make >> $installpg_log 2>&1 || error_exit "Failed to build TimescaleDB."
        make install >> $installpg_log 2>&1 || error_exit "Failed to install TimescaleDB."

        # 编译和安装 pgfincore
        log "$build_pgfincore"
        echo "$build_pgfincore"
        cd /tmp && if [ -d /tmp/pgfincore-1.3.1 ]; then rm -rf /tmp/pgfincore-1.3.1; fi
        unzip -o /tmp/pgfincore-1.3.1.zip > /dev/null 2>&1 || error_exit "Failed to unzip pgfincore-1.3.1.zip."
        cd /tmp/pgfincore-1.3.1 && make >> $installpg_log 2>&1 || error_exit "Failed to build pgfincore."
        make install >> $installpg_log 2>&1 || error_exit "Failed to install pgfincore."

        # 重启 PostgreSQL
        log "$restart_pg"
        echo "$restart_pg"
        su - "$PG_OS_USER" -c "$PG_PATH/pg_ctl restart -D $PG_DATA_PATH" >> $installpg_log 2>&1 || error_exit "Failed to restart PostgreSQL."

        # 创建 TimescaleDB 扩展
        log "$create_timescaledb"
        echo "$create_timescaledb"
        su - "$PG_OS_USER" -c "psql -U $PG_OS_USER -d template1 -p $pgport -c 'create extension timescaledb;'" >> $installpg_log 2>&1 || error_exit "Failed to create TimescaleDB extension."

        # 创建 pgfincore 扩展
        log "$create_pgfincore"
        echo "$create_pgfincore"
        su - "$PG_OS_USER" -c "psql -U $PG_OS_USER -d template1 -p $pgport -c 'create extension pgfincore;'" >> $installpg_log 2>&1 || error_exit "Failed to create pgfincore extension."
    else
        # 远程节点
        log "$copy_files (远程: $mnd)"
        echo "$copy_files (远程: $mnd)"
        scp -q "$DBAIOps_oper_dir/timescaledb-2.14.2.zip" "$mnd:/tmp" || error_exit "Failed to copy timescaledb-2.14.2.zip to $mnd."
        scp -q "$DBAIOps_oper_dir/pgfincore-1.3.1.zip" "$mnd:/tmp" || error_exit "Failed to copy pgfincore-1.3.1.zip to $mnd."

        # 编译和安装 TimescaleDB
        log "$build_timescaledb (远程: $mnd)"
        echo "$build_timescaledb (远程: $mnd)"
        ssh "$mnd" "
            cd /tmp && if [ -d /tmp/timescaledb-2.14.2 ]; then rm -rf /tmp/timescaledb-2.14.2; fi
            unzip -o /tmp/timescaledb-2.14.2.zip > /dev/null 2>&1 || exit 1
            cd /tmp/timescaledb-2.14.2 || exit 1
            ./bootstrap -DUSE_OPENSSL=0 -DREGRESS_CHECKS=OFF >> $installpg_log 2>&1 || exit 1
            cd /tmp/timescaledb-2.14.2/build && make >> $installpg_log 2>&1 || exit 1
            make install >> $installpg_log 2>&1 || exit 1
        " || error_exit "Failed to build and install TimescaleDB on $mnd."

        # 编译和安装 pgfincore
        log "$build_pgfincore (远程: $mnd)"
        echo "$build_pgfincore (远程: $mnd)"
        ssh "$mnd" "
            cd /tmp && if [ -d /tmp/pgfincore-1.3.1 ]; then rm -rf /tmp/pgfincore-1.3.1; fi
            unzip -o /tmp/pgfincore-1.3.1.zip > /dev/null 2>&1 || exit 1
            cd /tmp/pgfincore-1.3.1 && make >> $installpg_log 2>&1 || exit 1
            make install >> $installpg_log 2>&1 || exit 1
        " || error_exit "Failed to build and install pgfincore on $mnd."

        # 重启 PostgreSQL
        log "$restart_pg (远程: $mnd)"
        echo "$restart_pg (远程: $mnd)"
        ssh "$mnd" "su - $PG_OS_USER -c \"$PG_PATH/pg_ctl restart -D $PG_DATA_PATH\" >> $installpg_log 2>&1" || error_exit "Failed to restart PostgreSQL on $mnd."

        # 创建 TimescaleDB 扩展
        log "$create_timescaledb (远程: $mnd)"
        echo "$create_timescaledb (远程: $mnd)"
        ssh "$mnd" "su - $PG_OS_USER -c \"psql -U $PG_OS_USER -d template1 -p $pgport -c 'create extension timescaledb;'\" >> $installpg_log 2>&1" || error_exit "Failed to create TimescaleDB extension on $mnd."

        # 创建 pgfincore 扩展
        log "$create_pgfincore (远程: $mnd)"
        echo "$create_pgfincore (远程: $mnd)"
        ssh "$mnd" "su - $PG_OS_USER -c \"psql -U $PG_OS_USER -d template1 -p $pgport -c 'create extension pgfincore;'\" >> $installpg_log 2>&1" || error_exit "Failed to create pgfincore extension on $mnd."
    fi

    log "$install_success"
    echo "$install_success"
}

# 安装 PostgreSQL 扩展（从节点）
install_extension_s() {
    # 提示信息
    if [ "$LANGUAGE" = "cn" ]; then
        local install_title="正在安装 PostgreSQL 扩展"
        local install_cmake="正在安装 CMake"
        local copy_files="正在复制扩展文件到 /tmp"
        local build_timescaledb="正在编译和安装 TimescaleDB"
        local build_pgfincore="正在编译和安装 pgfincore"
        local install_pg_cron="正在安装 pg_cron"
        local install_success="PostgreSQL 扩展安装成功！"
    else
        local install_title="Installing PostgreSQL extensions"
        local install_cmake="Installing CMake"
        local copy_files="Copying extension files to /tmp"
        local build_timescaledb="Building and installing TimescaleDB"
        local build_pgfincore="Building and installing pgfincore"
        local install_pg_cron="Installing pg_cron"
        local install_success="PostgreSQL extensions installation succeeded!"
    fi

    log "$install_title"
    echo "$install_title"

    # 安装 CMake
    log "$install_cmake"
    echo "$install_cmake"
    export LD_LIBRARY_PATH=""
    install_cmake "$sld" || error_exit "Failed to install CMake."

    if echo "$localips" | grep -wq "$sld"; then
        # 本地节点
        log "$copy_files"
        echo "$copy_files"
        \cp "$DBAIOps_oper_dir/timescaledb-2.14.2.zip" /tmp || error_exit "Failed to copy timescaledb-2.14.2.zip to /tmp."
        \cp "$DBAIOps_oper_dir/pgfincore-1.3.1.zip" /tmp || error_exit "Failed to copy pgfincore-1.3.1.zip to /tmp."

        # 编译和安装 TimescaleDB
        log "$build_timescaledb"
        echo "$build_timescaledb"
        cd /tmp && if [ -d /tmp/timescaledb-2.14.2 ]; then rm -rf /tmp/timescaledb-2.14.2; fi
        unzip -o /tmp/timescaledb-2.14.2.zip > /dev/null 2>&1 || error_exit "Failed to unzip timescaledb-2.14.2.zip."
        cd /tmp/timescaledb-2.14.2 || error_exit "Failed to enter timescaledb-2.14.2 directory."
        ./bootstrap -DUSE_OPENSSL=0 -DREGRESS_CHECKS=OFF >> $installpg_log 2>&1 || error_exit "Failed to bootstrap TimescaleDB."
        cd /tmp/timescaledb-2.14.2/build && make >> $installpg_log 2>&1 || error_exit "Failed to build TimescaleDB."
        make install >> $installpg_log 2>&1 || error_exit "Failed to install TimescaleDB."
        log "TimescaleDB 扩展安装成功"
        echo "TimescaleDB 扩展安装成功"

        # 编译和安装 pgfincore
        log "$build_pgfincore"
        echo "$build_pgfincore"
        cd /tmp && if [ -d /tmp/pgfincore-1.3.1 ]; then rm -rf /tmp/pgfincore-1.3.1; fi
        unzip -o /tmp/pgfincore-1.3.1.zip > /dev/null 2>&1 || error_exit "Failed to unzip pgfincore-1.3.1.zip."
        cd /tmp/pgfincore-1.3.1 && make >> $installpg_log 2>&1 || error_exit "Failed to build pgfincore."
        make install >> $installpg_log 2>&1 || error_exit "Failed to install pgfincore."
        log "pgfincore 扩展安装成功"
        echo "pgfincore 扩展安装成功"

        # 安装 pg_cron
        log "$install_pg_cron"
        echo "$install_pg_cron"
        \cp "$DBAIOps_oper_dir/pg_cron-1.6.2.zip" /tmp || error_exit "Failed to copy pg_cron-1.6.2.zip to /tmp."
        cd /tmp && if [ -d pg_cron-1.6.2 ]; then rm -rf /tmp/pg_cron-1.6.2; fi
        unzip -o /tmp/pg_cron-1.6.2.zip > /dev/null 2>&1 || error_exit "Failed to unzip pg_cron-1.6.2.zip."
        cd /tmp/pg_cron-1.6.2 && make >> $installpg_log 2>&1 || error_exit "Failed to build pg_cron."
        make install >> $installpg_log 2>&1 || error_exit "Failed to install pg_cron."
    else
        # 远程节点
        log "$copy_files (远程: $sld)"
        echo "$copy_files (远程: $sld)"
        scp -q "$DBAIOps_oper_dir/timescaledb-2.14.2.zip" "$sld:/tmp" || error_exit "Failed to copy timescaledb-2.14.2.zip to $sld."
        scp -q "$DBAIOps_oper_dir/pg_cron-1.6.2.zip" "$sld:/tmp" || error_exit "Failed to copy pg_cron-1.6.2.zip to $sld."
        scp -q "$DBAIOps_oper_dir/pgfincore-1.3.1.zip" "$sld:/tmp" || error_exit "Failed to copy pgfincore-1.3.1.zip to $sld."

        # 编译和安装 TimescaleDB
        log "$build_timescaledb (远程: $sld)"
        echo "$build_timescaledb (远程: $sld)"
        ssh "$sld" "
            cd /tmp && if [ -d /tmp/timescaledb-2.14.2 ]; then rm -rf /tmp/timescaledb-2.14.2; fi
            unzip -o /tmp/timescaledb-2.14.2.zip > /dev/null 2>&1 || exit 1
            cd /tmp/timescaledb-2.14.2 || exit 1
            ./bootstrap -DUSE_OPENSSL=0 -DREGRESS_CHECKS=OFF >> $installpg_log 2>&1 || exit 1
            cd /tmp/timescaledb-2.14.2/build && make >> $installpg_log 2>&1 || exit 1
            make install >> $installpg_log 2>&1 || exit 1
        " || error_exit "Failed to build and install TimescaleDB on $sld."
        log "TimescaleDB 扩展安装成功 (远程: $sld)"
        echo "TimescaleDB 扩展安装成功 (远程: $sld)"

        # 安装 pg_cron
        log "$install_pg_cron (远程: $sld)"
        echo "$install_pg_cron (远程: $sld)"
        ssh "$sld" "
            source /etc/profile.d/pg.sh
            cd /tmp && if [ -d pg_cron-1.6.2 ]; then rm -rf /tmp/pg_cron-1.6.2; fi
            unzip -o /tmp/pg_cron-1.6.2.zip > /dev/null 2>&1 || exit 1
            cd /tmp/pg_cron-1.6.2 && make >> $installpg_log 2>&1 || exit 1
            make install >> $installpg_log 2>&1 || exit 1
        " || error_exit "Failed to build and install pg_cron on $sld."

        # 编译和安装 pgfincore
        log "$build_pgfincore (远程: $sld)"
        echo "$build_pgfincore (远程: $sld)"
        ssh "$sld" "
            cd /tmp && if [ -d /tmp/pgfincore-1.3.1 ]; then rm -rf /tmp/pgfincore-1.3.1; fi
            unzip -o /tmp/pgfincore-1.3.1.zip > /dev/null 2>&1 || exit 1
            cd /tmp/pgfincore-1.3.1 && make >> $installpg_log 2>&1 || exit 1
            make install >> $installpg_log 2>&1 || exit 1
        " || error_exit "Failed to build and install pgfincore on $sld."
        log "pgfincore 扩展安装成功 (远程: $sld)"
        echo "pgfincore 扩展安装成功 (远程: $sld)"
    fi

    log "$install_success"
    echo "$install_success"
}

# 更新 libpq
update_libpq() {
    # 提示信息
    if [ "$LANGUAGE" = "cn" ]; then
        local update_title="正在更新 libpq"
        local copy_libpq="正在复制 libpq.so.5.16"
        local create_symlink="正在创建符号链接"
        local skip_pg_node="跳过 PostgreSQL 节点"
        local update_success="libpq 更新成功！"
    else
        local update_title="Updating libpq"
        local copy_libpq="Copying libpq.so.5.16"
        local create_symlink="Creating symbolic link"
        local skip_pg_node="Skipping PostgreSQL node"
        local update_success="libpq update succeeded!"
    fi

    log "$update_title"
    echo "$update_title"

    # 获取 PostgreSQL 主节点主机名
    if echo "$localips" | grep -wq "$mnd"; then
        pg_host=$(hostname)
        log "PostgreSQL 主节点: $pg_host"
        echo "PostgreSQL 主节点: $pg_host"

        # 删除旧版本并复制新版本
        log "$copy_libpq (本地)"
        echo "$copy_libpq (本地)"
        rm -rf /lib64/libpq.so.5.16 || error_exit "Failed to remove old libpq.so.5.16."
        cp "$PG_BASE/lib/libpq.so.5.16" /lib64 || error_exit "Failed to copy libpq.so.5.16 to /lib64."
    else
        pg_host=$(ssh "$mnd" "hostname") || error_exit "Failed to get hostname of PostgreSQL master node."
        log "PostgreSQL 主节点: $pg_host"
        echo "PostgreSQL 主节点: $pg_host"

        # 从主节点复制 libpq.so.5.16
        log "$copy_libpq (从 $mnd 复制)"
        echo "$copy_libpq (从 $mnd 复制)"
        scp "$mnd:$PG_BASE/lib/libpq.so.5.16" /lib64 || error_exit "Failed to copy libpq.so.5.16 from $mnd."

        # 创建符号链接
        log "$create_symlink (本地)"
        echo "$create_symlink (本地)"
        rm -rf /lib64/libpq.so.5 || error_exit "Failed to remove old libpq.so.5."
        ln -s /lib64/libpq.so.5.16 /lib64/libpq.so.5 || error_exit "Failed to create symbolic link for libpq.so.5."
    fi

    # 更新所有节点的 libpq
    for ip in $ds_hosts; do
        if [ "$ip" == "$pg_host" ]; then
            log "$skip_pg_node: $ip"
            echo "$skip_pg_node: $ip"
        elif [ "$ip" == "$host" ]; then
            log "$copy_libpq (本地)"
            echo "$copy_libpq (本地)"
            scp "$pg_host:/lib64/libpq.so.5.16" /lib64 || error_exit "Failed to copy libpq.so.5.16 to local node."

            log "$create_symlink (本地)"
            echo "$create_symlink (本地)"
            rm -rf /lib64/libpq.so.5 || error_exit "Failed to remove old libpq.so.5."
            ln -s /lib64/libpq.so.5.16 /lib64/libpq.so.5 || error_exit "Failed to create symbolic link for libpq.so.5."
        else
            log "$copy_libpq (远程: $ip)"
            echo "$copy_libpq (远程: $ip)"
            scp /lib64/libpq.so.5.16 "$ip:/lib64" || error_exit "Failed to copy libpq.so.5.16 to $ip."

            log "$create_symlink (远程: $ip)"
            echo "$create_symlink (远程: $ip)"
            ssh "$ip" "rm -rf /lib64/libpq.so.5; ln -s /lib64/libpq.so.5.16 /lib64/libpq.so.5" || error_exit "Failed to create symbolic link for libpq.so.5 on $ip."
        fi
    done

    log "$update_success"
    echo "$update_success"
}


# 安装 PostgreSQL 主节点
install_m() {
    # 提示信息
    if [ "$LANGUAGE" = "cn" ]; then
        local install_title="正在安装 PostgreSQL"
        local install_file_not_found="PostgreSQL 安装文件不存在！"
        local compiling="正在编译 PostgreSQL"
        local configuring="正在配置 PostgreSQL"
        local install_cron="正在安装 pg_cron"
        local install_extension="正在安装扩展"
        local initdb="正在初始化数据库"
        local update_libpq="正在更新 libpq"
        local install_success="PostgreSQL 安装成功！"
    else
        local install_title="Installing PostgreSQL"
        local install_file_not_found="PostgreSQL installation file not found!"
        local compiling="Compiling PostgreSQL"
        local configuring="Configuring PostgreSQL"
        local install_cron="Installing pg_cron"
        local install_extension="Installing extensions"
        local initdb="Initializing database"
        local update_libpq="Updating libpq"
        local install_success="PostgreSQL installation succeeded!"
    fi

    log "$install_title"
    echo "$install_title"

    # 检查安装文件是否存在
    if [ ! -f "$DBAIOps_oper_dir/postgresql-16.2.tar.gz" ]; then
        log "$install_file_not_found"
        echo "$install_file_not_found"
        exit 1
    fi

    if echo "$localips" | grep -wq "$mnd"; then
        # 本地节点
        log "$compiling (本地)"
        echo "$compiling (本地)"
        \cp "$DBAIOps_oper_dir/postgresql-16.2.tar.gz" /tmp || error_exit "Failed to copy PostgreSQL archive to /tmp."
        cd /tmp && tar --no-same-owner -xzvf /tmp/postgresql-16.2.tar.gz > /dev/null 2>&1 || error_exit "Failed to extract PostgreSQL archive."
        cd /tmp/postgresql-16.2 || error_exit "Failed to enter PostgreSQL source directory."
        ./configure --prefix="$PG_BASE" > $installpg_log 2>&1 || error_exit "Failed to configure PostgreSQL."
        make >> $installpg_log 2>&1 || error_exit "Failed to build PostgreSQL."
        make install >> $installpg_log 2>&1 || error_exit "Failed to install PostgreSQL."
        set +e
        useradd "$PG_OS_USER" -m >> $installpg_log 2>&1
        echo 'passw0rd!@#$' | passwd "$PG_OS_USER" --stdin >> $installpg_log 2>&1
        chmod -R 755 "$PG_BASE"
        mkdir -p "$PG_DATA_PATH" && chown -R "$PG_OS_USER" "$PG_DATA_PATH" && chmod -R 700 "$PG_DATA_PATH" || error_exit "Failed to set up PostgreSQL data directory."
        su - "$PG_OS_USER" -c "$PG_PATH/initdb -D $PG_DATA_PATH" >> $installpg_log 2>&1 || error_exit "Failed to initialize PostgreSQL database."
        su - "$PG_OS_USER" -c "$PG_PATH/pg_ctl start -D $PG_DATA_PATH" >> $installpg_log 2>&1 || error_exit "Failed to start PostgreSQL."

        # 配置环境变量
        echo "export PGDATA=$PG_DATA_PATH" > /etc/profile.d/pg.sh
        echo "export PG_HOME=$PG_PATH" >> /etc/profile.d/pg.sh
        echo "export PATH=\$PG_HOME:\$PATH" >> /etc/profile.d/pg.sh
        echo "export LD_LIBRARY_PATH=$PG_BASE/lib:/usr/lib64:/usr/lib:\$LD_LIBRARY_PATH" >> /etc/profile.d/pg.sh
        chmod 644 /etc/profile.d/pg.sh

        # 配置 PostgreSQL
        log "$configuring (本地)"
        echo "$configuring (本地)"
        \cp "$DBAIOps_oper_dir/pgconf/postgresql.conf" /tmp || error_exit "Failed to copy postgresql.conf to /tmp."
        sed -i "s/port = 5433/port = $pgport/g" /tmp/postgresql.conf || error_exit "Failed to update port in postgresql.conf."
        sed -i "s/cron.database_name='DBAIOps_2020'/cron.database_name='$pgDBAIOpsdb'/g" /tmp/postgresql.conf || error_exit "Failed to update cron database name in postgresql.conf."
        hostmem=$(cat /proc/meminfo | grep MemTotal | awk '{print $2}') || error_exit "Failed to get host memory."
        sharedmem=$((hostmem / 4096))
        sed -i "s/shared_buffers = 1024MB/shared_buffers = ${sharedmem}MB/g" /tmp/postgresql.conf || error_exit "Failed to update shared_buffers in postgresql.conf."
        connection_nums=$((fstask_cnt / 3 * 600 + 600))
        sed -i "s/max_connections = 600/max_connections = ${connection_nums}/g" /tmp/postgresql.conf || error_exit "Failed to update max_connections in postgresql.conf."
        \cp /tmp/postgresql.conf "$PG_DATA_PATH/postgresql.conf" || error_exit "Failed to copy postgresql.conf to data directory."
        \cp "$DBAIOps_oper_dir/pgconf/pg_hba.conf" "$PG_DATA_PATH/pg_hba.conf" || error_exit "Failed to copy pg_hba.conf to data directory."
        chown -R "$PG_OS_USER" "$PG_DATA_PATH/postgresql.conf" "$PG_DATA_PATH/pg_hba.conf" || error_exit "Failed to set permissions on configuration files."

        # 安装 pg_cron
        log "$install_cron (本地)"
        echo "$install_cron (本地)"
        \cp "$DBAIOps_oper_dir/pg_cron-1.6.2.zip" /tmp || error_exit "Failed to copy pg_cron archive to /tmp."
        source /etc/profile.d/pg.sh
        cd /tmp && if [ -d pg_cron-1.6.2 ]; then rm -rf /tmp/pg_cron-1.6.2; fi
        unzip -o /tmp/pg_cron-1.6.2.zip > /dev/null 2>&1 || error_exit "Failed to unzip pg_cron archive."
        cd /tmp/pg_cron-1.6.2 && make >> $installpg_log 2>&1 || error_exit "Failed to build pg_cron."
        make install >> $installpg_log 2>&1 || error_exit "Failed to install pg_cron."

        # 安装扩展
        log "$install_extension (本地)"
        echo "$install_extension (本地)"
        install_extension_m

        # 初始化数据库
        log "$initdb (本地)"
        echo "$initdb (本地)"
        initdb_m

        # 安装 pg_cron
        install_pg_cron
    else
        # 远程节点
        log "$compiling (远程: $mnd)"
        echo "$compiling (远程: $mnd)"
        scp -q "$DBAIOps_oper_dir/postgresql-16.2.tar.gz" "$mnd:/tmp" || error_exit "Failed to copy PostgreSQL archive to $mnd."
        ssh "$mnd" "
            cd /tmp && tar --no-same-owner -xzvf /tmp/postgresql-16.2.tar.gz > /dev/null 2>&1 || exit 1
            cd /tmp/postgresql-16.2 || exit 1
            ./configure --prefix=$PG_BASE > $installpg_log 2>&1 || exit 1
            make >> $installpg_log 2>&1 || exit 1
            make install >> $installpg_log 2>&1 || exit 1
            useradd $PG_OS_USER -m >> $installpg_log 2>&1 || exit 1
            echo 'passw0rd!@#$' | passwd $PG_OS_USER --stdin >> $installpg_log 2>&1
            chmod -R 755 $PG_BASE
            mkdir -p $PG_DATA_PATH && chown -R $PG_OS_USER $PG_DATA_PATH && chmod -R 700 $PG_DATA_PATH || exit 1
            su - $PG_OS_USER -c \"$PG_PATH/initdb -D $PG_DATA_PATH\" >> $installpg_log 2>&1 || exit 1
            su - $PG_OS_USER -c \"$PG_PATH/pg_ctl start -D $PG_DATA_PATH\" >> $installpg_log 2>&1 || exit 1
            echo \"export PGDATA=$PG_DATA_PATH\" > /etc/profile.d/pg.sh
            echo \"export PG_HOME=$PG_PATH\" >> /etc/profile.d/pg.sh
            echo \"export PATH=\\\$PG_HOME:\\\$PATH\" >> /etc/profile.d/pg.sh
            echo \"export LD_LIBRARY_PATH=$PG_BASE/lib:/usr/lib64:/usr/lib:\\\$LD_LIBRARY_PATH\" >> /etc/profile.d/pg.sh
            chmod 644 /etc/profile.d/pg.sh
        " || error_exit "Failed to install PostgreSQL on $mnd."

        # 配置 PostgreSQL
        log "$configuring (远程: $mnd)"
        echo "$configuring (远程: $mnd)"
        cp -f "$DBAIOps_oper_dir/pgconf/postgresql.conf" /tmp || error_exit "Failed to copy postgresql.conf to /tmp."
        sed -i "s/port = 5433/port = $pgport/g" /tmp/postgresql.conf || error_exit "Failed to update port in postgresql.conf."
        sed -i "s/cron.database_name='DBAIOps_2020'/cron.database_name='$pgDBAIOpsdb'/g" /tmp/postgresql.conf || error_exit "Failed to update cron database name in postgresql.conf."
        hostmem=$(ssh "$mnd" "cat /proc/meminfo | grep MemTotal" | awk '{print $2}') || error_exit "Failed to get host memory on $mnd."
        sharedmem=$((hostmem / 4096))
        sed -i "s/shared_buffers = 1024MB/shared_buffers = ${sharedmem}MB/g" /tmp/postgresql.conf || error_exit "Failed to update shared_buffers in postgresql.conf."
        connection_nums=$((fstask_cnt / 3 * 600 + 600))
        sed -i "s/max_connections = 600/max_connections = ${connection_nums}/g" /tmp/postgresql.conf || error_exit "Failed to update max_connections in postgresql.conf."
        scp -q /tmp/postgresql.conf "$mnd:$PG_DATA_PATH/postgresql.conf" || error_exit "Failed to copy postgresql.conf to $mnd."
        scp -q "$DBAIOps_oper_dir/pgconf/pg_hba.conf" "$mnd:$PG_DATA_PATH/pg_hba.conf" || error_exit "Failed to copy pg_hba.conf to $mnd."
        ssh "$mnd" "chown -R $PG_OS_USER $PG_DATA_PATH/postgresql.conf $PG_DATA_PATH/pg_hba.conf" || error_exit "Failed to set permissions on configuration files on $mnd."

        # 安装 pg_cron
        log "$install_cron (远程: $mnd)"
        echo "$install_cron (远程: $mnd)"
        scp -q "$DBAIOps_oper_dir/pg_cron-1.6.2.zip" "$mnd:/tmp" || error_exit "Failed to copy pg_cron archive to $mnd."
        ssh "$mnd" "
            source /etc/profile.d/pg.sh
            cd /tmp && if [ -d pg_cron-1.6.2 ]; then rm -rf /tmp/pg_cron-1.6.2; fi
            unzip -o /tmp/pg_cron-1.6.2.zip > /dev/null 2>&1 || exit 1
            cd /tmp/pg_cron-1.6.2 && make >> $installpg_log 2>&1 || exit 1
            make install >> $installpg_log 2>&1 || exit 1
        " || error_exit "Failed to install pg_cron on $mnd."

        # 安装扩展
        log "$install_extension (远程: $mnd)"
        echo "$install_extension (远程: $mnd)"
        export LD_LIBRARY_PATH=''
        install_extension_m

        # 初始化数据库
        log "$initdb (远程: $mnd)"
        echo "$initdb (远程: $mnd)"
        initdb_m

        # 安装 pg_cron
        install_pg_cron
    fi
    # 添加定时清理任务
    auto_drop_pg_data

    # 更新 libpq
    log "$update_libpq"
    echo "$update_libpq"
    update_libpq

    log "$install_success"
    echo "$install_success"
}


install_s()
{
    echo "############################################################"
    echo "                     install slave pg                             "
    echo "############################################################"
    if [ ! -f $DBAIOps_oper_dir/postgresql-16*.tar.gz ];then
        c1 "PostgreSQL安装文件不存在！" red
        exit 1
    fi
    if echo "$localips" | grep -wq "$sld"; then
        echo "local node install postgresql"
        echo "Compiling:"
        \cp $DBAIOps_oper_dir/postgresql-16.2.tar.gz /tmp
        cd /tmp && tar --no-same-owner -xzvf /tmp/postgresql-16.2.tar.gz > /dev/null 2>&1 && cd /tmp/postgresql-16.2 && ./configure --prefix=$PG_BASE > $installpg_log 2>&1 && make >> $installpg_log 2>&1 && make install >> $installpg_log 2>&1 && useradd $PG_OS_USER -m >> $installpg_log 2>&1
        echo 'passw0rd!@#$'|passwd $PG_OS_USER --stdin >> $installpg_log 2>&1
        chmod -R 755 $PG_BASE
        if [ ! -d $PG_DATA_PATH ];
            then mkdir -p $PG_DATA_PATH;
        else
            rm -rf $PG_DATA_PATH
        fi && chown -R $PG_OS_USER $PG_DATA_PATH;chmod -R 700 $PG_DATA_PATH
        
        echo "export PGDATA=$PG_DATA_PATH" > /etc/profile.d/pg.sh
        echo "export PG_HOME=$PG_PATH" >> /etc/profile.d/pg.sh
        echo "export PATH=\$PG_HOME:\$PATH" >> /etc/profile.d/pg.sh
        echo "export LD_LIBRARY_PATH=$PG_BASE/lib:/usr/lib64:/usr/lib:\$LD_LIBRARY_PATH:" >> /etc/profile.d/pg.sh
        chmod 644 /etc/profile.d/pg.sh
    else
        echo "$sld:"
        echo "Compiling:"
        scp -q $DBAIOps_oper_dir/postgresql-16.2.tar.gz $sld:/tmp
        ssh $sld "cd /tmp;tar --no-same-owner -xzvf /tmp/postgresql-16.2.tar.gz > /dev/null 2>&1;cd /tmp/postgresql-16.2;./configure --prefix=$PG_BASE > $installpg_log 2>&1;make >> $installpg_log 2>&1;make install >> $installpg_log 2>&1;useradd $PG_OS_USER -m >>$installpg_log 2>&1;chmod -R 755 $PG_BASE;if [ ! -d $PG_DATA_PATH ];then mkdir -p $PG_DATA_PATH;fi;chown -R $PG_OS_USER $PG_DATA_PATH;chmod -R 700 $PG_DATA_PATH else rm -rf $PG_DATA_PATH fi"
        ssh $sld "echo 'passw0rd!@#$'|passwd $PG_OS_USER --stdin >> $installpg_log 2>&1"
        ssh $sld "echo \"export PGDATA=$PG_DATA_PATH\" > /etc/profile.d/pg.sh"
        ssh $sld "echo \"export PG_HOME=$PG_PATH\" >> /etc/profile.d/pg.sh"
        ssh $sld 'echo "export PATH=\$PG_HOME:\$PATH" >> /etc/profile.d/pg.sh'
        ssh $sld "echo \"export LD_LIBRARY_PATH=$PG_BASE/lib:/usr/lib64:/usr/lib:\\\$LD_LIBRARY_PATH\" >> /etc/profile.d/pg.sh"
        ssh $sld "chmod 644 /etc/profile.d/pg.sh"
    fi
    install_extension_s
    echo "Slave Postgres install successed!"
}

install_ms()
{
    if [ ! -f $DBAIOps_oper_dir/postgresql-16*.tar.gz ];then
        c1 "postgresql数据库安装文件不存在！" red
        exit 1
    fi
    install_m
    install_s

    #copy conf file
    echo "Configuring:"
    if echo "$localips" | grep -wq "$sld"; then
        su - $PG_OS_USER -c "$PG_PATH/psql -U $PG_OS_USER -p $pgport -c \"CREATE ROLE replica login replication encrypted password 'replica'\""
        \cp -f $DBAIOps_oper_dir/pgconf/pg_hba.conf.m /tmp
        sed -i "s/\[MASTER\]/$mnd/g" /tmp/pg_hba.conf.m
        sed -i "s/\[SLAVE\]/$sld/g" /tmp/pg_hba.conf.m
        \cp /tmp/pg_hba.conf.m $PG_DATA_PATH/pg_hba.conf
        chown -R $PG_OS_USER $PG_DATA_PATH/pg_hba.conf
        su - $PG_OS_USER -c "$PG_PATH/pg_ctl reload"
    else
        ssh $mnd "su - $PG_OS_USER -c \"$PG_PATH/psql -U $PG_OS_USER -p $pgport -c \\\"CREATE ROLE replica login replication encrypted password 'replica'\\\"\""
        \cp -f $DBAIOps_oper_dir/pgconf/pg_hba.conf.m /tmp
        sed -i "s/\[MASTER\]/$mnd/g" /tmp/pg_hba.conf.m
        sed -i "s/\[SLAVE\]/$sld/g" /tmp/pg_hba.conf.m
        scp /tmp/pg_hba.conf.m $mnd:$PG_DATA_PATH/pg_hba.conf
        ssh $mnd "chown -R $PG_OS_USER $PG_DATA_PATH/pg_hba.conf"
        ssh $mnd "su - $PG_OS_USER -c \"$PG_PATH/pg_ctl reload\""
    fi

    echo "Building Master Slave:"
    if echo "$localips" | grep -wq "$sld"; then
        su - $PG_OS_USER -c "touch ~/.pgpass"
        su - $PG_OS_USER -c "chmod 0600 ~/.pgpass"
        su - $PG_OS_USER -c "echo \"$mnd:$pgport:replication:replica:replica\" > ~/.pgpass"
        su - $PG_OS_USER -c "echo \"$sld:$pgport:replication:replica:replica\" >> ~/.pgpass"
        su - $PG_OS_USER -c "$PG_PATH/pg_basebackup -D $PG_DATA_PATH -Fp -Xs -v -P -h $mnd -p $pgport -U replica -R"
        chmod -R 700 $PG_DATA_PATH
        su - $PG_OS_USER -c "$PG_PATH/pg_ctl start -D $PG_DATA_PATH"
    else
        ssh $sld "su - $PG_OS_USER -c \"touch ~/.pgpass\""
        ssh $sld "su - $PG_OS_USER -c \"chmod 0600 ~/.pgpass\""
        ssh $sld "su - $PG_OS_USER -c 'echo \"$mnd:$pgport:replication:replica:replica\" > ~/.pgpass'"
        ssh $sld "su - $PG_OS_USER -c 'echo \"$sld:$pgport:replication:replica:replica\" >> ~/.pgpass'"
        ssh $sld "su - $PG_OS_USER -c \"$PG_PATH/pg_basebackup -D $PG_DATA_PATH -Fp -Xs -v -P -h $mnd -p $pgport -U replica -R\" "
        ssh $sld "chmod -R 700 $PG_DATA_PATH"
        ssh $sld "su - $PG_OS_USER -c \"$PG_PATH/pg_ctl start -D $PG_DATA_PATH\" > /dev/null 2>&1"
    fi
    echo "Postgres stream replication install successed!"
    status_ms
}

join_pg_to_DBAIOps(){
	location=`which ls|grep -v alias|sed 's/^[ \t]*//g'`
    chmod u+s $location
    location=`which tail|grep -v alias|sed 's/^[ \t]*//g'`
    chmod u+s $location
    location=`which du|grep -v alias|sed 's/^[ \t]*//g'`
    chmod u+s $location
    location=`which dmidecode|grep -v alias|sed 's/^[ \t]*//g'`
    chmod u+s $location
    dt=`date "+%Y-%m-%d %H:%M:%S"`
    ssh_port=`netstat -anp|grep "sshd "|grep -w "tcp"|awk '{print $4}'|awk -F ":" '{print $2}'`
    echo "insert into mgt_device(uid,devicetype,in_ip,in_username,in_password,opersys,position,use_flag,create_by,create_date,parent_id,factory,life,port,name,mon_count) values(" > /tmp/pg_monitor.sql
    echo "110100001,1,'$pg_node','$PG_OS_USER','OYL29FM914aDYtIyCbWPYmyu7E6MqU1iTx9no5Fh26cFvL1lQxI779BgEfW2Aw+MeYd7WlBVXinVdz3xUvqLuUEyA5CQjBiBYUm3kWzt1TiTX6FCWTk3RdHPTc9YCfgpmkZd6hA/Q37ks8lI/fS1jDCmkte0Uw/GnzScBNtjlA=',7,1,true,9999,'$dt',0,1,1,$ssh_port,'$mnd',2);" >> /tmp/pg_monitor.sql
    echo "insert into mgt_system(systype,uid,type,name,ip,username,password,use_flag,create_by,create_date,reserver1,port,important_level,baseline_profile_id,alert_profile_id,knowl_profile_id,mon_count,check_state) values(" >> /tmp/pg_monitor.sql
    echo "1,210400001,4,'pg_DBAIOps','$pg_node','postgres','$pg_pwd',true,9999,'$dt','postgres',$pgport,1,1826391013,1801380988,1218667422,5,0);" >> /tmp/pg_monitor.sql
    su - postgres -c "psql -p 15433 -d $pgDBAIOpsdb < /tmp/pg_monitor.sql"
    python3 /usr/software/knowl/MonitorDsamrtDB.py $mnd 'pg_DBAIOps'
}


autostart_m()
{
    echo "$mnd:"
    cp -f /tmp/postgresql-16.2/contrib/start-scripts/linux /etc/init.d/postgresql
    sed -i "s|prefix=/usr/local/pgsql|prefix=$PG_BASE|g" /etc/init.d/postgresql
    sed -i "s|PGDATA=\"/usr/local/pgsql/data\"|PGDATA=$PG_DATA_PATH|g" /etc/init.d/postgresql
    sed -i "s|PGLOG=\"\\\$PGDATA\/serverlog\"|PGLOG=$PG_DATA_PATH/pg_log/serverlog|g" /etc/init.d/postgresql
    chmod +x /etc/init.d/postgresql
    chkconfig --add postgresql
}


start_ms()
{
    echo "############################################################"
    echo "                    start postgres                          "
    echo "############################################################"
    echo "$sld:"
    if echo "$localips" | grep -wq "$sld"; then
        su - $PG_OS_USER -c "$PG_PATH/pg_ctl start -D $PG_DATA_PATH" > /dev/null 2>&1
    else
        ssh $sld "su - $PG_OS_USER -c \"$PG_PATH/pg_ctl start -D $PG_DATA_PATH\" > /dev/null 2>&1"
    fi

    echo "$mnd:"
    if echo "$localips" | grep -wq "$mnd"; then
        su - $PG_OS_USER -c "$PG_PATH/pg_ctl start -D $PG_DATA_PATH" > /dev/null 2>&1
    else
        ssh $mnd "su - $PG_OS_USER -c \"$PG_PATH/pg_ctl start -D $PG_DATA_PATH\" > /dev/null 2>&1"
    fi
    status_ms
}


start_m()
{
    echo "############################################################"
    echo "                    start postgres                          "
    echo "############################################################"
    if echo "$localips" | grep -wq "$mnd"; then
        pgstatm=`su - $PG_OS_USER -c "$PG_PATH/pg_ctl status -D $PG_DATA_PATH"|grep PID`
        if [ -n "$pgstatm" ];then
            c1 "PG Already started!" blue
	        exit 0
        else
            su - $PG_OS_USER -c "$PG_PATH/pg_ctl start -D $PG_DATA_PATH > /dev/null"
	    fi
    else
        echo "$mnd:"
        pgstatm=`ssh $mnd "su - $PG_OS_USER -c \"$PG_PATH/pg_ctl status -D $PG_DATA_PATH\""|grep PID`
        if [ -n "$pgstatm" ];then
            c1 "PG Already started!" blue
	        exit 0
        else
            ssh $mnd "su - $PG_OS_USER -c \"$PG_PATH/pg_ctl start -D $PG_DATA_PATH > /dev/null\""
	    fi
    fi
    if [ $? -eq 0 ];then
        c1 "PG Start Successed!" green
        exit 0
    else
        c1 "PG Start Failed!" red
        exit 1
    fi
}

stop_ms()
{
    echo "############################################################"
    echo "                     stop postgres                          "
    echo "############################################################"
    echo "$mnd:"
    if echo "$localips" | grep -wq "$mnd"; then
        pgstatm=`su - $PG_OS_USER -c "$PG_PATH/pg_ctl status -D $PG_DATA_PATH"|grep PID`
    else
        pgstatm=`ssh $mnd "su - $PG_OS_USER -c \"$PG_PATH/pg_ctl status -D $PG_DATA_PATH\"|grep PID"`
    fi
    if [ -z "$pgstatm" ];then
        c1 "PG Already stopped!" green
    else
        if echo "$localips" | grep -wq "$mnd"; then
            su - $PG_OS_USER -c "$PG_PATH/pg_ctl stop -D $PG_DATA_PATH -m fast"
        else
            ssh $mnd "su - $PG_OS_USER -c \"$PG_PATH/pg_ctl stop -D $PG_DATA_PATH -m fast\""
        fi
    fi

    echo "$sld:"
    if echo "$localips" | grep -wq "$sld"; then
        pgstatm=`su - $PG_OS_USER -c "$PG_PATH/pg_ctl status -D $PG_DATA_PATH"|grep PID`
    else
        pgstatm=`ssh $sld "su - $PG_OS_USER -c \"$PG_PATH/pg_ctl status -D $PG_DATA_PATH\"|grep PID"`
    fi
    if [ -z "$pgstatm" ];then
        c1 "PG Already stopped!" green
    else
        if echo "$localips" | grep -wq "$sld"; then
            su - $PG_OS_USER -c "$PG_PATH/pg_ctl stop -D $PG_DATA_PATH -m fast"
        else
            ssh $sld "su - $PG_OS_USER -c \"$PG_PATH/pg_ctl stop -D $PG_DATA_PATH -m fast\""
        fi
    fi
}

stop_m()
{
    echo "############################################################"
    echo "                     stop postgres                          "
    echo "############################################################"
    if echo "$localips" | grep -wq "$mnd"; then
        echo "local node stop PG database:"
        pgstatm=`su - $PG_OS_USER -c "$PG_PATH/pg_ctl status -D $PG_DATA_PATH"|grep PID`
        if [ -z "$pgstatm" ];then
            c1 "PG Already stopped!" green
        else
            su - $PG_OS_USER -c "$PG_PATH/pg_ctl stop -D $PG_DATA_PATH -m fast"
        fi
    else
        echo "$mnd:"
        pgstatm=`ssh $mnd "su - $PG_OS_USER -c \"$PG_PATH/pg_ctl status -D $PG_DATA_PATH\"|grep PID"`
        if [ -z "$pgstatm" ];then
            c1 "PG Already stopped!" green
        else
            ssh $mnd "su - $PG_OS_USER -c \"$PG_PATH/pg_ctl stop -D $PG_DATA_PATH -m fast\""
        fi
    fi
}

status_ms()
{
    echo "############################################################"
    echo "                    status postgres                         "
    echo "############################################################"
    echo "$mnd:"
    if echo "$localips" | grep -wq "$mnd"; then
        su - $PG_OS_USER -c "$PG_PATH/pg_ctl status -D $PG_DATA_PATH"|grep running
    else
        ssh $mnd "su - $PG_OS_USER -c \"$PG_PATH/pg_ctl status -D $PG_DATA_PATH\"|grep running"
    fi
    echo "$sld:"
    if echo "$localips" | grep -wq "$sld"; then
        su - $PG_OS_USER -c "$PG_PATH/pg_ctl status -D $PG_DATA_PATH"|grep running
    else
        ssh $sld "su - $PG_OS_USER -c \"$PG_PATH/pg_ctl status -D $PG_DATA_PATH\"|grep running"
    fi
}

status_m()
{
    echo "############################################################"
    echo "                    status postgres                         "
    echo "############################################################"
    if echo "$localips" | grep -wq "$mnd"; then
        echo "local node PG database status:"
        su - $PG_OS_USER -c "$PG_PATH/pg_ctl status -D $PG_DATA_PATH"|grep running
    else
        echo "$mnd:"
        ssh $mnd "su - $PG_OS_USER -c \"$PG_PATH/pg_ctl status -D $PG_DATA_PATH\"|grep running"
    fi
}

clean_ms()
{
    echo "############################################################"
    echo "                   clean pg service                         "
    echo "############################################################"
    stop_ms
    echo "$mnd:"
    if echo "$localips" | grep -wq "$mnd"; then
        tar -czvf pgdata_bak_`date +%Y%m%d%H%M%S`.tar.gz $PG_DATA_PATH > $installpg_log 2>&1 && rm -rf $PG_DATA_PATH && rm -rf /etc/profile.d/pg.sh && userdel -r $PG_OS_USER
    else
        ssh $mnd "tar -czvf pgdata_bak_`date +%Y%m%d%H%M%S`.tar.gz $PG_DATA_PATH > $installpg_log 2>&1 && rm -rf $PG_DATA_PATH && rm -rf /etc/profile.d/pg.sh && userdel -r $PG_OS_USER"
    fi
    #if [ $? - eq 0 ];then
    #    echo "PG Clean Successed!"
    #else
    #    echo "PG Clean Failed!" 
    #    exit 1
    #fi
    echo "$sld:"
    if echo "$localips" | grep -wq "$sld"; then
        tar -czvf pgdata_bak_`date +%Y%m%d%H%M%S`.tar.gz $PG_DATA_PATH > $installpg_log 2>&1 && rm -rf $PG_DATA_PATH && rm -rf /etc/profile.d/pg.sh && userdel -r $PG_OS_USER
    else
        ssh $sld "tar -czvf pgdata_bak_`date +%Y%m%d%H%M%S`.tar.gz $PG_DATA_PATH > $installpg_log 2>&1 && rm -rf $PG_DATA_PATH && rm -rf /etc/profile.d/pg.sh && userdel -r $PG_OS_USER"
    fi
}


clean_m()
{
    echo "############################################################"
    echo "                   clean pg service                         "
    echo "############################################################"
    ##stop pg service
    stop_m
    ##backup pg data
    echo "$mnd:"
    ssh $mnd "tar -czvf pgdata_bak_`date +%Y%m%d%H%M%S`.tar.gz $PG_DATA_PATH > DBAIOps_pg.log 2>&1 && rm -rf $PG_DATA_PATH && rm -rf /etc/profile.d/pg.sh && userdel -r $PG_OS_USER"
    #if [ $? - eq 0 ];then
    #    echo "PG Clean Successed!"
    #else
    #    echo "PG Clean Failed!" 
    #    exit 1
    #fi
}

upgrade_metadata()
{
    echo "############################################################"
    echo "             upgrade DBAIOps database metadata               "
    echo "############################################################"
    if echo "$localips" | grep -wq "$mnd"; then
        su - $PG_OS_USER -c "$PG_PATH/psql -p $pgport -U $PG_OS_USER -d $pgDBAIOpsdb -f /usr/software/patches/software/$1" > $installpg_log 2>&1
    else
        scp $1 $mnd:/tmp
        ssh $mnd "su - $PG_OS_USER -c \"$PG_PATH/psql -p $pgport -U $PG_OS_USER -d $pgDBAIOpsdb -f /tmp/$1 \" > $installpg_log 2>&1"
    fi
    echo "############################################################"
    echo "             DBAIOps database metadata upgrade successed     "
    echo "############################################################"
}



auto_drop_pg_data()
{
    echo "############################################################"
    echo "                   setting pg auto drop                     "
    echo "############################################################"
    echo "source /etc/profile.d/python3.sh;source /etc/profile.d/java.sh;python3 /usr/software/knowl/auto_drop_DBAIOps_data.py" > /usr/software/bin/DBAIOps_pg_drop.sh
    echo "source /etc/profile;0 12 * * * sh /usr/software/bin/DBAIOps_pg_drop.sh > /tmp/DBAIOps_autodrop.log 2>&1" > /var/spool/cron/root
}


uninstall_postgresql() {

    # 检查是本地还是远程操作
    if echo "$localips" | grep -wq "$mnd"; then
        RPM_CMD="rpm -qa | grep ^postgresql"
    else
        RPM_CMD="ssh $mnd 'rpm -qa | grep ^postgresql'"
    fi

    # 查找所有以postgresql开头的RPM包
    INSTALLED_PG=$(eval $RPM_CMD)

    # 如果没有找到已安装的PostgreSQL包，则退出
    if [ -z "$INSTALLED_PG" ]; then
        c1 "检查通过，没有已安装PostgreSQL包。" green
    else
        # 列出将要卸载的PostgreSQL包
        c1 "以下PostgreSQL包已安装:"  red
        echo "$INSTALLED_PG"

        # 提示用户确认是否卸载
        c1 "必须要卸载这些包，否则可能会导致系统安装失败。" red

        read -p "你确定要卸载所有这些PostgreSQL包吗？(y/n): " CONFIRM

        if [[ "$CONFIRM" == "y" || "$CONFIRM" == "Y" ]]; then
            # 逐个卸载PostgreSQL相关包
            for package in $INSTALLED_PG; do
                echo "正在卸载 $package..."
                if echo "$localips" | grep -wq "$mnd"; then
                    rpm -e --nodeps $package
                    userdel $PG_OS_USER
                else
                    ssh $mnd "rpm -e --nodeps $package"
                    ssh $mnd "userdel $PG_OS_USER"
                fi
            done
            c1 "所有PostgreSQL包已卸载。" green
        else
            c1 "用户取消了卸载操作。" red
            c1 "提示：必须要卸载已有的postgresql包，否则可能会导致系统安装失败。" red
            exit 0
        fi
    fi
}


if [ -z $DBAIOps_oper_dir ];then
    c1 "DBAIOps安装目录不存在！" red
    exit 1
fi

if [ ! -f $CONF/role.cfg ];then
    c1 "There is no role.cfg in $CONF" red
    exit 1
fi

if [ -z $2 ] && [ ! -z $1 ];then
    c1 "安装节点必须提供" red
    exit 1
else
    nm=`echo $2 | tr ',' '\n'|wc -l`
    if [ $nm == 1 ];then
        mnd=$2
    elif [ $nm == 2 ];then
        mnd=`echo $2 | tr ',' '\n'|head -1`
        sld=`echo $2 | tr ',' '\n'|tail -1`
    else
        c1 "只支持2节点主从" red
        exit 1
    fi
fi

pgport=`awk -F '=' '/^DSPG_Port/ {print $2}' $CONF/role.cfg`
pgDBAIOpsdb=`awk -F '=' '/^DSPG_Database/ {print $2}' $CONF/role.cfg`
pgfsdb=`awk -F '=' '/^DSPG_FS_Database/ {print $2}' $CONF/role.cfg`
PG_BASE=`awk -F '=' '/^DSPG_BASE/ {print $2}' $CONF/role.cfg`
PG_PATH=$PG_BASE/bin
PG_DATA_PATH=`awk -F '=' '/^DSPG_DATA_LOCALTION/ {print $2}' $CONF/role.cfg`
PG_OS_USER=`awk -F '=' '/^DSPG_OS_USER/ {print $2}' $CONF/role.cfg`
fstask_cnt=`awk -F '=' '/^DS_Other_Executor/ {print $2}' $CONF/role.cfg|awk -F ',' '{print NF}'`
pg_node=`awk -F '=' '/^DSPG_Node/ {print $2}' $CONF/role.cfg`
pg_pwd=`awk -F '=' '/^DSPG_Password/ {print $2}' $CONF/role.cfg`
ds_hosts=$(awk -F '=' '/^DS_Web|^DS_Collector|^DS_Monitor|^DS_Logana|^DS_Fstask|^DS_Other_Executor|^DS_Zookeeper|^DS_Redis/ {print $2}' $CONF/role.cfg | tr -s '\n' | tr ',' '\n' | sort -u)


if [ "$LANGUAGE" = "cn" ]; then
    install_log="安装日志：$installpg_log"
    install_ms="正在安装主从节点"
    install_m="正在安装主节点"
    start_ms="正在启动主从节点"
    start_m="正在启动主节点"
    stop_ms="正在停止主从节点"
    stop_m="正在停止主节点"
    status_ms="正在查看主从节点状态"
    status_m="正在查看主节点状态"
    clean_ms="正在清理主从节点"
    clean_m="正在清理主节点"
    upgrade_metadata="正在升级元数据"
    missing_os_type="请先执行 DBAIOps-system-package.sh！"
else
    install_log="Installation log: $installpg_log"
    install_ms="Installing master and slave nodes"
    install_m="Installing master node"
    start_ms="Starting master and slave nodes"
    start_m="Starting master node"
    stop_ms="Stopping master and slave nodes"
    stop_m="Stopping master node"
    status_ms="Checking status of master and slave nodes"
    status_m="Checking status of master node"
    clean_ms="Cleaning up master and slave nodes"
    clean_m="Cleaning up master node"
    upgrade_metadata="Upgrading metadata"
    missing_os_type="Please execute DBAIOps-system-package.sh first!"
fi

case $1 in
    "-install")
        c1 "$install_log" blue
        if [ "$mnd" ] && [ "$sld" ]; then
            uninstall_postgresql
            log "$install_ms"
            echo "$install_ms"
            if [ ! -f /usr/software/bin/logs/os_type.txt ]; then
                log "$missing_os_type"
                echo "$missing_os_type"
                exit 1
            fi
            install_ms
        else
            if [ ! -f /usr/software/bin/logs/os_type.txt ]; then
                log "$missing_os_type"
                echo "$missing_os_type"
                exit 1
            fi
            uninstall_postgresql
            log "$install_m"
            echo "$install_m"
            install_m
            #join_pg_to_DBAIOps
        fi
        ;;
    "-start")
        if [ "$mnd" ] && [ "$sld" ]; then
            log "$start_ms"
            echo "$start_ms"
            start_ms
        else
            log "$start_m"
            echo "$start_m"
            start_m
        fi
        ;;
    "-stop")
        if [ "$mnd" ] && [ "$sld" ]; then
            log "$stop_ms"
            echo "$stop_ms"
            stop_ms
        else
            log "$stop_m"
            echo "$stop_m"
            stop_m
        fi
        ;;
    "-status")
        if [ "$mnd" ] && [ "$sld" ]; then
            log "$status_ms"
            echo "$status_ms"
            status_ms
        else
            log "$status_m"
            echo "$status_m"
            status_m
        fi
        ;;
    "-clean")
        if [ "$mnd" ] && [ "$sld" ]; then
            log "$clean_ms"
            echo "$clean_ms"
            clean_ms
        else
            log "$clean_m"
            echo "$clean_m"
            clean_m
        fi
        ;;
    "-upgrade")
        upgrade_file=$3
        log "$upgrade_metadata"
        echo "$upgrade_metadata"
        upgrade_metadata "$upgrade_file"
        ;;
    *)
        print_usage
        exit 1
        ;;
esac
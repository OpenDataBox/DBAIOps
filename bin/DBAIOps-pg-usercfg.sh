#!/bin/bash
set -e
DBAIOps_oper_dir=/usr/software
DBAIOps_HOME=`awk -F '=' '/^DS_BASE_LOCALTION/ {print $2}' $DBAIOps_oper_dir/role.cfg`
CONF=$DBAIOps_HOME
localnode=`hostname`

print_usage(){
  echo "Usage: DBAIOps PostgreSQL DB User Config scripts"
  echo "./DBAIOps-pg-usercfg.sh username password"
}

if [ -z $DBAIOps_oper_dir ];then
    echo "DBAIOps安装目录不存在！"
    exit 1
fi

if [ ! -f $CONF/role.cfg ];then
    echo "There is no role.cfg in $CONF"
    exit 1
fi

username=$1
passwd=$2

if [ $# -ne 2 ];then 
   echo "参数数量必须等于2"
   print_usage
   exit 1
fi

if [ -z $2 ] || [ -z $1 ];then
    echo "必须指定数据库的用户名和密码"
    print_usage
    exit 1
fi

username_encryption=`java -jar $DBAIOps_oper_dir/return/lib/RsaEnTool.jar $username`
passwd_encryption=`java -jar $DBAIOps_oper_dir/return/lib/RsaEnTool.jar $passwd`
pg_user_default=`awk -F '=' '/^DSPG_User/ {print $2}' $CONF/role.cfg`
pg_passwd_default=`awk -F '=' '/^DSPG_Password/ {print $2}' $CONF/role.cfg`
pg_os_user=`awk -F '=' '/^DSPG_OS_USER/ {print $2}' $CONF/role.cfg`
pg_port=`awk -F '=' '/^DSPG_Port/ {print $2}' $CONF/role.cfg`
pg_DBAIOps_db=`awk -F '=' '/^DSPG_Database/ {print $2}' $CONF/role.cfg`
pg_ftask_db=`awk -F '=' '/^DSPG_FS_Database/ {print $2}' $CONF/role.cfg`
pg_base=`awk -F '=' '/^DSPG_BASE/ {print $2}' $CONF/role.cfg`
PG_PATH=$pg_base/bin
mnd_ip=`awk -F '=' '/^DSPG_Node/ {print $2}' $CONF/role.cfg`
mnd=`ssh $mnd_ip hostname`
echo $username_encryption
echo $passwd_encryption
#echo $pg_user_default
#echo $pg_passwd_default
sed -i '/DSPG_User/d' $CONF/role.cfg
sed -i '/DSPG_Password/d' $CONF/role.cfg
echo "DSPG_User=$username_encryption" >> $CONF/role.cfg
echo "DSPG_Password=$passwd_encryption" >> $CONF/role.cfg
#sed -i "s#$pg_user_default#$username_encryption#g" $CONF/role.cfg
#sed -i "s#$pg_passwd_default#$passwd_encryption#g" $CONF/role.cfg
fs_db_username=`java -jar $DBAIOps_oper_dir/return/lib/FstaskEnTool.jar $username`
fs_db_passwd=`java -jar $DBAIOps_oper_dir/return/lib/FstaskEnTool.jar $passwd`
fs_db_username_default=`awk -F '=' '/^DFC_FSTASK_DB_USERNAME/ {print $2}' $CONF/DBAIOps.cfg.init`
fs_db_passwd_default=`awk -F '=' '/^DFC_FSTASK_DB_PASSWORD/ {print $2}' $CONF/DBAIOps.cfg.init`
sed -i "s#$fs_db_username_default#$fs_db_username#g" $CONF/DBAIOps.cfg.init
sed -i "s#$fs_db_passwd_default#$fs_db_passwd#g" $CONF/DBAIOps.cfg.init
echo $fs_db_username
echo $fs_db_passwd


if [ $localnode == $mnd ];then
echo "local node init pg database"
su - $pg_os_user -c "$PG_PATH/psql -p $pg_port -d postgres -c \"create user $username with password '$passwd';\"" >> /tmp/DBAIOps_pg.log 2>&1
su - $pg_os_user -c "$PG_PATH/psql -p $pg_port -d postgres -c 'GRANT ALL PRIVILEGES ON DATABASE $pg_DBAIOps_db TO $username;'" >> /tmp/DBAIOps_pg.log 2>&1
su - $pg_os_user -c "$PG_PATH/psql -p $pg_port -d postgres -c 'GRANT ALL PRIVILEGES ON DATABASE $pg_ftask_db TO $username;'" >> /tmp/DBAIOps_pg.log 2>&1
su - $pg_os_user -c "$PG_PATH/psql -p $pg_port -d $pg_DBAIOps_db -c 'GRANT ALL PRIVILEGES ON all tables in schema public TO $username;'" >> /tmp/DBAIOps_pg.log 2>&1
su - $pg_os_user -c "$PG_PATH/psql -p $pg_port -d $pg_ftask_db -c 'GRANT ALL PRIVILEGES ON all tables in schema public TO $username;'" >> /tmp/DBAIOps_pg.log 2>&1
su - $pg_os_user -c "$PG_PATH/psql -p $pg_port -d $pg_DBAIOps_db -c 'GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO $username;'" >> /tmp/DBAIOps_pg.log 2>&1
su - $pg_os_user -c "$PG_PATH/psql -p $pg_port -d $pg_ftask_db -c 'GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO $username;'" >> /tmp/DBAIOps_pg.log 2>&1
else
echo "$mnd:"
echo "create user $username with password '$passwd'" > /tmp/createuser.sql
scp /tmp/createuser.sql $mnd:/tmp
echo '' > /tmp/createuser.sql
ssh $mnd "su - $pg_os_user -c \"$PG_PATH/psql -p $pg_port -d postgres -f /tmp/createuser.sql\" >> /tmp/DBAIOps_pg.log 2>&1"
ssh $mnd "echo '' > /tmp/createuser.sql"
ssh $mnd "su - $pg_os_user -c \"$PG_PATH/psql -p $pg_port -d postgres -c 'GRANT ALL PRIVILEGES ON DATABASE $pg_DBAIOps_db TO $username;'\" >> /tmp/DBAIOps_pg.log 2>&1"
ssh $mnd "su - $pg_os_user -c \"$PG_PATH/psql -p $pg_port -d postgres -c 'GRANT ALL PRIVILEGES ON DATABASE $pg_ftask_db TO $username;'\" >> /tmp/DBAIOps_pg.log 2>&1"
ssh $mnd "su - $pg_os_user -c \"$PG_PATH/psql -p $pg_port -d $pg_DBAIOps_db -c 'GRANT ALL PRIVILEGES ON all tables in schema public TO $username;'\" >> /tmp/DBAIOps_pg.log 2>&1"
ssh $mnd "su - $pg_os_user -c \"$PG_PATH/psql -p $pg_port -d $pg_ftask_db -c 'GRANT ALL PRIVILEGES ON all tables in schema public TO $username;'\" >> /tmp/DBAIOps_pg.log 2>&1"
ssh $mnd "su - $pg_os_user -c \"$PG_PATH/psql -p $pg_port -d $pg_DBAIOps_db -c 'GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO $username;'\" >> /tmp/DBAIOps_pg.log 2>&1"
ssh $mnd "su - $pg_os_user -c \"$PG_PATH/psql -p $pg_port -d $pg_ftask_db -c 'GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO $username;'\" >> /tmp/DBAIOps_pg.log 2>&1"
fi
echo "DBAIOps pg user created successfully!"

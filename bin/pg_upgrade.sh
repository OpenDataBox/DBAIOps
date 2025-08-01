#!/bin/bash
set -e 
ds_pg=`awk -F '=' '/^DSPG_Node/ {print $2}' /usr/software/role.cfg`
ds_zk=`awk -F '=' '/^DS_Zookeeper/ {print $2}' /usr/software/role.cfg`
ds_redis=`awk -F '=' '/^DS_Redis/ {print $2}' /usr/software/role.cfg`
ds_pg_port=`awk -F '=' '/^DSPG_Port/ {print $2}' /usr/software/role.cfg`
localip=`hostname -i|awk '{print $1}'`
localnode=`hostname`
upgrade_location=/home/postgres/upgrade
pg_base=`awk -F '=' '/^DSPG_BASE/ {print $2}' /usr/software/role.cfg`
PG_PATH=${pg_base}/bin
cfg_db=DBAIOps_tmp_cfg

create_tmp_cfg_db(){
if [ "$localip" == "$ds_pg" ];then
mkdir -p /home/postgres/upgrade
\cp /usr/software/DBAIOps_2018.sql $upgrade_location
chown -R postgres:postgres $upgrade_location
su - postgres -c "$PG_PATH/createdb ${cfg_db} -p $ds_pg_port" > ${upgrade_location}/DBAIOps_upgrade.log 2>&1
su - postgres -c "$PG_PATH/psql -p $ds_pg_port -d ${cfg_db} -f ${upgrade_location}/DBAIOps_2018.sql" >> ${upgrade_location}/DBAIOps_upgrade.log 2>&1
echo "create DBAIOps upgrade tmp db successed"
else
ssh $ds_pg "mkdir -p /home/postgres/upgrade"
scp /usr/software/DBAIOps_2018.sql ${ds_pg}:${upgrade_location}
ssh $ds_pg "chown -R postgres:postgres $upgrade_location"
ssh $ds_pg "su - postgres -c \"$PG_PATH/createdb ${cfg_db} -p $ds_pg_port\" > ${upgrade_location}/DBAIOps_upgrade.log 2>&1"
ssh $ds_pg "su - postgres -c \"$PG_PATH/psql -p $ds_pg_port -d ${cfg_db} -f ${upgrade_location}/DBAIOps_2018.sql\" >> ${upgrade_location}/DBAIOps_upgrade.log 2>&1"
fi
}

generate_cfg_scripts(){
python3 /usr/software/knowl/DBAIOpsupgrade.py ${cfg_db}
if [ "$localip" == "$ds_pg" ];then
\cp /tmp/pg_backup_cfg.sh ${upgrade_location}
\cp /tmp/pg_new_cfg.sh ${upgrade_location}
\cp /tmp/pg_drop.sh ${upgrade_location}
\cp /tmp/pg_drop.sql ${upgrade_location}
\cp /tmp/pg_load.sh ${upgrade_location}
echo "generate DBAIOps upgrade file successed"|tee -a ${upgrade_location}/DBAIOps_upgrade.log
chown -R postgres:postgres ${upgrade_location}
chmod -R 755 ${upgrade_location}/*.sh
else
scp /tmp/pg_backup_cfg.sh $ds_pg:${upgrade_location}
scp /tmp/pg_new_cfg.sh $ds_pg:${upgrade_location}
scp /tmp/pg_drop.sh $ds_pg:${upgrade_location}
scp /tmp/pg_drop.sql $ds_pg:${upgrade_location}
scp /tmp/pg_drop.sql $ds_pg:/tmp
scp /tmp/pg_load.sh $ds_pg:${upgrade_location}
ssh $ds_pg "echo 'generate DBAIOps upgrade file successed'|tee -a ${upgrade_location}/DBAIOps_upgrade.log"
ssh $ds_pg "chown -R postgres:postgres ${upgrade_location};chmod -R 755 ${upgrade_location}/*.sh"
fi
}

backup_user_model(){
if [ "$localip" == "$ds_pg" ];then
cd /home/postgres/upgrade
rm -rf user_*.txt
else
ssh $ds_pg "cd /home/postgres/upgrade;rm -rf user_*.txt"
fi
python3 /usr/software/knowl/DBAIOpsBackupUserModel.py ${upgrade_location}
}

load_user_model(){
if [ "$localip" == "$ds_pg" ];then
python3 /usr/software/knowl/DBAIOpsLoadUserModel.py ${upgrade_location}
else
scp $ds_pg:${upgrade_location}/user*.txt /tmp
python3 /usr/software/knowl/DBAIOpsLoadUserModel.py /tmp
fi
}

upgrade(){
if [ "$localip" == "$ds_pg" ];then
su - postgres -c "source ~/.bash_profile;sh ${upgrade_location}/pg_new_cfg.sh"
echo "generate DBAIOps new metadata cfg successed"|tee -a ${upgrade_location}/DBAIOps_upgrade.log
su - postgres -c "source ~/.bash_profile;sh ${upgrade_location}/pg_backup_cfg.sh"
echo "backup DBAIOps old metadata cfg successed"|tee -a ${upgrade_location}/DBAIOps_upgrade.log
\cp /tmp/DBAIOps_new_cfg.sql ${upgrade_location}
\cp /tmp/DBAIOps_backup_cfg.sql ${upgrade_location}
chown -R postgres:postgres ${upgrade_location}
su - postgres -c "source ~/.bash_profile;sh ${upgrade_location}/pg_drop.sh"|tee -a ${upgrade_location}/DBAIOps_upgrade.log
echo "delete DBAIOps old metadata cfg successed"|tee -a ${upgrade_location}/DBAIOps_upgrade.log
su - postgres -c "source ~/.bash_profile;sh ${upgrade_location}/pg_load.sh"|tee -a ${upgrade_location}/DBAIOps_upgrade.log
echo "load DBAIOps new metadata cfg successed"|tee -a ${upgrade_location}/DBAIOps_upgrade.log
else
ssh $ds_pg "su - postgres -c \"source ~/.bash_profile;sh ${upgrade_location}/pg_new_cfg.sh\";echo 'generate DBAIOps new metadata cfg successed'|tee -a ${upgrade_location}/DBAIOps_upgrade.log"
ssh $ds_pg "su - postgres -c \"source ~/.bash_profile;sh ${upgrade_location}/pg_backup_cfg.sh\";echo 'backup DBAIOps old metadata cfg successed'|tee -a ${upgrade_location}/DBAIOps_upgrade.log"
ssh $ds_pg "cp /tmp/DBAIOps_new_cfg.sql ${upgrade_location};cp /tmp/DBAIOps_backup_cfg.sql ${upgrade_location};chown -R postgres:postgres ${upgrade_location}"
ssh $ds_pg "su - postgres -c \"source ~/.bash_profile;sh ${upgrade_location}/pg_drop.sh\"|tee -a ${upgrade_location}/DBAIOps_upgrade.log;echo 'delete DBAIOps old metadata cfg successed'|tee -a ${upgrade_location}/DBAIOps_upgrade.log"
ssh $ds_pg "su - postgres -c \"source ~/.bash_profile;sh ${upgrade_location}/pg_load.sh\"|tee -a ${upgrade_location}/DBAIOps_upgrade.log;echo 'load DBAIOps new metadata cfg successed'|tee -a ${upgrade_location}/DBAIOps_upgrade.log"
fi
}

drop_tmp_cfg_db(){
if [ "$localip" == "$ds_pg" ];then
su - postgres -c "$PG_PATH/dropdb ${cfg_db} -p $ds_pg_port"
echo "drop DBAIOps tmp cfg db successed"|tee -a ${upgrade_location}/DBAIOps_upgrade.log
echo "DBAIOps metadata rolling upgrade successed"|tee -a ${upgrade_location}/DBAIOps_upgrade.log
else
ssh $ds_pg "su - postgres -c \"$PG_PATH/dropdb ${cfg_db} -p $ds_pg_port\";echo 'drop DBAIOps tmp cfg db successed'|tee -a ${upgrade_location}/DBAIOps_upgrade.log;echo 'DBAIOps metadata rolling upgrade successed'|tee -a ${upgrade_location}/DBAIOps_upgrade.log"
fi
}

check_model_bind(){
python3 /usr/software/knowl/check_model_bind.py
}

backup_monitor_data(){
if [ "$localnode" == "$ds_zk" ]; then
    if [ "$localip" == "$ds_pg" ]; then
        cp -r /usr/software/zkdata /home/postgres/upgrade > /dev/null
    else 
        scp -r /usr/software/zkdata $ds_pg:/home/postgres/upgrade > /dev/null
    fi
else
    scp -r $ds_zk:/usr/software/zkdata $ds_pg:/home/postgres/upgrade
fi
echo "zk data backup successed"
if [ "$localnode" == "$ds_redis" ]; then
    if [ "$localip" == "$ds_pg" ]; then
        cp -r /usr/software/redisdata /home/postgres/upgrade > /dev/null
    else
        scp -r /usr/software/redisdata $ds_pg:/home/postgres/upgrade > /dev/null
    fi
else
    scp -r $ds_redis:/usr/software/redisdata $ds_pg:/home/postgres/upgrade
fi
echo "redis data backup successed"
}



create_tmp_cfg_db
python3 /usr/software/knowl/DBAIOpsTabComp.py ${cfg_db}
generate_cfg_scripts
backup_user_model
upgrade
drop_tmp_cfg_db
load_user_model
check_model_bind
backup_monitor_data

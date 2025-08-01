#!/bin/bash


print_usage(){
  echo "Usage: sh init.sh <ip> <hostname>" 
  echo " <ip>            new ip"
  echo " <hostname>       Invariant host name "
}

if [ -z "$1" -o -z "$2" ];then
    print_usage
    exit 1
fi

localip=$1
hostname=$2

######################Do not modify the following ##############
sed -i "s/DSPG_Node=.*/DSPG_Node=$localip/g"  /usr/software/role.cfg
sed -i "s/.*$hostname/$localip $hostname/g" /etc/hosts
sed -i "s@\"graph_url\": \"bolt:.*@\"graph_url\": \"bolt://$localip:7687\",@g" /usr/software/webserver/conf/knowledge_graph.json
/usr/software/bin/DBAIOps.sh -stop
/usr/software/bin/DBAIOps-pg.sh -start $localip
/usr/software/bin/DBAIOps.sh -reinstall
/usr/software/bin/DBAIOps-zookeeper.sh -stop
/usr/software/bin/DBAIOps.sh -start




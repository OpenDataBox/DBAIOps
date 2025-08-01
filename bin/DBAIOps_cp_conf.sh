#!/bin/bash

scp -r /usr/software/webserver/conf/* 60.60.60.123:/u01/javan/newversion/dfc/software/webserver/conf
scp -r /usr/software/webserver/war/RtManageCon.war 60.60.60.123:/u01/javan/newversion/dfc/software/webserver/war
scp -r /usr/software/webserver/logo/* 60.60.60.123:/u01/javan/newversion/dfc/software/webserver/logo
scp /usr/software/webserver/bin/webserver.sh 60.60.60.123:/u01/javan/newversion/dfc/software/webserver/bin
scp -r /usr/software/webserver/src/* 60.60.60.123:/u01/javan/newversion/dfc/software/webserver/src
\cp  /usr/software/fstaskpkg/war/*.war /usr/fstaskpkg/war
\cp -r /usr/software/fstaskpkg/conf/* /usr/fstaskpkg/conf
\cp -r /usr/software/fstaskpkg/bin/* /usr/fstaskpkg/bin
cd /usr
tar -cvzf fstaskpkg.tar.gz fstaskpkg > /dev/null
scp fstaskpkg.tar.gz 60.60.60.123:/u01/javan/newversion/dfc/software
scp -r /usr/software/colscript/* 60.60.60.123:/u01/javan/newversion/dfc/software/colscript
scp -r /usr/software/return/conf/* 60.60.60.123:/u01/javan/newversion/dfc/software/return/conf/
scp -r /usr/software/return/file/* 60.60.60.123:/u01/javan/newversion/dfc/software/return/file/
scp -r /usr/software/return/lib/* 60.60.60.123:/u01/javan/newversion/dfc/software/return/lib/
scp -r /usr/software/return/bin/* 60.60.60.123:/u01/javan/newversion/dfc/software/return/bin/
ssh 60.60.60.123 'sed -i "s#useFlag=true#useFlag=false#g" /u01/javan/newversion/dfc/software/return/conf/wechat.properties'

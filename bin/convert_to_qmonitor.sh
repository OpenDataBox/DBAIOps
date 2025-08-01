#!/bin/bash
# 脚本到/usr/software/bin目录下
# 遍历当前目录中的文件
for file in *; do
    if [ $file == "convert_to_qmonitor.sh" ];then
        echo "skip convert_to_qmonitor.sh"
    else
        # 检查是否是文件
        if [[ -f "$file" ]]; then
            # 使用sed替换文件名中的'DBAIOps'为'qmonitor'
            new_file=$(echo "$file" | sed 's/DBAIOps/qmonitor/g')
        
        # 如果文件名改变了，则重命名文件
        if [[ "$file" != "$new_file" ]]; then
            mv "$file" "$new_file"
        fi
        
        # 接着替换文件内容中的'DBAIOps'为'qmonitor'
        sed -i 's/DBAIOps/qmonitor/g' "$new_file"
        fi
    fi
done

if [ -f "../DBAIOps_2018.sql" ]; then
    echo "重命名sql文件"
    mv ../DBAIOps_2018.sql ../qmonitor_2018.sql
fi
echo "修改DBAIOps_loadli"
sed -i 's/DBAIOps/qmonitor/g' ../knowl/DBAIOps_loadli.py
echo "修改默认的配置文件"
sed -i 's/DBAIOps/qmonitor/g' ../pgconf/postgresql.conf
sed -i 's/DBAIOps/qmonitor/g' ../DBAIOps.cfg.init
sed -i 's#TOMCATPATH/webapps/DBAIOps#TOMCATPATH/webapps/qmonitor#g' ../webserver/bin/webserver.sh

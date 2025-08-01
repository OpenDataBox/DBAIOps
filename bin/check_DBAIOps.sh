#!/bin/bash

# 添加到crontab中，每10分钟执行一次
# */10 * * * * /usr/bin/sh /usr/software/bin/check_DBAIOps.sh

# 获取检查时间
time=$(date +%Y-%m-%d_%H:%M:%S)
# 输出结果
check_time="检查时间：$time"
echo "$check_time"
echo "$check_time" >> /usr/software/logs/DBAIOps_check.log

# 执行命令
result=$(/usr/software/bin/DBAIOps.sh -status)

# 将结果写入日志文件
echo "$result" > /usr/software/logs/DBAIOps_check.log

# 检查结果中是否包含关键词"not"
if [[ "$result" == *"not"* ]]; then
    echo "服务异常，查看日志文件：/usr/software/logs/DBAIOps_check.log！"
    echo "服务异常！" >> /usr/software/logs/DBAIOps_check.log
    # 重启服务
    /usr/software/bin/DBAIOps.sh -restart
else
    echo "服务正常"
    echo "服务正常"  >> /usr/software/logs/DBAIOps_check.log
fi
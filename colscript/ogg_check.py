import sys
sys.path.append('/usr/software/knowl')
import CommUtil
import json
import DBUtil
import tags
from datetime import datetime
import time
import psycopg2
import sshHelper as ssh

def checkogg(ostype, hostusr, targetId):
    res_ogg = []
    metric = []
    metric_tmp1 = []
    metric_tmp2 = []
    metric_tmp4 = []

    if hostusr == 'root':
        ##先找到环境变量
        ##先判断是否存在ogg服务根据"mgr PARAMFILE"关键字来找进程
        cmd11 = "\"ps -ef|grep \\\"mgr PARAMFILE\\\"|grep -v \\\"grep\\\"|awk '{print \\$1\\\" \\\"\\$8\\\" \\\"\\$10}'\""
        res_cmd11 = helper.openCmd(cmd11).strip()
        
        if res_cmd11:
            for res_cmd1 in res_cmd11.splitlines():
                if res_cmd1.split(" ")[1] != "./mgr":
                    ogg_path = res_cmd1.split(" ")[1].replace("mgr", "ggsci") 
                    ogg_logfile = res_cmd1.split(" ")[1].replace("mgr", "ggserr.log") 
                else:
                    ogg_path = res_cmd1.split(" ")[2].split("dirprm")[0]+"ggsci"
                    ogg_logfile = res_cmd1.split(" ")[2].split("dirprm")[0]+"ggserr.log"

                ##接下来找ogg用户
                ogg_usr = res_cmd1.split(" ")[0]
                ##如果awk取出来的用户名显示不完整带+号
                if "+" in ogg_usr:
                    cmd2 = "\"cat /etc/passwd\""
                    res_cmd2 = helper.openCmd(cmd2).strip()
                    for x in res_cmd2.splitlines():
                        if x.startswith(ogg_usr.replace("+", "")):
                            ogg_usr = x.split(":")[0]
                ##取ggsci info all结果
                ##生成info all脚本
                cont = ogg_path + """ <<EOF
info all
exit
EOF"""
                cmd3 = "\"echo \\\"" + cont + "\\\" > /tmp/do.sh\""
                res_cmd3 = helper.openCmd(cmd3)

                cmd4 = "\"su - " + ogg_usr + " -c \\\"sh /tmp/do.sh\\\"|awk -F\\\"[ ]+|:\\\" '/MANAGER|REPLICAT|EXTRACT/{print \\$1,\\$2,\\$3,\\$4,\\$5,\\$6}' \""
                '''取出来的结果如下：
MANAGER RUNNING    
EXTRACT ABENDED DPUMP1 00 00 00
EXTRACT RUNNING EXT1 00 44 57
'''
                res_cmd4 = helper.openCmd(cmd4).strip()

                cmd5 = "tail \""+ogg_logfile+"\""
                res_cmd5 = helper.openCmd(cmd5).strip()

                lag_sec = 0
                op = ""
                os = ""
                og = ""
                ola = 0
                olo = ""
                ogg_res_temp = []

                for x in res_cmd4.splitlines():
                    cmd5 = "tail \""+ogg_logfile+"\""
                    res_cmd5 = helper.openCmd(cmd5).strip()
                    olo = res_cmd5

                    op = x.split(' ')[0]
                    os = x.split(' ')[1]
                    og = x.split(' ')[2]

                    if x.split(' ')[5] != 0 and x.split(' ')[5] != '':
                        lag_sec += int(x.split(' ')[5])
                    if x.split(' ')[4] != 0 and x.split(' ')[4] != '':
                        lag_sec += int(x.split(' ')[4]) * 60
                    if x.split(' ')[3] != 0 and x.split(' ')[3] != '':
                        lag_sec += int(x.split(' ')[3]) * 3600
                    if lag_sec != 0:
                        ola = lag_sec
                        lag_sec = 0

                    if os != '' and os != 'RUNNING':
                        tags.mkAlert(str(targetId),'OGG进程监控','OGG-Monitor-Status','',time.mktime(datetime.now().timetuple()),2,op+"进程"+og+"状态异常",'N','N')
                    if ola != '' and ola > 60:
                        tags.mkAlert(str(targetId),'OGG进程监控','OGG-Monitor-Delay','',time.mktime(datetime.now().timetuple()),2,op+"进程"+og+"延迟:"+str(ola)+'秒','N','N')
 
                    ogg_res_temp.append(dict(target_id_c=targetId,mtype_c="OGG",ogg_program_c=op,ogg_status_c=os,ogg_group_c=og,ogg_lag_n=ola,ogg_log_c=olo,check_date_c=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))) 
                    metric_tmp1.append(dict(name=og,value=op))
                    metric_tmp2.append(dict(name=og,value=os))
                    metric_tmp4.append(dict(name=og,value=ola))

                metric.append(dict(index_id="6160001",value=metric_tmp1))
                metric.append(dict(index_id="6160002",value=metric_tmp2))
                metric.append(dict(index_id="6160003",value=metric_tmp4))
                res_ogg = ogg_res_temp
                print('{"results":' + json.dumps(metric) + '}')

                #ss = 'target_id_c,mtype_c,ogg_program_c,ogg_status_c,ogg_group_c,ogg_lag_n,ogg_log_c,check_date_c'
                #outstr = (CommUtil.getSeparator()+'{"tb":"rpm_info","colname":"%s",' % (ss))
                #outstr += ('"col": ' + json.dumps(res_ogg) + '}')
                #print(outstr)

                #if len(tags.Alerts) > 0 :
                #    print(CommUtil.getSeparator()+'{"alert":"alert_message","colname":"tgt_c,src_c,cat_c,orig_c,ts_d,level_n,defer_c,sent_c,state_n,msg_c",')
                #    print('"col":' + json.dumps(tags.Alerts) + '}')

    else:
        ##先找到环境变量
        ##先判断是否存在ogg服务根据"mgr PARAMFILE"关键字来找进程
        cmd11 = "\"ps -ef|grep \\\"mgr PARAMFILE\\\"|grep -v \\\"grep\\\"|awk '{print \\$1\\\" \\\"\\$8\\\" \\\"\\$10}'\""
        res_cmd11 = helper.openCmd(cmd11).strip()
        if res_cmd11:
            for res_cmd1 in res_cmd11.splitlines():
                if res_cmd1.split(" ")[1] != "./mgr":
                    ogg_path = res_cmd1.split(" ")[1].replace("mgr", "ggsci")    
                    ogg_logfile = res_cmd1.split(" ")[1].replace("mgr", "ggserr.log")
                else:
                    ogg_path = res_cmd1.split(" ")[2].split("dirprm")[0]+"ggsci"
                    ogg_logfile = res_cmd1.split(" ")[2].split("dirprm")[0]+"ggserr.log"

                ##接下来找ogg用户和ogg运行路径
                ogg_usr = res_cmd1.split(" ")[0]
                ##如果awk取出来的用户名显示不完整带+号
                if "+" in ogg_usr:
                    cmd2 = "\"cat /etc/passwd\""
                    res_cmd2 = helper.openCmd(cmd2).strip()
                    for x in res_cmd2.splitlines():
                        if x.startswith(ogg_usr.replace("+", "")):
                            ogg_usr = x.split(":")[0]
                if ogg_usr == hostusr:
                    ##取ggsci info all结果
                    ##生成info all脚本
                    cont = ogg_path + """ <<EOF
info all
exit
EOF"""
                    cmd3 = "\"echo \\\"" + cont + "\\\" > /tmp/do.sh\""
                    res_cmd3 = helper.openCmd(cmd3)

                    cmd4 = "\"source ~/.bash_profile;sh /tmp/do.sh|awk -F\\\"[ ]+|:\\\" '/MANAGER|REPLICAT|EXTRACT/{print \\$1,\\$2,\\$3,\\$4,\\$5,\\$6}' \""
                    '''取出来的结果如下：
MANAGER RUNNING    
EXTRACT ABENDED DPUMP1 00 00 00
EXTRACT RUNNING EXT1 00 44 57
'''
                    res_cmd4 = helper.openCmd(cmd4).strip()

                    lag_sec = 0
                    op = ""
                    os = ""
                    og = ""
                    ola = 0
                    olo = ""
                    ogg_res_temp = []

                    for x in res_cmd4.splitlines():
                        cmd5 = "tail \""+ogg_logfile+"\""
                        res_cmd5 = helper.openCmd(cmd5).strip()
                        olo = res_cmd5

                        op = x.split(' ')[0]
                        os = x.split(' ')[1]
                        og = x.split(' ')[2]

                        if x.split(' ')[5] != 0 and x.split(' ')[5] != '':
                            lag_sec += int(x.split(' ')[5])
                        if x.split(' ')[4] != 0 and x.split(' ')[4] != '':
                            lag_sec += int(x.split(' ')[4]) * 60
                        if x.split(' ')[3] != 0 and x.split(' ')[3] != '':
                            lag_sec += int(x.split(' ')[3]) * 3600
                        if lag_sec != 0:
                            ola = lag_sec
                            lag_sec = 0

                        if os != '' and os != 'RUNNING':
                            tags.mkAlert(str(targetId),'OGG进程监控','OGG-Monitor-Status','',time.mktime(datetime.now().timetuple()),2,op+"进程"+og+"状态异常",'N','N')
                        if ola != '' and ola > 60:
                            tags.mkAlert(str(targetId),'OGG进程监控','OGG-Monitor-Delay','',time.mktime(datetime.now().timetuple()),2,op+"进程"+og+"延迟:"+str(ola)+'秒','N','N')

                        ogg_res_temp.append(dict(target_id_c=targetId,mtype_c="OGG",ogg_program_c=op,ogg_status_c=os,ogg_group_c=og,ogg_lag_n=ola,ogg_log_c=olo,check_date_c=datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

                        metric_tmp1.append(dict(name=og,value=op))
                        metric_tmp2.append(dict(name=og,value=os))
                        metric_tmp4.append(dict(name=og,value=ola))

                    metric.append(dict(index_id="6160001",value=metric_tmp1))
                    metric.append(dict(index_id="6160002",value=metric_tmp2))
                    metric.append(dict(index_id="6160003",value=metric_tmp4))
                    res_ogg = ogg_res_temp
                    print('{"results":' + json.dumps(metric) + '}')

                    #ss = 'target_id_c,mtype_c,ogg_program_c,ogg_status_c,ogg_group_c,ogg_lag_n,ogg_log_c,check_date_c'
                    #outstr = (CommUtil.getSeparator()+'{"tb":"rpm_info","colname":"%s",' % (ss))
                    #outstr += ('"col": ' + json.dumps(res_ogg) + '}')
                    #print(outstr)

                    #if len(tags.Alerts) > 0 :
                    #    print(CommUtil.getSeparator()+'{"alert":"alert_message","colname":"tgt_c,src_c,cat_c,orig_c,ts_d,level_n,defer_c,sent_c,state_n,msg_c",')
                    #    print('"col":' + json.dumps(tags.Alerts) + '}')

if __name__ == '__main__':
    dbInfo = eval(sys.argv[1])
    hostusr = dbInfo['in_usr']
    targetId = dbInfo['targetId']
    ostype, _, helper = DBUtil.get_ssh_help()
    if ostype != "Windows" and ostype != "AiX" and ostype != "HPUNIX":
        checkogg(ostype, hostusr, targetId)

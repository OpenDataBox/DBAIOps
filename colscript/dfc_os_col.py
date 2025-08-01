import os
import sys
import json
import time
import datetime

sys.path.append('/usr/software/knowl')
import DBUtil
import JavaRsa
import PromeUtil

map_table2 = [
['node_cpu_seconds_total','sum',3000007,{'mode':'irq'}]
]

map_table = [
['node_cpu_seconds_total','sum',3000103],
['node_cpu_seconds_total','sum',3000104,{'mode':'user'}],
['node_cpu_seconds_total','sum',3000105,{'mode':'system'}],
['node_cpu_seconds_total','sum',3000106,{'mode':'nice'}],
['node_cpu_seconds_total','sum',3000107,{'mode':'idle'}],
['node_cpu_seconds_total','sum',3000108,{'mode':'iowait'}],
['node_cpu_seconds_total','sum',3000109,{'mode':'softirq'}],
['node_cpu_seconds_total','sum',3000110,{'mode':'irq'}],
['node_cpu_seconds_total','sum',3000111,{'mode':'steal'}],
['node_cpu_seconds_total','cnt',3000010,{'mode':'idle'}],
['node_procs_running','max',3000009],
['node_procs_blocked','max',3000013],
['node_load1','max',3001018],
['node_load5','max',3001019],
['node_memory_MemTotal_bytes','sum,1024,0',3000016],
['node_memory_MemAvailable_bytes','sum,1024,0',3000017],
['node_memory_MemFree_bytes','sum,1024,0',3000007],
['node_memory_SwapTotal_bytes','sum,1048576,2',3001029],
['node_memory_SwapFree_bytes','sum,1048576,2',3001030],
['node_memory_Buffers_bytes','sum,1024,0',3001034],
['node_memory_Cached_bytes','sum,1024,0',3001035],
['node_memory_HugePages_Total','sum',3001021],
['node_memory_HugePages_Free','sum',2000014],
['node_memory_HugePages_Rsvd','sum',2000015],
['node_memory_HardwareCorrupted_bytes','sum',3001022],
['node_memory_PageTables_bytes','sum,1024,0',3001032],
['node_memory_Slab_bytes','sum,1024,0',3001033],
['node_memory_Shmem_bytes','sum,1048576,2',3001028],
['node_memory_numa_MemTotal','cnt',3000310],
['node_memory_numa_MemTotal','sum,1048576,2',3000311,None,'{node}'],
['node_memory_numa_MemFree','sum,1048576,2',3000312,None,'{node}'],
['node_intr_total','sum',3000112],
['node_context_switches_total','sum',3000113],
['node_sockstat_TCP_alloc','sum',3001073],
#['node_sockstat_TCP_inuse','sum',3001074],
['node_netstat_Tcp_CurrEstab','sum',3001074],
['node_sockstat_TCP_tw','sum',3001078],
['node_sockstat_TCP_orphan','sum',3001076],
['node_time_seconds','max,1,0',3000198],
['node_boot_time_seconds','max,1,0',3000197],
['node_filesystem_size_bytes','max,1024,0',3000303,None,'{mountpoint}'],
['node_filesystem_free_bytes','max,1024,0',2000001,None,'{mountpoint}'],
['node_filesystem_files','max',3000308,None,'{mountpoint}'],
['node_filesystem_files_free','max',2000002,None,'{mountpoint}'],
['node_filesystem_readonly','max',2000003,None,'{mountpoint}'],
['node_disk_reads_completed_total','sum',2000004,None,'{device}'],
['node_disk_writes_completed_total','sum',2000005,None,'{device}'],
['node_disk_read_bytes_total','sum',2000006,None,'{device}'],
['node_disk_written_bytes_total','sum',2000007,None,'{device}'],
['node_disk_read_time_seconds_total','sum',2000008,None,'{device}'],
['node_disk_write_time_seconds_total','sum',2000009,None,'{device}'],
['node_network_receive_drop_total','sum',2000010,None,'{device}'],
['node_network_receive_errs_total','sum',2000011,None,'{device}'],
['node_network_transmit_drop_total','sum',2000012,None,'{device}'],
['node_network_transmit_errs_total','sum',2000013,None,'{device}']
]

class Result(object):
    # pass
    def __str__(self):
        return "\n".join("{}={}".format(k, getattr(self, k))
                        for k in self.__dict__.keys())

def relate_pg2(conn, sql, nrow=0):
    result = Result()
    try:
        cur = conn.conn.cursor()
        cur.execute(sql)
        msg = []
        if nrow == 0:
            rows = cur.fetchall()
            for row in rows:
                msg.append(row)
        else:
            for i in range(nrow):
                row = cur.fetchone()
                if row is None:
                    break
                msg.append(row)
        result.code = 0
        result.msg = msg
    except psycopg2.ProgrammingError:
        result.code = 2
        result.msg = "SQL Error"
    except psycopg2.OperationalError:
        result.code = 1
        result.msg = "Connect Error"
    return result

def getSeparator():
    return '#!SPRT!#'

def cs(val):
    if val is None:
        return ''
    return str(val)

def encap(target_id,row,sdate):
    tup = dict(targetid_c=target_id,index_n=row[0],recordt_d=cs(sdate),ver_n=row[1],size_n=row[2],seq_n=row[3])
    for i in range(row[2]):
        tup['col%d_c' % (i+1)] = row[4+i]
    for i in range(20-row[2]):
        tup['col%d_c' % (row[2]+i+1)] = None
    return tup

def encap2(row):
    tup = dict(version=row[1],size=row[2],seq_id=row[3])
    for i in range(row[2]):
        tup['col%d' % (i+1)] = row[4+i]
    for i in range(20-row[2]):
        tup['col%d' % (row[2]+i+1)] = ''
    return tup

def tuple2(arr, f=False):
    s = ''
    for v in arr:
        if v is None:
            v = 'null'
        v = str(v).replace("'", "''")
        if s:
            if f:
                s += ",'%s'" % str(v)
            else:
                s += ",%s" % str(v)
        else:
            if f:
                s = "'%s'" % str(v)
            else:
                s = "%s" % str(v)
    if s and f:
        s = '(%s)' % s
    return s

def prometheus(host, port, mets):
    try:
        exptr = PromeUtil.Exporter(host, port)
        exptr.collect(mets)
        #print(mets)
        ret = True
    except:
        ret = False
    return ret

def os_metric(conn, uid, mets, metric):
    m = mets.get('node_time_seconds')
    if not m or not m['mets'][0]['val']:
        return None
    sql = '''select index_id,value::numeric,record_time,iname from mon_indexdata where uid='%s' and index_id between 3000199 and 3000299 order by index_id''' % uid
    result = relate_pg2(conn, sql)
    met = {}
    rt = None
    if result.code == 0:
        for row in result.msg:
            if row[0] == 3000199:
                met = {}
                rt = row[2]
            if rt == row[2]:
                if row[3]:
                    met[str(row[0])+'-'+str(row[3])] = float(row[1])
                else:
                    met[row[0]] = float(row[1])
    ct = int(time.time())
    #ct = round(m['mets'][0]['val'])
    sdate = datetime.datetime.fromtimestamp(ct)
    metric.append(dict(index_id="3000199", value=str(ct)))
    ks = ['node_netstat_Tcp_InSegs','node_netstat_Tcp_OutSegs','node_netstat_Tcp_RetransSegs','node_netstat_Udp_InDatagrams','node_netstat_Udp_InErrors',
          'node_netstat_Udp_OutDatagrams','node_netstat_Udp_RcvbufErrors','node_netstat_Udp_SndbufErrors',None,'node_netstat_IpExt_InOctets','node_netstat_IpExt_OutOctets']
    vals = [None]*15
    for i in range(len(ks)):
        if ks[i]:
            mt = mets.get(ks[i])
            if mt:
                vals[i+4] = mt['mets'][0]['val']
    if vals:
        t0 = 0
        for i in range(15):
            if vals[i] is not None:
                metric.append(dict(index_id=str(3000210+i), value=str(vals[i])))
                if met.get(3000199) and met.get(3000210+i) is not None and met[3000210+i] <= vals[i]:
                    metric.append(dict(index_id=str(3000250+i), value=str(round((vals[i]-met[3000210+i])/(ct-met[3000199]),2))))
                    if i == 5 or i == 6:
                        if i == 5:
                            t0 = vals[i]-met[3000210+i]
                        elif t0:
                            metric.append(dict(index_id=str(3000263), value=str(round((vals[i]-met[3000210+i])*100/t0,2))))
    vals = {}
    mt = mets.get('node_network_flags')
    if mt:
        for met in mt['mets']:
            v = [None]*17
            v[0] = met['tags']['device']
            if int(met['val']) & 1 == 1:
                v[1] = 1
            else:
                v[1] = 0
            vals[v[0]] = v
    ks = ['node_network_mtu_bytes',
          'node_network_info',
          'node_network_receive_packets_total',
          'node_network_receive_bytes_total',
          'node_network_receive_errs_total',
          'node_network_receive_drop_total',
          'node_network_receive_fifo_total',
          'node_network_receive_frame_total',
          'node_network_transmit_packets_total',
          'node_network_transmit_bytes_total',
          'node_network_transmit_errs_total',
          'node_network_transmit_drop_total',
          'node_network_transmit_fifo_total',
          'node_network_transmit_carrier_total',
          'node_network_transmit_colls_total'
         ]
    for i in range(len(ks)):
        mt = mets.get(ks[i])
        if mt:
            for met in mt['mets']:
                val = vals.get(met['tags']['device'])
                if val:
                    if i == 1:
                        val[i+2] = met['tags']['address']
                    else:
                        val[i+2] = met['val']
    tabular = []
    if vals:
        t = 0
        vals1 = []
        vals2 = []
        vals3 = []
        vals4 = []
        vals5 = []
        vals6 = []
        ttt = 0
        tab = []
        for ss in vals.values():
            t += 1
            #tabular.append(encap(uid,[3000202,1,17,t,ss[0],cs(ss[1]),cs(ss[2]),cs(ss[3]),cs(ss[4]),cs(ss[5]),cs(ss[6]),cs(ss[7]),cs(ss[8]),cs(ss[9]),cs(ss[10]),cs(ss[11]),cs(ss[12]),cs(ss[13]),cs(ss[14]),cs(ss[15]),cs(ss[16])],sdate))
            tab.append(encap2([3000202,1,17,t,ss[0],cs(ss[1]),cs(ss[2]),cs(ss[3]),cs(ss[4]),cs(ss[5]),cs(ss[6]),cs(ss[7]),cs(ss[8]),cs(ss[9]),cs(ss[10]),cs(ss[11]),cs(ss[12]),cs(ss[13]),cs(ss[14]),cs(ss[15]),cs(ss[16])]))
            if ss[0] == 'lo':
                continue
            if ss[5]:
                vals1.append(dict(name=ss[0],value=str(ss[5])))
                if met.get(3000199) and met.get('3000203-'+ss[0]) is not None and met['3000203-'+ss[0]] <= ss[5]:
                    vals2.append(dict(name=ss[0],value=str(round((ss[5]-met['3000203-'+ss[0]])/(ct-met[3000199])))))
            if ss[11]:
                vals3.append(dict(name=ss[0],value=str(ss[11])))
                if met.get(3000199) and met.get('3000205-'+ss[0]) is not None and met['3000205-'+ss[0]] <= ss[11]:
                    vals4.append(dict(name=ss[0],value=str(round((ss[11]-met['3000205-'+ss[0]])/(ct-met[3000199])))))
            if ss[5] and ss[11]:
                tt = ss[5] + ss[11]
                vals5.append(dict(name=ss[0],value=str(tt)))
                if met.get(3000199) and met.get('3000207-'+ss[0]) is not None and met['3000207-'+ss[0]] <= tt:
                    vals6.append(dict(name=ss[0],value=str(round((tt-met['3000207-'+ss[0]])/(ct-met[3000199])))))
                    ttt += (tt-met['3000207-'+ss[0]])/(ct-met[3000199])
        tabular.append(dict(index_id=3000202,content=tab))
        if vals1:
            metric.append(dict(index_id=str(3000203), value=vals1))
        if vals2:
            metric.append(dict(index_id=str(3000204), value=vals2))
        if vals3:
            metric.append(dict(index_id=str(3000205), value=vals3))
        if vals4:
            metric.append(dict(index_id=str(3000206), value=vals4))
        if vals5:
            metric.append(dict(index_id=str(3000207), value=vals5))
        if vals6:
            metric.append(dict(index_id=str(3000208), value=vals6))
            metric.append(dict(index_id=str(3000209), value=str(round(ttt,0))))
    vals = {}
    mt = mets.get('node_disk_reads_completed_total')
    if mt:
        for met in mt['mets']:
            v = [None]*12
            v[0] = met['tags']['device']
            vals[v[0]] = v
    ks = ['node_disk_reads_completed_total',
          'node_disk_reads_merged_total',
          'node_disk_read_bytes_total',
          'node_disk_read_time_seconds_total',
          'node_disk_writes_completed_total',
          'node_disk_writes_merged_total',
          'node_disk_written_bytes_total',
          'node_disk_write_time_seconds_total',
          'node_disk_io_now',
          'node_disk_io_time_seconds_total',
          'node_disk_io_time_weighted_seconds_total'
         ]
    for i in range(len(ks)):
        mt = mets.get(ks[i])
        if mt:
            for met in mt['mets']:
                val = vals.get(met['tags']['device'])
                if val:
                    if i in [2,6]:
                        val[i+1] = round(met['val'] / 512)
                    elif i in [3,7,9,10]:
                        val[i+1] = round(met['val'] * 1000)
                    else:
                        val[i+1] = round(met['val'])
    if vals:
        t = 0
        tab = []
        for ss in vals.values():
            t += 1
            #tabular.append(encap(uid,[3000102,1,12,t,ss[0],cs(ss[1]),cs(ss[2]),cs(ss[3]),cs(ss[4]),cs(ss[5]),cs(ss[6]),cs(ss[7]),cs(ss[8]),cs(ss[9]),cs(ss[10]),cs(ss[11])],sdate))
            tab.append(encap2([3000102,1,12,t,ss[0],cs(ss[1]),cs(ss[2]),cs(ss[3]),cs(ss[4]),cs(ss[5]),cs(ss[6]),cs(ss[7]),cs(ss[8]),cs(ss[9]),cs(ss[10]),cs(ss[11])]))
        tabular.append(dict(index_id=3000102,content=tab))
    return tabular
    #ss = 'targetid_c,index_n,recordt_d,ver_n,size_n,seq_n,col1_c,col2_c,col3_c,col4_c,col5_c,col6_c,col7_c,col8_c,col9_c,col10_c,col11_c,col12_c,col13_c,col14_c,col15_c,col16_c,col17_c,col18_c,col19_c,col20_c'
    #outstr = '%s{"tb":"mon_tabulardata","colname":"%s",' % (getSeparator(), ss)
    #outstr += ('"col":' + json.dumps(tabular) + '}')
    #print(outstr)

def parseParam(params):
    if params[0] == '{':
        paramDict = eval(params)
    else:
        paramDict = {}
        paramsList = params.split(",")
        for item in paramsList:
            if item != "":
                if "=" in item:
                    index = item.find("=")
                    paramDict[item[:index]] = item[index + 1:].strip()
    return paramDict

def main():
    dbInfo = eval(sys.argv[1])
    targetId = dbInfo['targetId']
    proto = dbInfo.get('protocol')
    if targetId[0:2] == '18' or proto == '5':
        import health_rds
        health_rds.main()
        return
    host = dbInfo['in_ip']
    port = dbInfo['in_port']
    # usr = dbInfo['in_usr']
    # pwd = dbInfo['in_pwd']
    # prop = dbInfo['otherConf']
    if proto not in ['4','5']:
        print('协议[%s]不支持' % proto)
        sys.exit()
    #targetId, pg = DBUtil.get_pg_env(dbInfo,0)
    pg = DBUtil.get_pg_from_cfg()
    if pg.conn is None:
        print('无法连接本地数据库')
        sys.exit()
    ct = int(time.time())
    mets = {}
    metric = []
    ret = prometheus(host, port, mets)
    ct2 = int(time.time())
    cdt = datetime.datetime.fromtimestamp(ct)
    #print('Elapsed: %d' % (ct2-ct))
    if ret:
        metric.append(dict(index_id="3000000", value="连接成功"))
        stage = {}
        PromeUtil.map2(mets, map_table, stage)
        #print(stage)
        if mets.get('node_filesystem_size_bytes'):
            fst = {}
            for met in mets['node_filesystem_size_bytes']['mets']:
                mp = met['tags'].get('mountpoint')
                fs = met['tags'].get('fstype')
                fst[mp] = fs
            ms = stage.get(2000003)
            if ms:
                for met in ms:
                    if float(met['value']):
                        fst[met['name']] = 'RO'
            mts = [3000303,3000308]
            for mt in mts:
                ms = stage.get(mt)
                if ms:
                    arr = []
                    for met in ms:
                        fs = fst.get(met['name']) 
                        if fs == 'RO' or fs.find('tmpfs') >= 0 or fs.find('cgroup') >= 0 or fs.find('overlay') >= 0:
                            continue 
                        arr.append(met)
                    if arr:
                        stage[mt] = arr
                        if mt == 3000303:
                            ms = stage.get(2000001)
                        else:
                            ms = stage.get(2000002)
                        if ms:
                            arr2 = []
                            for met in ms:
                                fs = fst.get(met['name']) 
                                for m in arr:
                                    if m['name'] == fs:
                                        v = round((float(m['value'])-float(met['value']))*100 / float(m['value']),2)
                                        if fs == '/':
                                            stage[3000005] = str(v)
                                        arr2.append(dict(name=fs,value=str(v)))
                                        break
                            if arr2:
                                if mt == 3000303:
                                    stage[3000300] = arr2
                                else:
                                    stage[3000301] = arr2
                    else:
                        del stage[mt]
            val = 0
            f = 0
            mts = [2000010,2000011,2000012,2000013]
            for mt in mts:
                ms = stage.get(mt)
                if ms:
                    t = 0
                    for met in ms:
                        dev = met['name']
                        if dev.find(':') > 0:
                            continue 
                        val += int(float(met['value']))
                        t += 1
                    if t > f:
                        f = t
            if f:
                metric.append(dict(index_id='3000201', value=str(val)))
            val = 0
            f = 0
            mts = [2000004,2000005]
            for mt in mts:
                ms = stage.get(mt)
                if ms:
                    t = 0
                    for met in ms:
                        dev = met['name']
                        if dev.find('dm-') == 0:
                            continue 
                        val += float(met['value'])
                        t += 1
                    if t > f:
                        f = t
            if f:
                metric.append(dict(index_id='3000114', value=str(f)))
                metric.append(dict(index_id='3000115', value=str(val)))
            val2 = 0
            f = 0
            mts = [2000006,2000007]
            for mt in mts:
                ms = stage.get(mt)
                if ms:
                    t = 0
                    for met in ms:
                        dev = met['name']
                        if dev.find('dm-') == 0:
                            continue 
                        val2 += float(met['value'])
                        t += 1
                    if t > f:
                        f = t
            if f:
                metric.append(dict(index_id='3000116', value=str(val2)))
            val3 = 0
            f = 0
            mts = [2000008,2000009]
            for mt in mts:
                ms = stage.get(mt)
                if ms:
                    t = 0
                    for met in ms:
                        dev = met['name']
                        if dev.find('dm-') == 0:
                            continue 
                        val3 += float(met['value'])
                        t += 1
                    if t > f:
                        f = t
            if f:
                metric.append(dict(index_id='3000117', value=str(val3)))
            v = stage.get(3000016)
            if v is not None:
                val = float(v)
                v2 = stage.get(3000007)
                if v2 is not None:
                    v = round((val - float(v2)) * 100 / val, 2)
                    stage[3000004] = str(v)
                v2 = stage.get(3000017)
                if v2 is not None:
                    v = round(float(v2) * 100 / val, 2)
                    stage[3000015] = str(v)
                    stage[3000014] = str(100-v)
                v2 = stage.get(3001035)
                if v2 is not None:
                    v = round(float(v2) * 100 / val, 2)
                    stage[3000011] = str(v)
                    v3 = stage.get(3001034)
                    if v3 is not None:
                        stage[3000400] = int(float(v2) + float(v3))
                v2 = stage.get(3001032)
                if v2 is not None:
                    v = round(float(v2) * 100 / val, 2)
                    stage[3001023] = str(v)
                v2 = stage.get(3001033)
                if v2 is not None:
                    v = round(float(v2) * 100 / val, 2)
                    stage[3001024] = str(v)
            v = stage.get(3001029)
            if v is not None:
                val = float(v)
                v2 = stage.get(3001030)
                if v2 is not None:
                    if val == 0:
                        v = 0
                    else:
                        v = round((val - float(v2)) * 100 / val, 2)
                    stage[3001031] = str(v)
            v = stage.get(3001021)
            if v is not None:
                val = float(v)
                v2 = stage.get(2000014)
                v3 = stage.get(2000015)
                if val and v2 is not None and v3 is not None:
                    v = round((val - (float(v2) - float(v3))) * 100 / val, 2)
                    if v >= 0: 
                        stage[3001020] = str(v)
            idx = [3000197,3000198,3000103,3000104,3000105,3000106,3000107,3000108,3000109,3000110,3000111,3000112,3000113,3000114,3000115,3000116,3000117]
            met = {}
            rt = None
            for id in idx:
                met[id] = [None, None, 0]
            sql = '''select index_id,value::numeric,record_time,iname from mon_indexdata where uid='%s' and index_id in (%s)''' % (targetId, tuple2(idx))
            result = relate_pg2(pg, sql)
            if result.code == 0:
                for row in result.msg:
                    if row[0] == 3000198:
                        rt = row[2]
                    met[row[0]] = [float(row[1]), row[2], 0]
                if rt and (cdt - rt).seconds < 3600:
                    for m in met.keys():
                        if met[m][1] == rt:
                            met[m][2] = 1
                    bt = stage.get(3000197)
                    if bt is not None:
                        bt = int(bt)
                    ut = stage.get(3000198)
                    if ut is not None:
                        ut = int(ut)
                    if bt and ut:
                        stage[3000031] = str(ut - bt)
                    if met[3000197][2] and int(met[3000197][0]) == bt and ut:
                        tt = ut - met[3000198][2]
                        ts = stage.get(3000103)
                        if ts is not None:
                            ts = float(ts)
                        if tt > 0 and met[3000103][2] and ts and ts > met[3000103][0]:
                            ts = ts - met[3000103][0]
                            v2 = None
                            v3 = None
                            for id in range(3000104,3000118):
                                if met[id][2] and stage.get(id) is not None:
                                    if id < 3000112:
                                        v = round((float(stage[id]) - met[id][0]) * 100 / ts, 2)
                                        if v >= 0:
                                            stage[3001010 + id - 3000104] = str(v)
                                            if id == 3000107:
                                                stage[3000003] = str(100-v)
                                            elif id == 3000108:
                                                stage[3000008] = str(v)
                                    elif id in [3000112,3000113]:
                                        v = round((float(stage[id]) - met[id][0]) / tt)
                                        if v >= 0:
                                            stage[3001087 + id - 3000112] = str(v)
                                    elif id == 3000115:
                                        v2 = round((float(stage[id]) - met[id][0]) / tt)
                                        if v2 >= 0:
                                            stage[3000100] = str(v2)
                                    elif id == 3000116:
                                        v = round((float(stage[id]) - met[id][0]) / tt / 1024)
                                        if v >= 0:
                                            stage[3000101] = str(v)
                                    elif id == 3000117:
                                        v3 = float(stage[id]) - met[id][0]
                            if v2 is not None and v3 is not None and v2 > 0:
                                v = round((v3 * 1000) / v2, 2)
                                if v >= 0:
                                    stage[3000006] = str(v)
        for id in stage.keys():
            if id > 3000000: 
                metric.append(dict(index_id=str(id), value=stage[id]))
        tabular = os_metric(pg, targetId, mets, metric)
    else:
        tabular = None
        metric.append(dict(index_id="3000000", value="连接失败"))
    #metric.append(dict(index_id="3009999", value=str(ct)))
    ct2 = time.time()
    metric.append(dict(index_id="1000101", value=str(int((ct2-ct)*1000))))
    if tabular:
        res = {}
        res["results"]=metric
        res["tabulardatas"]=tabular
        print(json.dumps(res, ensure_ascii=False))
    else:
        print('{"results":' + json.dumps(metric, ensure_ascii=False) + '}')
    ct2 = int(time.time())
    #print('Elapsed: %d' % (ct2-ct))

if __name__ == '__main__':
    main()

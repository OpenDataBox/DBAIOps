import sys

sys.path.append('/usr/software/knowl')
import DBUtil
from datetime import datetime
import json
import time

global version
import warnings
warnings.filterwarnings("ignore")

def get_cluster_info(db, tenant_type, pg, target_id):
    global version
    if tenant_type == "oracle":
        sql = '''select distinct value from ALL_VIRTUAL_SYS_PARAMETER_STAT_AGENT where name='min_observer_version' '''
    else:
        sql = '''select distinct value from __all_virtual_tenant_parameter_stat where name='min_observer_version' '''
    cs = DBUtil.getValue(db, sql)
    version = cs.fetchone()[0]
    sql = "delete from p_normal_cib where target_id='%s' and index_id=1000005 and cib_name in ('version','toolType')" % target_id
    pg.execute(sql)
    sql = """insert into p_normal_cib(target_id,index_id,cib_name,cib_value,record_time) values('%s',1000005,'version','%s',now()),
    ('%s',1000005,'toolType','%s',now())""" % (target_id, version, target_id, tenant_type)
    pg.execute(sql)
    pg.conn.commit()

    if version < '4.0':
        if tenant_type == "oracle":
            sql = "select distinct name,value,TENANT_ID from ALL_VIRTUAL_SYS_PARAMETER_STAT_AGENT t1, ALL_VIRTUAL_DATABASE_AGENT t2 where name like 'cluster%'"
        else:
            sql = "select distinct name,value,tenant_id from gv$tenant t1, __all_virtual_tenant_parameter_stat t2 where t2.name like 'cluster%'"
    else:
        if tenant_type == "oracle":
            sql = "select distinct name,value,t2.TENANT_ID from V$OB_PARAMETERS t1, dba_ob_tenants t2 where name like 'cluster%'"
        else:
            sql = "select distinct name,value,t1.tenant_id from DBA_OB_TENANTS t1, __all_virtual_tenant_parameter_stat t2 where t2.name like 'cluster%'"
    cursor = DBUtil.getValue(db, sql)
    rs = cursor.fetchall()
    cluster_id = ''
    cluster_name = ''
    tenant_id = ''
    if rs:
        for row in rs:
            if row[0] == 'cluster_id':
                cluster_id = row[1]
            elif row[0] == 'cluster':
                cluster_name = row[1]
            tenant_id = row[2]
    return cluster_id, cluster_name, tenant_id


mdict = {'rpc packet in': 2812001, 'rpc packet in bytes': 2812002, 'rpc packet out': 2812003,
         'rpc packet out bytes': 2812004, 'rpc deliver fail': 2812005, 'rpc net delay': 2812006,
         'rpc net frame delay': 2812007, 'mysql packet in': 2812008, 'mysql packet in bytes': 2812009,
         'mysql packet out': 2812010, 'mysql packet out bytes': 2812011, 'mysql deliver fail': 2812012,
         'rpc compress original packet cnt': 2812013, 'rpc compress compressed packet cnt': 2812014,
         'rpc compress original size': 2812015, 'rpc compress compressed size': 2812016,
         'rpc stream compress original packet cnt': 2812017, 'rpc stream compress compressed packet cnt': 2812018,
         'rpc stream compress original size': 2812019, 'rpc stream compress compressed size': 2812020,
         'request enqueue count': 2812021, 'request dequeue count': 2812022, 'request queue time': 2812023,
         'trans commit log sync time': 2812024, 'trans commit log sync count': 2812025,
         'trans commit log submit count': 2812026, 'trans system trans count': 2812027,
         'trans user trans count': 2812028, 'trans start count': 2812029, 'trans total used time': 2812030,
         'trans commit count': 2812031, 'trans commit time': 2812032, 'trans rollback count': 2812033,
         'trans rollback time': 2812034, 'trans timeout count': 2812035, 'trans single partition count': 2812036,
         'trans multi partition count': 2812037, 'trans zero partition count': 2812038,
         'redo log replay count': 2812039, 'redo log replay time': 2812040, 'prepare log replay count': 2812041,
         'prepare log replay time': 2812042, 'commit log replay count': 2812043, 'commit log replay time': 2812044,
         'abort log replay count': 2812045, 'abort log replay time': 2812046, 'clear log replay count': 2812047,
         'clear log replay time': 2812048, 'sp redo log cb count': 2812049, 'sp redo log cb time': 2812050,
         'sp commit log cb count': 2812051, 'sp commit log cb time': 2812052, 'redo log cb count': 2812053,
         'redo log cb time': 2812054, 'prepare log cb count': 2812055, 'prepare log cb time': 2812056,
         'commit log cb count': 2812057, 'commit log cb time': 2812058, 'abort log cb count': 2812059,
         'abort log cb time': 2812060, 'clear log cb count': 2812061, 'clear log cb time': 2812062,
         'trans memtable end count': 2812063, 'trans memtable end time': 2812064, 'trans callback sql count': 2812065,
         'trans callback sql time': 2812066, 'strong consistency stmt timeout count': 2812067,
         'slave read stmt timeout count': 2812068, 'slave read stmt retry count': 2812069,
         'trans fill redo log count': 2812070, 'trans fill redo log time': 2812071, 'trans submit log count': 2812072,
         'trans submit log time': 2812073, 'gts request total count': 2812074, 'gts acquire total time': 2812075,
         'gts acquire total count': 2812076, 'gts acquire total wait count': 2812077, 'trans stmt total count': 2812078,
         'trans stmt interval time': 2812079, 'trans batch commit count': 2812080, 'trans relocate row count': 2812081,
         'trans relocate total time': 2812082, 'trans multi partition update stmt count': 2812083,
         'gts wait elapse total time': 2812084, 'gts wait elapse total count': 2812085,
         'gts wait elapse total wait count': 2812086, 'gts rpc count': 2812087, 'gts try acquire total count': 2812088,
         'gts try wait elapse total count': 2812089, 'ha gts handle get request count': 2812090,
         'ha gts send get response count': 2812091, 'ha gts handle ping request count': 2812092,
         'ha gts handle ping response count': 2812093, 'sql select count': 2812094, 'sql select time': 2812095,
         'sql insert count': 2812096, 'sql insert time': 2812097, 'sql replace count': 2812098,
         'sql replace time': 2812099, 'sql update count': 2812100, 'sql update time': 2812101,
         'sql delete count': 2812102, 'sql delete time': 2812103, 'sql other count': 2812104, 'sql other time': 2812105,
         'ps prepare count': 2812106, 'ps prepare time': 2812107, 'ps execute count': 2812108,
         'ps close count': 2812109, 'ps close time': 2812110, 'opened cursors current': 2812111,
         'opened cursors cumulative': 2812112, 'sql local count': 2812113, 'sql remote count': 2812114,
         'sql distributed count': 2812115, 'active sessions': 2812116, 'single query count': 2812117,
         'multiple query count': 2812118, 'multiple query with one stmt count': 2812119,
         'sql inner select count': 2812120, 'sql inner select time': 2812121, 'sql inner insert count': 2812122,
         'sql inner insert time': 2812123, 'sql inner replace count': 2812124, 'sql inner replace time': 2812125,
         'sql inner update count': 2812126, 'sql inner update time': 2812127, 'sql inner delete count': 2812128,
         'sql inner delete time': 2812129, 'sql inner other count': 2812130, 'sql inner other time': 2812131,
         'row cache hit': 2812132, 'row cache miss': 2812133, 'block index cache hit': 2812134,
         'block index cache miss': 2812135, 'bloom filter cache hit': 2812136, 'bloom filter cache miss': 2812137,
         'bloom filter filts': 2812138, 'bloom filter passes': 2812139, 'block cache hit': 2812140,
         'block cache miss': 2812141, 'location cache hit': 2812142, 'location cache miss': 2812143,
         'location cache wait': 2812144, 'location cache get hit from proxy virtual table': 2812145,
         'location cache get miss from proxy virtual table': 2812146, 'location cache nonblock renew': 2812147,
         'location cache nonblock renew ignored': 2812148, 'location nonblock get hit': 2812149,
         'location nonblock get miss': 2812150, 'location cache rpc renew count': 2812151,
         'location cache renew': 2812152, 'location cache renew ignored': 2812153, 'mmap count': 2812154,
         'munmap count': 2812155, 'mmap size': 2812156, 'munmap size': 2812157, 'kvcache sync wash time': 2812158,
         'kvcache sync wash count': 2812159, 'location cache rpc renew fail count': 2812160,
         'location cache sql renew count': 2812161, 'location cache ignore rpc renew count': 2812162,
         'fuse row cache hit': 2812163, 'fuse row cache miss': 2812164, 'schema cache hit': 2812165,
         'schema cache miss': 2812166, 'clog cache hit': 2812167, 'clog cache miss': 2812168,
         'index clog cache hit': 2812169, 'index clog cache miss': 2812170, 'user tab col stat cache hit': 2812171,
         'user tab col stat cache miss': 2812172, 'user table stat cache hit': 2812173,
         'user table stat cache miss': 2812174, 'opt table stat cache hit': 2812175,
         'opt table stat cache miss': 2812176, 'opt column stat cache hit': 2812177,
         'opt column stat cache miss': 2812178, 'tmp page cache hit': 2812179, 'tmp page cache miss': 2812180,
         'tmp block cache hit': 2812181, 'tmp block cache miss': 2812182, 'io read count': 2812183,
         'io read delay': 2812184, 'io read bytes': 2812185, 'io write count': 2812186, 'io write delay': 2812187,
         'io write bytes': 2812188, 'memstore scan count': 2812189, 'memstore scan succ count': 2812190,
         'memstore scan fail count': 2812191, 'memstore get count': 2812192, 'memstore get succ count': 2812193,
         'memstore get fail count': 2812194, 'memstore apply count': 2812195, 'memstore apply succ count': 2812196,
         'memstore apply fail count': 2812197, 'memstore row count': 2812198, 'memstore get time': 2812199,
         'memstore scan time': 2812200, 'memstore apply time': 2812201, 'memstore read lock succ count': 2812202,
         'memstore read lock fail count': 2812203, 'memstore write lock succ count': 2812204,
         'memstore write lock fail count': 2812205, 'memstore wait write lock time': 2812206,
         'memstore wait read lock time': 2812207, 'io read micro index count': 2812208,
         'io read micro index bytes': 2812209, 'io prefetch micro block count': 2812210,
         'io prefetch micro block bytes': 2812211, 'io read uncompress micro block count': 2812212,
         'io read uncompress micro block bytes': 2812213, 'storage read row count': 2812214,
         'storage delete row count': 2812215, 'storage insert row count': 2812216, 'storage update row count': 2812217,
         'memstore mutator replay time': 2812218, 'memstore mutator replay count': 2812219,
         'memstore row purge count': 2812220, 'memstore row compaction count': 2812221, 'io read queue delay': 2812222,
         'io write queue delay': 2812223, 'io read callback queuing delay': 2812224,
         'io read callback process delay': 2812225, 'warm up request count': 2812226,
         'warm up request scan count': 2812227, 'warm up request get count': 2812228,
         'warm up request multi get count': 2812229, 'warm up request send count': 2812230,
         'warm up request send size': 2812231, 'warm up request in drop count': 2812232,
         'warm up request out drop count': 2812233, 'bandwidth in throttle size': 2812234,
         'bandwidth out throttle size': 2812235, 'warm up request ignored when send queue is full': 2812236,
         'warm up request rowkey check count': 2812237, 'warm up request multi scan count': 2812238,
         'memstore read row count': 2812239, 'ssstore read row count': 2812240, 'memstore big gap row count': 2812241,
         'memstore small gap row count': 2812242, 'memstore big gap count': 2812243,
         'memstore small gap count': 2812244, 'ssstore big gap row count': 2812245,
         'ssstore small gap row count': 2812246, 'ssstore big gap count': 2812247, 'ssstore small gap count': 2812248,
         'memstore range purge count': 2812249, 'memstore write lock wakenup count in lock_wait_mgr': 2812250,
         'memstore active purge submit sdr count': 2812251, 'memstore active purge handle sdr succ count': 2812252,
         'memstore active purge handle sdr fail count': 2812253,
         'memstore active purge handle sdr retry count': 2812254, 'memstore active purge handle sdr delay': 2812255,
         'rowid hit count': 2812256, 'exist row effect read': 2812257, 'exist row empty read': 2812258,
         'get row effect read': 2812259, 'get row empty read': 2812260, 'scan row effect read': 2812261,
         'scan row empty read': 2812262, 'bandwidth in sleep us': 2812263, 'bandwidth out sleep us': 2812264,
         'memstore write lock wait timeout count': 2812265, 'backup io read count': 2812266,
         'backup io read bytes': 2812267, 'backup io write count': 2812268, 'backup io write bytes': 2812269,
         'cos io read count': 2812270, 'cos io read bytes': 2812271, 'cos io write count': 2812272,
         'cos io write bytes': 2812273, 'cos io list count': 2812274, 'cos list io limit count': 2812275,
         'backup delete count': 2812276, 'cos delete count': 2812277, 'backup io read delay': 2812278,
         'backup io write delay': 2812279, 'cos io read delay': 2812280, 'cos io write delay': 2812281,
         'cos io list delay': 2812282, 'backup delete delay': 2812283, 'cos delete delay': 2812284,
         'backup io list count': 2812285, 'backup io read failed count': 2812286,
         'backup io write failed count': 2812287, 'backup io delete failed count': 2812288,
         'backup io list failed count': 2812289, 'refresh schema count': 2812290, 'refresh schema time': 2812291,
         'inner sql connection execute count': 2812292, 'inner sql connection execute time': 2812293,
         'partition table operator get count': 2812294, 'partition table operator get time': 2812295,
         'submitted to sliding window log count': 2812296, 'submitted to sliding window log size': 2812297,
         'index log flushed count': 2812298, 'index log flushed clog size': 2812299, 'clog flushed count': 2812300,
         'clog flushed size': 2812301, 'clog read size': 2812302, 'clog read count': 2812303,
         'clog disk read size': 2812304, 'clog disk read count': 2812305, 'clog disk read time': 2812306,
         'clog fetch log size': 2812307, 'clog fetch log count': 2812308, 'clog fetch log by localtion size': 2812309,
         'clog fetch log by location count': 2812310, 'clog read request succ size': 2812311,
         'clog read request succ count': 2812312, 'clog read request fail count': 2812313,
         'clog leader confirm time': 2812314, 'clog flush task generate count': 2812315,
         'clog flush task release count': 2812316, 'clog rpc delay time': 2812317, 'clog rpc count': 2812318,
         'clog non kv cache hit count': 2812319, 'clog rpc request handle time': 2812320,
         'clog rpc request count': 2812321, 'clog cache hit count': 2812322, 'clog state loop count': 2812323,
         'clog state loop time': 2812324, 'clog replay loop count': 2812325, 'clog replay loop time': 2812326,
         'clog to leader active count': 2812327, 'clog to leader active time': 2812328, 'on success cb count': 2812329,
         'on success cb time': 2812330, 'on leader revoke count': 2812331, 'on leader revoke time': 2812332,
         'on leader takeover count': 2812333, 'on leader takeover time': 2812334, 'clog write count': 2812335,
         'clog write time': 2812336, 'ilog write count': 2812337, 'ilog write time': 2812338,
         'clog flushed time': 2812339, 'clog task cb count': 2812340, 'clog cb queue time': 2812341,
         'clog ack count': 2812342, 'clog ack time': 2812343, 'clog first ack count': 2812344,
         'clog first ack time': 2812345, 'clog leader confirm count': 2812346, 'clog batch cb count': 2812347,
         'clog batch cb queue time': 2812348, 'clog memstore mutator total size': 2812349,
         'clog trans log total size': 2812350, 'clog submit log total size': 2812351,
         'clog batch buffer total size': 2812352, 'ilog batch buffer total size': 2812353,
         'clog file total size': 2812354, 'ilog file total size': 2812355, 'clog batch submitted count': 2812356,
         'clog batch committed count': 2812357, 'external log service fetch log size': 2812358,
         'external log service fetch log count': 2812359, 'external log service fetch rpc count': 2812360,
         'external log service heartbeat rpc count': 2812361, 'external log service heartbeat partition count': 2812362,
         'replay engine success replay transaction log count': 2812363,
         'replay engine success replay transaction log time': 2812364,
         'replay engine fail replay transaction log count': 2812365,
         'replay engine fail replay transaction log time': 2812366,
         'replay engine success replay start_membership log count': 2812367,
         'replay engine success replay start_membership log time': 2812368,
         'replay engine fail replay start_membership log count': 2812369,
         'replay engine fail replay start_membership log time': 2812370,
         'replay engine success replay offline replica count': 2812371,
         'replay engine fail replay offline replica count': 2812372, 'replay engine retry replay task count': 2812373,
         'replay engine handle replay task count': 2812374, 'replay engine total handle time': 2812375,
         'replay engine submitted replay task count': 2812376,
         'replay engine submitted transaction replay task count': 2812377,
         'replay engine submitted freeze replay task count': 2812378,
         'replay engine submitted offline replay task count': 2812379,
         'replay engine submitted split replay task count': 2812380,
         'replay engine submitted start membership replay task count': 2812381,
         'replay engine success replay split log count': 2812382, 'replay engine fail replay split log count': 2812383,
         'replay engine submitted partition meta replay task count': 2812384,
         'replay engine success replay partition meta log count': 2812385,
         'replay engine fail replay partition meta log count': 2812386,
         'replay engine submitted flashback replay task count': 2812387,
         'replay engine success replay flashback replica count': 2812388,
         'replay engine fail replay flashback replica count': 2812389,
         'replay engine submitted add partition to pg replay task count': 2812390,
         'replay engine success replay add partition to pg count': 2812391,
         'replay engine fail replay add partition to pg count': 2812392,
         'replay engine submitted remove pg partition replay task count': 2812393,
         'replay engine success replay remove pg partition count': 2812394,
         'replay engine fail replay remove pg partition count': 2812395,
         'replay engine handle submit task count': 2812396, 'replay engine handle submit task size': 2812397,
         'replay engine handle submit time': 2812398, 'election change leader count': 2812399,
         'election leader revoke count': 2812400, 'observer partition table updater batch count': 2812401,
         'observer partition table updater count': 2812402, 'observer partition table updater process time': 2812403,
         'observer partition table updater drop task count': 2812404,
         'observer partition table updater reput to queue count': 2812405,
         'observer partition table updater execute fail times': 2812406,
         'observer partition table updater success execute count': 2812407,
         'observer partition table updater total task count': 2812408, 'partition migrate count': 2812409,
         'partition migrate time': 2812410, 'partition add count': 2812411, 'partition add time': 2812412,
         'partition rebuild count': 2812413, 'partition rebuild time': 2812414, 'partition transform count': 2812415,
         'partition transform time': 2812416, 'partition remove count': 2812417, 'partition remove time': 2812418,
         'partition change member count': 2812419, 'partition change member time': 2812420,
         'succ switch leader count': 2812421, 'failed switch leader count': 2812422, 'success rpc process': 2812423,
         'failed rpc process': 2812424, 'balancer succ execute count': 2812425,
         'balancer failed execute count': 2812426, 'rebalance task failed execute count': 2812427,
         'partition modify quorum count': 2812428, 'partition modify quorum time': 2812429,
         'copy global index sstable count': 2812430, 'copy global index sstable time': 2812431,
         'copy local index sstable count': 2812432, 'copy local index sstable time': 2812433,
         'standby cutdata task count': 2812435, 'build only in member list count': 2812436,
         'build only in member list time': 2812437, 'single retrieve execute count': 2812438,
         'single retrieve execute time': 2812439, 'multi retrieve execute count': 2812440,
         'multi retrieve execute time': 2812441, 'multi retrieve rows': 2812442, 'single insert execute count': 2812443,
         'single insert execute time': 2812444, 'multi insert execute count': 2812445,
         'multi insert execute time': 2812446, 'multi insert rows': 2812447, 'single delete execute count': 2812448,
         'single delete execute time': 2812449, 'multi delete execute count': 2812450,
         'multi delete execute time': 2812451, 'multi delete rows': 2812452, 'single update execute count': 2812453,
         'single update execute time': 2812454, 'multi update execute count': 2812455,
         'multi update execute time': 2812456, 'multi update rows': 2812457,
         'single insert_or_update execute count': 2812458, 'single insert_or_update execute time': 2812459,
         'multi insert_or_update execute count': 2812460, 'multi insert_or_update execute time': 2812461,
         'multi insert_or_update rows': 2812462, 'single replace execute count': 2812463,
         'single replace execute time': 2812464, 'multi replace execute count': 2812465,
         'multi replace execute time': 2812466, 'multi replace rows': 2812467, 'batch retrieve execute count': 2812468,
         'batch retrieve execute time': 2812469, 'batch retrieve rows': 2812470, 'batch hybrid execute count': 2812471,
         'batch hybrid execute time': 2812472, 'batch hybrid retrieve rows': 2812473,
         'batch hybrid insert rows': 2812474, 'batch hybrid delete rows': 2812475, 'batch hybrid update rows': 2812476,
         'batch hybrid insert_or_update rows': 2812477, 'batch hybrid replace rows': 2812478,
         'table api login count': 2812479, 'table api OB_TRANSACTION_SET_VIOLATION count': 2812480,
         'query count': 2812481, 'query time': 2812482, 'query row count': 2812483, 'hbase scan count': 2812484,
         'hbase scan time': 2812485, 'hbase scan row count': 2812486, 'hbase put count': 2812487,
         'hbase put time': 2812488, 'hbase put row count': 2812489, 'hbase delete count': 2812490,
         'hbase delete time': 2812491, 'hbase delete row count': 2812492, 'hbase append count': 2812493,
         'hbase append time': 2812494, 'hbase append row count': 2812495, 'hbase increment count': 2812496,
         'hbase increment time': 2812497, 'hbase increment row count': 2812498, 'hbase check_put count': 2812499,
         'hbase check_put time': 2812500, 'hbase check_put row count': 2812501, 'hbase check_delete count': 2812502,
         'hbase check_delete time': 2812503, 'hbase check_delete row count': 2812504, 'hbase hybrid count': 2812505,
         'hbase hybrid time': 2812506, 'hbase hybrid row count': 2812507, 'single increment execute count': 2812508,
         'single increment execute time': 2812509, 'multi increment execute count': 2812510,
         'multi increment execute time': 2812511, 'multi increment rows': 2812512,
         'single append execute count': 2812513, 'single append execute time': 2812514,
         'multi append execute count': 2812515, 'multi append execute time': 2812516, 'multi append rows': 2812517,
         'DB time': 2812518, 'DB CPU': 2812519, 'DB inner sql time': 2812520, 'DB inner sql CPU': 2812521,
         'background elapsed time': 2812522, 'background cpu time': 2812523, '(backup/restore) cpu time': 2812524,
         'Tablespace encryption elapsed time': 2812525, 'Tablespace encryption cpu time': 2812526,
         'location cache size': 2812527, 'clog cache size': 2812528, 'index clog cache size': 2812529,
         'user table col stat cache size': 2812530, 'index cache size': 2812531, 'sys block cache size': 2812532,
         'user block cache size': 2812533, 'sys row cache size': 2812534, 'user row cache size': 2812535,
         'bloom filter cache size': 2812536, 'bloom filter cache strategy': 2812537, 'active memstore used': 2812538,
         'total memstore used': 2812539, 'major freeze trigger': 2812540, 'memstore limit': 2812541,
         'min memory size': 2812542, 'max memory size': 2812543, 'memory usage': 2812544, 'min cpus': 2812545,
         'max cpus': 2812546, 'cpu usage': 2812547, 'disk usage': 2812548, 'observer memory used size': 2812549,
         'observer memory free size': 2812550, 'is mini mode': 2812551, 'observer memory hold size': 2812552,
         'clog disk free size': 2812553, 'clog disk free ratio': 2812554,
         'clog last check log file collect time': 2812555, 'oblogger log bytes': 2812556, 'election log bytes': 2812557,
         'rootservice log bytes': 2812558, 'oblogger total log count': 2812559, 'election total log count': 2812560,
         'rootservice total log count': 2812561, 'async tiny log write count': 2812562,
         'async normal log write count': 2812563, 'async large log write count': 2812564,
         'async tiny log dropped count': 2812565, 'async normal log dropped count': 2812566,
         'async large log dropped count': 2812567, 'async active tiny log count': 2812568,
         'async active normal log count': 2812569, 'async active large log count': 2812570,
         'async released tiny log count': 2812571, 'async released normal log count': 2812572,
         'async released large log count': 2812573, 'async error log dropped count': 2812574,
         'async warn log dropped count': 2812575, 'async info log dropped count': 2812576,
         'async trace log dropped count': 2812577, 'async debug log dropped count': 2812578,
         'async log flush speed': 2812579, 'async generic log write count': 2812580,
         'async user request log write count': 2812581, 'async data maintain log write count': 2812582,
         'async root service log write count': 2812583, 'async schema log write count': 2812584,
         'async force allow log write count': 2812585, 'async generic log dropped count': 2812586,
         'async user request log dropped count': 2812587, 'async data maintain log dropped count': 2812588,
         'async root service log dropped count': 2812589, 'async schema log dropped count': 2812590,
         'async force allow log dropped count': 2812591, 'async tiny log write count for error log': 2812592,
         'async normal log write count for error log': 2812593, 'async large log write count for err/or log': 2812594,
         'async tiny log dropped count for error log': 2812595, 'async normal log dropped count for error log': 2812596,
         'async large log dropped count for error log': 2812597, 'async active tiny log count for error log': 2812598,
         'async active normal log count for error log': 2812599, 'async active large log count for error log': 2812600,
         'async released tiny log count for error log': 2812601,
         'async released normal log count for error log': 2812602,
         'async released large log count for error log': 2812603,
         'observer partition table updater user table queue size': 2812604,
         'observer partition table updater system table queue size': 2812605,
         'observer partition table updater core table queue size': 2812606, 'rootservice start time': 2812607,
         'rootservice waiting task count with high priority': 2812608,
         'rootservice scheduled task count with high priority': 2812609,
         'rootservice waiting task count with low priority': 2812610,
         'rootservice scheduled task count with low priority': 2812611,
         'trans distributed stmt count': 2812613,
         'trans local stmt count': 2812614,
         'trans remote stmt count': 2812615,
         'sp trans total used time': 2812616,
         'backup tagging count': 2812617,
         'backup tagging failed count': 2812618,
         'obs io read count': 2812619,
         'obs io read bytes': 2812620,
         'obs io write count': 2812621,
         'obs io write bytes': 2812622,
         'obs io list count': 2812623,
         'obs list io limit count': 2812624,
         'obs delete count': 2812625,
         'obs io read delay': 2812626,
         'obs io write delay': 2812627,
         'obs io list delay': 2812628,
         'obs delete delay': 2812629,
         'accessed data micro block count': 2812800,
         'accessed index micro block count': 2812801,
         'active proxy loader count for principal server': 2812802,
         'backup io tagging count': 2812803,
         'backup io tagging failed count': 2812804,
         'blockscaned data micro block count': 2812805,
         'blockscaned row count': 2812806,
         'cpu time': 2812807,
         'data micro block cache hit': 2812808,
         'distributed trans total used time': 2812809,
         'expired proxy loader count': 2812810,
         'failed proxy loader count': 2812811,
         'ha gts cache hit count': 2812812,
         'ha gts cache miss count': 2812813,
         'ha gts source request cost time': 2812814,
         'ha gts source request count': 2812815,
         'index block cache size': 2812816,
         'index micro block cache hit': 2812817,
         'load proxy request count': 2812818,
         'local trans total used time': 2812819,
         'log stream table operator get count': 2812820,
         'log stream table operator get time': 2812821,
         'proxy loading task count waiting in queue': 2812822,
         'query_and_mutate count': 2812823,
         'query_and_mutate row count': 2812824,
         'query_and_mutate time': 2812825,
         'read elr row count': 2812826,
         'secondary meta cache hit': 2812827,
         'secondary meta cache miss': 2812828,
         'sql distributed execute time': 2812829,
         'sql local execute time': 2812830,
         'sql remote execute time': 2812831,
         'storage filtered row count': 2812832,
         'table col stat cache size': 2812833,
         'table stat cache size': 2812834,
         'tablet ls cache hit': 2812835,
         'tablet ls cache miss': 2812836,
         'tablet ls cache size': 2812837,
         'total file count in fill file id cache': 2812838,
         'total time cost on fill file id cache': 2812839,
         'trans distribute trans count': 2812840,
         'trans early lock release enable count': 2812841,
         'trans early lock release unable count': 2812842,
         'trans local trans count': 2812843,
         'trans without participant count': 2812844,
         'user logons cumulative': 2812845,
         'user logons failed cumulative': 2812846,
         'user logons time cumulative': 2812847,
         'user logouts cumulative': 2812848,
         'worker time': 2812849,
         'opt ds stat cache hit': 2812850,
         'opt ds stat cache miss': 2812851,
         'standby fetch log bandwidth limit': 2812852,
         'standby fetch log bytes': 2812853,
         'storage meta cache hit': 2812854,
         'storage meta cache miss': 2812855,
         'tablet cache hit': 2812856,
         'tablet cache miss': 2812857,
         'tx data hit kv cache count': 2812858,
         'tx data hit mini cache count': 2812859,
         'tx data read tx ctx count': 2812860,
         'tx data read tx data memtable count': 2812861,
         'tx data read tx data sstable count': 2812862,
         'schema history cache hit': 2816000,
         'schema history cache miss': 2816001,
         'palf write io count to disk': 2816002,
         'palf write size to disk': 2816003,
         'palf write total time to disk': 2816004,
         'palf read count from cache': 2816005,
         'palf read size from cache': 2816006,
         'palf read total time from cache': 2816007,
         'palf read io count from disk': 2816008,
         'palf read size from disk': 2816009,
         'palf read total time from disk': 2816010,
         'palf handle rpc request count': 2816011,
         'archive read log size': 2816012,
         'archive write log size': 2816013,
         'restore read log size': 2816014,
         'restore write log size': 2816015,
         'wr snapshot task elapse time': 2816016,
         'wr snapshot task cpu time': 2816017,
         'wr purge task elapse time': 2816018,
         'wr purge task cpu time': 2816019,
         'wr schedular elapse time': 2816020,
         'wr schedular cpu time': 2816021,
         'wr user submit snapshot elapse time': 2816022,
         'wr user submit snapshot cpu time': 2816023,
         'wr collected active session history row count': 2816024,
         'ash schedular elapse time': 2816025,
         'effective observer memory limit': 2816026,
         'effective system memory': 2816027,
         'effective hidden sys memory': 2816028,
         'max session num': 2816029}

event_dict = {'bloomfilter build read': {'waits': 2813000, 'time': 2814000},
              'db file compact read': {'waits': 2813001, 'time': 2814001},
              'db file compact write': {'waits': 2813002, 'time': 2814002},
              'db file index build read': {'waits': 2813003, 'time': 2814003},
              'db file index build write': {'waits': 2813004, 'time': 2814004},
              'db file migrate read': {'waits': 2813005, 'time': 2814005},
              'db file migrate write': {'waits': 2813006, 'time': 2814006},
              'memstore memory page alloc info': {'waits': 2813007, 'time': 2814007},
              'memstore memory page alloc wait': {'waits': 2813008, 'time': 2814008},
              'db file data index read': {'waits': 2813009, 'time': 2814009},
              'db file data read': {'waits': 2813010, 'time': 2814010},
              'interm result disk read': {'waits': 2813011, 'time': 2814011},
              'interm result disk write': {'waits': 2813012, 'time': 2814012},
              'row store disk read': {'waits': 2813013, 'time': 2814013},
              'row store disk write': {'waits': 2813014, 'time': 2814014},
              'wait remove partition': {'waits': 2813015, 'time': 2814015},
              'memstore read lock wait': {'waits': 2813016, 'time': 2814016},
              'memstore write lock wait': {'waits': 2813017, 'time': 2814017},
              'row lock wait': {'waits': 2813018, 'time': 2814018},
              'wait start stmt': {'waits': 2813019, 'time': 2814019},
              'wait end stmt': {'waits': 2813020, 'time': 2814020},
              'wait end trans': {'waits': 2813021, 'time': 2814021},
              'partition location cache lock wait': {'waits': 2813022, 'time': 2814022},
              'latch: kvcache bucket wait': {'waits': 2813023, 'time': 2814023},
              'latch: clog cache lock wait': {'waits': 2813024, 'time': 2814024},
              'latch:plan cache evict lock wait': {'waits': 2813025, 'time': 2814025},
              'latch: sequence cache lock': {'waits': 2813026, 'time': 2814026},
              'latch:server locality cache lock wait': {'waits': 2813027, 'time': 2814027},
              'latch:master rs cache lock wait': {'waits': 2813028, 'time': 2814028},
              'spinlock: ls meta lock wait': {'waits': 2813029, 'time': 2814029},
              'latch: deadlock lock': {'waits': 2813030, 'time': 2814030},
              'latch: tablet bucket lock wait': {'waits': 2813031, 'time': 2814031},
              'px loop condition wait': {'waits': 2813032, 'time': 2814032},
              'hashmap lock wait': {'waits': 2813033, 'time': 2814033},
              'latch: tablet auto increment service wait': {'waits': 2813034, 'time': 2814034}}


def cs(val, dt=False):
    if val is None:
        return ''
    else:
        if dt:
            return val.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return str(val)


def microsecond2date(mircosec):
    timestamp_to_date_time = datetime.datetime.fromtimestamp(mircosec / 1000000).strftime(
        '%Y-%m-%d %H:%M:%S.%f')
    return timestamp_to_date_time


def initDict(mdict):
    sql = '''select * from v$statname'''
    cs1 = DBUtil.getValue(ob, sql)
    rs = cs1.fetchall()
    for row in rs:
        index_id = int(row[2]) + 2812001
        mdict[row[3]] = index_id
    print(mdict)


def get_ob_schemainfo(conn, target_id):
    sql = '''select col1,col2,col3,col4 from p_oracle_cib where target_id='{0}' and index_id=2801010 and 
seq_id>0'''.format(target_id)
    cs1 = DBUtil.getValue(conn, sql)
    rs1 = cs1.fetchall()
    return rs1


def metric_to_his(conn, target_id, schema_lst):
    id_lst = []
    for row in schema_lst:
        schema_id = row[0]
        id_lst.append(schema_id)
    try:
        sql = '''
begin;
insert into mon_indexdata_his select * from mon_indexdata where 
uid in {0};
insert into mon_indexdata_his select * from mon_indexdata where 
uid = '{1}';
delete from mon_indexdata where uid in {0};
delete from mon_indexdata where uid = '{1}';
commit;
'''.format(tuple(id_lst), target_id)
        conn.execute(sql)
    except Exception as e:
        errorInfo = str(e)
        raise Exception(errorInfo)


def ob_disk_size_metric_cluster(db, metric, target_id, pg):
    global version
    if version > '4.0':
        sql2 = '''select tenant_id, round(sum(DATA_SIZE/1024/1024/1024),2) data_size,round(sum(REQUIRED_SIZE/1024/1024/1024),2) disk_size from CDB_OB_TABLET_REPLICAS group by tenant_id
        order by 1'''
        cs2 = DBUtil.getValue(db, sql2)
        rs2 = cs2.fetchall()
        for row in rs2:
            iname = row[0]
            metric.append(dict(index_id=2812863, value=[dict(name=iname, value=cs(row[1]))]))
            metric.append(dict(index_id=2812864, value=[dict(name=iname, value=cs(row[2]))]))

        sql1 = '''select SVR_IP,SVR_PORT, round(sum(DATA_SIZE/1024/1024/1024),2) data_size,round(sum(REQUIRED_SIZE/1024/1024/1024),2) disk_size from CDB_OB_TABLET_REPLICAS group by SVR_IP, SVR_PORT
        order by 1'''
        cs1 = DBUtil.getValue(db, sql1)
        rs1 = cs1.fetchall()
        for row in rs1:
            iname = row[0] + ':' + str(row[1])
            metric.append(dict(index_id=2812866, value=[dict(name=iname, value=cs(row[2]))]))
            metric.append(dict(index_id=2812867, value=[dict(name=iname, value=cs(row[3]))]))
        sql3 = '''select zone, t1.* from 
            (select SVR_IP,SVR_PORT, round(sum(DATA_SIZE/1024/1024/1024),2) data_size,round(sum(REQUIRED_SIZE/1024/1024/1024),2) disk_size from cdb_OB_TABLET_REPLICAS group by SVR_IP, SVR_PORT) t1,
            DBA_OB_SERVERS t2 where t1.SVR_IP= t2.SVR_IP and t1.SVR_PORT = t2.SVR_PORT'''
        cs3 = DBUtil.getValue(db, sql3)
        rs3 = cs3.fetchall()
        zone_dict = dict()
        for row in rs3:
            if row[0] not in zone_dict.keys():
                zone_dict[row[0]] = []
                zone_dict[row[0]].append(row)
            else:
                zone_dict[row[0]].append(row)
        cluster_balance = 1
        for k, v in zone_dict.items():
            if len(v) < 2:
                metric.append(dict(index_id=2812868, value=[dict(name=k, value="0")]))
            else:
                max = min = 0
                for row in v:
                    if row[3] > max:
                        max = row[3]
                    if min == 0:
                        min = row[3]
                    elif row[3] < min:
                        min = row[3]
                if max == 0 and min == 0:
                    metric.append(dict(index_id=2812868, value=[dict(name=k, value="0")]))
                elif max > 0 and min == 0:
                    metric.append(dict(index_id=2812868, value=[dict(name=k, value="2")]))
                    cluster_balance = 0
                if (max - min) / min < 0.1:
                    metric.append(dict(index_id=2812868, value=[dict(name=k, value="1")]))
                else:
                    metric.append(dict(index_id=2812868, value=[dict(name=k, value="2")]))
                    cluster_balance = 0
        metric.append(dict(index_id=2812869, value=cluster_balance))
        sql3 = '''select
                svr_ip,
                svr_port,
                cpu_capacity,
                cpu_assigned,
                round(mem_capacity / 1024 / 1024 / 1024,2) mem_total_GB,
                round(mem_assigned / 1024 / 1024 / 1024,2) mem_assigned_GB,
                round(data_disk_capacity / 1024 / 1024 / 1024,2) data_disk_total_GB,
                round(data_disk_in_use / 1024 / 1024 / 1024,2) data_disk_in_use_GB, 
                round(log_disk_capacity / 1024 / 1024 / 1024,2) log_disk_total_GB,
                round(log_disk_in_use / 1024 / 1024 / 1024,2) log_disk_in_use_GB	
            from
                __all_virtual_server'''
        cs3 = DBUtil.getValue(db, sql3)
        rs3 = cs3.fetchall()
        for row in rs3:
            iname = row[0] + ':' + str(row[1])
            data_disk_usage = round(row[7] / row[6] * 100, 2)
            log_disk_usage = round(row[9] / row[8] * 100, 2)
            cpu_assigned_ratio = round(row[3] / row[2] * 100, 2)
            mem_assigned_ratio = round(row[5] / row[4] * 100, 2)
            metric.append(dict(index_id=2812873, value=[dict(name=iname, value=cs(data_disk_usage))]))
            metric.append(dict(index_id=2812874, value=[dict(name=iname, value=cs(log_disk_usage))]))
            metric.append(dict(index_id=2812875, value=[dict(name=iname, value=cs(cpu_assigned_ratio))]))
            metric.append(dict(index_id=2812876, value=[dict(name=iname, value=cs(mem_assigned_ratio))]))
    else:
        sql2 = '''select tenant_id,round(sum(data_size)/1024/1024/1024,2), round(sum(required_size)/1024/1024/1024,2) from __all_virtual_meta_table group by  tenant_id
        '''
        cs2 = DBUtil.getValue(db, sql2)
        rs2 = cs2.fetchall()
        for row in rs2:
            iname = row[0]
            metric.append(dict(index_id=2812863, value=[dict(name=iname, value=cs(row[1]))]))
            metric.append(dict(index_id=2812864, value=[dict(name=iname, value=cs(row[2]))]))
        sql1 = '''select convert(tenant_id,char),zone, SVR_IP,SVR_PORT, round(sum(data_size)/1024/1024/1024,2), round(sum(required_size)/1024/1024/1024,2) from __all_virtual_meta_table group by  tenant_id, zone, SVR_IP,SVR_PORT'''
        cs1 = DBUtil.getValue(db, sql1)
        rs1 = cs1.fetchall()
        tenant_dict = dict()
        for row in rs1:
            if row[0] not in tenant_dict.keys():
                tenant_dict[row[0]] = []
                tenant_dict[row[0]].append(row)
            else:
                tenant_dict[row[0]].append(row)
        for tenant, value in tenant_dict.items():
            zone_dict = {}
            for row in value:
                if row[0] not in zone_dict.keys():
                    zone_dict[row[1]] = []
                    zone_dict[row[1]].append(row)
                else:
                    zone_dict[row[1]].append(row)
            tenant_balance = 1
            for zone, v in zone_dict.items():
                iname = str(tenant) + '-' + zone
                if len(v) < 2:
                    metric.append(dict(index_id=2812865, value=[dict(name=iname, value="0")]))
                else:
                    max = min = 0
                    for row in v:
                        if row[4] > max:
                            max = row[4]
                        if min == 0:
                            min = row[4]
                        elif row[4] < min:
                            min = row[4]
                    if max == 0 and min == 0:
                        metric.append(dict(index_id=2812865, value=[dict(name=iname, value="0")]))
                    elif max > 0 and min == 0:
                        metric.append(dict(index_id=2812865, value=[dict(name=iname, value="2")]))
                        tenant_balance = 0
                    elif (max - min) / min < 0.1:
                        metric.append(dict(index_id=2812865, value=[dict(name=iname, value="1")]))
                    else:
                        metric.append(dict(index_id=2812865, value=[dict(name=iname, value="2")]))
                        tenant_balance = 0
            metric.append(dict(index_id=2812870, value=[dict(name=tenant, value=tenant_balance)]))
        sql4 = '''select zone, SVR_IP,SVR_PORT, round(sum(data_size)/1024/1024/1024,2), round(sum(required_size)/1024/1024/1024,2) 
            from __all_virtual_meta_table group by  zone, SVR_IP,SVR_PORT'''
        cs4 = DBUtil.getValue(db, sql4)
        rs4 = cs4.fetchall()
        zone_dict = dict()
        for row in rs4:
            if row[0] not in zone_dict.keys():
                zone_dict[row[0]] = []
                zone_dict[row[0]].append(row)
            else:
                zone_dict[row[0]].append(row)
        cluster_balance = 1
        for k, v in zone_dict.items():
            if len(v) < 2:
                metric.append(dict(index_id=2812868, value=[dict(name=k, value="0")]))
            else:
                max = min = 0
                for row in v:
                    if row[3] > max:
                        max = row[3]
                    if min == 0:
                        min = row[3]
                    elif row[3] < min:
                        min = row[3]
                if max == 0 and min == 0:
                    metric.append(dict(index_id=2812868, value=[dict(name=k, value="0")]))
                elif max > 0 and min == 0:
                    metric.append(dict(index_id=2812868, value=[dict(name=k, value="2")]))
                    cluster_balance = 0
                if (max - min) / min < 0.1:
                    metric.append(dict(index_id=2812868, value=[dict(name=k, value="1")]))
                else:
                    metric.append(dict(index_id=2812868, value=[dict(name=k, value="2")]))
                    cluster_balance = 0
        metric.append(dict(index_id=2812869, value=cluster_balance))

        sql3 = '''select t2.id,t2.svr_ip,t2.svr_port,t2.cpu_total,t2.cpu_assigned,round(t2.mem_total/1024/1024/1024,1) mem_total_GB,round(t2.mem_assigned/1024/1024/1024,1) mem_assigned_GB,round(t2.disk_total/1024/1024/1024,1) disk_total_GB,
            round(t2.disk_in_use/1024/1024/1024,2) disk_in_use_GB,t2.unit_num from  __all_virtual_server_stat t2'''
        cs3 = DBUtil.getValue(db, sql3)
        rs3 = cs3.fetchall()
        for row in rs3:
            iname = row[1] + ':' + str(row[2])
            data_disk_usage = round(row[8] / row[7] * 100, 2)
            log_disk_usage = 0
            cpu_assigned_ratio = round(row[4] / row[3] * 100, 2)
            mem_assigned_ratio = round(row[6] / row[5] * 100, 2)
            metric.append(dict(index_id=2812873, value=[dict(name=iname, value=cs(data_disk_usage))]))
            metric.append(dict(index_id=2812874, value=[dict(name=iname, value=cs(log_disk_usage))]))
            metric.append(dict(index_id=2812875, value=[dict(name=iname, value=cs(cpu_assigned_ratio))]))
            metric.append(dict(index_id=2812876, value=[dict(name=iname, value=cs(mem_assigned_ratio))]))
        # blacklist
        sql4 = "SELECT count(*) FROM __all_virtual_election_info WHERE remaining_time_in_blacklist > 0"
        cs4 = DBUtil.getValue(db, sql4)
        rs4 = cs4.fetchone()
        if rs4:
            metric.append(dict(index_id=2810007, value=cs(rs4[0])))


def ob_disk_size_metric_tenant(db, metric, target_id, pg, tenant_type):
    global version
    if version > '4.0':
        sql1 = '''select round(sum(DATA_SIZE/1024/1024/1024),2) data_size,round(sum(REQUIRED_SIZE/1024/1024/1024),2) disk_size from DBA_OB_TABLET_REPLICAS
        order by 1'''
        cs1 = DBUtil.getValue(db, sql1)
        rs1 = cs1.fetchall()
        for row in rs1:
            data_size = row[0]
            request_size = row[1]
            metric.append(dict(index_id=2812863, value=cs(data_size)))
            metric.append(dict(index_id=2812864, value=cs(request_size)))
        if tenant_type == 'oracle':
            sql3 = '''select zone, t1.SVR_IP, t1.SVR_PORT, t1.data_size, t1.disk_size from 
(select SVR_IP,SVR_PORT, round(sum(DATA_SIZE/1024/1024/1024),2) data_size,round(sum(REQUIRED_SIZE/1024/1024/1024),2) disk_size from DBA_OB_TABLET_REPLICAS group by SVR_IP, SVR_PORT) t1,
(select SVR_IP,SVR_PORT, zone from ALL_VIRTUAL_SERVER_AGENT) t2
where t1.SVR_IP = t2.SVR_IP and t1.SVR_port= t2.SVR_port'''
        else:
            sql3 = '''select zone,t1.* from 
(select SVR_IP,SVR_PORT, round(sum(DATA_SIZE/1024/1024/1024),2) data_size,round(sum(REQUIRED_SIZE/1024/1024/1024),2) disk_size from DBA_OB_TABLET_REPLICAS group by SVR_IP, SVR_PORT) t1, 
(select SVR_IP,SVR_PORT,zone from __all_virtual_unit) t2 where t1.SVR_IP = t2.SVR_IP and t1.SVR_port= t2.SVR_port '''
        cs3 = DBUtil.getValue(db, sql3)
        rs3 = cs3.fetchall()
        zone_dict = dict()
        for row in rs3:
            if row[0] not in zone_dict.keys():
                zone_dict[row[0]] = []
                zone_dict[row[0]].append(row)
            else:
                zone_dict[row[0]].append(row)
        tenant_balance = 1
        for k, v in zone_dict.items():
            if len(v) < 2:
                metric.append(dict(index_id=2812865, value=[dict(name=k, value="0")]))
            else:
                max = min = 0
                for row in v:
                    if row[3] > max:
                        max = row[3]
                    if row[3] < min:
                        min = row[3]
                if min == 0:
                    if max - min == 0:
                        metric.append(dict(index_id=2812865, value=[dict(name=k, value="0")]))
                        tenant_balance = 0
                    else:
                        metric.append(dict(index_id=2812865, value=[dict(name=k, value="1")]))
                else:
                    if (max - min) / min < 0.1:
                        metric.append(dict(index_id=2812865, value=[dict(name=k, value="1")]))
                    else:
                        metric.append(dict(index_id=2812865, value=[dict(name=k, value="2")]))
                        tenant_balance = 0
        metric.append(dict(index_id=2812870, value=tenant_balance))


def ob_event_metric(db, metric, target_id, pg):
    sql1 = '''select svr_ip,svr_port, event,total_waits,time_waited_micro/1000 from gV$SYSTEM_EVENT where event in ('bloomfilter build read','db file compact read','db file compact write','db file index build read','db file index build write',
'db file migrate read','db file migrate write','memstore memory page alloc info','memstore memory page alloc wait','db file data index read',
'db file data read','interm result disk read','interm result disk write','row store disk read','row store disk write','wait remove partition',
'memstore read lock wait','memstore write lock wait','row lock wait','wait start stmt','wait end stmt','wait end trans','partition location cache lock wait',
'latch: kvcache bucket wait','latch: clog cache lock wait','latch:plan cache evict lock wait','latch: sequence cache lock','latch:server locality cache lock wait',
'latch:master rs cache lock wait','spinlock: ls meta lock wait','latch: deadlock lock','latch: tablet bucket lock wait','px loop condition wait','hashmap lock wait',
'latch: tablet auto increment service wait')'''
    cs1 = DBUtil.getValue(db, sql1)
    rs1 = cs1.fetchall()
    for row in rs1:
        iname = row[0] + ':' + str(row[1])
        for k, v in event_dict[row[2]].items():
            if k == 'waits':
                metric.append(dict(index_id=v, value=[dict(name=iname, value=cs(row[3]))]))
            elif k == 'time':
                metric.append(dict(index_id=v, value=[dict(name=iname, value=cs(row[4]))]))
    sql2 = '''select svr_ip,svr_port, event,total_waits,time_waited_micro/1000 from gv$system_event where TOTAL_WAITS > 0'''
    cs2 = DBUtil.getValue(db, sql2)
    rs2 = cs2.fetchall()
    for row in rs2:
        iname = row[0] + ':' + str(row[1]) + '-' + str(row[2])
        metric.append(dict(index_id=2813035, value=[dict(name=iname, value=cs(row[3]))]))
        metric.append(dict(index_id=2814035, value=[dict(name=iname, value=cs(row[4]))]))


def transaction_metric(db, metric, target_id, pg):
    sql2 = ''' select distinct iname from mon_indexdata where index_id in (2812884,2812885) and uid='{0}' '''.format(
        target_id)
    cs2 = DBUtil.getValue(pg, sql2)
    rs2 = cs2.fetchall()
    tenant_lst = []
    if rs2:
        tenant_lst = [row[0] for row in rs2]
    if version > '4.0':
        sql = '''select tenant_id, min(CTX_CREATE_TIME) from GV$OB_TRANSACTION_PARTICIPANTS group by tenant_id'''
    else:
        sql = '''select tenant_id,min(ctx_create_time) from __all_virtual_trans_stat group by tenant_id'''
    cs1 = DBUtil.getValue(db, sql)
    rs = cs1.fetchall()
    if rs:
        for row in rs:
            iname = row[0]
            if str(iname) in tenant_lst:
                tenant_lst.remove(str(iname))
            oldest_trans_time = row[1]
            time_duration = (datetime.now() - datetime.strptime(oldest_trans_time, '%Y-%m-%d %H:%M:%S.%f')).seconds
            metric.append(dict(index_id=2812884, value=[dict(name=iname, value=cs(oldest_trans_time))]))
            metric.append(dict(index_id=2812885, value=[dict(name=iname, value=cs(time_duration))]))
        if len(tenant_lst):
            for tenant in tenant_lst:
                metric.append(dict(index_id=2812884, value=[dict(name=tenant, value=cs(0))]))
                metric.append(dict(index_id=2812885, value=[dict(name=tenant, value=cs(0))]))
    else:
        for tenant in tenant_lst:
            metric.append(dict(index_id=2812884, value=[dict(name=tenant, value=cs(0))]))
            metric.append(dict(index_id=2812885, value=[dict(name=tenant, value=cs(0))]))


def transaction_metric_tenant(metric, pg, cluster_target_id, tenant_id):
    sql = '''select index_id, value from mon_Indexdata t1, (select record_time from mon_Indexdata where uid='{0}' 
and index_id=2810000) t2 where uid='{0}' and index_id in (2812884,2812885) and iname='{1}' and 
t1.record_time=t2.record_time'''.format(cluster_target_id, tenant_id)
    cs1 = DBUtil.getValue(pg, sql)
    rs = cs1.fetchall()
    if rs:
        for row in rs:
            if row[0] == 2812884:
                oldest_trans_time = row[1]
            if row[0] == 2812885:
                time_duration = row[1]
        metric.append(dict(index_id=2812884, value=cs(oldest_trans_time)))
        metric.append(dict(index_id=2812885, value=cs(time_duration)))
    else:
        metric.append(dict(index_id=2812884, value=cs(-1)))
        metric.append(dict(index_id=2812885, value=cs(0)))


def tenant_memory_info(metric, pg, cluster_target_id, tenant_id):
    sql = '''
        select
            index_id,
            iname,
            value
        from
            mon_Indexdata t1
        where
            uid='{0}' 
            and index_id in (2814037,2814038,2814048,2814049,2814051,2814053,2814060,2814061,2814054,2814058)
            and (iname like '%-{1}:%' or iname='{1}')
            and record_time in (select record_time from mon_Indexdata where uid=t1.uid
        and index_id=2810000)
    '''.format(cluster_target_id, tenant_id)
    cs1 = DBUtil.getValue(pg, sql)
    rs = cs1.fetchall()
    if rs:
        vals = []
        vals2 = []
        vals3 = []
        vals4 = []
        vals5 = []
        vals6 = []
        vals7 = []
        vals8 = []
        vals9 = []
        vals10 = []
        for row in rs:
            index_id = row[0]
            iname = row[1]
            value = row[2]
            if index_id == 2814037:
                vals.append(dict(name=iname, value=cs(value)))
            if index_id == 2814038:
                vals2.append(dict(name=iname, value=cs(value)))
            if index_id == 2814048:
                vals3.append(dict(name=iname, value=cs(value)))
            if index_id == 2814053:
                vals4.append(dict(name=iname, value=cs(value)))
            if index_id == 2814049:
                vals5.append(dict(name=iname, value=cs(value)))
            if index_id == 2814051:
                vals6.append(dict(name=iname, value=cs(value)))
            if index_id == 2814060:
                vals7.append(dict(name=iname, value=cs(value)))
            if index_id == 2814061:
                vals8.append(dict(name=iname, value=cs(value)))
            if index_id == 2814054:
                vals9.append(dict(name=iname, value=cs(value)))
            if index_id == 2814058:
                vals10.append(dict(name=iname, value=cs(value)))
        metric.append(dict(index_id=2814037, value=vals))
        metric.append(dict(index_id=2814038, value=vals2))
        metric.append(dict(index_id=2814048, value=vals3))
        metric.append(dict(index_id=2814053, value=vals4))
        metric.append(dict(index_id=2814049, value=vals5))
        metric.append(dict(index_id=2814051, value=vals6))
        metric.append(dict(index_id=2814060, value=vals7))
        metric.append(dict(index_id=2814061, value=vals8))
        metric.append(dict(index_id=2814054, value=vals9))
        metric.append(dict(index_id=2814058, value=vals10))


def ob_session_metric(db, metric, target_id, tenant_type, subtype):
    if version > '4.0':
        sql1 = '''select t1.*, case when t2.active_sessions is not null then t2.active_sessions else 0 end  from 
    (select svr_ip,svr_port,count(*) total_sessions from gV$OB_PROCESSLIST group by svr_ip,svr_port) t1
    left join 
    (select svr_ip,svr_port,count(*) active_sessions from gV$OB_PROCESSLIST where state='ACTIVE' group by svr_ip,svr_port) t2
    on t1.svr_ip=t2.svr_ip and t1.svr_port=t2.svr_port'''
        cs1 = DBUtil.getValue(db, sql1)
        rs1 = cs1.fetchall()
        total_sessions = 0
        if rs1:
            for row in rs1:
                iname = row[0] + ':' + str(row[1])
                metric.append(dict(index_id=2812871, value=[dict(name=iname, value=row[2])]))
                metric.append(dict(index_id=2812872, value=[dict(name=iname, value=row[3])]))
                total_sessions += int(row[2])
        if subtype != 'cluster':
            max_connections = 0
            if tenant_type == 'oracle':
                sql2 = '''SELECT SVR_ip,SVR_PORT,value FROM GV$OB_PARAMETERS WHERE NAME LIKE '_resource_limit_max_session_num' '''
                cs2 = DBUtil.getValue(db, sql2)
                rs2 = cs2.fetchall()
                for row in rs2:
                    server1 = row[0] + ':' + str(row[1])
                    if int(row[2]) > 0:
                        max_connections += int(row[2])
                    else:
                        sql3 = '''select SVR_IP, SVR_PORT, round(MEMORY_SIZE*0.05/(1024*100),0) from GV$OB_UNITS'''
                        cs3 = DBUtil.getValue(db, sql3)
                        rs3 = cs3.fetchall()
                        for r in rs3:
                            server2 = r[0] + ':' + str(r[1])
                            if server1 == server2:
                                max_connections += max(100, r[2])
            else:
                sql2 = '''select value from __all_sys_variable where name='max_connections' '''
                cs2 = DBUtil.getValue(db, sql2)
                rs2 = cs2.fetchone()
                max_connections = rs2[0]
            session_usage = round(int(total_sessions) / int(max_connections) * 100, 2)
            metric.append(dict(index_id=2812880, value=cs(session_usage)))
    else:
        if tenant_type == 'oracle':
            sql1 = '''select t1.*, case when t2.active_sessions is not null then t2.active_sessions else 0 end  from 
            (select svr_ip,svr_port,count(*) total_sessions from ALL_VIRTUAL_PROCESSLIST group by svr_ip,svr_port) t1
            left join 
            (select svr_ip,svr_port,count(*) active_sessions from ALL_VIRTUAL_PROCESSLIST where state='ACTIVE' group by svr_ip,svr_port) t2
            on t1.svr_ip=t2.svr_ip and t1.svr_port=t2.svr_port'''
            cs1 = DBUtil.getValue(db, sql1)
            rs1 = cs1.fetchall()
            if rs1:
                for row in rs1:
                    iname = row[0] + ':' + str(row[1])
                    metric.append(dict(index_id=2812871, value=[dict(name=iname, value=row[2])]))
                    metric.append(dict(index_id=2812872, value=[dict(name=iname, value=row[3])]))
        else:
            if subtype == 'cluster':
                sql1 = '''select t1.tenant_name, t1.svr_ip,t1.svr_port, case when t2.total_sessions is not null then t2.total_sessions else 0 end, case when t3.active_sessions is not null then t3.active_sessions else 0 end  from 
            (select tenant_name,svr_ip,svr_port from __all_tenant t1,__all_resource_pool t2,__all_unit t3 where t1.tenant_id=t2.tenant_id and t2.resource_pool_id= t3.resource_pool_id) t1
            left join
            (select tenant, svr_ip,svr_port,count(*) total_sessions from __all_virtual_processlist where length(tenant) > 0  group by tenant, svr_ip,svr_port) t2 on t1.tenant_name=t2.tenant
            and t1.svr_ip=t2.svr_ip and t1.svr_port=t2.svr_port
            left join 
            (select tenant, svr_ip,svr_port,count(*) active_sessions from __all_virtual_processlist where length(tenant) > 0  and state='ACTIVE' group by tenant,svr_ip,svr_port) t3
            on t1.svr_ip=t3.svr_ip and t1.svr_port=t3.svr_port and t1.tenant_name=t3.tenant'''
                cs1 = DBUtil.getValue(db, sql1)
                rs1 = cs1.fetchall()
                for row in rs1:
                    iname = row[1] + ':' + str(row[2]) + '-' + str(row[0])
                    metric.append(dict(index_id=2812871, value=[dict(name=iname, value=row[3])]))
                    metric.append(dict(index_id=2812872, value=[dict(name=iname, value=row[4])]))


def ob_session_metric_3_mysql(metric, pg, cluster_target_id, tenant_name):
    sql = '''select index_id,substr(iname,0,position('-' in iname)), sum(value::numeric) from mon_indexdata where  uid='{0}' 
and index_id in (2812871,2812872) and substr(iname,position('-' in iname)+1) = '{1}' group by index_id, 
substr(iname,0,position('-' in iname))'''.format(cluster_target_id, tenant_name)
    cs1 = DBUtil.getValue(pg, sql)
    rs1 = cs1.fetchall()
    for row in rs1:
        iname = row[1]
        if row[0] == 2812871:
            metric.append(dict(index_id=2812871, value=[dict(name=iname, value=str(row[2]))]))
        elif row[0] == 2812872:
            metric.append(dict(index_id=2812872, value=[dict(name=iname, value=str(row[2]))]))


def ob_locks(db, metric, target_id, pg):
    global version
    tx_cnt = 0
    tx_max_time = 0
    tr_cnt = 0
    tr_max_time = 0
    tm_cnt = 0
    tm_max_time = 0
    if version > '4.0':
        sql1 = '''select * from gv$ob_locks WHERE type='TR' and lMODE='NONE'
    union
    select * from gv$ob_locks WHERE type='TX' and lMODE='NONE'
    union
    select * from gv$ob_locks WHERE type='TM' and lMODE='NONE' '''
        cs1 = DBUtil.getValue(db, sql1)
        rs1 = cs1.fetchall()
        for row in rs1:
            if row[4] == 'TR':
                tr_cnt += 1
                if int(row[9]) > tr_max_time:
                    tr_max_time = int(row[9])
            elif row[4] == 'TX':
                tx_cnt += 1
                if int(row[9]) > tx_max_time:
                    tx_max_time = int(row[9])
            elif row[4] == 'TM':
                tm_cnt += 1
                if int(row[9]) > tm_max_time:
                    tm_max_time = int(row[9])
        tr_max_time = round(tr_max_time / 1000000, 2)
        tx_max_time = round(tx_max_time / 1000000, 2)
        tm_max_time = round(tm_max_time / 1000000, 2)
    else:
        sql1 = '''select 'TR',count(*),max(ctime) from gv$lock WHERE type=0 and lMODE=0'''
        cs1 = DBUtil.getValue(db, sql1)
        rs1 = cs1.fetchall()
        for row in rs1:
            if row[0] == 'TR':
                tr_cnt = row[1]
                if row[2]:
                    tr_max_time = round(int(row[2]) / 1000000, 2)
    metric.append(dict(index_id=2812877, value=cs(tr_cnt)))
    metric.append(dict(index_id=2812878, value=cs(tx_cnt)))
    metric.append(dict(index_id=2812879, value=cs(tm_cnt)))
    metric.append(dict(index_id=2812881, value=cs(tr_max_time)))
    metric.append(dict(index_id=2812882, value=cs(tx_max_time)))
    metric.append(dict(index_id=2812883, value=cs(tm_max_time)))


def ob_metric_cluster(db, metric):
    # from pandas import DataFrame
    # import numpy as np
    # global version
    sql1 = '''select SVR_IP, SVR_PORT, NAME, sum(VALUE) from gv$sysstat group by SVR_IP, SVR_PORT, NAME'''
    cs1 = DBUtil.getValue(db, sql1)
    rs1 = cs1.fetchall()
    for row in rs1:
        iname = row[0] + ':' + str(row[1])
        if 'max cpus' in row[2]:
            metric.append(dict(index_id=2812898, value=[dict(name=iname, value=cs(row[3] / 100))]))
        if row[2] in mdict.keys():
            metric.append(dict(index_id=mdict[row[2]], value=[dict(name=iname, value=cs(row[3]))]))
    t = time.time()
    metric.append(dict(index_id=2812612, value=int(t)))


def ob_metric_tenant(db, metric):
    sql1 = '''select con_id, SVR_IP, SVR_PORT, STAT_ID, NAME, VALUE from gv$sysstat'''
    cs1 = DBUtil.getValue(db, sql1)
    rs1 = cs1.fetchall()
    for row in rs1:
        iname = row[1] + ':' + str(row[2]) + ':' + str(row[0])
        if 'max cpus' in row[4]:
            metric.append(dict(index_id=2812898, value=[dict(name=iname, value=cs(row[5] / 100))]))
        if row[4] in mdict.keys():
            metric.append(dict(index_id=mdict[row[4]], value=[dict(name=iname, value=cs(row[5]))]))
    t = time.time()
    metric.append(dict(index_id=2812612, value=int(t)))


def ob_memstore_info(ob, metric, tenant_type):
    if version > '4.0':
        sql = '''SELECT  SVR_IP, SVR_PORT,
            max(round(MEMSTORE_USED / FREEZE_TRIGGER * 100, 2)) percent_trigger
            FROM
            GV$OB_MEMSTORE group by  SVR_IP, SVR_PORT'''
    else:
        if tenant_type == 'oracle':
            sql = '''select SVR_IP, SVR_PORT, max(round(TOTAL/FREEZE_TRIGGER*100,2)) percent_trigger FROM gv$memstore group by SVR_IP, SVR_PORT'''
        else:
            sql = '''select IP, PORT, max(round(TOTAL/FREEZE_TRIGGER*100,2)) percent_trigger FROM gv$memstore group by IP, PORT'''

    cs1 = DBUtil.getValue(ob, sql)
    rs1 = cs1.fetchall()
    for row in rs1:
        iname = row[0] + ':' + str(row[1])
        metric.append(dict(index_id='2812897', value=[dict(name=iname, value=cs(row[2]))]))

    if version > '4.0':
        sql2 = '''select m.SVR_IP, m.SVR_PORT,max(round(MEMSTORE_USED/m.MEMSTORE_LIMIT/100*p.value*100,2)) from GV$OB_MEMSTORE m, gV$OB_PARAMETERS p 
            where p.name='memstore_limit_percentage'  and p.SVR_IP=m.SVR_IP and p.SVR_PORT=m.SVR_PORT group by m.SVR_IP, m.SVR_PORT'''
    else:
        if tenant_type == 'oracle':
            sql2 = '''select m.SVR_IP, m.SVR_PORT,max(round(TOTAL/m.MEM_LIMIT/100*p.value*100,2)) from gv$memstore m, all_VIRTUAL_SYS_PARAMETER_STAT_AGENT p 
            where p.name='memstore_limit_percentage'  and p.SVR_IP=m.SVR_IP and p.SVR_PORT=m.SVR_PORT group by m.SVR_IP, m.SVR_PORT'''
        else:
            sql2 = '''select m.IP, m.PORT,max(round(TOTAL/m.MEM_LIMIT/100*p.value*100,2)) from gv$memstore m, __all_virtual_tenant_parameter_stat p 
            where p.name='memstore_limit_percentage'  and p.SVR_IP=m.IP and p.SVR_PORT=m.PORT group by m.IP, m.PORT'''

    cs2 = DBUtil.getValue(ob, sql2)
    rs2 = cs2.fetchall()
    for row in rs2:
        iname = row[0] + ':' + str(row[1])
        metric.append(dict(index_id='2812899', value=[dict(name=iname, value=cs(row[2]))]))


def ob_system_memory_info(ob, metric):
    sql = '''
    select
        tenant_id,
        svr_ip,
        svr_port,
        ctx_name,
        sum(used) a,
        sum(hold) a,
        mod_name
    from
        __all_virtual_memory_info
    where hold > 0
    group by
        1,
        2,
        3,
        4,
        7
    '''
    cs1 = DBUtil.getValue(ob, sql)
    rs1 = cs1.fetchall()
    if rs1:
        kvcache = {}
        mem_500 = {}
        tenant_hold = {}
        tenant_used = {}
        mod_hold = {}
        mod_used = {}
        vals = []
        vals2 = []
        for row in rs1:
            tenant_id = str(row[0])
            svr_ip = str(row[1])
            svr_port = str(row[2])
            ctx_name = row[3]
            total_used = row[4]
            hold = row[5]
            mod_name = row[6]
            if tenant_id in tenant_hold.keys():
                tenant_hold[tenant_id] += hold
            else:
                tenant_hold[tenant_id] = hold
            if tenant_id in tenant_used.keys():
                tenant_used[tenant_id] += hold
            else:
                tenant_used[tenant_id] = hold
            iname = svr_ip + ':' + svr_port
            iname2 = ctx_name + '-' + svr_ip + ':' + svr_port
            tenant_info = ctx_name + '-' + tenant_id + ':' + svr_ip + ':' + svr_port
            mod_info = ctx_name + '_' + mod_name + '-' + tenant_id + ':' + svr_ip + ':' + svr_port
            mod_hold[mod_info] = hold
            mod_used[mod_info] = total_used
            vals.append(dict(name=tenant_info, value=cs(total_used)))
            vals2.append(dict(name=tenant_info, value=cs(hold)))
            if tenant_id == 500:
                if iname2 in mem_500.keys():
                    mem_500[iname2] += row[4]
                else:
                    mem_500[iname2] = row[4]
                if 'KVSTORE_CACHE_ID' not in ctx_name:
                    if iname in kvcache.keys():
                        kvcache[iname] += row[4]
                    else:
                        kvcache[iname] = row[4]
        top30_mod_hold = dict(sorted(mod_hold.items(), key=lambda item: item[1], reverse=True)[:50])
        top30_mod_use = dict(sorted(mod_used.items(), key=lambda item: item[1], reverse=True)[:50])
        for iname, row in top30_mod_hold.items():
            metric.append(dict(index_id=2814061, value=[dict(name=iname, value=cs(row))]))
        for iname, row in top30_mod_use.items():
            metric.append(dict(index_id=2814060, value=[dict(name=iname, value=cs(row))]))
        for iname, row in tenant_hold.items():
            metric.append(dict(index_id=2814051, value=[dict(name=iname, value=cs(row))]))
        for iname, row in tenant_used.items():
            metric.append(dict(index_id=2814058, value=[dict(name=iname, value=cs(row))]))
        metric.append(dict(index_id=2814038, value=vals))
        metric.append(dict(index_id=2814053, value=vals2))
        for iname, row in kvcache.items():
            metric.append(dict(index_id=2812916, value=[dict(name=iname, value=cs(row))]))
        for iname, row in mem_500.items():
            metric.append(dict(index_id=2812918, value=[dict(name=iname, value=cs(row[3]))]))

    sql = '''
    select
        tenant_id,
        svr_ip,
        svr_port,
        cache_name,
        cache_size,
        hit_ratio
    from
        __all_virtual_kvcache_info
    '''
    cs1 = DBUtil.getValue(ob, sql)
    rs1 = cs1.fetchall()
    if rs1:
        kvcache_total = {}
        for row in rs1:
            tenant_id = str(row[0])
            svr_ip = str(row[1])
            svr_port = str(row[2])
            cache_name = row[3]
            cache_size = row[4]
            hit_ratio = row[5]
            if tenant_id in kvcache_total.keys():
                kvcache_total[tenant_id] += cache_size
            else:
                kvcache_total[tenant_id] = cache_size
            iname = svr_ip + ':' + svr_port
            tenant_info = cache_name + '-' + tenant_id + ':' + svr_ip + ':' + svr_port
            metric.append(dict(index_id=2814037, value=[dict(name=tenant_info, value=cs(cache_size))]))
            metric.append(dict(index_id=2814048, value=[dict(name=tenant_info, value=cs(hit_ratio))]))
        for iname, row in kvcache_total.items():
            metric.append(dict(index_id=2814049, value=[dict(name=iname, value=cs(row))]))

    sql3 = '''select svr_ip, svr_port,ctx_name,round(sum(hold)/1024) from __all_virtual_memory_info where ctx_name='LIBEASY' group by svr_ip, svr_port'''
    cs3 = DBUtil.getValue(ob, sql3)
    rs3 = cs3.fetchall()
    if rs3:
        for row in rs3:
            iname = row[0] + ':' + str(row[1])
            metric.append(dict(index_id=2812919, value=[dict(name=iname, value=cs(row[3]))]))

        sql4 = '''select svr_ip,svr_port,name,value from __all_virtual_sys_parameter_stat where name in ('__easy_memory_limit','system_memory')'''
        cs4 = DBUtil.getValue(ob, sql4)
        rs4 = cs4.fetchall()
        if rs4:
            param_easy_dict = {}
            param_system_dict = {}
            for row in rs4:
                iname = row[0] + ':' + str(row[1])
                if 'G' in row[3]:
                    set_mem_kb = float(row[3].replace('G', '')) * 1024 * 1024
                elif 'M' in row[3]:
                    set_mem_kb = float(row[3].replace('M', '')) * 1024
                if row[2] == '__easy_memory_limit':
                    param_easy_dict[iname] = set_mem_kb
                elif row[2] == 'system_memory':
                    param_system_dict[iname] = set_mem_kb
        max_easy_ratio = 0
        for row in rs3:
            iname = row[0] + ':' + str(row[1])
            if iname in param_easy_dict.keys():
                ratio = round(row[3] / param_easy_dict[iname] * 100, 2)
                if ratio > max_easy_ratio:
                    max_easy_ratio = ratio
        metric.append(dict(index_id="2812920", value=max_easy_ratio))

        max_system_ratio = 0
        for row in rs1:
            iname = str(row[0]) + ':' + str(row[1])
            if iname in param_system_dict.keys():
                if param_system_dict[iname] == 0:
                    pg = DBUtil.get_pg_from_cfg()
                    _,ssh,_ = DBUtil.getsshinfo(pg, row[0])
                    result = ssh.exec_cmd("cat /proc/meminfo | grep MemAvailable | awk \'{print $2}\'")
                    if isinstance(result,tuple):
                        result = ssh.exec_cmd("cat /proc/meminfo | grep MemFree | awk \'{print $2}\'")
                        if isinstance(result,tuple):
                            raise Exception(result[1])
                        else:
                            ratio = round(row[2] / (row[2] + float(result.strip())) * 100, 2)
                    else:
                        ratio = round(row[2] / (row[2] + float(result.strip())) * 100, 2)
                else:
                    ratio = round(row[2] / param_system_dict[iname] * 100, 2)
                if ratio > max_system_ratio:
                    max_system_ratio = ratio
        metric.append(dict(index_id="2812921", value=max_system_ratio))


def ob_tenant_size_metric_tenant(metric, pg, cluster_target_id, tenant_id):
    sql = '''select index_id, value from mon_Indexdata t1, (select record_time from mon_Indexdata where uid='{0}' 
    and index_id=2810000) t2 where uid='{0}' and index_id in (2812863,2812864,2812870) and iname='{1}' and 
    t1.record_time=t2.record_time'''.format(cluster_target_id, tenant_id)
    cs1 = DBUtil.getValue(pg, sql)
    rs = cs1.fetchall()
    if rs:
        for row in rs:
            if row[0] == 2812863:
                data_size = row[1]
            if row[0] == 2812864:
                request_size = row[1]
            if row[0] == 2812870:
                tenant_balance = row[1]
        metric.append(dict(index_id=2812863, value=cs(data_size)))
        metric.append(dict(index_id=2812864, value=cs(request_size)))
        metric.append(dict(index_id=2812870, value=cs(tenant_balance)))
    else:
        metric.append(dict(index_id=2812863, value=cs(0)))
        metric.append(dict(index_id=2812864, value=cs(0)))
        metric.append(dict(index_id=2812870, value=cs(-1)))

    sql = '''select index_id, substr(iname,position('-' in iname)+1), value from mon_Indexdata t1, (select record_time from mon_Indexdata where uid='{0}' 
    and index_id=2810000) t2 where uid='{0}' and index_id=2812865 and iname like '{1}-%' and 
    t1.record_time=t2.record_time'''.format(cluster_target_id, tenant_id)
    cs1 = DBUtil.getValue(pg, sql)
    rs = cs1.fetchall()
    if rs:
        for row in rs:
            zone = row[1]
            zone_balance = row[2]
            metric.append(dict(index_id=2812865, value=[dict(name=zone, value=zone_balance)]))

def get_sql_retry_cnt(ob, subtype, tenant_type, metric):
    if version < '4.0':
        if subtype == 'cluster':
            sql = """
                select
                    svr_ip,
                    svr_port,
                    at2.tenant_name ,
                    sum(retry_cnt)
                from
                    gv$sql_audit sa,`__all_tenant` at2 
                    where sa.tenant_id = at2.tenant_id 
                group by
                    svr_ip,
                    svr_port,
                    at2.tenant_name
                """
        else:
            if tenant_type == 'oracle':
                sql = """
                    select
                        svr_ip,
                        svr_port,
                        tenant_id,
                        sum(retry_cnt)
                    from
                        gv$sql_audit sa
                    group by
                        svr_ip,
                        svr_port,
                        tenant_id
                    """
            else:
                sql = """
                    select
                        svr_ip,
                        svr_port,
                        tenant_id,
                        sum(retry_cnt)
                    from
                        gv$sql_audit 
                    group by
                        svr_ip,
                        svr_port,
                        tenant_id
                    """
    else:
        if tenant_type == 'oracle':
            sql = """
                select
                    svr_ip,
                    svr_port,
                    at2.tenant_name ,
                    sum(retry_cnt)
                from
                    gv$ob_sql_audit sa,DBA_OB_TENANTS at2 
                    where sa.tenant_id = at2.tenant_id 
                group by
                    svr_ip,
                    svr_port,
                    at2.tenant_name
                """
        else:
            sql = """
                select
                    svr_ip,
                    svr_port,
                    at2.tenant_name ,
                    sum(retry_cnt)
                from
                    gv$ob_sql_audit sa,DBA_OB_TENANTS at2 
                    where sa.tenant_id = at2.tenant_id 
                group by
                    svr_ip,
                    svr_port,
                    at2.tenant_name
                """
    cs1 = DBUtil.getValue(ob, sql)
    rs1 = cs1.fetchall()
    if rs1:
        for row in rs1:
            tenant_info = row[0] + ':' + str(row[1]) + ':' + str(row[2])
            metric.append(dict(index_id=2810005, value=[dict(name=tenant_info, value=cs(row[3]))]))


def check_obproxy_aviable(pg, target_id):
    import requests
    proxy_dict = {}
    sql1 = '''select cib_value from p_normal_cib where target_id='{0}' and cib_name='_obproxy_metric_url' '''.format(target_id)
    cs1 = DBUtil.getValue(pg, sql1)
    rs1 = cs1.fetchone()
    if rs1:
        proxy_list = rs1[0].split(';')
        for url in proxy_list:
            key_name = url.split(':')[0]
            response = requests.get('http://' + url, timeout=5)
            if response.status_code == 200:
                proxy_dict[key_name] = True
            else:
                if url in str(e):
                    proxy_dict[key_name] = False
    return proxy_dict


if __name__ == '__main__':
    target_id, pg = DBUtil.get_pg_env()
    subtype, cluster_name, tenant_name, tenantType, host, port, conn_type = DBUtil.get_ob_basic()
    metric = []
    flag = True
    if conn_type == 'obproxy':
        if subtype == 'cluster':
            proxy_dict = check_obproxy_aviable(pg, target_id)
        else:
            cluster_target_id = DBUtil.get_cluster_target_id(pg, target_id)
            proxy_dict = check_obproxy_aviable(pg, cluster_target_id)
        if proxy_dict:
            proxy_failed_cnt = 0
            sample_cnt = 0
            for proxy_ip, state in proxy_dict.items():
                sample_cnt += 1
                if state:
                    metric.append(dict(index_id="2811020", value=[dict(name=proxy_ip, value='连接成功')]))
                else:
                    metric.append(dict(index_id="2811020", value=[dict(name=proxy_ip, value='连接失败')]))
                    proxy_failed_cnt += 1
                if proxy_ip == host:
                    if state:
                        flag = True
                    else:
                        flag = False
            failed_ratio = round(proxy_failed_cnt/sample_cnt * 100)
            metric.append(dict(index_id="2811021", value=cs(failed_ratio)))
        else:
            flag = True
    else:
        flag = True

    if flag:
        t_begin = time.time()
        ob, subtype, tenant_name, tenant_type, cluster_name = DBUtil.get_ob_env()
        t_connect_end = time.time()
        connect_elapsed = round((t_connect_end - t_begin) * 1000, 2)
        global version
        if tenant_type == "oracle":
            sql = '''select distinct value from ALL_VIRTUAL_SYS_PARAMETER_STAT_AGENT where name='min_observer_version' '''
        else:
            sql = '''select distinct value from __all_virtual_tenant_parameter_stat where name='min_observer_version' '''
        cs1 = DBUtil.getValue(ob, sql)
        version = cs1.fetchone()[0]
        try:
            if ob:
                get_sql_retry_cnt(ob, subtype, tenant_type, metric)
                if subtype == 'cluster':
                    import obproxy_metric
                    ob_metric_cluster(ob, metric)
                    ob_disk_size_metric_cluster(ob, metric, target_id, pg)
                    ob_session_metric(ob, metric, target_id, tenant_type, subtype)
                    ob_locks(ob, metric, target_id, pg)
                    transaction_metric(ob, metric, target_id, pg)
                    ob_system_memory_info(ob, metric)
                    obproxy_metric.get_obproxy_info(ob, pg, target_id, metric, host)
                else:
                    ob_metric_tenant(ob, metric)
                    if version > '4.0':
                        ob_disk_size_metric_tenant(ob, metric, target_id, pg, tenant_type)
                    ob_session_metric(ob, metric, target_id, tenant_type, subtype)
                    ob_event_metric(ob, metric, target_id, tenant_type)
                    ob_locks(ob, metric, target_id, pg)
                    cluster_id, cluster_name, tenant_id = get_cluster_info(ob, tenant_type, pg, target_id)
                    if cluster_id:
                        cluster_target_id = DBUtil.get_cluster_target_id(pg, target_id)
                        time.sleep(2)
                        transaction_metric_tenant(metric, pg, cluster_target_id, tenant_id)
                        tenant_memory_info(metric, pg, cluster_target_id, tenant_id)
                        if version < '4.0':
                            ob_tenant_size_metric_tenant(metric, pg, cluster_target_id, tenant_id)
                            if tenant_type == 'mysql':
                                ob_session_metric_3_mysql(metric, pg, cluster_target_id, tenant_name)
                    ob_memstore_info(ob, metric, tenant_type)
                metric.append(dict(index_id="2810000", value="连接成功"))
            else:
                metric.append(dict(index_id="2810000", value="连接失败"))
            t_collector_end = time.time()
            collector_elapsed = round((t_collector_end - t_begin) * 1000, 2)
            metric.append(dict(index_id="1000101", value=cs(collector_elapsed)))
            metric.append(dict(index_id="1000102", value=cs(connect_elapsed)))
            print('{"results":' + json.dumps(metric) + '}')
        except Exception as e:
            errorInfo = str(e)
            raise Exception(errorInfo)
    else:
        metric.append(dict(index_id="2810000", value="连接失败"))
        metric.append(dict(index_id="1000101", value=cs(0)))
        metric.append(dict(index_id="1000102", value=cs(0)))
        print('{"results":' + json.dumps(metric) + '}')

# Author	= xxxx


import json
import sys
from datetime import datetime

sys.path.append('/usr/software/knowl')

import DBUtil
import warnings
warnings.filterwarnings("ignore")
global pid

process_type = 'mongod'


def mongo_serverstatus(mongo, metric):
    global pid
    global process_type
    # 数据库服务端信息
    sql = 'serverStatus'
    result = mongo.noitemdict_value(sql)
    out = result.msg
    out_list = dict(out)
    # 连接数
    connections = out_list.get('connections')
    current = connections.get('current')
    available = connections.get('available')
    totalCreated = connections.get('totalCreated')
    process_type = out_list.get('process')
    if 'active' not in connections.keys():
        active = current
    else:
        active = connections['active']  # 4.0.7开始引入
    metric.append(dict(index_id=2101001, value=available))
    metric.append(dict(index_id=2101002, value=totalCreated))
    metric.append(dict(index_id=2101003, value=current))
    metric.append(dict(index_id=2101004, value=active))
    # MMAPv1引擎相关信息
    if 'backgroundFlushing' in out_list.keys():
        flushes = out_list['backgroundFlushing'].get('flushes')
        total_ms = out_list['backgroundFlushing'].get('total_ms')
        metric.append(dict(index_id=2101005, value=flushes))
        metric.append(dict(index_id=2102001, value=total_ms))
    if 'dur' in out_list.keys():
        # 负载指标
        commits = out_list['dur'].get('commits')
        journaledMB = out_list['dur'].get('journaledMB')
        writeToDataFilesMB = out_list['dur'].get('writeToDataFilesMB')
        commitsInWriteLock = out_list['dur'].get('commitsInWriteLock')
        metric.append(dict(index_id=2101007, value=commits))
        metric.append(dict(index_id=2101008, value=journaledMB))
        metric.append(dict(index_id=2101009, value=writeToDataFilesMB))
        metric.append(dict(index_id=2101010, value=commitsInWriteLock))
        # 性能指标
        writeToJournalMs = out_list['dur'].get('timeMs').get('writeToJournal')
        writeToDataFilesMs = out_list['dur'].get('timeMs').get('writeToDataFiles')
        metric.append(dict(index_id=2102002, value=writeToJournalMs))
        metric.append(dict(index_id=2102003, value=writeToDataFilesMs))

    # 网络
    if 'network' in out_list.keys():
        bytesIn = out_list['network'].get('bytesIn')
        bytesOut = out_list['network'].get('bytesOut')
        metric.append(dict(index_id=2101011, value=bytesIn))
        metric.append(dict(index_id=2101012, value=bytesOut))
    # dml 操作记录
    if 'opcounters' in out_list.keys():
        insert = out_list['opcounters'].get('insert')
        query = out_list['opcounters'].get('query')
        update = out_list['opcounters'].get('update')
        delete = out_list['opcounters'].get('delete')
        getmore = out_list['opcounters'].get('getmore')
        command = out_list['opcounters'].get('command')
        metric.append(dict(index_id=2101013, value=insert))
        metric.append(dict(index_id=2101014, value=query))
        metric.append(dict(index_id=2101015, value=update))
        metric.append(dict(index_id=2101016, value=delete))
        metric.append(dict(index_id=2101017, value=getmore))
        metric.append(dict(index_id=2101018, value=command))
    # metric
    metric_list = out_list['metrics']
    # 执行失败命令数
    if 'commands' in metric_list.keys():
        commands = metric_list['commands']
        failed_commands = 0
        for key in commands.keys():
            if key != '<UNKNOWN>':
                if 'failed' in commands[f'{key}'].keys():
                    fails = commands[f'{key}'].get('failed')
                    failed_commands = failed_commands + float(fails)
        metric.append(dict(index_id=2101019, value=failed_commands))
    # 游标
    if 'cursor' in metric_list.keys():
        cursortimedout = metric_list['cursor'].get('timedOut')
        cursornotimeout = metric_list['cursor'].get('open').get('noTimeout')
        cursorpinned = metric_list['cursor'].get('open').get('pinned')
        cursortotal = metric_list['cursor'].get('open').get('total')
        metric.append(dict(index_id=2101028, value=cursortimedout))
        metric.append(dict(index_id=2101025, value=cursornotimeout))
        metric.append(dict(index_id=2101026, value=cursorpinned))
        metric.append(dict(index_id=2101027, value=cursortotal))
    # document
    if 'document' in metric_list.keys():
        docdeleted = metric_list['document'].get('deleted')
        docinserted = metric_list['document'].get('inserted')
        docreturned = metric_list['document'].get('returned')
        docupdated = metric_list['document'].get('updated')
        metric.append(dict(index_id=2101029, value=docdeleted))
        metric.append(dict(index_id=2101030, value=docinserted))
        metric.append(dict(index_id=2101031, value=docreturned))
        metric.append(dict(index_id=2101032, value=docupdated))
    # operation
    if 'operation' in metric_list.keys():
        scanAndOrder = metric_list['operation'].get('scanAndOrder')
        metric.append(dict(index_id=2101033, value=scanAndOrder))
    # queryExecutor
    if 'queryExecutor' in metric_list.keys():
        scanned = metric_list['queryExecutor'].get('scanned')
        scannedObjects = metric_list['queryExecutor'].get('scannedObjects')
        metric.append(dict(index_id=2101034, value=scanned))
        metric.append(dict(index_id=2101035, value=scannedObjects))
    # record
    if 'record' in metric_list.keys():
        recordmoves = metric_list['record'].get('moves')
        metric.append(dict(index_id=2101036, value=recordmoves))
    # 多副本相关统计信息
    if 'repl' in metric_list.keys():
        repls = metric_list['repl']
        if repls:
            if 'apply' in repls.keys():
                applyops = repls['apply'].get('ops')
                metric.append(dict(index_id=2107025, value=applyops))
            if 'buffer' in repls.keys():
                buffer_count = repls.get('buffer').get('count')
                buffer_maxSizeBytes = repls.get('buffer').get('maxSizeBytes')
                buffer_sizeBytes = repls.get('buffer').get('sizeBytes')
                metric.append(dict(index_id=2107026, value=buffer_count))
                metric.append(dict(index_id=2107028, value=buffer_sizeBytes))
            if 'network' in repls.keys() and not process_type:
                network_bytes = repls.get('network').get('bytes')
                network_getmores = repls.get('network').get('getmores').get('num')
                network_ops = repls.get('network').get('ops')
                metric.append(dict(index_id=2107029, value=network_bytes))
                metric.append(dict(index_id=2107030, value=network_getmores))
                metric.append(dict(index_id=2107031, value=network_ops))

    # wiredTiger 引擎指标信息
    if 'wiredTiger' in out_list.keys():
        wiredTiger = out_list['wiredTiger']
        # 缓存
        if 'cache' in wiredTiger.keys():
            cache_info = wiredTiger['cache']
            max_cache = cache_info.get('maximum bytes configured')
            use_cache = cache_info.get('bytes currently in the cache')
            if 'bytes dirty in the cache cumulative' in cache_info.keys():
                total_dirty_data = cache_info['bytes dirty in the cache cumulative']
                metric.append(dict(index_id=2101039, value=total_dirty_data))
            cur_dirty_data = cache_info.get('tracked dirty bytes in the cache')
            read_bytes = cache_info.get('bytes read into cache')
            write_bytes = cache_info.get('bytes written from cache')
            evict_page_from_cache = cache_info.get('eviction server evicting pages')
            if 'application threads page read from disk to cache count' in cache_info.keys():
                read_to_cache = cache_info['application threads page read from disk to cache count']
                metric.append(dict(index_id=2101042, value=read_to_cache))
                cache_to_disk = cache_info['application threads page write from cache to disk count']
                metric.append(dict(index_id=2101043, value=cache_to_disk))
            used_cache_per = round(float(use_cache) * 100 / float(max_cache), 2)
            metric.append(dict(index_id=2101021, value=used_cache_per))
            metric.append(dict(index_id=2101037, value=max_cache))
            metric.append(dict(index_id=2101038, value=use_cache))
            metric.append(dict(index_id=2101171, value=cur_dirty_data))
            metric.append(dict(index_id=2101040, value=read_bytes))
            metric.append(dict(index_id=2101041, value=write_bytes))
            metric.append(dict(index_id=2101176, value=evict_page_from_cache))
        # 连接
        if 'connection' in wiredTiger.keys():
            read_ios = wiredTiger['connection'].get('total read I/Os')
            write_ios = wiredTiger['connection'].get('total write I/Os')
            open_files = wiredTiger['connection'].get('files currently open')
            use_mem = wiredTiger['connection'].get('memory allocations')
            free_mem = wiredTiger['connection'].get('memory frees')
            reuse_mem = wiredTiger['connection'].get('memory re-allocations')
            metric.append(dict(index_id=2101044, value=read_ios))
            metric.append(dict(index_id=2101045, value=write_ios))
            metric.append(dict(index_id=2101046, value=open_files))
            metric.append(dict(index_id=2101047, value=use_mem))
            metric.append(dict(index_id=2101048, value=free_mem))
            metric.append(dict(index_id=2101049, value=reuse_mem))
        # 块 管理
        if 'block-manager' in wiredTiger.keys():
            read_block = wiredTiger['block-manager'].get('blocks read')
            write_block = wiredTiger['block-manager'].get('blocks written')
            read_byte = wiredTiger['block-manager'].get('bytes read')
            write_byte = wiredTiger['block-manager'].get('bytes written')
            metric.append(dict(index_id=2101050, value=read_block))
            metric.append(dict(index_id=2101051, value=write_block))
            metric.append(dict(index_id=2101052, value=read_byte))
            metric.append(dict(index_id=2101053, value=write_byte))
        # capacity
        if 'capacity' in wiredTiger.keys():
            if 'bytes written for checkpoint' in wiredTiger['capacity'].keys():
                checkpoint_write_byte = wiredTiger['capacity']['bytes written for checkpoint']
                metric.append(dict(index_id=2101054, value=checkpoint_write_byte))
            if 'bytes written for eviction' in wiredTiger['capacity'].keys():
                evcit_write_byte = wiredTiger['capacity']['bytes written for eviction']
                metric.append(dict(index_id=2101055, value=evcit_write_byte))
            if 'bytes written for log' in wiredTiger['capacity'].keys():
                log_write_byte = wiredTiger['capacity']['bytes written for log']
                metric.append(dict(index_id=2101056, value=log_write_byte))
        # 游标
        if 'cached cursor count' in wiredTiger.get('cursor').keys():
            cache_cursors = wiredTiger['cursor']['cached cursor count']
            reuse_cursors = wiredTiger['cursor']['cursors reused from cache']
            open_cursors = wiredTiger['cursor']['open cursor count']
            metric.append(dict(index_id=2101057, value=cache_cursors))
            metric.append(dict(index_id=2101058, value=reuse_cursors))
            metric.append(dict(index_id=2101059, value=open_cursors))
        # 锁

        # 日志
        if 'log' in wiredTiger.keys():
            wlog = wiredTiger['log']
            log_write = wlog.get('log bytes written')
            log_flushes = wlog.get('log flush operations')
            log_scans = wlog.get('log scan operations')
            log_syncs = wlog.get('log sync operations')
            log_sync_time = wlog.get('log sync time duration (usecs)')
            log_process_recored = wlog.get('records processed by log scan')
            log_writes = wlog.get('log write operations')
            log_buffer = wlog.get('total log buffer size')
            metric.append(dict(index_id=2101060, value=log_write))
            metric.append(dict(index_id=2101061, value=log_flushes))
            metric.append(dict(index_id=2101062, value=log_scans))
            metric.append(dict(index_id=2101063, value=log_syncs))
            metric.append(dict(index_id=2101065, value=log_writes))
            metric.append(dict(index_id=2101067, value=log_buffer))
            metric.append(dict(index_id=2101066, value=log_process_recored))
            metric.append(dict(index_id=2101064, value=log_sync_time))
        # 性能 perf
        if 'perf' in wiredTiger.keys():
            file_read_latency_1 = wiredTiger['perf'][
                'file system read latency histogram (bucket 1) - 10-49ms']
            file_read_latency_2 = wiredTiger['perf'][
                'file system read latency histogram (bucket 2) - 50-99ms']
            file_read_latency_3 = wiredTiger['perf'][
                'file system read latency histogram (bucket 3) - 100-249ms']
            file_read_latency_4 = wiredTiger['perf'][
                'file system read latency histogram (bucket 4) - 250-499ms']
            file_read_latency_5 = wiredTiger['perf'][
                'file system read latency histogram (bucket 5) - 500-999ms']
            file_read_latency_6 = wiredTiger['perf'][
                'file system read latency histogram (bucket 6) - 1000ms+']
            file_write_latency_1 = wiredTiger['perf'][
                'file system write latency histogram (bucket 1) - 10-49ms']
            file_write_latency_2 = wiredTiger['perf'][
                'file system write latency histogram (bucket 2) - 50-99ms']
            file_write_latency_3 = wiredTiger['perf'][
                'file system write latency histogram (bucket 3) - 100-249ms']
            file_write_latency_4 = wiredTiger['perf'][
                'file system write latency histogram (bucket 4) - 250-499ms']
            file_write_latency_5 = wiredTiger['perf'][
                'file system write latency histogram (bucket 5) - 500-999ms']
            file_write_latency_6 = wiredTiger['perf'][
                'file system write latency histogram (bucket 6) - 1000ms+']
            metric.append(dict(index_id=2101068, value=file_read_latency_1))
            metric.append(dict(index_id=2101069, value=file_read_latency_2))
            metric.append(dict(index_id=2101070, value=file_read_latency_3))
            metric.append(dict(index_id=2101071, value=file_read_latency_4))
            metric.append(dict(index_id=2101072, value=file_read_latency_5))
            metric.append(dict(index_id=2101073, value=file_read_latency_6))
            metric.append(dict(index_id=2101074, value=file_write_latency_1))
            metric.append(dict(index_id=2101075, value=file_write_latency_2))
            metric.append(dict(index_id=2101076, value=file_write_latency_3))
            metric.append(dict(index_id=2101077, value=file_write_latency_4))
            metric.append(dict(index_id=2101078, value=file_write_latency_5))
            metric.append(dict(index_id=2101079, value=file_write_latency_6))
        # 会话
        open_session = wiredTiger.get('session').get('open session count')
        metric.append(dict(index_id=2101080, value=open_session))
        # 事务
        commit_trans = wiredTiger.get('transaction').get('transactions committed')
        rollback_trans = wiredTiger.get('transaction').get('transactions rolled back')
        metric.append(dict(index_id=2101081, value=commit_trans))
        metric.append(dict(index_id=2101082, value=rollback_trans))
        if 'update conflicts' in wiredTiger.get('transaction').keys():
            update_confi = wiredTiger['transaction']['update conflicts']
            metric.append(dict(index_id=2101083, value=update_confi))
        if 'concurrentTransactions' in wiredTiger.keys():
            wcontran = wiredTiger['concurrentTransactions']
            active_write_tickets = wcontran.get('write')['out']
            avai_write_tickets = wcontran.get('write')['available']
            active_read_tickets = wcontran.get('read')['out']
            avai_read_tickets = wcontran.get('read')['available']
            metric.append(dict(index_id=2102028, value=active_write_tickets))
            metric.append(dict(index_id=2102029, value=avai_write_tickets))
            metric.append(dict(index_id=2102030, value=active_read_tickets))
            metric.append(dict(index_id=2102031, value=avai_read_tickets))
        if 'thread-yield' in wiredTiger.keys():
            wthdy = wiredTiger['thread-yield']
            page_busy_block = wthdy.get('page acquire busy blocked')
            page_evict_block = wthdy.get('page acquire eviction blocked')
            page_lock_block = wthdy.get('page acquire locked blocked')
            page_read_block = wthdy.get('page acquire read blocked')
            page_sleep_time = wthdy.get('page acquire time sleeping (usecs)')
            metric.append(dict(index_id=2102032, value=page_sleep_time))
            metric.append(dict(index_id=2102057, value=page_busy_block))
            metric.append(dict(index_id=2102058, value=page_evict_block))
            metric.append(dict(index_id=2102059, value=page_lock_block))
            metric.append(dict(index_id=2102060, value=page_read_block))

        # snapshot-window-settings
        if 'snapshot-window-settings' in wiredTiger.get('transaction').keys():
            cache_pressure_per = wiredTiger['transaction']['snapshot-window-settings'].get('current cache pressure percentage')
            metric.append(dict(index_id=2101086, value=cache_pressure_per))
        if 'application threads page read from disk to cache time (usecs)' in wiredTiger.get('cache').keys():
            read_to_cache_time = cache_info.get('application threads page read from disk to cache time (usecs)')
            cache_to_disk_time = cache_info.get('application threads page write from cache to disk time (usecs)')
            metric.append(dict(index_id=2102026, value=read_to_cache_time))
            metric.append(dict(index_id=2102027, value=cache_to_disk_time))

    # 全局事务  3.6.3+ and on mongos in 4.2+
    # 以下指标 4.0.2+ and mongos in 4.2.1+
    if 'transactions' in out_list.keys():
        trans_list = out_list['transactions']
        currentActive = trans_list.get('currentActive')
        currentInactive = trans_list.get('currentInactive')
        currentOpen = trans_list.get('currentOpen')
        totalAborted = trans_list.get('totalAborted')
        totalCommitted = trans_list.get('totalCommitted')
        totalStarted = trans_list.get('totalStarted')
        metric.append(dict(index_id=2101157, value=currentActive))
        metric.append(dict(index_id=2101158, value=currentInactive))
        metric.append(dict(index_id=2101159, value=currentOpen))
        metric.append(dict(index_id=2101160, value=totalAborted))
        metric.append(dict(index_id=2101161, value=totalCommitted))
        metric.append(dict(index_id=2101162, value=totalStarted))
    # 内存使用情况
    if 'mem' in out_list.keys():
        mem_dict = out_list.get('mem')
        resident = mem_dict.get('resident')
        virtual = mem_dict.get('virtual')
        mapped = mem_dict.get('mapped')
        metric.append(dict(index_id=2101166, value=resident))
        metric.append(dict(index_id=2101167, value=virtual))
        metric.append(dict(index_id=2101168, value=mapped))
    # 补充信息 extra_info
    page_faults = out_list.get('extra_info').get('page_faults')
    metric.append(dict(index_id=2101169, value=page_faults))
    # 全局锁
    if 'globalLock' in out_list.keys():
        globalLock = out_list['globalLock']
        # globallock_totalTime = str(round(float(globalLock.get('totalTime'))/1000,2))
        globallock_queue_total = globalLock.get('currentQueue')['total']
        globallock_queue_read = globalLock.get('currentQueue')['readers']
        globallock_queue_write = globalLock.get('currentQueue')['writers']
        globallock_active_total = globalLock.get('activeClients')['total']
        globallock_active_read = globalLock.get('activeClients')['readers']
        globallock_active_write = globalLock.get('activeClients')['writers']
        metric.append(dict(index_id=2102004, value=globallock_queue_total))
        metric.append(dict(index_id=2102005, value=globallock_queue_read))
        metric.append(dict(index_id=2102006, value=globallock_queue_write))
        metric.append(dict(index_id=2102007, value=globallock_active_total))
        metric.append(dict(index_id=2102008, value=globallock_active_read))
        metric.append(dict(index_id=2102009, value=globallock_active_write))
        # metric.append(dict(index_id=2102010, value=globallock_totalTime))
    # 锁
    if 'locks' in out_list.keys():
        locks_list = out_list['locks']
        if 'acquireCount' in locks_list.get('Global').keys():
            if 'R' in locks_list['Global']['acquireCount'].keys():
                global_wait_Slocks = locks_list['Global']['acquireCount']['R']
            else:
                global_wait_Slocks = 0
            if 'W' in locks_list['Global']['acquireCount'].keys():
                global_wait_Xlocks = locks_list['Global']['acquireCount']['W']
            else:
                global_wait_Xlocks = 0
        else:
            global_wait_Slocks = 0
            global_wait_Xlocks = 0
        if 'timeAcquiringMicros' in locks_list['Global'].keys():
            if 'R' in locks_list['Global']['timeAcquiringMicros'].keys():
                global_Slocks_waittime = locks_list['Global']['timeAcquiringMicros']['R']
            else:
                global_Slocks_waittime = 0
            if 'W' in locks_list['Global']['timeAcquiringMicros'].keys():
                global_Xlocks_waittime = locks_list['Global']['timeAcquiringMicros']['W']
            else:
                global_Xlocks_waittime = 0
        else:
            global_Slocks_waittime = 0
            global_Xlocks_waittime = 0
        if 'acquireCount' in locks_list['Database'].keys():
            if 'R' in locks_list['Database']['acquireCount'].keys():
                database_wait_Slocks = locks_list['Database']['acquireCount']['R']
            else:
                database_wait_Slocks = 0
            if 'W' in locks_list['Database']['acquireCount'].keys():
                database_wait_Xlocks = locks_list['Database']['acquireCount']['W']
            else:
                database_wait_Xlocks = 0
        else:
            database_wait_Slocks = 0
            database_wait_Xlocks = 0
        if 'timeAcquiringMicros' in locks_list['Database'].keys():
            if 'R' in locks_list['Database']['timeAcquiringMicros'].keys():
                database_Slocks_waittime = locks_list['Database']['timeAcquiringMicros']['R']
            else:
                database_Slocks_waittime = 0
            if 'W' in locks_list['Database']['timeAcquiringMicros'].keys():
                database_Xlocks_waittime = locks_list['Database']['timeAcquiringMicros']['W']
            else:
                database_Xlocks_waittime = 0
        else:
            database_Slocks_waittime = 0
            database_Xlocks_waittime = 0
        if 'acquireCount' in locks_list['Collection'].keys():
            if 'R' in locks_list['Collection']['acquireCount'].keys():
                Collection_wait_Slocks = locks_list['Collection']['acquireCount']['R']
            else:
                Collection_wait_Slocks = 0
            if 'W' in locks_list['Collection']['acquireCount'].keys():
                Collection_wait_Xlocks = locks_list['Collection']['acquireCount']['W']
            else:
                Collection_wait_Xlocks = 0
        else:
            Collection_wait_Slocks = 0
            Collection_wait_Xlocks = 0
        if 'timeAcquiringMicros' in locks_list['Collection'].keys():
            if 'R' in locks_list['Collection']['timeAcquiringMicros'].keys():
                Collection_Slocks_waittime = locks_list['Collection']['timeAcquiringMicros']['R']
            else:
                Collection_Slocks_waittime = 0
            if 'W' in locks_list['Collection']['timeAcquiringMicros'].keys():
                Collection_Xlocks_waittime = locks_list['Collection']['timeAcquiringMicros']['W']
            else:
                Collection_Xlocks_waittime = 0
        else:
            Collection_Slocks_waittime = 0
            Collection_Xlocks_waittime = 0
        metric.append(dict(index_id=2102011, value=global_wait_Slocks))
        metric.append(dict(index_id=2102012, value=global_wait_Xlocks))
        metric.append(dict(index_id=2102013, value=global_Slocks_waittime))
        metric.append(dict(index_id=2102014, value=global_Xlocks_waittime))
        metric.append(dict(index_id=2102015, value=database_wait_Slocks))
        metric.append(dict(index_id=2102016, value=database_wait_Xlocks))
        metric.append(dict(index_id=2102017, value=database_Slocks_waittime))
        metric.append(dict(index_id=2102018, value=database_Xlocks_waittime))
        metric.append(dict(index_id=2102019, value=Collection_wait_Slocks))
        metric.append(dict(index_id=2102020, value=Collection_wait_Xlocks))
        metric.append(dict(index_id=2102021, value=Collection_Slocks_waittime))
        metric.append(dict(index_id=2102022, value=Collection_Xlocks_waittime))

    # metric.append(dict(index_id=2102023, value=Collection_wait_Slocks))
    # metric.append(dict(index_id=2102024, value=Collection_wait_Xlocks))
    # metric.append(dict(index_id=2102025, value=Collection_Slocks_waittime))
    # metric.append(dict(index_id=2102049, value=Collection_Xlocks_waittime))
    # 总体
    sql = 'serverStatus'
    result = mongo.noitemdict_value(sql)
    out = result.msg
    out_list = dict(out)
    pid = out_list.get('pid')
    uptime = out_list.get('uptime')
    metric.append(dict(index_id=2106001, value=uptime))
    metric.append(dict(index_id=2106002, value=pid))
    if 'opcountersRepl' in out_list.keys():
        replop_dict = out_list['opcountersRepl']
        repl_insert = replop_dict.get('insert')
        repl_query = replop_dict.get('query')
        repl_update = replop_dict.get('update')
        repl_delete = replop_dict.get('delete')
        repl_getmore = replop_dict.get('getmore')
        repl_command = replop_dict.get('command')
        metric.append(dict(index_id=2107008, value=repl_insert))
        metric.append(dict(index_id=2107009, value=repl_query))
        metric.append(dict(index_id=2107010, value=repl_update))
        metric.append(dict(index_id=2107011, value=repl_delete))
        metric.append(dict(index_id=2107012, value=repl_getmore))
        metric.append(dict(index_id=2107013, value=repl_command))
    # 多副本指标
    rep_stat = mongo.serverStatus_nodict('replSetGetStatus', 'myState')  # 获取副本集状态，0：STARTUP，1：PRIMARY，2：SECONDARY，3：RECOVERING，4：FATAL，5：STARTUP2，6：UNKNOWN，7：ARBITER，8：DOWN，9：ROLLBACK，10：REMOVED
    if rep_stat.code == 0:
        myState = rep_stat.msg
        wtime_num = metric_list['getLastError']['wtime']['num']
        wtime_totalMillis = metric_list['getLastError']['wtime']['totalMillis']
        wtimeouts = metric_list['getLastError']['wtimeouts']
        metric.append(dict(index_id=2107001, value=myState))
        metric.append(dict(index_id=2107002, value=wtime_num))
        metric.append(dict(index_id=2107003, value=wtime_totalMillis))
        metric.append(dict(index_id=2107004, value=wtimeouts))
        db_stats = mongo.noitemdict_value('replSetGetStatus')
        primary_optime = 0
        secondary_optime = []
        for key in db_stats.msg['members']:
            if key['stateStr'] == 'PRIMARY':
                primary_optime = key['optimeDate']
            if key['stateStr'] == 'SECONDARY':
                secondary_optime.append(key['optimeDate'])
        seconds_lag = []
        for sec in secondary_optime:
            lag = (primary_optime - sec).total_seconds()
            seconds_lag.append(lag)
        if seconds_lag:
            max_lag = max(seconds_lag)
            min_lag = min(seconds_lag)
            metric.append(dict(index_id=2107006, value=min_lag))
            metric.append(dict(index_id=2107007, value=max_lag))


def mongo_rep_delay(mongo, metric):
    """
    查看MongoDB 副本集配置  2101174
    :param mongo:
    :param row_dict:
    :return:
    """
    result = mongo.noitemdict_value('replSetGetConfig')
    if result.code == 0:
        member_list = dict(result.msg).get('config').get('members')
        vars = []
        for i in member_list:
            if 'slaveDelay' in i.keys():
                vars.append(i['slaveDelay'])
            else:
                vars.append(i['secondaryDelaySecs'])
        if vars:
            metric.append(dict(index_id=2101174, value=str(max(vars))))


def server_main(dbinfo, metric):
    """
    获取MongoDB metric总函数
    =param mssql=
    =return=
    """
    mongo = DBUtil.get_mongo_env(dbinfo)
    mongo_serverstatus(mongo, metric)
    if process_type == 'mongod': # mongod支持副本集
        mongo_rep_delay(mongo, metric)


if __name__ == '__main__':
    dbInfo = eval(sys.argv[1])
    metric = []
    cur_time = datetime.now()
    mongo = DBUtil.get_mongo_env(dbInfo)
    metric.append(dict(index_id="1000102", value=str(round((datetime.now() - cur_time).microseconds/1000,0))))
    result = mongo.excute('serverStatus')
    if result.code == 0:
        metric.append(dict(index_id="2100000", value='连接成功'))
        server_main(dbInfo, metric)
    else:
        metric.append(dict(index_id="2100000", value='连接失败'))
    lat_time = datetime.now()
    diff_ms = (lat_time - cur_time).microseconds
    metric.append(dict(index_id="1000101", value=str(round(diff_ms/1000,0))))
    print('{"results":' + json.dumps(metric,ensure_ascii=False) + '}')

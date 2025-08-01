#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
sys.path.append('/usr/software/knowl')
import DBUtil
import CommUtil


def generateawr(conn, dbname, dbid, inst_number, snap_id_begin, snap_id_end):
    awr_path = f"http://{CommUtil.get_ip()}:18090/awr/"
    # awr_path = "/usr/software/awr/"
    awr_file_name = "awrrpt_" + dbname + "_" + str(inst_number) + "_" + str(snap_id_begin) + "_" + str(
        snap_id_end) + ".html"
    fp = open("/usr/software/report/awr/" + awr_file_name, 'w')
    sql = "select * from table(dbms_workload_repository.awr_report_html({0},{1},{2},{3})) \
".format(dbid, inst_number, snap_id_begin, snap_id_end)
    cursor = DBUtil.getValue(conn, sql)
    res = cursor.fetchall()
    for row in res:
        print(row[0], file=fp)
    fp.close()
    print("msg=" + awr_path + awr_file_name)


def determinesnapId(conn, db_id, inst_number, snap_id_begin, snap_id_end):
    sql = '''
select count(*) from dba_hist_snapshot b,dba_hist_snapshot e where b.dbid=e.dbid and e.instance_number=b.instance_number
and b.dbid={0} and b.instance_number={1} and b.snap_id={2} and e.snap_id={3} and b.startup_time=e.startup_time
'''.format(db_id, inst_number, snap_id_begin, snap_id_end)
    cursor = DBUtil.getValue(conn, sql)
    res = cursor.fetchone()
    return res[0]


def main():
    ora = DBUtil.get_ora_env()
    db_name, db_id, inst_id, begin_snap, end_snap = DBUtil.getawrinfo()
    flag = determinesnapId(ora, db_id, inst_id, begin_snap, end_snap)
    if flag == 0:
        print("msg=选择的两个SNAP之间发生过数据库重新启动,无法生成AWR报告,请重新选择SNAP")
    else:
        generateawr(ora, db_name, db_id, inst_id, begin_snap, end_snap)


if __name__ == "__main__":
    main()

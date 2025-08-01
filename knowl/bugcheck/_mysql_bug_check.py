import sys
sys.path.append('/usr/software/knowl')
import DBUtil
import pandas as pd
import json


def read_cve_xls():
    io = r'/usr/software/knowl/bugcheck/cve.xlsx'
    data = pd.read_excel(io, sheet_name='mysql')
    cve_dic = {'name': 'cveinfo', 'cvedetail': []}
    for index, row in data.iterrows():
        tmp_dict = {}
        tmp_dict['cve_name'] = row['cve_id']
        tmp_dict['db_version_affected'] = row['affected_db_version']
        tmp_dict['resolved_version'] = row['patch_list']
        tmp_dict['publish_date'] = row['publish_date']
        cve_dic['cvedetail'].append(tmp_dict)
    return cve_dic


def main_bug_check(pg,cve_dict):
    sql1 = '''select t2.appSystemName,t2.name,cib_value,ip from 
    (select name,cib_value,ip from p_oracle_cib p, mgt_system m where cib_name='version' and index_id=2210001 and 
    m.uid=p.target_id and m.systype=1 and type='2') t1 left join
    (select appSystemName,name from mgt_system mgt left join (select a.id as appSystemId, a.app_system_name  as appSystemName,b.id as groupId,b.db_name as groupName from group_application_system a
left join group_db b on a.db_id ~ ( ',' || b.id || ',' ) where a.use_flag=true and b.use_flag=true ) w on(mgt.groupdbid=w.groupId)) t2 on( t1.name=t2.name)
    '''
    cs1 = DBUtil.getValue(pg, sql1)
    rs1 = cs1.fetchall()
    bug_check_dict = {}
    affected_db_lst = []
    for row in rs1:
        tmp_dict = {}
        tmp_dict['appSystemName'] = row[0]
        tmp_dict['db_name'] = row[1]
        db_version = row[2].split('-')[0].strip()
        tmp_dict['version'] = db_version
        tmp_dict['ip'] = row[3]
        tmp_dict['cveinfo'] = []
        tmp_dict['patchinfo'] = set()
        for cveinfo in cve_dict['cvedetail']:
            resolve_db_info = cveinfo['resolved_version'].split(',')
            for db in resolve_db_info:
                db_affected = db.split('-')[0]
                db_resolved = db.split('-')[1]
                if 'and prior' in db_affected:
                    db_max = db_affected.split()[0].strip()
                    db_min = db_max.split('.')[0] + '.' + db_max.split('.')[1]
                    if db_min <= row[2] <= db_max:
                        tmp_dict['cveinfo'].append(cveinfo['cve_name'])
                        tmp_dict['patchinfo'].add(db_resolved)
                else:
                    db = db.strip()
                    if row[2].startswith(db):
                        tmp_dict['cveinfo'].append(cveinfo['cve_name'])
                        tmp_dict['patchinfo'].add(db_resolved)
        if tmp_dict['cveinfo']:
            tmp_dict['patchinfo'] = min(tmp_dict['patchinfo'])
            affected_db_lst.append(tmp_dict)
    bug_check_dict['db_bug_info'] = affected_db_lst
    return bug_check_dict


def bug_check_by_name(pg,cve_name, cve_dict):
    sql1 = '''select t2.appSystemName,t2.name,cib_value,ip from 
    (select name,cib_value,ip from p_oracle_cib p, mgt_system m where cib_name='version' and index_id=2210001 and 
    m.uid=p.target_id and m.systype=1 and type='2') t1 left join
    (select appSystemName,name from mgt_system mgt left join (select a.id as appSystemId, a.app_system_name  as appSystemName,b.id as groupId,b.db_name as groupName from group_application_system a
left join group_db b on a.db_id ~ ( ',' || b.id || ',' ) where a.use_flag=true and b.use_flag=true ) w on(mgt.groupdbid=w.groupId)) t2 on( t1.name=t2.name) '''
    cs1 = DBUtil.getValue(pg, sql1)
    rs1 = cs1.fetchall()
    bug_check_dict = {}
    affected_db_lst = []
    for row in rs1:
        tmp_dict = {}
        tmp_dict['appSystemName'] = row[0]
        tmp_dict['db_name'] = row[1]
        db_version = row[2].split('-')[0].strip()
        tmp_dict['version'] = db_version
        tmp_dict['ip'] = row[3]
        tmp_dict['cveinfo'] = []
        tmp_dict['patchinfo'] = set()
        for cveinfo in cve_dict['cvedetail']:
            if cveinfo['cve_name'] == cve_name:
                resolve_db_info = cveinfo['resolved_version'].split(',')
                for db in resolve_db_info:
                    db_affected = db.split('-')[0]
                    db_resolved = db.split('-')[1]
                    if 'and prior' in db_affected:
                        db_max = db_affected.split()[0].strip()
                        db_min = db_max.split('.')[0] + '.' + db_max.split('.')[1]
                        if db_min <= row[2] <= db_max:
                            tmp_dict['cveinfo'].append(cve_name)
                            tmp_dict['patchinfo'].add(db_resolved)
                    else:
                        db = db.strip()
                        if row[2].startswith(db):
                            tmp_dict['cveinfo'].append(cve_name)
                            tmp_dict['patchinfo'].add(db_resolved)
        if tmp_dict['cveinfo']:
            tmp_dict['patchinfo'] = min(tmp_dict['patchinfo'])
            affected_db_lst.append(tmp_dict)
    bug_check_dict['db_bug_info'] = affected_db_lst
    return bug_check_dict


def bug_check_by_date(pg,publish_date, cve_dict):
    sql1 = '''select t2.appSystemName,t2.name,cib_value,ip from 
    (select name,cib_value,ip from p_oracle_cib p, mgt_system m where cib_name='version' and index_id=2210001 and 
    m.uid=p.target_id and m.systype=1 and type='2') t1 left join
    (select appSystemName,name from mgt_system mgt left join (select a.id as appSystemId, a.app_system_name  as appSystemName,b.id as groupId,b.db_name as groupName from group_application_system a
left join group_db b on a.db_id ~ ( ',' || b.id || ',' ) where a.use_flag=true and b.use_flag=true ) w on(mgt.groupdbid=w.groupId)) t2 on( t1.name=t2.name) '''
    cs1 = DBUtil.getValue(pg, sql1)
    rs1 = cs1.fetchall()
    bug_check_dict = {}
    affected_db_lst = []
    for row in rs1:
        tmp_dict = {}
        tmp_dict['appSystemName'] = row[0]
        tmp_dict['db_name'] = row[1]
        db_version = row[2].split('-')[0].strip()
        tmp_dict['version'] = db_version
        tmp_dict['ip'] = row[3]
        tmp_dict['cveinfo'] = []
        tmp_dict['patchinfo'] = set()
        for cveinfo in cve_dict['cvedetail']:
            if cveinfo['publish_date'].strip() == publish_date.strip():
                resolve_db_info = cveinfo['resolved_version'].split(',')
                for db in resolve_db_info:
                    db_affected = db.split('-')[0]
                    db_resolved = db.split('-')[1]
                    if 'and prior' in db_affected:
                        db_max = db_affected.split()[0].strip()
                        db_min = db_max.split('.')[0] + '.' + db_max.split('.')[1]
                        if db_min <= row[2] <= db_max:
                            tmp_dict['cveinfo'].append(cveinfo['cve_name'])
                            tmp_dict['patchinfo'].add(db_resolved)
                    else:
                        db = db.strip()
                        if row[2].startswith(db):
                            tmp_dict['cveinfo'].append(cveinfo['cve_name'])
                            tmp_dict['patchinfo'].add(db_resolved)
        if tmp_dict['cveinfo']:
            tmp_dict['patchinfo'] = min(tmp_dict['patchinfo'])
            affected_db_lst.append(tmp_dict)
    bug_check_dict['db_bug_info'] = affected_db_lst
    return bug_check_dict


def main():
    dbinfo = json.loads(sys.argv[1])
    cve_name = dbinfo['cve_name']
    publish_date = dbinfo['publish_date']
    pg = DBUtil.get_pg_from_cfg()
    cve_dict = read_cve_xls()

    if not cve_name and not publish_date:
        bug_check_dict = main_bug_check(pg,cve_dict)
    elif cve_name and not publish_date:
        bug_check_dict = bug_check_by_name(pg,cve_name, cve_dict)
    elif publish_date and not cve_name:
        bug_check_dict = bug_check_by_date(pg,publish_date, cve_dict)
    print(json.dumps(bug_check_dict))

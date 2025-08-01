import sys
import json
import pandas as pd
sys.path.append('/usr/software/knowl')
import DBUtil


def read_cve_xls():
    io = r'/usr/software/knowl/bugcheck/cve.xlsx'
    data = pd.read_excel(io, sheet_name='oracle')
    columns_rename = {'CVE': 'cve_id',
                      'Supported Versions Affected': 'db_version_affected',
                      'Patch List': 'patch_list',
                      'publish date': 'publish_date'
                      }
    data.rename(columns=columns_rename, inplace=True)
    df = data.to_dict(orient='records')
    cve_dic = {'name': 'cveinfo', 'cvedetail': df}
    # for index, row in data.iterrows():
    #     tmp_dict = {}
    #     tmp_dict['cve_id'] = row['CVE']
    #     tmp_dict['db_version_affected'] = row['Supported Versions Affected']
    #     tmp_dict['patch_list'] = row['Patch List']
    #     tmp_dict['publish_date'] = row['publish date']
    #     cve_dic['cvedetail'].append(tmp_dict)
    return cve_dic


def store_cve(engine):
    io = r'/usr/software/knowl/bugcheck/cve.xlsx'
    data = pd.read_excel(io, sheet_name='oracle')
    try:
        data.to_sql('buginfo', engine, index=False, if_exists='replace')
    except Exception as e:
        print(e)

def main_bug_check(pg,cve_dict):
    sql1 = '''select t5.appSystemName, t1.name,t2.dbv,t1.psu,t3.platform_name,t4.rac,t1.ip from 
    (select name, cib_value psu, ip from p_oracle_cib p, mgt_system m where cib_name='psu' and index_id=2201000 and m.uid=p.target_id and m.systype=1 and type='1' and m.use_flag=true) t1  left join
	(select appSystemName,name from mgt_system mgt,(select a.id as appSystemId, a.app_system_name  as appSystemName,b.id as groupId,b.db_name as groupName from group_application_system a
left join group_db b on a.db_id ~ ( ',' || b.id || ',' ) where a.use_flag=true and b.use_flag=true ) w
where mgt.groupdbid=w.groupId) t5 on (t5.name= t1.name),
    (select name, cib_value dbv, ip from p_oracle_cib p, mgt_system m where cib_name='version' and index_id=2201000 and m.uid=p.target_id and m.systype=1 and type='1' and m.use_flag=true) t2,
	(select name, cib_value platform_name, ip from p_oracle_cib p, mgt_system m where cib_name='platform_name' and index_id=2201000 and m.uid=p.target_id and m.systype=1 and type='1' and m.use_flag=true) t3,
	(select name, cib_value as rac, ip from p_oracle_cib p, mgt_system m where cib_name='parallel' and index_id=2201001 and m.uid=p.target_id and m.systype=1 and type='1' and m.use_flag=true) t4
    where t1.name=t2.name and t1.ip = t2.ip and t1.name=t3.name and t1.ip= t3.ip and t1.ip=t4.ip and t1.name=t4.name '''
    cs1 = DBUtil.getValue(pg, sql1)
    rs1 = cs1.fetchall()
    bug_check_dict = {}
    affected_db_lst = []
    for row in rs1:
        tmp_dict = {}
        tmp_dict['appSystemName'] = row[0]
        tmp_dict['db_name'] = row[1]
        if not row[3]:
            db_version = row[2]
        else:
            if row[3].startswith('RDBMS'):
                tmpdbv = row[3].split('_')[1]
                db_version = tmpdbv.split('DB')[0]
            elif row[3].startswith('PSU'):
                db_version = row[3].split()[1]
            else:
                db_version = row[2]
        tmp_dict['version'] = db_version
        tmp_dict['ip'] = row[6]
        tmp_dict['cveinfo'] = []
        tmp_dict['patchinfo'] = set()
        for cveinfo in cve_dict['cvedetail']:
            db_patch_info = cveinfo['patch_list'].split(',')
            for db in db_patch_info:
                patch_info = db.split('-')
                if db.count('-') == 3:
                    dbv = patch_info[0]
                    platform = patch_info[1]
                    type = patch_info[2]
                    patch = patch_info[3]
                elif db.count('-') == 2:
                    dbv = patch_info[0]
                    platform = patch_info[1]
                    patch = patch_info[2]
                if len(dbv.split('.')) == 4:
                    if db_version.startswith(dbv):
                        tmp_dict['cveinfo'].append(cveinfo['cve_id'])
                        tmp_dict['patchinfo'].add(patch)
                elif len(dbv.split('.')) == 3:
                    db_min = dbv.split('.')[0] + '.' + dbv.split('.')[1]
                    if db_min < db_version < dbv or db_version.startswith(dbv):
                        tmp_dict['cveinfo'].append(cveinfo['cve_id'])
                        tmp_dict['patchinfo'].add(patch)
        if tmp_dict['cveinfo']:
            tmp_dict['patchinfo'] = list(tmp_dict['patchinfo'])
            affected_db_lst.append(tmp_dict)
    bug_check_dict['db_bug_info'] = affected_db_lst
    return bug_check_dict


def bug_check_by_date(pg,publish_date, cve_dict):
    sql1 = '''select t5.appSystemName, t1.name,t2.dbv,t1.psu,t3.platform_name,t4.rac,t1.ip from 
    (select name, cib_value psu, ip from p_oracle_cib p, mgt_system m where cib_name='psu' and index_id=2201000 and m.uid=p.target_id and m.systype=1 and type='1' and m.use_flag=true) t1  left join
	(select appSystemName,name from mgt_system mgt,(select a.id as appSystemId, a.app_system_name  as appSystemName,b.id as groupId,b.db_name as groupName from group_application_system a
left join group_db b on a.db_id ~ ( ',' || b.id || ',' ) where a.use_flag=true and b.use_flag=true ) w
where mgt.groupdbid=w.groupId) t5 on (t5.name= t1.name),
    (select name, cib_value dbv, ip from p_oracle_cib p, mgt_system m where cib_name='version' and index_id=2201000 and m.uid=p.target_id and m.systype=1 and type='1' and m.use_flag=true) t2,
	(select name, cib_value platform_name, ip from p_oracle_cib p, mgt_system m where cib_name='platform_name' and index_id=2201000 and m.uid=p.target_id and m.systype=1 and type='1' and m.use_flag=true) t3,
	(select name, cib_value as rac, ip from p_oracle_cib p, mgt_system m where cib_name='parallel' and index_id=2201001 and m.uid=p.target_id and m.systype=1 and type='1' and m.use_flag=true) t4
    where t1.name=t2.name and t1.ip = t2.ip and t1.name=t3.name and t1.ip= t3.ip and t1.ip=t4.ip and t1.name=t4.name '''
    cs1 = DBUtil.getValue(pg, sql1)
    rs1 = cs1.fetchall()
    bug_check_dict = {}
    affected_db_lst = []
    for row in rs1:
        tmp_dict = {}
        tmp_dict['appSystemName'] = row[0]
        tmp_dict['db_name'] = row[1]
        if not row[3]:
            db_version = row[2]
        else:
            if row[3].startswith('RDBMS'):
                tmpdbv = row[3].split('_')[1]
                db_version = tmpdbv.split('DB')[0]
            elif row[3].startswith('PSU'):
                db_version = row[3].split()[1]
            else:
                db_version = row[2]
        tmp_dict['version'] = db_version
        tmp_dict['ip'] = row[6]
        tmp_dict['cveinfo'] = []
        tmp_dict['patchinfo'] = set()
        for cveinfo in cve_dict['cvedetail']:
            if cveinfo['publish_date'].strip() == publish_date.strip():
                db_patch_info = cveinfo['patch_list'].split(',')
                for db in db_patch_info:
                    dbv = db.split('-')[0]
                    patch = db.split('-')[3]
                    if len(dbv.split('.')) == 4:
                        if db_version.startswith(dbv):
                            tmp_dict['cveinfo'].append(cveinfo['cve_id'])
                            tmp_dict['patchinfo'].add(patch)
                    elif len(dbv.split('.')) == 3:
                        db_min = dbv.split('.')[0] + '.' + dbv.split('.')[1]
                        if db_min < db_version < dbv or db_version.startswith(dbv):
                            tmp_dict['cveinfo'].append(cveinfo['cve_id'])
                            tmp_dict['patchinfo'].add(patch)
        if tmp_dict['cveinfo']:
            tmp_dict['patchinfo'] = list(tmp_dict['patchinfo'])
            affected_db_lst.append(tmp_dict)
    bug_check_dict['db_bug_info'] = affected_db_lst
    return bug_check_dict


def bug_check_by_name(pg,cve_id, cve_dict):
    sql1 = '''select t5.appSystemName, t1.name,t2.dbv,t1.psu,t3.platform_name,t4.rac,t1.ip from 
    (select name, cib_value psu, ip from p_oracle_cib p, mgt_system m where cib_name='psu' and index_id=2201000 and m.uid=p.target_id and m.systype=1 and type='1' and m.use_flag=true) t1  left join
	(select appSystemName,name from mgt_system mgt,(select a.id as appSystemId, a.app_system_name  as appSystemName,b.id as groupId,b.db_name as groupName from group_application_system a
left join group_db b on a.db_id ~ ( ',' || b.id || ',' ) where a.use_flag=true and b.use_flag=true ) w
where mgt.groupdbid=w.groupId) t5 on (t5.name= t1.name),
    (select name, cib_value dbv, ip from p_oracle_cib p, mgt_system m where cib_name='version' and index_id=2201000 and m.uid=p.target_id and m.systype=1 and type='1' and m.use_flag=true) t2,
	(select name, cib_value platform_name, ip from p_oracle_cib p, mgt_system m where cib_name='platform_name' and index_id=2201000 and m.uid=p.target_id and m.systype=1 and type='1' and m.use_flag=true) t3,
	(select name, cib_value as rac, ip from p_oracle_cib p, mgt_system m where cib_name='parallel' and index_id=2201001 and m.uid=p.target_id and m.systype=1 and type='1' and m.use_flag=true) t4
    where t1.name=t2.name and t1.ip = t2.ip and t1.name=t3.name and t1.ip= t3.ip and t1.ip=t4.ip and t1.name=t4.name '''
    cs1 = DBUtil.getValue(pg, sql1)
    rs1 = cs1.fetchall()
    bug_check_dict = {}
    affected_db_lst = []
    for row in rs1:
        tmp_dict = {}
        tmp_dict['appSystemName'] = row[0]
        tmp_dict['db_name'] = row[1]
        db_version = 0
        if not row[3]:
            db_version = row[2]
        else:
            if row[3].startswith('RDBMS'):
                tmpdbv = row[3].split('_')[1]
                db_version = tmpdbv.split('DB')[0]
            elif row[3].startswith('PSU'):
                db_version = row[3].split()[1]
            else:
                db_version = row[2]
        tmp_dict['version'] = db_version
        tmp_dict['ip'] = row[6]
        tmp_dict['cveinfo'] = []
        tmp_dict['patchinfo'] = set()
        for cveinfo in cve_dict['cvedetail']:
            if cveinfo['cve_id'] == cve_id:
                db_patch_info = cveinfo['patch_list'].split(',')
                for db in db_patch_info:
                    dbv = db.split('-')[0]
                    patch = db.split('-')[3]
                    if len(dbv.split('.')) == 4:
                        if db_version.startswith(dbv):
                            tmp_dict['cveinfo'].append(cveinfo['cve_id'])
                            tmp_dict['patchinfo'].add(patch)
                    elif len(dbv.split('.')) == 3:
                        db_min = dbv.split('.')[0] + '.' + dbv.split('.')[1]
                        if db_min < db_version < dbv or db_version.startswith(dbv):
                            tmp_dict['cveinfo'].append(cveinfo['cve_id'])
                            tmp_dict['patchinfo'].add(patch)
        if tmp_dict['cveinfo']:
            tmp_dict['patchinfo'] = list(tmp_dict['patchinfo'])
            affected_db_lst.append(tmp_dict)
    bug_check_dict['db_bug_info'] = affected_db_lst
    return bug_check_dict

def main():
    dbinfo = json.loads(sys.argv[1])
    cve_name = dbinfo['cve_name']
    publish_date = dbinfo['publish_date']
    pg = DBUtil.get_pg_from_cfg()
    cve_dict = read_cve_xls()
#     sql = '''select appSystemName,name from mgt_system mgt,(select a.id as appSystemId, a.app_system_name  as appSystemName,b.id as groupId,b.db_name as groupName from group_application_system a
# left join group_db b on a.db_id ~ ( ',' || b.id || ',' ) where a.use_flag=true and b.use_flag=true )w
# where mgt.groupdbid=w.groupId'''
#     cs = DBUtil.getValue(pg, sql)
#     rs = cs.fetchall()
#     if rs:
    if not cve_name and not publish_date:
        bug_check_dict = main_bug_check(pg,cve_dict)
    elif cve_name and not publish_date:
        bug_check_dict = bug_check_by_name(pg,cve_name, cve_dict)
    elif publish_date and not cve_name:
        bug_check_dict = bug_check_by_date(pg,publish_date, cve_dict)
    print(json.dumps(bug_check_dict))
    # else:
    #     tipdict={"tipinfo": "组织架构未配置，无法正常使用该功能，请先到【系统管理->组织架构管理】菜单项配置组织架构。"}
    #     print(json.dumps(tipdict))

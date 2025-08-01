import sys
import pandas as pd

sys.path.append('/usr/software/knowl')
import DBUtil


def store_cve(pg):
    cve = r'/usr/software/knowl/bugcheck/cve.xlsx'
    data_oracle = pd.read_excel(cve, sheet_name='oracle')
    data_mysql = pd.read_excel(cve, sheet_name='mysql')
    rows_execl = data_oracle.shape[0] + data_mysql.shape[0]
    sql = 'select count(*) from buginfo'
    cursor = DBUtil.getValue(pg, sql)
    result = cursor.fetchone()[0]
    if rows_execl != result:
        insert_template = 'truncate table buginfo;INSERT INTO buginfo VALUES\n'
        # 处理CSV数据并生成SQL语句
        for index, row in data_oracle.iterrows():
            # 清除空值和NULL，并用空字符串替换
            cve_id = row['cve_id']
            cve_description = row['cve_description']
            cvss_score = row['cvss_score']
            affected_db_version = row['affected_db_version']
            patch_list = row['patch_list']
            publish_date = row['publish_date']
            insert_template += f"('{cve_id}', '{cve_description}', '{cvss_score}', '{affected_db_version}', '{patch_list}', '{publish_date}'),\n"
        for index, row in data_mysql.iterrows():
            # 清除空值和NULL，并用空字符串替换
            cve_id = row['cve_id']
            cve_description = row['cve_description']
            cvss_score = row['cvss_score']
            affected_db_version = row['affected_db_version']
            patch_list = row['patch_list']
            publish_date = row['publish_date']
            insert_template += f"('{cve_id}', '{cve_description}', {cvss_score}, '{affected_db_version}', '{patch_list}', '{publish_date}'),\n"
        sql = insert_template[:-2] + ';commit;'
        pg.execute(sql)


def oracle_report(pg,rs):
    sql2 = '''
    select name,dbv,psu,patches,ip  from 
    (select t.name,s.dbv,t.psu,t.ip, t.target_id from
        (select name, cib_value psu, ip, target_id from p_oracle_cib p, mgt_system m where cib_name='psu' and index_id=2201000 and m.uid=p.target_id and m.systype=1 and type='1') t,
        (select name, cib_value dbv, ip, target_id from p_oracle_cib p, mgt_system m where cib_name='version' and index_id=2201000 and m.uid=p.target_id and m.systype=1 and type='1') s
        where t.name=s.name and t.ip = s.ip) p,(select target_id,string_agg(target_id,',') patches from p_oracle_cib where index_id='2202012' and seq_id <> 0 group by target_id) m where p.target_id=m.target_id
    '''
    cs2 = DBUtil.getValue(pg, sql2)
    rs2 = cs2.fetchall()
    buginfo = {}
    buginfo['cve_id'] = rs[0]
    buginfo['cve_description'] = rs[1]
    buginfo['cvss_score'] = rs[2]
    buginfo['affect_db_version'] = rs[3]
    affected_db = []
    for row in rs2:
        tmp_dict = {}
        tmp_dict['db_name'] = row[0]
        db_version = 0
        if not row[2]:
            db_version = row[1]
        else:
            if row[2].startswith('RDBMS'):
                tmpdbv = row[2].split('_')[1]
                db_version = tmpdbv.split('DB')[0]
            elif row[2].startswith('PSU'):
                db_version = row[2].split()[1]
        tmp_dict['ip'] = row[4]
        tmp_dict['db_version'] = db_version
        tmp_dict['patch'] = ''
        for patchinfo in rs[4].split(','):
            affected_db_version = patchinfo.split('-')[0]
            patch = patchinfo.split('-')[1]
            if len(affected_db_version.split('.')) == 4:
                if db_version.startswith(affected_db_version):
                    patch_id = patch.split()[1]
                    if patch_id not in row[3]:
                        tmp_dict['patch'] = patch
            elif len(affected_db_version.split('.')) == 3:
                db_min = affected_db_version.split('.')[0] + '.' + affected_db_version.split('.')[1]
                if db_min < db_version < affected_db_version or db_version.startswith(affected_db_version):
                    patch_id = patch.split()[1]
                    if patch_id not in row[3]:
                        tmp_dict['patch'] = patch
        if tmp_dict['patch']:
            affected_db.append(tmp_dict)
    buginfo['affect_db'] = affected_db
    buginfo['publish_date'] = rs[5]
    return buginfo


def mysql_report(pg,rs):
    sql2 = '''select name,cib_value,ip from p_oracle_cib p, mgt_system m where cib_name='version' and index_id=2210001 and 
    m.uid=p.target_id and m.systype=1 and type='2' '''
    cs2 = DBUtil.getValue(pg, sql2)
    rs2 = cs2.fetchall()
    buginfo = {}
    buginfo['cve_id'] = rs[0]
    buginfo['cve_description'] = rs[1]
    buginfo['cvss_score'] = rs[2]
    buginfo['affect_db_version'] = rs[3]
    affected_db = []
    for row in rs2:
        tmp_dict = {}
        tmp_dict['db_name'] = row[0]
        db_version = row[1].split('-')[0].strip()
        tmp_dict['db_version'] = db_version
        tmp_dict['ip'] = row[2]
        tmp_dict['patch'] = ''
        for db in rs[4].split(','):
            db_affected = db.split('-')[0]
            db_resolved = db.split('-')[1]
            if 'and prior' in db_affected:
                db_max = db_affected.split()[0].strip()
                db_min = db_max.split('.')[0] + '.' + db_max.split('.')[1]
                if db_min <= row[1] <= db_max:
                    tmp_dict['patch'] = db_resolved
            else:
                db = db.strip()
                if row[1].startswith(db):
                    tmp_dict['patch'] = db_resolved
        if tmp_dict['patch']:
                affected_db.append(tmp_dict)
        buginfo['affect_db'] = affected_db
        buginfo['publish_date'] = rs[5]
        return buginfo


def generate_report(pg, cve_id):
    sql1 = '''select * from buginfo where cve_id='{0}' '''.format(cve_id)
    cs1 = DBUtil.getValue(pg, sql1)
    rs1 = cs1.fetchone()
    if rs1:
        type = rs1[6]
        if type == 'oracle':
            buginfo = oracle_report(pg,rs1)
        else:
            buginfo = mysql_report(pg,rs1)
        return buginfo
    else:
        buginfo = "CVE资料库中未发现查询的CVE_ID"
        return buginfo

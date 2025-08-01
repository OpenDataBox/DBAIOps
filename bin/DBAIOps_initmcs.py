#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import uuid
import socket
sys.path.append('/usr/software/knowl')
import DBUtil
import psycopg2
import ResultCode
import warnings
import traceback
from JavaRsa import decrypt
warnings.filterwarnings("ignore")

def getFileCont(file_name):
    f = open(file_name,'r',encoding='utf-8') 
    file_cont = f.read()
    f.close()
    return file_cont


class Postgre():
    def __init__(self, host, usr, pwd, port, dbname, exflag=1):
        try:
            self.conn = psycopg2.connect(database=dbname, user=usr, password=pwd, host=host, port=port)
            self.conn.set_client_encoding('utf-8')
            self.msg = None
        except psycopg2.OperationalError as e:
            if exflag == 1:
                print("msg=WORD_BEGIN" + str(e) + "WORD_END")
                sys.exit(1)
            else:
                self.conn = None
                self.msg = str(e)

    def execute(self, sql, bt=False):
        result = ResultCode.Result()
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            self.conn.commit()
            result.code = 0
            result.msg = cursor
        except psycopg2.ProgrammingError as e:
            self.conn.rollback()
            errorInfo = str(e)
            result.code = 1
            result.msg = errorInfo
            if bt:
                exstr = traceback.format_exc()
                print(exstr)
        except psycopg2.OperationalError as e:
            self.conn.rollback()
            errorInfo = str(e)
            result.code = 1
            result.msg = errorInfo
            if bt:
                exstr = traceback.format_exc()
                print(exstr)
        except psycopg2.Error as e:
            self.conn.rollback()
            errInfo = str(e)
            result.code = 1
            result.msg = errInfo
            if bt:
                exstr = traceback.format_exc()
                print(exstr)
        return result


if __name__ == '__main__':
    dbInfo = eval(sys.argv[1])
    ##pg info
    dbip = dbInfo['pg_ip']
    dbname = dbInfo['pg_dbname']
    username = dbInfo['pg_usr']
    usrnm = decrypt(username)
    password = dbInfo['pg_pwd']
    pgport = dbInfo['pg_port']
    passwd = decrypt(password)
    pg = Postgre(dbip, usrnm, passwd, pgport, dbname)

    try:

        fc = getFileCont("/tmp/init_mcs.sql")
        sqlf = """
begin;
delete from mon_comp_status;
""" + fc + """
end;"""
        pg.execute(sqlf)
        init_domain = getFileCont("/tmp/init_domain.txt").strip()
        sql1 = '''select id,management_nodes from public.collector_network_domain where name='顶级域' '''
        cs1 = DBUtil.getValue(pg, sql1)
        rs1 = cs1.fetchone()
        db_domain_lst = []
        if rs1:
            uuid_db = rs1[0]
            domain = rs1[1]
            db_domain_lst = domain.split(';')
        uuid_domain = uuid.uuid4()
        uuid_range = uuid.uuid4()
        init_domain_lst = init_domain.split(';')
        domain_lst = init_domain_lst
        final_domain_lst = list(set(domain_lst))
        domain_node = ';'.join(final_domain_lst)
        if rs1:
            sql_domain = '''
begin;
delete from public.collector_network_domain where name='顶级域' and id='{0}';
delete from public.collector_domain_mgt_node_range where domain_id='{0}';
insert into public.collector_network_domain(id,name,management_nodes,create_by,create_time,update_by,update_time,use_flag,init_flag) values('{1}','顶级域','{2}',null,now(),null,now(),'t','t');
insert into public.collector_domain_mgt_node_range(id,domain_id,start_ip,end_ip) values('{3}','{1}','0.0.0.0','0.0.0.0');
end;
'''.format(uuid_db,uuid_domain,domain_node,uuid_range)
        else:
            sql_domain = '''
begin;
insert into public.collector_network_domain(id,name,management_nodes,create_by,create_time,update_by,update_time,use_flag,init_flag) values('{0}','顶级域','{1}',null,now(),null,now(),'t','t');
insert into public.collector_domain_mgt_node_range(id,domain_id,start_ip,end_ip) values('{2}','{0}','0.0.0.0','0.0.0.0');
end;
'''.format(uuid_domain,domain_node,uuid_range)
        pg.execute(sql_domain)
        # 更新neo4j连接信息
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        sql = f"""
        UPDATE public.sys_param SET value='{{
        "graph_url": "bolt://{ip}:7687",
        "graph_name": "ihCPO+F2n6/WZgRaOn0IKTZjtzV6WUboswwGjFWnl/RLhNwXTGeMIe8TSRuaKorqtg7gSKO272Nl3fLcEdlmgPh7NRzX/UmKwwgu4UNv6F6ooX83Sg/evHv5zzrG5HIgLoXUUiahUoXrbd913h/VWzXKzFkuZTUmRyuHJGgK7Q4=",
        "graph_pd": "R9TGb4YKs/5TeTzN6VR9qYi4gn9lHvv2GbQrEPZNEXpzj81gg0SEMS/mJFNoMFAyJmx/dJl9iMly2bfJuYWL9QGKO6mF6150Pl/rHVNQqmqTSq9wcUfiKUeOVo4EPgWJzrGU5vHHrDoHDDrKRuZQBP9FrRlsxC5rMRbuGckPYcc=",
        "analysis_othername": "metric_kg_analyze",
        "analysis_metric": "neo4j_knowl_by_indexid"
        }}
        ' WHERE code='995';
        """
        pg.execute(sql)
    except psycopg2.DatabaseError as e:
        print("初始化数据库报错：" + str(e))
        if not pg is None:
            pg.close()

#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from neo4j import GraphDatabase
import pandas as pd

import sys
sys.path.append('/usr/software/knowl')
import DBUtil

# Neo4j 连接信息
uri = "bolt://192.168.32.98:7687"  # Neo4j 地址
user = "neo4j"                     # 用户名
password = "DBAIOps@DFC_2021"       # 密码

# 创建 Neo4j 驱动实例
driver = GraphDatabase.driver(uri, auth=(user, password))

def execute_query(driver, query, parameters=None):
    """执行 CQL 查询并返回结果"""
    with driver.session() as session:
        result = session.run(query, parameters)
        return result.data()

class Mcrypt:
    def __init__(self):
        secretkey = '6agrioBE1D9yoGOX4yyDMyMFs72jYvJ8'
        self.key = secretkey  # 密钥
        self.iv = secretkey[0:16]  # 偏移量
        self.BLOCK_SIZE = 32
        # 不足BLOCK_SIZE的补位(s可能是含中文，而中文字符utf-8编码占3个位置,gbk是2，所以需要以len(s.encode())，而不是len(s)计算补码)
        self.pad = lambda s: s + (self.BLOCK_SIZE - len(s.encode()) % self.BLOCK_SIZE) * chr(self.BLOCK_SIZE - len(s.encode()) % self.BLOCK_SIZE)
        # 去除补位
        self.unpad = lambda s: s[:-ord(s[len(s) - 1:])]

    def encrypt(self, text):
        """
        加密 ：先补位，再AES加密，后base64编码
        :param text: 需加密的明文
        :return:
        """
        from Crypto.Cipher import AES  
        from base64 import b64encode
        # text = pad(text) 包pycrypto的写法，加密函数可以接受str也可以接受bytess
        text = self.pad(text).encode()  # 包pycryptodome 的加密函数不接受str
        cipher = AES.new(key=self.key.encode(), mode=AES.MODE_CBC, IV=self.iv.encode())
        encrypted_text = cipher.encrypt(text)
        # 进行64位的编码,返回得到加密后的bytes，decode成字符串
        return b64encode(encrypted_text).decode('utf-8')

    def decrypt(self, encrypted_text):
        """
        解密 ：偏移量为key[0:16]；先base64解，再AES解密，后取消补位
        :param encrypted_text : 已经加密的密文
        :return:
        """
        from Crypto.Cipher import AES  
        from base64 import b64decode
        encrypted_text = b64decode(encrypted_text)
        cipher = AES.new(key=self.key.encode(), mode=AES.MODE_CBC, IV=self.iv.encode())
        decrypted_text = cipher.decrypt(encrypted_text)
        return self.unpad(decrypted_text).decode('utf-8')


pc = Mcrypt()

# 新增运维经验背景知识

def get_index_name(index_id):
    pg = DBUtil.get_pg_from_cfg()
    sql = "select description from mon_index mi where mi.index_id=%s" % index_id
    cs = DBUtil.getValue(pg, sql)
    index_name = cs.fetchone()[0]
    return index_name

def create_knowledge_from_excel(file_path):
    """从Excel文件创建运维经验背景知识（按列顺序读取数据）

    Args:
        file_path (str): Excel文件路径
    """
    # 读取Excel文件的前三个工作区
    data = pd.read_excel(file_path)

    for _, row in data.iterrows():
        # 按列顺序获取数据，并过滤空值
        knowledge_id = row[0] if pd.notna(row[0]) else ''  # 第一列，空值替换为空字符串
        knowledge_name = pc.encrypt(row[1].strip()) if pd.notna(row[1]) else ''  # 第二列
        knowledge_desc = row[2] if pd.notna(row[2]) else ''  # 第四列
        problems = pc.encrypt(row[3]) if pd.notna(row[3]) else ''  # 第三列
        special_rule = pc.encrypt(row[4]) if pd.notna(row[4]) else ''  # 第五列
        exclude_index = row[5] if pd.notna(row[5]) else ''  # 第六列
        relate_index = row[6] if pd.notna(row[6]) else ''  # 第七列
        
        # 处理 problems 和 description 字段
        f_pro = ''.join(str(row[2]).split()).lower()  # 第三列
        f_desc = ''.join(str(row[3]).split()).lower()  # 第四列
        
        # 判断 problem_index 和 desc_index
        problem_index = 'true' if any(keyword in f_pro for keyword in ['metric,', 'cib,', 'module,']) else 'false'
        desc_index = 'true' if any(keyword in f_desc for keyword in ['metric,', 'cib,', 'module,']) else 'false'
        
        # 生成 CQL 语句
        cql = """
            CREATE (n:运维经验知识 {
                knowledge_id: '%s',
                knowledge_name: '%s',
                knowledge_desc: '%s',
                special_rule: '%s',
                problems: '%s',
                exclude_index: '%s',
                relate_index: '%s',
                problem_index: '%s',
                desc_index: '%s'
            }) RETURN n;
        """ % (knowledge_id, knowledge_name, knowledge_desc, special_rule, problems, exclude_index, relate_index, problem_index, desc_index)
        
        # 执行 CQL 语句
        execute_query(driver, cql)
    print("运维经验背景知识创建完成")

def create_index_problem_from_excel(file_path, db_type,sheets):
    """从Excel文件新增指标异常信息（按列顺序读取数据）

    Args:
        file_path (str): Excel文件路径
        db_type (str): 数据库类型
    """
    # 读取Excel文件的前三个工作区
    sheet_names = list(range(sheets))
    data_sheets = pd.read_excel(file_path, sheet_name=sheet_names)  # 读取前三个工作表

    # 遍历每个工作表
    for sheet_name, data in data_sheets.items():
        print(f"正在导入工作区: {sheet_name}")
        for _, row in data.iterrows():
            # 按列顺序获取数据，并过滤空值
            index_id = pc.encrypt(str(row[0])) if pd.notna(row[0]) else ''  # 第一列
            index_desc = '\n'.join(line for line in str(row[1]).replace(';', '；').replace("'", "\\'").splitlines() if line.strip()) if pd.notna(row[1]) else ''  # 第二列
            problems = pc.encrypt(row[2]) if pd.notna(row[2]) else ''  # 第三列
            
            # 判断 include_index
            f_pro = ''.join(str(row[2]).split()).lower()  # 第三列
            include_index = 'true' if any(keyword in f_pro for keyword in ['metric,', 'cib,']) else 'false'
            
            # 生成 CQL 语句
            cql = """
                CREATE (n:指标知识 {
                    index_id: '%s',
                    index_desc: '%s',
                    db_type: '%s',
                    problems: '%s',
                    include_index: '%s',
                    index_name:'%s'
                }) RETURN n;
            """ % (index_id, index_desc, db_type, problems, include_index,get_index_name(row[0]))
            
            # 执行 CQL 语句
            execute_query(driver, cql)
    print("指标信息创建完成")


def delete_nodes_by_label(driver, label):
    """删除指定标签的所有节点"""
    query = f"MATCH (n:{label}) DETACH DELETE n"
    execute_query(driver, query)
    print(f"已删除所有标签为 '{label}' 的节点")


def update_plan_rule(file_path):
    """更新计划规则"""
    # 读取Excel文件
    data = pd.read_excel(file_path)
    
    for _, row in data.iterrows():
        # 按列顺序获取数据，并过滤空值
        plan_name = row[0] if pd.notna(row[0]) else ''  # 第一列
        plan_rule = pc.encrypt(row[1]) if pd.notna(row[1]) else ''  # 第二列
        cql = """
            CREATE (n:执行计划规则 {
                plan_name: '%s',
                plan_rule: '%s'
            })
        """ % (plan_name, plan_rule)
        execute_query(driver, cql)
    print("计划规则更新完成")


if __name__ == '__main__':
    # 删除“指标知识”和“运维经验知识”两个类型的节点
    delete_nodes_by_label(driver, "指标知识")
    delete_nodes_by_label(driver, "运维经验知识")
    create_knowledge_from_excel('/root/docs/common_knowledge.xlsx')
    create_knowledge_from_excel('/root/docs/oracle_knowledge.xlsx')
    create_index_problem_from_excel('/root/docs/oracle_index.xlsx', '2101',3)


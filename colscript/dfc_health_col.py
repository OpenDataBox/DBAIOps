import psycopg2
import cx_Oracle as oracle
import re
# coding=utf-8

class Result(object):

    # pass
    def __str__(self):
        return "\n".join("{}={}".format(k, getattr(self, k))
                        for k in self.__dict__.keys())

# -----postgre-----
def relate_pg(**args):
    conn =1
    result = Result()
    try:
        conn = psycopg2.connect(database=args['database'],user=args['user'],password=args['password'],host=args['host'],port=args['port'])
        cur=conn.cursor()
        cur.execute(args['sql'])
        rows=cur.fetchall()
        rows = rows[0:4]
        msg = []
        result.code = 0
        for row in rows:
            # print(list(row))
            msg.append(row)
        result.msg = msg
    except psycopg2.ProgrammingError:
        result.code = 2
        result.msg = "SQL Error"
    except psycopg2.OperationalError:
        result.code = 1
        result.msg = "Connect Error"
    finally:
        if 1 == conn:
            result.code = 1
            result.msg = "Connect Error"
    # print(result)
    return result

def relate_oracle(**args):
    result = Result()
    #print(args['sql'])
    try:
        tns = oracle.makedsn(args['host'], args['port'], args['database'])
        db = oracle.connect(args['user'], args['password'], tns)
        cur = db.cursor()
        cur.execute(args['sql'])
        rows = cur.fetchall()
        msg = []
        for row in rows:
            msg.append(row)
        result.code = 0
        result.msg = msg
    except oracle.DatabaseError as e:
        result.code = 1
        result.msg = "Connect Error"
    return result



def getValueFromDB(url,usr,pwd,sql):
    type,host,port,database = parseURL(url)
    config = {
        'database': database,
        'user': usr,
        'password': pwd,
        'host': host,
        'port': port,
        'sql': sql
    }
    if "oracle" == type:
        result = relate_oracle(**config)
    elif "postgresql" == type:
        result = relate_pg(**config)
    return result

def parseURL(url):
    pattern = r'(\w+):(\w+)([thin:@/]+)([0-9.]+):(\d+)([:/])(\w+)'
    matchObj = re.match(pattern, url, re.I)
    return matchObj.group(2),matchObj.group(4),matchObj.group(5),matchObj.group(7)



if __name__ == '__main__':
    sql = '''select D.tablespace_name,round((REAL_SPACE-nvl(FREE_SPACE,0))*100/TOTAL_SPACE,2) PCT_USED,(REAL_SPACE-nvl(FREE_SPACE,0))/REAL_SPACE PCT_USED2 from
(select a.tablespace_name,sum(BYTES) REAL_SPACE,sum(decode(b.AUTOEXTENSIBLE,'YES',MAXBYTES,BYTES)) TOTAL_SPACE,sum(decode(b.AUTOEXTENSIBLE,'YES',MAXBYTES-BYTES,0)) EXT_SPACE from dba_tablespaces a,dba_data_files b where a.tablespace_name=b.tablespace_name and a.contents<>'UNDO' group by a.tablespace_name) D,
(SELECT TABLESPACE_NAME,SUM(BYTES) FREE_SPACE FROM DBA_FREE_SPACE GROUP BY TABLESPACE_NAME) F
where D.TABLESPACE_NAME = F.TABLESPACE_NAME(+)'''
    usr = "system"
    pwd = "oracle"
    url = "jdbc:oracle:thin:@60.60.60.83:1521:node83"
    result = getValueFromDB(url,usr,pwd,sql)
    flag = False
    print('{"metric":[{"index_id":"2000200","value":[')
    for row in result.msg:
      print('{"name":"' + row[0] + '","value":"' + str(row[1]) + '"},')
      if row[1] > 0:
        if not flag:
          flag = True
          msg = 'The following tablespace(s) used_rate>90%:'
        msg = msg + row[0] + '(' + str(row[1]) + '%)'
    print(']}],')
    if flag:
      print('"check":[{"model":"1","id":"1","result":"FAIL","detail":"' + msg + '"}]}')
    else:
      print('"check":[{"model":"1","id":"1","result":"OK"}]}')

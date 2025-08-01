import sys
sys.path.append('/usr/software/knowl')
import ResultCode
import traceback
import psycopg2

from JavaRsa import decrypt


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
    fd = open('/usr/software/role.cfg', 'r')
    for row in fd.readlines():
        if 'DSPG_Node=' in row:
            pg_ip = row.split('=')[1].strip()
        elif 'DSPG_Port' in row:
            pg_port = row.split('=')[1].strip()
        elif 'DSPG_User' in row:
            pg_user = row.split('=')[1].strip()
            pg_user = decrypt(pg_user)
        elif 'DSPG_Password' in row:
            pg_pwd = row.split('=')[1].strip()
            pg_pwd = decrypt(pg_pwd)
        elif 'DSPG_Database' in row:
            pg_db = row.split('=')[1].strip()
    pg = Postgre(pg_ip, pg_user, pg_pwd, pg_port, pg_db,0)
    if pg.conn is None:
        sys.exit(0)
    try:
        sql = '''
begin;
truncate table fs_trigger_group;
INSERT INTO public.fs_trigger_group (id, app_name, title, group_order, address_type, address_list) VALUES (1000, 'rt-job-executor', 'commonExecutor', 1, 0, '127.0.0.1:9090');
INSERT INTO public.fs_trigger_group (id, app_name, title, group_order, address_type, address_list) VALUES (1001, 'rt-job-executor', 'returnOPSExecutor', 2, 0, '127.0.0.1:9090');
end;
'''
        pg.execute(sql)
    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

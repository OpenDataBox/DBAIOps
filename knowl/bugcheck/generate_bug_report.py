import sys
import json
from _generate_bug_report import *
sys.path.append('/usr/software/knowl')
import DBUtil

if __name__ == '__main__':
    dbinfo = json.loads(sys.argv[1])
    cve_name = dbinfo['cve_name']
    pg = DBUtil.get_pg_from_cfg()
    store_cve(pg)
    buginfo = generate_report(pg, cve_name)
    print(json.dumps(buginfo))

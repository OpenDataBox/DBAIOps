#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

sys.path.append('/usr/software/knowl')
import DBUtil
import psycopg2
import re
import PGUtil
import ResultCode
import tags


def register(file_name):
    ltag = ['0', 'Summary']
    return tags.register(ltag, file_name)


class Result(object):
    def __str__(self):
        return "\n".join("{}={}".format(k, getattr(self, k))
                         for k in self.__dict__.keys())


def getValue(ora, sql):
    result = ora.execute(sql)
    if (result.code != 0):
        print("msg=" + result.msg)
        sys.exit()
    return result.msg


def parseURL(url):
    pattern = r'(\w+):(\w+)([thin:@/]+)([0-9.]+):(\d+)([:/])(\w+)'
    matchObj = re.match(pattern, url, re.I)
    return matchObj.group(2), matchObj.group(4), matchObj.group(5), matchObj.group(7)


if __name__ == '__main__':

    dbInfo = eval(sys.argv[1])
    ##pg info
    dbip = dbInfo['pg_ip']
    dbname = dbInfo['pg_dbname']
    username = dbInfo['pg_usr']
    password = dbInfo['pg_pwd']
    pgport = dbInfo['pg_port']
    ##ora info
    usr = dbInfo['ora_usr']
    pwd = dbInfo['ora_pwd']
    host = dbInfo['ora_ip']
    port = dbInfo['ora_port']
    database = dbInfo['ora_sid']

    targetid = dbInfo['targetId']
    begintime = dbInfo['start_time']
    endtime = dbInfo['end_time']

    rpt_id = dbInfo['rptid']

    pg = PGUtil.Postgre(dbip, username, password, pgport, dbname)

    try:
        result = ""
        ##总体评价
        insql = '''        
begin;
delete from rpt_summary where rpt_id = '{0}' and target_id = '{1}' and rpt_note='总体评价';

insert into rpt_summary(rpt_id,target_id,rpt_item,rpt_score,rpt_note)
select '{0}' rpt_id,'{1}' target_id,'数据库配置' rpt_item, 
(select count(1) from rpt_finding where rpt_id='{0}'
and target_id='{1}'
and rpt_finding_module like 'basic%'
and rpt_finding_module <>'basic_runinfo_ri') rpt_score,'总体评价' rpt_note;

with model as (
    select distinct
      b.model_item_name,
      b.model_item_id,
      b.model_id,
      d.health_check_id
    from
      h_model_item b,
      h_health_model c,
      h_health_check d
    where b.use_flag = true
          and c.use_flag = true
          and d.target_id = '{1}'
          and d.model_id = c.model_id
          and b.model_id = d.model_id
) 
insert into rpt_summary(rpt_id,target_id,rpt_item,rpt_score,rpt_note)
select '{0}' rpt_id,'{1}' target_id,'数据库健康度' rpt_item,round(sum(score)::numeric,2) rpt_score,'总体评价' rpt_note from (
select avg(a.score) score,b.model_item_name
from 
h_health_check_item_score a,
model b 
where a.model_item_id=b.model_item_id
and a.model_id=b.model_id
and a.health_check_id = b.health_check_id 
and a.record_time between '{2}' and '{3}'
group by b.model_item_name
) a;

insert into rpt_summary(rpt_id,target_id,rpt_item,rpt_score,rpt_note)
select '{0}' rpt_id,'{1}' target_id,'数据库负载' rpt_item,round(avg(a.load_score),2) rpt_score,'总体评价' rpt_note
from p_perf_eva_his a,
p_perf_eva b
where b.eva_id=a.eva_id 
and b.target_id='{1}'
and a.record_time between '{2}' and '{3}';

insert into rpt_summary(rpt_id,target_id,rpt_item,rpt_score,rpt_note)
select '{0}' rpt_id,'{1}' target_id,'数据库性能' rpt_item,round(avg(a.perf_score),2) rpt_score,'总体评价' rpt_note
from p_perf_eva_his a,
p_perf_eva b
where b.eva_id=a.eva_id 
and b.target_id='{1}'
and a.record_time between '{2}' and '{3}';

end;
'''.format(rpt_id, targetid, begintime, endtime)
        pg.execute(insql)

        ##分项评价
        insql = '''
begin;

delete from rpt_summary where rpt_id = '{0}' and target_id = '{1}' and rpt_note='分项评价';

insert into rpt_summary(rpt_id,target_id,rpt_item,rpt_score,rpt_note)
select '{0}' rpt_id,'{1}' target_id,b.model_item_name rpt_item,round(avg(a.score)::numeric,2) rpt_score,'分项评价' rpt_note
from 
h_health_check_item_score a,
h_model_item b,
h_health_model c,
h_health_check d
where a.model_item_id=b.model_item_id
and b.use_flag=true
and c.use_flag=true
and a.model_id=c.model_id
and b.model_id=c.model_id 
and a.record_time between '{2}' and '{3}'
and d.target_id ='{1}'
and d.model_id = c.model_id
group by b. model_item_name
'''.format(rpt_id, targetid, begintime, endtime)
        pg.execute(insql)

        ##更新评价字段
        upsql = '''
begin;
delete from rpt_summary where rpt_id='{0}' and target_id='{1}' and rpt_item='数据库负载' and rpt_note='分项评价';

update rpt_summary set rpt_adjust=
case when rpt_score=0 then '良好'
     when rpt_score<5 then '正常'
     when rpt_score>=5 and rpt_score<10 then '一般'
else '较差' end
where rpt_id='{0}' and target_id='{1}' and rpt_item='数据库配置';

update rpt_summary set rpt_adjust=
case when rpt_score >=90 then '良好'
     when rpt_score >=80 and rpt_score<90 then '正常'
     when rpt_score >=60 and rpt_score<80 then '一般'
else '较差' end
where rpt_id='{0}' and target_id='{1}' and rpt_item='数据库健康度';

update rpt_summary set rpt_adjust=
case when rpt_score >=90 then '良好'
     when rpt_score >=80 and rpt_score<90 then '正常'
     when rpt_score >=60 and rpt_score<80 then '一般'
else '较差' end
where rpt_id='{0}' and target_id='{1}' and rpt_item='数据库性能';

update rpt_summary set rpt_adjust=
case when rpt_score >=90 then '极高'
     when rpt_score <90 and rpt_score>=75 then '较高'
     when rpt_score <75 and rpt_score>=60 then '中等'
else '较小' end
where rpt_id='{0}' and target_id='{1}' and rpt_item='数据库负载';

update rpt_summary set rpt_adjust=
case when rpt_score >=12 then '良好'
     when rpt_score >=10 and rpt_score<12 then '正常'
     when rpt_score >=8 and rpt_score<10 then '一般'
else '较差' end
where rpt_id='{0}' and target_id='{1}' and rpt_item='操作系统';

update rpt_summary set rpt_adjust=
case when rpt_score >=9 then '良好'
     when rpt_score >=7 and rpt_score<9 then '正常'
     when rpt_score >=5 and rpt_score<7 then '一般'
else '较差' end
where rpt_id='{0}' and target_id='{1}' and rpt_item='数据库IO';

update rpt_summary set rpt_adjust=
case when rpt_score >=23 then '良好'
     when rpt_score >=18 and rpt_score<23 then '正常'
     when rpt_score >=13 and rpt_score<18 then '一般'
else '较差' end
where rpt_id='{0}' and target_id='{1}' and rpt_item='数据库总体状况';

update rpt_summary set rpt_adjust=
case when rpt_score >=12 then '良好'
     when rpt_score >=9 and rpt_score<12 then '正常'
     when rpt_score >=6 and rpt_score<9 then '一般'
else '较差' end
where rpt_id='{0}' and target_id='{1}' and rpt_item='数据库并发执行';

update rpt_summary set rpt_adjust=
case when rpt_score >=8 then '良好'
     when rpt_score >=6 and rpt_score<8 then '正常'
     when rpt_score >=4 and rpt_score<6 then '一般'
else '较差' end
where rpt_id='{0}' and target_id='{1}' and rpt_item='数据库命中率';

update rpt_summary set rpt_adjust=
case when rpt_score >=7 then '良好'
     when rpt_score >=5 and rpt_score<7 then '正常'
     when rpt_score >=3.5 and rpt_score<5 then '一般'
else '较差' end
where rpt_id='{0}' and target_id='{1}' and rpt_item='数据库RAC';

end;
'''.format(rpt_id, targetid)
        pg.execute(upsql)
    except psycopg2.DatabaseError as e:
        if not pg is None:
            pg.close()

    # except Exception as e:
    #    errorInfo = str(e)
    #    print("异常：" + errorInfo)

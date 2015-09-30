### This is data graph library for generic function for many graphs
### This will respond the jsons for the graph which are all getting inputs as column names, days and table name
### Date Created: Sep 25th, 2015
### Originated By Hariharaselvam Balasubramanian (4470)

from mysqlclass import MysqlPython
import json
import datetime
import re
from bson import json_util

def data_graph(**params):
	conn = MysqlPython('localhost', 'root', 'mysql123', 'SCG');
	days = params['days']
	tablename= params['tablename']
	column_one= params['column_one']
	column_two= params['column_two']
	timestamp_col= params['timestamp_col']
	where_condition= params['where_condition']
	convert = params['convert']
	graph_sql = "select "+column_one+" , "+column_two+" , "+timestamp_col+" from "+tablename+" where "+where_condition+" and "+timestamp_col+">=DATE_SUB(CURDATE(),INTERVAL "+str(days)+" DAY) ORDER BY "+column_one+" , "+column_two+" , "+timestamp_col+" asc";
	print "\n"+graph_sql+"\n"	
        data = conn.select_advanced(graph_sql);
        series_list=[];
        json_string='[ { "name" : "Show/Hide All" } ';
        for row in data:
                if row[0] not in series_list:
                        series_list.append(row[0]);

        for series in series_list:
                graph_data=[]
                for row in data:
                        if row[0]==series:
                                timestamp=str(row[2]);
                                timestamp=int(datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime('%s')) * 1000;
                                count=row[1]
				if convert == 'uptime':
					count= convert_to_min(row[1])
				if convert == 'percent':
					count= convert_percent(row[1])
                                if count != None:
                                        graph_data.append("["+str(timestamp)+","+str(count)+"]");
                json_string=json_string+', { "name" : "'+series+'" , "data" : '+'[ '+', '.join(graph_data)+' ] }';
        json_string=json_string+' ]';
        return json_string;
                	


def convert_to_min(uptime):
	pat="\d+[a-z]"
	uptime=re.findall(pat,uptime)
        #uptime=uptime.split();
        day=0;
        hour=0;
        min=0;
        sec=0;
        for upt in uptime:
                if upt.endswith('d'):
                        day=int(upt[:-1]);
                        continue;
                        continue;
                if upt.endswith('h'):
                        hour=int(upt[:-1]);
                        continue;
                if upt.endswith('m'):
                        min=int(upt[:-1]);
                        continue;
                if upt.endswith('s'):
                        sec=int(upt[:-1]);
        result=(day*24*60)+(hour*60)+(min*1)+int(sec/60)
        return result;

def convert_percent(percent):
	percent=percent.replace("%","")
	return int(percent)

def convert_timestamp(search_time):
        print search_time
        try:
                dtime=datetime.datetime.strptime(search_time,"%b %d, %Y %H:%M");
                print dtime
                search_time=dtime.strftime("%Y-%m-%d %H:%M")
        except Exception:
                pass
        return str(search_time)

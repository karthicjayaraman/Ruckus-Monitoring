### This is ZD logs blue print
### Date: Sep 29th, 2015



from flask import Blueprint,g, request
from flask_cors import cross_origin
import json
import datetime
from bson import json_util
from ..lib.data_tables import big_table
zd_logs = Blueprint('zd_logs', __name__, url_prefix='/zd')

@zd_logs.route('/get_logs', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_logs():
        start=0;
        limit=20;
        starttime='2014-09-09 17:30:12';
        endtime='2014-09-09 17:30:22';
        search='2014-9-09 17:30:16';
        page=0;
        if request.method == 'POST':
                json_data = request.get_json();
                limit=json_data.get("limit", "")
                page=json_data.get("page","")
                starttime=json_data.get("start_time","")
                endtime=json_data.get("end_time","")
                search=json_data.get("search_time","")
        limit=int(limit);
        page=int(page);
        start=page*limit;
        columns=['Timestamp','Content']
       # logs_act_sql="select "+",".join(columns)+" from Logs where Timestamp between '" +str(starttime)+ "' and '" +str(endtime)+ "' limit " +str(start)+ ", " +str(limit)
        #logs_act_sql="select "+",".join(columns)+" from Logs where Timestamp between '" +str(starttime)+ "' and '" +str(endtime)+ "' ORDER BY Timestamp ASC limit " +str(start)+ ", " +str(limit)
	
	"""if search:
            logs_act_sql="select "+",".join(columns)+" from Logs where Timestamp between '" +str(starttime)+ "' and '" +str(endtime)+ "'OR Timestamp between '" +str(search)+ "' and '"+str(endtime)+ "'  ORDER BY Timestamp ASC limit " +str(start)+ ", " +str(limit)
        else:
        logs_act_sql="select "+",".join(columns)+" from Logs where Timestamp between '" +str(starttime)+ "' and '" +str(endtime)+ "' ORDER BY Timestamp DESC limit " +str(start)+ ", " +str(limit)"""

        if search:
           logs_act_sql="select "+",".join(columns)+" from Logs where Timestamp = '" +str(search)+ "' ORDER BY Timestamp DESC limit " +str(start)+ ", " +str(limit)

        else:
           logs_act_sql="select "+",".join(columns)+" from Logs where Timestamp between '" +str(starttime)+ "' and '" +str(endtime)+ "' ORDER BY Timestamp DESC limit " +str(start)+ ", " +str(limit)





        result=[];
        data = g.conn.select_advanced(logs_act_sql);
        for row in data:
                result.append(dict(zip(columns, row)))
        count_sql="select count(*) from Logs ";
        cdata = g.conn.select_advanced(count_sql);
        count=cdata[0];
        count_filsql="select count(*) from Logs Where Timestamp = '" +str(search)+ "' ";
        cdata1 = g.conn.select_advanced(count_filsql);
        filcount=cdata1[0];
        json_data={'count':count,'items':result,'filteredcount':filcount}
        return json.dumps(json_data, default=json_util.default)


@zd_logs.route('/logs', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def logs():
        page=1;
        limit=10;
        table="Logs";
        where="1=1";
        columns=['Timestamp','Content']
        sparams={};
        if request.method == 'POST':
                json_data = request.get_json();
                ### Limit parameters
                limit=json_data.get("limit", "")
                page=json_data.get("page","")
                if limit=='':
                        limit=10;
                else:
                        limit=int(limit);
                if page=='':
                        page=1;
                else:
                        page=int(page);
                ### Search parameters
                Timestamp="";
                Content="";
                Timestamp=json_data.get("Timestamp","")
                Content=json_data.get("Content","")
                if TimeStamp!='' and TimeStamp!=None:
                        sparams['Timestamp']=convert_timestamp(timestamp);
                if Content!='' and Content!=None:
                        sparams['Content']=Content;
        return big_table(tablename=table,where_condition=where,limit=limit,page=page,columns=columns,search=sparams);

def convert_timestamp(search_time):
        print search_time
        try:
                dtime=datetime.datetime.strptime(search_time,"%b %d, %Y %H:%M");
                print dtime
		search_time=dtime.strftime("%Y-%m-%d %H:%M")
        except Exception:
                pass
        return str(search_time)

  

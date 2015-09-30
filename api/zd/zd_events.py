### This is ZD events blue print
### This will respond the jsons regarding events such as 
### Date: Sep 29th, 2015



from flask import Blueprint,g, request
from flask_cors import cross_origin
import json
import datetime
from bson import json_util
from ..lib.data_tables import big_table
zd_events = Blueprint('zd_events', __name__, url_prefix='/zd')

@zd_events.route('/get_events', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_events():
        start=0;
        limit=20;
        starttime='2014-11-06 06:30:12';
        endtime='2014-11-06 06:30:18';
        page=0;
        if request.method == 'POST':
                json_data = request.get_json();
                limit=json_data.get("limit", "")
                page=json_data.get("page","")
                starttime=json_data.get("start_time","")
                endtime=json_data.get("end_time","")
        limit=int(limit);
        page=int(page);
        start=page*limit;
        columns=['datetime','system','severity','events']
        events_act_sql="select "+",".join(columns)+" from events where datetime between '" +str(starttime)+ "' and '" +str(endtime)+ "' limit " +str(start)+ ", " +str(limit)
        #logs_act_sql= "SELECT * FROM `Logs` where Timestamp between '2014-09-09 17:30:02' and '2014-09-09 17:30:24'"
        result=[];
        data = g.conn.select_advanced(events_act_sql);
        for row in data:
		result.append(dict(zip(columns, row)))
        count_sql="select count(*) from events ";
        cdata = g.conn.select_advanced(count_sql);
        count=cdata[0];
        json_data={'count':count, 'items':result}
        return json.dumps(json_data, default=json_util.default)



@zd_events.route('/events', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def events():
        page=1;
        limit=10;
        table="events";
	columns=['datetime','system','severity','events']
        where="1=1";
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
                datetime="";
                system="";
                severity="";
                events="";
                datetime=json_data.get("datetime","")
                system=json_data.get("system","")
                severity=json_data.get("severity","")
                events=json_data.get("events","")
                if datetime!='' and datetime!=None:
                        sparams['datetime']=datetime;
                if system!='' and system!=None:
                        sparams['system']=system;
                if severity!='' and severity!=None:
                        sparams['severity']=severity;
                if events!='' and events!=None:
                        sparms['events']=events;
        return big_table(tablename=table,where_condition=where,limit=limit,page=page,columns=columns,search=sparams);




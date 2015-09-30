### This is SCG events blue print
### This will respond the jsons regarding events such as global config, add, edit, display
### Date: Sep 9th, 2015



from flask import Blueprint,g, request
from flask_cors import cross_origin
import json
import datetime
from bson import json_util
from ..lib.data_tables import big_table
scg_events = Blueprint('scg_events', __name__, url_prefix='/scg')

@scg_events.route('/get_events', methods=['GET', 'POST', 'OPTIONS'])
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
        columns=['Timestamp','SCGName','Severity','Event']
        events_act_sql="select "+",".join(columns)+" from Events where Timestamp between '" +str(starttime)+ "' and '" +str(endtime)+ "' limit " +str(start)+ ", " +str(limit)
        #logs_act_sql= "SELECT * FROM `Logs` where Timestamp between '2014-09-09 17:30:02' and '2014-09-09 17:30:24'"
        result=[];
        data = g.conn.select_advanced(events_act_sql);
        for row in data:
                result.append(dict(zip(columns, row)))
        count_sql="select count(*) from Events ";
        cdata = g.conn.select_advanced(count_sql);
        count=cdata[0];
        json_data={'count':count, 'items':result}
        return json.dumps(json_data, default=json_util.default)



@scg_events.route('/events', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def events():
        page=1;
        limit=10;
        table="Events";
        where="1=1";
	columns=['Timestamp','SCGName','Severity','Event']
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
                SCGName="";
                Severity="";
                Event="";
                Timestamp=json_data.get("Timestamp","")
                SCGName=json_data.get("SCGName","")
                Severity=json_data.get("Severity","")
                Event=json_data.get("Event","")
		if TimeStamp!='' and TimeStamp!=None:
                        sparams['Timestamp']=convert_timestamp(timestamp);
                if SCGName!='' and SCGName!=None:
                        sparams['SCGName']=SCGName;
                if Severity!='' and Severity!=None:
                        sparams['Severity']=Severity;
		if Event!='' and Event!=None:
			sparms['Event']=Event;
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




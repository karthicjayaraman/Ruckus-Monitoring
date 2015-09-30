### This is ZD Dashboard blue print
### This will respond the jsons regarding ZD dashboard such as global config, devices, dataplane, controlplane
### Date: Sep 3rd, 2015

from flask import Blueprint,g, request
from flask_cors import cross_origin
import json
import datetime
from bson import json_util
from ..lib.data_tables import big_table
from ..lib.data_graphs import data_graph
zd_dashboard = Blueprint('zd_dashboard', __name__, url_prefix='/zd')



@zd_dashboard.route('/critical_system', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def critical_system():
        page=1;
        limit=10;
        table="CriticalActivities";
        where="1=1";
        columns=['Content']
        sparams={};
        if request.method == 'POST':
                json_data = request.get_json();
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
                Timestamp=""
                #IPAddress="";
                #MacAddress="";
		#Content="";
                #Timestamp=json_data.get("Timestamp","")
                #IPAddress=json_data.get("IPAddress","")
                #MacAddress=json_data.get("MacAddress","")
		Content=json_data.get("Content","")
	#	if Timestamp!='' and Timestamp!=None:
         #               sparams['Timestamp']=convert_timestamp(timestamp);
                #if IPAddress!='' and IPAddress!=None:
                #        sparams['IPAddress']=IPAddress;
		#if MacAddress!='' and MacAddress!=None:
	#		sparams['MacAddress']=MacAddress;
		if Content!='' and Content!=None:
			sparams['Content']=Content;
                
        return big_table(tablename=table,where_condition=where,limit=limit,page=page,columns=columns,search=sparams);


@zd_dashboard.route('/get_critical_activities', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_critical_activities():
        page=1;
        limit=10;
        table="CriticalActivities";
        where="1=1";
        columns=['Timestamp','IPAddress','MacAddress','Content']
        sparams={};
        if request.method == 'POST':
                json_data = request.get_json();
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
                Timestamp=""
                IPAddress="";
                MacAddress="";
                Content="";
                Timestamp=json_data.get("Timestamp","")
                IPAddress=json_data.get("IPAddress","")
                MacAddress=json_data.get("MacAddress","")
                Content=json_data.get("Content","")
                if Timestamp!='' and Timestamp!=None:
                        sparams['Timestamp']=convert_timestamp(timestamp);
                if IPAddress!='' and IPAddress!=None:
                        sparams['IPAddress']=IPAddress;
                if MacAddress!='' and MacAddress!=None:
                        sparams['MacAddress']=MacAddress;
                if Content!='' and Content!=None:
                        sparams['Content']=Content;

	return big_table(tablename=table,where_condition=where,limit=limit,page=page,columns=columns,search=sparams);

@zd_dashboard.route('/get_ap_activities', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_ap_activities():
        page=1;
        limit=10;
        table="APActivities";
        where="1=1";
        columns=['Timestamp','IPAddress','Activity']
        sparams={};
        if request.method == 'POST':
                json_data = request.get_json();
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
                Timestamp=""
                IPAddress="";
                Activity=""
                Timestamp=json_data.get("Timestamp","")
                IPAddress=json_data.get("IPAddress","")
                Activity=json_data.get("Activity","")
                if Timestamp!='' and Timestamp!=None:
                        sparams['Timestamp']=convert_timestamp(timestamp);
                if IPAddress!='' and IPAddress!=None:
                        sparams['IPAddress']=IPAddress;
                if Activity!='' and Activity!=None:
			sparams['Activity']=Activity;
                        
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

@zd_dashboard.route('/EventActivities', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def EventActivities():
        start=1;
        limit=20;
        page=1;
        #scg_name=""
        scg_log="";
        timestamp=""
        columns=['DateTime','Severity','Activity']
        if request.method == 'POST':
                json_data = request.get_json();
                limit=json_data.get("limit", "")
                page=json_data.get("page","")
               # scg_name=json_data.get("scg_name","")
                scg_log=json_data.get("scg_log","")
                DateTime=json_data.get("DateTime","")
                if limit=='':
                        limit=20;
                else:
                        limit=int(limit);
                if page=='':
                        page=1;
                else:
                        page=int(page);
        page=page-1;
        start=limit*page
        wh=0;
        where_clause=" where "
        if scg_log!='' and scg_log!=None:
                where_clause=where_clause+" Activity like '%%"+scg_log+"%%' and"
                wh=1;
        '''
        if scg_name!='' and scg_name!=None:
                where_clause=where_clause+" SCGName like '%%"+scg_name+"%%' and"
                wh=1;
        '''
        if timestamp!='' and timestamp!=None:
                timestamp=convert_timestamp(timestamp);
                where_clause=where_clause+" Timestamp like '%%"+timestamp+"%%' and"
                wh=1;
        if wh==1:
                where_clause=where_clause[:-4]
        else:
                where_clause=""
        count_sql="select count(*) from ruckus.EventActivities";
        cdata = g.conn.select_advanced(count_sql);
        count = cdata[0];
        fcount=count;
        if wh==1:
                f_count_sql=count_sql+where_clause;
                print f_count_sql
                fc_data= g.conn.select_advanced(f_count_sql);
                fcount = fc_data[0];
                print fcount
        if fcount < start:
                start=0;

        ap_act_sql="select DateTime,Severity,Activity from ruckus.EventActivities "+where_clause+" order by DateTime desc limit "+str(start)+","+str(limit);

        print "\n"+ap_act_sql+"\n"
        result=[];
        data = g.conn.select_advanced(ap_act_sql);
        for row in data:
                #print row
                result.append(dict(zip(columns, row)))
        json_data={'count':count, 'items':result, 'filter_count':fcount }
        print "\n\n"
        return json.dumps(json_data, default=json_util.default)



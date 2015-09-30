### This is SCG dashboard graphs blue print
### This will respond the jsons regarding scg trends such as global config, devices, dataplane, controlplane
### Date: Sep 3rd, 2015

from flask import Blueprint,g, request
from flask_cors import cross_origin
import json
import datetime
from bson import json_util
scg_dashboard_graph = Blueprint('scg_dashboard_graph', __name__, url_prefix='/scg')

@scg_dashboard_graph.route('/get_controlplane_graph_data', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_controlplane_graph_data():
        scgip='10.150.5.7';
        period='24-h'
        days=7;
        cplane='SCG-5-perf-C';
        if request.method == 'POST':
                json_data = request.get_json();
                scgip=json_data.get("scg_ip", "")
                controlplane=json_data.get("control_plane", "")
                period=json_data.get("period", "")
        if period=='' or period==None:
                period='8-h'


        control_sql="SELECT RXMBytes,TXMBytes,TotalMBytes,Timestamp FROM `ControlPlaneUsageHistory` where  ControlPlaneName='"+cplane+"' and SCGIP='"+scgip+"' and Period ='"+period+"' and Timestamp>=DATE_SUB(CURDATE(),INTERVAL "+str(days)+" DAY) order by Timestamp asc"
        data = g.conn.select_advanced(control_sql);
        print control_sql        
	rxmbytes_list=[]
        txmbytes_list=[]
        totalmbytes_list=[]
        graph_data=[];
        for row in data:
                timestamp=str(row[3]);
                rxmbytes=str(row[0]);
                txmbytes=str(row[1]);
                totalmbytes=str(row[2]);
                timestamp1=int(datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime('%s')) * 1000;
                rxmbytes_list.append("["+str(timestamp1)+","+str(rxmbytes)+"]")
                txmbytes_list.append("["+str(timestamp1)+","+str(txmbytes)+"]") 
              
		
        json_string='[ { "name" : "Show/Hide All" } ';
        json_string=json_string+', { "name" : "rxmbytes" , "data" : '+'[ '+', '.join(rxmbytes_list)+' ] }';
               
        json_string=json_string+', { "name" : "txmbytes" , "data" : '+'[ '+', '.join(txmbytes_list)+' ] }';
        json_string=json_string+', { "name" : "totalmbytes" , "data" : '+'[ '+', '.join(totalmbytes_list)+' ] }'; 
        json_string=json_string+' ]';
	return json_string;

@scg_dashboard_graph.route('/get_dataplane_graph_data', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_dataplane_graph_data():
           
        scgip='10.150.5.7';
        period='24-h'
        days=7;
        cplane='SCG-5-perf-C';
        dplane='SCG-5-perf-D0';
        if request.method == 'POST':
                json_data = request.get_json();
                scgip=json_data.get("scg_ip", "")
                controlplane=json_data.get("control_plane", "")
                period=json_data.get("period", "")
        if period=='' or period==None:
                period='8-h'

        data_sql="SELECT RXMBytes,TXMBytes,TotalMBytes,Timestamp FROM `DataPlaneUsageHistory` where  ControlPlaneName='"+cplane+"' and DataPlaneName='"+dplane+"'and  SCGIP='"+scgip+"' and Period ='"+period+"' and Timestamp>=DATE_SUB(CURDATE(),INTERVAL "+str(days)+" DAY) order by Timestamp asc"
        data = g.conn.select_advanced(data_sql);
        print data_sql
        rxmbytes_list=[]
        txmbytes_list=[]
        totalmbytes_list=[]
        graph_data=[];
        for row in data:
                timestamp=str(row[3]);
                rxmbytes=str(row[0]);
                txmbytes=str(row[1]);
                totalmbytes=str(row[2]);
                timestamp1=int(datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime('%s')) * 1000;
                rxmbytes_list.append("["+str(timestamp1)+","+str(rxmbytes)+"]")
                txmbytes_list.append("["+str(timestamp1)+","+str(txmbytes)+"]")


        json_string='[ { "name" : "Show/Hide All" } ';
        json_string=json_string+', { "name" : "rxmbytes" , "data" : '+'[ '+', '.join(rxmbytes_list)+' ] }';

        json_string=json_string+', { "name" : "txmbytes" , "data" : '+'[ '+', '.join(txmbytes_list)+' ] }';
        json_string=json_string+', { "name" : "totalmbytes" , "data" : '+'[ '+', '.join(totalmbytes_list)+' ] }';
        json_string=json_string+' ]';
        return json_string;


@scg_dashboard_graph.route('/get_zone_graph_data', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_zone_graph_data():

        scgip='10.150.5.7';
        days=7;
        cplane='SCG-5-perf-C';
        dplane='SCG-5-perf-D0';
        zone='perf';
        if request.method == 'POST':
                json_data = request.get_json();
                scgip=json_data.get("scg_ip", "")
                zone=json_data.get("zone", "")

        zone_sql="SELECT RXMBytes,TXMBytes,TotalMBytes,Timestamp FROM `ZoneDataUsage` where SCGIP='"+scgip+"' and ZoneName ='"+zone+"' and Timestamp>=DATE_SUB(CURDATE(),INTERVAL "+str(days)+" DAY) order by Timestamp asc"
        data = g.conn.select_advanced(zone_sql);
        print zone_sql
        rxmbytes_list=[]
        txmbytes_list=[]
        totalmbytes_list=[]
        graph_data=[];
        for row in data:
                timestamp=str(row[3]);
                rxmbytes=str(row[0]);
                txmbytes=str(row[1]);
                totalmbytes=str(row[2]);
                timestamp1=int(datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime('%s')) * 1000;
                rxmbytes_list.append("["+str(timestamp1)+","+str(rxmbytes)+"]")
                txmbytes_list.append("["+str(timestamp1)+","+str(txmbytes)+"]")
	
 	json_string='[ { "name" : "Show/Hide All" } ';
        json_string=json_string+', { "name" : "rxmbytes" , "data" : '+'[ '+', '.join(rxmbytes_list)+' ] }';

        json_string=json_string+', { "name" : "txmbytes" , "data" : '+'[ '+', '.join(txmbytes_list)+' ] }';
        json_string=json_string+', { "name" : "totalmbytes" , "data" : '+'[ '+', '.join(totalmbytes_list)+' ] }';
        json_string=json_string+' ]';
        return json_string;

### This is SCG Trends blue print
### This will respond the jsons regarding scg trends such as global config, devices, dataplane, controlplane
### Date: Sep 3rd, 2015

from flask import Blueprint,g, request
from flask_cors import cross_origin
import json
import datetime
from bson import json_util
scg_trends = Blueprint('scg_trends', __name__, url_prefix='/scg')


@scg_trends.route('/get_client_count_data')
@cross_origin()
def get_client_count_data():
        days='7';
        if request.method == 'POST':
                json_data = request.get_json();
                days=json_data.get("days", "")

        noOfclients_sql="select ScgIP,NoOfClients,Timestamp from DevicesCompleteInfo where Timestamp>=DATE_SUB(CURDATE(),INTERVAL "+str(days)+" DAY) ORDER BY ScgIP, TimeStamp asc";
        data = g.conn.select_advanced(noOfclients_sql);
        scgip_list=[];
        json_string='[ { "name" : "Show/Hide All" } ';
        for row in data:
                if row[0] not in scgip_list:
                        scgip_list.append(row[0]);

        for scgip in scgip_list:
                graph_data=[]
                for row in data:
                        if row[0]==scgip:
                                timestamp=str(row[2]);
                                timestamp=int(datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime('%s')) * 1000;
                                count=row[1]
                                if count != None:
                                        graph_data.append("["+str(timestamp)+","+str(count)+"]");
                json_string=json_string+', { "name" : "'+scgip+'" , "data" : '+'[ '+', '.join(graph_data)+' ] }';
        json_string=json_string+' ]';
        return json_string;

@scg_trends.route('/get_ap_count_data')
@cross_origin()
def get_ap_count_data():
        days='7';
        if request.method == 'POST':
                json_data = request.get_json();
                days=json_data.get("days", "")
        noOfapcount_sql="select ScgIP,NoOfAPs,Timestamp from DevicesCompleteInfo WHERE  Timestamp>=DATE_SUB(CURDATE(),INTERVAL "+str(days)+" DAY) ORDER BY ScgIP, TimeStamp asc";
        data = g.conn.select_advanced(noOfapcount_sql);
        scgip_list=[];
        json_string='[ { "name" : "Show/Hide All" }';
        for row in data:
                if row[0] not in scgip_list:
                        scgip_list.append(row[0]);

        for scgip in scgip_list:
                scgip_data={'name':scgip};
                graph_data=[]
                for row in data:
                        if row[0]==scgip:
                                timestamp=str(row[2]);
                                timestamp=int(datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime('%s')) * 1000;
                                count=row[1]
                                if count != None:
                                        graph_data.append("["+str(timestamp)+","+str(count)+"]");
                json_string=json_string+',{ "name" :"'+scgip+'" , "data" : '+'[ '+', '.join(graph_data)+' ] }';
        json_string=json_string+' ]';
        return json_string;


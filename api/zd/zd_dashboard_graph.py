### This is ZD dashboard graphs blue print
### Date: Sep 3rd, 2015

from flask import Blueprint,g, request
from flask_cors import cross_origin
import json
import datetime
from bson import json_util
from ..lib.data_graphs import data_graph
zd_dashboard_graph = Blueprint('zd_dashboard_graph', __name__, url_prefix='/zd')

@zd_dashboard_graph.route('/get_client_device_data',  methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_client_device_data():
        days='1';
        if request.method == 'POST':
                json_data = request.get_json();
                days=json_data.get("days", "")
                if days=='' or days==None:
                        days='7';
        table_name="ruckus.Zone_Director_Complete_Info";
        column_one="NameAndField"
        column_two="NumberOfClientDevices"
        timestamp_col="Date"
        days=int(days)
        where="1=1"
	convert=""
        return data_graph(tablename=table_name,column_one=column_one,column_two=column_two,timestamp_col=timestamp_col,where_condition=where,days=days,convert=convert)

@zd_dashboard_graph.route('/get_memory_util_data', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_memory_util_data():
        days='1';
        if request.method == 'POST':
                json_data = request.get_json();
                days=json_data.get("days", "")
                if days=='' or days==None:
                        days='7';
        table_name="ruckus.Zone_Director_Complete_Info";
        column_one="NameAndField"
        column_two="UsedPercentage"
        timestamp_col="Date"
        days=int(days)
        where="1=1"
	convert="percent"
        return data_graph(tablename=table_name,column_one=column_one,column_two=column_two,timestamp_col=timestamp_col,where_condition=where,days=days,convert=convert)

@zd_dashboard_graph.route('/get_cpu_data', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_cpu_data():
        days='1';
        if request.method == 'POST':
                json_data = request.get_json();
                days=json_data.get("days", "")
                if days=='' or days==None:
                        days='7';
        table_name="ruckus.Zone_Director_Complete_Info";
        column_one="NameAndField"
        column_two="Cpu"
        timestamp_col="Date"
        days=int(days)
        where="1=1"
	convert=""
        return data_graph(tablename=table_name,column_one=column_one,column_two=column_two,timestamp_col=timestamp_col,where_condition=where,days=days,convert=convert)
 
@zd_dashboard_graph.route('/get_apcount_data', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_apcount_data():
        days='1';
        if request.method == 'POST':
                json_data = request.get_json();
                days=json_data.get("days", "")
                if days=='' or days==None:
                        days='7';
        table_name="ruckus.Zone_Director_Complete_Info";
        column_one="NameAndField"
        column_two="NumberOfAps"
        timestamp_col="Date"
        days=int(days)
        where="1=1"
	convert=""
        return data_graph(tablename=table_name,column_one=column_one,column_two=column_two,timestamp_col=timestamp_col,where_condition=where,days=days,convert=convert)


@zd_dashboard_graph.route('/get_uptime_data', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_uptime_data():
        days='1';
        if request.method == 'POST':
                json_data = request.get_json();
                days=json_data.get("days", "")
                if days=='' or days==None:
                        days='7';
        table_name="ruckus.Zone_Director_Complete_Info";
        column_one="NameAndField"
        column_two="UpTime"
        timestamp_col="Date"
        days=int(days)
        where="1=1"
	convert="uptime"
        return data_graph(tablename=table_name,column_one=column_one,column_two=column_two,timestamp_col=timestamp_col,where_condition=where,days=days,convert=convert )



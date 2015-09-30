### This is SCG Dashboard blue print
### This will respond the jsons regarding scg dashboard such as global config, devices, dataplane, controlplane
### Date: Sep 3rd, 2015

from flask import Blueprint,g, request
from flask_cors import cross_origin
import json
import datetime
from bson import json_util
from ..lib.data_tables import big_table
from ..lib.data_graphs import data_graph
scg_dashboard = Blueprint('scg_dashboard', __name__, url_prefix='/scg')

### End points 
@scg_dashboard.route('/global_config', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def global_config():
	config={}
	config['time']=datetime.datetime.now().strftime("%A %b %d, %Y  %I:%M %p");
	pi_sql="select Pinterval from Settings.polling_interval where Device='SCG'";
	data_pi = g.conn.select_advanced(pi_sql);
	config['pollingInterval']=int(data_pi[0]);
	config['noOfDays']=7;
	lu_sql="SELECT TIMESTAMP FROM Devices ORDER BY TIMESTAMP DESC LIMIT 1";
	data = g.conn.select_advanced(lu_sql);
	config['lastUpdated']=str(data[0]);
	#json_string="{'time':'"+str(config['time'])+"','pollingInterval':'"+str(config['pollingInterval'])+"','noOfDays':'7', 'lastUpdated':'"+str(config['lastUpdated'])+"'}";	
	#return json_string
	return json.dumps(config, default=json_util.default)

@scg_dashboard.route('/get_devices')
@cross_origin()
def get_devices():
	columns=['SCGIP','ClusterName','Role','NoOfControlPlane','NoOfDataPlane','NoOfAPs','NoOfClients','SCGVersion','ControlPlaneSoftwareVersion','DataPlaneSoftwareVersion','Consumed','WiFiControlLicenses','Timestamp']
	device_sql="select "+",".join(columns)+" from Devices";
	result=[];
	data = g.conn.select_advanced(device_sql);
	for row in data:
		row_data=dict(zip(columns, row));
		row_data['NoOfPlanes']=str(row_data['NoOfControlPlane'])+"/"+str(row_data['NoOfDataPlane']);
		row_data['WiFiControlLicenses']=str(row_data['Consumed'])+"/"+str(row_data['WiFiControlLicenses']);
		scgip=row_data['SCGIP'];
		### number of connected, disconnected and all APs
		noOfDisConAp=g.conn.select_advanced("SELECT SUM( DisconnectedAP ) FROM `ZoneDetails` WHERE SCGIP =  '"+scgip+"'");
		noOfDisConAp=noOfDisConAp[0];
		if noOfDisConAp==None:
			noOfDisConAp='0';
		noOfDisConAp=int(noOfDisConAp);
		totalAP=noOfDisConAp+int(row_data['NoOfAPs']);
		row_data['NoOfAPs']=str(totalAP)+"("+str(row_data['NoOfAPs'])+"/"+str(noOfDisConAp)+")";
		#row_data['Timestamp']=str(row_data['Timestamp']);
		follower=g.conn.select_advanced("select ManagementIP from ControlPlaneDetails where SCGIP='"+scgip+"' and Role='Follower'");
		row_data['Follower']=",".join(follower);
  		result.append(row_data);
	return json.dumps(result, default=json_util.default)



@scg_dashboard.route('/get_control_plane', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_control_plane():
	scgip='';
	if request.method == 'POST':
     		json_data = request.get_json()
		scgip=json_data.get("scg_ip", "")
	planes={}
	columns=['ControlPlaneName','Model','SerialNumber','Description','Firmware','ManagementIP','ClusterIP','ControlIP','Role','NumberOfPorts','NumberOfAPs','NumberOfClients','CPUPercentage_Max_Min_Avg','MemoryPercentage_Max_Min_Avg','DiskUsage_Max_Min_Avg','Status','Uptime'];
	cplane_sql="select "+",".join(columns)+" from ControlPlaneDetails where SCGIP='"+scgip+"'";
	result=[]
	data = g.conn.select_advanced(cplane_sql);
        for row in data:
		cd_plane={}
		cplane=row[0];
		dpcols=['DataPlaneName','IPAddress','MACAddress','Model','SerialNumber','Firmware','ManagedBy','NumberOfTunnels','Status','Uptime'];
		dp_sql="select "+",".join(dpcols)+" from DataPlaneDetails where SCGIP='"+scgip+"' and ControlPlaneName='"+cplane+"'";
		ddata = g.conn.select_advanced(dp_sql);
		dplane_list=[]
		for dp in ddata:
			dplane_list.append(dict(zip(dpcols, dp)))
                cplane=dict(zip(columns, row))
		for key in cplane:
			if cplane[key]==None:
				cplane[key]="null";
		cplane['cpu_min']=cplane['CPUPercentage_Max_Min_Avg'];
		cplane['memory_min']=cplane['MemoryPercentage_Max_Min_Avg'];
		cplane['disk_min']=cplane['DiskUsage_Max_Min_Avg'];
		cd_plane['cplane']=cplane
		cd_plane['dplane']=dplane_list
		result.append(cd_plane);
        return json.dumps(result, default=json_util.default)
	

@scg_dashboard.route('/get_zone_details', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_zone_details():
        page=1;
        limit=10;
        table="ZoneDetails";
        where="1=1";
        columns=['ZoneName','Description','ManagementDomain','CreatedOn','CreatedBy','NumberofWLANs','NumberofAPs','NumberofClients','TunnelType']
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
	        zone_name="";
        	description="";
        	management_domain="";
        	created_date="";
        	created_by="";
        	number_wlan="";
        	number_ap="";
        	number_clients="";
        	tunnel_type="";
                zone_name=json_data.get("zone_name","")
                description=json_data.get("description","")
                management_domain=json_data.get("management_domain","")
                created_date=json_data.get("created_date","")
                created_by=json_data.get("created_by","")
                number_wlan=json_data.get("number_wlan","")
                number_ap=json_data.get("number_ap","")
                number_clients=json_data.get("number_clients","")
                tunnel_type=json_data.get("tunnel_type","")
        	if zone_name!='' and zone_name!=None:
			sparams['ZoneName']=zone_name;
        	if description!='' and description!=None:
			sparams['Description']=description;
        	if management_domain!='' and management_domain!=None:
			sparams['ManagementDomain']=management_domain;
        	if created_date!='' and created_date!=None:
			sparams['CreatedOn']=created_date;
        	if created_by!='' and created_by!=None:
			sparams['CreatedBy']=created_by;
        	if number_wlan!='' and number_wlan!=None:
			sparams['NumberofWLANs']=number_wlan;
        	if number_ap!='' and number_ap!=None:
			sparams['NumberofAPs']=number_ap;
        	if number_clients!='' and number_clients!=None:
			sparams['NumberofClients']=number_clients;
        	if tunnel_type!='' and tunnel_type!=None:
			sparams['TunnelType']=tunnel_type;
		### Where clause
		scg_ip="";
		scg_ip=json_data.get("scg_ip", "")
		if scg_ip!='' and scg_ip!=None:
			where = " SCGIP='"+scg_ip+"'"
        return big_table(tablename=table,where_condition=where,limit=limit,page=page,columns=columns,search=sparams);

@scg_dashboard.route('/get_critical_activities', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_critical_activities():
        page=1;
        limit=10;
        table="CriticalActivities";
        where="1=1";
        columns=['Timestamp','SCGName','Content']
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
                scg_name=""
                scg_log="";
                timestamp=""
                scg_name=json_data.get("scg_name","")
                scg_log=json_data.get("scg_log","")
                timestamp=json_data.get("timestamp","")
                if scg_name!='' and scg_name!=None:
                        sparams['SCGName']=scg_name;
                if scg_log!='' and scg_log!=None:
                        sparams['Content']=scg_log;
                if timestamp!='' and timestamp!=None:
                        sparams['Timestamp']=convert_timestamp(timestamp);
        return big_table(tablename=table,where_condition=where,limit=limit,page=page,columns=columns,search=sparams);

@scg_dashboard.route('/get_ap_activities', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_ap_activities():
        page=1;
	limit=10;
	table="APActivities";
	where="1=1";
        columns=['Timestamp','SCGName','Activity']
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
                scg_name=""
                scg_log="";
                timestamp=""
                scg_name=json_data.get("scg_name","")
                scg_log=json_data.get("scg_log","")
                timestamp=json_data.get("timestamp","")
		if scg_name!='' and scg_name!=None:
			sparams['SCGName']=scg_name;
		if scg_log!='' and scg_log!=None:
			sparams['Activity']=scg_log;
		if timestamp!='' and timestamp!=None:
			sparams['Timestamp']=convert_timestamp(timestamp);
	return big_table(tablename=table,where_condition=where,limit=limit,page=page,columns=columns,search=sparams);



@scg_dashboard.route('/get_ap_activities_full', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_ap_activities_full():
        columns=['Timestamp','SCGName','Activity']
        ap_act_sql="select Timestamp,SCGName,Activity from APActivities";
        result=[];
        data = g.conn.select_advanced(ap_act_sql);
        for row in data:
                result.append(dict(zip(columns, row)))
        count_sql="select count(*) from APActivities";
        cdata = g.conn.select_advanced(count_sql);
        count=cdata[0];
        json_data={'count':count, 'items':result}

        return json.dumps(json_data, default=json_util.default)


### Popup window tables
@scg_dashboard.route('/get_wlans', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_wlans():
        page=1;
        limit=10;
        table="WlanDetails_SNMP_Complete_Info";
        where="1=1";
        columns=['Zone','SSID','Clients','RXMBytes','TXMBytes','AuthType','Domain','TimeStamp']
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
                zone="";
                SSID="";
                Clients="";
                RXMBytes="";
                TXMBytes="";
                AuthType="";
                Domain="";
                TimeStamp="";
                zone=json_data.get("zone","")
                SSID=json_data.get("SSID","")
                Clients=json_data.get("Clients","")
                RXMBytes=json_data.get("RXMBytes","")
                TXMBytes=json_data.get("TXMBytes","")
                AuthType=json_data.get("AuthType","")
                Domain=json_data.get("Domain","")
                TimeStamp=json_data.get("TimeStamp","")
                if zone!='' and zone!=None:
                        sparams['Zone']=zone;
                if SSID!='' and SSID!=None:
                        sparams['SSID']=SSID;
                if Clients!='' and Clients!=None:
                        sparams['Clients']=Clients;
                if RXMBytes!='' and RXMBytes!=None:
                        sparams['RXMBytes']=RXMBytes;
                if TXMBytes!='' and TXMBytes!=None:
                        sparams['TXMBytes']=TXMBytes;
                if AuthType!='' and AuthType!=None:
                        sparams['AuthType']=AuthType;
                if Domain!='' and Domain!=None:
                        sparams['Domain']=Domain;
                if TimeStamp!='' and TimeStamp!=None:
                        sparams['Timestamp']=convert_timestamp(timestamp);
                ### Where clause
                scg_ip="";
                scg_ip=json_data.get("scg_ip", "")
                if scg_ip!='' and scg_ip!=None:
                        where = " SCGIP='"+scg_ip+"'"
        return big_table(tablename=table,where_condition=where,limit=limit,page=page,columns=columns,search=sparams);


@scg_dashboard.route('/get_apdetails', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_apdetails():
        page=1;
        limit=10;
        table="APDetails";
        where="1=1";
        columns=['ControlPlane','APMACAddress','APName','APZone','ConnectionStatus','Uptime','SerialNumber','FirmwareVersion','IPAddress','ExternalIPAddress','Model','MeshRoleHops','ConfigurationStatus','DataPlane','RXMBytes','TXMBytes','TotalMBytes','TimeStamp']
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
                ControlPlane="";
                APMACAddress="";
                APName="";
                ConnectionStatus="";
                Uptime="";
                SerialNumber="";
                FirmwareVersion="";
                IPAddress="";
                ExternalIPAddress="";
                Model="";
                ControlPlane=json_data.get("ControlPlane","")
                APMACAddress=json_data.get("APMACAddress","")
                APName=json_data.get("APName","")
                ConnectionStatus=json_data.get("ConnectionStatus","")
                Uptime=json_data.get("Uptime","")
                SerialNumber=json_data.get("SerialNumber","")
                FirmwareVersion=json_data.get("FirmwareVersion","")
                IPAddress=json_data.get("IPAddress","")
                ExternalIPAddress=json_data.get("ExternalIPAddress","")
                Model=json_data.get("Model","")
                MeshRoleHops=json_data.get("MeshRoleHops","")
                ConfigurationStatus=json_data.get("ConfigurationStatus","")
                DataPlane=json_data.get("DataPlane","")
                RXMBytes=json_data.get("RXMBytes","")
                TXMBytes=json_data.get("TXMBytes","")
                TotalMBytes=json_data.get("TotalMBytes","")
                TimeStamp=json_data.get("TimeStamp","")
                if ControlPlane!='' and ControlPlane!=None:
                        sparams['ControlPlane']=ControlPlane;
                if APMACAddress!='' and APMACAddress!=None:
                        sparams['APMACAddress']=APMACAddress;
                if APName!='' and APName!=None:
                        sparams['APName']=APName;
                if ConnectionStatus!='' and ConnectionStatus!=None:
                        sparams['ConnectionStatus']=ConnectionStatus;
                if Uptime!='' and Uptime!=None:
                        sparams['Uptime']=Uptime;
                if SerialNumber!='' and SerialNumber!=None:
                        sparams['SerialNumber']=SerialNumber;
                if FirmwareVersion!='' and FirmwareVersion!=None:
                        sparams['FirmwareVersion']=FirmwareVersion;
                if IPAddress!='' and IPAddress!=None:
                        sparams['IPAddress']=IPAddress;
                if ExternalIPAddress!='' and ExternalIPAddress!=None:
                        sparams['ExternalIPAddress']=ExternalIPAddress;
                if Model!='' and Model!=None:
                        sparams['Model']=Model;
                if MeshRoleHops!='' and MeshRoleHops!=None:
                        sparams['MeshRoleHops']=MeshRoleHops;
                if ConfigurationStatus!='' and ConfigurationStatus!=None:
                        sparams['ConfigurationStatus']=ConfigurationStatus;
                if DataPlane!='' and DataPlane!=None:
                        sparams['DataPlane']=DataPlane;
                if RXMBytes!='' and RXMBytes!=None:
                        sparams['RXMBytes']=RXMBytes;
                if TXMBytes!='' and TXMBytes!=None:
                        sparams['TXMBytes']=TXMBytes;
                if TotalMBytes!='' and TotalMBytes!=None:
                        sparams['TotalMBytes']=TotalMBytes;
                if TimeStamp!='' and TimeStamp!=None:
                        sparams['Timestamp']=convert_timestamp(timestamp);
                ### Where clause
                scg_ip="";
                scg_ip=json_data.get("scg_ip", "")
                if scg_ip!='' and scg_ip!=None:
                        where = " SCGIP='"+scg_ip+"'"
        return big_table(tablename=table,where_condition=where,limit=limit,page=page,columns=columns,search=sparams);



@scg_dashboard.route('/get_apactivities', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_zone_apactivities():
        page=1;
        limit=10;
        table="APActivities";
        where="1=1";
        columns=['Timestamp','SCGName','Activity']
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
                management_domain="";
                Timestamp=json_data.get("Timestamp","")
                SCGName=json_data.get("SCGName","")
                Activity=json_data.get("Activity","")
                if SCGName!='' and SCGName!=None:
                        sparams['SCGName']=SCGName;
                if Activity!='' and Activity!=None:
                        sparams['Activity']=Activity;
                if TimeStamp!='' and TimeStamp!=None:
                        sparams['Timestamp']=convert_timestamp(timestamp);
                ### Where clause
                scg_ip="";
                scg_ip=json_data.get("scg_ip", "")
                if scg_ip!='' and scg_ip!=None:
                        where = " SCGIP='"+scg_ip+"'"
        return big_table(tablename=table,where_condition=where,limit=limit,page=page,columns=columns,search=sparams);

### End points for Graphs

@scg_dashboard.route('/get_client_device_data',  methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_client_device_data():
        days='7';
        if request.method == 'POST':
                json_data = request.get_json();
                days=json_data.get("days", "")
		if days=='' or days==None:
			days='7';
        table_name="DevicesCompleteInfo";
        column_one="ScgIP"
        column_two="NoOfClients"
        timestamp_col="Timestamp"
        days=int(days)
        where="1=1"
	convert=""
        return data_graph(tablename=table_name,column_one=column_one,column_two=column_two,timestamp_col=timestamp_col,where_condition=where,days=days,convert=convert)
		
@scg_dashboard.route('/get_ap_device_data', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_ap_device_data():
        days='7';
        if request.method == 'POST':
                json_data = request.get_json();
                days=json_data.get("days", "")
                if days=='' or days==None:
                        days='7';
        table_name="DevicesCompleteInfo";
        column_one="ScgIP"
        column_two="NoOfAPs"
        timestamp_col="Timestamp"
        days=int(days)
        where="1=1"
	convert=""
        return data_graph(tablename=table_name,column_one=column_one,column_two=column_two,timestamp_col=timestamp_col,where_condition=where,days=days,convert=convert)


@scg_dashboard.route('/get_tunnel_graph_data', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_tunnel_graph_data():
        scgip='';
	days='12'
        if request.method == 'POST':
                json_data = request.get_json();
                scgip=json_data.get("scg_ip", "")
		days=json_data.get("days", "")
	if days=='' or days==None:
		days='7'
        #if scgip=='scgip':
        #        scg_sql="SELECT SCGIP from Devices limit 1";
        #        scg_d=g.conn.select_advanced(scg_sql);
        #        scgip=scg_d[0];
	control_planes=[]
        table_name="DataPlaneDetailsCompleteInfo";
        column_one="DataPlaneName"
        column_two="NumberOfTunnels"
        timestamp_col="Timestamp"
        days=int(days)
	convert=""
        cplane_sql="SELECT `ControlPlaneName` FROM `ControlPlaneDetails` where `SCGIP`='"+scgip+"' ";
        cplane_d=g.conn.select_advanced(cplane_sql);
	for cplane in cplane_d:
        	where="ControlPlaneName='"+cplane+"' and SCGIP='"+scgip+"' and DataPlaneName!=''"
        	data= data_graph(tablename=table_name,column_one=column_one,column_two=column_two,timestamp_col=timestamp_col,where_condition=where,days=days,convert=convert)

		json_string=' { "cplane_name": "'+cplane+'", "data": [ '+data+' ] } ';
        	control_planes.append(json_string)
	result="["+",".join(control_planes)+"]"
	return result
	
@scg_dashboard.route('/get_cplane_uptime_data', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_cplane_uptime_data():
        scgip='';
        days='7';
        if request.method == 'POST':
                json_data = request.get_json();
		scgip=json_data.get("scg_ip","")
                days=json_data.get("days", "")
                if days=='' or days==None:
                        days='7';
        table_name="ControlPlaneDetailsCompleteInfo";
        column_one="ControlPlaneName"
        column_two="Uptime"
        timestamp_col="TimeStamp"
        days=int(days)
        where="SCGIP='"+scgip+"'"
	convert="uptime"
        return data_graph(tablename=table_name,column_one=column_one,column_two=column_two,timestamp_col=timestamp_col,where_condition=where,days=days,convert=convert)

@scg_dashboard.route('/get_dplane_uptime_data', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_dplane_uptime_data():
        scgip='';
	days='7'
        if request.method == 'POST':
                json_data = request.get_json();
                scgip=json_data.get("scg_ip", "")
                days=json_data.get("days", "")
                if days=='' or days==None:
                        days='7';
        control_planes=[]
        table_name="DataPlaneDetailsCompleteInfo";
        column_one="DataPlaneName"
        column_two="Uptime"
        timestamp_col="Timestamp"
        days=int(days)
	convert="uptime"
        cplane_sql="SELECT `ControlPlaneName` FROM `ControlPlaneDetails` where `SCGIP`='"+scgip+"' ";
        cplane_d=g.conn.select_advanced(cplane_sql);
        for cplane in cplane_d:
                where="ControlPlaneName='"+cplane+"' and SCGIP='"+scgip+"' and DataPlaneName!=''"
                data= data_graph(tablename=table_name,column_one=column_one,column_two=column_two,timestamp_col=timestamp_col,where_condition=where,days=days,convert=convert)

                json_string=' { "cplane_name": "'+cplane+'", "data": [ '+data+' ] } ';
                control_planes.append(json_string)
        result="["+",".join(control_planes)+"]"
        return result


def convert_timestamp(search_time):
	print search_time
        try:
                dtime=datetime.datetime.strptime(search_time,"%b %d, %Y %H:%M");
		print dtime
                search_time=dtime.strftime("%Y-%m-%d %H:%M")
        except Exception:
                pass
	return str(search_time)

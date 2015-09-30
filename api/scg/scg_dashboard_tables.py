###WLANS complete tables 
###23 sept 2015

from flask import Blueprint,g, request
from flask_cors import cross_origin
import json
import datetime
from bson import json_util
from ..lib.data_tables import big_table
scg_dashboard_tables =  Blueprint('scg_dashboard_tables', __name__, url_prefix='/scg')


@scg_dashboard_tables.route('/no_of_wlans', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def no_of_wlans():
        start=1;
        limit=20;
        page=1;
        scg_name=""
        scg_log="";
        timestamp=""
        columns=['Zone','SSID','Clients','RXMBytes','TXMBytes','AuthType','Domain','TimeStamp']
        if request.method == 'POST':
                json_data = request.get_json();
                limit=json_data.get("limit", "")
                page=json_data.get("page","")
               # scg_name=json_data.get("scg_name","")
                scg_log=json_data.get("scg_log","")
                timestamp=json_data.get("timestamp","")
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
        count_sql="select count(*) from WlanDetails_SNMP_Complete_Info";
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

        ap_act_sql="select Zone,SSID,Clients,RXMBytes,TXMBytes,AuthType,Domain,Timestamp from WlanDetails_SNMP_Complete_Info "+where_clause+" order by Timestamp desc limit "+str(start)+","+str(limit);

	print "\n"+ap_act_sql+"\n"
        result=[];
        data = g.conn.select_advanced(ap_act_sql);
        for row in data:
                #print row
                result.append(dict(zip(columns, row)))
        json_data={'count':count, 'items':result, 'filter_count':fcount }
        print "\n\n"
        return json.dumps(json_data, default=json_util.default)


@scg_dashboard_tables.route('/no_of_apdetails', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def no_of_apdetails():
        start=1;
        limit=20;
        page=1;
        scg_name=""
        scg_log="";
        timestamp=""
	columns=['ControlPlane','APMACAddress','APName','APZone','ConnectionStatus','Uptime','SerialNumber','FirmwareVersion','IPAddress','ExternalIPAddress','Model','MeshRoleHops','ConfigurationStatus','DataPlane','RXMBytes','TXMBytes','TotalMBytes','TimeStamp']
        if request.method == 'POST':
                json_data = request.get_json();
                limit=json_data.get("limit", "")
                page=json_data.get("page","")
               # scg_name=json_data.get("scg_name","")
                scg_log=json_data.get("scg_log","")
                timestamp=json_data.get("timestamp","")
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

	if timestamp!='' and timestamp!=None:
                timestamp=convert_timestamp(timestamp);
                where_clause=where_clause+" Timestamp like '%%"+timestamp+"%%' and"
                wh=1;
        if wh==1:
                where_clause=where_clause[:-4]
        else:
                where_clause=""
        count_sql="select count(*) from APDetails";
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
	
	ap_act_sql="select ControlPlane,APMACAddress,APName,APZone,ConnectionStatus,Uptime,SerialNumber,FirmwareVersion,IPAddress,ExternalIPAddress,Model,MeshRoleHops,ConfigurationStatus,DataPlane,RXMBytes,TXMBytes,TotalMBytes,TimeStamp from APDetails "+where_clause+" order by Timestamp desc limit "+str(start)+","+str(limit);

        print "\n"+ap_act_sql+"\n"
        result=[];
        data = g.conn.select_advanced(ap_act_sql);
        for row in data:
                #print row
                result.append(dict(zip(columns, row)))
        json_data={'count':count, 'items':result, 'filter_count':fcount }
        print "\n\n"
        return json.dumps(json_data, default=json_util.default)


@scg_dashboard_tables.route('/no_of_apactivities', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def no_of_apactivities():
        start=1;
        limit=20;
        page=1;
        scg_name=""
        scg_log="";
        timestamp=""
        columns=['Timestamp','SCGName','Activity']
        if request.method == 'POST':
                json_data = request.get_json();
                limit=json_data.get("limit", "")
                page=json_data.get("page","")
               # scg_name=json_data.get("scg_name","")
                scg_log=json_data.get("scg_log","")
                timestamp=json_data.get("timestamp","")
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
	if timestamp!='' and timestamp!=None:
                timestamp=convert_timestamp(timestamp);
                where_clause=where_clause+" Timestamp like '%%"+timestamp+"%%' and"
                wh=1;
        if wh==1:
                where_clause=where_clause[:-4]
        else:
                where_clause=""
        count_sql="select count(*) from APActivities";
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

        ap_act_sql="select Timestamp,SCGName,Activity from APActivities "+where_clause+" order by Timestamp desc limit "+str(start)+","+str(limit);

        print "\n"+ap_act_sql+"\n"
        result=[];
        data = g.conn.select_advanced(ap_act_sql);
        for row in data:
                #print row
                result.append(dict(zip(columns, row)))
        json_data={'count':count, 'items':result, 'filter_count':fcount }
        print "\n\n"
        return json.dumps(json_data, default=json_util.default)




@scg_dashboard_tables.route('/get_wlans', methods=['GET', 'POST', 'OPTIONS'])
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

def convert_timestamp(search_time):
        print search_time
        try:
                dtime=datetime.datetime.strptime(search_time,"%b %d, %Y %H:%M");
                print dtime
                search_time=dtime.strftime("%Y-%m-%d %H:%M")
        except Exception:
                pass
        return str(search_time)




@scg_dashboard_tables.route('/get_apdetails', methods=['GET', 'POST', 'OPTIONS'])
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
                        sparams['TimeStamp']=TimeStamp;
		if TimeStamp!='' and TimeStamp!=None:
                        sparams['Timestamp']=convert_timestamp(timestamp);


                ### Where clause
                scg_ip="";
                scg_ip=json_data.get("scg_ip", "")
                if scg_ip!='' and scg_ip!=None:
                        where = " SCGIP='"+scg_ip+"'"
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


@scg_dashboard_tables.route('/get_apactivities', methods=['GET', 'POST', 'OPTIONS'])
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

def convert_timestamp(search_time):
        print search_time
        try:
                dtime=datetime.datetime.strptime(search_time,"%b %d, %Y %H:%M");
                print dtime
                search_time=dtime.strftime("%Y-%m-%d %H:%M")
        except Exception:
                pass
        return str(search_time)








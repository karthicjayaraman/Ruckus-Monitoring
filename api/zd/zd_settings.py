### This is Zone Director Settings blue print
### This will respond the jsons regarding scg settings such as Email, FTP, MIB, log alert
### Date: Sep 29th, 2015
### Originated By Hariharaselvam Balasubramanian (4470)

from flask import Blueprint,g, request, send_from_directory
from flask_cors import cross_origin
from werkzeug import secure_filename
import json
import pexpect
import os
from bson import json_util
zd_settings = Blueprint('zd_settings', __name__, url_prefix='/zd')



### Email methods starts here ###

### Get Email settings
@zd_settings.route('/get_email_setting', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_email_setting():
	smtp_sql="select * from Settings.EmailSetting where SMTPGateway != ''";
	smtp_data=g.conn.select_advanced(smtp_sql);
	smtp_hash={};
	smtp_hash['smtpgateway']=smtp_data[0][1];
	smtp_hash['port']=smtp_data[0][2];
	smtp_hash['sender_id']=smtp_data[0][3];
	smtp_hash['password']=smtp_data[0][4];
	reciever_sql="select ID, ReceiverId, PhoneNumber from Settings.EmailSetting where Device='SCG'";
	email_data=g.conn.select_advanced(reciever_sql);
	columns=['ID', 'ReceiverId', 'PhoneNumber']
	emails=[]
	for row in email_data:
		emails.append(dict(zip(columns, row))) 
	json_data={'smtp':smtp_hash,'emails':emails}
	return json.dumps(json_data, default=json_util.default)

### Update Email Gateway informations
@zd_settings.route('/update_gateway', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def update_gateway():
        gateway=""
        port=""
        id=''
        if request.method == 'POST':
                json_data = request.get_json()
                gateway=json_data.get("gateway", "")
                port=json_data.get("port", "")
                id=json_data.get("id", "")
        if id=='':
                id=0;
        id=int(id)
        conditional_query='ID = %s';
        result= g.conn.update('Settings.EmailSetting', conditional_query, id, SMTPGateway=gateway, Port=port)
        json_data={'rows_updated':result}
        return json.dumps(json_data, default=json_util.default)
	
### Update recievers
@zd_settings.route('/update_recievers', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def update_recievers():
        email=""
        phone=""
        id=''
        if request.method == 'POST':
                json_data = request.get_json()
                email=json_data.get("email", "")
                phone=json_data.get("phone", "")
                id=json_data.get("id", "")
        if id=='':
                id=0;
        id=int(id)
        conditional_query='ID = %s';
        result= g.conn.update('Settings.EmailSetting', conditional_query, id, ReceiverID=email, PhoneNumber=phone)
        json_data={'rows_updated':result}
        return json.dumps(json_data, default=json_util.default)

### Add Recievers
@zd_settings.route('/add_recievers', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def add_recievers():
        email=""
        phone=""
        if request.method == 'POST':
                json_data = request.get_json()
                email=json_data.get("email", "")
                phone=json_data.get("phone", "")
        result= g.conn.insert('Settings.EmailSetting', SMTPGateway='', Port='', SenderID='', Password='',  ReceiverID=email, PhoneNumber=phone)
        json_data={'row_inserted':result}
        return json.dumps(json_data, default=json_util.default)

### Delete Recievers
@zd_settings.route('/delete_recievers', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def delete_recievers():
	id=''
        if request.method == 'POST':
                json_data = request.get_json()
	        id=json_data.get("id", "")
        if id=='':
                id=0;
        id=int(id)
        conditional_query='ID = %s';
        result= g.conn.delete('Settings.EmailSetting',conditional_query, id )     
        json_data={'rows_deleted':result}
        return json.dumps(json_data, default=json_util.default)

### Email methods ends here

### ------------------------------------------------------------------------------------- ###

### FTP Settings starts here

@zd_settings.route('/get_ftp_setting', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_ftp_setting():
	pro=pexpect.spawn("/etc/init.d/xinetd status")
	status="unavailable";	
	try:
		pro.expect("is running...")
		status="running";
	except pexpect.EOF:
		pass
	except pexpect.TIMEOUT:
		pass
	except Exception:
		pass
	ftp={"status":status}

	path="/tftpboot"
	files = []
	for file in os.listdir(path):
		if file.endswith('.tar.gz'):
			size=os.path.getsize(path+"/"+file)
			files.append({ "name":file,"size":size})
	ftp["files"]=files;
        return json.dumps(ftp, default=json_util.default)

### FTP settings ends here

### ------------------------------------------------------------------------------------ ###

### Swatch configuration settings starts here

### Swatch Config data for table
@zd_settings.route('/get_swatch_config', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_swatch_config():
	swatch_sql="SELECT * FROM ruckus.SwatchRegex";
	swatch_data=g.conn.select_advanced(swatch_sql);
	columns=['RegexID','RegEx'];
	swatch=[];
	for row in swatch_data:
		swatch.append(dict(zip(columns, row)))
	
        return json.dumps(swatch, default=json_util.default)

### Update Swatch Config Data
@zd_settings.route('/update_swatch', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def update_swatch():
        regex=""
        id=''
        if request.method == 'POST':
                json_data = request.get_json()
                regex=json_data.get("regex", "")
                id=json_data.get("id", "")
        if id=='':
                id=0;
        id=int(id)
        conditional_query='RegexID = %s';
        result= g.conn.update('ruckus.SwatchRegex', conditional_query, id, RegEx=regex)
        json_data={'rows_updated':result}
        return json.dumps(json_data, default=json_util.default)

### Add Swatch
@zd_settings.route('/add_swatch', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def add_swatch():
        regex=""
        if request.method == 'POST':
                json_data = request.get_json()
                regex=json_data.get("regex", "")
        result= g.conn.insert('ruckus.SwatchRegex', RegEx=regex)
        json_data={'row_inserted':result}
        return json.dumps(json_data, default=json_util.default)

### Delete Swatch Config Data
@zd_settings.route('/delete_swatch', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def delete_swatch():
        id=''
        if request.method == 'POST':
                json_data = request.get_json()
                id=json_data.get("id", "")
        if id=='':
                id=0;
        id=int(id)
        conditional_query='RegexID = %s';
        result= g.conn.delete('ruckus.SwatchRegex', conditional_query, id )
        json_data={'rows_deleted':result}
        return json.dumps(json_data, default=json_util.default)

### Swatch Configuration settings ends here

### ----------------------------------------------------------------------------- ###

### Event Configuration settings starts here

### Get Event Config Data
@zd_settings.route('/get_event_config', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_event_config():
        event_sql="SELECT ID, Severity, Regex FROM ruckus.EventSeverity";
        event_data=g.conn.select_advanced(event_sql);
        columns=['ID','Severity','Regex'];
        event=[];
        for row in event_data:
                event.append(dict(zip(columns, row)))        
        return json.dumps(event, default=json_util.default)

### Update Event Config Data
@zd_settings.route('/update_event', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def update_event():
        regex=""
        severity=""
        id=''
        if request.method == 'POST':
                json_data = request.get_json()
                regex=json_data.get("regex", "")
                severity=json_data.get("severity", "")
                id=json_data.get("id", "")
        if id=='':
                id=0;
        id=int(id)
        conditional_query='ID = %s';
        result= g.conn.update('ruckus.EventSeverity', conditional_query, id, Regex=regex, Severity=severity)
        json_data={'rows_updated':result}
        return json.dumps(json_data, default=json_util.default)

### Add Events
@zd_settings.route('/add_events', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def add_events():
        regex=""
        severity=""
        if request.method == 'POST':
                json_data = request.get_json()
                regex=json_data.get("regex", "")
                severity=json_data.get("severity", "")
        result= g.conn.insert('ruckus.EventSeverity', Regex=regex, Severity=severity)
        json_data={'row_inserted':result}
        return json.dumps(json_data, default=json_util.default)

### Delete Event Config
@zd_settings.route('/delete_events', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def delete_events():
        id=''
        if request.method == 'POST':
                json_data = request.get_json()
                id=json_data.get("id", "")
        if id=='':
                id=0;
        id=int(id)
        conditional_query='ID = %s';
        result= g.conn.delete('ruckus.EventSeverity',conditional_query, id )
        json_data={'rows_deleted':result}
        return json.dumps(json_data, default=json_util.default)

### Event Configuration settings ends here

### ----------------------------------------------------------------------------- ###

### Log Alert Configuration settings starts here

### Get Log Alert Config Data
@zd_settings.route('/get_log_alert_config', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_log_alert_config():
        log_sql="SELECT ID, RegEx, Type FROM ruckus.Log_Maintain_Regex";
        log_data=g.conn.select_advanced(log_sql);
        columns=['ID', 'RegEx', 'Type'];
        logs=[];
        for row in log_data:
                logs.append(dict(zip(columns, row)))
        return json.dumps(logs, default=json_util.default)

### Update Log Alert Config Data
@zd_settings.route('/update_log_alert', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def update_log_alert():
        regex=""
        type=""
        id=''
        if request.method == 'POST':
                json_data = request.get_json()
                regex=json_data.get("regex", "")
                type=json_data.get("type", "")
                id=json_data.get("id", "")
        if id=='':
                id=0;
        id=int(id)
        conditional_query='ID = %s';
        result= g.conn.update('ruckus.Log_Maintain_Regex', conditional_query, id, RegEx=regex, Type=type)
        json_data={'rows_updated':result}
        return json.dumps(json_data, default=json_util.default)

### Add log alert setting
@zd_settings.route('/add_log_alerts', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def add_log_alerts():
        regex=""
        type=""
        if request.method == 'POST':
                json_data = request.get_json()
                regex=json_data.get("regex", "")
                type=json_data.get("type", "")
        result= g.conn.insert('ruckus.Log_Maintain_Regex', RegEx=regex, Type=type)
        json_data={'row_inserted':result}
        return json.dumps(json_data, default=json_util.default)

### Delete log alert setting
@zd_settings.route('/delete_log_alert', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def delete_log_alert():
        id=''
        if request.method == 'POST':
                json_data = request.get_json()
                id=json_data.get("id", "")
        if id=='':
                id=0;
        id=int(id)
        conditional_query='ID = %s';
        result= g.conn.delete('ruckus.Log_Maintain_Regex',conditional_query, id )
        json_data={'rows_deleted':result}
        return json.dumps(json_data, default=json_util.default)

### Log Alert Configuration settings ends here

### ------------------------------------------------------------------------------------------- ###

### User MIBs settings starts here

### Get User MIB files list
@zd_settings.route('/get_user_mib', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_user_mib():
	path="/var/www/cgi-bin/RK/mibs/"
	mib_list=[]
	for ver in os.listdir(path):
		for file in os.listdir(path+ver):
			mib={'version':ver}
			mib['filename']=file
			mib['created_time']=os.path.getmtime(path+ver+"/"+file)
			mib['size']=os.path.getsize(path+ver+"/"+file) 
			mib_list.append(mib);		
        return json.dumps(mib_list, default=json_util.default)

### Upload MIB files
@zd_settings.route('/upload_mib_files', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def upload_mib_files():
	path="/var/www/cgi-bin/RK/mibs/"
	version=""
	if request.method == 'POST':
		fileitem = request.files['mib_file']
		json_data = request.get_json()
                version=json_data.get("version", "")
		filename = secure_filename(fileitem.filename)
		fileitem.save(os.path.join(path+version, filename))
		return "{'status': 'success'}"
	else:
		return "{'status': 'fail'}"

### Download MIB file
@zd_settings.route('/download_mib_file', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def download_mib_file():
        path="/var/www/cgi-bin/RK/mibs/"
        version=""
	filename=""
        if request.method == 'POST':
                json_data = request.get_json()
                version=json_data.get("version", "")
		filename=json_data.get("filename", "")
	filepath=path+version
	try:
		return send_from_directory(directory=filepath, filename=filename)
        except Exception:
		return "File not found on the server. Check the filename and version you have passed."

### Delete MIB file
@zd_settings.route('/delete_mib_file', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def delete_mib_file():
        path="/var/www/cgi-bin/RK/mibs/"
        version=""
        filename=""
        if request.method == 'POST':
                json_data = request.get_json()
                version=json_data.get("version", "")
                filename=json_data.get("filename", "")
        filepath=path+version
        try:
		os.remove(path+version+"/"+filename)
                return "File deleted successfully"
        except Exception:
                return "File not found on the server. Check the filename and version you have passed."

### User MIBs settings ends here

### ------------------------------------------------------------------------------------------- ###






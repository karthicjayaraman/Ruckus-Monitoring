### This is SCG logs blue print
### This will respond the jsons regarding scg logs such as global config, add, edit, display
### Date: Sep 9th, 2015



from flask import Blueprint,g, request
from flask_cors import cross_origin
import json
import datetime
import md5
import pexpect
from bson import json_util
ms_user = Blueprint('ms_user', __name__, url_prefix='/user')

@ms_user.route('/login', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def login():
	username=''
	password=''
	result=0;
	if request.method == 'POST':
                json_data = request.get_json();
                username=json_data.get("username", "")
                password=json_data.get("password", "")
	if username=='admin':
		auth_sql = "select password, access from Settings.user_setting where username='"+username+"'";
		auth_data = g.conn.select_advanced(auth_sql);
		encrypted_pass=md5.md5(password).hexdigest();
		if encrypted_pass == auth_data[0]:
			result=1;
	elif username!='':
		server_sql = "select address, accesskey from Settings.Auth_Server where servertype='tacacs'";
		server_data = g.conn.select_advanced(server_sql);
		for data in server_data:
			host=data[0];
			key=data[1];	
			perl_prog="perl tacacs_plus_auth.pl "+host+" "+key+" "+username+" "+password;
			pro=pexpect.spawn(perl_prog);
			try:
                		pro.expect("Result : pass")
                		status="ok";
			except Exception:
				pass
			if status=='ok':
				result=1;
				break;
	json_data={'status':result}
	return json.dumps(json_data, default=json_util.default)
		
					

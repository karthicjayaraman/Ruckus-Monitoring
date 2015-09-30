### This is SCG logs blue print
### This will respond the jsons regarding scg logs such as global config, add, edit, display
### Date: Sep 9th, 2015



from flask import Blueprint,g, request
from flask_cors import cross_origin
import json
import datetime
from bson import json_util
from ..lib.data_tables import big_table
scg_mail_logs = Blueprint('scg_mail_logs', __name__, url_prefix='/scg')

@scg_mail_logs.route('/get_mail_logs', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_mail_logs():
	log_file="/var/www/cgi-bin/SCG/logs/Mail.log";
	fo=file(log_file,"r")
	lines=fo.readlines();
	fo.close();
	json_data=[]
	for line in lines:
		words=line.split(" : ")
		lw={'timestamp':words[0],'content':words[1]}
		json_data.append(lw)
        return json.dumps(json_data, default=json_util.default)





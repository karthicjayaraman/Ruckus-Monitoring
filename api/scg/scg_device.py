### This is SCG Devices blue print
### This will respond the jsons regarding scg devices such as global config, add, edit, display
### Date: Sep 3rd, 2015

from flask import Blueprint,g, request
from flask_cors import cross_origin
import json
from bson import json_util
scg_device = Blueprint('scg_device', __name__, url_prefix='/scg')



@scg_device.route('/get_config_devices', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_config_devices():
        columns=['SCGIP','Model','SerialNumber','SCGVersion','ControlPlaneSoftwareVersion']
        device_sql="select "+",".join(columns)+" from Devices";
        result=[];
        data = g.conn.select_advanced(device_sql);
        for row in data:
                result.append(dict(zip(columns, row)))
        return json.dumps(result, default=json_util.default)




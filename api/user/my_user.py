###user table that produces json output
### Date: Sep 14, 2015


from flask import Blueprint,g, request
from flask_cors import cross_origin
import json
from bson import json_util
user_device = Blueprint('user_device', __name__, url_prefix='/user')



@user_device.route('/get_my_user', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_my_user():
        columns=['username','password','access']
        device_sql="select "+",".join(columns)+" from Settings.user_setting";
        result=[];
        data = g.conn.select_advanced(device_sql);
        for row in data:
                result.append(dict(zip(columns, row)))
        return json.dumps(result, default=json_util.default)


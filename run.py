### Ruckus Monitoring Server
from flask import Flask, render_template, g, redirect
from OpenSSL import SSL

### blue prints
### SCG
from api.scg.scg_dashboard import scg_dashboard
from api.scg.scg_device import scg_device
from api.scg.scg_settings import scg_settings
from api.scg.scg_trends import scg_trends
from api.scg.scg_logs import scg_logs
from api.scg.scg_events import scg_events

from api.scg.scg_mail_logs import scg_mail_logs
from api.scg.scg_dashboard_graph import scg_dashboard_graph

#from api.scg.scg_dashboard_tables import scg_dashboard_tables

### ZD
from api.zd.zd_dashboard import zd_dashboard
from api.zd.zd_dashboard_graph import zd_dashboard_graph
from api.zd.zd_settings import zd_settings
from api.zd.zd_logs import zd_logs
from api.zd.zd_events import zd_events
from api.zd.zd_mail_logs import zd_mail_logs
from api.zd.zd_popup import zd_popup

### User Management
from api.user.ms_user import ms_user
from api.user.my_user import user_device
### library
from api.lib.mysqlclass import MysqlPython
#from api.lib.data_tables import big_table
#app = Flask(__name__)
app = Flask(__name__, static_folder='', static_url_path='')
app.register_blueprint(scg_dashboard)
app.register_blueprint(scg_device)
app.register_blueprint(scg_settings)
app.register_blueprint(scg_trends)
app.register_blueprint(scg_logs)
app.register_blueprint(scg_events)
app.register_blueprint(scg_mail_logs)


app.register_blueprint(ms_user)
app.register_blueprint(user_device)


app.register_blueprint(scg_dashboard_graph)
app.register_blueprint(zd_dashboard)
app.register_blueprint(zd_dashboard_graph)
app.register_blueprint(zd_settings)
app.register_blueprint(zd_logs)
app.register_blueprint(zd_events)
app.register_blueprint(zd_mail_logs)
app.register_blueprint(zd_popup)
#app.register_blueprint(scg_dashboard_tables)


@app.route('/')
def show_home():
	return redirect("index.html", code=302)

@app.before_request
def db_connect():
	#print "Called"
	g.conn = MysqlPython('localhost', 'root', 'mysql123', 'SCG')
	#data = g.conn.select_advanced("select * from Devices")
	#print data

@app.teardown_request
def db_disconnect(exception=None):
	pass
	#g.conn.close()
	#return response

if __name__ == '__main__':
	context = ('/var/www/html/xcloud/cert/ca.crt', '/var/www/html/xcloud/cert/ca.key')
	app.run(host='0.0.0.0', port=5000, ssl_context=context, threaded=True, debug=True)
        #app.run(host="0.0.0.0", debug=True)


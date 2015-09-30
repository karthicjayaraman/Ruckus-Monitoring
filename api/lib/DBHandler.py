from xcloud_api import *
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#from temper import *
from my_worker import *
import boto.ec2
from flask import render_template, current_app
from flask import Blueprint
from flask.ext.paginate import Pagination
from time import gmtime, strptime
import datetime
import traceback
from time import sleep
import boto.dynamodb2
from boto.dynamodb2.exceptions import UnknownFilterTypeError
from boto.dynamodb2.exceptions import ValidationException
from boto.dynamodb2.items import Item
from boto.dynamodb2.table import Table
from boto.dynamodb2.fields import HashKey, RangeKey, KeysOnlyIndex, AllIndex , GlobalAllIndex
from pprint import pprint
import decimal, simplejson
import MySQLdb
import random
from random import randrange
from uuid import uuid4


print "--------------"

print uuid4()

print "-----------------"

class DecimalJSONEncoder(simplejson.JSONEncoder):
	def default(self, o):
		if isinstance(o, decimal.Decimal):
			return str(o)
		return super(DecimalJSONEncoder, self).default(o)

mod = Blueprint('customers', __name__)


try:
	aws_access_key_id = os.environ['OPS_AWS_KEY_ID']
	aws_secret_access_key = os.environ['OPS_AWS_SECRET_KEY']
except KeyError:
	print "Please set the environment variable FOO"


@app.before_request
def db_connect():
	g.conn = MySQLdb.connect(host='localhost',user='root',passwd='root',db='xcloud',use_unicode=True, charset="utf8")
	g.cursor = g.conn.cursor()

@app.teardown_request
def db_disconnect(exception=None):
	g.cursor.close()
	g.conn.close()
	#return response

@app.route('/check_email_availability', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def check_email_availability():
  output = {}
  if request.method == 'POST':
     json_data = request.get_json()
     email = json_data.get("email", "")
     g.cursor.execute("select * from user where email='"+email+ "'")
     data = g.cursor.fetchone()
     if data is None:
         output['status'] = "0" 
     else:
         output['status'] = "1" 
  return json.dumps(output)
    
@app.route('/login', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def login():
  output = {}
  if request.method == 'POST':
      username = request.form['username']
      password = request.form['password']
      g.cursor.execute("select * from user where email='"+username+ "'and password='"+password+"'")
      data = g.cursor.fetchone()
      #data = xcloud_db.DB_fetchone()
      print data
      if data is None:
          status = "4"
          output['status'] = "4"
      else:
      	  print "new sesssion Created",uuid4()
      	  session['uid'] = str(uuid4())
          session['username'] = username
          session['userid'] = data[0]
          session['logged_in'] = data[1]+data[2]
          output['uid'] = session['uid']
          output['status'] = "0"
          output['role'] = data[5]
          output['fname'] = data[1]
          output['lname'] = data[2]
          status = "0"
      #print username
      #print password
  #output = {"username" : username,"password":password}
  #output = {"status":status}
  return json.dumps(output)

@app.route('/check_session_data', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def check_session_data():
	try:
		if(session['uid']!=""):
			status = 0
		else:
			status = 1
	except KeyError:
		status = 1
	return str(status)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['username'] = None
    session.clear()
    output = {}
    output['result'] = 'success'
    return json.dumps(output)


@app.route('/register', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def register():
  output = {}
  error_msg = {}
  if request.method == 'POST':
     json_data = request.get_json()
     fname = json_data.get("fname", "")
     lname = json_data.get("lname", "")  
     email = json_data.get("email", "")
     role = json_data.get("role", "")
     password = 'ruckus123'
     sta = "0"
     g.cursor.execute("select * from user where email='"+email+ "'")
     data = g.cursor.fetchone()
     if data is None:
         g.cursor.execute("insert into user set first_name='"+fname+"',last_name='"+lname+"',email='"+email+"',password='"+password+"',role='"+role+"',created_at=now()")
         g.conn.commit()
         output = {"status":"0"}
     else:
         output = {"status":"1"}
  return json.dumps(output)


@app.route('/all_user', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def all_user():
  output = {}
  g.cursor.execute("select id,first_name,last_name,email,role from user where id!='1' order by id desc")
  data = g.cursor.fetchall()
  output = {"status" : "up"}
  return json.dumps(data)

@app.route('/user_info', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def user_info():
  output = {}
  if request.method == 'POST':
      json_data = request.get_json()
      user_id = json_data.get("id", "")
      g.cursor.execute("select id,first_name,last_name,email,status,role from user where id='"+user_id+"'")
      data = g.cursor.fetchone()
      print data
      output = {"status" : "up"}
  return json.dumps(data)

@app.route('/update_user', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def update_user():
  output = {}
  if request.method == 'POST':
      json_data = request.get_json()
      user_id = json_data.get("id", "")
      fname = json_data.get("fname", "")
      lname = json_data.get("lname", "")  
      email = json_data.get("email", "")
      role = json_data.get("role", "")
      if role is None:
          g.cursor.execute("update user set first_name='"+fname+"',last_name='"+lname+"',email='"+email+"' where id='"+user_id+"'")
      else:
          g.cursor.execute("update user set first_name='"+fname+"',last_name='"+lname+"',email='"+email+"',role='"+role+"' where id='"+user_id+"'") 
      g.conn.commit()
      data = g.cursor.fetchone()
      print data
      output = {"status" : "up"}
  return json.dumps(output)


@app.route('/delete_user', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def delete_user():
  output = {}
  if request.method == 'POST':
      json_data = request.get_json()
      user_id = str(json_data.get("id", ""))
      print user_id
      g.cursor.execute("delete from user where id='"+user_id+"'")
      g.conn.commit()
      output = {"status" : "Deleted"}
  return json.dumps(output)

@app.route('/get_testdata', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_testdata():
  output = []
  g.cursor.execute("select testdata from xcloud_testdata where id=1")
  response = g.cursor.fetchall()
  print response
  return response

tmp_output = {}

tmp_instance = []

def get_ec2_instances(region):
	
	tmp_total = {}
	tmp_output = {}
	tmp_info = []
	ec2_conn = boto.ec2.connect_to_region(region)
	reservations = ec2_conn.get_all_reservations()
	#print len(reservations)
	tmp_total['total'] = len(reservations)
	if(len(reservations) > 0):
		for x in reservations:
			tmp_output = {}
			#pprint(x.instances[0].__dict__)
			tmp_output['instance'] = x.instances[0].tags['Name']
			tmp_output['ip_address'] = x.instances[0].ip_address
			tmp_output['architecture'] = x.instances[0].architecture
			tmp_output['instance_type'] = x.instances[0].instance_type
			tmp_output['key_name'] = x.instances[0].key_name
			tmp_info.append(tmp_output)
	return json.dumps(tmp_info)
	#return json.dumps(tmp_output)


@app.route('/get_aws_instance', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_aws_instance():
	output = []
	if request.method == 'POST':
		json_data = request.get_json()
		region = str(json_data.get("region", ""))
		output = get_ec2_instances(region)
		return output

@app.route('/aws_instance', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def aws_instance():
	sql="SELECT region.region_id,region.region_name,xcloud_instance_info.* FROM region INNER JOIN xcloud_instance_info ON region.id=xcloud_instance_info.region_id;"
	result=[]
	try:
		g.cursor.execute(sql)
		results = g.cursor.fetchall()
		temp=[]
		for row in results:
			if int(row[3]) not in temp:
				temp.append(int(row[3]))
		for i in temp:
			n = 0
			region={}
			for row in results:
				g.cursor.execute("select response from xcloud_new_service where instance_id='"+str(row[2])+"'")
				r = g.cursor.fetchone()
				if i==int(row[3]) and n==0:
					instance_info={}
					region["id"]=int(row[3])
					region["region_id"]=row[0]
					region["region_name"]=row[1]
					region["instance_info"]=[]
					instance_info["id"]=int(row[2])
					instance_info["instance_name"]=row[4]
					instance_info["ip_address"]=row[5]
					instance_info["instance_type"]=row[6]
					instance_info["keyname"]=row[7]
					instance_info["architecture"]=row[8]
					instance_info["api_status"]= str(r[0])
					region["instance_info"].append(instance_info)
					n=n+1
				elif i==int(row[3]):
					instance_info={}
					instance_info["id"]=int(row[2])
					instance_info["instance_name"]=row[4]
					instance_info["ip_address"]=row[5]
					instance_info["instance_type"]=row[6]
					instance_info["keyname"]=row[7]
					instance_info["api_status"]= str(r[0])
					instance_info["architecture"]=row[8]
					region["instance_info"].append(instance_info)
			result.append(region)
			n=0
	except:
		print "Error: unable to fecth data"
	return json.dumps(result)

'''
@app.route('/aws_instance', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def aws_instance():
	output = {}
	info = []
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("select region.region_id,region.region_name,xcloud_instance_info.* from region inner join xcloud_instance_info on region.id=xcloud_instance_info.region_id")
	data = cursor.fetchall()
	dd = {}
	for row in data:
		#print row
		tmp = {}
		ss = {}
		ipadd = []
		id1 = str(row[3])
		if dd.get(id1):
			tmp = dd.get(id1)
			ipadd = tmp["instance_info"]
		else:
			print id1
			dd[id1] = tmp
			tmp["instance_info"] = ipadd
		cursor.execute("select response from xcloud_new_service where instance_id='"+str(row[2])+"'")
		r = cursor.fetchone()
		tmp["id"] = row[3]
		tmp["region_id"] = row[0]
		tmp["region_name"] = row[1]
		ss = {"id":row[2],"instance_name":row[4],"ip_address":row[5],"instance_type":row[6],"key_name":row[7],"architecture":row[8],"api_status":str(r[0])}
		ipadd.append(ss)
		##info.append(tmp)
	#print info
	#print dd
	return json.dumps(dd)
'''

def pagination():

    start = 0

    total = 158

    limit = 50

    static_limit = 50

    b = total / limit

    c = total % limit


    for num in range(start,b):
    #print num
        print "https://api.stormpath.com/v1/applications/36i2nT8zqeSvSjOJp3Rz1Y/accounts?offset="+str(start)+"&limit="+str(limit)
        start = limit+1
        limit = limit + static_limit

    if(c!=0):
        print "https://api.stormpath.com/v1/applications/36i2nT8zqeSvSjOJp3Rz1Y/accounts?offset="+str(start)+"&limit="+str(total)


@app.route('/aws_test', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def aws_test():
	output = {}
	try:
		r = requests.get('https://api.stormpath.com/v1/applications/36i2nT8zqeSvSjOJp3Rz1Y/accounts?offset=0&limit=1', auth=('D0XWX5WA2LEK23RMOJCW4WCVX', 'TaZArb/euHstvE+lElB/9uukMc/xfeK189cDhFkKwhE'))
		output['response_code'] = str(r.status_code)
		if(str(r.status_code)=="200"):
			tmp = json.loads(r.content)
			total = tmp["size"]
			page, per_page, offset = get_page_items()
			api_url = "https://api.stormpath.com/v1/applications/36i2nT8zqeSvSjOJp3Rz1Y/accounts?offset="+str(offset)+"&limit="+str(per_page)+""
			request.path = "home.html#/aws_customer"
			r = requests.get(api_url, auth=('D0XWX5WA2LEK23RMOJCW4WCVX', 'TaZArb/euHstvE+lElB/9uukMc/xfeK189cDhFkKwhE'))
			tmp = json.loads(r.content)
			customers = tmp["items"]
			pagination = get_pagination(page=page,per_page=per_page,total=total,record_name='customers',href='home.html#/aws_cutomer?page={0}')
			#pagination = get_pagination(page=page,per_page=per_page,total=total,record_name='customers')
			#print app.root_path
			print page ,per_page, offset
		else:
			print "Else"
	except  requests.HTTPError, e:
		output['status'] = "1"
	except requests.ConnectionError, e:
		output['status'] = "1"
	return render_template('aws_customer.html', users=customers,page=page,per_page=per_page,pagination=pagination)


@app.route('/aws_customer_test', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def aws_customer_test():
	start = 0
	r = requests.get('https://api.stormpath.com/v1/applications/36i2nT8zqeSvSjOJp3Rz1Y/accounts?offset=0&limit=1', auth=('D0XWX5WA2LEK23RMOJCW4WCVX', 'TaZArb/euHstvE+lElB/9uukMc/xfeK189cDhFkKwhE'))
	tmp = json.loads(r.content)
	total = tmp["size"]
	limit = 50
	static_limit = 50
	b = total / limit
	c = total % limit
	ss = []
	for num in range(start,b):
		tmp = {}
		tmp_output = {}
		api_url = "https://api.stormpath.com/v1/applications/36i2nT8zqeSvSjOJp3Rz1Y/accounts?offset="+str(start)+"&limit="+str(static_limit)
		r = requests.get(api_url, auth=('D0XWX5WA2LEK23RMOJCW4WCVX', 'TaZArb/euHstvE+lElB/9uukMc/xfeK189cDhFkKwhE'))
		if(r.status_code==200):
			res = json.loads(r.content)
			item_length = len(res["items"])
			for i in  range(item_length):
				tmp = {}
				#tmp["email"] = str(res["items"][i]['email'])
				#tmp["createdAt"] = str(res["items"][i]['createdAt'])
				try:
					tmp["username"] = str(res["items"][i]['username'])
					#tmp["status"] = str(res["items"][i]['status'])
					tmp["surname"] = str(res["items"][i]['surname'])
					tmp["fullName"] = str(res["items"][i]['fullName'])
					tmp["givenName"] = str(res["items"][i]['givenName'])
					tmp["email"] = str(res["items"][i]['email'])
					tmp["createdAt"] = str(res["items"][i]['createdAt'])
				except UnicodeError:
					tmp["username"] = res["items"][i]['username'].encode('utf-8')
					tmp["surname"] = res["items"][i]['surname'].encode('utf-8')
					tmp["fullName"] = res["items"][i]['fullName'].encode('utf-8')
					tmp["givenName"] = res["items"][i]['givenName'].encode('utf-8')
					tmp["email"] = str(res["items"][i]['email'])
					tmp["createdAt"] = str(res["items"][i]['createdAt'])
				ss.append(tmp)
		start = limit
		limit = limit + static_limit
	if(c!=0):
		api_url = "https://api.stormpath.com/v1/applications/36i2nT8zqeSvSjOJp3Rz1Y/accounts?offset="+str(start)+"&limit="+str(c)
		r = requests.get(api_url, auth=('D0XWX5WA2LEK23RMOJCW4WCVX', 'TaZArb/euHstvE+lElB/9uukMc/xfeK189cDhFkKwhE'))
		if(r.status_code==200):
			res = json.loads(r.content)
			item_length = len(res["items"])
			for j in range(item_length):
				tmp = {}
				try:
					tmp["username"] = str(res["items"][j]['username'])
					#tmp["status"] = str(res["items"][j]['status'])
					tmp["surname"] = str(res["items"][j]['surname'])
					tmp["fullName"] = str(res["items"][j]['fullName'])
					tmp["givenName"] = str(res["items"][j]['givenName'])
					tmp["email"] = str(res["items"][j]['email'])
					tmp["createdAt"] = str(res["items"][j]['createdAt'])
				except UnicodeError:
					tmp["username"] = res["items"][j]['username'].encode('utf-8')
					tmp["surname"] = res["items"][j]['surname'].encode('utf-8')
					tmp["fullName"] = res["items"][j]['fullName'].encode('utf-8')
					tmp["givenName"] = res["items"][j]['givenName'].encode('utf-8')
					tmp["email"] = str(res["items"][j]['email'])
					tmp["createdAt"] = str(res["items"][j]['createdAt'])
				ss.append(tmp)
	return json.dumps(ss)



@app.route('/stormpath_graph', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def stormpath_graph():
	start = 0
	r = requests.get('https://api.stormpath.com/v1/applications/36i2nT8zqeSvSjOJp3Rz1Y/accounts?offset=0&limit=1', auth=('D0XWX5WA2LEK23RMOJCW4WCVX', 'TaZArb/euHstvE+lElB/9uukMc/xfeK189cDhFkKwhE'))
	tmp = json.loads(r.content)
	total = tmp["size"]
	limit = 50
	static_limit = 50
	b = total / limit
	c = total % limit
	ss = []
	if(c!=0):
		b = b+1
	for i in range(b):
		api_url = "https://api.stormpath.com/v1/applications/36i2nT8zqeSvSjOJp3Rz1Y/accounts?offset="+str(start)+"&limit="+str(static_limit)
		r = requests.get(api_url, auth=('D0XWX5WA2LEK23RMOJCW4WCVX', 'TaZArb/euHstvE+lElB/9uukMc/xfeK189cDhFkKwhE'))
		if(r.status_code==200):
			res = json.loads(r.content)
			item_length = len(res["items"])
			for j in range(item_length):
				tmp = {}
				if(res["items"][j]['createdAt']):
					tmp["createdAt"] = str(res["items"][j]['createdAt'])
				ss.append(tmp)				
		start = limit
		limit = limit + static_limit
	temp={}
	dates=[]
	for dic in ss:
		date=dic["createdAt"].split("T")[0]
		if not temp.has_key(date):
			temp[date]=1
			dates.append(date)
		else:
			temp[date]=temp[date]+1
	dates=sorted(dates, key=lambda d: map(int, d.split('-')))
	result=[[],[]]
	for date in dates:
		datechange=datetime.datetime.strptime(date,'%Y-%m-%d').strftime('%d %b,%Y')
		result[0].append(datechange)
		result[1].append(temp[date])
	return json.dumps(result)

def get_page_items():
	page = int(request.args.get('page', 1))
	per_page = request.args.get('per_page')
	if not per_page:
		per_page = current_app.config.get('PER_PAGE', 10)
	else:
		per_page = int(per_page)
	offset = (page - 1) * per_page
	return page, per_page, offset

def get_css_framework():
	return current_app.config.get('CSS_FRAMEWORK', 'bootstrap3')

def get_link_size():
	return current_app.config.get('LINK_SIZE', 'sm')

def show_single_page_or_not():
	return current_app.config.get('SHOW_SINGLE_PAGE', False)


def get_pagination(**kwargs):
	kwargs.setdefault('record_name', 'records')
	return Pagination(css_framework=get_css_framework(),link_size=get_link_size(),show_single_page=show_single_page_or_not(),**kwargs)
	
def url_for_other_page(page):
	args = request.view_args.copy()
	args['page'] = page
	return url_for(request.endpoint, **args)
app.jinja_env.globals['url_for_other_page'] = "Test"


@app.route('/aws_customer', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def aws_customer():
	output = {}
	tmp_output = {}
	tmp_info = {}
	tmp_total = {}
	info = []
	try:
		r = requests.get('https://api.stormpath.com/v1/applications/36i2nT8zqeSvSjOJp3Rz1Y/accounts?offset=0&limit=100', auth=('D0XWX5WA2LEK23RMOJCW4WCVX', 'TaZArb/euHstvE+lElB/9uukMc/xfeK189cDhFkKwhE'))
		output['response_code'] = str(r.status_code)
		try:
			tmp_output = r.text
			#print tmp_output.items[1]
			#for s in tmp_output:
				#print "Testing"
		except ValueError:
			output['response_text'] = r.text
	except	requests.HTTPError, e:
		output['status'] = "1"
	except requests.ConnectionError, e:
		output['status'] = "1"
	#print output
	return tmp_output

@app.route('/aws_instance_report', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def aws_instance_report():
  output = {}
  if request.method == 'POST':
      json_data = request.get_json()
      instance_id = str(json_data.get("id", ""))
      g.cursor.execute("select text from xcloud_instance_report where instance_id='"+instance_id+"'")
      data = g.cursor.fetchone()
  return data

@app.route('/instance_report', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def instance_report():
	output = {}
  	if request.method == 'POST':
		json_data = request.get_json()
		instance_id = str(json_data.get("id", ""))
		g.cursor.execute("select report from xcloud_instance_report where instance_id='"+instance_id+"'")
		data = g.cursor.fetchone()
		#log = str("/var/www/html/xcloud_flask/xcloud_api/"+data[0])
		#f = open(log, 'rb')
		#b = f.read()
		#f.close()
	#print log
	#print os.getcwd()
	return data[0]
	#return render_template('', name=log)
	#return b


@app.route('/get_region', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_region():
	#demo_tester()
	#tmp_info = [{"id":0,"region_id":"All Regions","name":"All Regions"}]
	tmp_info = []
	region_sql = "select id,region_id,region_name from region order by id asc"
	try:
		g.cursor.execute(region_sql)
		results = g.cursor.fetchall()
		for row in results:
			tmp = {}
			tmp["id"] = int(row[0])
			tmp["region_id"] = str(row[1])
			tmp["name"] = str(row[2])
			tmp_info.append(tmp)
	except:
		print "Error: unable to fecth data"
	return json.dumps(tmp_info)




@app.route('/get_customer_stats', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_customer_stats():	
	info = []
	tmp_year = {}
	year_list = []
	month_list = []
	tmp_month = {}

	tmp_date = {}
	date_list = []
	g.cursor.execute("select created_at from dynamodb_customer_info")
	results = g.cursor.fetchall()
	for r in results:
		tmp = {}
		if(r[0]!='None'):
			s = int(r[0])
			year = datetime.datetime.fromtimestamp(s).strftime('%Y')
			if not tmp_year.has_key(year):
				tmp_year[year] = 1
				year_list.append(year)
				for t in results:
					if(t[0]!='None'):
						s1 = int(t[0])
						tmp_y =  datetime.datetime.fromtimestamp(s1).strftime('%Y')
						if(tmp_y==year):
							month = datetime.datetime.fromtimestamp(s1).strftime('%b,%Y')
							if not tmp_month.has_key(month):
								tmp_month[month] = 1
								month_list.append(month)
								for t2 in results:
									if(t2[0]!='None'):
										s2 = int(t2[0])
										tmp_m = datetime.datetime.fromtimestamp(s2).strftime('%b,%Y')
										if(tmp_m==month):
											date = datetime.datetime.fromtimestamp(s2).strftime('%d %b,%Y')
											if not tmp_date.has_key(date):
												tmp_date[date] = 1
												date_list.append(date)
											else:
												tmp_date[date] = tmp_date[date] + 1
							else:
								tmp_month[month] = tmp_month[month] + 1
			else:
				tmp_year[year] = tmp_year[year] + 1
	list2_data = []
	list_data = []


	for y in year_list:
		tmp = {}
		tmp2 = {}
		tmp["name"] = str(y)
		tmp["drilldown"] = str(y)
		tmp["y"] = int(tmp_year[y])
		list_data.append(tmp)
		tmp2["id"] = str(y)
		tmp2["name"] = "Total Customers"
		tmp2["data"] = []
		list2_data.append(tmp2)
		for m in month_list:
			k = m.split(",")
			month = k[0]
			year = k[1]
			if(year==y):
				t5 = {}
				t5["y"] = int(tmp_month[m])
				t5["drilldown"] = str(m)
				t5["name"] = str(m)
				#print t5
				for l in list2_data:
					if(l["id"]==year):
						j5 = {}
						j5["id"] = str(m)
						j5["name"] = "Total Customers"
						j5["data"] =[]
						v5 = []
						date_list = sorted(date_list)
						for d in date_list:
							a = d.split(" ")
							if(a[1]==m):
								j5["data"].append([d,tmp_date[d]])
						l["data"].append(t5)
						list2_data.append(j5)
	return json.dumps([list_data,list2_data])

@app.route('/get_scantables', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_scantables():
	tmp_info = []
	dynamodbtables_sql = "select id,table_name from dynamodb where type='1' order by id asc"
	try:
		g.cursor.execute(dynamodbtables_sql)
		results = g.cursor.fetchall()
		for row in results:
			tmp = {}
			tmp["id"] = int(row[0])
			tmp["name"] = str(row[1])
			tmp_info.append(tmp)
	except:
		print "Error: unable to fecth data"
	return json.dumps(tmp_info)

@app.route('/get_querytables', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_querytables():
	tmp_info = []
	dynamodbtables_sql = "select id,table_name from dynamodb where type='0' order by id asc"
	try:
		g.cursor.execute(dynamodbtables_sql)
		results = g.cursor.fetchall()
		for row in results:
			tmp = {}
			tmp["id"] = int(row[0])
			tmp["name"] = str(row[1])
			tmp_info.append(tmp)
	except:
		print "Error: unable to fecth data"
	return json.dumps(tmp_info)

@app.route('/get_dynamodb_keys', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_dynamodb_keys():
	output = {}
	tmp_info = []
	if request.method == 'POST':
		json_data = request.get_json()
		table_id = str(json_data.get("id", ""))
		key_sql = "select id,key_type,key_name,key_name_type from dynamodb_keys where dynamodb_id='"+table_id+"'"
		try:
			g.cursor.execute(key_sql)
			results = g.cursor.fetchall()
			for row in results:
				tmp = {}
				tmp["id"] = int(row[0])
				tmp["type"] = str(row[1])
				tmp["name"] = str(row[2])
				tmp["key_type"] = str(row[3])
				tmp_info.append(tmp)
		except:
			print "Error: unable to fecth data"
	return json.dumps(tmp_info)



@app.route('/get_dynamodboperators', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_dynamodboperators():
	tmp_info = []
	dynamodboperators_sql = "select name,key_name from dynamodb_operator order by id asc"
	try:
		g.cursor.execute(dynamodboperators_sql)
		results = g.cursor.fetchall()
		for row in results:
			tmp = {}
			tmp["name"] = str(row[0])
			tmp["key_name"] = str(row[1])
			tmp_info.append(tmp)
	except:
		print "Error: unable to fecth data"
	return json.dumps(tmp_info)


def get_countrycode(api_url):
	r = requests.get(api_url, auth=('D0XWX5WA2LEK23RMOJCW4WCVX', 'TaZArb/euHstvE+lElB/9uukMc/xfeK189cDhFkKwhE'))
	if(r.status_code==200):
		res = json.loads(r.content)
		#print str(res["country"])
		return str(res["country"])

@app.route('/stormpath_country', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def stormpath_country():
	res = [[],[]]
	cc_sql = "select xcloud_country_codes.name,xcloud_country.count from xcloud_country inner join xcloud_country_codes on xcloud_country.country_code=xcloud_country_codes.country_code  where xcloud_country.country_code!='' and  xcloud_country.count >= 10 order by xcloud_country.count desc"
	try:
		g.cursor.execute(cc_sql)
		results = g.cursor.fetchall()
		for row in results:
			print row
			res[0].append(row[0])
			res[1].append(row[1])
	except:
		print "Error: unable to fecth data"
	return json.dumps(res)


def getReportDict(dbitem):
	r = {}
	for k,v in dbitem.items():
		if isinstance(v, decimal.Decimal):
			r[k] = int(v)
		else:
			r[k] = v
	return r

def get_db_items(region,tbl_name,records):
	#tmp_tbl = str(record[0]["tbl"])
	print tbl_name
	if(tbl_name=="AccessPointClaimCache"):
		region = "us-east-1"
	conn = boto.dynamodb2.connect_to_region(region)
	get_tbl = Table(tbl_name,connection=conn)
	try:
		results = get_tbl.scan(**records)
	except:
		print "Error in Search"
	tmp_info = []
	try:
		for res in results:
			tmp_info.append(getReportDict(res))
	except UnknownFilterTypeError:
		print "Error found"
	except ValidationException:
		print "ValidationException"
	return json.dumps(tmp_info)


def get_query_items(region,tbl_name,records):

	#print tbl_name

	#print records

	#print region

	conn = boto.dynamodb2.connect_to_region(region)

	get_tbl = Table(tbl_name,connection=conn)

	try:
		results = get_tbl.query_2(**records)
	except:
		print "Error Found"
	tmp_info = []
	try:
		for res in results:
			tmp_info.append(getReportDict(res))
	except:
		print "Error"
	#print tmp_info
	return json.dumps(tmp_info,cls=DecimalJSONEncoder)

@app.route('/get_dynamodb_table_size', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_dynamodb_table_size():
	if request.method == 'POST':
		json_data = request.get_json()
		tmp_region = json_data[0]
		tmp_tbl_name = json_data[1]
		region = str(tmp_region[0]["region_id"])
		tbl_name = str(tmp_tbl_name[0]["name"])
		#conn = boto.dynamodb2.connect_to_region(region)
		#result = conn.describe_table(tbl_name)
		info = []
		tmp_table = {}
		tmp_info = []
		if(tbl_name=="AccessPointClaimCache"):
			region = "us-east-1"
			conn = boto.dynamodb2.connect_to_region(region,aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)
			result = conn.describe_table(tbl_name)
			tmp = {}
			tmp["region_id"] = str(region)
			tmp["region_name"] = str("US East (N. Virginia)")
			tmp["records"] = result['Table']['ItemCount']
			tmp_info.append({tbl_name:[tmp]})
		else:
			for r in tmp_region:
				tmp = {}
				region = str(r["region_id"])
				conn = boto.dynamodb2.connect_to_region(region)
				result = conn.describe_table(tbl_name)
				tmp["region_id"] = region
				tmp["region_name"] = str(r["name"])
				tmp["records"] = result['Table']['ItemCount']
				info.append(tmp)
				#print tbl_name
				#print region
			tmp_info.append({tbl_name:sorted(info,reverse=True)})
		return json.dumps(tmp_info)

@app.route('/get_dynamodb_query_items', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_dynamodb_query_items():
	
	if request.method == 'POST':
		
		json_data = request.get_json()
		tmp_region = json_data[0]
		tbl_name = json_data[1]
		filters = json_data[2]
		result=[]
		info = {}
		infoOuter=[]
		tmp_info = {}

		for r in tmp_region:
			infoOuter=[]
			tmp_data = {}
			
			region = str(r["region_id"])

			i = 0
			
			for t in tbl_name:

				tmp = {}

				tmp_tbl_name = t["name"]

				if(str(filters[i]['h_key1']['type'])=="HashKeyElement"):
					tmp_key = str(filters[i]['h_key1']['name'])+"__"+str(filters[i]['h_operator'])
					if(str(filters[i]['h_key1']['key_type'])=="S"):
						tmp[tmp_key] = str(filters[i]['h_string'])
					else:
						tmp[tmp_key] = int(filters[i]['h_string'])
				if(filters[i]['r_string']):
					if(str(filters[i]['r_key1']['type'])=="RangeKeyElement"):
						tmp_key = str(filters[i]['r_key1']['name'])+"__"+str(filters[i]['r_operator'])
						if(str(filters[i]['r_key1']['key_type'])=="S"):
							tmp[tmp_key] = str(filters[i]['r_string'])
						else:
							tmp[tmp_key] = int(filters[i]['r_string'])
				i = i + 1
				infoOuter.append(json.loads(get_query_items(region,tmp_tbl_name,tmp)))
			if not tmp_info.has_key(region):
				print "Length",len(infoOuter[0])
				if(len(infoOuter[0]) > 0):
					tmp_info[region]=infoOuter
		result.append(tmp_info)
	return json.dumps(result)

@app.route('/get_dynamodb_items', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_dynamodb_items():
	if request.method == 'POST':
		json_data = request.get_json()
		tmp_region = json_data[0]
		tmp_tbl_name = json_data[1]
		filters = json_data[2]
		tbl_name = str(tmp_tbl_name[0]["name"])

		tmp_info = []

		info = {}

		tmp_data = {}

		print tmp_region

		if(tbl_name=="AccessPointClaimCache"):
			tmp_region = [{'region_id': 'us-east-1', 'id': 1, 'name': 'US East (N. Virginia)'}]

		for r in tmp_region:
			region = str(r["region_id"])
			for f in filters:
				tmp = {}
				if(str(f['search_operator']['key_name'])=="not_null"):
					tmp_key = str(f['hash_key'])+"__"+str("null")
				elif(str(f['search_operator']['key_name'])=="null"):
					tmp_key = str(f['hash_key'])+"__"+str("null")
				else:
					tmp_key = str(f['hash_key'])+"__"+str(f['search_operator']['key_name'])
				
				if(str(f['type']['type'])=="N"):
					if(str(f['search_operator']['key_name'])=="not_null"):
						tmp[tmp_key] = False
					elif(str(f['search_operator']['key_name'])=="null"):
						tmp[tmp_key] = True
					else:
						tmp[tmp_key] = int(f['search_string'])
				else:
					if(str(f['search_operator']['key_name'])=="not_null"):
						tmp[tmp_key] = False
					elif(str(f['search_operator']['key_name'])=="null"):
						tmp[tmp_key] = True
					else:
						tmp[tmp_key] = str(f['search_string'])
				info.update(tmp)

			if(len(json.loads(get_db_items(region,tbl_name,info))) > 0):

				tmp_data[region] = json.loads(get_db_items(region,tbl_name,info))
		
		tmp_info.append(tmp_data)
		
		return json.dumps(tmp_info)
		#print "Testing",tmp_region[0]
		#print tmp_tbl_name

		#region = str(tmp_region["region_id"])
		#tbl_name = str(tmp_tbl_name["name"])
		#tmp_info = []
		#info = {'limit':50}
		#info = {}

		#print "region name",region

		#print "Table Name",tbl_name

		'''
		for f in filters:
			print str(f['hash_key']['key_type'])
			tmp = {}
			tmp_key = str(f['hash_key']['key_name'])+"__"+str(f['search_operator']['key_name'])
			if(str(f['hash_key']['key_type'])=="N"):
				tmp[tmp_key] = int(f['search_string'])
			elif(str(f['hash_key']['key_type'])=="S"):
				tmp[tmp_key] = str(f['search_string'])
			#tmp["s"] = str(f['hash_key']['key_name'])+"__"+str(f['search_operator']['key_name'])
			#tmp["key_name"] = str(f['hash_key']['key_name'])
			#tmp["type"] = str(f['hash_key']['key_type'])
			#tmp["op"] = str(f['search_operator']['key_name'])
			#tmp["str"] = int(f['search_string'])
			info.update(tmp)
			#tmp_info.append(tmp)
		tmp_info = get_db_items(region,tbl_name,info)
		#test = "Testing"
		'''	
	return tmp_info

@app.route('/background_task', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def background_task():
	statistics_tbl_cleanup()
	result = add.delay(session['userid'])
	session['TASK_ID'] = result.id
	print "Worker ID",result.id

	if(result.ready()):
		a = "Completed"
	else:
		a = "Not Done"
	return a

aysnc_res = ""




def get_regions():
	#tmp_info = [{"id":0,"region_id":"All Regions","name":"All Regions"}]
	tmp_info = []
	region_sql = "select id,region_id,region_name from region order by id asc"
	try:
		g.cursor.execute(region_sql)
		results = g.cursor.fetchall()
		for row in results:
			tmp = {}
			tmp["id"] = int(row[0])
			tmp["region_id"] = str(row[1])
			tmp["name"] = str(row[2])
			tmp_info.append(tmp)
	except Exception as e:
		print e
		print "Error: unable to fecth data"
	return tmp_info



@app.route('/background_task_2', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def background_task_2():

	print get_regions()

	'''
	aysnc_res = session['TASK_ID']
	print "Value of this",aysnc_res
	result = add.AsyncResult(aysnc_res)
	print "the Values og Results",result.get()
	'''
	#print get_region()
	'''
	if aysnc_res.ready() == True:
		b  = "Iam done"
	else:
		b = "Not Done"
	'''
	tmp = {"deom":"deom"}
	return "Tested"

@app.route('/get_ap_stats1', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_ap_stats1():
	info = []
	tmp_info = []
	test = {}
	region_info = []
	t = {}
	tmp = {}

	a1 = []
	region_list =  get_regions()
	model = ["Xi-1","Xi-2","Xi-3","Xo-1"]
	for r in region_list:
		t = {}
		for m in model:
			a2 = {}
			test = {}
			tmp = {}
			g.cursor.execute("select sum(tbl.count) as xi_1_count,tbl.model as Xi_1_model from ((SELECT dynamodb_customer_info.id,dynamodb_ap_info.count,dynamodb_ap_info.model FROM dynamodb_customer_info inner join dynamodb_ap_info on dynamodb_ap_info.customer_id=dynamodb_customer_info.id WHERE dynamodb_customer_info.region_id='"+str(r["id"])+"' and dynamodb_ap_info.model='"+str(m)+"' ORDER BY dynamodb_ap_info.count  DESC) as tbl)")
			ap_count = g.cursor.fetchone()
			c = str(ap_count[0])
			if c == "None":
				c = str("0")
			test[m] = c
			a2["name"] = m
			a2["data"] = [1,2,3,4,5]
			a1.append(a2)
			#print m,"------------------",c
			#test["xi-1"] = 120
			#test["xi-2"] = 120
			#test["xi-3"] = 120
			t.update(test)
		tmp[r["name"]] = [t]
		info.append(tmp)
	#print info
	print a1
	return "data"

@app.route('/get_ap_stats', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_ap_stats():
	info = []
	inner = []
	tmp_info = {}
	temp = {}
	xaxis = []
	total = []
	j = 0
	model = ["Xi-1","Xi-2","Xi-3","Xo-1"]
	for m in model:
		inner = []
		g.cursor.execute("select DISTINCT xcloud_ap_info.region_id as reg,region.region_name,(select count(*) from xcloud_ap_info where region_id=reg) as counter from xcloud_ap_info INNER join region on region.id=xcloud_ap_info.region_id ORDER BY counter DESC")
		region_list = g.cursor.fetchall()
		for r in region_list:
			tmp = {}
			if(j==0):
				xaxis.append(r[1])
				total.append(r[2])
			tmp["name"] = m
			g.cursor.execute("select count(*) from xcloud_ap_info where region_id='"+str(r[0])+"' and model='"+str(m)+"'")
			ap_count = g.cursor.fetchone()
			c = str(ap_count[0])
			if c == "None":
				c = str("0")
			inner.append(int(c))
		j = 1
		if not temp.has_key(tmp["name"]):
			tmp["data"] = inner
			info.append(tmp)
	return json.dumps([xaxis,info,total])


'''

@app.route('/get_ap_stats', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_ap_stats():
	dummy_func()
	info = []
	inner = []
	tmp_info = {}
	temp = {}
	xaxis = []
	region_list =  get_regions()
	j = 0
	model = ["Xi-1","Xi-2","Xi-3","Xo-1"]
	for m in model:
		inner = []
		g.cursor.execute("select DISTINCT dynamodb_customer_info.region_id as reg,region.region_name,(select count(*) from dynamodb_customer_info where region_id=reg) as counter from dynamodb_customer_info inner join region on region.id=dynamodb_customer_info.region_id ORDER BY counter  DESC")
		region_list = g.cursor.fetchall()
		for r in region_list:
			tmp = {}
			if(j==0):
				xaxis.append(r[1])
			tmp["name"] = m
			g.cursor.execute("select count(*) from dynamodb_customer_info inner join xcloud_ap_info on xcloud_ap_info.customer_id=dynamodb_customer_info.id where dynamodb_customer_info.region_id='"+str(r[0])+"' and xcloud_ap_info.model='"+str(m)+"'")
			ap_count = g.cursor.fetchone()
			c = str(ap_count[0])
			if c == "None":
				c = str("0")
			inner.append(int(c))
		j = 1
		if not temp.has_key(tmp["name"]):
			tmp["data"] = inner
			info.append(tmp)
			#print r["id"],"-----------------",m
	return json.dumps([info,xaxis])
		#print m
	#print "Am working"
'''

@app.route('/get_ap_version', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_ap_version():
	info = []
	temp = {}
	v_temp = {}
	ver_info = []
	total = []
	k = 0
	model = ["Xi-1","Xi-2","Xi-3","Xo-1"]
	g.cursor.execute("select DISTINCT version as ver,(select count(*) from xcloud_ap_info where version=ver) as counter from xcloud_ap_info ORDER BY counter  DESC")
	results = g.cursor.fetchall()
	for m in model:
		inner = []
		for r in results:
			tmp = {}
			ver = str(r[0])
			if(ver==''):
				ver = "Unknown"
			if ver not in ver_info:
				ver_info.append(ver)
			tmp["name"] = m
			g.cursor.execute("select count(*) from xcloud_ap_info where version='"+str(r[0])+"' and model='"+str(m)+"'")
			ap_count = g.cursor.fetchone()
			c = str(ap_count[0])
			if c == "None":
				c = int("0")
			else:
				c = int(c)
			inner.append(c)
			if(k==0):
				total.append(r[1])
		k = 1
		if not temp.has_key(tmp["name"]):
			tmp["data"] = inner
			info.append(tmp)
	return json.dumps([ver_info,info,total])
'''
@app.route('/get_ap_version', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_ap_version():
	get_demo()
	info = []
	temp = {}
	v_temp = {}
	ver_info = []
	total = []
	g.cursor.execute("select DISTINCT version from xcloud_ap_info")
	results = g.cursor.fetchall()
	model = ["Xi-1","Xi-2","Xi-3","Xo-1"]
	for r in results:
		k = 0
		for m in model:
			g.cursor.execute("select count(*) from xcloud_ap_info where version='"+str(r[0])+"' and model='"+str(m)+"'")
			ap_count = g.cursor.fetchone()
			c = str(ap_count[0])
			if c == "None":
				c = int("0")
			else:
				c = int(ap_count[0])
			k = k + c
		total.append(k)
	print total
	for m in model:
		inner = []
		k = 0
		for r in results:
			tmp = {}
			ver = str(r[0])
			if(ver==''):
				ver = "Unknown"
			if ver not in ver_info:
				ver_info.append(ver)
			tmp["name"] = m
			g.cursor.execute("select count(*) from xcloud_ap_info where version='"+str(r[0])+"' and model='"+str(m)+"'")
			ap_count = g.cursor.fetchone()
			c = str(ap_count[0])
			if c == "None":
				c = int("0")
			else:
				c = int(c)
			inner.append(c)
		if not temp.has_key(tmp["name"]):
			tmp["data"] = inner
			info.append(tmp)

	return json.dumps([ver_info,info,total])

'''

def demo_tester1():
	info = []
	g.cursor.execute("select DISTINCT ap_cc_set from xcloud_ap_info")
	results = g.cursor.fetchall()
	region_list =  get_regions()
	model = ["Xi-1","Xi-2","Xi-3","Xo-1"]
	for m in model:
		inner = []
		for r in region_list:
			for d in results:
				tmp = {}
				print d[0],"--------",r["id"],"--------",m
	'''
	for m in model:
		inner = []
		k = 0
		for r in results:
			tmp = {}
			print "select count(*) from xcloud_ap_info where version='"+str(r[0])+"'"
	'''

@app.route('/get_ap_scountry222', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_ap_scountry222():
	info = []
	inner = []
	tmp_info = {}
	temp = {}
	model = ["Xi-1","Xi-2","Xi-3","Xo-1"]
	tmp = {}
	g.cursor.execute("SELECT DISTINCT dynamodb_customer_info.country,xcloud_country_codes.name FROM dynamodb_customer_info inner join xcloud_country_codes on dynamodb_customer_info.country=xcloud_country_codes.country_code")
	results = g.cursor.fetchall()
	for m in model:
		inner = []
		k = 0
		for row in results:
			tmp = {}
			tmp["name"] = m
			g.cursor.execute("select sum(tbl.count) as xi_1_count,tbl.model as Xi_1_model from ((SELECT dynamodb_customer_info.id,dynamodb_ap_info.count,dynamodb_ap_info.model FROM dynamodb_customer_info inner join dynamodb_ap_info on dynamodb_ap_info.customer_id=dynamodb_customer_info.id WHERE dynamodb_customer_info.country='"+str(row[0])+"' and dynamodb_ap_info.model='"+str(m)+"' ORDER BY dynamodb_ap_info.count  DESC) as tbl)")
			ap_count = g.cursor.fetchone()
			c = str(ap_count[0])
			if c == "None":
				c = int("0")
			else:
				c = int(ap_count[0])
			inner.append(int(c))
			k = k + c
		if not temp.has_key(tmp["name"]):
			print "Length of inner",len(inner)
			tmp["data"] = inner
			info.append(tmp)
			#print "Country",row[0],"Model",m
	tester_func()
	return json.dumps(info)

'''
@app.route('/get_ap_scountry', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_ap_scountry():

	work_flow()
	info = []
	info_outer = []
	info_country = []
	temp ={}
	total = []
	model = ["Xi-1","Xi-2","Xi-3","Xo-1"]
	g.cursor.execute("SELECT DISTINCT dynamodb_customer_info.country,xcloud_country_codes.name FROM dynamodb_customer_info inner join xcloud_country_codes on dynamodb_customer_info.country=xcloud_country_codes.country_code")
	results = g.cursor.fetchall()
	for row in results:
		k = 0
		for m in model:
			g.cursor.execute("select sum(tbl.count) as xi_1_count,tbl.model as Xi_1_model from ((SELECT dynamodb_customer_info.id,dynamodb_ap_info.count,dynamodb_ap_info.model FROM dynamodb_customer_info inner join dynamodb_ap_info on dynamodb_ap_info.customer_id=dynamodb_customer_info.id WHERE dynamodb_customer_info.country='"+str(row[0])+"' and dynamodb_ap_info.model='"+str(m)+"' ORDER BY dynamodb_ap_info.count  DESC) as tbl)")
			ap_count = g.cursor.fetchone()
			c = str(ap_count[0])
			if c == "None":
				c = int("0")
			else:
				c = int(ap_count[0])
			k = k + c		
		if(k >= 10):
			info.append(row[0])
			info_country.append(row[1])
			total.append(k)
	for m in model:
		inner = []
		for i in info:
			tmp = {}
			tmp["name"] = m
			g.cursor.execute("select sum(tbl.count) as xi_1_count,tbl.model as Xi_1_model from ((SELECT dynamodb_customer_info.id,dynamodb_ap_info.count,dynamodb_ap_info.model FROM dynamodb_customer_info inner join dynamodb_ap_info on dynamodb_ap_info.customer_id=dynamodb_customer_info.id WHERE dynamodb_customer_info.country='"+str(i)+"' and dynamodb_ap_info.model='"+str(m)+"' ORDER BY dynamodb_ap_info.count  DESC) as tbl)")
			ap_count = g.cursor.fetchone()
			c = str(ap_count[0])
			if c == "None":
				c = int("0")
			else:
				c = int(ap_count[0])
			inner.append(int(c))
		if not temp.has_key(tmp["name"]):
			tmp["data"] = inner
			info_outer.append(tmp)
	return json.dumps([info_country,info_outer,total])
	#print info
'''


@app.route('/get_ap_scountry', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_ap_scountry():
	info = []
	info_country = []
	cc_code = []
	temp = {}
	info_outer = []
	total = []
	j = 0
	model = ["Xi-1","Xi-2","Xi-3","Xo-1"]
	g.cursor.execute("select * from (select DISTINCT cc as code,xcloud_country_codes.name,(select count(*) from xcloud_ap_info where cc=code) as counter from xcloud_ap_info left join xcloud_country_codes on xcloud_country_codes.country_code=cc) as tmp_table where tmp_table.counter >=5 ORDER BY counter DESC")
	results = g.cursor.fetchall()
	for m in model:
		inner = []
		for c in results:
			t1 = int(c[2])
			tmp = {}
			tmp["name"] = m
			cc_code = str(c[1])
			if not c[0]:
				cc_code = "Unknown"
			g.cursor.execute("select count(*) from xcloud_ap_info where cc='"+str(c[0])+"' and model='"+str(m)+"'")
			ap_count = g.cursor.fetchone()
			c = str(ap_count[0])
			if c == "None":
				c = int("0")
			else:
				c = int(ap_count[0])
			inner.append(int(c))
			if(j==0):
				info_country.append(cc_code)
				total.append(t1)
		j = 1
		if not temp.has_key(tmp["name"]):
			tmp["data"] = inner
			info_outer.append(tmp)
	return json.dumps([info_country,info_outer,total])


@app.route('/get_ap_geolocation', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_ap_geolocation():
	info = []
	g.cursor.execute("select * from (select DISTINCT cc as code,xcloud_country_codes.name,xcloud_country_codes.latitude,xcloud_country_codes.longitude,(select count(*) from xcloud_ap_info where cc=code) as counter from xcloud_ap_info left join xcloud_country_codes on xcloud_country_codes.country_code=cc) as tmp_table where code!='' and code!='Z2' ORDER BY counter DESC")
	results = g.cursor.fetchall()
	i = 0
	for r in results:
		tmp = {}
		tmp["id"] = int(i)
		tmp["show"] = False
		tmp["country"] = str(r[0])
		tmp["options"] = {}
		tmp["coords"] = {}
		tmp["coords"]["latitude"] = float(r[2])
		tmp["coords"]["longitude"] = float(r[3])
		info.append(tmp)
		i = i + 1
	return json.dumps(info)

@app.route('/get_ap_info', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_ap_info():
	info = []
	xaxis = []
	yaxis = []
	if request.method == 'POST':
		json_data = request.get_json()
		cc = json_data.get("cc", "")
		g.cursor.execute("SELECT DISTINCT model as m,(select count(*) from xcloud_ap_info where cc='"+str(cc)+"' and model=m) as counter FROM xcloud_ap_info WHERE cc='"+str(cc)+"' ORDER BY counter DESC")
		results = g.cursor.fetchall()
		for r in results:
			xaxis.append(str(r[0]))
			yaxis.append(int(r[1]))
	return json.dumps([xaxis,yaxis,sum(yaxis)])

@app.route('/get_tenant_geolocation', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_tenant_geolocation():
	info = []
	print "select * from (SELECT DISTINCT dynamodb_customer_info.country as cc,xcloud_country_codes.name,xcloud_country_codes.latitude,xcloud_country_codes.longitude,(select count(*) from dynamodb_customer_info where country=cc) as counter FROM dynamodb_customer_info left join xcloud_country_codes on dynamodb_customer_info.country=xcloud_country_codes.country_code) as tmp_table ORDER BY counter DESC"
	g.cursor.execute("select * from (SELECT DISTINCT dynamodb_customer_info.country as cc,xcloud_country_codes.name,xcloud_country_codes.latitude,xcloud_country_codes.longitude,(select count(*) from dynamodb_customer_info where country=cc) as counter FROM dynamodb_customer_info left join xcloud_country_codes on dynamodb_customer_info.country=xcloud_country_codes.country_code) as tmp_table ORDER BY counter DESC")
	results = g.cursor.fetchall()
	i = 0
	for r in results:
		cc = str(r[0])
		if(cc!="None"):
			tmp = {}
			tmp["id"] = int(i)
			tmp["latitude"] = float(r[2])
			tmp["longitude"] = float(r[3])
			tmp["showWindow"] = False
			tmp["cc"] = cc
			tmp["options"] = {}
			if(i <= 5):
				tmp["options"]["animation"] = 1
			#tmp["window"] = {}
			#tmp["window"]["title"] = str("This is the Test Data for now")
			info.append(tmp)
			i = i + 1
	return json.dumps(info)


@app.route('/get_tenant_info', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_tenant_info():
	info = []
	xaxis = []
	yaxis = []
	if request.method == 'POST':
		json_data = request.get_json()
		cc = json_data.get("cc", "")
		g.cursor.execute("select count(*) from dynamodb_customer_info where country='"+str(cc)+"'")
		result = g.cursor.fetchall()
	return json.dumps(result[0])


'''

@app.route('/get_ap_scountry', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_ap_scountry():
	gen_fun()
	info = []
	info_country = []
	cc_code = []
	temp = {}
	info_outer = []
	total = []
	model = ["Xi-1","Xi-2","Xi-3","Xo-1"]
	g.cursor.execute("select DISTINCT xcloud_ap_info.cc,xcloud_country_codes.name from xcloud_ap_info left join xcloud_country_codes on xcloud_country_codes.country_code=xcloud_ap_info.cc")
	results = g.cursor.fetchall()
	for r in results:
		k = 0
		for m in model:
			g.cursor.execute("select count(*) from xcloud_ap_info where cc='"+str(r[0])+"' and model='"+str(m)+"'")
			ap_count = g.cursor.fetchone()
			c = str(ap_count[0])
			if c == "None":
				c = int("0")
			else:
				c = int(ap_count[0])
			k = k + c
			country = str(r[1])
			
		if(k >= 5):
			if(country=='None'):
				country = "Unknown"
			if country not in info_country:
				cc_code.append(str(r[0]))
				info_country.append(country)
				total.append(k)
			#print "The Country--------",country,"Counter--------------",k
	#print info_country,"----------",cc_code

	for m in model:
		inner = []
		for c in cc_code:
			tmp = {}
			tmp["name"] = m
			g.cursor.execute("select count(*) from xcloud_ap_info where cc='"+str(c)+"' and model='"+str(m)+"'")
			ap_count = g.cursor.fetchone()
			c = str(ap_count[0])
			if c == "None":
				c = int("0")
			else:
				c = int(ap_count[0])
			inner.append(int(c))
		if not temp.has_key(tmp["name"]):
			tmp["data"] = inner
			info_outer.append(tmp)
	return json.dumps([info_country,info_outer,total])
'''


@app.route('/get_dynamodb_stats', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_dynamodb_stats():
	print "--------------------------------------"
	print "username",session["username"]
	print "--------------------------------------"
	print "User ID",session["userid"]
	print "--------------------------------------"
	info = []
	tmp = {}
	region = []
	g.cursor.execute("select count(*) from dynamodb_customer_info")
	xtenant = g.cursor.fetchone()
	g.cursor.execute('select (SELECT count(*) FROM xcloud_ap_info WHERE model="Xi-1") as xi1_count,(SELECT count(*) FROM xcloud_ap_info WHERE model="Xi-2") as xi2_count,(SELECT count(*) FROM xcloud_ap_info WHERE model="Xi-3") as xi3_count,(SELECT count(*) FROM xcloud_ap_info WHERE model="Xo-1") as xo1_count')
	ap_count = g.cursor.fetchone()
	tmp["xtenant"] = str(xtenant[0])
	tmp["xi_1"] = int(ap_count[0])
	tmp["xi_2"] = int(ap_count[1])
	tmp["xi_3"] = int(ap_count[2])
	tmp["xo_1"] = int(ap_count[3])
	info.append(tmp)
	return json.dumps(info)

def dashboard_status(id):
	g.cursor.execute("select count(*) from xcloud_dashboard where widget_id='"+str(id)+"' and user_id='"+str(session['userid'])+"'")
	result = g.cursor.fetchone()
	if result[0] == 0:
		return False
	else:
		return True
	#print result[0]

@app.route('/get_dashboard', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_dashboard():
	info = []
	g.cursor.execute("select id,name,status from xcloud_widget order by id asc")
	results = g.cursor.fetchall()
	for row in results:
		res = {}
		res["id"] = int(row[0])
		res["name"] = str(row[1])
		res["status"] = int(row[2])
		res["ticked"] = dashboard_status(res["id"])
		info.append(res)
	return json.dumps(info)

@app.route('/report_info', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def report_info():
	info = []
	g.cursor.execute("select id,unix_timestamp(updated_at) * 1000 as updated_at,status from xcloud_statistics where user_id='"+str(session['userid'])+"'")
	result = g.cursor.fetchone()
	if result is not None:
		tmp = {}
		tmp["report"] = str(result[1])
		tmp["status"] = str(result[2])
		info.append(tmp)
	return json.dumps(info)



@app.route('/custom_dash', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def custom_dash():
	g.cursor.execute("delete from xcloud_dashboard where user_id='"+str(session['userid'])+"'")
	if request.method == 'POST':
		json_data = request.get_json()
		dashboard = json_data[0]
		for d in dashboard:
			g.cursor.execute("insert into xcloud_dashboard set widget_id='"+str(d['id'])+"',user_id='"+str(session['userid'])+"',updated_at=now()")
			g.conn.commit()
		info = []
		g.cursor.execute("select xcloud_widget.name from xcloud_dashboard inner join xcloud_widget on xcloud_widget.id=xcloud_dashboard.widget_id where xcloud_dashboard.user_id='"+str(session['userid'])+"'")
		results = g.cursor.fetchall()
		for row in results:
			tmp = {}
			tmp["name"] = str(row[0])
			info.append(tmp)
	return json.dumps(info)
	#return "compled"

@app.route('/get_user_dashboard', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_user_dashboard():
	info = []
	g.cursor.execute("select xcloud_widget.name from xcloud_dashboard inner join xcloud_widget on xcloud_widget.id=xcloud_dashboard.widget_id where xcloud_dashboard.user_id='"+str(session['userid'])+"'")
	results = g.cursor.fetchall()
	for row in results:
		tmp = {}
		tmp["name"] = str(row[0])
		info.append(tmp)
	return json.dumps(info)


@app.route('/get_tenant_stats', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_tenant_stats():
	xaxis = []
	yaxis = []
	g.cursor.execute("select region.region_name,(SELECT count(*) from dynamodb_customer_info where dynamodb_customer_info.region_id=region.id) as count from region ORDER BY count DESC")
	results = g.cursor.fetchall()
	for r in results:
		xaxis.append(r[0])
		yaxis.append(r[1])
	return json.dumps([xaxis,yaxis])

@app.route('/get_tenant_country', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_tenant_country():
	info = []
	xaxis = []
	yaxis = []
	g.cursor.execute("SELECT DISTINCT dynamodb_customer_info.country as cc,xcloud_country_codes.name,(select count(*) from dynamodb_customer_info where country=cc) as counter FROM dynamodb_customer_info left join xcloud_country_codes on dynamodb_customer_info.country=xcloud_country_codes.country_code ORDER BY counter DESC")
	results = g.cursor.fetchall()
	for row in results:
		if(row[2] > 1):
			if not row[1]:
				s = "Unknown"
			else:
				s = row[1]
			xaxis.append(s)
			yaxis.append(row[2])
	return json.dumps([xaxis,yaxis])

@app.route('/report_statistics', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def report_statistics():
	result = add_together.delay(4, 4)
	print "The Data is here",result
	#region_list = get_region().response[0]
	#print region_list
	tmp = {"demo":"demo"}
	return tmp



	'''
	for res in test:
		cust_info_sql = "insert into dynamodb_customer_info set region_id='"+str(region_id)+"',xtenant='"+str(res["xtenant"])+"',email='"+str(res["email"])+"',given_name='"+str(res["given_name"])+"',surname='"+str(res["surname"])+"',country='"+str(res["country"])+"',company_name='"+str(res["company_name"])+"',updated_at=now()"
		cursor.execute(cust_info_sql)
		db.commit()
	'''

def sample():

	with app.app_context():
		db_connect()
		region_list = get_regions()
		print region_list
		db_disconnect()


	'''

	with app.test_request_context():
		db_connect()

		db_disconnect()
		pass
	print "demo"
	'''

		#db_connect()
		#ss =  get_region().response[0]

	'''

	print "hello Worlds"
	with app.app_context():
		db_connect()
		print "SS"
		db_disconnect()
	'''

	#region_list = get_regions()
#sample()

def statistics_tbl_cleanup():
	g.cursor.execute("update xcloud_statistics set status='1' where id='1'")
	g.conn.commit()
	g.cursor.execute("truncate table dynamodb_customer_info")
	g.cursor.execute("truncate table xcloud_ap_info")



def func():
	info = []
	g.cursor.execute("SELECT DISTINCT created_at as c,(select count(*) from dynamodb_customer_info where created_at=c) as counter from dynamodb_customer_info ORDER BY counter DESC")
	results = g.cursor.fetchall()
	for r in results:
		tmp = str(r[0])
		if(tmp!="None"):
			time = int(r[0]) * 1000
			info.append([time,int(r[1])])
	print info

@app.route('/get_top_customers', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_top_customers():
	#func()
	info = []
	g.cursor.execute("select DISTINCT customer_id as cus,dynamodb_customer_info.*,xcloud_country_codes.name,(select count(*) from xcloud_ap_info where xcloud_ap_info.customer_id=cus) as count from xcloud_ap_info inner join dynamodb_customer_info on dynamodb_customer_info.id=xcloud_ap_info.customer_id left join xcloud_country_codes on xcloud_country_codes.country_code=dynamodb_customer_info.country ORDER BY count DESC")
	results = g.cursor.fetchall()
	for row in results:
		if(int(row[12]) >= 10):
			tmp = {}
			tmp["id"] = str(row[1])
			tmp["xtenant"] = str(row[3])
			tmp["email"] = str(row[4])
			tmp["given_name"] = str(row[5])
			tmp["surname"] = str(row[6])
			country = str(row[11])
			if(country=="None"):
				country = "Unknown"
			tmp["country"] = country	
			tmp["company_name"] = str(row[8])
			tmp["count"] = int(row[12])
			info.append(tmp)
			#print row[3]
	return json.dumps(info)


@app.route('/get_xtenant_config', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_xtenant_config():
	info = []
	xaxis = []
	yaxis = []
	if request.method == 'POST':
		json_data = request.get_json()
		customer_id = json_data['id']
		g.cursor.execute("select DISTINCT model as m,(select count(*) from xcloud_ap_info where xcloud_ap_info.model=m and customer_id='"+str(customer_id)+"') as count from xcloud_ap_info where customer_id='"+str(customer_id)+"' ORDER BY count DESC")
		results = g.cursor.fetchall()
		for row in results:
			xaxis.append(str(row[0]))
			yaxis.append(int(row[1]))
	return json.dumps([xaxis,yaxis])

@app.route('/get_active_xtenant', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_active_xtenant():
	info = []
	g.cursor.execute("SELECT count(*) FROM dynamodb_customer_info")
	total = g.cursor.fetchone()
	g.cursor.execute("SELECT count(DISTINCT customer_id) FROM xcloud_ap_info")
	active = g.cursor.fetchone()
	inactive = total[0] - active[0]
	xaxis = ["Active Customers","Inactive Customers"]
	yaxis = [active[0],inactive]
	return json.dumps([xaxis,yaxis])

@app.route('/get_locked_ap', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_locked_ap():
	info = []
	xaxis = []
	yaxis = []
	g.cursor.execute("SELECT DISTINCT ap_cc_set as m,(select count(*) from xcloud_ap_info where ap_cc_set=m) as counter from xcloud_ap_info ORDER BY counter DESC")
	results = g.cursor.fetchall()
	for row in results:
		ap = str(row[0])
		if(ap=="0"):
			tmp = "WWW"
		elif(ap=="1"):
			tmp = "Locked"
		else:
			tmp = "Unknown"
		xaxis.append(tmp)
		yaxis.append(row[1])
	return json.dumps([xaxis,yaxis])


@app.route('/get_ap_health', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_ap_health():
	info = []
	xaxis = []
	yaxis = []
	g.cursor.execute("SELECT DISTINCT ap_health as m,(select count(*) from xcloud_ap_info where ap_health=m) as counter from xcloud_ap_info ORDER BY counter DESC")
	results = g.cursor.fetchall()
	for row in results:
		ap = str(row[0])
		if(ap=="1"):
			tmp = "Good"
		elif(ap=="2"):
			tmp = "OK"
		else:
			tmp = "Unknown"
		xaxis.append(tmp)
		yaxis.append(row[1])
	return json.dumps([xaxis,yaxis])

def generateIP():
    blockOne = randrange(0, 255, 1)
    blockTwo = randrange(0, 255, 1)
    blockThree = randrange(0, 255, 1)
    blockFour = randrange(0, 255, 1)
    return str(blockOne) + '.' + str(blockTwo) + '.' + str(blockThree) + '.' + str(blockFour)
    if blockOne == 10:
        return generateRandomIP()
    elif blockOne == 172:
        return generateRandomIP()
    elif blockOne == 192:
        return generateRandomIP()
    else:
        return str(blockOne) + '.' + str(blockTwo) + '.' + str(blockThree) + '.' + str(blockFour)

def randomMAC():
	mac = [ 0x00, 0x16, 0x3e,
		random.randint(0x00, 0x7f),
		random.randint(0x00, 0xff),
		random.randint(0x00, 0xff) ]
	return (':'.join(map(lambda x: "%02x" % x, mac))).upper()

@app.route('/ap_simulator', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def ap_simulator():
	info = []
	model = ["Xi-1","Xi-2","Xi-3","Xo-1"]
	ap_name = "Cloud Manager"
	if request.method == 'POST':
		json_data = request.get_json()
		xtenant = json_data['xtenant']
		ap_count = int(json_data['ap_count'])
		xi_1 = int(json_data['xi_1'])
		xi_2 = int(json_data['xi_2'])
		xi_3 = int(json_data['xi_3'])
		xo_1 = int(json_data['xo_1'])
		for m in model:
			ap_name = "Cloud Manager - "+str(m)
			if(m=="Xi-1"):
				ap_count = xi_1
			elif(m=="Xi-2"):
				ap_count = xi_2
			elif(m=="Xi-3"):
				ap_count = xi_3
			elif(m=="Xo-1"):
				ap_count = xo_1
			for i in range(ap_count):
				apstats = {}
				ap_serial = random.randrange(100000000000,999999999999)
				apstats["ap_cc_set"] = int(1)
				apstats["update_time "] = int(1440989442)
				apstats["ap_rad0_cw "] = str("20")
				apstats["ap_ip"] = generateIP()
				apstats["create_time"] = int(1439270819)
				apstats["custom_tags"] = [str(m)]
				apstats["ap_serial"] = int(ap_serial)
				apstats["ap_rad1_ch"] = str("0")
				apstats["is_modified"] = int(0)
				apstats["networks"] = []
				apstats["ap_mac"] = str(randomMAC())
				apstats["last_heard"] = int(1440989442)
				apstats["ap_name"] = str(ap_name)
				apstats["ap_cc"] = str("US")
				apstats["xtenant"] = str(xtenant)
				apstats["is_deleted"] = int(0)
				apstats["ap_rad0_ch"] = str("0")
				apstats["ap_rad1_cw"] = str("20")
				apstats["ap_model "] = str(m)
				#print apstats
				info.append(apstats)
	return json.dumps(info)
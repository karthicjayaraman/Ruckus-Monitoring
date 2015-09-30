from xcloud_api import *

@app.route('/')
def show_home():
    return redirect("/index.html", code=302)

@app.route('/check_session', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def check_session():
  status = ""
  if session.get('username'):
      status = "0"
  else:
     status = "5"
  return status

@app.route('/get_username', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def get_username():
  status = ""
  output = {}
  if session.get('username'):
      output = {"status":"0","username":session['username'],"userid":str(session['userid'])}
  else:
      output = {"status":"1"}
  return json.dumps(output)


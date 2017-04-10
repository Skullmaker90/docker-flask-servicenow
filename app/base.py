from flask import Flask, request, session, jsonify

from flask_session import Session
from flask_cors import CORS

from Servicenow import Servicenow

app = Flask(__name__)
app.secret_key = 'SECRET_KEY'
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)
CORS(app, supports_credentials=True)

def get_auth(user, passwd):
    SN = Servicenow()
    r = SN.authenticate(user, passwd)
    if r:
      return SN
    else:
      return False

@app.route('/', methods=['GET', 'POST', 'PUT'])
def index():
    if request.method == 'GET':
       if not 'username' in session:
           return jsonify('User not Authenticated')
       return jsonify('User Authenticated, please POST with query')
    if request.method == 'POST':
       SN = get_auth(session.get('username'), session('passwd'))
       r = SN.get('?sysparm_query=' + request.form['query'])
       return jsonify(r.json())
    if request.method == 'PUT':
       SN = get_auth(session.get('username'), session('passwd'))
       items = [item['sys_id'] for item in SN.get('?sysparm_query=' + request.json['query']).json()['result']]
       data = request.json['data']
       for _id in items:
           SN.put('/' + _id, data)
       return jsonify('Success'), 200

@app.route('/login', methods=['POST'])
def login():
    user = request.form['username']
    passwd = request.form['password']
    if Servicenow().authenticate(user, passwd):
        session['username'] = user
        session['passwd'] = passwd
        return jsonify('Success'), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

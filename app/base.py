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

def check_auth(user, passwd):
    response = Servicenow().authenticate(user, passwd)
    return response

def get_auth(user, passwd):
    SN = Servicenow()
    SN.authenticate(user, passwd)
    return SN

@app.route('/', methods=['GET', 'POST', 'PUT'])
def index():
    if not 'username' in session:
        return jsonify({'status_code': 401, 'User not authenticated': ''})
    if request.method == 'GET':
        return jsonify({'status_code': 204, 'User authenticated': ''})
    if request.method == 'POST':
        r = session['callback'].get('?sysparm_query=' + request.form['query'])
        return jsonify(r.json())
    if request.method == 'PUT':
        items = [item['sys_id'] for item in session['callback'].get('?sysparm_query=' + request.json['query']).json()['result']]
        data = request.json['data']
        for _id in items:
            SN.put('/' + _id, data)
        return jsonify({'status_code': 200, 'Success': ''})

@app.route('/login', methods=['POST'])
def login():
    user, passwd = request.form['username'], request.form['password']
    is_success = check_auth(user, passwd)
    if is_success['status_code'] == 200:
        session['username'] = user
        session['password'] = passwd
        session['callback'] = get_auth(session['username'], session['password'])
    return jsonify(is_success)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

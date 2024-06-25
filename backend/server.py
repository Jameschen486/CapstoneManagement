from flask import Flask, request, jsonify
from flask_cors import CORS
# from flask_mysqldb import MySQL
import groups

from authentication import login, register

app = Flask(__name__)
# CORS(app)
# mysql = MySQL()

# app.config['MYSQL_DATABASE_DB'] = 'projdb'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# app.config['MYSQL_DATABASE_PORT'] = '5002'
# mysql.init_app(app)

MAX_STUDENT_PER_GROUP = 6


@app.route('/')
def home():
    return "TEST"

@app.post('/login')
def auth_login():
    email = request.form['email']
    password = request.form['password']
    return jsonify(login(email, password))

@app.post('/register')
def auth_register():
    email = request.form['email']
    password = request.form['password']
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    return jsonify(register(email, password, firstName, lastName))

@app.route('/group/create', methods=['POST'])
def create_group_endpoint():
    data = request.form
    group_name = data.get('name')
    group_description = data.get('description')
    creator_id = data.get('creator_id')

    response, status_code = groups.create_group(group_name, group_description, creator_id)
    return jsonify(response), status_code

@app.route('/groups/view', methods=['GET'])
def view_groups_route():
    return jsonify(groups.view_groups())

@app.route('/group/join', methods=['POST'])
def join_group_route():
    data = request.form
    group_id = data.get('group_id')
    student_id = data.get('student_id')
    response, status_code = groups.join_group(group_id, student_id, MAX_STUDENT_PER_GROUP)
    return jsonify(response), status_code

@app.route('/group/request/handle', methods=['POST'])
def handle_join_request_route():
    data = request.form
    creator_id = data.get('creator_id')
    applicant_id = data.get('applicant_id')
    group_id = data.get('group_id')
    accept = data.get('accept', 'false').lower() == 'true'
    response, status_code = groups.handle_join_request(creator_id, applicant_id, group_id, accept, MAX_STUDENT_PER_GROUP)
    return jsonify(response), status_code

@app.route('/group/', methods=['GET'])
def view_group_details_route():
    group_id = request.args.get('group_id')
    response, status_code = groups.view_group_details(group_id)
    return jsonify(response), status_code

@app.route('/user/join_requests', methods=['GET'])
def view_join_requests_route():
    user_id = request.args.get('user_id')
    response, status_code = groups.view_join_requests(user_id)
    return jsonify(response), status_code

@app.route('/group/leave', methods=['POST'])
def leave_group_route():
    data = request.form
    user_id = data.get('user_id')
    response, status_code = groups.leave_group(user_id)
    return jsonify(response), status_code

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5097)
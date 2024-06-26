from flask import Flask, request, jsonify
from flask_cors import CORS
# from flask_mysqldb import MySQL
import groups

from authentication import login, register, jwt_decode, return_user
from error import HTTPError
from projects import Project

app = Flask(__name__)
CORS(app)
# mysql = MySQL()

# app.config['MYSQL_DATABASE_DB'] = 'projdb'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# app.config['MYSQL_DATABASE_PORT'] = '5002'
# mysql.init_app(app)

MAX_STUDENT_PER_GROUP = 6

# ERROR HANDLER
@app.errorhandler(HTTPError)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

def authorization(token, requirement):
    # Have to remove prefix from standard format
    token = str(token).split()
    token = token[1]
    payload = jwt_decode(token)
    if payload is None:
        raise HTTPError("Invalid Signature", 401)
    if payload['role'] < requirement:
        raise HTTPError("Insufficent Privelage", 400)
    return True


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

@app.get('/user')
def get_user():
    token = request.authorization
    user = request.args['id']
    if authorization(token, 0):       
        return jsonify(return_user(user))

@app.route('/group/create', methods=['POST'])
def create_group_endpoint():
    data = request.form
    group_name = data.get('groupname')
    creator_id = data.get('ownerid')
    response, status_code = groups.create_group(group_name, creator_id)
    return jsonify(response), status_code

@app.route('/groups/view', methods=['GET'])
def view_groups_route():
    return jsonify(groups.view_groups())

@app.route('/group/join', methods=['POST'])
def join_group_route():
    data = request.form
    group_id = data.get('groupid')
    student_id = data.get('userid')
    response, status_code = groups.join_group(group_id, student_id, MAX_STUDENT_PER_GROUP)
    return jsonify(response), status_code

@app.route('/group/request/handle', methods=['POST'])
def handle_join_request_route():
    data = request.form
    user_id = data.get('userid')
    applicant_id = data.get('applicantid')
    group_id = data.get('groupid')
    accept = data.get('accept')
    response, status_code = groups.handle_join_request(user_id, applicant_id, group_id, accept, MAX_STUDENT_PER_GROUP)
    return jsonify(response), status_code

@app.route('/group/', methods=['GET'])
def view_group_details_route():
    group_id = request.args.get('groupid')
    response, status_code = groups.view_group_details(group_id)
    return jsonify(response), status_code

@app.route('/user/join_requests', methods=['GET'])
def view_join_requests_route():
    user_id = request.args.get('userid')
    response, status_code = groups.view_join_requests(user_id)
    return jsonify(response), status_code

@app.route('/group/leave', methods=['POST'])
def leave_group_route():
    data = request.form
    user_id = data.get('userid')
    response, status_code = groups.leave_group(user_id)
    return jsonify(response), status_code

@app.route('/project/create', methods=['POST'])
def create_project_route():
    data = request.form
    owner_id = int(data['owner_id'])
    title = data['title']
    response, status_code = Project.create(title, owner_id)
    return jsonify(response), status_code

@app.route('/project/details', methods=['GET'])
def get_project_details_route():
    data = request.form
    user_id = int(data['user_id'])
    project_id = data.get('project_id', default=None, type=int)
    response, status_code = Project.get_details(project_id, user_id)
    return jsonify(response), status_code

@app.route('/project/update', methods=['PUT'])
def update_project_route():
    data = request.form
    response, status_code = Project.update(data)
    return jsonify(response), status_code

@app.route('/project/delete', methods=['DELETE'])
def delete_project_route():
    data = request.form
    user_id = int(data['user_id'])
    project_id = data.get('project_id', default=None, type=int)
    response, status_code = Project.delete(user_id, project_id)
    return jsonify(response), status_code
    

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
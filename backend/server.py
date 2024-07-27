from flask import Flask, request, jsonify
from flask_cors import CORS
# from flask_mysqldb import MySQL
import groups

from authentication import login, register, jwt_decode, return_user, auth_id, auth_role, updateUserRole, updateUserName
from error import HTTPError
from projects import Project
from skills import Skill
import preference
import message, channel

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

@app.post('/updateUserRole')
def update_user_role():
    email1 = request.form['email1']
    password = request.form['password']
    email2 = request.form['email2']
    role = request.form['role']
    return jsonify(updateUserRole(email1, password, email2, role))

@app.post('/updateUserName')
def update_user_name():
    email = request.form['email']
    password = request.form['password']
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    return jsonify(updateUserName(email, password, firstName,lastName))

@app.route('/group/create', methods=['POST'])
def create_group_endpoint():
    group_name = request.form['groupname']
    user_id = int(request.form['ownerid'])
    token = request.authorization
    if auth_id(token, user_id):
        response, status_code = groups.create_group(group_name, user_id)
        return jsonify(response), status_code

@app.route('/groups/view', methods=['GET'])
def view_groups_route():
    token = request.authorization
    if auth_role(token, 0):
        return jsonify(groups.view_groups())

@app.route('/group/join', methods=['POST'])
def join_group_route():
    data = request.form
    group_id = int(data.get('groupid'))
    user_id = int(data.get('userid'))
    token = request.authorization
    if auth_id(token, user_id):
        response, status_code = groups.join_group(group_id, user_id, MAX_STUDENT_PER_GROUP)
        return jsonify(response), status_code

@app.route('/group/request/handle', methods=['POST'])
def handle_join_request_route():
    data = request.form
    user_id = int(data.get('userid'))
    applicant_id = int(data.get('applicantid'))
    group_id = int(data.get('groupid'))
    accept = bool(data.get('accept'))
    token = request.authorization
    if auth_id(token, user_id):
        response, status_code = groups.handle_join_request(user_id, applicant_id, group_id, accept, MAX_STUDENT_PER_GROUP)
        return jsonify(response), status_code

@app.route('/group', methods=['GET'])
def view_group_details_route():
    group_id = int(request.args.get('groupid'))
    token = request.authorization
    if auth_role(token, 0):
        response, status_code = groups.view_group_details(group_id)
        return jsonify(response), status_code

@app.route('/user/join_requests', methods=['GET'])
def view_join_requests_route():
    user_id = int(request.args.get('userid'))
    token = request.authorization
    if auth_id(token, user_id):
        response, status_code = groups.view_join_requests(user_id)
        return jsonify(response), status_code

@app.route('/group/leave', methods=['POST'])
def leave_group_route():
    data = request.form
    user_id = int(data.get('userid'))
    token = request.authorization
    if auth_id(token, user_id): 
        response, status_code = groups.leave_group(user_id)
        return jsonify(response), status_code
    
@app.get('/user')
def get_user():
    token = request.authorization
    user = int(request.args['id'])
    if auth_role(token, 0):       
        return jsonify(return_user(user))

@app.route('/project/create', methods=['POST'])
def create_project_route():
    token = request.authorization
    data = request.form
    userid = int(data['userid'])
    ownerid = data.get('ownerid', default=None, type=int)
    title = data['title']
    if auth_id(token, userid): 
        response, status_code = Project.create(userid, ownerid, title)
        return jsonify(response), status_code

@app.route('/project/details', methods=['GET'])
def get_project_details_route():
    token = request.authorization
    data = request.form
    userid = int(data['userid'])
    projectid = data.get('projectid', default=None, type=int)
    if auth_id(token, userid): 
        response, status_code = Project.get_details(userid, projectid)
        return jsonify(response), status_code
    
@app.route('/projects/view', methods=['GET'])
def view_projects_route():
    token = request.authorization
    data = request.form
    userid = int(data['userid'])
    if auth_id(token, userid): 
        response, status_code = Project.view_all(userid)
        return jsonify(response), status_code

@app.route('/project/update', methods=['PUT'])
def update_project_route():
    token = request.authorization
    data = request.form
    userid = int(data['userid'])
    if auth_id(token, userid): 
        response, status_code = Project.update(data)
        return jsonify(response), status_code

@app.route('/project/delete', methods=['DELETE'])
def delete_project_route():
    token = request.authorization
    data = request.form
    userid = int(data['userid'])
    project_id = data.get('projectid', default=None, type=int)
    if auth_id(token, userid): 
        response, status_code = Project.delete(userid, project_id)
        return jsonify(response), status_code
    
@app.route('/skill/create', methods=['POST'])
def create_skill_route():
    token = request.authorization
    data = request.form
    userid = int(data['userid'])
    skillname = data.get('skillname', default=None)
    if auth_id(token, userid): 
        response, status_code = Skill.create(userid, skillname)
        return jsonify(response), status_code

@app.route('/skills/view', methods=['GET'])
def get_skill_details_route():
    token = request.authorization
    data = request.form
    userid = int(data['userid'])
    if auth_id(token, userid): 
        response, status_code = Skill.view(userid)
        return jsonify(response), status_code
    
@app.route('/skill/add/student', methods=['POST'])
def skill_add_student_route():
    token = request.authorization
    data = request.form
    userid = int(data['userid'])
    studentid = data.get('studentid', default=None, type=int)
    skillid = data.get('skillid', default=None, type=int)
    if auth_id(token, userid): 
        response, status_code = Skill.add_skill_student(userid, studentid, skillid)
        return jsonify(response), status_code

@app.route('/skills/view/student', methods=['GET'])
def skills_view_student_route():
    token = request.authorization
    data = request.form
    userid = int(data['userid'])
    studentid = data.get('studentid', default=None, type=int)
    if auth_id(token, userid): 
        response, status_code = Skill.view_skills_student(userid, studentid)
        return jsonify(response), status_code
    
@app.route('/skill/remove/student', methods=['DELETE'])
def skill_remove_student():
    token = request.authorization
    data = request.form
    userid = int(data['userid'])
    studentid = data.get('studentid', default=None, type=int)
    skillid = data.get('skillid', default=None, type=int)
    if auth_id(token, userid): 
        response, status_code = Skill.remove_skill_student(userid, studentid, skillid)
        return jsonify(response), status_code

@app.route('/skill/add/project', methods=['POST'])
def skill_add_project_route():
    token = request.authorization
    data = request.form
    userid = int(data['userid'])
    projectid = data.get('projectid', default=None, type=int)
    skillid = data.get('skillid', default=None, type=int)
    if auth_id(token, userid): 
        response, status_code = Skill.add_skill_project(userid, projectid, skillid)
        return jsonify(response), status_code

@app.route('/skills/view/project', methods=['GET'])
def skills_view_project_route():
    token = request.authorization
    data = request.form
    userid = int(data['userid'])
    projectid = data.get('projectid', default=None, type=int)
    if auth_id(token, userid): 
        response, status_code = Skill.view_skills_project(userid, projectid)
        return jsonify(response), status_code
    
@app.route('/skill/remove/project', methods=['DELETE'])
def skill_remove_project():
    token = request.authorization
    data = request.form
    userid = int(data['userid'])
    projectid = data.get('projectid', default=None, type=int)
    skillid = data.get('skillid', default=None, type=int)
    if auth_id(token, userid): 
        response, status_code = Skill.remove_skill_project(userid, projectid, skillid)
        return jsonify(response), status_code


@app.route('/preference/add', methods=['POST'])
def add_preference_route():
    data = request.form
    user_id = int(data.get('user_id'))
    project_ids = data.getlist('project_ids')
    ranks = data.getlist('ranks')
    token = request.authorization
    if auth_id(token, user_id): 
        response, status_code = preference.add_preference(user_id, [int(pid) for pid in project_ids], [int(rank) for rank in ranks])
        return jsonify(response), status_code

@app.route('/preference/edit', methods=['POST'])
def edit_preference_route():
    data = request.form
    user_id = int(data.get('user_id'))
    project_ids = data.getlist('project_ids')
    ranks = data.getlist('ranks')
    token = request.authorization
    if auth_id(token, user_id): 
        response, status_code = preference.edit_preference(user_id, project_ids, ranks)
        return jsonify(response), status_code

@app.route('/preference/view', methods=['GET'])
def view_preference_route():
    user_id = int(request.args.get('user_id'))
    student_id = int(request.args.get('student_id'))
    token = request.authorization
    if auth_id(token, user_id):
        role = return_user(user_id)["role"]
        response, status_code = preference.view_preference(user_id, student_id, role)
        return jsonify(response), status_code
    
@app.route('/group/channel', methods=['GET'])
def get_group_channel():
    token = request.authorization
    data = request.form
    userid = int(data['userid'])
    groupid = data.get('groupid', default=None, type=int)
    
    if auth_id(token, userid): 
        response, status_code = channel.get_group_channelid(userid, groupid)
        return jsonify(response), status_code
    
@app.route('/project/channel', methods=['GET'])
def get_project_channel():
    token = request.authorization
    data = request.form
    userid = int(data['userid'])
    projectid = data.get('projectid', default=None, type=int)
    
    if auth_id(token, userid): 
        response, status_code = channel.get_project_channelid(userid, projectid)
        return jsonify(response), status_code

@app.route('/channel/messages', methods=['GET'])
def get_channel_messages():
    token = request.authorization
    data = request.form
    userid = int(data['userid'])
    channelid = data.get('channelid', default=None, type=int)
    last_message = data.get('last_message', default=None, type=int)
    
    if auth_id(token, userid): 
        response, status_code = channel.view_message(userid, channelid, last_message)
        return jsonify(response), status_code

@app.route('/message/send', methods=['POST'])
def send_message_route():
    token = request.authorization
    data = request.form
    userid = int(data['userid'])
    content = data.get('content', default=None, type=str)
    senderid = data.get('senderid', default=None, type=int)
    channelid = data.get('channelid', default=None, type=int)
    
    if auth_id(token, userid): 
        response, status_code = message.send(userid, content, senderid, channelid)
        return jsonify(response), status_code
    
@app.route('/message/edit', methods=['PUT'])
def edit_message_route():
    token = request.authorization
    data = request.form
    userid = int(data['userid'])
    content = data.get('content', default=None, type=str)
    msgid = data.get('messageid', default=None, type=int)
    
    if auth_id(token, userid): 
        response, status_code = message.edit(userid, msgid, content)
        return jsonify(response), status_code

@app.route('/message/delete', methods=['DELETE'])
def delete_message_route():
    token = request.authorization
    data = request.form
    userid = int(data['userid'])
    msgid = data.get('messageid', default=None, type=int)
    
    if auth_id(token, userid): 
        response, status_code = message.delete(userid, msgid)
        return jsonify(response), status_code





if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)

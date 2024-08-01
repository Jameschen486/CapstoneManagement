from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message
# from flask_mysqldb import MySQL
import groups
import notifications

from authentication import login, register, jwt_decode, return_user, auth_id, auth_role, updateUserRole, updateUserName, auth_password_reset, auth_reset_request, updateUserEmailRequest, updateUserEmail
from error import HTTPError
from projects import Project
from skills import Skill
from flask_mail import Mail, Message
import preference
from algorithms import allocate
import permission
import message, channel
import sys

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'capstone.managementdemo@gmail.com'
app.config['MAIL_PASSWORD'] = 'qcln cwre sqli oyqq'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'capstone.managementdemo@gmail.com'
mail = Mail(app)
CORS(app)
# mysql = MySQL()

# app.config['MYSQL_DATABASE_DB'] = 'projdb'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# app.config['MYSQL_DATABASE_PORT'] = '5002'
# mysql.init_app(app)

MAX_STUDENT_PER_GROUP = 6

def make_res_code(res, code):
  ret_res = {"message": res}
  return jsonify(ret_res), code

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
    try:
        role = int(request.form.get('role', default=0))
    except:
        role = 0
    return jsonify(register(email, password, firstName, lastName, role))

@app.post('/updateUserRole')
def update_user_role():
    email1 = request.form['email1']
    password = request.form['password']
    email2 = request.form['email2']
    role = request.form['role']
    return jsonify(updateUserRole(email1, password, email2, role))

@app.post('/updateUserName')
def update_user_name():
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    user_id = int(request.form['user_id'])
    token = request.authorization
    if auth_id(token, user_id):
        response, status_code = updateUserName(user_id,firstName,lastName)
        return jsonify(response), status_code


@app.post('/auth_reset_request')
def request_password_reset():
    email = request.form['email']
    return jsonify(auth_reset_request(email, mail))


@app.post('/auth_password_reset')
def reset_password():
    email = request.form['email']
    reset_code = request.form['reset_code']
    new_password = request.form['new_password']
    return jsonify(auth_password_reset(email, reset_code, new_password))


@app.post('/updateUserEmailRequest')
def request_email_reset_req():
    email = request.form['email']
    newEmail = request.form['newEmail']
    return jsonify(updateUserEmailRequest(email, newEmail, mail))


@app.post('/updateUserEmail')
def request_email_reset():
    email = request.form['email']
    newEmail = request.form['newEmail']
    reset_code = request.form['reset_code']
    return jsonify(updateUserEmail(email, newEmail, reset_code))


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
    accept = data.get('accept').lower() == 'true'
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
      
@app.route('/group/assign_project', methods=['PUT'])
def group_assign_project_route():
  """ Assigns project to group
      Does nothing if group is already assigned
  
  Form data:
    groupid (int)
    projectid (int)
    
  Responses:
    200, ok / project already assigned
    400, invalid groupid or projectid
    401, No token given
    403, Not enough permissions
    500, likely failed sql transaction
  """
  tok = request.authorization
  if tok == None:
    return make_res_code("No token given", 401)
  
  data = request.form
  
  try:
    gid = int(data.get('groupid'))
  except ValueError:
    return make_res_code("Malformed input, groupid not int", 400)
  
  try:
    pid = int(data.get('projectid'))
  except ValueError:
    return make_res_code("Malformed input, project not int", 400)
  
  try: 
    auth_role(tok, permission.Role.ADMIN, permission.Role.COORDINATOR)
  except:
    return make_res_code("Insufficient permissions", 403)
  
  res, status_code = groups.assign_project(gid, pid)
  return jsonify(res), status_code
    
@app.route('/group/unassign_project', methods=['PUT'])
def group_unassign_project_route():
  """ Unassigns project from group
      Does nothing if group has no assigned project
  
  Form data:
    groupid (int)
  
  Responses:
    200, ok / no project assigned
    400, Invalid groupid
    403, Not enough permissions
    500, likely failed sql transaction
  """
  tok = request.authorization
  if tok == None:
    return make_res_code("No token given", 401)
  data = request.form
  
  try:
    gid = int(data.get('groupid'))
  except ValueError:
    return make_res_code("Malformed input, groupid not int", 400)
  
  try:
    auth_role(tok, permission.Role.ADMIN, permission.Role.COORDINATOR)
  except:
    return make_res_code("Insufficient permissions", 403)
  
  res, status_code = groups.unassign_project(gid)
  return jsonify(res), status_code
    
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
    userid = request.args.get('userid', type=int)
    projectid  = request.args.get('projectid', default=None, type=int)
    if auth_id(token, userid): 
        response, status_code = Project.get_details(userid, projectid)
        return jsonify(response), status_code
    
@app.route('/projects/view', methods=['GET'])
def view_projects_route():
    token = request.authorization
    userid = request.args.get('userid', type=int)
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
    userid = request.args.get('userid', type=int)
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
    userid = request.args.get('userid', type=int)
    studentid = request.args.get('studentid', default=None, type=int)
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
    userid = request.args.get('userid', type=int)
    projectid  = request.args.get('projectid', default=None, type=int)
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
    
@app.route('/allocate/auto', methods=['GET', 'POST'])
def allocate_auto():
    for item in allocate():
        print(item, file=sys.stderr)
        groups.assign_project(item['group_id'], item['project_id'])
    return jsonify(allocate())
# def send_email():
#   msg = Message(
#     'Hello',
#     recipients=['chichun2002@gmail.com'],
#     body='This is a test email sent from Flask-Mail!'
#   )
#   mail.send(msg)
@app.route('/unallocate/auto', methods=['GET', 'POST'])
def unallocate_all():
    for group in groups.view_groups():
        groups.unassign_project(group[0])
    return 'True', 200


@app.route('/channel/io', methods=['PUT'])
def channel_manual_io():
    token = request.authorization
    data = request.form
    userid = int(data['userid'])
    target_userid = data.get('target_userid', default=None, type=int)
    channelid = data.get('channelid', default=None, type=int)
    io = data.get('io', default=None, type=str)
    
    if auth_id(token, userid): 
        response, status_code = channel.manual_io(userid, target_userid, channelid, io)
        return jsonify(response), status_code

@app.route('/group/channel', methods=['GET'])
def get_group_channel():
    token = request.authorization
    userid = request.args.get('userid', type=int)
    groupid  = request.args.get('groupid', default=None, type=int)
    
    if auth_id(token, userid): 
        response, status_code = channel.get_group_channelid(userid, groupid)
        return jsonify(response), status_code
    
@app.route('/project/channel', methods=['GET'])
def get_project_channel():
    token = request.authorization
    userid = request.args.get('userid', type=int)
    projectid  = request.args.get('projectid', default=None, type=int)
    
    if auth_id(token, userid): 
        response, status_code = channel.get_project_channelid(userid, projectid)
        return jsonify(response), status_code

@app.route('/users/channels', methods=['GET'])
def get_users_channel():
    """
    Warning: 
    get_users_channel() includes a channel -> user has access to that channel
    user has access to a channel !-> get_users_channel() includes that channel (e.g. TUTOR can access all channels)
    """
    token = request.authorization
    userid = request.args.get('userid', type=int)
    target_userid = request.args.get('target_userid', default=None, type=int)
    
    if auth_id(token, userid): 
        response, status_code = channel.get_users_channels(userid, target_userid)
        return jsonify(response), status_code

@app.route('/channel/messages', methods=['GET'])
def get_channel_messages():
    token = request.authorization
    userid = request.args.get('userid', type=int)
    channelid = request.args.get('channelid', default=None, type=int)
    last_message = request.args.get('last_message', default=None, type=int)
    latest_message = request.args.get('latest_message', default='false', type=str)
    
    if auth_id(token, userid): 
        response, status_code = channel.view_message(userid, channelid, last_message, latest_message)
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

@app.route('/notifications/view', methods=['GET'])
def view_notifications_route():
    token = request.authorization
    user_id = int(request.args.get('userid'))

    if auth_id(token, user_id):
        response, status_code = notifications.view_notifications(user_id)
        return jsonify(response), status_code
    
@app.route('/notification/view', methods=['GET'])
def view_individual_notification_route():
    token = request.authorization
    user_id = int(request.args.get('userid'))
    notif_id= int(request.args.get('notifid'))
    
    if auth_id(token, user_id):
        response, status_code = notifications.view_notification(user_id, notif_id)
        return jsonify(response), status_code
    
@app.route('/notification/delete', methods=['DELETE'])
def delete_notification_route():
    token = request.authorization
    data = request.args
    user_id = int(data.get('userid'))
    notif_id = int(data.get('notifid'))
    
    if auth_id(token, user_id):
        response, status_code = notifications.delete_notification(user_id, notif_id)
        return jsonify(response), status_code
    
@app.route('/notifications/delete', methods=['DELETE'])
def delete_notifications_route():
    token = request.authorization
    data = request.args
    user_id = int(data.get('userid'))

    if auth_id(token, user_id):
        response, status_code = notifications.delete_all_notifications(user_id)
        return jsonify(response), status_code


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)

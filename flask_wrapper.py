from flask import Flask, request, jsonify
from flask_cors import CORS
from src import groups
from users import login

MAX_STUDENT_PER_GROUP = 6

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "TEST"

@app.post('/aut/login')
def auth_login():
    username = request.form['username']
    password = request.form['password']
    return jsonify(login(username,password))

@app.route('/group/create', methods=['POST'])
def create_group_endpoint():
    data = request.form()
    group_name = data.get('name')
    group_description = data.get('description')
    creator_id = data.get('creator_id')

    response, status_code = groups.create_group(group_name, group_description, creator_id)
    return jsonify(response), status_code

@app.route('/group/view', methods=['GET'])
def view_groups_route():
    return jsonify(groups.view_groups())

@app.route('/group/join', methods=['POST'])
def join_group_route():
    data = request.form()
    group_id = data.get('group_id')
    student_id = data.get('student_id')
    response, status_code = groups.join_group(group_id, student_id, MAX_STUDENT_PER_GROUP)
    return jsonify(response), status_code

if __name__ == "__main__":
    app.run(debug=True)
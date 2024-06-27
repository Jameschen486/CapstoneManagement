from flask import Flask, request, jsonify
from flask_cors import CORS
# from flask_mysqldb import MySQL

from authentication import login, register
from projects import Project

app = Flask(__name__)
# CORS(app)
# mysql = MySQL()

# app.config['MYSQL_DATABASE_DB'] = 'projdb'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# app.config['MYSQL_DATABASE_PORT'] = '5002'
# mysql.init_app(app)


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
    app.run(debug=True, host='0.0.0.0', port=5100)
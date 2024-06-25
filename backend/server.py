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
    creator_id = data['user_id']
    name = data.get('name')
    response, status_code = Project.create(name, creator_id)
    return jsonify(response), status_code

@app.route('/project/update', methods=['PUT'])
def update_project_route():
    data = request.form
    response, status_code = Project.update(data)
    return jsonify(response), status_code

@app.route('/project/update', methods=['DELETE'])
def delete_project_route():
    data = request.form
    user_id = data['user_id']
    project_id = data.get('project_id')
    response, status_code = Project.delete(user_id, project_id)
    return jsonify(response), status_code

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5100)
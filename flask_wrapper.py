from flask import Flask, request, jsonify
from flask_cors import CORS

from users import login
from backend.projects import Project

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

@app.route('/project/create', methods=['POST'])
def create_project_route():
    data = request.form
    creator_id = data['creator_id']
    name = data.get('name')
    response, status_code = Project.create(name, creator_id)
    return jsonify(response), status_code

@app.route('/project/update', methods=['PUT'])
def update_project_route():
    data = request.form
    response, status_code = Project.update(data)
    return jsonify(response), status_code

    


if __name__ == "__main__":
    app.run(debug=True)
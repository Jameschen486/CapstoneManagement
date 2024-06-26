from flask import Flask, request, jsonify
from flask_cors import CORS
# from flask_mysqldb import MySQL

from authentication import login, register, jwt_decode, return_user
from error import HTTPError

app = Flask(__name__)
CORS(app)
# mysql = MySQL()

# app.config['MYSQL_DATABASE_DB'] = 'projdb'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# app.config['MYSQL_DATABASE_PORT'] = '5002'
# mysql.init_app(app)

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


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
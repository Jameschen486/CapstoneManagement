from flask import Flask, request, jsonify
from flask_cors import CORS

from authentication import login

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

if __name__ == "__main__":
    app.run(debug=True)
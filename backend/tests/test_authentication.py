import dbAcc
import authentication
import string
import pytest
import server
from permission import Role
from tests import helper
from error import HTTPError

client = helper.CLIENT

def clear_users():
  curs = dbAcc.conn.cursor()
  curs.execute("TRUNCATE users RESTART IDENTITY CASCADE")
  dbAcc.conn.commit()

user_d0 = [0, "admin@provider.com", "admin", "them", "adminPassword", 3]
user_d1 = [1, "Email@provider.com", "me", "them", "password", 0]
USERS = [
    {"email": f"Email@provider.com", "password": f"password", "firstName": f"James", "lastName": f"test"}
]
#
#   Update user role tests
#

# Successful test
def test_updateUserRole0():
    hashedPassword = authentication.getHashOf(user_d0[4])
    dbAcc.create_user(user_d0[1], hashedPassword, user_d0[2], user_d0[3], user_d0[5])
    dbAcc.create_user(user_d1[1], user_d1[4], user_d1[2], user_d1[3], user_d1[5])

    authentication.updateUserRole(user_d0[1], user_d0[4], user_d1[1], 1)
    user = dbAcc.get_user_by_email(user_d1[1])
    assert(user[5] == 1)
    clear_users()

# invalid email and passsword provided test
def test_updateUserRole1():

    hashedPassword = authentication.getHashOf(user_d0[4])

    try:
        dbAcc.create_user("incorrectemail@gmail.com", hashedPassword, user_d0[2], user_d0[3], user_d0[5])
    except HTTPError as e:
        assert e.status_code == 400

    dbAcc.create_user(user_d0[1], hashedPassword, user_d0[2], user_d0[3], user_d0[5])
    dbAcc.create_user(user_d1[1], user_d1[4], user_d1[2], user_d1[3], user_d1[5])

    try:
        authentication.updateUserRole(user_d0[1], "incorrectpassword", user_d1[1], 1)
    except HTTPError as e:
        assert e.status_code == 400

    try:
        authentication.updateUserRole(user_d0[1], user_d0[4], "randomemail@gmail.com", 1)
    except HTTPError as e:
        assert e.status_code == 400

    clear_users()

#
# Update user name tests
#

# Successful test
def test_updateUserName0():
    hashedPassword = authentication.getHashOf(user_d0[4])
    dbAcc.create_user(user_d0[1], hashedPassword, user_d0[2], user_d0[3], user_d0[5])
    authentication.updateUserName(user_d0[1], user_d0[4], "Joe", "Mama")
    user = dbAcc.get_user_by_email(user_d0[1])
    assert(user[2] == "Joe")
    assert(user[3] == "Mama")
    clear_users()

# test incorrect email and password
def test_updateUserName1():
    hashedPassword = authentication.getHashOf(user_d0[4])
    dbAcc.create_user(user_d0[1], hashedPassword, user_d0[2], user_d0[3], user_d0[5])

    try:
        authentication.updateUserName("incorrect email", user_d0[4], "Joe", "Mama")
    except HTTPError as e:
        assert e.status_code == 400

    try:
        authentication.updateUserName(user_d0[1], "incorrectpassword", "Joe", "Mama")
    except HTTPError as e:
        assert e.status_code == 400

    clear_users()

def test_reset_req0():

    user_info = USERS[0]
    client.post('/register', data = user_info)
    response = client.post('/login', data = user_info)
    token = response.json["token"]

    user = dbAcc.get_user_by_email("Email@provider.com")
    assert dbAcc.get_reset_code(user[0]) is None

    response = client.post('/auth_reset_request', data = {"email": "Email@provider.com"}, headers = helper.token2headers(token))
    reset_code = dbAcc.get_reset_code(user[0])
    assert reset_code is not None

    clear_users()

def test_reset0():

    user_info = USERS[0]
    client.post('/register', data = user_info)
    response = client.post('/login', data = user_info)
    token = response.json["token"]

    user = dbAcc.get_user_by_email("Email@provider.com")
    assert dbAcc.get_reset_code(user[0]) is None

    response = client.post('/auth_reset_request', data = {"email": "Email@provider.com"}, headers = helper.token2headers(token))
    reset_code = dbAcc.get_reset_code(user[0])
    assert reset_code is not None

    authentication.auth_password_reset("Email@provider.com", reset_code, "newPassword")
    reset_code = dbAcc.get_reset_code(user[0])
    assert reset_code is None

    user1 = dbAcc.get_user_by_email("Email@provider.com")
    hashedPassword = authentication.getHashOf("newPassword")
    assert user1[4] == hashedPassword

    clear_users()

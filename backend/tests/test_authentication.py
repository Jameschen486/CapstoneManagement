import dbAcc
import authentication
import string
from error import HTTPError

def clear_users():
  curs = dbAcc.conn.cursor()
  curs.execute("TRUNCATE users RESTART IDENTITY CASCADE")
  dbAcc.conn.commit()

user_d0 = [0, "admin@provider.com", "admin", "them", "adminPassword", 3]
user_d1 = [1, "Email@provider.com", "me", "them", "password", 0]
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

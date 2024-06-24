import hashlib
import random
import dbAcc
import dbAcc

class HTTPError(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message

def login(email, password) :
    user_login = None
    user = dbAcc.get_user_by_email(email)
    hashpass = getHashOf(password)

    if getHashOf(password) == user['password']:
        user_login = user
        token = str(random.randint(0, 500000))
        user['tokens'].append(token)
        return {
            'token': token,
            'authUserId': user_login['uId']
        }

    else:
        raise HTTPError(400, 'Invalid email or password, please try again')
def userRegister(email, password, firstName, lastName, role):

    user = dbAcc.get_user_by_email(email)
    if user['username'] == email:
        raise HTTPError(400, 'User already exists, please try login or reset password')
    else:
        hashedPassword = getHashOf(password)
        dbAcc.create_user(email, hashedPassword, firstName, lastName, role)
    return


def getHashOf(password):
    return hashlib.md5(password.encode()).hexdigest()
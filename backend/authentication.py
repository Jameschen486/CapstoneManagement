import hashlib
import random
import dbAcc
import dbAcc

def login(username, password) :
    data_store = getData()
    validUser = False
    user_login = None

    class HTTPError(Exception):
        def __init__(self, status_code, message):
            self.status_code = status_code
            self.message = message
            
    user = dbAcc.get_user_by_email(username)
    hashpass = getHashOf(password)

    if getHashOf(password) == user['password']:
        user_login = user
        validUser = True
        token = str(random.randint(0, 500000))
        user['tokens'].append(token)
        return {
            'token': token,
            'authUserId': user_login['uId']
        }

    else:
        raise HTTPError(400, 'Invalid login, try again')

def getHashOf(password):
    return hashlib.md5(password.encode()).hexdigest()
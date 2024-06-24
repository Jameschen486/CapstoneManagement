import hashlib
import random
import dbAcc
import dbAcc
import jwt

key = "rngwarriors"

def jwt_encode(payload):
    return jwt.encode(payload, key, algorithm="HS256")

def jwt_decode(token):
    try: 
        payload = jwt.decode(token, key, algorithms="HS256")
        return payload
    except:
        return None

class HTTPError(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message

def login(email, password) :
    user = dbAcc.get_user_by_email(email)
    if user is None:
        raise HTTPError(400, 'Invalid email or password, please try again')
    
    if getHashOf(password) == user[4]:
        payload = {
            'userid': user[0],
            'role': user[5]
        }
        token = jwt_encode(payload)
        return {
            'userid': user[0],
            'token': token
        }
    else:
        raise HTTPError(400, 'Invalid email or password, please try again')
    
def register(email, password, firstName, lastName, role=0):
    if dbAcc.get_user_by_email(email) is not None:

        raise HTTPError(400, 'User already exists, please try login or reset password')
    else:
        hashedPassword = getHashOf(password)
        dbAcc.create_user(email, hashedPassword, firstName, lastName, role)
    return


def getHashOf(password):
    return hashlib.md5(password.encode()).hexdigest()
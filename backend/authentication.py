import hashlib
import random
import dbAcc
import dbAcc
import jwt

from error import HTTPError

key = "rngwarriors"

def jwt_encode(payload):
    return jwt.encode(payload, key, algorithm="HS256")

def jwt_decode(token):
    try: 
        payload = jwt.decode(token, key, algorithms="HS256", options={"verify_signature": True})
    except:
        raise HTTPError("Invalid Signature", 401)
    return payload

def auth_role(token, role):
    # Have to remove prefix from standard format
    token = str(token).split()
    token = token[1]
    payload = jwt_decode(token)
    if payload['role'] != role:
        raise HTTPError("Insufficent Privelage", 400)
    return payload

def auth_id(token, id):
    # Have to remove prefix from standard format
    token = str(token).split()
    token = token[1]
    payload = jwt_decode(token)
    if payload['userid'] != id:
        raise HTTPError(f"{payload['userid']} != {id} {type(payload['userid'])} != {type(id)} Insufficent Privelage", 400)
    return payload


def login(email, password) :
    user = dbAcc.get_user_by_email(email)
    if user is None:
        raise HTTPError('Invalid email or password, please try again', 400)
    
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
        raise HTTPError('Invalid email or password, please try again', 400)
    
def register(email, password, firstName, lastName, role=0):
    if dbAcc.get_user_by_email(email) is not None:
        raise HTTPError('User already exists, please try login or reset password', 400)
    else:
        hashedPassword = getHashOf(password)
        dbAcc.create_user(email, hashedPassword, firstName, lastName, role)
    return

def return_user(id):
    user = dbAcc.get_user_by_id(id)
    if user is None:
        raise HTTPError(f'{id} User does not exsist', 400)
    return {"userid" : user.userid, "email" : user.email, "first_name" : user.first_name, "last_name" : user.last_name, "role" : user.role, "groupid" : user.groupid}


def getHashOf(password):
    return hashlib.md5(password.encode()).hexdigest()
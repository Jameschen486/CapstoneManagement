import hashlib
import random
import dbAcc
import dbAcc
import jwt

from error import HTTPError
from datetime import datetime
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

def auth_reset_request(email):
    user = dbAcc.get_user_by_email(email)
    if user is None:
        raise HTTPError('Invalid email or password, please try again', 400)

    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 6))
    timestamp = datetime.now()

    dbAcc.create_reset_code(user[0], code, timestamp)

    #setting email
    msg = EmailMessage()
    msg.set_content(f"""
Hello {user[2]},
your password reset code for streams is {code}.
If you did not make this request, you can ignore this email.""")

    msg['Subject'] = "Password reset for Capstone Management"
    msg['To'] = email
    msg['From'] = server_mail

    #sending email
    server = smtplib.SMTP('mail')
    server.send_message(msg)
    server.quit
    save_data()

    return

def auth_password_reset(email, reset_code, new_password):
    user = dbAcc.get_user_by_email(email)
    if (reset_code != dbAcc.get_reset_code(user[0])):
        raise HTTPError('Incorrect reset code, try again.', 400)

    hashedPassword = getHashOf(new_password)
    update_password(user[0], hashedPassword)
    dbAcc.remove_reset_code(user[0])
    return
import random
TEST_PASSWORD = "123"
TEST_USERNAME = "JOHN"
user_database = [
    {"email": TEST_USERNAME, "password": TEST_PASSWORD, "uId": 1}
]
def getData() :
    return {"users": user_database}

def login(username, password) :
    data_store = getData()
    validUser = False
    user_login = None
    class HTTPError(Exception):
        def __init__(self, status_code, message):
            self.status_code = status_code
            self.message = message
            
    for user in data_store['users']:
        if username == user['email'] and password == user['password']:
            user_login = user
            validUser = True
            break
    if not validUser:
        raise HTTPError(400, 'Invalid login, try again')
    
    token = str(random.randint(0, 500000))

    for user in data_store['users']:
        if user['uId'] == user_login['uId']:
            user['tokens'].append(token)
    
    return {
        'token': token,
        'authUserId': user_login['uId']
    }
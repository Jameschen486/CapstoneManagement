"""
Some functions assumed the admin has information ADMIN
"""
import dbAcc
import server
from permission import Role

CLIENT = server.app.test_client()

URL = 'http://localhost:5001'

TABLES = ["channels", "users", "projects", "groups", "grouprequests", "preferences", "notifications", "messages", "accesschannels"]

ADMIN = {"email": "admin_email", "password": "admin_password", "firstName": "admin_firstName", "lastName": "admin_lastName"} 

USERS = [
    {"email": f"email{i}", "password": f"password{i}", "firstName": f"firstName{i}", "lastName": f"lastName{i}"} 
    for i in range(10)
]

def truncate(table:str = None):
    curs = dbAcc.conn.cursor()

    if table is None:
        for table in TABLES:
            curs.execute(f"TRUNCATE {table} RESTART IDENTITY CASCADE")
    else:
        curs.execute(f"TRUNCATE {table} RESTART IDENTITY CASCADE")

    dbAcc.conn.commit()



def token2headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def get_admin() -> tuple:
    # TODO: Remove call of set_role(). He should be admin naturally
    CLIENT.post('/register', data = ADMIN)
    response = CLIENT.post('/login', data = ADMIN)

    set_role(response.json["userid"], Role.ADMIN)

    user_id = response.json["userid"]
    token = response.json["token"]

    return user_id, token


def create_user(index:int = 0, role:int = Role.STUDENT) -> tuple:
    # ensure admin exists
    CLIENT.post('/register', data = ADMIN)

    user_info = USERS[index]
    CLIENT.post('/register', data = user_info)
    response = CLIENT.post('/login', data = user_info)
    set_role(response.json["userid"], role)
    
    response = CLIENT.post('/login', data = user_info)
    user_id = response.json["userid"]
    token = response.json["token"]

    return user_id, token


def set_role(user_id:int, role:int = Role.STUDENT):
    """
    Note that the token of user changes as role changes,
    need to login again for the new token
    """
    # TODO: update role via admin instead
    dbAcc.update_role(user_id, role)





import dbAcc
import server

CLIENT = server.app.test_client()

URL = 'http://localhost:5001'

TABLES = ["channels", "users", "projects", "groups", "grouprequests", "preferences", "notifications", "messages", "accesschannels"]

USERS = [
    {"email": f"email{i}", "password": f"password{i}", "firstName": f"firstName{i}", "lastName": f"lastName{i}"} 
    for i in range(10)
]

def truncate(table:str = None):
    curs = dbAcc.conn.cursor()

    if table == None:
        for table in TABLES:
            curs.execute(f"TRUNCATE {table} RESTART IDENTITY CASCADE")
    else:
        curs.execute(f"TRUNCATE {table} RESTART IDENTITY CASCADE")

    dbAcc.conn.commit()


def get_user(index:int = 0) -> int:
    user_info = USERS[index]
    CLIENT.post('/register', data = user_info)
    user_id = CLIENT.post('/login', data = user_info).json["userid"]

    return user_id
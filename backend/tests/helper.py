"""
Some functions assumed the admin has information ADMIN
"""
import dbAcc
import server
from permission import Role

CLIENT = server.app.test_client()

URL = 'http://localhost:5001'

TABLES = ["channels", "users", "projects", "groups", "grouprequests", "preferences", "skills", "userskills", "projectskills", "resetcodes", "notifications", "messages", "accesschannels"]

ADMIN = {"email": "admin_email", "password": "admin_password", "firstName": "admin_firstName", "lastName": "admin_lastName"} 

USERS = [
    {"email": f"email{i}", "password": f"password{i}", "firstName": f"firstName{i}", "lastName": f"lastName{i}"} 
    for i in range(10)
]

SKILLS = [
    {"skillname": f"skill{i}"} 
    for i in range(10)
]

GROUP_NAMES = [
    f"group_name{i}" for i in range(10)
]

PORJECT_NAMES = [
    f"project_name{i}" for i in range(10)
]

def truncate(table:str = None):
    curs = dbAcc.conn.cursor()

    if table is None:
        for t in TABLES:
            curs.execute(f"TRUNCATE {t} RESTART IDENTITY CASCADE")
    else:
        curs.execute(f"TRUNCATE {t} RESTART IDENTITY CASCADE")

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


def create_skill(index:int = 0) -> int:
    admin_id, admin_token = get_admin()
    skill_id = CLIENT.post('/skill/create', data = {"userid":admin_id, "skillname":SKILLS[index]["skillname"]}, headers = token2headers(admin_token)).json["skillid"]
    return skill_id


def create_group(creator_id:int, creator_token:str, group_name:int = 0, member_indexs:list = []):
    if type(group_name) is int:
        group_name = GROUP_NAMES[group_name]

    group_id = CLIENT.post('/group/create', data = {"ownerid":creator_id, "groupname":group_name}, headers = token2headers(creator_token)).json["group_id"]
    for index in member_indexs:
        member_id, member_token = create_user(index)
        join_group(creator_id, creator_token, member_id, member_token, group_id)
        
    channel_id = CLIENT.get('/group/channel', data = {"groupid":group_id, "userid":creator_id}, headers = token2headers(creator_token)).json["channelid"]

    return group_id, channel_id


def create_project(creator_id:int, creator_token:str, title:int = 0, group_ids:list = []):
    if type(title) is int:
        title = PORJECT_NAMES[title]

    project_id = CLIENT.post('/porject/create', data = {"userid": creator_id, "ownerid":creator_id, "title":title}, headers = token2headers(creator_token)).json["projectid"]

    # TODO: assign project to groups

    channel_id = CLIENT.get('/project/channel', data = {"projectid":project_id, "userid":creator_id}, headers = token2headers(creator_token)).json["channelid"]

    return project_id, channel_id


def join_group(creator_id:int, creator_token:int, member_id:int, member_token:int, group_id:int):
    CLIENT.post('/group/join', data = {"groupid":group_id, "userid":member_id}, headers = token2headers(member_token))
    CLIENT.post('/group/request/handle', data = {"userid": creator_id, "applicantid": member_id, "groupid": group_id, "accept": True}, headers = token2headers(creator_token))


def view_message(channel_id:int, last_msg_id:int = None) -> list:
    id, token = get_admin()
    return CLIENT.get('/channel/messages', data = {"userid":id, "channelid": channel_id}, headers = token2headers(token)).json["messages"]
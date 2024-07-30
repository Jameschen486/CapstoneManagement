from algorithms import allocate
from tests import helper
from permission import Role

client = helper.CLIENT

def test():
    
    user = [0] * 9
    token = [0] * 9
    for i in range(9):
        user[i], token[i] = helper.create_user(i, role=Role.STUDENT)
    client_id, client_token = helper.create_user(9, role=Role.CLIENT)
    admin, admin_token = helper.create_user(10, role=Role.ADMIN)

    group_1 = client.post('/group/create', data={"groupname": "Test Group 1", "ownerid": user[0]}, headers = helper.token2headers(token[0])).get_json()['group_id']
    group_2 = client.post('/group/create', data={"groupname": "Test Group 2", "ownerid": user[3]}, headers = helper.token2headers(token[3])).get_json()['group_id']
    group_3 = client.post('/group/create', data={"groupname": "Test Group 3", "ownerid": user[6]}, headers = helper.token2headers(token[6])).get_json()['group_id']

    client.post('/group/join', data={"groupid": group_1, "userid": user[1]}, headers = helper.token2headers(token[1]))
    client.post('/group/join', data={"groupid": group_1, "userid": user[2]}, headers = helper.token2headers(token[2]))
    client.post('/group/join', data={"groupid": group_2, "userid": user[4]}, headers = helper.token2headers(token[4]))
    client.post('/group/join', data={"groupid": group_2, "userid": user[5]}, headers = helper.token2headers(token[5]))
    client.post('/group/join', data={"groupid": group_3, "userid": user[7]}, headers = helper.token2headers(token[7]))
    client.post('/group/join', data={"groupid": group_3, "userid": user[8]}, headers = helper.token2headers(token[8]))

    client.post('/group/request/handle', data={"userid": user[0], "applicantid": user[1], "groupid": group_1, "accept": True}, headers = helper.token2headers(token[0]))
    client.post('/group/request/handle', data={"userid": user[0], "applicantid": user[2], "groupid": group_1, "accept": True}, headers = helper.token2headers(token[0]))
    client.post('/group/request/handle', data={"userid": user[3], "applicantid": user[4], "groupid": group_2, "accept": True}, headers = helper.token2headers(token[3]))
    client.post('/group/request/handle', data={"userid": user[3], "applicantid": user[5], "groupid": group_2, "accept": True}, headers = helper.token2headers(token[3]))
    client.post('/group/request/handle', data={"userid": user[6], "applicantid": user[7], "groupid": group_3, "accept": True}, headers = helper.token2headers(token[6]))
    client.post('/group/request/handle', data={"userid": user[6], "applicantid": user[8], "groupid": group_3, "accept": True}, headers = helper.token2headers(token[6]))

    proj = [0]*3
    proj[0] = client.post('/project/create', data = {"userid":client_id, "ownerid":client_id, "title": "project_title0"}, headers = helper.token2headers(client_token)).get_json()['projectid']
    proj[1] = client.post('/project/create', data = {"userid":client_id, "ownerid":client_id, "title": "project_title1"}, headers = helper.token2headers(client_token)).get_json()['projectid']
    proj[2] = client.post('/project/create', data = {"userid":client_id, "ownerid":client_id, "title": "project_title2"}, headers = helper.token2headers(client_token)).get_json()['projectid']

    skill = [0] * 3
    for i in range(3):
        skill[i] = client.post('/skill/create', data = {"userid":admin, "skillname":f"skill_{i}"}, headers = helper.token2headers(admin_token)).get_json()['skillid']

    client.post('/skill/add/project', data = {"userid": client_id, "projectid": proj[0], "skillid": skill[2]}, headers = helper.token2headers(client_token))
    client.post('/skill/add/project', data = {"userid": client_id, "projectid": proj[0], "skillid": skill[1]}, headers = helper.token2headers(client_token))
    client.post('/skill/add/project', data = {"userid": client_id, "projectid": proj[1], "skillid": skill[0]}, headers = helper.token2headers(client_token))
    client.post('/skill/add/project', data = {"userid": client_id, "projectid": proj[1], "skillid": skill[2]}, headers = helper.token2headers(client_token))
    client.post('/skill/add/project', data = {"userid": client_id, "projectid": proj[1], "skillid": skill[1]}, headers = helper.token2headers(client_token))
    client.post('/skill/add/project', data = {"userid": client_id, "projectid": proj[2], "skillid": skill[2]}, headers = helper.token2headers(client_token))
    client.post('/skill/add/project', data = {"userid": client_id, "projectid": proj[2], "skillid": skill[1]}, headers = helper.token2headers(client_token))

    for i in range(9):
        client.post('/skill/add/student', data = {"userid": user[i], "studentid": user[i], "skillid": skill[(i^2)%3]}, headers = helper.token2headers(token[i]))
        client.post('/skill/add/student', data = {"userid": user[i], "studentid": user[i], "skillid": skill[(i^3)%3]}, headers = helper.token2headers(token[i]))

    client.post('/preference/add', data={"user_id": user[0], "project_ids": [proj[0], proj[1], proj[2]], "ranks": ["3", "2", "1"]}, headers=helper.token2headers(token[0]))
    client.post('/preference/add', data={"user_id": user[1], "project_ids": [proj[0], proj[1], proj[2]], "ranks": ["2", "1", "3"]}, headers=helper.token2headers(token[1]))
    client.post('/preference/add', data={"user_id": user[2], "project_ids": [proj[0], proj[1], proj[2]], "ranks": ["3", "2", "1"]}, headers=helper.token2headers(token[2]))
    client.post('/preference/add', data={"user_id": user[3], "project_ids": [proj[0], proj[1], proj[2]], "ranks": ["2", "1", "3"]}, headers=helper.token2headers(token[3]))
    client.post('/preference/add', data={"user_id": user[4], "project_ids": [proj[0], proj[1], proj[2]], "ranks": ["2", "1", "3"]}, headers=helper.token2headers(token[4]))
    client.post('/preference/add', data={"user_id": user[5], "project_ids": [proj[0], proj[1], proj[2]], "ranks": ["1", "2", "3"]}, headers=helper.token2headers(token[5]))
    client.post('/preference/add', data={"user_id": user[6], "project_ids": [proj[0], proj[1], proj[2]], "ranks": ["1", "2", "3"]}, headers=helper.token2headers(token[6]))
    client.post('/preference/add', data={"user_id": user[7], "project_ids": [proj[0], proj[1], proj[2]], "ranks": ["1", "3", "2"]}, headers=helper.token2headers(token[7]))
    client.post('/preference/add', data={"user_id": user[8], "project_ids": [proj[0], proj[1], proj[2]], "ranks": ["1", "2", "3"]}, headers=helper.token2headers(token[8]))
        
    print(client.get('/allocate/auto').get_json())
    # assert False
    
allocate()
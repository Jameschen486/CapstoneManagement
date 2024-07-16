from tests import helper
from permission import Role


def test_create_group():
    helper.truncate()
    user_id, token = helper.create_user(role=Role.STUDENT)
    
    response = helper.CLIENT.post('/group/create', data={"groupname": "Test Group", "ownerid": user_id}, headers = helper.token2headers(token))
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Group created successfully!"
    assert "group_id" in data

def test_view_groups():
    helper.truncate()
    user_id, token = helper.create_user(role=Role.STUDENT)
    helper.CLIENT.post('/group/create', data={"groupname": "Test Group", "ownerid": user_id}, headers = helper.token2headers(token))

    response = helper.CLIENT.get('/groups/view', headers = helper.token2headers(token))
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["groupname"] == "Test Group"

def test_join_group():
    helper.truncate()
    user_id, token = helper.create_user(role=Role.STUDENT)
    group_id = helper.CLIENT.post('/group/create', data={"groupname": "Test Group", "ownerid": user_id}, headers = helper.token2headers(token)).get_json()["group_id"]
    student_id, token2 = helper.create_user(role=Role.STUDENT)
    
    response = helper.CLIENT.post('/group/join', data={"groupid": group_id, "userid": student_id}, headers = helper.token2headers(token2))
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Join request sent successfully!"

def test_handle_join_request():
    helper.truncate()
    user_id, token = helper.create_user(role=Role.STUDENT)
    group_id = helper.CLIENT.post('/group/create', data={"groupname": "Test Group", "ownerid": user_id}, headers = helper.token2headers(token)).get_json()["group_id"]
    student_id, token2 = helper.create_user(role=Role.STUDENT)
    helper.CLIENT.post('/group/join', data={"groupid": group_id, "userid": student_id}, headers = helper.token2headers(token2))
    
    response = helper.CLIENT.post('/group/request/handle', data={"userid": user_id, "applicantid": student_id, "groupid": group_id, "accept": True}, headers = helper.token2headers(token))
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == f"User {student_id} added to your group."

def test_view_group_details():
    helper.truncate()
    user_id, token = helper.create_user(role=Role.STUDENT)
    group_id = helper.CLIENT.post('/group/create', data={"groupname": "Test Group", "ownerid": user_id}, headers = helper.token2headers(token)).get_json()["group_id"]
    
    response = helper.CLIENT.get('/group', query_string={"groupid": group_id}, headers = helper.token2headers(token))
    assert response.status_code == 200
    data = response.get_json()
    assert data["groupid"] == group_id
    assert data["groupname"] == "Test Group"

def test_view_join_requests():
    helper.truncate()
    user_id, token = helper.create_user(role=Role.STUDENT)
    group_id = helper.CLIENT.post('/group/create', data={"groupname": "Test Group", "ownerid": user_id}, headers = helper.token2headers(token)).get_json()["group_id"]
    student_id, token2 = helper.create_user(role=Role.STUDENT)
    helper.CLIENT.post('/group/join', data={"groupid": group_id, "userid": student_id}, headers = helper.token2headers(token2))
    
    response = helper.CLIENT.get('/user/join_requests', query_string={"userid": user_id}, headers = helper.token2headers(token))
    assert response.status_code == 200
    data = response.get_json()
    assert "join_requests" in data

def test_leave_group():
    helper.truncate()
    user_id, token = helper.create_user(role=Role.STUDENT)
    group_id = helper.CLIENT.post('/group/create', data={"groupname": "Test Group", "ownerid": user_id}, headers = helper.token2headers(token)).get_json()["group_id"]
    student_id, token2 = helper.create_user(role=Role.STUDENT)
    helper.CLIENT.post('/group/join', data={"groupid": group_id, "userid": student_id}, headers = helper.token2headers(token2))
    helper.CLIENT.post('/group/request/handle', data={"userid": user_id, "applicantid": student_id, "groupid": group_id, "accept": True}, headers = helper.token2headers(token))
    
    response = helper.CLIENT.post('/group/leave', data={"userid": student_id})
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "User has left the group"
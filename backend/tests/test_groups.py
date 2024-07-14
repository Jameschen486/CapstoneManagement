from tests.helper import CLIENT, truncate, get_user

def test_create_group():
    truncate()
    user_id = get_user(0)
    
    response = CLIENT.post('/group/create', data={"groupname": "Test Group", "ownerid": user_id})
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Group created successfully!"
    assert "group_id" in data

def test_view_groups():
    truncate()
    user_id = get_user(0)
    CLIENT.post('/group/create', data={"groupname": "Test Group", "ownerid": user_id})

    response = CLIENT.get('/groups/view')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["groupname"] == "Test Group"

def test_join_group():
    truncate()
    user_id = get_user(0)
    group_id = CLIENT.post('/group/create', data={"groupname": "Test Group", "ownerid": user_id}).get_json()["group_id"]
    student_id = get_user(1)
    
    response = CLIENT.post('/group/join', data={"groupid": group_id, "userid": student_id})
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Join request sent successfully!"

def test_handle_join_request():
    truncate()
    user_id = get_user(0)
    group_id = CLIENT.post('/group/create', data={"groupname": "Test Group", "ownerid": user_id}).get_json()["group_id"]
    student_id = get_user(1)
    CLIENT.post('/group/join', data={"groupid": group_id, "userid": student_id})
    
    response = CLIENT.post('/group/request/handle', data={"userid": user_id, "applicantid": student_id, "groupid": group_id, "accept": True})
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == f"User {student_id} added to your group."

def test_view_group_details():
    truncate()
    user_id = get_user(0)
    group_id = CLIENT.post('/group/create', data={"groupname": "Test Group", "ownerid": user_id}).get_json()["group_id"]
    
    response = CLIENT.get('/group', query_string={"groupid": group_id})
    assert response.status_code == 200
    data = response.get_json()
    assert data["groupid"] == group_id
    assert data["groupname"] == "Test Group"

def test_view_join_requests():
    truncate()
    user_id = get_user(0)
    group_id = CLIENT.post('/group/create', data={"groupname": "Test Group", "ownerid": user_id}).get_json()["group_id"]
    student_id = get_user(1)
    CLIENT.post('/group/join', data={"groupid": group_id, "userid": student_id})
    
    response = CLIENT.get('/user/join_requests', query_string={"userid": user_id})
    assert response.status_code == 200
    data = response.get_json()
    assert "join_requests" in data

def test_leave_group():
    truncate()
    user_id = get_user(0)
    group_id = CLIENT.post('/group/create', data={"groupname": "Test Group", "ownerid": user_id}).get_json()["group_id"]
    student_id = get_user(1)
    CLIENT.post('/group/join', data={"groupid": group_id, "userid": student_id})
    CLIENT.post('/group/request/handle', data={"userid": user_id, "applicantid": student_id, "groupid": group_id, "accept": True})
    
    response = CLIENT.post('/group/leave', data={"userid": student_id})
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "User has left the group"


print("1")
test_create_group()
print("2")
test_view_groups()
test_join_group()
test_handle_join_request()
test_view_group_details()
test_view_join_requests()
test_leave_group()
print("OK")
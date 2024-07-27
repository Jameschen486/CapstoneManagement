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
    assert data[0][1] == "Test Group"

def test_join_group():
    helper.truncate()
    user_id, token = helper.create_user(role=Role.STUDENT)
    group_id = helper.CLIENT.post('/group/create', data={"groupname": "Test Group", "ownerid": user_id}, headers = helper.token2headers(token)).get_json()["group_id"]
    student_id, token2 = helper.create_user(index=1, role=Role.STUDENT)
    
    response = helper.CLIENT.post('/group/join', data={"groupid": group_id, "userid": student_id}, headers = helper.token2headers(token2))
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Join request sent successfully!"

def test_handle_join_request():
    helper.truncate()
    user_id, token = helper.create_user(role=Role.STUDENT)
    group_id = helper.CLIENT.post('/group/create', data={"groupname": "Test Group", "ownerid": user_id}, headers = helper.token2headers(token)).get_json()["group_id"]
    student_id, token2 = helper.create_user(index=1, role=Role.STUDENT)
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
    student_id, token2 = helper.create_user(index=1, role=Role.STUDENT)
    helper.CLIENT.post('/group/join', data={"groupid": group_id, "userid": student_id}, headers = helper.token2headers(token2))
    
    response = helper.CLIENT.get('/user/join_requests', query_string={"userid": user_id}, headers = helper.token2headers(token))
    assert response.status_code == 200
    data = response.get_json()
    assert "join_requests" in data.keys()

def test_leave_group():
    helper.truncate()
    user_id, token = helper.create_user(role=Role.STUDENT)
    group_id = helper.CLIENT.post('/group/create', data={"groupname": "Test Group", "ownerid": user_id}, headers = helper.token2headers(token)).get_json()["group_id"]
    student_id, token2 = helper.create_user(index=1, role=Role.STUDENT)
    helper.CLIENT.post('/group/join', data={"groupid": group_id, "userid": student_id}, headers = helper.token2headers(token2))
    helper.CLIENT.post('/group/request/handle', data={"userid": user_id, "applicantid": student_id, "groupid": group_id, "accept": True}, headers = helper.token2headers(token))
    
    response = helper.CLIENT.post('/group/leave', data={"userid": student_id}, headers = helper.token2headers(token2))
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "User has left the group"

def test_leave_group_not_member():
    helper.truncate()
    student_id, token = helper.create_user(role=Role.STUDENT)
    
    response = helper.CLIENT.post('/group/leave', data={"userid": student_id}, headers=helper.token2headers(token))
    assert response.status_code == 403
    data = response.get_json()
    assert data["message"] == "User is not a member of any group"

def test_leave_group_last_member():
    helper.truncate()
    user_id, token = helper.create_user(role=Role.STUDENT)
    group_id = helper.CLIENT.post('/group/create', data={"groupname": "testgroup", "ownerid": user_id}, headers=helper.token2headers(token)).json["group_id"]
    assert group_id == 1
    response = helper.CLIENT.post('/group/leave', data={"userid": user_id}, headers=helper.token2headers(token))
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "User has left the group, group has been removed"

def test_leave_group_creator_with_members():
    helper.truncate()
    user_id, token = helper.create_user(role=Role.STUDENT)
    group_id = helper.CLIENT.post('/group/create', data={"groupname": "testgroup", "ownerid": user_id}, headers=helper.token2headers(token)).json["group_id"]
    
    member_id, token2 = helper.create_user(index = 1, role=Role.STUDENT)
    helper.CLIENT.post('/group/join', data={"groupid": group_id, "userid": member_id}, headers=helper.token2headers(token2))
    helper.CLIENT.post('/group/request/handle', data={"userid": user_id, "applicantid": member_id, "groupid": group_id, "accept": True}, headers=helper.token2headers(token))

    response = helper.CLIENT.post('/group/leave', data={"userid": user_id}, headers=helper.token2headers(token))
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "User has left the group"

    # Verify that the next member is now the group owner
    group_details = helper.CLIENT.get('/group', query_string={"groupid": group_id}, headers=helper.token2headers(token2)).json
    assert group_details["ownerid"] == member_id

def test_leave_group_member_not_creator():
    helper.truncate()
    user_id, token = helper.create_user(role=Role.STUDENT)
    group_id = helper.CLIENT.post('/group/create', data={"groupname": "testgroup", "ownerid": user_id}, headers=helper.token2headers(token)).json["group_id"]
    
    member_id, token2 = helper.create_user(index = 1, role=Role.STUDENT)
    helper.CLIENT.post('/group/join', data={"groupid": group_id, "userid": member_id}, headers=helper.token2headers(token2))
    helper.CLIENT.post('/group/request/handle', data={"userid": user_id, "applicantid": member_id, "groupid": group_id, "accept": True}, headers=helper.token2headers(token))

    response = helper.CLIENT.post('/group/leave', data={"userid": member_id}, headers=helper.token2headers(token2))
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "User has left the group"

    # Verify that the group still exists and the original creator is still the owner
    group_details = helper.CLIENT.get('/group', query_string={"groupid": group_id}, headers=helper.token2headers(token)).json
    assert group_details["ownerid"] == user_id
    assert len(group_details["group_members"]) == 1
    
def test_assign_unassign_project():
  #setup
  helper.truncate()
  aid, atok = helper.create_user(role=Role.ADMIN)
  uid, utok = helper.create_user(role=Role.STUDENT)
  res = helper.CLIENT.post('/group/create', data={"groupname": "a", "ownerid": uid}, headers=helper.token2headers(utok))
  data = res.get_json()
  gid = data["group_id"]
  oid, otok = helper.create_user(role=Role.CLIENT) 
  res = helper.CLIENT.post('/project/create', data = {"userid":oid, "ownerid":oid, "title":"project_title0"}, headers=helper.token2headers(otok))
  data = res.get_json()
  pid = data["projectid"]
  #assign working
  res = helper.CLIENT.put('/group/assign_project', data = {"groupid":gid, "projectid":pid}, headers=helper.token2headers(atok))
  data = res.get_json()
  assert res.status_code == 200
  res = helper.CLIENT.get('/group', query_string = {"groupid":gid}, headers = helper.token2headers(utok))
  data = res.get_json()
  assert data["project"] == pid
  
  #already assigned
  res = helper.CLIENT.put('/group/assign_project', data = {"groupid":gid, "projectid":pid}, headers=helper.token2headers(atok))
  assert res.status_code == 200
  
  #no token
  res = helper.CLIENT.put('/group/assign_project', data = {"groupid":gid, "projectid":pid})
  assert res.status_code == 401
  
  #bad groupid, not int, non existant
  res = helper.CLIENT.put('/group/assign_project', data = {"groupid":"foo", "projectid":pid},headers=helper.token2headers(atok))
  assert res.status_code == 400
  res = helper.CLIENT.put('/group/assign_project', data = {"groupid":-1, "projectid":pid}, headers=helper.token2headers(atok))
  assert res.status_code == 400
  
  #bad projectid, not int, non existant
  res = helper.CLIENT.put('/group/assign_project', data = {"groupid":gid, "projectid":"foo"},headers=helper.token2headers(atok))
  assert res.status_code == 400
  res = helper.CLIENT.put('/group/assign_project', data = {"groupid":gid, "projectid":-1}, headers=helper.token2headers(atok))
  assert res.status_code == 400
  
  #bad perms
  res = helper.CLIENT.put('/group/assign_project', data = {"groupid":gid, "projectid":pid}, headers=helper.token2headers(utok))
  assert res.status_code == 403
  
  #unassign working
  res = helper.CLIENT.put('/group/unassign_project', data = {"groupid":gid}, headers=helper.token2headers(atok))
  assert res.status_code == 200
  res = helper.CLIENT.get('/group', query_string = {"groupid":gid}, headers = helper.token2headers(utok))
  data = res.get_json()
  assert data["project"] == None
  
  #no project assigned
  res = helper.CLIENT.put('/group/unassign_project', data = {"groupid":gid}, headers=helper.token2headers(atok))
  assert res.status_code == 200
  
  #no token
  res = helper.CLIENT.put('/group/unassign_project', data = {"groupid":gid})
  assert res.status_code == 401
  
  #bad groupid, not int, non existant
  res = helper.CLIENT.put('/group/unassign_project', data = {"groupid":"a"}, headers=helper.token2headers(atok))
  assert res.status_code == 400
  res = helper.CLIENT.put('/group/unassign_project', data = {"groupid":-1}, headers=helper.token2headers(atok))
  assert res.status_code == 400
  
  #bad perms
  res = helper.CLIENT.put('/group/unassign_project', data = {"groupid":gid}, headers=helper.token2headers(utok))
  assert res.status_code == 403
  #failed sql transaction is hard to test for
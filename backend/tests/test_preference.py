from tests import helper
from permission import Role

def test_add_preference():

    helper.truncate()
    user_id, token = helper.create_user(role=Role.CLIENT)
    project_id1 = helper.CLIENT.post('/project/create', data={"userid": user_id, "ownerid": user_id, "title": "project_title1"}, headers=helper.token2headers(token)).json["projectid"]
    project_id2 = helper.CLIENT.post('/project/create', data={"userid": user_id, "ownerid": user_id, "title": "project_title2"}, headers=helper.token2headers(token)).json["projectid"]
    student_id, token2 = helper.create_user(index=1, role=Role.STUDENT)

    response = helper.CLIENT.post('/preference/add', data={
        "user_id": student_id,
        "project_ids": [str(project_id1), str(project_id2)],
        "ranks": ["1", "2"]
    }, headers=helper.token2headers(token2))
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Preferences added successfully!"


def test_edit_preference():

    helper.truncate()
    user_id, token = helper.create_user(role=Role.CLIENT)
    project_id1 = helper.CLIENT.post('/project/create', data={"userid": user_id, "ownerid": user_id, "title": "project_title1"}, headers=helper.token2headers(token)).json["projectid"]
    project_id2 = helper.CLIENT.post('/project/create', data={"userid": user_id, "ownerid": user_id, "title": "project_title2"}, headers=helper.token2headers(token)).json["projectid"]
    student_id, token2 = helper.create_user(index = 1, role=Role.STUDENT)

    # Add initial preferences
    helper.CLIENT.post('/preference/add', data={"user_id": student_id, "project_id": project_id1}, headers=helper.token2headers(token2))

    # Edit preferences
    response = helper.CLIENT.post('/preference/edit', data={
        "user_id": student_id,
        "project_ids": [project_id1, project_id2],
        "ranks": [2, 1]
    }, headers=helper.token2headers(token2))
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Preferences updated successfully!"

    # Check the rank actually has changed.
    response = helper.CLIENT.get('/preference/view', query_string={"user_id": student_id, "student_id": student_id}, headers=helper.token2headers(token2))
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert data[0]["project_id"] == project_id1
    assert data[0]["rank"] == 2
    assert data[1]["project_id"] == project_id2
    assert data[1]["rank"] == 1

def test_view_preference_as_student():

    helper.truncate()
    user_id, token = helper.create_user(role=Role.CLIENT)
    project_id = helper.CLIENT.post('/project/create', data={"userid": user_id, "ownerid": user_id, "title": "project_title"}, headers=helper.token2headers(token)).json["projectid"]
    student_id, token2 = helper.create_user(index=1, role=Role.STUDENT)
    helper.CLIENT.post('/preference/add', data={"user_id": student_id, "project_ids": [str(project_id)], "ranks": ["1"]}, headers=helper.token2headers(token2))

    # View preference as the student
    response = helper.CLIENT.get('/preference/view', query_string={"user_id": student_id, "student_id": student_id}, headers=helper.token2headers(token2))
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["project_id"] == project_id
    assert data[0]["rank"] == 1

def test_view_preference_as_client():

    helper.truncate()
    user_id, token = helper.create_user(role=Role.CLIENT)
    project_id = helper.CLIENT.post('/project/create', data={"userid": user_id, "ownerid": user_id, "title": "project_title"}, headers=helper.token2headers(token)).json["projectid"]
    student_id, token2 = helper.create_user(index = 1, role=Role.STUDENT)
    helper.CLIENT.post('/preference/add', data={"user_id": student_id, "project_ids": [str(project_id)], "ranks": ["1"]}, headers=helper.token2headers(token2))

    # View preference as a client
    response = helper.CLIENT.get('/preference/view', query_string={"user_id": user_id, "student_id": student_id}, headers=helper.token2headers(token))
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["project_id"] == project_id
    assert data[0]["rank"] == 1

def test_view_preference_insufficient_privilege():

    helper.truncate()
    user_id, token = helper.create_user(role=Role.CLIENT)
    project_id = helper.CLIENT.post('/project/create', data={"userid": user_id, "ownerid": user_id, "title": "project_title"}, headers=helper.token2headers(token)).json["projectid"]

    student_id, token2 = helper.create_user(index=1, role=Role.STUDENT)
    student_id2, token3 = helper.create_user(index=2, role=Role.STUDENT)
    helper.CLIENT.post('/preference/add', data={"user_id": student_id, "project_ids": [str(project_id)], "ranks": ["1"]}, headers=helper.token2headers(token2))

    # Attempt to view preference as a coordinator (insufficient privilege)
    response = helper.CLIENT.get('/preference/view', query_string={"user_id": student_id2, "student_id": student_id}, headers=helper.token2headers(token3))
    assert response.status_code == 403
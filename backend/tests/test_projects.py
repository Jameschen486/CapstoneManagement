from tests import helper
from premission import Role



client = helper.CLIENT


def test_create_1():
    helper.truncate()

    user_id, token = helper.create_user(role=Role.CLIENT)
    
    response = client.post('/project/create', data = {"userid":user_id, "ownerid":user_id, "title":"project_title"}, headers = helper.token2headers(token))
    assert response.status_code == 201
    project_id = response.json["projectid"]

    response = client.get('/project/details', data = {"userid":user_id, "projectid":project_id}, headers = helper.token2headers(token))
    assert response.status_code == 200
    json = response.json

    # info of the project is correct
    assert (
        json["projectid"] == project_id and
        json["ownerid"] == user_id and
        json["title"] == "project_title" and
        json["clients"] == None and
        json["specializations"] == None and
        json["groupcount"] == "0" and          # to be fixed
        json["background"] == None and
        json["requirements"] == None and
        json["reqknowledge"] == None and
        json["outcomes"] == None and
        json["supervision"] == None and
        json["additional"] == None and
        json["channel"] == None 
    )


def test_create_2():
    helper.truncate()

    user_id0, token0 = helper.create_user(0, Role.CLIENT)
    user_id1, token1 = helper.create_user(1, Role.CLIENT)
    
    project_id0 = client.post('/project/create', data = {"userid":user_id0, "ownerid":user_id0, "title":"project_title0"}, headers = helper.token2headers(token0)).json["projectid"]
    project_id1 = client.post('/project/create', data = {"userid":user_id0, "ownerid":user_id0, "title":"project_title1"}, headers = helper.token2headers(token0)).json["projectid"]
    project_id2 = client.post('/project/create', data = {"userid":user_id1, "ownerid":user_id1, "title":"project_title2"}, headers = helper.token2headers(token1)).json["projectid"]

    json0 = client.get('/project/details', data = {"userid":user_id0, "projectid":project_id0}, headers = helper.token2headers(token0)).json
    json1 = client.get('/project/details', data = {"userid":user_id0, "projectid":project_id1}, headers = helper.token2headers(token0)).json
    json2 = client.get('/project/details', data = {"userid":user_id1, "projectid":project_id2}, headers = helper.token2headers(token1)).json

    # info of projects are correct
    assert (
        json0["projectid"] == project_id0 and
        json0["ownerid"] == user_id0 and
        json0["title"] == "project_title0"
        and
        json1["projectid"] == project_id1 and
        json1["ownerid"] == user_id0 and
        json1["title"] == "project_title1"
        and
        json2["projectid"] == project_id2 and
        json2["ownerid"] == user_id1 and
        json2["title"] == "project_title2"
    )

    # user_1 can't access the project of user_2
    response = client.get('/project/details', data = {"userid":user_id1, "projectid":project_id0}, headers = helper.token2headers(token1))
    assert response.status_code == 403



def test_update():
    helper.truncate()

    user_id, token = helper.create_user(role=Role.CLIENT)
    project_id0 = client.post('/project/create', data = {"userid":user_id, "ownerid":user_id, "title":"project_title0"}, headers = helper.token2headers(token)).json["projectid"]
    project_id1 = client.post('/project/create', data = {"userid":user_id, "ownerid":user_id, "title":"project_title1"}, headers = helper.token2headers(token)).json["projectid"]

    response = client.put('/project/update', data = {"userid":user_id, "projectid":project_id0, "title":"new title"}, headers = helper.token2headers(token))
    assert response.status_code == 200
    assert response.json["projectid"] == project_id0

    json0 = client.get('/project/details', data = {"userid":user_id, "projectid":project_id0}, headers = helper.token2headers(token)).json
    json1 = client.get('/project/details', data = {"userid":user_id, "projectid":project_id1}, headers = helper.token2headers(token)).json
    
    # title altered
    assert json0["title"] == "new title"
    # title of another project not affected
    assert json1["title"] == "project_title1"

    # if there are duplicate titles, fail to alter
    response = client.put('/project/update', data = {"userid":user_id, "projectid":project_id1, "title":"new title"}, headers = helper.token2headers(token))
    assert response.status_code == 400
    assert json1["title"] == "project_title1"


def test_delete():
    helper.truncate()

    user_id0, token0 = helper.create_user(0, Role.CLIENT)
    project_id0 = client.post('/project/create', data = {"userid":user_id0, "ownerid":user_id0, "title":"project_title0"}, headers = helper.token2headers(token0)).json["projectid"]
    project_id1 = client.post('/project/create', data = {"userid":user_id0, "ownerid":user_id0, "title":"project_title1"}, headers = helper.token2headers(token0)).json["projectid"]
    user_id1, token1 = helper.create_user(1, Role.CLIENT)

    # can not delete others project
    response = client.delete('/project/delete', data = {"userid":user_id1, "projectid":project_id0}, headers = helper.token2headers(token1))
    assert response.status_code == 403
    assert client.get('/project/details', data = {"userid":user_id0, "projectid":project_id0}, headers = helper.token2headers(token0)).status_code == 200

    # project deleted
    response = client.delete('/project/delete', data = {"userid":user_id0, "projectid":project_id0}, headers = helper.token2headers(token0))
    assert response.status_code == 200
    assert client.get('/project/details', data = {"userid":user_id0, "projectid":project_id0}, headers = helper.token2headers(token0)).status_code == 400
    assert client.get('/project/details', data = {"userid":user_id0, "projectid":project_id1}, headers = helper.token2headers(token0)).status_code == 200

    # deleted project can not be updated
    response = client.put('/project/update', data = {"userid":user_id0, "projectid":project_id0, "title":"new title"}, headers = helper.token2headers(token0))
    assert response.status_code == 400


def test_premission_create():
    helper.truncate()
    
    client_id0, client_token0 = helper.create_user(0, Role.CLIENT)
    client_id1, client_token1 = helper.create_user(1, Role.CLIENT)
    student_id, student_token = helper.create_user(2, Role.STUDENT)
    tutor_id, tutor_token = helper.create_user(3, Role.TUTOR)
    coordinator_id, coordinator_token = helper.create_user(4, Role.COORDINATOR)
    admin_id, admin_token = helper.get_admin()

    ids = [client_id0, client_id1, student_id, tutor_id, coordinator_id, admin_id]
    tokens = [client_token0, client_token1, student_token, tutor_token, coordinator_token, admin_token]
    for i in range(len(ids)):
        for j in range(len(ids)):
            user_id = ids[i]
            owner_id = ids[j]
            response = client.post('/project/create', data = {"userid":user_id, "ownerid":owner_id, "title":f"project_title({i},{j})"}, headers = helper.token2headers(tokens[i]))

            if (
                # can not create project for non-client user
                owner_id not in [client_id0, client_id1] or
                # client can not create project for other clients

                {user_id, owner_id} == {client_id0, client_id1} or
                # user_id belongs to student or tutor
                user_id in [student_id, tutor_id]
            ):
                assert response.status_code == 403
            else:
                assert response.status_code == 201


def test_premission_2():
    helper.truncate()
    
    client_id0, client_token0 = helper.create_user(0, Role.CLIENT)
    client_id1, client_token1 = helper.create_user(1, Role.CLIENT)
    student_id, student_token = helper.create_user(2, Role.STUDENT)
    tutor_id, tutor_token = helper.create_user(3, Role.TUTOR)
    coordinator_id, coordinator_token = helper.create_user(4, Role.COORDINATOR)
    admin_id, admin_token = helper.get_admin()

    id2token = {client_id0:client_token0, client_id1:client_token1, student_id:student_token, tutor_id:tutor_token, coordinator_id:coordinator_token, admin_id:admin_token}

    project_id = client.post('/project/create', data = {"userid":client_id0, "ownerid":client_id0, "title":"project_title"}, headers = helper.token2headers(client_token0)).json["projectid"]

    # About view
    for user_id in [client_id1]:
        response = client.get('/project/details', data = {"userid":user_id, "projectid":project_id}, headers = helper.token2headers(id2token[user_id]))
        assert response.status_code == 403
    for user_id in [client_id0, student_id, tutor_id, coordinator_id, admin_id]:
        response = client.get('/project/details', data = {"userid":user_id, "projectid":project_id}, headers = helper.token2headers(id2token[user_id]))
        assert response.status_code == 200

    # About update
    for user_id in [client_id1, student_id, tutor_id]:
        response = client.put('/project/update', data = {"userid":user_id, "projectid":project_id, "title":f"title{user_id}"}, headers = helper.token2headers(id2token[user_id]))
        assert response.status_code == 403
    for user_id in [client_id0, coordinator_id, admin_id]:
        response = client.put('/project/update', data = {"userid":user_id, "projectid":project_id, "title":f"title{user_id}"}, headers = helper.token2headers(id2token[user_id]))
        assert response.status_code == 200

    # About delete
    for user_id in [client_id1, student_id, tutor_id]:
        response = client.delete('/project/delete', data = {"userid":user_id, "projectid":project_id}, headers = helper.token2headers(id2token[user_id]))
        assert response.status_code == 403
    for user_id in [client_id0, coordinator_id, admin_id]:
        response = client.delete('/project/delete', data = {"userid":user_id, "projectid":project_id}, headers = helper.token2headers(id2token[user_id]))
        assert response.status_code == 200
        # recreate the project
        project_id = client.post('/project/create', data = {"userid":client_id0, "ownerid":client_id0, "title":"project_title"}, headers = helper.token2headers(client_token0)).json["projectid"]
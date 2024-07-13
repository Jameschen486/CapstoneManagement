from tests import helper
import server


client = helper.CLIENT


def test_create_1():
    helper.truncate()

    user_id, token = helper.get_user()
    
    response = client.post('/project/create', data = {"ownerid":user_id , "title": "project_title"}, headers = helper.token2headers(token))
    assert response.status_code == 201
    project_id = response.json["projectid"]

    response = client.get('/project/details', data = {"userid":user_id , "projectid": project_id}, headers = helper.token2headers(token))
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

    user_id0, token0 = helper.get_user(0)
    user_id1, token1 = helper.get_user(1)
    
    project_id0 = client.post('/project/create', data = {"ownerid":user_id0, "title": "project_title0"}, headers = helper.token2headers(token0)).json["projectid"]
    project_id1 = client.post('/project/create', data = {"ownerid":user_id0, "title": "project_title1"}, headers = helper.token2headers(token0)).json["projectid"]
    project_id2 = client.post('/project/create', data = {"ownerid":user_id1, "title": "project_title2"}, headers = helper.token2headers(token1)).json["projectid"]

    json0 = client.get('/project/details', data = {"userid":user_id0, "projectid": project_id0}, headers = helper.token2headers(token0)).json
    json1 = client.get('/project/details', data = {"userid":user_id0, "projectid": project_id1}, headers = helper.token2headers(token0)).json
    json2 = client.get('/project/details', data = {"userid":user_id1, "projectid": project_id2}, headers = helper.token2headers(token1)).json

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
    response = client.get('/project/details', data = {"userid":user_id1, "projectid": project_id0}, headers = helper.token2headers(token1))
    assert response.status_code == 403



def test_update():
    helper.truncate()

    user_id, token = helper.get_user()
    project_id0 = client.post('/project/create', data = {"ownerid":user_id, "title": "project_title0"}, headers = helper.token2headers(token)).json["projectid"]
    project_id1 = client.post('/project/create', data = {"ownerid":user_id, "title": "project_title1"}, headers = helper.token2headers(token)).json["projectid"]

    response = client.put('/project/update', data = {"userid":user_id, "projectid": project_id0, "title": "new title"}, headers = helper.token2headers(token))
    assert response.status_code == 200
    assert response.json["projectid"] == project_id0

    json0 = client.get('/project/details', data = {"userid":user_id, "projectid": project_id0}, headers = helper.token2headers(token)).json
    json1 = client.get('/project/details', data = {"userid":user_id, "projectid": project_id1}, headers = helper.token2headers(token)).json
    
    # title altered
    assert json0["title"] == "new title"
    # title of another project not affected
    assert json1["title"] == "project_title1"

    # if there are duplicate titles, fail to alter
    response = client.put('/project/update', data = {"userid":user_id, "projectid": project_id1, "title": "new title"}, headers = helper.token2headers(token))
    assert response.status_code == 400
    assert json1["title"] == "project_title1"


def test_delete():
    helper.truncate()

    user_id0, token0 = helper.get_user(0)
    project_id0 = client.post('/project/create', data = {"ownerid":user_id0, "title": "project_title0"}, headers = helper.token2headers(token0)).json["projectid"]
    project_id1 = client.post('/project/create', data = {"ownerid":user_id0, "title": "project_title1"}, headers = helper.token2headers(token0)).json["projectid"]
    user_id1, token1 = helper.get_user(1)

    # can not delete others project
    response = client.delete('/project/delete', data = {"userid":user_id1, "projectid": project_id0}, headers = helper.token2headers(token1))
    assert response.status_code == 403
    assert client.get('/project/details', data = {"userid":user_id0, "projectid": project_id0}, headers = helper.token2headers(token0)).status_code == 200

    # project deleted
    response = client.delete('/project/delete', data = {"userid":user_id0, "projectid": project_id0}, headers = helper.token2headers(token0))
    assert response.status_code == 200
    assert client.get('/project/details', data = {"userid":user_id0, "projectid": project_id0}, headers = helper.token2headers(token0)).status_code == 400
    assert client.get('/project/details', data = {"userid":user_id0, "projectid": project_id1}, headers = helper.token2headers(token0)).status_code == 200

    # deleted project can not be updated
    response = client.put('/project/update', data = {"userid":user_id0, "projectid": project_id0, "title": "new title"}, headers = helper.token2headers(token0))
    assert response.status_code == 400

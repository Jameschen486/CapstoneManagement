from tests import helper
import server


client = helper.CLIENT


def test_create_1():
    helper.truncate()

    user_id = helper.get_user()
    
    response = client.post('/project/create', data = {"owner_id":user_id , "title": "project_title"})
    assert response.status_code == 201
    project_id = response.json["project_id"]

    response = client.get('/project/details', data = {"user_id":user_id , "project_id": project_id})
    assert response.status_code == 200
    json = response.json

    # info of the project is correct
    assert (
        json["project_id"] == project_id and
        json["owner_id"] == user_id and
        json["title"] == "project_title" and
        json["clients"] == None and
        json["specializations"] == None and
        json["group_count"] == "0" and          # to be fixed
        json["background"] == None and
        json["requirements"] == None and
        json["req_knowledge"] == None and
        json["outcomes"] == None and
        json["supervision"] == None and
        json["additional"] == None and
        json["channel"] == None 
    )


def test_create_2():
    helper.truncate()

    user_id0 = helper.get_user(0)
    user_id1 = helper.get_user(1)
    
    project_id0 = client.post('/project/create', data = {"owner_id":user_id0, "title": "project_title0"}).json["project_id"]
    project_id1 = client.post('/project/create', data = {"owner_id":user_id0, "title": "project_title1"}).json["project_id"]
    project_id2 = client.post('/project/create', data = {"owner_id":user_id1, "title": "project_title2"}).json["project_id"]

    json0 = client.get('/project/details', data = {"user_id":user_id0, "project_id": project_id0}).json
    json1 = client.get('/project/details', data = {"user_id":user_id0, "project_id": project_id1}).json
    json2 = client.get('/project/details', data = {"user_id":user_id1, "project_id": project_id2}).json

    # info of projects are correct
    assert (
        json0["project_id"] == project_id0 and
        json0["owner_id"] == user_id0 and
        json0["title"] == "project_title0"
        and
        json1["project_id"] == project_id1 and
        json1["owner_id"] == user_id0 and
        json1["title"] == "project_title1"
        and
        json2["project_id"] == project_id2 and
        json2["owner_id"] == user_id1 and
        json2["title"] == "project_title2"
    )

    # user_1 can't access the project of user_2
    response = client.get('/project/details', data = {"user_id":user_id1, "project_id": project_id0})
    assert response.status_code == 403



def test_update():
    helper.truncate()

    user_id = helper.get_user()
    project_id0 = client.post('/project/create', data = {"owner_id":user_id, "title": "project_title0"}).json["project_id"]
    project_id1 = client.post('/project/create', data = {"owner_id":user_id, "title": "project_title1"}).json["project_id"]

    response = client.put('/project/update', data = {"user_id":user_id, "project_id": project_id0, "title": "new title"})
    assert response.status_code == 200
    assert response.json["project_id"] == project_id0

    json0 = client.get('/project/details', data = {"user_id":user_id, "project_id": project_id0}).json
    json1 = client.get('/project/details', data = {"user_id":user_id, "project_id": project_id1}).json
    
    # title altered
    assert json0["title"] == "new title"
    # title of another project not affected
    assert json1["title"] == "project_title1"

    # if there are duplicate titles, fail to alter
    response = client.put('/project/update', data = {"user_id":user_id, "project_id": project_id1, "title": "new title"})
    assert response.status_code == 400
    assert json1["title"] == "project_title1"


def test_delete():
    helper.truncate()

    user_id0 = helper.get_user(0)
    project_id0 = client.post('/project/create', data = {"owner_id":user_id0, "title": "project_title0"}).json["project_id"]
    project_id1 = client.post('/project/create', data = {"owner_id":user_id0, "title": "project_title1"}).json["project_id"]
    user_id1 = helper.get_user(1)

    # can not delete others project
    response = client.delete('/project/delete', data = {"user_id":user_id1, "project_id": project_id0})
    assert response.status_code == 403
    assert client.get('/project/details', data = {"user_id":user_id0, "project_id": project_id0}).status_code == 200

    # project deleted
    response = client.delete('/project/delete', data = {"user_id":user_id0, "project_id": project_id0})
    assert response.status_code == 200
    assert client.get('/project/details', data = {"user_id":user_id0, "project_id": project_id0}).status_code == 400
    assert client.get('/project/details', data = {"user_id":user_id0, "project_id": project_id1}).status_code == 200

    # deleted project can not be updated
    response = client.put('/project/update', data = {"user_id":user_id0, "project_id": project_id0, "title": "new title"})
    assert response.status_code == 400

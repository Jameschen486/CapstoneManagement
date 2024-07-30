from tests import helper
from permission import Role
import pytest

client = helper.CLIENT
@pytest.fixture(autouse=True)
def run_around_tests():
    helper.truncate()
    yield
    helper.truncate()

def test_create_1():
    user_id, token = helper.create_user(role=Role.COORDINATOR)
    
    response = client.post('/skill/create', data = {"userid":user_id, "skillname":"skill_name"}, headers = helper.token2headers(token))
    assert response.status_code == 201
    skill_id = response.json["skillid"]

    response = client.get('/skills/view', query_string = {"userid":user_id}, headers = helper.token2headers(token))
    assert response.status_code == 200
    json = response.json

    # info of the skill is correct
    assert (
        json[str(skill_id)]["skillid"] == skill_id and
        json[str(skill_id)]["skillname"] == "skill_name"
    )


def test_create_2():
    admin_id, admin_token = helper.get_admin()
    coordinator_id, coordinator_token = helper.create_user(0, Role.COORDINATOR)
    student_id, student_token = helper.create_user(1, Role.STUDENT)

    skill_id0 = client.post('/skill/create', data = {"userid":admin_id, "skillname":"skill_admin"}, headers = helper.token2headers(admin_token)).json["skillid"]
    skill_id1 = client.post('/skill/create', data = {"userid":coordinator_id, "skillname":"skill_coordinator1"}, headers = helper.token2headers(coordinator_token)).json["skillid"]
    skill_id2 = client.post('/skill/create', data = {"userid":coordinator_id, "skillname":"skill_coordinator2"}, headers = helper.token2headers(coordinator_token)).json["skillid"]
    
    json_admin = client.get('/skills/view', query_string = {"userid":admin_id}, headers = helper.token2headers(admin_token)).json
    json_coordinator = client.get('/skills/view', query_string = {"userid":coordinator_id}, headers = helper.token2headers(coordinator_token)).json
    json_student = client.get('/skills/view', query_string = {"userid":student_id}, headers = helper.token2headers(student_token)).json


    # info of skills are correct, and they are accessible to everyone
    skill_key0 = str(skill_id0)
    skill_key1 = str(skill_id1)
    skill_key2 = str(skill_id2)

    assert (
        json_admin[skill_key0]["skillid"] == json_coordinator[skill_key0]["skillid"] == json_student[skill_key0]["skillid"] == skill_id0 and
        json_admin[skill_key0]["skillname"] == json_coordinator[skill_key0]["skillname"] == json_student[skill_key0]["skillname"] == "skill_admin"
        and
        json_admin[skill_key1]["skillid"] == json_coordinator[skill_key1]["skillid"] == json_student[skill_key1]["skillid"] == skill_id1 and
        json_admin[skill_key1]["skillname"] == json_coordinator[skill_key1]["skillname"] == json_student[skill_key1]["skillname"] == "skill_coordinator1"
        and
        json_admin[skill_key2]["skillid"] == json_coordinator[skill_key2]["skillid"] == json_student[skill_key2]["skillid"] == skill_id2 and
        json_admin[skill_key2]["skillname"] == json_coordinator[skill_key2]["skillname"] == json_student[skill_key2]["skillname"] == "skill_coordinator2"
    )


def test_student():
    skill_id0 = helper.create_skill(0)
    skill_id1 = helper.create_skill(1)
    student_id, student_token = helper.create_user(0, Role.STUDENT)
    tutor_id, tutor_token = helper.create_user(1, Role.TUTOR)

    response = client.post('/skill/add/student', data = {"userid": student_id, "studentid": student_id, "skillid": skill_id0}, headers = helper.token2headers(student_token))
    assert response.status_code == 201
    response = client.get('/skills/view/student', query_string = {"userid": student_id, "studentid": student_id}, headers = helper.token2headers(student_token))
    assert response.status_code == 200
    assert response.json[str(skill_id0)] == helper.SKILLS[0]["skillname"]

    response = client.post('/skill/add/student', data = {"userid": student_id, "studentid": student_id, "skillid": skill_id1}, headers = helper.token2headers(student_token))
    assert response.status_code == 201
    response = client.get('/skills/view/student', query_string = {"userid": tutor_id, "studentid": student_id}, headers = helper.token2headers(tutor_token))
    assert response.status_code == 200
    assert response.json[str(skill_id0)] == helper.SKILLS[0]["skillname"]
    assert response.json[str(skill_id1)] == helper.SKILLS[1]["skillname"]

    response = client.delete('/skill/remove/student', data = {"userid": student_id, "studentid": student_id, "skillid": skill_id0}, headers = helper.token2headers(student_token))
    assert response.status_code == 200
    response = client.get('/skills/view/student', query_string = {"userid": student_id, "studentid": student_id}, headers = helper.token2headers(student_token))
    assert response.status_code == 200
    assert str(skill_id0) not in response.json.keys()


def test_project():
    client_id, client_token = helper.create_user(1, Role.CLIENT)
    coordinator_id, coordinator_token = helper.create_user(4, Role.COORDINATOR)
    admin_id, admin_token = helper.get_admin()

    skill_id = helper.create_skill()

    project_id = client.post('/project/create', data = {"userid":client_id, "ownerid":client_id, "title":"project_title"}, headers = helper.token2headers(client_token)).json["projectid"]
    response = client.post('/skill/add/project', data = {"userid": coordinator_id, "projectid": project_id, "skillid": skill_id}, headers = helper.token2headers(coordinator_token))
    assert response.status_code == 201

    response = client.delete('/skill/remove/project', data = {"userid": admin_id, "projectid": project_id, "skillid": skill_id}, headers = helper.token2headers(admin_token))
    assert response.status_code == 200


def test_role():
    client_id0, client_token0 = helper.create_user(0, Role.CLIENT)
    client_id1, client_token1 = helper.create_user(1, Role.CLIENT)
    student_id, student_token = helper.create_user(2, Role.STUDENT)
    tutor_id, tutor_token = helper.create_user(3, Role.TUTOR)
    coordinator_id, coordinator_token = helper.create_user(4, Role.COORDINATOR)
    admin_id, admin_token = helper.get_admin()

    id2token = {client_id0:client_token0, client_id1:client_token1, student_id:student_token, tutor_id:tutor_token, coordinator_id:coordinator_token, admin_id:admin_token}
    project_id = client.post('/project/create', data = {"userid":client_id0, "ownerid":client_id0, "title":"project_title"}, headers = helper.token2headers(client_token0)).json["projectid"]
    skill_ids = []

    for user_id, user_token in id2token.items():
        response = client.post('/skill/create', data = {"userid":user_id, "skillname":f"skill_admin{user_id}"}, headers = helper.token2headers(user_token))
        
        if user_id in [coordinator_id, admin_id]:
            assert response.status_code == 201
            skill_ids.append(response.json["skillid"])
        else:
            assert response.status_code == 403


    for user_id, user_token in id2token.items():
        response = client.post('/skill/add/project', data = {"userid": user_id, "projectid": project_id, "skillid": skill_ids[0]}, headers = helper.token2headers(user_token))
        if user_id in [client_id0, coordinator_id, admin_id]:
            assert response.status_code == 201      # success
        else:
            assert response.status_code == 403      # student / other client can not add skill to project

        for target_id, _ in id2token.items():
            response = client.post('/skill/add/student', data = {"userid": user_id, "studentid": target_id, "skillid": skill_ids[1]}, headers = helper.token2headers(user_token))
            if target_id != student_id:
                assert response.status_code == 403
            elif user_id in [student_id, admin_id]:
                assert response.status_code == 201
            else:
                assert response.status_code == 403

        response = client.delete('/skill/remove/project', data = {"userid": admin_id, "projectid": project_id, "skillid": skill_ids[0]}, headers = helper.token2headers(admin_token))
        response = client.delete('/skill/remove/student', data = {"userid": admin_id, "studentid": student_id, "skillid": skill_ids[1]}, headers = helper.token2headers(admin_token))
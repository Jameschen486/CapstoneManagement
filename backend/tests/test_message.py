from tests import helper
from permission import Role
import pytest, dbAcc


client = helper.CLIENT
@pytest.fixture(autouse=True)
def run_around_tests():
    helper.truncate()
    yield
    helper.truncate()


def test_send_1():
    user_id, token = helper.create_user()
    group_id, channel_id = helper.create_group(user_id, token)

    response = client.post('/message/send', data = {"userid":user_id, "content":"content_str", "senderid":user_id, "channelid": channel_id}, headers = helper.token2headers(token))
    assert response.status_code == 201

    response = client.get('/channel/messages', query_string = {"userid":user_id, "channelid": channel_id}, headers = helper.token2headers(token))
    assert response.status_code == 200
    msgs = response.json["messages"]
    assert len(msgs) == 1
    assert msgs[0]["content"] == "content_str"

    
def test_send_2():
    user_id0, token0 = helper.create_user(0)
    user_id1, token1 = helper.create_user(1)
    user_id2, token2 = helper.create_user(2)
    group_id, channel_id = helper.create_group(user_id0, token0, member_indexs=[1])

    response = client.post('/message/send', data = {"userid":user_id0, "content":"content_str0", "senderid":user_id0, "channelid": channel_id}, headers = helper.token2headers(token0))
    assert response.status_code == 201
    response = client.post('/message/send', data = {"userid":user_id1, "content":"content_str1", "senderid":user_id1, "channelid": channel_id}, headers = helper.token2headers(token1))
    assert response.status_code == 201
    last_msg_id = response.json["messageid"]
    response = client.post('/message/send', data = {"userid":user_id2, "content":"content_str2", "senderid":user_id2, "channelid": channel_id}, headers = helper.token2headers(token2))
    assert response.status_code == 403

    response = client.get('/channel/messages', query_string = {"userid":user_id0, "channelid": channel_id}, headers = helper.token2headers(token0))
    assert response.status_code == 200
    msgs = response.json["messages"]
    assert len(msgs) == 2
    assert msgs[0]["content"] == "content_str1"
    assert msgs[1]["content"] == "content_str0"

    response = client.get('/channel/messages', query_string = {"userid":user_id1, "channelid": channel_id, "last_message": last_msg_id}, headers = helper.token2headers(token1))
    assert response.status_code == 200
    msgs = response.json["messages"]
    assert len(msgs) == 1
    assert msgs[0]["content"] == "content_str0"

    response = client.get('/channel/messages', query_string = {"userid":user_id2, "channelid": channel_id}, headers = helper.token2headers(token2))
    assert response.status_code == 403
    helper.join_group(user_id0, token0, user_id2, token2, group_id)
    response = client.get('/channel/messages', query_string = {"userid":user_id2, "channelid": channel_id, "latest_message":True}, headers = helper.token2headers(token2))
    assert response.status_code == 200
    msgs = response.json["messages"]
    assert len(msgs) == 1
    assert msgs[0]["content"] == "content_str1"



def test_edit():
    student_id, student_token = helper.create_user(0, Role.STUDENT)
    client_id, client_token = helper.create_user(1, Role.CLIENT)
    tutor_id, tutor_token = helper.create_user(2, Role.TUTOR)
    coordinator_id, coordinator_token = helper.create_user(3, Role.COORDINATOR)
    admin_id, admin_token = helper.get_admin()

    group_id, channel_id = helper.create_group(student_id, student_token)
    msg_id = client.post('/message/send', data = {"userid":admin_id, "content":"content_str", "senderid":student_id, "channelid": channel_id}, headers = helper.token2headers(admin_token)).json["messageid"]

    response = client.put('/message/edit', data = {"userid":student_id, "content":"content_str_student", "messageid": msg_id}, headers = helper.token2headers(student_token))
    assert response.status_code == 200
    assert helper.view_message(channel_id)[0]["content"] == "content_str_student"

    response = client.put('/message/edit', data = {"userid":client_id, "content":"content_str_client", "messageid": msg_id}, headers = helper.token2headers(client_token))
    assert response.status_code == 403
    assert helper.view_message(channel_id)[0]["content"] == "content_str_student"

    response = client.put('/message/edit', data = {"userid":tutor_id, "content":"content_str_tutor", "messageid": msg_id}, headers = helper.token2headers(tutor_token))
    assert response.status_code == 403
    assert helper.view_message(channel_id)[0]["content"] == "content_str_student"

    response = client.put('/message/edit', data = {"userid":coordinator_id, "content":"content_str_coordinator", "messageid": msg_id}, headers = helper.token2headers(coordinator_token))
    assert response.status_code == 200
    assert helper.view_message(channel_id)[0]["content"] == "content_str_coordinator"

    response = client.put('/message/edit', data = {"userid":admin_id, "content":"content_str_admin", "messageid": msg_id}, headers = helper.token2headers(admin_token))
    assert response.status_code == 200
    assert helper.view_message(channel_id)[0]["content"] == "content_str_admin"
    

def test_delete():
    user_id0, token0 = helper.create_user(0)
    user_id1, token1 = helper.create_user(1)
    user_id2, token2 = helper.create_user(2)
    group_id, channel_id = helper.create_group(user_id0, token0, member_indexs=[1])

    msg_id0 = client.post('/message/send', data = {"userid":user_id0, "content":"content_str0", "senderid":user_id0, "channelid": channel_id}, headers = helper.token2headers(token0)).json["messageid"]
    msg_id1 = client.post('/message/send', data = {"userid":user_id1, "content":"content_str1", "senderid":user_id1, "channelid": channel_id}, headers = helper.token2headers(token1)).json["messageid"]

    helper.join_group(user_id0, token0, user_id2, token2, group_id)
    client.post('/group/leave', data={"userid": user_id1}, headers = helper.token2headers(token1))

    response = client.get('/channel/messages', query_string = {"userid":user_id1, "channelid": channel_id}, headers = helper.token2headers(token1))
    assert response.status_code == 403
    response = client.get('/channel/messages', query_string = {"userid":user_id2, "channelid": channel_id}, headers = helper.token2headers(token2))
    assert response.json["messages"][0]["content"] == "content_str1"

    response = client.delete('/message/delete', data = {"userid": user_id2, "messageid": msg_id1}, headers = helper.token2headers(token2))
    assert response.status_code == 403
    assert helper.view_message(channel_id)[0]["content"] == "content_str1"

    admin_id, admin_token = helper.get_admin()
    response = client.delete('/message/delete', data = {"userid": admin_id, "messageid": msg_id1}, headers = helper.token2headers(admin_token))
    assert response.status_code == 200
    assert helper.view_message(channel_id)[0]["content"] == "content_str0"

    # TODO: allow owner of group to delete message
    #response = client.delete('/message/delete', data = {"userid": user_id0, "messageid": msg_id0}, headers = helper.token2headers(token0))
    #assert response.status_code == 200
    #assert len(helper.view_message(channel_id)) == 0


def test_project():
    admin_id, admin_token = helper.get_admin()
    student_id0, student_token0 = helper.create_user(0)
    student_id1, student_token1 = helper.create_user(1)
    student_id2, student_token2 = helper.create_user(2)
    client_id, client_token = helper.create_user(3, role=Role.CLIENT)
    

    group_id0, channel_id0 = helper.create_group(student_id0, student_token0, group_name=0)
    group_id1, channel_id1 = helper.create_group(student_id1, student_token1, group_name=1, member_indexs=[2])
    project_id, project_channel_id = helper.create_project(client_id, client_token, group_ids=[group_id0, group_id1])

    group_msg_id = client.post('/message/send', data = {"userid":student_id0, "content":"group_content_str", "senderid":student_id0, "channelid": channel_id0}, headers = helper.token2headers(student_token0)).json["messageid"]
    project_msg_id = client.post('/message/send', data = {"userid":student_id0, "content":"project_content_str", "senderid":student_id0, "channelid": project_channel_id}, headers = helper.token2headers(student_token0)).json["messageid"]
    response = client.post('/message/send', data = {"userid":student_id0, "content":"bad_content_str", "senderid":student_id0, "channelid": channel_id1}, headers = helper.token2headers(student_token0))
    assert response.status_code == 403

    assert helper.view_message(channel_id0)[0]["content"] == "group_content_str"
    assert helper.view_message(project_channel_id)[0]["content"] == "project_content_str"
    response = client.get('/channel/messages', query_string = {"userid":student_id1, "channelid": channel_id0}, headers = helper.token2headers(student_token1))
    assert response.status_code == 403
    response = client.get('/channel/messages', query_string = {"userid":student_id2, "channelid": project_channel_id}, headers = helper.token2headers(student_token2))
    assert response.json["messages"][0]["content"] == "project_content_str"

    response = client.post('/message/send', data = {"userid":client_id, "content":"group_content_str", "senderid":client_id, "channelid": project_channel_id}, headers = helper.token2headers(client_token))
    assert response.status_code == 201
    # TODO: allow owner of project to delete message
    #response = client.delete('/message/delete', data = {"userid": client_id, "messageid": project_msg_id}, headers = helper.token2headers(client_token))
    #assert response.status_code == 200

    response = client.get('/users/channels', query_string = {"userid":student_id0, "target_userid":student_id0}, headers = helper.token2headers(student_token0))
    assert response.status_code == 200
    assert set(helper.users_channel_ids(student_id0, student_token0)) == set([channel_id0, project_channel_id])
    assert set(helper.users_channel_ids(student_id2, student_token2)) == set([channel_id1, project_channel_id])
    assert set(helper.users_channel_ids(client_id, client_token)) == set([project_channel_id])
    assert set(helper.users_channel_ids(admin_id, admin_token)) == set([])


def test_manual_io_channel():
    admin_id, admin_token = helper.get_admin()
    student_id0, student_token0 = helper.create_user(0)
    student_id1, student_token1 = helper.create_user(1)
    student_id2, student_token2 = helper.create_user(2)
    client_id, client_token = helper.create_user(3, role=Role.CLIENT)

    group_id, channel_id = helper.create_group(student_id0, student_token0, group_name=0, member_indexs=[1])
    project_id, project_channel_id = helper.create_project(client_id, client_token, group_ids=[group_id])

    client.post('/group/leave', data={"userid": student_id1}, headers=helper.token2headers(student_token1))
    client.put('/channel/io', data={"userid": admin_id, "target_userid": student_id0, "channelid": channel_id, "io": "leave"}, headers=helper.token2headers(admin_token))
    assert set(helper.users_channel_ids(student_id0, student_token0)) == set([project_channel_id])
    assert set(helper.users_channel_ids(student_id1, student_token1)) == set([])

    helper.join_group(student_id0, student_token0, student_id2, student_token2, group_id)
    client.put('/channel/io', data={"userid": admin_id, "target_userid": student_id1, "channelid": project_channel_id, "io": "join"}, headers=helper.token2headers(admin_token))
    assert set(helper.users_channel_ids(student_id2, student_token2)) == set([channel_id, project_channel_id])
    assert set(helper.users_channel_ids(student_id1, student_token1)) == set([project_channel_id])









from tests import helper
from permission import Role
import dbAcc

def test_update_project_notification():

    helper.truncate()
    owner_id, token = helper.create_user(role=Role.ADMIN)
    project_data = {"userid": owner_id, "ownerid": owner_id, "title": "Initial Project Title"}
    project_id = helper.CLIENT.post('/project/create', data=project_data, headers=helper.token2headers(token)).json['projectid']

    student_id1, token2 = helper.create_user(index=1, role=Role.STUDENT)
    student_id2, token3 = helper.create_user(index=2, role=Role.STUDENT)
    student_id3, token4 = helper.create_user(index=3, role=Role.STUDENT)
    group_id = helper.CLIENT.post('/group/create', data={"groupname": "Test Group", "ownerid": student_id1}, headers = helper.token2headers(token2)).get_json()["group_id"]
    helper.CLIENT.post('/group/join', data={"groupid": group_id, "userid": student_id2}, headers = helper.token2headers(token3))
    helper.CLIENT.post('/group/request/handle', data={"userid": student_id1, "applicantid": student_id2, "groupid": group_id, "accept": True}, headers = helper.token2headers(token2))
    helper.CLIENT.post('/group/join', data={"groupid": group_id, "userid": student_id3}, headers = helper.token2headers(token4))
    helper.CLIENT.post('/group/request/handle', data={"userid": student_id1, "applicantid": student_id3, "groupid": group_id, "accept": True}, headers = helper.token2headers(token2))
    helper.CLIENT.put('/group/assign_project', data={"groupid": group_id, "projectid": project_id}, headers=helper.token2headers(token))
    res = helper.CLIENT.get('/group', query_string = {"groupid":group_id}, headers = helper.token2headers(token2))
    data = res.get_json()
    assert data["project"] == project_id
    assert dbAcc.get_assigned_users(project_id) == [student_id1, student_id2, student_id3]

    update_data = {"userid": owner_id,"projectid": project_id,"title": "Updated Project Title"}
    update_resp = helper.CLIENT.put('/project/update', data=update_data, headers=helper.token2headers(token))

    # Assert update response
    assert update_resp.status_code == 200
    assert update_resp.get_json()["message"] == "Project updated."

    # Check notifications for each student
    notifs = dbAcc.get_notifs(student_id1)
    assert len(notifs) == 3
    assert notifs[0].content == f"The project Updated Project Title has been updated."

    notifs = dbAcc.get_notifs(student_id2)
    assert notifs[0].content == f"The project Updated Project Title has been updated."

    notifs = dbAcc.get_notifs(student_id3)
    assert notifs[0].content == f"The project Updated Project Title has been updated."


def test_view_notifications():

    helper.truncate()
    user_id, token = helper.create_user(role=Role.STUDENT)
    dbAcc.create_notif(user_id, "Test notification 1")
    dbAcc.create_notif(user_id, "Test notification 2")

    # View notifications for the user
    response = helper.CLIENT.get('/notifications/view', data={"userid": user_id}, headers=helper.token2headers(token))
    assert response.status_code == 200


    data = response.get_json()
    assert len(data) == 2
    assert data[0]["content"] == "Test notification 2"
    assert data[1]["content"] == "Test notification 1"

def test_message_send_notification():

    helper.truncate()
    user_id, token = helper.create_user(role=Role.STUDENT)
    user_id2, token2 = helper.create_user(index=1, role=Role.STUDENT)
    group_id, channel_id = helper.create_group(user_id, token)

    helper.CLIENT.post('/group/join', data={"groupid": group_id, "userid": user_id2}, headers = helper.token2headers(token2))
    helper.CLIENT.post('/group/request/handle', data={"userid": user_id, "applicantid": user_id2, "groupid": group_id, "accept": True}, headers = helper.token2headers(token))

    response = helper.CLIENT.post('/message/send', data = {"userid":user_id, "content":"content_str", "senderid":user_id, "channelid": channel_id}, headers = helper.token2headers(token))
    assert response.status_code == 201

    # Check notifications for the receiver
    response = helper.CLIENT.get('/notifications/view', data={"userid": user_id2}, headers=helper.token2headers(token2))
    assert response.status_code == 200
    data = response.get_json()
    assert data[0]["content"] == f"New message in channel {channel_id}"

    # Check the sender is not receiving the notification
    response2 = helper.CLIENT.get('/notifications/view', data={"userid": user_id}, headers=helper.token2headers(token))
    assert response2.status_code == 200
    data2 = response2.get_json()
    assert len(data2) == 1

def test_view_individual_notification():
    helper.truncate()
    user_id, token = helper.create_user(role=Role.STUDENT)
    user_id2, token2 = helper.create_user(index=1, role=Role.STUDENT)
    group_id, channel_id = helper.create_group(user_id, token)

    helper.CLIENT.post('/group/join', data={"groupid": group_id, "userid": user_id2}, headers=helper.token2headers(token2))
    helper.CLIENT.post('/group/request/handle', data={"userid": user_id, "applicantid": user_id2, "groupid": group_id, "accept": True}, headers=helper.token2headers(token))

    response = helper.CLIENT.post('/message/send', data={"userid": user_id, "content": "Hello!", "senderid": user_id, "channelid": channel_id}, headers=helper.token2headers(token))
    assert response.status_code == 201

    notif_response = helper.CLIENT.get('/notifications/view', data={"userid": user_id2}, headers=helper.token2headers(token2))
    assert notif_response.status_code == 200
    notifications = notif_response.get_json()
    assert len(notifications) > 1
    notif_id = notifications[0]["notifid"]

    # User 2 views the specific notification
    individual_notif_response = helper.CLIENT.get('/notification/view', data={"userid": user_id2, "notifid": notif_id}, headers=helper.token2headers(token2))
    assert individual_notif_response.status_code == 200
    notification_data = individual_notif_response.get_json()
    assert notification_data["notifid"] == notif_id
    assert notification_data["content"] == f"New message in channel {channel_id}"


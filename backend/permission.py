"""
Assumed existence of objects in database.
Raise RoleError when user has bad role.
"""

from enum import IntEnum
import typing
#from authentication import return_user
from error import RoleError
import dbAcc
from typing import Union

class Role(IntEnum):
    STUDENT = 0
    TUTOR = 1
    COORDINATOR = 2
    ADMIN = 3
    CLIENT = 4




########################################################################
# About projects

def project_create(userid:int, ownerid:int):
    user = dbAcc.get_user_by_id(userid)
    owner = dbAcc.get_user_by_id(ownerid)

    if owner.role not in [Role.CLIENT, Role.ADMIN]:
        raise RoleError(description=f"Intended onwer {ownerid} is not a client/admin")
    if (userid != ownerid) and (user.role not in [Role.COORDINATOR, Role.ADMIN]):
        raise RoleError(description=f"User {userid} is not an coordinator/admin, can not create project for others")


def project_details(userid:int, projectid:int):
    user = dbAcc.get_user_by_id(userid)
    project = dbAcc.get_project_by_id(projectid)

    if user.role == Role.CLIENT and userid != project.owner_id:
        raise RoleError(description=f"Client {userid} can not view others project")


def projects_view_all(userid:int):
    pass


def project_edit(userid:int, projectid:int):
    user = dbAcc.get_user_by_id(userid)
    project = dbAcc.get_project_by_id(projectid)

    if user.role in [Role.STUDENT, Role.TUTOR]:
        raise RoleError(description=f"Student/tutor {userid} can not edit projects")
    if user.role == Role.CLIENT and userid != project.owner_id:
        raise RoleError(description=f"Client {userid} can not edit others projects")







########################################################################
# Skill

def skill_create(userid:int):
    user = dbAcc.get_user_by_id(userid)
    if user.role not in [Role.COORDINATOR, Role.ADMIN, Role.CLIENT]:
        raise RoleError(description=f"Only coordinator/admin can create skills")
    

def skill_view():
    pass


def skill_view_student(studentid:int):
    student = dbAcc.get_user_by_id(studentid)

    if student.role != Role.STUDENT:
        raise RoleError(description=f"Target {studentid} is not a student")


def skill_view_project():
    pass


def skill_set_student(userid:int, studentid:int):
    user = dbAcc.get_user_by_id(userid)
    student = dbAcc.get_user_by_id(studentid)

    if student.role != Role.STUDENT:
        raise RoleError(description=f"Intended onwer {studentid} is not a student")
    if (userid != studentid) and (user.role != Role.ADMIN):
        raise RoleError(description=f"User {userid} is not an admin, can not set skill for others")


def skill_set_project(userid:int, projectid:int):
    user = dbAcc.get_user_by_id(userid)
    ownerid = dbAcc.get_project_by_id(projectid).owner_id

    if (userid != ownerid) and (user.role not in [Role.COORDINATOR, Role.ADMIN]):
        raise RoleError(description=f"User {userid} is not an coordinator/admin, can not set skill for other projects")




################################################################
# Channel

def get_group_channel(userid:int, groupid:int):
    user = dbAcc.get_user_by_id(userid)
    if (user.groupid != groupid) and (user.role not in [Role.TUTOR, Role.COORDINATOR, Role.ADMIN]):
        raise RoleError(description=f"User {userid} is not in the group {groupid} nor an tutor/coordinator/admin, can not get the group channel")


def get_project_channel(userid:int, projectid:int):
    user = dbAcc.get_user_by_id(userid)
    group = dbAcc.get_group_by_id(user.groupid)
    project = dbAcc.get_project_by_id(projectid)
    if (project.owner_id != userid) and (group.project != projectid) and (user.role not in [Role.TUTOR, Role.COORDINATOR, Role.ADMIN]):
        raise RoleError(description=f"User {userid} is not in the project {projectid} nor an tutor/coordinator/admin, can not get the group channel")

def get_users_channel(userid:int, target_userid:int):
    user = dbAcc.get_user_by_id(userid)
    if (userid != target_userid) and (user.role not in [Role.COORDINATOR, Role.ADMIN]):
        raise RoleError(description=f"User {userid} is not an coordinator/admin, can not get others channels")


def manual_io_channel(adminid:int):
    admin = dbAcc.get_user_by_id(adminid)
    if admin.role != Role.ADMIN:
        raise RoleError(description=f"User {adminid} is not an admin, can not manually add/remove users in channels")


################################################################
# Message

def send_message(userid:int, channelid: int, senderid: int):
    user = dbAcc.get_user_by_id(userid)
    sender = dbAcc.get_user_by_id(senderid)
    sender_channels = dbAcc.get_users_channels(senderid)
    sender_channel_ids = [channel.channelid for channel in sender_channels]

    if (userid != senderid) and (user.role != Role.ADMIN):
        raise RoleError(description=f"User {userid} is not an admin, can not send message on the behalf of others {senderid}")
    if (channelid not in sender_channel_ids) and (sender.role != Role.ADMIN):
        raise RoleError(description=f"User {senderid} is not in the channel nor an admin, can not send message to channel {channelid}")
    

def set_message(userid:int, msgid:int):
    # TODO: allow owner of group/project to set message

    user = dbAcc.get_user_by_id(userid)
    msg = dbAcc.get_message_by_id(msgid)
    senderid = msg.ownerid

    if (userid != senderid) and (user.role not in [Role.COORDINATOR, Role.ADMIN]):
        raise RoleError(description=f"User {userid} is not an coordinator/admin, can not set message on the behalf of others {senderid}")
    

def view_channel_message(userid:int, channelid: int):
    user = dbAcc.get_user_by_id(userid)
    members = dbAcc.get_channel_members(channelid)
    member_ids = [member.userid for member in members]

    if (userid not in member_ids) and (user.role not in [Role.TUTOR, Role.COORDINATOR, Role.ADMIN]):
        raise RoleError(description=f"User {userid} is not in the channel nor an tutor/coordinator/admin, can not view message in channel {channelid}")


################################################################
# notifications

def create_notif(userid:int):
    user = dbAcc.get_user_by_id(userid)

    if (user.role != Role.ADMIN):
        raise RoleError(description=f"User {userid} is not an admin, can not manually create notification")
    

def get_notifs(userid:int, ownerid:int):
    user = dbAcc.get_user_by_id(userid)

    if (userid != ownerid) and (user.role != Role.ADMIN):
        raise RoleError(description=f"User {userid} is not an admin, can not view others notifications")
    

def delete_notif(userid:int, notifid:int):
    user = dbAcc.get_user_by_id(userid)
    ownerid = dbAcc.get_notif_by_id(notifid).userid

    if (userid != ownerid) and (user.role != Role.ADMIN):
        raise RoleError(description=f"User {userid} is not an admin, can not delete others notifications")
    


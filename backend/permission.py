"""
Assumed existence of objects in database.
Raise RoleError when user has bad role.
"""

from enum import IntEnum
import typing
from authentication import return_user
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
    user = return_user(userid)
    owner = return_user(ownerid)

    if owner["role"] != Role.CLIENT:
        raise RoleError(description=f"Intended onwer {ownerid} is not a client")
    if (userid != ownerid) and (user["role"] not in [Role.COORDINATOR, Role.ADMIN]):
        raise RoleError(description=f"User {userid} is not an coordinator/admin, can not create project for others")


def project_details(userid:int, projectid:int):
    user = return_user(userid)
    project = dbAcc.get_project_by_id(projectid)

    if user["role"] == Role.CLIENT and userid != project.owner_id:
        raise RoleError(description=f"Client {userid} can not view others project")


def projects_view_all(userid:int):
    pass


def project_edit(userid:int, projectid:int):
    user = return_user(userid)
    project = dbAcc.get_project_by_id(projectid)

    if user["role"] in [Role.STUDENT, Role.TUTOR]:
        raise RoleError(description=f"Student/tutor {userid} can not edit projects")
    if user["role"] == Role.CLIENT and userid != project.owner_id:
        raise RoleError(description=f"Client {userid} can not edit others projects")







########################################################################
# Skill

def skill_create(userid:int):
    user = return_user(userid)
    if user["role"] not in [Role.COORDINATOR, Role.ADMIN]:
        raise RoleError(description=f"Only coordinator/admin can create skills")
    

def skill_view():
    pass


def skill_view_student(studentid:int):
    student = return_user(studentid)

    if student["role"] != Role.STUDENT:
        raise RoleError(description=f"Target {studentid} is not a student")


def skill_view_project():
    pass


def skill_set_student(userid:int, studentid:int):
    user = return_user(userid)
    student = return_user(studentid)

    if student["role"] != Role.STUDENT:
        raise RoleError(description=f"Intended onwer {studentid} is not a student")
    if (userid != studentid) and (user["role"] != Role.ADMIN):
        raise RoleError(description=f"User {userid} is not an admin, can not set skill for others")


def skill_set_project(userid:int, projectid:int):
    user = return_user(userid)
    ownerid = dbAcc.get_project_by_id(projectid).owner_id

    if (userid != ownerid) and (user["role"] not in [Role.COORDINATOR, Role.ADMIN]):
        raise RoleError(description=f"User {userid} is not an coordinator/admin, can not set skill for other projects")




################################################################
# Message

# The following are done automatically, thus permission not applicable
#   Channels create/delete/assigne/remove 
#   Add/remove users in channels

def send_message(userid:int, channelid: int, senderid: int):
    user = return_user(userid)
    sender = return_user(senderid)
    sender_channels = dbAcc.get_users_channels(senderid)
    sender_channel_ids = [channel.channelid for channel in sender_channels]

    if (userid != senderid) and (user["role"] != Role.ADMIN):
        raise RoleError(description=f"User {userid} is not an admin, can not send message on the behalf of others {senderid}")
    if (channelid not in sender_channel_ids) and (sender["role"] != Role.ADMIN):
        raise RoleError(description=f"User {senderid} is not in the channel nor an admin, can not send message to channel {channelid}")
    

def set_message(userid:int, msgid:int):
    # TODO: allow owner of group/project to set message

    user = return_user(userid)
    msg = dbAcc.get_message_by_id(msgid)
    senderid = msg.ownerid

    if (userid != senderid) and (user["role"] != Role.ADMIN):
        raise RoleError(description=f"User {userid} is not an admin, can not set message on the behalf of others {senderid}")
    

def view_channel_message(userid:int, channelid: int):
    user = return_user(userid)
    members = dbAcc.get_channel_members(channelid)
    member_ids = [member.userid for member in members]

    if (userid not in member_ids) and (user["role"] not in [Role.TUTOR, Role.COORDINATOR, Role.ADMIN]):
        raise RoleError(description=f"User {userid} is not in the channel nor an tutor/coordinator/admin, can not view message in channel {channelid}")


def create_notif(userid:int):
    user = return_user(userid)

    if (user["role"] != Role.ADMIN):
        raise RoleError(description=f"User {userid} is not an admin, can not manually create notification")
    

def get_notif(userid:int, ownerid:int):
    user = return_user(userid)

    if (userid != ownerid) and (user["role"] != Role.ADMIN):
        raise RoleError(description=f"User {userid} is not an admin, can not view others notifications")
    

def delete_notif(userid:int, ownerid:int):
    user = return_user(userid)

    if (userid != ownerid) and (user["role"] != Role.ADMIN):
        raise RoleError(description=f"User {userid} is not an admin, can not delete others notifications")
    


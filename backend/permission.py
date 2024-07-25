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

    if owner["role"] not in [Role.CLIENT, Role.ADMIN]:
        raise RoleError(description=f"Intended onwer {ownerid} is not a client/admin")
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






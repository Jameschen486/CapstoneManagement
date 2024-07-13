from enum import IntEnum
from authentication import return_user
from error import RoleError
import dbAcc


class Role(IntEnum):
    STUDENT = 0
    TUTOR = 1
    COORDINATOR = 2
    ADMIN = 3
    CLIENT = 4



########################################################################
# About projects

def project_create(userid, ownerid) -> bool:
    user = return_user(userid)
    owner = return_user(ownerid)

    if owner["role"] != Role.CLIENT:
        raise RoleError(description=f"Intended onwer {ownerid} is not a client")
    if (userid != ownerid) and (user["role"] not in [Role.COORDINATOR, Role.ADMIN]):
        raise RoleError(description=f"User {userid} is not an coordinator nor admin, can not create project for others")

    return True


def project_details(userid, projectid) -> bool:
    user = return_user(userid)
    project = dbAcc.get_project_by_id(projectid)

    if user["role"] == Role.CLIENT and userid != project.owner_id:
        raise RoleError(description=f"Client {userid} can not view others project")

    return True


def project_update(userid, projectid) -> bool:
    user = return_user(userid)
    project = dbAcc.get_project_by_id(projectid)

    if user["role"] in [Role.STUDENT, Role.TUTOR]:
        raise RoleError(description=f"Student/tutor {userid} can not update projects")
    if user["role"] == Role.CLIENT and userid != project.owner_id:
        raise RoleError(description=f"Client {userid} can not update others projects")

    return True


def project_delete(userid, projectid) -> bool:
    user = return_user(userid)
    project = dbAcc.get_project_by_id(projectid)

    if user["role"] in [Role.STUDENT, Role.TUTOR]:
        raise RoleError(description=f"Student/tutor {userid} can not delete projects")
    if user["role"] == Role.CLIENT and userid != project.owner_id:
        raise RoleError(description=f"Client {userid} can not delete others projects")

    return True


########################################################################
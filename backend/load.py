"""
Load from database, raise exception if not exists.
"""

import dbAcc
from error import InputError


def user(userid:int) -> dbAcc.User_d_full:
    user = dbAcc.get_user_by_id(userid)
    if user is None:
        raise InputError(description=f"User {userid} does not exist")
    return user

def project(projectid:int) -> dbAcc.Proj_d_full:
    project = dbAcc.get_project_by_id(projectid)
    if project is None:
        raise InputError(description=f"Project {projectid} does not exist")
    return project

def skill(skillid:int) -> dbAcc.Skill_d:
    skill = dbAcc.get_skill_by_id(skillid)
    if skill is None:
        raise InputError(description=f"Skill {skillid} does not exist")
    return skill
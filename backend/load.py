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

def group(groupid:int) -> dbAcc.Group_d_full:
    group = dbAcc.get_group_by_id(groupid)
    if group is None:
        raise InputError(description=f"Group {group} does not exist")
    return group

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

def channel(channelid:int) -> dbAcc.Channel_d_base:
    channels = dbAcc.get_all_channels()
    channel_dict = {channel.channelid: channel for channel in channels}
    channel = channel_dict.get(channelid)
    if channel is None:
        raise InputError(description=f"Channel {channelid} does not exist")
    return channel

def message(messageid:int) -> dbAcc.Message_d_base:
    message = dbAcc.get_message_by_id(messageid)
    if message is None:
        raise InputError(description=f"Message {messageid} does not exist")
    return message
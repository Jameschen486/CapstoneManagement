import dbAcc

def join(userid:int, channelid:int) -> bool:
    members = dbAcc.get_channel_members(channelid)
    member_ids = [member.userid for member in members]

    if userid not in member_ids:
        dbAcc.add_user_to_channel(userid, channelid)
        return True
    else:
        return False

def leave(userid:int, channelid:int):
    members = dbAcc.get_channel_members(channelid)
    member_ids = [member.userid for member in members]

    if userid in member_ids:
        dbAcc.remove_user_from_channel(userid, channelid)
        return True
    else:
        return False

def join_group(groupid:int, userid:int):
    group = dbAcc.get_group_by_id(groupid)
    group_channelid = group.channel
    join(userid, group_channelid)

    project = dbAcc.get_project_by_id(group.project)
    if project is not None:
        project_channelid = project.channel
        join(userid, project_channelid)


def leave_group(groupid:int, userid:int):
    group = dbAcc.get_group_by_id(groupid)
    group_channelid = group.channel
    leave(userid, group_channelid)

    project = dbAcc.get_project_by_id(group.project)
    if project is not None:
        project_channelid = project.channel
        leave(userid, project_channelid)


def assign_project(projectid:int, groupid:int):
    # assumed groups have no duplicate members

    project_channelid = dbAcc.get_project_by_id(projectid).channel
    group_members = dbAcc.get_group_members(groupid)
    
    for member in group_members:
        join(member.userid, project_channelid)


def unassign_project(projectid:int, groupid:int):
    # assumed groups have no duplicate members

    project_channelid = dbAcc.get_project_by_id(projectid).channel
    group_members = dbAcc.get_group_members(groupid)

    for member in group_members:
        leave(member.userid, project_channelid)
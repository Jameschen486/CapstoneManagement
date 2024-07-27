import dbAcc, load, permission, message

def get_group_channelid(userid:int, groupid:int):
    load.user(userid)
    group = load.group(groupid)
    permission.get_group_channel(userid, groupid)

    return {"channelid": group.channel}, 200

def get_project_channelid(userid:int, projectid:int):
    load.user(userid)
    project = load.project(projectid)
    permission.get_project_channel(userid, projectid)

    return {"channelid": project.channel}, 200

def manual_join(userid:int, targetid:int, channelid:int):
    load.user(userid)
    load.user(targetid)
    load.channel(channelid)
    permission.manual_io_channel(userid)

    join(targetid, channelid)


def manual_leave(userid:int, targetid:int, channelid:int):
    load.user(userid)
    load.user(targetid)
    load.channel(channelid)
    permission.manual_io_channel(userid)

    leave(targetid, channelid)


def view_message(userid:int, channelid:int, last_message:int = None):
    load.user(userid)
    load.channel(channelid)
    permission.view_channel_message(userid, channelid)

    msgs = dbAcc.get_channel_messages(channelid, last_message)
    
    return {"messages": message.format(msgs)}, 200


################################################################
# Functions below do not check for InputError nor AccessError

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




#def create_group(groupid):
#    pass

#def create_project(projectid):
#    pass

def join_group(groupid:int, userid:int):
    group = dbAcc.get_group_by_id(groupid)
    group_channelid = group.channel
    join(userid, group_channelid)

    project = dbAcc.get_project_by_id(group.project)
    project_channelid = project.channel
    join(userid, project_channelid)


def leave_group(groupid:int, userid:int):
    group = dbAcc.get_group_by_id(groupid)
    group_channelid = group.channel
    leave(userid, group_channelid)

    project = dbAcc.get_project_by_id(group.project)
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




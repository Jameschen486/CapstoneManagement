import dbAcc, load, permission, message
from error import InputError
import sys

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

def get_users_channels(userid:int, target_userid:int):
    load.user(userid)
    load.user(target_userid)
    permission.get_users_channel(userid, target_userid)

    channels = dbAcc.get_users_channels(target_userid)
    channels = [channel._asdict() for channel in channels]
    return {"channels": channels}, 200

def manual_io(userid:int, target_userid:int, channelid:int, io:str = None):
    load.user(userid)
    load.user(target_userid)
    load.channel(channelid)
    permission.manual_io_channel(userid)

    if io == "join":
        succeed = join(target_userid, channelid)
    elif io == "leave":
        succeed = leave(target_userid, channelid)
    else:
        raise InputError(description=r"please specify field {io} as join or leave")

    return {"succeed": succeed}, 200


def view_message(userid:int, channelid:int, last_message:int = None, latest_message:str = 'false'):
    load.user(userid)
    load.channel(channelid)
    permission.view_channel_message(userid, channelid)

    if latest_message == 'true':
        msg = dbAcc.get_latest_message(channelid)
        if msg is None:
            msgs = []
        else:
            msgs = [msg]
            
    else:
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






import dbAcc
import load
from error import InputError, AccessError, RoleError
import permission


def content_is_valid(msg_str:str):
    return msg_str is not None


def send(userid:int, content:str, senderid:int, channelid:int):
    load.user(userid)
    load.channel(channelid)
    load.user(senderid)
    if not content_is_valid(content):
        InputError(description=f"Invalid message: {content}")

    permission.send_message(userid, channelid, senderid)
    dbAcc.create_message(channelid, senderid, content)
    

def edit(userid:int, msgid:int, content:str):
    load.user(userid)
    load.message(msgid)
    if not content_is_valid(content):
        InputError(description=f"Invalid new message: {content}")

    permission.set_message(userid, msgid)
    dbAcc.edit_message(msgid, content)


def delete(userid:int, msgid:int):
    load.user(userid)
    load.message(msgid)

    permission.set_message(userid, msgid)
    dbAcc.delete_message(msgid)
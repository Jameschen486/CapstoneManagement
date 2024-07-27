import dbAcc
import load
from error import InputError, AccessError, RoleError
import permission
import typing

def content_is_valid(msg_str:str) -> bool:
    return msg_str is not None


def send(userid:int, content:str, senderid:int, channelid:int):
    load.user(userid)
    load.channel(channelid)
    load.user(senderid)
    if not content_is_valid(content):
        InputError(description=f"Invalid message: {content}")

    permission.send_message(userid, channelid, senderid)
    msgid = dbAcc.create_message(channelid, senderid, content)

    return {"message": "Message sent.", "messageid": msgid}, 201
    

def edit(userid:int, msgid:int, content:str):
    load.user(userid)
    load.message(msgid)
    if not content_is_valid(content):
        InputError(description=f"Invalid new message: {content}")

    permission.set_message(userid, msgid)
    dbAcc.edit_message(msgid, content)

    return {"message": "Message updated.", "messageid": msgid}, 200


def delete(userid:int, msgid:int):
    load.user(userid)
    load.message(msgid)

    permission.set_message(userid, msgid)
    dbAcc.delete_message(msgid)

    return {"message": "Message deleted.", "messageid": msgid}, 200


def format(msg:typing.Union[dbAcc.Message_d_base, list]) -> typing.Union[dict, list]:
    if type(msg) is list:
        formatted_msgs = []
        for m in msg:
            formatted_msgs.append(format(m))
        return formatted_msgs

    return msg._asdict()
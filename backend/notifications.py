import dbAcc

def view_notifications(user_id: int):
    """
    Retrieves all notifications for a given user.

    Parameters:
        user_id (int): The ID of the user whose notifications are to be retrieved.

    Returns:
        A list of notifications or an empty list if no notifications are found.
    """
    notifications = dbAcc.get_notifs(user_id)
    ret = []
    for n in notifications:
        ret.append({"notifid": n[0], "timestamp": n[1], "content": n[2]})
    return ret, 200

def view_notification(user_id: int, notif_id: int): 
    """
    Retrieves details of a specific notification for a user.

    Parameters:
        user_id (int): The ID of the user requesting the notification.
        notif_id (int): The ID of the notification to view.

    Returns:
        dict: A dictionary with notification details.
    """
    notifications = dbAcc.get_notifs(user_id)
    exist = False
    for n in notifications:
        if notif_id == n[0]:
            exist = True
            break

    if not exist:
        return {"message": "Notification not found"}, 400

    notification = dbAcc.get_notif_by_id(notif_id)

    response = {
        "notifid": notification[0],
        "userid": notification[1],
        "created": notification[2],
        "isnew": notification[3],
        "content": notification[4]
    }
    return response, 200


def delete_notification(user_id: int, notif_id: int):
    """
    Deletes a notification given a user_id and notif_id

    Parameters:
        user_id (int): The ID of the user requesting the notification.
        message_id (int): The ID of the notification to view.

    Returns:
        dict: message saying whether the deletion is successful or not
    """
    notifications = dbAcc.get_notifs(user_id)
    exist = False
    for n in notifications:
        if notif_id == n[0]:
            exist = True
            break

    if not exist:
        return {"message": "Notification not found"}, 400

    dbAcc.delete_notif(notif_id)
    return {"message": f"Successfully deleted notification {notif_id}"}, 200


def delete_all_notifications(user_id: int):
    """
    Deletes all notifications for a specific user.

    Parameters:
        user_id (int): The ID of the user requesting the deletion.

    Returns:
        dict: A dictionary with a message indicating the result of the deletion.
    """
    notifications = dbAcc.get_notifs(user_id)
    if not notifications:
        return {"message": "No notifications found"}, 200

    dbAcc.delete_all_notifs(user_id)
    return {"message": "All notifications deleted successfully"}, 200
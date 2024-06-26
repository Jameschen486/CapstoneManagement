import psycopg2
from error import InputError, AccessError
import dbAcc
from dbAcc import get_all_groups, get_groupcount_by_name, get_user_by_id, get_group_members, create_join_request, add_user_to_group, remove_all_join_requests, remove_join_request, get_group_by_id, get_join_requests, remove_user_from_group

def create_group(group_name, creator_id):

    # Error case 1: No group name is provided
    if group_name == None:
        raise InputError(description="Group name is required")
    
    no_groups = get_groupcount_by_name(group_name)
    
    # Error Case 2: A group with same name already registered.
    if no_groups > 0:
        raise InputError(description="Group with the same name already exists")
    
    # Error Case 3: If the user is already in a group, return error message
    if get_user_by_id(creator_id).groupid != None:
        raise AccessError(description="User is already in a group")
    
    group_id = dbAcc.create_group(creator_id, group_name)
    return {"message": "Group created successfully!", "group_id": group_id}, 201

def view_groups():
    return get_all_groups()


def join_group(group_id, student_id, group_capacity):

    # Check 1: The user is not already in a group
    if get_user_by_id(student_id).groupid != None:
        raise AccessError(description="User is already in a group")
    
    # Check 2: The group is full or not
    if len(get_group_members(group_id)) >= group_capacity:
        raise AccessError(description="Group is full")
    
    # Send a join request
    create_join_request(student_id, group_id)
    return {"message": "Join request sent successfully!"}, 201

def handle_join_request(user_id, applicant_id, group_id, accept, group_capacity):
    c_id = get_group_by_id(group_id)[1]
    if not user_id != c_id:
        raise AccessError(description="You do not have access to accept/reject join requests")
    
    if accept == 1:
        if len(get_group_members(group_id)) >= group_capacity:
            raise AccessError(description="Group is full")
        
        add_user_to_group(applicant_id, group_id)
        remove_all_join_requests(applicant_id)
        return  {"message": f"User {applicant_id} added to your group."}, 201
        # TODO In next sprint send notification to applicant.
    else:
        remove_join_request(applicant_id, group_id)
        return {"message": f"User {applicant_id} rejected."}, 201
        # TODO In next sprint send notification to applicant.

def view_group_details(group_id):
    group_details = get_group_by_id(group_id)
    group_members = get_group_members(group_id)
    
    if not group_details:
        raise InputError(description="Group not found")

    return {
        "group_details": group_details,
        "group_members": group_members
    }, 200

def view_join_requests(user_id):
    join_requests = get_join_requests(user_id)

    if join_requests == []:
        return {"message": "No join requests"}, 200
    
    return {"join_requests": join_requests}, 200

def leave_group(user_id):
    if get_user_by_id(user_id)[6] == None:
        raise AccessError(description="User is not a member of any group")
    
    remove_user_from_group(user_id)
    return {"message": "User has left the group"}, 200
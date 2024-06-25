import psycopg2
from backend.error import InputError, AccessError
from backend.dbAcc import create_group, get_all_groups, get_groupcount_by_name, get_user_by_id, get_group_members, create_join_request, add_user_to_group, remove_all_join_requests, remove_join_request, get_group_by_id, get_join_requests

def create_group(group_name, creator_id):

    # Error case 1: No group name is provided
    if group_name == None:
        raise InputError(description="Group name is required")
    
    no_groups = get_groupcount_by_name(group_name)
    
    # Error Case 2: A group with same name already registered.
    if get_groupcount_by_name(group_name) > 0:
        raise InputError(description="Group with the same name already exists")
    
    group_id = create_group(group_name, creator_id)
    return {"message": "Group created successfully!", "group_id": group_id}, 201

def view_groups():
    return get_all_groups()


def join_group(group_id, student_id, group_capacity):

    # Check 1: The user is not already in a group
    if get_user_by_id(student_id)[5] != None:
        raise AccessError(description="User is already in a group")
    
    # Check 2: The group is full or not
    if len(get_group_members(group_id)) >= group_capacity:
        raise AccessError(description="Group is full")
    
    # Send a join request
    create_join_request(student_id, group_id)
    return {"message": "Join request sent successfully!"}, 201

def handle_join_request(creator_id, applicant_id, group_id, accept, group_capacity):
    if not is_user_creator(creator_id, group_id):
        raise AccessError(description="You do not have access to accept/reject join requests")
    
    if accept:
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
    
    if not group_details:
        raise InputError(description="Group not found")

    return group_details, 200

def view_join_requests(user_id):
    join_requests = get_join_requests(user_id)

    if join_requests == []:
        return {"message": "No join requests"}, 200
    
    return {"join_requests": join_requests}, 200

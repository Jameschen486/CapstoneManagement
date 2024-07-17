import dbAcc
from error import InputError, AccessError
from permission import Role

def add_preference(student_id, project_ids, ranks):

    existing_preferences = dbAcc.get_user_preferences(student_id)
    existing_project_ids = [pref.projectid for pref in existing_preferences]
    existing_ranks = [pref.rank for pref in existing_preferences]

    # Check if the projects are already in the preference list and if the ranks are taken
    for project_id, rank in zip(project_ids, ranks):
        if project_id in existing_project_ids:
            raise InputError(description=f"Project ID {project_id} is already in the preference list")
        if rank in existing_ranks:
            raise InputError(description=f"Rank {rank} is already taken")
        
    dbAcc.create_preferences(student_id, project_ids, ranks)
    return {"message": "Preferences added successfully!"}, 201

# Not too sure about our design rn, this function currently replaces ALL the preference list with the new passed in preferences
def edit_preference(student_id, project_ids, ranks):

    dbAcc.delete_preferences(student_id)
    dbAcc.create_preferences(student_id, project_ids, ranks)
    return {"message": "Preferences updated successfully!"}, 200

def view_preference(user_id, student_id, role):
    # Allow the student to view their own preferences or roles with higher access right now clients, coordinator and admin
    if user_id == student_id or role in [Role.CLIENT, Role.COORDINATOR, Role.ADMIN]:
        preferences = dbAcc.get_user_preferences(student_id)
        return [{"project_id": pref.projectid, "rank": pref.rank} for pref in preferences], 200
    else:
        raise AccessError(description="You do not have permission to view this student's preferences")
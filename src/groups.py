import psycopg2
from src.error import InputError, AccessError

def get_db_connection():
    return True

def create_group(group_name, group_description, creator_id):
    
    # Error case 1: No group name is provided
    if not group_name:
        raise InputError(description="Group name is required")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id FROM groups WHERE name = %s', (group_name,))
    existing_group = cur.fetchone()
    
    # Error Case 2: A group with same name already registered.
    if existing_group:
        cur.close()
        conn.close()
        raise InputError(description="Group with the same name already exists")

    cur.execute('INSERT INTO groups (name, description, creator_id) VALUES (%s, %s, %s) RETURNING id',
                (group_name, group_description, creator_id))
    group_id = cur.fetchone()[0]

    cur.execute('INSERT INTO group_members (group_id, student_id) VALUES (%s, %s)', (group_id, creator_id))
    conn.commit()
    cur.close()
    conn.close()

    # Successful creation
    return {"message": "Group created successfully!", "group_id": group_id}, 201

def view_groups():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM groups')
    groups = cur.fetchall()
    cur.close()
    conn.close()

    groups_list = []
    for group in groups:
        group_data = {
            'id': group[0],
            'name': group[1],
            'description': group[2],
            'creator_id': group[3]
        }
        groups_list.append(group_data)

    return groups_list

def join_group(group_id, student_id, group_capacity):
    conn = get_db_connection()
    cur = conn.cursor()

    # Check 1: The user is not already in a group
    cur.execute('SELECT group_id FROM group_members WHERE student_id = %s', (student_id,))
    user_group = cur.fetchone()
    if user_group:
        cur.close()
        conn.close()
        raise AccessError(description="User is already in a group")
    
    # Check 2: The group is full or not
    cur.execute('SELECT COUNT(*) FROM group_members WHERE group_id = %s', (group_id,))
    group_member_count = cur.fetchone()[0]
    if group_member_count >= group_capacity:
        cur.close()
        conn.close()
        raise AccessError(description="Group is full")

    cur.execute('INSERT INTO join_requests (group_id, student_id) VALUES (%s, %s)', (group_id, student_id))
    conn.commit()
    cur.close()
    conn.close()

    return {"message": "Join request sent successfully!"}, 201
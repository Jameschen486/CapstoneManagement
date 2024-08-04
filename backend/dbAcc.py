import psycopg2
import typing
from collections import namedtuple
from datetime import datetime

import psycopg2.extras
import psycopg2.pool
import dbChannel
import sys

try:
  #everything working with a single connection in non threaded workloads
  connpool = psycopg2.pool.SimpleConnectionPool(1, 10, dbname='projdb', user='postgres', password='postgres', host="postgres")
except:
  print("Unable to connect to database.")
  exit()

#setup namedtuples
User_d_full = namedtuple("User_d_full", ["userid", "email", "first_name", "last_name", "password", "role", "groupid"])
User_d_base = namedtuple("User_d_base", ["userid", "first_name", "last_name"])
Group_d_full = namedtuple("Group_d_full", ["groupid", "ownerid", "group_name", "project", "channel"])
Group_d_base = namedtuple("Group_d_base", ["groupid", "group_name", "member_count"])
Proj_d_full = namedtuple("Proj_d_full", ["project_id", "owner_id", "title", "clients", "specializations", 
                                         "groupcount", "background", "requirements", "req_knowledge", 
                                         "outcomes", "supervision", "additional", "channel"])
Skill_d = namedtuple("Skill_d", ["skill_id", "skill_name"])
Group_skill_d = namedtuple("Group_skill_d", ["skill_id", "skill_count"])
Groups_skill_d = namedtuple("Groups_skill_d", ["groupid", "skillid", "skillcount"])
Projects_skill_d = namedtuple("Projects_skills_d", ["projectid", "groupcount", "skillid"])
Reset_code_d = namedtuple("Reset_code_d", ["userid", "code", "timestamp"])
User_pref_d = namedtuple("User_pref_d", ["projectid", "rank"])
Group_pref_d = namedtuple("Group_pref_d", ["groupid", "projectid", "rank"])
Notif_d_full = namedtuple("Notif_d_base", ["notifid", "userid", "created", "isnew", "content"])
Notif_d_base = namedtuple("Notif_d_base", ["notifid", "timestamp", "content"])
Channel_d_base = namedtuple("Channel_d_base", ["channelid", "channel_name"])
Message_d_base = namedtuple("Message_d_base", ["messageid", "ownerid", "timestamp", "content"])

def run_psql_stmt(stmt: str, vals: tuple, commit: bool = False):
  ''' Genericly runs sql and returns the cursor for fetching
      exists so that there isnt so much boilerplate in the rest of the funcs
  
  Paramters:
    stmt (string), psql statement
    vals (tuple), vals to pass to statement
    commit (boolean), whether we should commit the connection
    
  Returns
    psycopg2.cursor, to run fetch on
  '''
  conn = connpool.getconn()
  curs = conn.cursor()
  curs.execute(stmt, vals)
  if commit:
    conn.commit()
  connpool.putconn(conn)
  return curs

#--------------------------------
#   Users
# Manipulation
def create_user(email: str, password: str, first_name:str , last_name: str, role: int) -> int:
  ''' Creates a user in the databse

  Parameters:
    - email (string)
    - password (string), hashed password
    - first_name
    - last_name
    - role (integer), user's intended role

  Returns:
    - integer, the users id
  '''
  stmt = "INSERT INTO users (email, password, firstname, lastname, role) VALUES (%s, %s, %s, %s, %s) RETURNING userid"
  vals = (email, password, first_name, last_name, role)
  curs = run_psql_stmt(stmt, vals, commit=True)
  ret = curs.fetchone()[0]
  return ret

def update_password(userid: int, password: str):
  ''' Updates a users password with given value

  Parameters:
    - userid (integer), id of user to change
    - password (string), new password
  '''
  stmt = "UPDATE users SET password = %s WHERE userid = %s"
  vals =  (password, userid)
  run_psql_stmt(stmt, vals, commit=True)


def update_role(userid: int, role: int):
  ''' Modifies the role of a user

  Parameters:
    - userid, id of user to issue change
    - role (integer), new role
  '''
  stmt = "UPDATE users SET role = %s WHERE userid = %s"
  vals =  (role, userid)
  run_psql_stmt(stmt, vals, commit=True)

def update_user_name(userid: int, firstName: str, lastName: str):
  ''' Modifies the name of a user

  Parameters:
    - userid, id of user to issue change
    - firstName (String)
    - lastName (String)
  '''
  stmt = "UPDATE users SET firstName = %s, lastName = %s WHERE userid = %s"
  vals =  (firstName, lastName, userid)
  run_psql_stmt(stmt, vals, commit=True)

def update_email(userid: int, email: str):
  ''' Modifies the email of a user

  Parameters:
    - userid, id of user to issue change
    - email (string), new email
  '''
  stmt = "UPDATE users SET email = %s WHERE userid = %s"
  vals =  (email, userid)
  run_psql_stmt(stmt, vals, commit=True)

# Retrieval
def get_user_by_id(userid: int) -> User_d_full:
  ''' Queries the database for user information
  
  Parameters:
    - userid (integer)
    
  Returns:
    - tuple (userid, email, first_name, last_name, password, role, groupid)
    - None, if user does not exist
    
  Notes:
    Does no checking, ensure you do not create two users with the same email address
  '''
  stmt = "SELECT * FROM users WHERE userid = %s"
  vals =  (userid,)
  curs = run_psql_stmt(stmt, vals)
  deets = curs.fetchone()
  if deets == None:
    return None
  return User_d_full(deets[0], deets[1], deets[2], deets[3], deets[4], deets[5], deets[6])
  
def get_user_by_email(email: str) -> User_d_full:
  ''' Queries the database for user information
  
  Parameters:
    - email (string)
    
  Returns:
    - tuple (userid, email, first_name, last_name, password, role, groupid)
    - None, if user does not exist
  '''
  stmt = "SELECT * FROM users WHERE email = %s"
  vals =  (email,)
  curs = run_psql_stmt(stmt, vals)
  deets = curs.fetchone()
  if deets == None:
    return None
  return User_d_full(deets[0], deets[1], deets[2], deets[3], deets[4], deets[5], deets[6])

#--------------------------------
#   Groups
# Manipulation
def create_group(ownerid: int, group_name: str) -> int:
  ''' Creates a new group, sets its owner, adds its owner to the group
      creates a channel for the group and adds its owner to the channel
  
  Parameters:
    - ownerid (integer), user id of owner/creator
    - group_name (string)
    
  Returns:
    - groupid (integer)
  '''
  stmt = "INSERT INTO groups (ownerid, groupname) VALUES (%s, %s) RETURNING groupid"
  vals =  (ownerid, group_name)
  curs = run_psql_stmt(stmt, vals, commit=True)
  new_grp_id = curs.fetchone()[0]
  new_ch_id = create_channel(group_name)
  assign_channel_to_group(new_ch_id, new_grp_id)  
  add_user_to_group(ownerid, new_grp_id) #will also add user to channel
  return new_grp_id
  
def add_user_to_group(userid: int, groupid: int):
  ''' Adds user to specified group, as well as the group's channel
  
  Parameters
    - userid (integer), user id of person to add
    - group_id (integer)
  '''
  stmt = "UPDATE users SET groupid = %s WHERE userid = %s"
  vals =  (groupid, userid)
  run_psql_stmt(stmt, vals, commit=True)
  dbChannel.join_group(groupid, userid)

  
def update_group_owner(userid: int, groupid: int):
  ''' Updates the owner of  a given group
  
  Parameters:
    userid (int), new owner of group
    groupid (int)
  '''
  stmt = "UPDATE groups SET ownerid = %s WHERE groupid = %s"
  vals =  (userid, groupid)
  run_psql_stmt(stmt, vals, commit=True)
  
def remove_user_from_group(userid: int):
  ''' Removes a user from the group they are in, 
      also removes them from the group's channel 
  
  Parameters:
    - userid (integer) 
  '''
  groupid = get_user_by_id(userid).groupid
  stmt = "UPDATE users SET groupid = NULL WHERE userid = %s"
  vals =  (userid,)
  run_psql_stmt(stmt, vals, commit=True)
  if groupid is not None:
    dbChannel.leave_group(groupid, userid)

def delete_group(groupid : int):
  ''' Deletes a group from the system, also deletes group's channel
  
  Parameters:
    groupid (int)
    
  Notes:
    all users access to the group's channel should also be deleted, 
    but delete group only gets called when everyone leaves, 
    and leaving groups also removes access 
  '''
  stmt = """DELETE FROM channels USING groups 
               WHERE groups.groupid = %s 
               AND channels.channelid = groups.channel;
               DELETE FROM groups WHERE groupid = %s"""
  vals =  (groupid, groupid)
  run_psql_stmt(stmt, vals, commit=True)

# Retrieval
def get_all_groups() -> typing.List[Group_d_base]:
  ''' Queries databse for details on every group
  
  Returns:
    - [tuple] (groupid, groupname, member_count) 
  '''
  stmt = """SELECT groups.groupid, groups.groupname, COUNT(users.userid) 
               FROM groups 
               JOIN users 
               ON users.groupid = groups.groupid
               GROUP BY groups.groupid"""
  vals = ()
  curs = run_psql_stmt(stmt, vals)
  ret_list = []
  for rec in curs:
    ret_list.append(rec)
  return ret_list

def get_group_by_id(groupid: int) -> Group_d_full:
  ''' Queries the database for information on a particular group
  
  Parameters:
    - groupid (integer)
    
  Returns:
    - tuple (groupid, ownerid, group_name, project, channel)
    - None, if groupid is invalid
    
  Notes:
    Project and channel in the return tuple may be None if no group or channel is assigned
  '''
  stmt = "SELECT * FROM groups WHERE groupid=%s"
  vals =  (groupid,)
  curs = run_psql_stmt(stmt, vals)
  deets = curs.fetchone()
  if deets == None:
      return None
  return Group_d_full(deets[0], deets[1], deets[2], deets[3], deets[4])

def get_groupcount_by_name(groupname: str) -> int:
  ''' Queries the databse for the number of groups with a given name
  
  Parameters:
   - groupname (string)
   
  Returns:
    - int, number of groups sharing the given name
  '''
  stmt = "SELECT count(*) FROM groups WHERE groupname = %s"
  vals =  (groupname,)
  curs = run_psql_stmt(stmt, vals)
  return curs.fetchone()[0]
  
def get_group_members(groupid: int) -> typing.List[User_d_base]:
  ''' Get details for all members of a given group
  
  Parameters:
    - groupid (integer)
    
  returns:
    - [tuple] (userid, first_name, last_name) 
    - [] if group does not exist
  '''
  stmt = "SELECT userid, firstname, lastname FROM users WHERE groupid = %s"
  vals =  (groupid,)
  curs = run_psql_stmt(stmt, vals)
  ret_list = []
  for rec in curs:
    ret_list.append(User_d_base(rec[0], rec[1], rec[2]))
  return ret_list

#----------------------------------
# Join requests
# Manipulation
def create_join_request(userid: int, groupid: int):
  ''' Creates a requests for userid to join groupid
  
  Parameters:
    - userid (integer), user making the request
    - groupid (integer), group being requested to join
  '''
  stmt = "INSERT INTO grouprequests (userid, groupid) VALUES (%s, %s)"
  vals =  (userid, groupid)
  run_psql_stmt(stmt, vals, commit=True)
  
def remove_all_join_requests(userid: int):
  ''' Removes all group join requests that a user has made
  
  Parameters:
    - userid (integer), user whose requests should be removed
    
  Notes:
    For use when a users request is approved, we should delete all others
  '''
  stmt = "DELETE FROM grouprequests WHERE userid = %s"
  vals =  (userid,)
  run_psql_stmt(stmt, vals, commit=True)
  
def remove_join_request(userid: int, groupid: int):
  ''' Removes a single join request for a group from a user
  
  Parameters:
    - userid (integer), userid of who made the request
    - groupid (integer), groupid of specific request
  '''
  stmt = "DELETE FROM grouprequests WHERE userid = %s AND groupid = %s"
  vals =  (userid, groupid)
  run_psql_stmt(stmt, vals, commit=True)
  
# Retrieval
def get_join_requests(userid: int) -> typing.List[User_d_base]:
  ''' Gets all join requests for group that the user is an owner of
  
  Parameters:
    - userid (integer)
    
  Returns:
    - [tuples(userid, first_name, last_name)], details of user attempting to join
    - [], if there are no requests
  '''
  stmt = """SELECT grouprequests.userid, users.firstName, users.lastName
               FROM groups
               JOIN grouprequests
               ON groups.groupid = grouprequests.groupid
               JOIN users
               ON users.userid = grouprequests.userid
               WHERE groups.ownerid = %s
               """
  vals =  (userid,)
  curs = run_psql_stmt(stmt, vals)
  ret_list = []
  for rec in curs:
    ret_list.append(User_d_base(rec[0], rec[1], rec[2]))
  return ret_list

#--------------------------------
#   Project
# Manipulation
def create_project(ownerid: int, title: str, clients: str, specializations: str, 
                   groupcount: str, background: str, requirements: str, 
                   req_knowledge :str, outcomes: str, supervision: str, additional:str) -> int:
  ''' Creates a project in the database, as well a channel for the project
      and adds projects owner to the channel
  
  Parameters:
    - ownerid (integer), id of user creating the project
    - title (string), title of project
    - clients (string), clients of project
    - specializations (string)
    - groupcount (string), number of groups that can be assigned to project 
    - background (string)
    - requirements (string)
    - req_knowledge (string)
    - outcomes (string)
    - supervision (string)
    - additional (string)
    
  Returns:
    - integer, the project id
  '''
  stmt = """INSERT INTO projects 
               (ownerid, title, clients, specials, groupcount, background, reqs, reqKnowledge, outcomes, supervision, additional)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
               RETURNING projectid"""
  
  vals = (ownerid, title, clients, specializations, 
                groupcount, background, requirements, 
                req_knowledge, outcomes, supervision, additional)
  curs = run_psql_stmt(stmt, vals, commit=True)
  new_prj_id = curs.fetchone()[0]
  new_ch_id = create_channel(title)
  assign_channel_to_project(new_ch_id, new_prj_id)
  add_user_to_channel(ownerid, new_ch_id)
  return new_prj_id

def get_project_by_id(projectid: int) -> Proj_d_full:
  ''' Queries the database for project information
  
  Parameters:
    - projectid (integer)
    
  Returns:
    - tuple (project_id, owner_id, title, clients, specializations, 
             groupcount, background, requirements, req_knowledge, 
             outcomes, supervision, additional, channel)
    - None, if project does not exist
    
  Notes:
    channel int the return tuple may be None if no channel is assigned
  '''
  stmt = "SELECT * FROM projects WHERE projectid = %s"
  vals =  (projectid,)
  curs = run_psql_stmt(stmt, vals)
  ret = curs.fetchone()
  if ret == None:
    return None
  
  return Proj_d_full(ret[0], ret[1], ret[2], ret[3], ret[4], ret[5], ret[6], ret[7], ret[8], ret[9], ret[10], ret[11], ret[12])

def get_all_projects() -> typing.List[Proj_d_full]:
  ''' Queries the database for all existing projects
  
  Returns:
    - [tuple] (project_id, owner_id, title, clients, specializations, 
             groupcount, background, requirements, req_knowledge, 
             outcomes, supervision, additional)
  '''
  stmt = "SELECT * FROM projects"
  vals = ()
  curs = run_psql_stmt(stmt, vals)
  ret_list = []
  for rec in curs:
    ret_list.append(Proj_d_full(rec[0], rec[1], rec[2], rec[3], rec[4], rec[5], rec[6], rec[7], rec[8], rec[9], rec[10], rec[11], rec[12]))
  return ret_list

def update_project(projectid: int, ownerid: int, title: str, clients: str, specializations:str, 
                   groupcount: str, background: str, requirements: str, 
                   req_knowledge: str, outcomes: str, supervision: str, additional: str):
  ''' Updates project fields in the database for the given id
  
  Parameters:
  - projectid (integer), id of project to change
  - ownerid (integer), new id
  - title (string), title of project
  - clients (string), clients of project
  - specializations (string)
  - groupcount (string), number of groups that can be assigned to project 
  - background (string)
  - requirements (string)
  - req_knowledge (string)
  - outcomes (string)
  - supervision (string)
  - additional (string)
  '''
  stmt = """UPDATE projects SET 
               ownerid = %s, 
               title = %s, 
               clients = %s, 
               specials = %s, 
               groupcount = %s, 
               background = %s, 
               reqs = %s, 
               reqKnowledge = %s, 
               outcomes = %s, 
               supervision = %s, 
               additional = %s
               WHERE projectid = %s"""
  vals =  (ownerid, title, clients, specializations, 
                groupcount, background, requirements, 
                req_knowledge, outcomes, supervision, additional, projectid)
  run_psql_stmt(stmt, vals, commit=True)
  
def delete_project_by_id(projectid: int):
  ''' Deletes a project given its id also deletes its channel
  
  Parameters:
    - projectid (integer), id of project to delete
  '''
  stmt = """DELETE FROM channels USING projects 
               WHERE projects.projectid = %s 
               AND channels.channelid = projects.channel; 
               DELETE FROM projects WHERE projectid = %s"""
  vals =  (projectid, projectid)
  run_psql_stmt(stmt, vals, commit=True)
  
def assign_project_to_group(projectid: int, groupid: int):
  ''' Assigns a project to a group
      also adds group members to projects channel
  '''
  stmt = """WITH proj AS (SELECT channel FROM projects WHERE projectid = %s)
            UPDATE groups SET assign = %s WHERE groupid = %s RETURNING (SELECT channel FROM proj)"""
  vals =  (projectid, projectid, groupid)
  run_psql_stmt(stmt, vals, commit=True)
  dbChannel.assign_project(projectid, groupid)
  
def unassign_project_from_group(groupid: int):
  ''' Unassigns a groups assigned project
  
  Paramters: 
    groupid (int)
  '''
  projectid = get_group_by_id(groupid).project
  stmt = """WITH proj AS (
                  SELECT projects.channel FROM groups 
                  JOIN projects ON projects.projectid = groups.assign
                  WHERE groupid = %s)
                UPDATE groups SET assign = %s 
                WHERE groupid = %s RETURNING (SELECT channel FROM proj)"""
  vals =  (groupid, None, groupid)
  run_psql_stmt(stmt, vals, commit=True)
  if projectid is not None:
    dbChannel.unassign_project(projectid, groupid)
  
def get_assigned_users(projectid: int):
  ''' Returns all students assigned to a project
  
  Parameters:
    - projectid (int)
    
  Returns:
    - [Int], userids of assigned users
  '''
  stmt = """SELECT users.userid FROM groups 
               JOIN users ON users.groupid = groups.groupid 
               WHERE assign = %s"""
  vals =  (projectid,)
  curs = run_psql_stmt(stmt, vals)
  ret = []
  for rec in curs:
    ret.append(rec[0])
  return ret

#------------------------
# Skills

def create_skill(skillname: str) -> int:
  ''' Creates a new skill in the database
  
  Parameters:
    skillname (string)
    
  Returns:
    integer, id of newly created skill
  '''
  stmt = "INSERT INTO skills (skillname) VALUES (%s) RETURNING skillid"
  vals =  (skillname,)
  curs = run_psql_stmt(stmt, vals, commit=True)
  return curs.fetchone()[0]

def add_skill_to_user(skillid: int, userid: int):
  ''' Adds the given skill to a users list of skills
  
  Parameters:
    skillid (integer), skill to add
    userid (integer), user to add the skill to
  '''
  stmt = "INSERT INTO userskills (userid, skillid) VALUES (%s, %s)"
  vals =  (userid, skillid)
  run_psql_stmt(stmt, vals, commit=True)
  
def remove_skill_from_user(skillid: int, userid: int):
  ''' Removes given skill from list of users skills
  
  Parameters:
    skillid (integer)
    userid (integer)
  '''
  stmt = "DELETE FROM userskills WHERE userid = %s AND skillid = %s"
  vals =  (userid, skillid)
  run_psql_stmt(stmt, vals, commit=True)
  
def add_skill_to_project(skillid: int, projectid:int):
  ''' Adds a skill requirement to a project
  
  Parameters:
    skillid (integer)
    projectid (integer)
  '''
  stmt = "INSERT INTO projectskills (projectid, skillid) VALUES (%s, %s)"
  vals =  (projectid, skillid)
  run_psql_stmt(stmt, vals, commit=True)
  
def remove_skill_from_project(skillid: int, projectid: int):
  '''Removes skill requirement from a project
  
  Parameters
    skillid (integer)
    projectid (integer)
  '''
  stmt = "DELETE FROM projectskills WHERE projectid = %s AND skillid = %s"
  vals =  (projectid, skillid)
  run_psql_stmt(stmt, vals, commit=True)
  
#---------------------------
# Retrieval
def get_skill_by_id(skillid: int) -> Skill_d:
  ''' Queries the database for skill information
  
  Parameters:
    - skillid (integer)
    
  Returns:
    - tuple (skill_id, skill_name)
    - None, if skill does not exist
  '''
  stmt = "SELECT * FROM skills WHERE skillid = %s"
  vals =  (skillid,)
  curs = run_psql_stmt(stmt, vals)
  ret = curs.fetchone()
  if ret == None:
    return None
  return Skill_d(ret[0], ret[1])

def get_all_skills() -> typing.List[Skill_d]:
  ''' Returns a list of all skills and their details
  
  Returns:
    [tuple] (skill_id, skill_name)
  '''
  stmt = "SELECT * FROM skills"
  vals = ()
  curs = run_psql_stmt(stmt, vals)
  ret = []
  for rec in curs:
    ret.append(Skill_d(rec[0], rec[1]))
  return ret

def get_user_skills(userid: int) -> typing.List[int]:
  '''Returns a list of skills that a user has
  
  Returns:
    [integer], skillids for all skills a user has
  '''
  stmt = """SELECT skills.skillid FROM users 
               JOIN userskills ON userskills.userid = users.userid
               JOIN skills ON skills.skillid = userskills.skillid
               WHERE users.userid = %s"""
  vals =  (userid,)
  curs = run_psql_stmt(stmt, vals)
  ret = []
  for rec in curs:
    ret.append(rec[0])
  return ret

def get_project_skills(projectid:int) -> typing.List[Skill_d]:
  '''Returns a list of skills required for a project
  
  Returns:
    [Tuple], (skill_id, skill_name)
  '''
  stmt = """ SELECT skills.skillid, skills.skillname FROM projects
               JOIN projectskills ON projectskills.projectid = projects.projectid
               JOIN skills ON skills.skillid = projectskills.skillid
               WHERE projects.projectid = %s"""
  vals =  (projectid,)
  curs = run_psql_stmt(stmt, vals)
  ret = []
  for rec in curs:
    ret.append(Skill_d(rec[0], rec[1]))
  return ret

def get_group_skills(groupid: int) -> typing.List[Group_skill_d]:
  ''' Gets the combined skills of all memebers of a group
  
  Parameters:
    groupid (integer)
    
  Returns:
    [Tuple], (skill_id, count), skill and number of members with the skill
  '''
  stmt = """ SELECT skills.skillid, COUNT(skills.skillid) FROM users
               JOIN userskills ON userskills.userid = users.userid
               JOIN skills ON skills.skillid = userskills.skillid
               WHERE users.groupid = %s
               GROUP BY skills.skillid"""
  vals =  (groupid,)
  curs = run_psql_stmt(stmt, vals)
  ret = []
  for rec in curs:
    ret.append(Group_skill_d(rec[0], rec[1]))
  return ret

def get_all_groups_skills():
  ''' Gets all skills for all groups
  Returns:
    [tuple], (groupid, skill_id, count)
  '''
  stmt = """ SELECT groups.groupid, skills.skillid, COUNT(skills.skillid) FROM groups
              JOIN users ON users.groupid = groups.groupid
              JOIN userskills ON userskills.userid = users.userid
              JOIN skills ON skills.skillid = userskills.skillid
              GROUP BY groups.groupid, skills.skillid"""
  vals = ()
  curs = run_psql_stmt(stmt, vals)
  ret = []
  for rec in curs:
    ret.append(Groups_skill_d(rec[0], rec[1], rec[2]))
  return ret

def get_all_project_skills():
  ''' Gets all skills for all projects
  
  Returns:
    [tuple], (projectid, groupcount, skillid)
    
  Notes:
    Groupcount will be 0, if the groupcount stored was something other than a number
  '''
  stmt = """SELECT projects.projectid, projects.groupcount, projectskills.skillid FROM projects
               JOIN projectskills ON projectskills.projectid = projects.projectid"""
  vals = ()
  curs = run_psql_stmt(stmt, vals)
  ret = []
  for rec in curs:
    groupcount = 0
    try:
      groupcount = int(rec[1])
    except:
      groupcount = 0
    ret.append(Projects_skill_d(rec[0], groupcount, rec[2]))
  return ret

#-----------------------
# Reset codes

def create_reset_code(userid: int, code: str, timestamp: datetime):
  ''' Creates a code for resetting a password in the database
  
  Parameters:
    userid (integer)
    code (string)
    timestamp (datetime)
    
  Notes:
    There should only ever be one code per user -- this function will handle that
  '''
  stmt = """INSERT INTO resetcodes (userid, code, created) VALUES (%s, %s, %s)
                  ON CONFLICT (userid) DO UPDATE
                  SET code = %s, created = %s"""
  vals =  (userid, code, timestamp, code, timestamp)
  run_psql_stmt(stmt, vals, commit=True)
  
def get_reset_code(userid: int):
  ''' Gets the reset code for a user
  
  Parameters:
    userid (int)
  
  Returns:
    tuple, (userid, code, timestamp)
    None, if code does not exist
  '''
  stmt = """SELECT * FROM resetcodes WHERE userid = %s"""
  vals =  (userid,)
  curs = run_psql_stmt(stmt, vals)
  rec = curs.fetchone()
  if rec == None:
      return None
  return Reset_code_d(rec[0], rec[1], rec[2])

def remove_reset_code(userid: int):
  ''' Removes the reset code for the user
  
  Parameters:
    userid (integer)
  '''
  stmt = "DELETE FROM resetcodes WHERE userid = %s"
  vals =  (userid,)
  run_psql_stmt(stmt, vals, commit=True)

#--------------------
#Preferences

def create_preferences(userid: int, projectids: typing.List[int], ranks: typing.List[int]):
  ''' Creates preferences for a user in the database
  
  Paremeters:
    userid (integer)
    projectids list[integer], list of all projectids
    ranks list[integer], ranks corresponding to projects 
  '''
  vals = []
  for i in range(0, len(projectids)):
    vals.append((userid, projectids[i], ranks[i]))
  conn = connpool.getconn()
  curs = conn.cursor()
  psycopg2.extras.execute_values(curs, "INSERT INTO preferences (userid, projectid, rank) VALUES %s", vals)
  conn.commit()
  connpool.putconn(conn)
  
def delete_preferences(userid: int):
  ''' Deletes all preferences a user has

  Paramters:
    userid (integer)
  '''
  stmt = "DELETE FROM preferences WHERE userid = %s"
  vals =  (userid,)
  run_psql_stmt(stmt, vals, commit=True)
  
def get_user_preferences(userid: int) -> typing.List[User_pref_d]:
  ''' Gets a single users preferences
  
  Paremeters:
    userid (integer)
    
  Returns:
    list[tuple] (projectid, rank)
  '''
  stmt = "SELECT projectid, rank FROM preferences WHERE userid = %s"
  vals =  (userid,)
  curs = run_psql_stmt(stmt, vals)
  ret = []
  for rec in curs:
    ret.append(User_pref_d(rec[0], rec[1]))
  return ret

def get_all_preferences():
  ''' Gets all preferences in the system
  
  Returns:
    list[tuple] (groupid, projectid, rank)
  
  Notes:
    This will not get preferences for users that are not in a group
  '''
  stmt = """SELECT groups.groupid, preferences.projectid, preferences.rank FROM groups
              JOIN users ON users.groupid = groups.groupid
              JOIN preferences ON preferences.userid = USERS.userid"""
  vals = ()
  curs = run_psql_stmt(stmt, vals)
  ret = []
  for rec in curs:
    ret.append(Group_pref_d(rec[0], rec[1], rec[2]))
  return ret
  
#--------
# Notifications

def create_notif(userid: int, content: str) -> int:
  ''' Creates a notification for given user
  
  Parameters:
    userid (integer)
    timestamp (datetime.datetime), time of creation
    content (string)
    
  Returns:
    notificationid, id of notification just created
  '''
  stmt = "INSERT INTO notifications (userid, isnew, content) VALUES (%s, %s, %s) RETURNING notifid"
  vals =  (userid, True, content)
  curs = run_psql_stmt(stmt, vals, commit=True)
  return curs.fetchone()[0]

def get_notif_by_id(notifid: int) -> Notif_d_full:
  ''' Queries the database for notif information
  
  Parameters:
    - notifid (integer)
    
  Returns:
    - tuple (notifid, userid, created, isnew, content)
    - None, if project does not exist
  '''
  stmt = "SELECT * FROM notifications WHERE notifid = %s"
  vals =  (notifid,)
  curs = run_psql_stmt(stmt, vals)
  ret = curs.fetchone()
  if ret == None:
    return None
  return Notif_d_full(ret[0], ret[1], ret[2], ret[3], ret[4])
  
def get_notifs(userid: int) -> typing.List[Notif_d_base]:
  ''' Returns all notifs for a given user
  
  Paremters:
    userid (integer)
    
  Returns:
    [tuple] (notifid, timestamp, content)
  '''
  stmt = """ WITH update AS 
              (UPDATE notifications SET isnew = %s WHERE userid = %s RETURNING notifid, created, content)
              SELECT * FROM update ORDER BY created DESC"""
  vals =  (False, userid)
  curs = run_psql_stmt(stmt, vals, commit=True)
  ret = []
  for rec in curs:
    ret.append(Notif_d_base(rec[0], rec[1], rec[2]))
  return ret

def get_new_notifs(userid: int) -> int:
  ''' Gets the number of new notifications a user has
    Notifications are no longer 'new' if get_notifs has been called before
    
  Parameters:
    userid (int)
  
  Returns:
    int, number of new notifs
  '''
  stmt = "SELECT count(*) FROM notifications WHERE userid = %s AND isnew = %s"
  vals =  (userid, True)
  curs = run_psql_stmt(stmt, vals)
  return curs.fetchone()[0]

def delete_notif(notifid: int):
  ''' Deletes the specified notification

  Parameters:
    notifid (integer)
  '''
  stmt = "DELETE FROM notifications WHERE notifid = %s"
  vals =  (notifid,)
  run_psql_stmt(stmt, vals, commit=True)
  
def delete_all_notifs(userid: int):
  ''' Deletes all notifs that a user has
  
  Paramters:
    userid (integer)
  '''
  stmt = "DELETE FROM notifications WHERE userid = %s"
  vals =  (userid,)
  run_psql_stmt(stmt, vals, commit=True)
  
#-----------------
# Channels
# manipulation

def create_channel(channelname: str) -> int:
  ''' Creates a new channel in the database
  
  Parameters:
    channelname (string)
  
  Returns:
    channelid (int), id of newly created channel
    
  Notes:
    automatically called in create_group and create_project
  '''
  stmt = "INSERT INTO channels (channelname) VALUES (%s) RETURNING channelid"
  vals =  (channelname,)
  curs = run_psql_stmt(stmt, vals, commit=True)
  return curs.fetchone()[0]

def delete_channel(channelid: int):
  ''' Deletes a channel in the database
      Should also delete all messages for said channel
      
  Parameters:
    channelid (int)
  
  Notes:
    channels are deleted automatically when groups/projects are deleted
    Should also 'unassign' channels from projects and groups automatically
  '''
  stmt = """DELETE FROM channels WHERE channelid = %s"""
  vals =  (channelid,)
  run_psql_stmt(stmt, vals, commit=True)

def assign_channel_to_group(channelid: int, groupid: int):
  ''' Assigns a channel to a group
  
  Parameters:
    channelid (int)
    groupid (int)  
    
  Notes:
    automatically called in create_group
  '''
  stmt = "UPDATE groups SET channel = %s WHERE groupid = %s"
  vals =  (channelid, groupid)
  run_psql_stmt(stmt, vals, commit=True)

def assign_channel_to_project(channelid: int, projectid: int):
  ''' Assigns a channel to a project
  
  Parameters:
    channelid (int)
    projectid (int)
  
  Notes:
    automatically called in create_project
    Must also use add_user_to_channel(), will not automatically give group members access to channels
  '''
  stmt = "UPDATE projects SET channel = %s WHERE projectid = %s"
  vals =  (channelid, projectid)
  run_psql_stmt(stmt, vals, commit=True)

def add_user_to_channel(userid: int, channelid: int):
  ''' Gives specified user access to specified channel
  
  Parameters:
    userid (int)
    channelid (int)
    
  Notes:
    automatically called in add_user_to_group, create_project and create_group (for project and group owners)
  '''
  stmt = "INSERT INTO accesschannels (userid, channelid) VALUES (%s, %s)"
  vals =  (userid, channelid)
  run_psql_stmt(stmt, vals, commit=True)

def add_users_to_channel(userids: typing.List[int], channelid: int):
  ''' adds multiple users to a given channel
      slightly faster than performing multiple calls to add_user_to_channel
      
  Paramters:
    - userids ([int])
    - channelid (int)
  '''
  conn = connpool.getconn()
  vals = [(x, channelid) for x in userids]
  curs = conn.cursor()
  psycopg2.extras.execute_values(curs, "INSERT INTO accesschannels (userid, channelid) VALUES %s", vals)
  conn.commit()
  connpool.putconn(conn)

def remove_user_from_channel(userid:int, channelid: int):
  ''' Removes a specified user's access to a specified channel
  
  Parameters:
    userid (int)
    channelid (int)
    
  Notes:
    users are removed automatically in remove_user_from_group
  '''
  stmt = "DELETE FROM accesschannels WHERE userid = %s AND channelid = %s"
  vals =  (userid, channelid)
  run_psql_stmt(stmt, vals, commit=True)

def remove_users_from_channel(userids: typing.List[int], channelid: int):
  ''' Removes multiple users from a channel 
      should be faster than running multiple remove user
      
  Paramters:
    userids ([int])
    channelid (int)
  '''
  stmt = "DELETE FROM accesschannels WHERE userid IN %s AND channelid = %s"
  vals =  (tuple(userids), channelid)
  run_psql_stmt(stmt, vals, commit=True)
  
#retrieval
def get_users_channels(userid: int) -> typing.List[Channel_d_base]:
  ''' Gets all channels a user has access to
  
  Parameters:
    userid (int)
    
  Returns:
    [tuple] (channelid, channel_name)
  '''
  stmt = """SELECT channels.channelid, channels.channelname FROM users
               JOIN accesschannels ON accesschannels.userid = users.userid
               JOIN channels ON channels.channelid = accesschannels.channelid
               WHERE users.userid = %s"""
  vals =  (userid,)
  curs = run_psql_stmt(stmt, vals)
  ret = []
  for rec in curs:
    ret.append(Channel_d_base(rec[0], rec[1]))
  return ret

def get_all_channels() -> typing.List[Channel_d_base]:
  ''' Returns all channels that currently exist
  
  Returns:
    [tuple] (channelid, channel_name)
  '''
  stmt = "SELECT channelid, channelname FROM channels"
  vals = ()
  curs = run_psql_stmt(stmt, vals)
  ret = []
  for rec in curs:
    ret.append(Channel_d_base(rec[0], rec[1]))
  return ret

def get_channel_members(channelid: int) -> typing.List[User_d_base]:
  ''' Gets all members that have access to specified channel
  
  Parameters:
    channelid (int)
    
  Returns
    [tuple] (userid, first_name, last_name)
  '''
  stmt = """SELECT users.userid, users.firstName, users.lastName FROM channels
              JOIN accesschannels ON accesschannels.channelid = channels.channelid
              JOIN users ON users.userid = accesschannels.userid
              WHERE channels.channelid = %s"""
  vals =  (channelid,)
  curs = run_psql_stmt(stmt, vals)
  ret = []
  for rec in curs:
    ret.append(User_d_base(rec[0], rec[1], rec[2]))
  return ret

#-----------------
# Messages
# manipulation

def create_message(channelid: int, ownerid: int, content: str):
  ''' Creates a message inside a given channel
  
  Parameters:
    channelid (int)
    ownerid (int)
    content (string)
  
  Notes:
    The timestamp for the message is created automatically in the databse (see the 'DEFAULT current_timestamp')
  '''
  stmt = "INSERT INTO messages (channelid, ownerid, content) VALUES (%s, %s, %s) RETURNING messageid"
  vals =  (channelid, ownerid, content)
  curs = run_psql_stmt(stmt, vals, commit=True)
  return curs.fetchone()[0]

def get_message_by_id(messageid: int) -> Message_d_base:
  ''' Queries the database for message information
  
  Parameters:
    - messageid (integer)
    
  Returns:
    - tuple (messageid, ownerid, timestamp, content)
    - None, if project does not exist
  '''
  stmt = "SELECT messageid, ownerid, created, content FROM messages WHERE messageid = %s"
  vals =  (messageid,)
  curs = run_psql_stmt(stmt, vals)
  ret = curs.fetchone()
  if ret == None:
    return None
  return Message_d_base(ret[0], ret[1], ret[2], ret[3])

def edit_message(messageid: int, content: str):
  ''' Edits the content of a specified message
  
  Parameters:
    messageid (int)
    content (string)
  '''
  stmt = "UPDATE messages SET content = %s WHERE messageid = %s"
  vals =  (content, messageid)
  run_psql_stmt(stmt, vals, commit=True)

def delete_message(messageid: int):
  ''' Deletes a specified message
  
  Parameters:
    messageid (int)
  '''
  stmt = "DELETE FROM messages WHERE messageid = %s"
  vals =  (messageid,)
  run_psql_stmt(stmt, vals, commit=True)

#retrieval
def get_channel_messages(channelid: int, last_message: int = None) -> typing.List[Message_d_base]:
  ''' Gets a page of messages given the last message
      Gets 50 messages before the last_message given
      If no last_message is supplied, gets the latest 50 messages sent in a channel
  
  Paramters:
    channelid (int)
    last_message (int), min message id in last page retrieved
    
  Returns:
    [tuple] (messageid, ownerid, timestamp, content)
  '''
  if last_message == None: 
    stmt = "SELECT MAX(messageid) FROM messages"
    vals = ()
    curs = run_psql_stmt(stmt, vals)
    last_message = curs.fetchone()[0]
    if last_message == None:
      #there are no messages
      return []
    else:
      last_message += 1
  stmt = """SELECT messageid, ownerid, created, content FROM messages 
               WHERE channelid = %s 
               AND messageid < %s
               ORDER BY messageid desc
               LIMIT 50"""
  vals =  (channelid, last_message)
  curs = run_psql_stmt(stmt, vals)
  ret = []
  for rec in curs:
    ret.append(Message_d_base(rec[0], rec[1], rec[2], rec[3]))
  return ret

def get_latest_message(channelid: int) -> Message_d_base:
  ''' Gets the latest message sent in a channel, useful for real-time-updating when a message is sent
  
  Parameters:
    channelid (int)
    
  Returns:
    tuple (messageid, ownerid, timestamp, content)
    None, if there are no messages in the channel
  '''
  stmt = """SELECT messageid, ownerid, created, content FROM messages 
               WHERE channelid = %s 
               ORDER BY created DESC
               LIMIT 1"""
  vals =  (channelid,)
  curs = run_psql_stmt(stmt, vals)
  rec = curs.fetchone()
  if rec == None:
    return None
  return Message_d_base(rec[0], rec[1], rec[2], rec[3])
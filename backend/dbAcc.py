import psycopg2
import typing
from collections import namedtuple

# TODO: swap to using connection pool
try: 
  conn = psycopg2.connect(dbname='projdb', user='postgres', password='postgres', host="postgres")
except: 
  print("Unable to connect to database.")
  exit()
  
#setup namedtuples
User_d_full = namedtuple("User_d_full", ["userid", "email", "first_name", "last_name", "password", "role", "groupid"])
User_d_base = namedtuple("User_d_base", ["userid", "first_name", "last_name"])
Group_d_full = namedtuple("Group_d_full", ["groupid", "ownerid", "group_name"])
Group_d_base = namedtuple("Group_d_base", ["groupid", "group_name", "member_count"])
Proj_d_full = namedtuple("Proj_d_full", ["project_id", "owner_id", "title", "clients", "specializations", 
                                         "groupcount", "background", "requirements", "req_knowledge", 
                                         "outcomes", "supervision", "additional"])
Skill_d = namedtuple("Skill_d", ["skill_id", "skill_name"])

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
  curs = conn.cursor()
  curs.execute("INSERT INTO users (email, password, firstname, lastname, role) VALUES (%s, %s, %s, %s, %s) RETURNING userid", 
               (email, password, first_name, last_name, role))
  conn.commit()
  return curs.fetchone()[0]

def update_password(userid: int, password: str):
  ''' Updates a users password with given value
  
  Parameters:
    - userid (integer), id of user to change
    - password (string), new password
  '''
  curs = conn.cursor()
  curs.execute("UPDATE users SET password = %s WHERE userid = %s", (password, userid))
  conn.commit()

def update_role(userid: int, role: int):
  ''' Modifies the role of a user
  
  Parameters:
    - userid, id of user to issue change
    - role (integer), new role
  '''
  curs = conn.cursor()
  curs.execute("UPDATE users SET role = %s WHERE userid = %s", (role, userid))
  conn.commit()
  
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
  curs = conn.cursor()
  curs.execute("SELECT * FROM users WHERE userid = %s", (userid,))
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
  curs = conn.cursor()
  curs.execute("SELECT * FROM users WHERE email = %s", (email,))
  deets = curs.fetchone()
  if deets == None:
    return None
  return User_d_full(deets[0], deets[1], deets[2], deets[3], deets[4], deets[5], deets[6])

#--------------------------------
#   Groups
# Manipulation
def create_group(ownerid: int, group_name: str) -> int:
  ''' Creates a new group, sets its owner, and adds its owner to the group
  
  Parameters:
    - ownerid (integer), user id of owner/creator
    - group_name (string)
    
  Returns:
    - groupid (integer)
  '''
  curs = conn.cursor()
  curs.execute("INSERT INTO groups (ownerid, groupname) VALUES (%s, %s) RETURNING groupid", (ownerid, group_name))
  conn.commit()
  new_group_id = curs.fetchone()[0]
  add_user_to_group(ownerid, new_group_id)
  return new_group_id
  
def add_user_to_group(userid: int, group_id: int):
  ''' Adds user to specified group
  
  Parameters
    - userid (integer), user id of person to add
    - group_id (integer)
  '''
  curs = conn.cursor()
  curs.execute("UPDATE users SET groupid = %s WHERE userid = %s", (group_id, userid))
  conn.commit()
  
def remove_user_from_group(userid: int):
  ''' Removes a user from the group they may be in
  
  Parameters:
    - userid (integer) 
  '''
  curs = conn.cursor()
  # Should we check and reassign owner if we need to?
  # curs.execute("""SELECT groups.groupid 
  #              FROM users
  #              JOIN groups
  #              ON groups.ownerid = %s""", (userid))
  # owned_group = curs.fetchone()
  # if owned_group != None:
  #   get_group_members(owned_group)
  curs.execute("UPDATE users SET groupid = NULL WHERE userid = %s", (userid,))
  conn.commit()

# Retrieval
def get_all_groups() -> typing.List[Group_d_base]:
  ''' Queries databse for details on every group
  
  Returns:
    - [tuple] (groupid, groupname, member_count) 
  '''
  curs = conn.cursor()
  curs.execute("""SELECT groups.groupid, groups.groupname, COUNT(users.userid) 
               FROM groups 
               JOIN users 
               ON users.groupid = groups.groupid
               GROUP BY groups.groupid""")
  ret_list = []
  for rec in curs:
    ret_list.append(rec)
  return ret_list

def get_group_by_id(groupid: int) -> Group_d_full:
  ''' Queries the database for information on a particular group
  
  Parameters:
    - groupid (integer)
    
  Returns:
    - tuple (groupid, ownerid, group_name)
    - None, if groupid is invalid
  '''
  curs = conn.cursor()
  curs.execute("SELECT * FROM groups WHERE groupid=%s", (groupid,))
  deets = curs.fetchone()
  if deets == None:
      return None
  return Group_d_full(deets[0], deets[1], deets[2])

def get_groupcount_by_name(groupname: str) -> int:
  ''' Queries the databse for the number of groups with a given name
  
  Parameters:
   - groupname (string)
   
  Returns:
    - int, number of groups sharing the given name
  '''
  curs = conn.cursor()
  curs.execute("SELECT count(*) FROM groups WHERE groupname = %s", (groupname,))
  return curs.fetchone()[0]
  
def get_group_members(groupid: int) -> typing.List[User_d_base]:
  ''' Get details for all members of a given group
  
  Parameters:
    - groupid (integer)
    
  returns:
    - [tuple] (userid, first_name, last_name) 
    - [] if group does not exist
  '''
  curs = conn.cursor()
  curs.execute("SELECT userid, firstname, lastname FROM users WHERE groupid = %s", (groupid,))
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
  curs = conn.cursor()
  curs.execute("INSERT INTO grouprequests (userid, groupid) VALUES (%s, %s)", (userid, groupid))
  conn.commit()
  
def remove_all_join_requests(userid: int):
  ''' Removes all group join requests that a user has made
  
  Parameters:
    - userid (integer), user whose requests should be removed
    
  Notes:
    For use when a users request is approved, we should delete all others
  '''
  curs = conn.cursor()
  curs.execute("DELETE FROM grouprequests WHERE userid = %s", (userid,))
  conn.commit()
  
def remove_join_request(userid: int, groupid: int):
  ''' Removes a single join request for a group from a user
  
  Parameters:
    - userid (integer), userid of who made the request
    - groupid (integer), groupid of specific request
  '''
  curs = conn.cursor()
  curs.execute("DELETE FROM grouprequests WHERE userid = %s AND groupid = %s", (userid, groupid))
  conn.commit()
  
# Retrieval
def get_join_requests(userid: int) -> typing.List[User_d_base]:
  ''' Gets all join requests for group that the user is an owner of
  
  Parameters:
    - userid (integer)
    
  Returns:
    - [tuples(userid, first_name, last_name)], details of user attempting to join
    - [], if there are no requests
  '''
  curs = conn.cursor()
  curs.execute("""SELECT grouprequests.userid, users.firstName, users.lastName
               FROM groups
               JOIN grouprequests
               ON groups.groupid = grouprequests.groupid
               JOIN users
               ON users.userid = grouprequests.userid
               WHERE groups.ownerid = %s
               """, (userid,))
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
  ''' Creates a project in the database
  
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
  curs = conn.cursor()
  curs.execute("""INSERT INTO projects 
               (ownerid, title, clients, specials, groupcount, background, reqs, reqKnowledge, outcomes, supervision, additional)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
               RETURNING projectid""", 
               (ownerid, title, clients, specializations, 
                groupcount, background, requirements, 
                req_knowledge, outcomes, supervision, additional))
  conn.commit()
  return curs.fetchone()[0]

def get_project_by_id(projectid: int) -> Proj_d_full:
  ''' Queries the database for project information
  
  Parameters:
    - projectid (integer)
    
  Returns:
    - tuple (project_id, owner_id, title, clients, specializations, 
             groupcount, background, requirements, req_knowledge, 
             outcomes, supervision, additional)
    - None, if project does not exist
  '''
  curs = conn.cursor()
  curs.execute("SELECT * FROM projects WHERE projectid = %s", (projectid,))
  ret = curs.fetchone()
  if ret == None:
    return None
  return Proj_d_full(ret[0], ret[1], ret[2], ret[3], ret[4], ret[5], ret[6], ret[7], ret[8], ret[9], ret[10], ret[11])

def get_all_projects() -> typing.List[Proj_d_full]:
  ''' Queries the database for all existing projects
  
  Returns:
    - [tuple] (project_id, owner_id, title, clients, specializations, 
             groupcount, background, requirements, req_knowledge, 
             outcomes, supervision, additional)
  '''
  curs = conn.cursor()
  curs.execute("SELECT * FROM projects")
  ret_list = []
  for rec in curs:
    ret_list.append(Proj_d_full(rec[0], rec[1], rec[2], rec[3], rec[4], rec[5], rec[6], rec[7], rec[8], rec[9], rec[10], rec[11]))
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
  curs = conn.cursor()
  curs.execute("""UPDATE projects SET 
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
               WHERE projectid = %s""", 
               (ownerid, title, clients, specializations, 
                groupcount, background, requirements, 
                req_knowledge, outcomes, supervision, additional, projectid))
  conn.commit()
  
def delete_project_by_id(projectid: int):
  ''' Deletes a project given its id
  
  Parameters:
    - projectid (integer), id of project to delete
  '''
  curs = conn.cursor()
  #preferences and groups have foreign keys to projects, remember this
  curs.execute("DELETE FROM projects WHERE projectid = %s", (projectid,))
  conn.commit()
  
#------------------------
# Skills

def create_skill(skillname: str) -> int:
  ''' Creates a new skill in the database
  
  Parameters:
    skillname (string)
    
  Returns:
    integer, id of newly created skill
  '''
  curs = conn.cursor()
  curs.execute("INSERT INTO skills (skillname) VALUES (%s) RETURNING skillid", (skillname,))
  conn.commit()
  return curs.fetchone()[0]

def add_skill_to_user(skillid: int, userid: int):
  ''' Adds the given skill to a users list of skills
  
  Parameters:
    skillid (integer), skill to add
    userid (integer), user to add the skill to
  '''
  curs = conn.cursor()
  curs.execute("INSERT INTO userskills (userid, skillid) VALUES (%s, %s)", (userid, skillid))
  conn.commit()
  
def remove_skill_from_user(skillid: int, userid: int):
  ''' Removes given skill from list of users skills
  
  Parameters:
    skillid (integer)
    userid (integer)
  '''
  curs = conn.cursor()
  curs.execute("DELETE FROM userskills WHERE userid = %s AND skillid = %s", (userid, skillid))
  conn.commit()
  
def add_skill_to_project(skillid: int, projectid:int):
  ''' Adds a skill requirement to a project
  
  Parameters:
    skillid (integer)
    projectid (integer)
  '''
  curs = conn.cursor()
  curs.execute("INSERT INTO projectskills (projectid, skillid) VALUES (%s, %s)", (projectid, skillid))
  conn.commit()
  
def remove_skill_from_project(skillid: int, projectid: int):
  '''Removes skill requirement from a project
  
  Parameters
    skillid (integer)
    projectid (integer)
  '''
  curs = conn.cursor()
  curs.execute("DELETE FROM projectskills WHERE projectid = %s AND skillid = %s", (projectid, skillid))
  conn.commit()
  
#---------------------------
# Retrieval
def get_all_skills() -> typing.List[Skill_d]:
  ''' Returns a list of all skills and their details
  
  Returns:
    [tuple] (skill_id, skill_name)
  '''
  curs = conn.cursor()
  curs.execute("SELECT * FROM skills")
  ret = []
  for rec in curs:
    ret.append(Skill_d(rec[0], rec[1]))
  return ret

def get_user_skills(userid: int) -> typing.List[int]:
  '''Returns a list of skills that a user has
  
  Returns:
    [integer], skillids for all skills a user has
  '''
  curs = conn.cursor()
  curs.execute("""SELECT skills.skillid FROM users 
               JOIN userskills ON userskills.userid = users.userid
               JOIN skills ON skills.skillid = userskills.skillid
               WHERE users.userid = %s""", (userid,))
  ret = []
  for rec in curs:
    ret.append(rec[0])
  return ret

def get_project_skills(projectid:int) -> typing.List[Skill_d]:
  '''Returns a list of skills required for a project
  
  Returns:
    [Tuple], (skill_id, skill_name)
  '''
  curs = conn.cursor()
  curs.execute(""" SELECT skills.skillid, skills.skillname FROM projects
               JOIN projectskills ON projectskills.projectid = projects.projectid
               JOIN skills ON skills.skillid = projectskills.skillid
               WHERE projects.projectid = %s""", (projectid,))
  ret = []
  for rec in curs:
    ret.append(Skill_d(rec[0], rec[1]))
  return ret

def get_group_skills(groupid: int) -> typing.List[int]:
  ''' Gets the combined skills of all memebers of a group
  
  Parameters:
    groupid (integer)
    
  Returns:
    [integer], skillids for all memebers of a group
  '''
  curs = conn.cursor()
  curs.execute(""" SELECT skills.skillid FROM users
               JOIN userskills ON userskills.userid = users.userid
               JOIN skills ON skills.skillid = userskills.skillid
               WHERE users.groupid = %s""", (groupid,))
  ret = []
  for rec in curs:
    ret.append(rec[0])
  return ret
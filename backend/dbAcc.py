import psycopg2
import typing
from collections import namedtuple
from datetime import datetime

import psycopg2.extras

# TODO: swap to using connection pool
try:
  conn = psycopg2.connect(dbname='projdb', user='postgres', password='postgres', host="postgres")
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
Notif_d_base = namedtuple("Notif_d_base", ["notifid", "timestamp", "content"])
Channel_d_base = namedtuple("Channel_d_base", ["channelid", "channel_name"])
Message_d_base = namedtuple("Message_d_base", ["messageid", "ownerid", "timestamp", "content"])

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

def update_user_name(userid: int, firstName: str, lastName: str):
  ''' Modifies the name of a user

  Parameters:
    - userid, id of user to issue change
    - firstName (String)
    - lastName (String)
  '''
  curs = conn.cursor()
  curs.execute("UPDATE users SET firstName = %s, lastName = %s WHERE userid = %s", (firstName, lastName, userid))
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
  ''' Creates a new group, sets its owner, adds its owner to the group
      creates a channel for the group and adds its owner to the channel
  
  Parameters:
    - ownerid (integer), user id of owner/creator
    - group_name (string)
    
  Returns:
    - groupid (integer)
  '''
  curs = conn.cursor()
  curs.execute("INSERT INTO groups (ownerid, groupname) VALUES (%s, %s) RETURNING groupid", (ownerid, group_name))
  conn.commit()
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
  curs = conn.cursor()
  curs.execute("UPDATE users SET groupid = %s WHERE userid = %s", (groupid, userid))
  conn.commit()
  new_grp_d = get_group_by_id(groupid)
  add_user_to_channel(userid, new_grp_d.channel)

  
def update_group_owner(userid: int, groupid: int):
  ''' Updates the owner of  a given group
  
  Parameters:
    userid (int), new owner of group
    groupid (int)
  '''
  curs = conn.cursor()
  curs.execute("UPDATE groups SET ownerid = %s WHERE groupid = %s", (userid, groupid))
  conn.commit()
  
def remove_user_from_group(userid: int):
  ''' Removes a user from the group they are in, 
      also removes them from the group's channel 
  
  Parameters:
    - userid (integer) 
  '''
  curs = conn.cursor()
  #ownership transferred in backend funcs rather than here
  curs.execute(""" DELETE FROM accesschannels 
               WHERE userid = %s 
               AND channelid = (
                SELECT groups.channel FROM users 
                JOIN groups ON groups.groupid = users.groupid 
                WHERE users.userid = %s);
               UPDATE users SET groupid = NULL WHERE userid = %s""", (userid, userid, userid))
  conn.commit()

def delete_group(groupid : int):
  ''' Deletes a group from the system, also deletes group's channel
  
  Parameters:
    groupid (int)
    
  Notes:
    all users access to the group's channel should also be deleted, 
    but delete group only gets called when everyone leaves, 
    and leaving groups also removes access 
  '''
  curs = conn.cursor()
  curs.execute("""DELETE FROM channels USING groups 
               WHERE groups.groupid = %s 
               AND channels.channelid = groups.channel;
               DELETE FROM groups WHERE groupid = %s""", (groupid, groupid))
  
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
    - tuple (groupid, ownerid, group_name, project, channel)
    - None, if groupid is invalid
    
  Notes:
    Project and channel in the return tuple may be None if no group or channel is assigned
  '''
  curs = conn.cursor()
  curs.execute("SELECT * FROM groups WHERE groupid=%s", (groupid,))
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
  curs = conn.cursor()
  curs.execute("""INSERT INTO projects 
               (ownerid, title, clients, specials, groupcount, background, reqs, reqKnowledge, outcomes, supervision, additional)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
               RETURNING projectid""", 
               (ownerid, title, clients, specializations, 
                groupcount, background, requirements, 
                req_knowledge, outcomes, supervision, additional))
  conn.commit()
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
  curs = conn.cursor()
  curs.execute("SELECT * FROM projects WHERE projectid = %s", (projectid,))
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
  curs = conn.cursor()
  curs.execute("SELECT * FROM projects")
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
  ''' Deletes a project given its id also deletes its channel
  
  Parameters:
    - projectid (integer), id of project to delete
  '''
  curs = conn.cursor()
  curs.execute("""DELETE FROM channels USING projects 
               WHERE projects.projectid = %s 
               AND channels.channelid = projects.channel; 
               DELETE FROM projects WHERE projectid = %s""", (projectid, projectid))
  conn.commit()
  
def assign_project_to_group(projectid: int, groupid: int):
  ''' Assigns a project to a group
      also adds group members to projects channel
  '''
  curs = conn.cursor()
  curs.execute("""WITH proj AS (SELECT channel FROM projects WHERE projectid = %s)
                  UPDATE groups SET assign = %s WHERE groupid = %s RETURNING (SELECT channel FROM proj)""", (projectid, projectid, groupid))
  conn.commit()
  ch_id = curs.fetchone()[0]
  usr_d_l = get_group_members(groupid)
  usr_id_l = [x.userid for x in usr_d_l]
  add_users_to_channel(usr_id_l, ch_id)
  
def unassign_project_from_group(groupid: int):
  ''' Unassigns a groups assigned project
  
  Paramters: 
    groupid (int)
  '''
  curs = conn.cursor()
  curs.execute("""WITH proj AS (
                  SELECT projects.channel FROM groups 
                  JOIN projects ON projects.projectid = groups.assign
                  WHERE groupid = %s)
                UPDATE groups SET assign = %s 
                WHERE groupid = %s RETURNING (SELECT channel FROM proj)""", (groupid, None, groupid))
  conn.commit()
  ch_id = curs.fetchone()[0]
  usr_d_l = get_group_members(groupid)
  usr_id_l = [x.userid for x in usr_d_l]
  remove_users_from_channel(usr_id_l, ch_id)
  
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
def get_skill_by_id(skillid: int) -> Skill_d:
  ''' Queries the database for skill information
  
  Parameters:
    - skillid (integer)
    
  Returns:
    - tuple (skill_id, skill_name)
    - None, if skill does not exist
  '''
  curs = conn.cursor()
  curs.execute("SELECT * FROM skills WHERE skillid = %s", (skillid,))
  ret = curs.fetchone()
  if ret == None:
    return None
  return Skill_d(ret[0], ret[1])

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

def get_group_skills(groupid: int) -> typing.List[Group_skill_d]:
  ''' Gets the combined skills of all memebers of a group
  
  Parameters:
    groupid (integer)
    
  Returns:
    [Tuple], (skill_id, count), skill and number of members with the skill
  '''
  curs = conn.cursor()
  curs.execute(""" SELECT skills.skillid, COUNT(skills.skillid) FROM users
               JOIN userskills ON userskills.userid = users.userid
               JOIN skills ON skills.skillid = userskills.skillid
               WHERE users.groupid = %s
               GROUP BY skills.skillid""", (groupid,))
  ret = []
  for rec in curs:
    ret.append(Group_skill_d(rec[0], rec[1]))
  return ret

def get_all_groups_skills():
  ''' Gets all skills for all groups
  Returns:
    [tuple], (groupid, skill_id, count)
  '''
  curs = conn.cursor()
  curs.execute(""" SELECT groups.groupid, skills.skillid, COUNT(skills.skillid) FROM groups
              JOIN users ON users.groupid = groups.groupid
              JOIN userskills ON userskills.userid = users.userid
              JOIN skills ON skills.skillid = userskills.skillid
              GROUP BY groups.groupid, skills.skillid""")
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
  curs = conn.cursor()
  curs.execute("""SELECT projects.projectid, projects.groupcount, projectskills.skillid FROM projects
               JOIN projectskills ON projectskills.projectid = projects.projectid""")
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
  curs = conn.cursor()
  curs.execute("""INSERT INTO resetcodes (userid, code, created) VALUES (%s, %s, %s)
                  ON CONFLICT (userid) DO UPDATE
                  SET code = %s, created = %s""", (userid, code, timestamp, code, timestamp))
  conn.commit()
  
def get_reset_code(userid: int):
  ''' Gets the reset code for a user
  
  Parameters:
    userid (int)
  
  Returns:
    tuple, (userid, code, timestamp)
    None, if code does not exist
  '''
  curs = conn.cursor()
  curs.execute("""SELECT * FROM resetcodes WHERE userid = %s""", (userid,))
  rec = curs.fetchone()
  if rec == None:
      return None
  return Reset_code_d(rec[0], rec[1], rec[2])

def remove_reset_code(userid: int):
  ''' Removes the reset code for the user
  
  Parameters:
    userid (integer)
  '''
  curs = conn.cursor()
  curs.execute("DELETE FROM resetcodes WHERE userid = %s", (userid,))
  conn.commit()

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
  curs = conn.cursor()
  psycopg2.extras.execute_values(curs, "INSERT INTO preferences (userid, projectid, rank) VALUES %s", vals)
  conn.commit()
  
def delete_preferences(userid: int):
  ''' Deletes all preferences a user has

  Paramters:
    userid (integer)
  '''
  curs = conn.cursor()
  curs.execute("DELETE FROM preferences WHERE userid = %s", (userid,))
  conn.commit()
  
def get_user_preferences(userid: int) -> typing.List[User_pref_d]:
  ''' Gets a single users preferences
  
  Paremeters:
    userid (integer)
    
  Returns:
    list[tuple] (projectid, rank)
  '''
  curs = conn.cursor()
  curs.execute("SELECT projectid, rank FROM preferences WHERE userid = %s", (userid,))
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
  
  curs = conn.cursor()
  curs.execute("""SELECT groups.groupid, preferences.projectid, preferences.rank FROM groups
              JOIN users ON users.groupid = groups.groupid
              JOIN preferences ON preferences.userid = USERS.userid""")
  ret = []
  for rec in curs:
    ret.append(Group_pref_d(rec[0], rec[1], rec[2]))
  return ret
  
#--------
# Notifications

def create_notif(userid: int, timestamp: datetime, content: str) -> int:
  ''' Creates a notification for given user
  
  Parameters:
    userid (integer)
    timestamp (datetime.datetime), time of creation
    content (string)
    
  Returns:
    notificationid, id of notification just created
  '''
  curs = conn.cursor()
  curs.execute("INSERT INTO notifications (userid, created, isnew, content) VALUES (%s, %s, %s, %s) RETURNING notifid", (userid, timestamp, True, content))
  conn.commit()
  return curs.fetchone()[0]
  
def get_notifs(userid: int) -> typing.List[Notif_d_base]:
  ''' Returns all notifs for a given user
  
  Paremters:
    userid (integer)
    
  Returns:
    [tuple] (notifid, timestamp, content)
  '''
  curs = conn.cursor()
  curs.execute(""" WITH update AS 
              (UPDATE notifications SET isnew = %s WHERE userid = %s RETURNING notifid, created, content)
              SELECT * FROM update ORDER BY created DESC""", (False, userid))
  conn.commit()
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
  curs = conn.cursor()
  curs.execute("SELECT count(*) FROM notifications WHERE userid = %s AND isnew = %s", (userid, True))
  return curs.fetchone()[0]

def delete_notif(notifid: int):
  ''' Deletes the specified notification

  Parameters:
    notifid (integer)
  '''
  curs = conn.cursor()
  curs.execute("DELETE FROM notifications WHERE notifid = %s", (notifid,))
  conn.commit()
  
def delete_all_notifs(userid: int):
  ''' Deletes all notifs that a user has
  
  Paramters:
    userid (integer)
  '''
  curs = conn.cursor()
  curs.execute("DELETE FROM notifications WHERE userid = %s", (userid,))
  conn.commit()
  
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
  curs = conn.cursor()
  curs.execute("INSERT INTO channels (channelname) VALUES (%s) RETURNING channelid", (channelname,))
  conn.commit()
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
  curs = conn.cursor()
  curs.execute("""DELETE FROM channels WHERE channelid = %s""", (channelid,))
  # curs.execute("""DELETE FROM accesschannels WHERE channelid = %s;
  #              DELETE FROM messages WHERE channelid = %s;
  #              DELETE FROM channels WHERE channelid = %s""", (channelid, channelid, channelid))
  conn.commit()

def assign_channel_to_group(channelid: int, groupid: int):
  ''' Assigns a channel to a group
  
  Parameters:
    channelid (int)
    groupid (int)  
    
  Notes:
    automatically called in create_group
  '''
  curs = conn.cursor()
  curs.execute("UPDATE groups SET channel = %s WHERE groupid = %s", (channelid, groupid))
  conn.commit()

def assign_channel_to_project(channelid: int, projectid: int):
  ''' Assigns a channel to a project
  
  Parameters:
    channelid (int)
    projectid (int)
  
  Notes:
    automatically called in create_project
    Must also use add_user_to_channel(), will not automatically give group members access to channels
  '''
  curs = conn.cursor()
  curs.execute("UPDATE projects SET channel = %s WHERE projectid = %s", (channelid, projectid))
  conn.commit()

def add_user_to_channel(userid: int, channelid: int):
  ''' Gives specified user access to specified channel
  
  Parameters:
    userid (int)
    channelid (int)
    
  Notes:
    automatically called in add_user_to_group, create_project and create_group (for project and group owners)
  '''
  curs = conn.cursor()
  curs.execute("INSERT INTO accesschannels (userid, channelid) VALUES (%s, %s)", (userid, channelid))
  conn.commit()

def add_users_to_channel(userids: typing.List[int], channelid: int):
  ''' adds multiple users to a given channel
      slightly faster than performing multiple calls to add_user_to_channel
      
  Paramters:
    - userids ([int])
    - channelid (int)
  '''
  vals = [(x, channelid) for x in userids]
  curs = conn.cursor()
  psycopg2.extras.execute_values(curs, "INSERT INTO accesschannels (userid, channelid) VALUES %s", vals)
  conn.commit()

def remove_user_from_channel(userid:int, channelid: int):
  ''' Removes a specified user's access to a specified channel
  
  Parameters:
    userid (int)
    channelid (int)
    
  Notes:
    users are removed automatically in remove_user_from_group
  '''
  curs = conn.cursor()
  curs.execute("DELETE FROM accesschannels WHERE userid = %s AND channelid = %s", (userid, channelid))
  conn.commit()

def remove_users_from_channel(userids: typing.List[int], channelid: int):
  ''' Removes multiple users from a channel 
      should be faster than running multiple remove user
      
  Paramters:
    userids ([int])
    channelid (int)
  '''
  curs = conn.cursor()
  curs.execute("DELETE FROM accesschannels WHERE userid IN %s AND channelid = %s", (tuple(userids), channelid))
  conn.commit()
  
#retrieval
def get_users_channels(userid: int) -> typing.List[Channel_d_base]:
  ''' Gets all channels a user has access to
  
  Parameters:
    userid (int)
    
  Returns:
    [tuple] (channelid, channel_name)
  '''
  curs = conn.cursor()
  curs.execute("""SELECT channels.channelid, channels.channelname FROM users
               JOIN accesschannels ON accesschannels.userid = users.userid
               JOIN channels ON channels.channelid = accesschannels.channelid
               WHERE users.userid = %s""", (userid,))
  ret = []
  for rec in curs:
    ret.append(Channel_d_base(rec[0], rec[1]))
  return ret

def get_all_channels() -> typing.List[Channel_d_base]:
  ''' Returns all channels that currently exist
  
  Returns:
    [tuple] (channelid, channel_name)
  '''
  curs = conn.cursor()
  curs.execute("SELECT channelid, channelname FROM channels")
  ret = []
  for rec in curs:
    ret.append(rec[0], rec[1])
  return ret

def get_channel_members(channelid: int) -> typing.List[User_d_base]:
  ''' Gets all members that have access to specified channel
  
  Parameters:
    channelid (int)
    
  Returns
    [tuple] (userid, first_name, last_name)
  '''
  curs = conn.cursor()
  curs.execute("""SELECT users.userid, users.firstName, users.lastName FROM channels
              JOIN accesschannels ON accesschannels.channelid = channels.channelid
              JOIN users ON users.userid = accesschannels.userid
              WHERE channels.channelid = %s""", (channelid,))
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
  curs = conn.cursor()
  curs.execute("INSERT INTO messages (channelid, ownerid, content) VALUES (%s, %s, %s) RETURNING messageid", (channelid, ownerid, content))
  conn.commit()
  return curs.fetchone()[0]

def edit_message(messageid: int, content: str):
  ''' Edits the content of a specified message
  
  Parameters:
    messageid (int)
    content (string)
  '''
  curs = conn.cursor()
  curs.execute("UPDATE messages SET content = %s WHERE messageid = %s", (content, messageid))
  conn.commit()

def delete_message(messageid: int):
  ''' Deletes a specified message
  
  Parameters:
    messageid (int)
  '''
  curs = conn.cursor()
  curs.execute("DELETE FROM messages WHERE messageid = %s", (messageid,))
  conn.commit()

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
  curs = conn.cursor()
  if last_message == None: 
    curs.execute("SELECT MAX(messageid) FROM messages")
    last_message = curs.fetchone()[0]
    if last_message == None:
      #there are no messages
      return []
    else:
      last_message += 1
  print("PAGESTART = " + str(last_message))
  curs.execute("""SELECT messageid, ownerid, created, content FROM messages 
               WHERE channelid = %s 
               AND messageid < %s
               ORDER BY messageid desc
               LIMIT 50""", (channelid, last_message))
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
  '''
  curs = conn.cursor()
  curs.execute("""SELECT messageid, ownerid, created, content FROM messages 
               WHERE channelid = %s 
               ORDER BY created DESC
               LIMIT 1""", (channelid,))
  rec = curs.fetchone()
  return Message_d_base(rec[0], rec[1], rec[2], rec[3])
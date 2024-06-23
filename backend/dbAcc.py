import psycopg2

# TODO: swap to using connection pool
try: 
  conn = psycopg2.connect(dbname='projdb', user='postgres', password='postgres', host="postgres")
except: 
  print("Unable to connect to database.")
  exit()

#--------------------------------
#   Users
# Manipulation
def create_user(email, password, first_name, last_name, role):
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
  return curs.fetchone()[0]

# def update_role(userid, role):
#   ''' Modifies the role of a user
#   Parameters:
#     - userid, id of user to issue change
#     - role (integer), new role
#   '''
#   curs = conn.curs()
#   curs.execute("UPDATE users SET role = %s WHERE userid = %s", role, userid)
  
# Retrieval
def get_user_by_id(userid):
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
  return curs.fetchone()
  
def get_user_by_email(email):
  ''' Queries the database for user information
  Parameters:
    - email (string)
  Returns:
    - tuple (userid, email, first_name, last_name, password, role, groupid)
    - None, if user does not exist
  '''
  curs = conn.cursor()
  curs.execute("SELECT * FROM users WHERE email = %s", (email,))
  return curs.fetchone()  

#--------------------------------
#   Groups
# Manipulation
def create_group(ownerid, group_name):
  ''' Creates a new group, sets its owner, and adds its owner to the group
  Parameters:
    - ownerid (integer), user id of owner/creator
    - group_name (string)
  Returns:
    - groupid (integer)
  '''
  curs = conn.cursor()
  curs.execute("INSERT INTO groups (groupowner, groupname) VALUES (%s, %s) RETURNING groupid", (ownerid, group_name))
  new_group_id = curs.fetchone()[0]
  add_user_to_group(ownerid, new_group_id)
  return new_group_id
  
def add_user_to_group(to_add, group_id):
  ''' Adds user to specified group
  Parameters
    - to_add (integer), user id of person to add
    - group_id (integer)
  '''
  curs = conn.cursor()
  curs.execute("UPDATE users SET groupid = %s WHERE userid = %s", (group_id, to_add))

# Retrieval
def get_all_groups():
  ''' Queries databse for details on every group
  Returns:
    - [(groupid, groupname, member_count)] 
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

def get_group_by_id(groupid):
  ''' Queries the database for information on a particular group
  Parameters:
    - groupid (integer)
  returns:
    - tuple (groupid, ownerid, group name)
  '''
  curs = conn.cursor()
  curs.execute("SELECT * FROM groups WHERE groupid=%s", (groupid,))
  q_ret = curs.fetchone()
  return (q_ret[0], q_ret[1], q_ret[2])

def get_groupcount_by_name(groupname):
  ''' Queries the databse for the number of groups with a given name
  Parameters:
   - groupname (string)
  Returns:
    - int, number of groups sharing the given name
  '''
  curs = conn.cursor()
  curs.execute("SELECT count(*) FROM groups WHERE groupname = %s", (groupname,))
  return curs.fetchone()[0]
  
def get_group_members(groupid):
  ''' Get details for all members of a given group
  Parameters:
    - groupid (integer)
  returns:
    - [tuple] (userid, first name, last name) 
    - None if group does not exist
  '''
  curs = conn.cursor()
  curs.execute("SELECT * FROM users WHERE groupid = %s", (groupid,))
  ret_list = []
  for rec in curs:
    ret_list.append((rec[0], rec[2], rec[3]))
  return ret_list






#--------------------------------
#   Project
# Manipulation
def create_project(name, owner_id, channel_id, group_id, spec, description, 
                   requirement, required_knowledge, outcome, additional):
  ''' Creates a project in the databse
  Parameters:

  Returns:
    - integer, the project id
  '''
  curs = conn.cursor()
  curs.execute("INSERT INTO projects (ownerid, channel, groupno, spec, description, req, reqKnowledge, outcomes, additional) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING projectid", (owner_id, channel_id, group_id, spec, description, requirement, required_knowledge, outcome, additional))
  #curs.execute("INSERT INTO projects (projectname, ownerid, channel, groupno, spec, description, req, reqKnowledge, outcomes, additional) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING projectid", (name, owner_id, channel_id, group_id, spec, description, requirement, required_knowledge, outcome, additional))
  return curs.fetchone()[0]



def get_project_by_id(project_id):
  ''' Queries the database for project information
  Parameters:
    - projectid (integer)
  Returns:
    - tuple (project_id, owner_id, channel_id, group_id, spec, description, 
             requirement, required_knowledge, outcome, additional)
    - None, if user does not exist
  Notes:
    Does no checking, ensure you do not create two users with the same email address
  '''
  curs = conn.cursor()
  curs.execute("SELECT * FROM projects WHERE projectid = %s", (project_id,))
  return curs.fetchone()


def get_all_projects():
  ''' Queries the database for project information
  Parameters:
    - projectid (integer)
  Returns:
    - tuple (project_id, owner_id, channel_id, group_id, spec, description, 
             requirement, required_knowledge, outcome, additional)
    - None, if user does not exist
  Notes:
    Does no checking, ensure you do not create two users with the same email address
  '''
  curs = conn.cursor()
  curs.execute("SELECT * FROM projects")
  return curs.fetchall()


def update_project(project_id, owner_id, channel_id, group_id, spec, description, 
                   requirement, required_knowledge, outcome, additional):
  ''' updates the project in the databse 
  Parameters:


  '''
  curs = conn.cursor()
  #this only update group_id
  curs.execute("UPDATE project SET groupid = %s WHERE projectid = %s", (group_id, project_id))
  

def delete_project_by_id(project_id):
  ''' Queries the database for project information
  Parameters:
    - projectid (integer)

  Notes:
    Does no checking
  '''
  pass



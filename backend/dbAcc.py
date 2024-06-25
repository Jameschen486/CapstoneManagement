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
  conn.commit()
  return curs.fetchone()[0]

def update_password(userid, password):
  ''' Updates a users password with given value
  Parameters:
    - userid (integer), id of user to change
    - password (string), new password
  '''
  curs = conn.curs()
  curs.execute("UPDATE users SET password = %s WHERE userid = %s", (password, userid))
  conn.commit()

def update_role(userid, role):
  ''' Modifies the role of a user
  Parameters:
    - userid, id of user to issue change
    - role (integer), new role
  '''
  curs = conn.curs()
  curs.execute("UPDATE users SET role = %s WHERE userid = %s", role, userid)
  conn.commit()
  
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
  curs.execute("INSERT INTO groups (ownerid, groupname) VALUES (%s, %s) RETURNING groupid", (ownerid, group_name))
  conn.commit()
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
  
def remove_user_from_group(userid):
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

#----------------------------------
# Join requests
# Manipulation
def create_join_request(userid, groupid):
  ''' Creates a requests for userid to join groupid
  Parameters:
    - userid (integer), user making the request
    - groupid (integer), group being requested to join
  '''
  curs = conn.cursor()
  curs.execute("INSERT INTO grouprequests (userid, groupid) VALUES (%s, %s)", (userid, groupid))
  conn.commit()
  
def remove_all_join_requests(userid):
  ''' Removes all group join requests that a user has made
  Parameters:
    - userid (integer), user whose requests should be removed
  Notes:
    For use when a users request is approved, we should delete all others
  '''
  curs = conn.cursor()
  curs.execute("DELETE FROM grouprequests WHERE userid = %s", (userid,))
  conn.commit()
  
def remove_join_request(userid, groupid):
  ''' Removes a single join request for a group from a user
  Parameters:
    - userid (integer), userid of who made the request
    - groupid (integer), groupid of specific request
  '''
  curs = conn.cursor()
  curs.execute("DELETE FROM grouprequests WHERE userid = %s AND groupid = %s", (userid, groupid))
  conn.commit()
  
# Retrieval
def get_join_requests(userid):
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
    ret_list.append(rec)
  return ret_list
  
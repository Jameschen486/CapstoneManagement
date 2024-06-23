import dbAcc

def clear_users():
  curs = dbAcc.conn.cursor()
  curs.execute("TRUNCATE users RESTART IDENTITY CASCADE")
  dbAcc.conn.commit()
  
def clear_groups():
  curs = dbAcc.conn.cursor()
  curs.execute("TRUNCATE groups RESTART IDENTITY CASCADE")
  dbAcc.conn.commit()
  
def test_user_create_retrieve():
  user_deets = ("Email@provider.com", "password", "me", "them", 1)
  id = dbAcc.create_user(user_deets[0], user_deets[1], user_deets[2], user_deets[3], user_deets[4])
  given = dbAcc.get_user_by_id(id)
  #(id, email, firstname, lastname, password, role, groupid)
  expected = (id, user_deets[0],  user_deets[2], user_deets[3], user_deets[1], user_deets[4], None)
  assert given == expected
  given2 = dbAcc.get_user_by_id(200)
  assert given2 == None
  clear_users()
  assert dbAcc.get_user_by_id(id) == None

def test_user_retrieve_email():
  user_deets = ("Email1@provider.com", "password", "me", "them", 1)
  id = dbAcc.create_user(user_deets[0], user_deets[1], user_deets[2], user_deets[3], user_deets[4])
  given = dbAcc.get_user_by_email(user_deets[0])
  expected = expected = (id, user_deets[0],  user_deets[2], user_deets[3], user_deets[1], user_deets[4], None)
  assert expected == given
  given2 = dbAcc.get_user_by_email("fake@notreal.com")
  assert given2 == None
  clear_users()


    
own_d = ["group@owner.com", "group", "owner", "password", 1]
use_d = ["Email@provider.com", "me", "them", "password", 1]
groupid = 0
def test_group_setup():
  own_id = dbAcc.create_user(own_d[0], own_d[3], own_d[1], 
                            own_d[2], own_d[4])
  own_d.insert(0, own_id)
  use_id = dbAcc.create_user(use_d[0], use_d[3], use_d[1], 
                            use_d[2], use_d[4])
  use_d.insert(0, use_id)

def test_group_create_retrieve():
  groupname = "testgroup"
  global groupid
  groupid = dbAcc.create_group(own_d[0], groupname)
  group_d = dbAcc.get_group_details(groupid)
  assert group_d == (groupid, own_d[0], groupname)
  own_deets = dbAcc.get_user_by_id(own_d[0])
  assert own_deets[5] == groupid

def test_add_get_users():
  dbAcc.add_user_to_group(use_d[0], groupid)
  members = dbAcc.get_group_members(groupid)
  assert (use_d[0], use_d[2], use_d[3]) in members
  assert (own_d[0], own_d[2], own_d[3]) in members
  clear_users()
  clear_groups()
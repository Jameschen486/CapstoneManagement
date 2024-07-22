import dbAcc
import datetime
import random

def clear_users():
  curs = dbAcc.conn.cursor()
  curs.execute("TRUNCATE users RESTART IDENTITY CASCADE")
  dbAcc.conn.commit()
  
def clear_groups():
  curs = dbAcc.conn.cursor()
  curs.execute("TRUNCATE groups RESTART IDENTITY CASCADE")
  dbAcc.conn.commit()
  
def clear_grouprequests():
  curs = dbAcc.conn.cursor()
  curs.execute("TRUNCATE grouprequests CASCADE")
  dbAcc.conn.commit()
  
def clear_projects():
  curs = dbAcc.conn.cursor()
  curs.execute("TRUNCATE projects RESTART IDENTITY CASCADE")
  dbAcc.conn.commit()
  
def clear_skills():
  curs = dbAcc.conn.cursor()
  curs.execute("TRUNCATE skills RESTART IDENTITY CASCADE")
  dbAcc.conn.commit()
  
def clear_reset_codes():
  curs = dbAcc.conn.cursor()
  curs.execute("TRUNCATE resetcodes CASCADE")
  dbAcc.conn.commit()
  
def clear_preferences():
  curs = dbAcc.conn.cursor()
  curs.execute("TRUNCATE preferences CASCADE")
  dbAcc.conn.commit()
  
def clear_notifs():
  curs = dbAcc.conn.cursor()
  curs.execute("TRUNCATE notifications RESTART IDENTITY CASCADE")
  dbAcc.conn.commit()
  
def clear_channels():
  curs = dbAcc.conn.cursor()
  curs.execute("TRUNCATE accesschannels RESTART IDENTITY CASCADE")
  dbAcc.conn.commit()
  curs.execute("TRUNCATE channels RESTART IDENTITY CASCADE")
  dbAcc.conn.commit()
  
def clear_messages():
  curs = dbAcc.conn.cursor()
  curs.execute("TRUNCATE messages RESTART IDENTITY CASCADE")
  dbAcc.conn.commit()
  
own_d = [0, "group@owner.com", "group", "owner", "password", 1]
use_d = [0, "Email@provider.com", "me", "them", "password", 1]
def test_user_create_retrieve():
  own_d[0] = dbAcc.create_user(own_d[1], own_d[4], own_d[2], own_d[3], own_d[5])
  given = dbAcc.get_user_by_id(own_d[0])
  #(id, email, firstname, lastname, password, role, groupid)
  assert given == tuple(own_d + [None])
  given = dbAcc.get_user_by_id(200)
  assert given == None
  clear_users()
  assert dbAcc.get_user_by_id(own_d[0]) == None

def test_user_retrieve_email():
  user_deets = ("Email1@provider.com", "password", "me", "them", 1)
  id = dbAcc.create_user(user_deets[0], user_deets[1], user_deets[2], user_deets[3], user_deets[4])
  given = dbAcc.get_user_by_email(user_deets[0])
  expected = (id, user_deets[0],  user_deets[2], user_deets[3], user_deets[1], user_deets[4], None)
  assert expected == given
  given2 = dbAcc.get_user_by_email("fake@notreal.com")
  assert given2 == None
  clear_users()
  
def test_user_update_details():
  #tests: update_password, update_role
  use_d = [0, "Email1@provider.com", "me", "them", "password", 1]
  use_d[0] = dbAcc.create_user(use_d[1], use_d[4], use_d[2], use_d[3], use_d[5])
  
  new_password = "newpass"
  dbAcc.update_password(use_d[0], new_password)
  new_d = dbAcc.get_user_by_id(use_d[0])
  assert new_d[4] == new_password
  
  dbAcc.update_role(use_d[0], 2)
  new_d = dbAcc.get_user_by_id(use_d[0])
  assert new_d[5]
  clear_users()


groupid = 0
def test_group_setup():
  own_d[0] = dbAcc.create_user(own_d[1], own_d[4], own_d[2], 
                            own_d[3], own_d[5])
  use_d[0] = dbAcc.create_user(use_d[1], use_d[4], use_d[2], 
                            use_d[3], use_d[5])

def test_group_create_retrieve():
  groupname = "testgroup"
  global groupid
  groupid = dbAcc.create_group(own_d[0], groupname)
  group_d = dbAcc.get_group_by_id(groupid)
  assert group_d == (groupid, own_d[0], groupname, None, None)
  
  dbAcc.add_user_to_group(use_d[0], groupid)
  dbAcc.update_group_owner(use_d[0], groupid)
  group_d = dbAcc.get_group_by_id(groupid)
  assert group_d == (groupid, use_d[0], groupname, None, None)
  
  own_deets = dbAcc.get_user_by_id(own_d[0])
  assert own_deets[6] == groupid
  count = dbAcc.get_groupcount_by_name(groupname)
  assert count == 1

def test_add_get_remove_users():
  dbAcc.add_user_to_group(use_d[0], groupid)
  members = dbAcc.get_group_members(groupid)
  assert (use_d[0], use_d[2], use_d[3]) in members
  assert (own_d[0], own_d[2], own_d[3]) in members
  
  dbAcc.remove_user_from_group(own_d[0])
  members = dbAcc.get_group_members(groupid)
  assert (own_d[0], own_d[2], own_d[3]) not in members

  given = dbAcc.get_all_groups()
  assert (groupid, "testgroup", 1) in given
  newgroupid = dbAcc.create_group(own_d[0], "newgroup")
  given = dbAcc.get_all_groups()
  assert (groupid, "testgroup", 1) in given
  assert (newgroupid, "newgroup", 1) in given
  clear_users()
  clear_groups()
  
  
grp_d = [0, "groupname", 0]
def test_join_requests():
  use_d2 = [0, "Email@provider.com", "us", "now", "password", 1]
  own_d[0] = dbAcc.create_user(own_d[1], own_d[4], own_d[2], 
                              own_d[3], own_d[5])
  use_d[0] = dbAcc.create_user(use_d[1], use_d[4], use_d[2], 
                              use_d[3], use_d[5])
  use_d2[0] = dbAcc.create_user(use_d2[1], use_d2[4], use_d2[2], 
                                use_d2[3], use_d2[5])
  grp_d[0] = dbAcc.create_group(own_d[0], grp_d[1])
  grp_d[2] += 1
  
  dbAcc.create_join_request(use_d[0], grp_d[0])
  dbAcc.create_join_request(use_d2[0], grp_d[0])
  retlist = dbAcc.get_join_requests(own_d[0])
  assert (use_d[0], use_d[2], use_d[3]) in retlist
  assert (use_d2[0], use_d2[2], use_d2[3]) in retlist
  
  dbAcc.remove_join_request(use_d[0], grp_d[0])
  retlist = dbAcc.get_join_requests(own_d[0])
  assert (use_d[0], use_d[2], use_d[3]) not in retlist
  assert (use_d2[0], use_d2[2], use_d2[3]) in retlist

  dbAcc.remove_all_join_requests(use_d2[0])
  retlist = dbAcc.get_join_requests(own_d[0])
  assert retlist == []
  clear_users()
  clear_groups()
  clear_grouprequests()
  
own_d = [0, "group@owner.com", "group", "owner", "password", 1]
def test_projects():
  own_d[0] = dbAcc.create_user(own_d[1], own_d[4], own_d[2], own_d[3], own_d[5])
  pd = [0, own_d[0], "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", None]
  pd[0] = dbAcc.create_project(own_d[0], pd[2], pd[3], pd[4], pd[5], pd[6], pd[7], pd[8], pd[9], pd[10], pd[11])
  ret = dbAcc.get_all_projects()
  pdt = tuple(pd)
  assert pdt in ret
  ret = dbAcc.get_project_by_id(pd[0])
  assert ret == pdt
  new_title = "new"
  dbAcc.update_project(pd[0], own_d[0], new_title, pd[3], pd[4], pd[5], pd[6], pd[7], pd[8], pd[9], pd[10], pd[11])
  ret = dbAcc.get_project_by_id(pd[0])
  assert ret.title == new_title
  dbAcc.delete_project_by_id(pd[0])
  ret = dbAcc.get_project_by_id(pd[0])
  assert ret == None
  ret = dbAcc.get_all_projects()
  assert ret == []
  clear_users()
  clear_groups()
  clear_grouprequests()
  
def test_skills():
  skl_d1 = [0, "python"]
  skl_d2 = [0, "c++"]
  skl_d1[0] = dbAcc.create_skill(skl_d1[1])
  skl_d2[0] = dbAcc.create_skill(skl_d2[1])
  given = dbAcc.get_all_skills()
  assert tuple(skl_d1) in given
  assert tuple(skl_d2) in given
  
  own_d[0] = dbAcc.create_user(own_d[1], own_d[4], own_d[2], own_d[3], own_d[5])
  use_d[0] = dbAcc.create_user(use_d[1], use_d[4], use_d[2], use_d[3], use_d[5])
  dbAcc.add_skill_to_user(skl_d1[0], own_d[0])
  dbAcc.add_skill_to_user(skl_d2[0], use_d[0])
  given = dbAcc.get_user_skills(own_d[0])
  assert skl_d1[0]in given
  given = dbAcc.get_user_skills(use_d[0])
  assert skl_d2[0] in given
  
  dbAcc.add_skill_to_user(skl_d2[0], own_d[0])
  grp_id = dbAcc.create_group(own_d[0], "testgroup")
  dbAcc.add_user_to_group(use_d[0], grp_id)
  given = dbAcc.get_group_skills(grp_id)
  assert (skl_d1[0], 1) in given
  assert (skl_d2[0], 2) in given
  
  dbAcc.remove_skill_from_user(skl_d1[0], own_d[0])
  given = dbAcc.get_user_skills(own_d[0])
  assert skl_d1[0] not in given
  
  proj_id = dbAcc.create_project("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "10")
  dbAcc.add_skill_to_project(skl_d1[0], proj_id)
  given = dbAcc.get_project_skills(proj_id)
  assert given == [tuple(skl_d1)]
  clear_users()
  clear_projects()
  clear_groups()
  clear_skills()
  
def test_reset_codes():
  use_d[0] = dbAcc.create_user(use_d[1], use_d[4], use_d[2], use_d[3], use_d[5])
  code1 = [use_d[0], "resetcode", datetime.datetime.now()]
  dbAcc.create_reset_code(code1[0], code1[1], code1[2])
  given = dbAcc.get_reset_code(use_d[0])
  assert given == tuple(code1)
  
  code2 = [use_d[0], "newcode", datetime.datetime.now()]
  dbAcc.create_reset_code(code2[0], code2[1], code2[2])
  given = dbAcc.get_reset_code(use_d[0])
  assert given == tuple(code2)
  
  dbAcc.remove_reset_code(use_d[0])
  given = dbAcc.get_reset_code(use_d[0])
  assert given == None
  clear_users()
  clear_reset_codes()

use_d0 = [0, "Email@provider.com", "me", "them", "password", 1]
use_d1 = [0, "Email@provider.com", "me", "them", "password", 1]
use_d2 = [0, "Email@provider.com", "me", "them", "password", 1]
use_d3 = [0, "Email@provider.com", "me", "them", "password", 1]
use_d4 = [0, "Email@provider.com", "me", "them", "password", 1]
def test_preferences():
  use_d0[0] = dbAcc.create_user(use_d0[1], use_d0[4], use_d0[2], use_d0[3], use_d0[5])
  use_d1[0] = dbAcc.create_user(use_d1[1], use_d1[4], use_d1[2], use_d1[3], use_d1[5])
  use_d2[0] = dbAcc.create_user(use_d2[1], use_d2[4], use_d2[2], use_d2[3], use_d2[5])
  use_d3[0] = dbAcc.create_user(use_d3[1], use_d3[4], use_d3[2], use_d3[3], use_d3[5])
  use_d4[0] = dbAcc.create_user(use_d4[1], use_d4[4], use_d4[2], use_d4[3], use_d4[5])
  
  prefs0 = [1, 2, 3, 4, 5]
  prefs1 = [2, 3, 4, 5, 1]
  prefs2 = [3, 4, 5, 1, 2]
  prefs3 = [4, 5, 1, 2, 3]
  prefs4 = [5, 1, 2, 3, 4]
  ranks = [1, 2, 3, 4, 5]
  
  own_d[0] = dbAcc.create_user(own_d[1], own_d[4], own_d[2], own_d[3], own_d[5])
  pd = [0, own_d[0], "a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
  pids = []
  pids.append(dbAcc.create_project(own_d[0], pd[2], pd[3], pd[4], pd[5], pd[6], pd[7], pd[8], pd[9], pd[10], pd[11]))
  pids.append(dbAcc.create_project(own_d[0], pd[2], pd[3], pd[4], pd[5], pd[6], pd[7], pd[8], pd[9], pd[10], pd[11]))
  pids.append(dbAcc.create_project(own_d[0], pd[2], pd[3], pd[4], pd[5], pd[6], pd[7], pd[8], pd[9], pd[10], pd[11]))
  pids.append(dbAcc.create_project(own_d[0], pd[2], pd[3], pd[4], pd[5], pd[6], pd[7], pd[8], pd[9], pd[10], pd[11]))
  pids.append(dbAcc.create_project(own_d[0], pd[2], pd[3], pd[4], pd[5], pd[6], pd[7], pd[8], pd[9], pd[10], pd[11]))
  
  dbAcc.create_preferences(use_d0[0], prefs0, ranks)
  dbAcc.create_preferences(use_d1[0], prefs1, ranks)
  dbAcc.create_preferences(use_d2[0], prefs2, ranks)
  dbAcc.create_preferences(use_d3[0], prefs3, ranks)
  dbAcc.create_preferences(use_d4[0], prefs4, ranks)
  
  given = dbAcc.get_user_preferences(use_d0[0])
  assert (prefs0[0], ranks[0]) in given
  assert (prefs0[1], ranks[1]) in given
  assert (prefs0[2], ranks[2]) in given
  assert (prefs0[3], ranks[3]) in given
  assert (prefs0[4], ranks[4]) in given
  
  grp_d = [0, "group"]
  grp_d[0] = dbAcc.create_group(use_d0[0], grp_d[1])
  dbAcc.add_user_to_group(use_d1[0], grp_d[0])
  dbAcc.add_user_to_group(use_d2[0], grp_d[0])
  dbAcc.add_user_to_group(use_d3[0], grp_d[0])
  dbAcc.add_user_to_group(use_d4[0], grp_d[0])
  
  skill_combs = []
  for i in range (1, 5):
    for j in range(1, 5):
      skill_combs.append((grp_d[0], i, j))
  given = dbAcc.get_all_preferences()
  for comb in skill_combs:
    assert comb in given
    
  dbAcc.delete_preferences(use_d0[0])
  given = dbAcc.get_user_preferences(use_d0[0])
  assert given == []
  
  clear_users()
  clear_groups()
  clear_projects()
  clear_preferences()
  
def test_get_alls(): 
  use_d0[0] = dbAcc.create_user(use_d0[1], use_d0[4], use_d0[2], use_d0[3], use_d0[5])
  use_d1[0] = dbAcc.create_user(use_d1[1], use_d1[4], use_d1[2], use_d1[3], use_d1[5])
  use_d2[0] = dbAcc.create_user(use_d2[1], use_d2[4], use_d2[2], use_d2[3], use_d2[5])
  use_d3[0] = dbAcc.create_user(use_d3[1], use_d3[4], use_d3[2], use_d3[3], use_d3[5])
  use_d4[0] = dbAcc.create_user(use_d4[1], use_d4[4], use_d4[2], use_d4[3], use_d4[5])
  
  grp_d = [0, "group"]
  grp_d[0] = dbAcc.create_group(use_d0[0], grp_d[1])
  dbAcc.add_user_to_group(use_d1[0], grp_d[0])
  dbAcc.add_user_to_group(use_d2[0], grp_d[0])
  dbAcc.add_user_to_group(use_d3[0], grp_d[0])
  dbAcc.add_user_to_group(use_d4[0], grp_d[0])
  
  skl_d0 = [0, "python"]
  skl_d1 = [0, "c++"]
  skl_d2 = [0, "javascript"]
  skl_d3 = [0, "c"]
  skl_d4 = [0, "c#"]
  skl_d5 = [0, "sql"]

  skl_d0[0] = dbAcc.create_skill(skl_d0[1])
  skl_d1[0] = dbAcc.create_skill(skl_d1[1])
  skl_d2[0] = dbAcc.create_skill(skl_d2[1])
  skl_d3[0] = dbAcc.create_skill(skl_d3[1])
  skl_d4[0] = dbAcc.create_skill(skl_d4[1])
  skl_d5[0] = dbAcc.create_skill(skl_d5[1])

  #two of each skill, only one for skl_d0 and skl_d1
  dbAcc.add_skill_to_user(skl_d0[0], use_d0[0])
  dbAcc.add_skill_to_user(skl_d1[0], use_d0[0])
  dbAcc.add_skill_to_user(skl_d1[0], use_d1[0])
  dbAcc.add_skill_to_user(skl_d2[0], use_d1[0])
  dbAcc.add_skill_to_user(skl_d2[0], use_d2[0])
  dbAcc.add_skill_to_user(skl_d3[0], use_d2[0])
  dbAcc.add_skill_to_user(skl_d3[0], use_d3[0])
  dbAcc.add_skill_to_user(skl_d4[0], use_d3[0])
  dbAcc.add_skill_to_user(skl_d4[0], use_d4[0])
  dbAcc.add_skill_to_user(skl_d5[0], use_d4[0])
  
  given = dbAcc.get_all_groups_skills()
  assert (grp_d[0], skl_d0[0], 1) in given
  assert (grp_d[0], skl_d1[0], 2) in given
  assert (grp_d[0], skl_d2[0], 2) in given
  assert (grp_d[0], skl_d3[0], 2) in given
  assert (grp_d[0], skl_d4[0], 2) in given
  assert (grp_d[0], skl_d5[0], 1) in given
  
  own_d[0] = dbAcc.create_user(own_d[1], own_d[4], own_d[2], own_d[3], own_d[5])
  pd = [0, own_d[0], "a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
  pids = []
  pids.append(dbAcc.create_project(own_d[0], pd[2], pd[3], pd[4], pd[5], pd[6], pd[7], pd[8], pd[9], pd[10], pd[11]))
  pids.append(dbAcc.create_project(own_d[0], pd[2], pd[3], pd[4], pd[5], pd[6], pd[7], pd[8], pd[9], pd[10], pd[11]))
  pids.append(dbAcc.create_project(own_d[0], pd[2], pd[3], pd[4], pd[5], pd[6], pd[7], pd[8], pd[9], pd[10], pd[11]))
  pids.append(dbAcc.create_project(own_d[0], pd[2], pd[3], pd[4], pd[5], pd[6], pd[7], pd[8], pd[9], pd[10], pd[11]))
  pids.append(dbAcc.create_project(own_d[0], pd[2], pd[3], pd[4], pd[5], pd[6], pd[7], pd[8], pd[9], pd[10], pd[11]))
  
  #two of each skill, only one for skl_d0 and skl_d1
  dbAcc.add_skill_to_project(skl_d0[0], pids[0])
  dbAcc.add_skill_to_project(skl_d1[0], pids[0])
  dbAcc.add_skill_to_project(skl_d1[0], pids[1])
  dbAcc.add_skill_to_project(skl_d2[0], pids[1])
  dbAcc.add_skill_to_project(skl_d2[0], pids[2])
  dbAcc.add_skill_to_project(skl_d3[0], pids[2])
  dbAcc.add_skill_to_project(skl_d3[0], pids[3])
  dbAcc.add_skill_to_project(skl_d4[0], pids[3])
  dbAcc.add_skill_to_project(skl_d4[0], pids[4])
  dbAcc.add_skill_to_project(skl_d5[0], pids[4])
  
  given = dbAcc.get_all_project_skills()
  assert (pids[0], 0, skl_d0[0]) in given
  assert (pids[0], 0, skl_d1[0]) in given
  assert (pids[1], 0, skl_d1[0]) in given
  assert (pids[1], 0, skl_d2[0]) in given
  assert (pids[2], 0, skl_d2[0]) in given
  assert (pids[2], 0, skl_d3[0]) in given
  assert (pids[3], 0, skl_d3[0]) in given
  assert (pids[3], 0, skl_d4[0]) in given
  assert (pids[4], 0, skl_d4[0]) in given
  assert (pids[4], 0, skl_d5[0]) in given

  clear_users()
  clear_groups()
  clear_projects()
  clear_skills()
  
def test_notifications():
  use_d0[0] = dbAcc.create_user(use_d0[1], use_d0[4], use_d0[2], use_d0[3], use_d0[5])
  notif_d0 = [0, datetime.datetime.now(), "notification0"]
  notif_d1 = [0, datetime.datetime.now(), "notification1"]
  
  notif_d0[0] = dbAcc.create_notif(use_d0[0], notif_d0[1], notif_d0[2])
  notif_d1[0] = dbAcc.create_notif(use_d0[0], notif_d1[1], notif_d1[2])
  
  given = dbAcc.get_new_notifs(use_d0[0])
  assert given == 2
  
  given = dbAcc.get_notifs(use_d0[0])
  assert tuple(notif_d0) in given
  assert tuple(notif_d1) in given
  
  given = dbAcc.get_new_notifs(use_d0[0])
  assert given == 0
  
  dbAcc.delete_notif(notif_d1[0])
  given = dbAcc.get_notifs(use_d0[0])
  assert tuple(notif_d0) in given
  assert tuple(notif_d1) not in given
  
  notif_d1[0] = dbAcc.create_notif(use_d0[0], notif_d1[1], notif_d1[2])
  given = dbAcc.get_new_notifs(use_d0[0])
  assert given == 1
  dbAcc.delete_all_notifs(use_d0[0])
  given = dbAcc.get_notifs(use_d0[0])
  assert given == []
  
  clear_users()
  clear_notifs()
  
def test_channels():
  #create 1 user two channels, add user to both
  use_d0[0] = dbAcc.create_user(use_d0[1], use_d0[4], use_d0[2], use_d0[3], use_d0[5])
  ch_d0 = [0, "channel0"]
  ch_d0[0] = dbAcc.create_channel(ch_d0[1])
  ch_d1 = [0, "channel1"]
  ch_d1[0] = dbAcc.create_channel(ch_d1[1])
  dbAcc.add_user_to_channel(use_d0[0], ch_d0[0])
  dbAcc.add_user_to_channel(use_d0[0], ch_d1[0])
  given = dbAcc.get_users_channels(use_d0[0])
  assert tuple(ch_d0) in given
  assert tuple(ch_d1) in given
  #create new user, add to one channel
  use_d1[0] = dbAcc.create_user(use_d1[1], use_d1[4], use_d1[2], use_d1[3], use_d1[5])
  dbAcc.add_user_to_channel(use_d1[0], ch_d0[0])
  given = dbAcc.get_channel_members(ch_d0[0])
  assert (use_d0[0], use_d0[2], use_d0[3]) in given
  assert (use_d1[0], use_d1[2], use_d1[3]) in given
  given = dbAcc.get_channel_members(ch_d1[0])
  assert (use_d0[0], use_d0[2], use_d0[3]) in given
  assert (use_d1[0], use_d1[2], use_d1[3]) not in given
  #remove second user from channel
  dbAcc.remove_user_from_channel(use_d1[0], ch_d0[0])
  given = dbAcc.get_users_channels(use_d1[0])
  assert tuple(ch_d0) not in given
  assert tuple(ch_d1) not in given
  given = dbAcc.get_channel_members(ch_d0[0])
  assert (use_d0[0], use_d0[2], use_d0[3]) in given
  assert (use_d1[0], use_d1[2], use_d1[3]) not in given
  #create group, assign channel to group
  grp_d = [0, "group"]
  grp_d[0] = dbAcc.create_group(use_d0[0], grp_d[1])
  dbAcc.assign_channel_to_group(ch_d0[0], grp_d[0])
  given = dbAcc.get_group_by_id(grp_d[0])
  assert given.channel == ch_d0[0]
  #create project, assign channel to project
  own_d[0] = dbAcc.create_user(own_d[1], own_d[4], own_d[2], own_d[3], own_d[5])
  pd = [0, own_d[0], "a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
  pd[0] = dbAcc.create_project(own_d[0], pd[2], pd[3], pd[4], pd[5], pd[6], pd[7], pd[8], pd[9], pd[10], pd[11])
  dbAcc.assign_channel_to_project(ch_d1[0], pd[0])
  given = dbAcc.get_project_by_id(pd[0])
  assert given.channel == ch_d1[0]
  #delete channel, check unassigned to users groups and projects
  dbAcc.delete_channel(ch_d0[0])
  given = dbAcc.get_users_channels(use_d0[0])
  assert tuple(ch_d0) not in given
  assert tuple(ch_d1) in given
  given = dbAcc.get_group_by_id(grp_d[0])
  assert given.channel == None
  dbAcc.delete_channel(ch_d1[0])
  given = dbAcc.get_project_by_id(pd[0])
  assert given.channel == None

  clear_users()
  clear_groups()
  clear_projects()
  clear_channels()
  
def test_messages():
  #create user, channel
  use_d0[0] = dbAcc.create_user(use_d0[1], use_d0[4], use_d0[2], use_d0[3], use_d0[5])
  ch_d0 = [0, "groupchannel0"]
  ch_d0[0] = dbAcc.create_channel(ch_d0[0])
  #create message, get message
  msg_d0 = [0, use_d0[0], datetime.datetime.now(), "a"]
  msg_d0[0] = dbAcc.create_message(ch_d0[0], msg_d0[1], msg_d0[2], msg_d0[3])
  given = dbAcc.get_channel_messages(ch_d0[0])
  assert tuple(msg_d0) in given
  given = dbAcc.get_latest_message(ch_d0[0])
  assert tuple(msg_d0) == given
  #edit message
  new_cont = "b"
  dbAcc.edit_message(msg_d0[0], new_cont)
  given = dbAcc.get_latest_message(ch_d0[0])
  assert given.content == new_cont
  #delete message
  dbAcc.delete_message(msg_d0[0])
  given = dbAcc.get_channel_messages(ch_d0[0])
  assert given == []
  #make more than a page of messages
  messages = []
  for i in range(1, 201):
    cur_msg = [0, use_d0[0], datetime.datetime.now(), str(i)]
    cur_msg[0] = dbAcc.create_message(ch_d0[0], cur_msg[1], cur_msg[2], cur_msg[3])
    messages.append(cur_msg)
  #get pages, length = 50
  page1 = [msg for msg in messages if int(msg[3]) > 150]
  page2 = [msg for msg in messages if int(msg[3]) > 100 and int(msg[3]) < 151]
  page3 = [msg for msg in messages if int(msg[3]) > 50 and int(msg[3]) < 101]
  page4 = [msg for msg in messages if int(msg[3]) > 0 and int(msg[3]) < 51]
  given = dbAcc.get_channel_messages(ch_d0[0])
  for msg in page1:
    assert tuple(msg) in given
  given = dbAcc.get_channel_messages(ch_d0[0], page1[0][2])
  for msg in page2:
    assert tuple(msg) in given
  given = dbAcc.get_channel_messages(ch_d0[0], page2[0][2])
  for msg in page3:
    assert tuple(msg) in given
  given = dbAcc.get_channel_messages(ch_d0[0], page3[0][2])
  for msg in page4:
    assert tuple(msg) in given
  
  clear_users()
  clear_channels()
import dbAcc

def test_user_create_retrieve():
  user_deets = ("Email@provider.com", "password", "me", "them", 1)
  id = dbAcc.create_user(user_deets[0], user_deets[1], user_deets[2], user_deets[3], user_deets[4])
  given = dbAcc.get_user_by_id(id)
  #(id, email, firstname, lastname, password, role, groupid)
  expected = (id, user_deets[0],  user_deets[2], user_deets[3], user_deets[1], user_deets[4], None)
  assert given == expected

def test_user_retrieve_email():
  user_deets = ("Email1@provider.com", "password", "me", "them", 1)
  id = dbAcc.create_user(user_deets[0], user_deets[1], user_deets[2], user_deets[3], user_deets[4])
  given = dbAcc.get_user_by_email(user_deets[0])
  expected = expected = (id, user_deets[0],  user_deets[2], user_deets[3], user_deets[1], user_deets[4], None)
  assert expected == given
  
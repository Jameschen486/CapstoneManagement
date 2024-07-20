import dbAcc
import authentication

def clear_users():
  curs = dbAcc.conn.cursor()
  curs.execute("TRUNCATE users RESTART IDENTITY CASCADE")
  dbAcc.conn.commit()

def test_updateUserRole0():
    user_d0 = [0, "admin@provider.com", "admin", "them", "adminPassword", 3]
    user_d1 = [1, "Email@provider.com", "me", "them", "password", 0]
    hashedPassword = authentication.getHashOf(user_d0[4])
    dbAcc.create_user(user_d0[1], hashedPassword, user_d0[2], user_d0[3], user_d0[5])
    dbAcc.create_user(user_d1[1], user_d1[4], user_d1[2], user_d1[3], user_d1[5])

    authentication.updateUserRole(user_d0[1], user_d0[4], user_d1[1], 1)
    user = dbAcc.get_user_by_email(user_d1[1])
    assert(user[5] == 1)
    clear_users()

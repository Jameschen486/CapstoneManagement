import authentication
import dbAcc

#reset request

#successful reset password request
def test_reset_req_1():
    use_d0 = [0, "Email1@provider.com", "me1", "them1", "password1", 1]

    dbAcc.create_user(use_d0[1], use_d0[4], use_d0[2], use_d0[3], use_d0[5])
    assert(dbAcc.get_reset_code(use_d0[0]) == None)

    authentication.auth_reset_request(use_d0[1])
    assert(dbAcc.get_reset_code(use_d0[0]) != None)

#invalid email provided
def test_reset_req_2():
    use_d0 = [0, "Email1@provider.com", "me1", "them1", "password1", 1]
    dbAcc.create_user(use_d0[1], use_d0[4], use_d0[2], use_d0[3], use_d0[5])
    given = authentication.auth_reset_request(123)
    assert(given == 400)


#Reset password

#successfully reset password
def test_reset_code1():
    use_d0 = [0, "Email1@provider.com", "me1", "them1", "password1", 1]
    user1 = dbAcc.create_user(use_d0[1], use_d0[4], use_d0[2], use_d0[3], use_d0[5])

    authentication.auth_reset_request(use_d0[1])
    resetCode = dbAcc.get_reset_code(use_d0[0])
    newPassword = "newPassword1"
    hashedPassword = getHashOf(newPassword)
    authentication.auth_password_reset(use_d0[1], resetCode, newPassword)

    assert(use_d0[5] == hashedPassword)
    assert(dbAcc.get_reset_code(use_d0[0]) == None)

#incorrect reset code provided should return 400
def test_reset_code2():
    use_d0 = [0, "Email1@provider.com", "me1", "them1", "password1", 1]
    user1 = dbAcc.create_user(use_d0[1], use_d0[4], use_d0[2], use_d0[3], use_d0[5])

    authentication.auth_reset_request(use_d0[1])
    resetCode = dbAcc.get_reset_code(use_d0[0])
    newPassword = "newPassword1"
    given = authentication.auth_password_reset(use_d0[1], resetCode + "1", newPassword)
    assert(given == 400)

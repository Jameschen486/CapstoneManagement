
TEST_PASSWORD = "123"
TEST_USERNAME = "JOHN"

def login(username, password) :
    """check if username and password match database then intialise a web tocken for the user

    Args:
        username (string): username
        password (string): password

    Returns:
        string: web_token
    """

    if username == TEST_USERNAME and password == TEST_PASSWORD:
        return 1
    return 0
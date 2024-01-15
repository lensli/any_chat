from .database import User_Db

def user_login(username,password):
    udb = User_Db()
    return udb.check_credentials(username,password)

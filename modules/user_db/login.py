from .database import DB
ob_path = "C:\\home\\get$\\"
def user_login(username,password):
    db = DB(ob_path)
    return db.check_credentials(username,password)
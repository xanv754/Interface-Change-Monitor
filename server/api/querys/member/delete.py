from utils.database import open_connection, close_connection
from constants.userStatus import userstatus
from pymongo.results import DeleteResult
from constants.collections import USER

def delete_user(username: str) -> DeleteResult:
    try:
        db = open_connection()
        collection = db.get_collection(USER)
        res = collection.delete_one({"username": username})
    except Exception as error:
        close_connection()
        raise error
    else:
        close_connection()
        return res
    
def delete_users_disabled() -> DeleteResult:
    try:
        db = open_connection()
        collection = db.get_collection(USER)
        res = collection.delete_many({"status": userstatus.disabled})
    except Exception as error:
        close_connection()
        raise error
    else:
        close_connection()
        return res
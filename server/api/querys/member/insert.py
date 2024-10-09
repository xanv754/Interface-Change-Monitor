from utils.database import open_connection, close_connection
from pymongo.results import InsertOneResult
from constants.collections import USER
from entity.admin import Admin
from entity.user import User

def insert_user(user: (Admin | User)) -> InsertOneResult:
    try:
        db = open_connection()
        collection = db.get_collection(USER)
        res = collection.insert_one(user.model_dump(exclude={'id'}))
    except Exception as error:
        close_connection()
        raise error
    else: 
        close_connection()
        return res
    
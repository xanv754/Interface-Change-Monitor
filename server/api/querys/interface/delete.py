from utils.database import open_connection, close_connection
from constants.collections import INTERFACE, BACKUP_INTERFACE
from pymongo.results import DeleteResult

def delete_interfaces() -> DeleteResult:
    try:
        db = open_connection()
        collection = db.get_collection(INTERFACE)
        res = collection.delete_many({})
    except Exception as error:
        close_connection()
        raise error
    else:
        close_connection()
        return res

# BACKUP 
def delete_backup() -> DeleteResult:
    try:
        db = open_connection()
        collection = db.get_collection(BACKUP_INTERFACE)
        res = collection.delete_many({})
    except Exception as error:
        close_connection()
        raise error
    else:
        close_connection()
        return res
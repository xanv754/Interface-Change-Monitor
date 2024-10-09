from utils.database import open_connection, close_connection
from constants.collections import ELEMENT
from pymongo.results import DeleteResult

def delete_elements() -> DeleteResult:
    try:
        db = open_connection()
        collection = db.get_collection(ELEMENT)
        res = collection.delete_many({})
    except Exception as error:
        close_connection()
        raise error
    else:
        close_connection()
        return res
    
def delete_elements_by_month(month: str) -> DeleteResult:
    try:
        db = open_connection()
        collection = db.get_collection(ELEMENT)
        res = collection.delete_many({"assignment.reviewMonth": month})
    except Exception as error:
        close_connection()
        raise error
    else:
        close_connection()
        return res
    
def delete_element(id: str) -> DeleteResult:
    try:
        db = open_connection()
        collection = db.get_collection(ELEMENT)
        res = collection.delete_one({"_id": id})
    except Exception as error:
        close_connection()
        raise error
    else:
        close_connection()
        return res
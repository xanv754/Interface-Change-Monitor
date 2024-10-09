from utils.database import open_connection, close_connection
from models.assignment import AssignmentModel
from constants.collections import ELEMENT
from pymongo.results import UpdateResult
from bson.objectid import ObjectId

def update_assignment(id: str, assigment: AssignmentModel) -> UpdateResult:
    try:
        db = open_connection()
        collection = db.get_collection(ELEMENT)
        res = collection.update_one({"_id": ObjectId(id)}, {"$set": {"assignment": assigment.model_dump()}})
    except Exception as error:
        close_connection()
        raise error
    else:
        close_connection()
        return res
    
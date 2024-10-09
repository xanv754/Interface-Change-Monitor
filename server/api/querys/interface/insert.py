from constants.collections import INTERFACE, BACKUP_INTERFACE
from utils.database import open_connection, close_connection
from pymongo.results import InsertManyResult
from entity.interface import Interface
from typing import List

def insert_interfaces(interfaces: List[Interface]) -> InsertManyResult:
    try:
        data = []
        for interface in interfaces: data.append(interface.model_dump())
        db = open_connection()
        collection = db.get_collection(INTERFACE)
        res = collection.insert_many(data)
    except Exception as error:
        close_connection()
        raise error
    else:
        close_connection()
        return res
    
def insert_backup(interfaces: List[Interface]) -> InsertManyResult:
    try:
        data = []
        for interface in interfaces: data.append(interface.model_dump())
        db = open_connection()
        collection = db.get_collection(BACKUP_INTERFACE)
        res = collection.insert_many(data)
    except Exception as error:
        close_connection()
        raise error
    else:
        close_connection()
        return res
from utils.database import open_connection, close_connection
from models.interface import InterfaceModel
from pymongo.results import UpdateResult
from constants.collections import USER
from typing import List
   
def update_account(username: str, account_status: str) -> UpdateResult:
    try:
        db = open_connection()
        collection = db.get_collection(USER)
        res = collection.update_one({"username": username}, {"$set": {"status": account_status}})
    except Exception as error:
        close_connection()
        raise error
    else:
        close_connection()
        return res
    
def update_assigned(username: str, assigned_interface: List[InterfaceModel]) -> UpdateResult:
    try:
        data = []
        for interface in assigned_interface: data.append(interface.model_dump())
        db = open_connection()
        collection = db.get_collection(USER)
        res = collection.update_one({"username": username}, {"$set": {"assigned": data}})
    except Exception as error:
        close_connection()
        raise error
    else:
        close_connection()
        return res
        
def update_name(username: str, name: str) -> UpdateResult:
    try:
        db = open_connection()
        collection = db.get_collection(USER)
        res = collection.update_one({"username": username}, {"$set": {"name": name}})
    except Exception as error:
        close_connection()
        raise error
    else:
        close_connection()
        return res
    
def update_lastname(username: str, lastname: str) -> UpdateResult:
    try:
        db = open_connection()
        collection = db.get_collection(USER)
        res = collection.update_one({"username": username}, {"$set": {"lastname": lastname}})
    except Exception as error:
        close_connection()
        raise error
    else:
        close_connection()
        return res
    
def update_password(username: str, password: str) -> UpdateResult:
    try:
        db = open_connection()
        collection = db.get_collection(USER)
        res = collection.update_one({"username": username}, {"$set": {"password": password}})
    except Exception as error:
        close_connection()
        raise error
    else:
        close_connection()
        return res
    
def update_last_password(username:str, password: str) -> UpdateResult:
    try:
        db = open_connection()
        collection = db.get_collection(USER)
        res = collection.update_one({"username": username}, {"$set": {"lastPassword": password}})
    except Exception as error:
        close_connection()
        raise error
    else:
        close_connection()
        return res
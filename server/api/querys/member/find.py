from utils.database import open_connection, close_connection
from constants.userStatus import userstatus
from constants.userType import usertype
from constants.collections import USER
from entity.user import User
from entity.admin import Admin
from typing import List

def find_users() -> list:
    try:
        users = []
        db = open_connection()
        collection = db.get_collection(USER)
        res_db = collection.find()
        for res in res_db:
            if res["type"] == usertype.admin:
                admin = Admin(
                    id=str(res["_id"]), 
                    username=res["username"], 
                    password=res["password"], 
                    lastPassword=res["lastPassword"],
                    name=res["name"], 
                    lastname=res["lastname"], 
                    type=res["type"], 
                    status=res["status"]
                )
                users.append(admin)
            elif res["type"] == usertype.user:
                user = User(
                    id=str(res["_id"]), 
                    username=res["username"], 
                    password=res["password"], 
                    lastPassword=res["lastPassword"],
                    name=res["name"], 
                    lastname=res["lastname"], 
                    type=res["type"], 
                    assigned=res["assigned"], 
                    status=res["status"]
                )
                users.append(user)
    except Exception as error:
        close_connection()
        raise error
    else: 
        close_connection()
        return users
    
def find_users_pending() -> list:
    try:
        users = []
        db = open_connection()
        collection = db.get_collection(USER)
        res_db = collection.find({
            "$or": [
                {"status": userstatus.pending},
                {"status": userstatus.password_pending}
            ]
        })
        for res in res_db:
            if res["type"] == usertype.admin:
                admin = Admin(
                    id=str(res["_id"]), 
                    username=res["username"], 
                    password=res["password"], 
                    lastPassword=res["lastPassword"],
                    name=res["name"], 
                    lastname=res["lastname"], 
                    type=res["type"], 
                    status=res["status"]
                )
                users.append(admin)
            elif res["type"] == usertype.user:
                user = User(
                    id=str(res["_id"]), 
                    username=res["username"], 
                    password=res["password"], 
                    lastPassword=res["lastPassword"],
                    name=res["name"], 
                    lastname=res["lastname"], 
                    type=res["type"], 
                    assigned=res["assigned"], 
                    status=res["status"]
                )
                users.append(user)
    except Exception as error:
        close_connection()
        raise error
    else: 
        close_connection()
        return users

def find_users_disabled() -> list:
    try:
        users = []
        db = open_connection()
        collection = db.get_collection(USER)
        res_db = collection.find({"status": userstatus.disabled})
        for res in res_db:
            if res["type"] == usertype.admin:
                admin = Admin(
                    id=str(res["_id"]), 
                    username=res["username"], 
                    password=res["password"], 
                    lastPassword=res["lastPassword"],
                    name=res["name"], 
                    lastname=res["lastname"], 
                    type=res["type"], 
                    status=res["status"]
                )
                users.append(admin)
            elif res["type"] == usertype.user:
                user = User(
                    id=str(res["_id"]), 
                    username=res["username"], 
                    password=res["password"], 
                    lastPassword=res["lastPassword"],
                    name=res["name"], 
                    lastname=res["lastname"], 
                    type=res["type"], 
                    assigned=res["assigned"], 
                    status=res["status"]
                )
                users.append(user)
    except Exception as error:
        close_connection()
        raise error
    else: 
        close_connection()
        return users
       
def find_type_user() -> List[User]:
    try:
        users: List[User] = []
        db = open_connection()
        collection = db.get_collection(USER)
        res_db = collection.find({"type": usertype.user, "status": userstatus.enabled})
        for res in res_db:
            user = User(
                id=str(res["_id"]), 
                username=res["username"], 
                password=res["password"], 
                lastPassword=res["lastPassword"],
                name=res["name"], 
                lastname=res["lastname"], 
                type=res["type"], 
                assigned=res["assigned"], 
                status=res["status"]
            )
            users.append(user)
    except Exception as error:
        close_connection()
        raise error
    else: 
        close_connection()
        return users

def find_type_admin() -> List[Admin]:
    try:
        users: List[Admin] = []
        db = open_connection()
        collection = db.get_collection(USER)
        res_db = collection.find({"type": usertype.admin, "status": userstatus.enabled})
        for res in res_db:
            user = Admin(
                id=str(res["_id"]), 
                username=res["username"], 
                password=res["password"], 
                lastPassword=res["lastPassword"],
                name=res["name"], 
                lastname=res["lastname"], 
                type=res["type"], 
                status=res["status"]
            )
            users.append(user)
    except Exception as error:
        close_connection()
        raise error
    else: 
        close_connection()
        return users
    
def find_user(username: str) -> (User | Admin):
    try:
        db = open_connection()
        collection = db.get_collection(USER)
        res_db = collection.find_one({"username": username})
        if res_db and res_db["type"] == usertype.admin:
            admin = Admin(
                id=str(res_db["_id"]), 
                username=res_db["username"], 
                password=res_db["password"], 
                lastPassword=res_db["lastPassword"],
                name=res_db["name"], 
                lastname=res_db["lastname"], 
                type=res_db["type"], 
                status=res_db["status"]
            )
            close_connection()
            return admin
        elif res_db and res_db["type"] == usertype.user:
            user = User(
                id=str(res_db["_id"]), 
                username=res_db["username"], 
                password=res_db["password"], 
                lastPassword=res_db["lastPassword"],
                name=res_db["name"], 
                lastname=res_db["lastname"], 
                type=res_db["type"], 
                assigned=res_db["assigned"], 
                status=res_db["status"]
            )
            close_connection()
            return user
        else: 
            close_connection()
            return res_db
    except Exception as error:
        close_connection()
        raise error
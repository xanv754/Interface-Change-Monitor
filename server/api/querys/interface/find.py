from constants.collections import INTERFACE, BACKUP_INTERFACE
from utils.database import open_connection, close_connection
from entity.interface import Interface
from typing import List

def find_interfaces() -> List[Interface]:
    try: 
        interfaces: List[Interface] = []
        db = open_connection()
        collection = db.get_collection(INTERFACE)
        res_db = collection.find()
        for res in res_db: 
            interface = Interface(**res)
            interfaces.append(interface)
    except Exception as error:
        close_connection()
        raise error
    else:
        close_connection()
        return interfaces

def find_interface(ip: str, community: str, ifIndex: str) -> Interface:
    try:
        db = open_connection()
        collection = db.get_collection("Interfaces")
        res_db = collection.find_one({"ip": ip, "community": community, "ifIndex": ifIndex})
        if res_db:
            interface = Interface(**res_db)
            close_connection()
            return interface
        else: 
            close_connection()
            return res_db
    except Exception as error:
        close_connection()
        raise error

# BACKUP
def find_backup() -> List[Interface]:
    try: 
        db = open_connection()
        collection = db.get_collection(BACKUP_INTERFACE)
        res_db = collection.find()
        interfaces: List[Interface] = []
        for res in res_db: 
            interface = Interface(**res)
            interfaces.append(interface)
    except Exception as error:
        close_connection()
        raise error
    else:
        close_connection()
        return interfaces

def find_interface_backup(ip: str, community: str, ifIndex: str) -> Interface:
    try:
        db = open_connection()
        collection = db.get_collection(BACKUP_INTERFACE)
        res_db = collection.find_one({"ip": ip, "community": community, "ifIndex": ifIndex})
        if res_db:
            interface = Interface(**res_db)
            close_connection()
            return interface
        else:
            close_connection()
            return res_db
    except Exception as error:
        close_connection()
        raise error
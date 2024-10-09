from utils.database import open_connection, close_connection
from constants.collections import ELEMENT
from bson.objectid import ObjectId
from entity.element import Element
from utils.date import get_date
from typing import List

def find_elements_backup() -> List[Element]:
    try: 
        db = open_connection()
        collection = db.get_collection(ELEMENT)
        res_db = collection.find()
        elements: List[Element] = []
        for res in res_db: 
            element = Element(
                id=str(res["_id"]), 
                date=res["date"], 
                old=res["old"], 
                current=res["current"], 
                assignment=res["assignment"]
            )
            elements.append(element)
    except Exception as error:
        close_connection()
        raise error
    else:
        close_connection()
        return elements

def find_elements() -> List[Element]:
    try: 
        db = open_connection()
        collection = db.get_collection(ELEMENT)
        res_db = collection.find({'date': get_date()})
        elements: List[Element] = []
        for res in res_db: 
            element = Element(
                id=str(res["_id"]), 
                date=res["date"], 
                old=res["old"], 
                current=res["current"], 
                assignment=res["assignment"]
            )
            elements.append(element)
    except Exception as error:
        close_connection()
        raise error
    else:
        close_connection()
        return elements
    
def find_elements_by_month_assigment(month: str) -> List[Element]:
    try: 
        db = open_connection()
        collection = db.get_collection(ELEMENT)
        res_db = collection.find({'assignment.reviewMonth': month})
        elements: List[Element] = []
        for res in res_db: 
            element = Element(
                id=str(res["_id"]), 
                date=res["date"], 
                old=res["old"], 
                current=res["current"], 
                assignment=res["assignment"]
            )
            elements.append(element)
    except Exception as error:
        close_connection()
        raise error
    else:
        close_connection()
        return elements
    
def find_element(id: str) -> Element:
    try:
        db = open_connection()
        collection = db.get_collection(ELEMENT)
        res = collection.find_one({"_id": ObjectId(id)})
        if res:
            element = Element(
                id=str(res["_id"]), 
                date=res["date"], 
                old=res["old"], 
                current=res["current"],
                assignment=res["assignment"]
            )
            close_connection()
            return element
        else: 
            close_connection()
            return res
    except Exception as error:
        close_connection()
        raise error
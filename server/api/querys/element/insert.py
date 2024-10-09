from utils.database import open_connection, close_connection
from pymongo.results import InsertManyResult
from constants.collections import ELEMENT
from entity.element import Element
from typing import List

def insert_elements(elements: List[Element]) -> InsertManyResult:  
    try:
        db = open_connection()
        collection = db.get_collection(ELEMENT)
        data = []
        for element in elements: data.append(element.model_dump(exclude={'id'}))
        res = collection.insert_many(data)
    except Exception as error:
        close_connection()
        raise error
    else:
        close_connection()
        return res

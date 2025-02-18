import json
import redis
from os import getenv
from typing import List
from dotenv import load_dotenv
from constants import InterfaceType
from database import GKEYS
from schemas import ChangesSchema, ChangesJson
from system import DetectChanges
from test import constants, DefaultEquipment, DefaultInterface

load_dotenv(override=True)

URI_REDIS_TEST = getenv("URI_REDIS_TEST")

class DefaultChanges:
    @staticmethod
    def get_changes() -> List[ChangesSchema]:
        date = constants.DATE_CONSULT
        new_equipment = DefaultEquipment.new_insert()
        DefaultInterface.new_insert(
            clean=False,
            date=date,
            equipment=new_equipment,
            interface_type=InterfaceType.OLD.value
        )
        DefaultInterface.new_insert(
            clean=False,
            date=date,
            equipment=new_equipment,
            interface_type=InterfaceType.NEW.value,
            ifName=constants.IFNAME_TWO
        )
        change_controller = DetectChanges()
        changes = change_controller.get_changes(date=date)
        return changes
    
    @staticmethod
    def clean_table() -> None:
        try:
            database = redis.Redis.from_url(URI_REDIS_TEST)
            cursor, keys = database.scan(cursor=0, match=f"{ChangesJson.ID.value}:*")
            while True:
                for key in keys:
                    database.delete(key)
                if cursor == 0:
                    break
                cursor, keys = database.scan(cursor=cursor, match=f"{ChangesJson.ID.value}:*")
            database.close()
        except Exception as e:
            print(e)
    
    @staticmethod
    def new_insert(id: int, changes: ChangesSchema) -> bool:
        try:
            DefaultChanges.clean_table()
            id = str(id)
            changes = json.dumps(changes.model_dump())
            database = redis.Redis.from_url(URI_REDIS_TEST)
            database.hset(f"{GKEYS.CHANGES.value}:{ChangesJson.ID.value}:{id}", mapping={
                "changes": changes
            })
            database.close()
        except Exception as e:
            print(e)
            return False
        else:
            return True
        
    @staticmethod
    def get_all_changes() -> List[ChangesSchema]:
        try:
            database = redis.Redis.from_url(URI_REDIS_TEST)
            cursor, keys = database.scan(cursor=0, match=f"{GKEYS.CHANGES.value}:{ChangesJson.ID.value}:*")
            changes: List[ChangesSchema] = []
            while True:
                for key in keys:
                    data = database.hgetall(key)
                    data_decoded = {k.decode('utf-8'): v.decode('utf-8') for k, v in data.items()}
                    changes_data = json.loads(data_decoded[ChangesJson.CHANGES.value])
                    change = ChangesSchema(**changes_data)
                    changes.append(change)
                if cursor == 0:
                    break
                cursor, keys = database.scan(cursor=cursor, match=f"{ChangesJson.ID.value}:*")
            database.close()
            return changes
        except Exception as e:
            print(e)
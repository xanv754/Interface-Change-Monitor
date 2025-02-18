import traceback
import json
from typing import List
from schemas import ChangesSchema, ChangesJson
from database import RedisDatabase, GKEYS
from utils import Log

class ChangesModel:
    id: str
    changes: str

    def __init__(self, id: int, changes: ChangesSchema):
        self.id = str(id)
        data = changes.model_dump()
        self.changes = json.dumps(data)

    
    @staticmethod
    def get_all_changes() -> List[ChangesSchema]:
        try:
            changes: List[ChangesSchema] = []
            database = RedisDatabase()
            connection = database.get_connection()
            cursor, keys = connection.scan(cursor=0, match=f"{GKEYS.CHANGES.value}:{ChangesJson.ID.value}:*")
            while True:
                for key in keys:
                    data = connection.hgetall(key)
                    data_decoded = {k.decode('utf-8'): v.decode('utf-8') for k, v in data.items()}
                    changes_data = json.loads(data_decoded[ChangesJson.CHANGES.value])
                    change = ChangesSchema(**changes_data)
                    changes.append(change)
                if cursor == 0:
                    break
                cursor, keys = connection.scan(cursor=cursor, match=f"{GKEYS.CHANGES.value}:{ChangesJson.ID.value}:*")
            database.close_connection()
            return changes
        except Exception as e:
            traceback.print_exc()
            Log.save(e, __file__, Log.error)
            return []

    @staticmethod
    def reset_changes():
        try:
            database = RedisDatabase()
            connection = database.get_connection()
            cursor, keys = connection.scan(cursor=0, match=f"{GKEYS.CHANGES.value}:{ChangesJson.ID.value}:*")
            while True:
                for key in keys:
                    connection.delete(key)
                if cursor == 0:
                    break
                cursor, keys = connection.scan(cursor=cursor, match=f"{GKEYS.CHANGES.value}:{ChangesJson.ID.value}:*")
            database.close_connection()
        except Exception as e:
            Log.save(e, __file__, Log.error, console=True)
            return False
        else:
            return True

    def register(self) -> bool:
        try:
            database = RedisDatabase()
            connection = database.get_connection()
            connection.hset(f"{GKEYS.CHANGES.value}:{ChangesJson.ID.value}:{self.id}", mapping={
                ChangesJson.CHANGES.value: self.changes
            })
            database.close_connection()
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return False
        else:
            return True
        
    def get_changes(self) -> dict:
        return self.changes
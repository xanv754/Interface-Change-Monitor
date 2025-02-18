import json
from typing import List
from schemas import ChangesSchema
from database import RedisDatabase
from utils import Log

class Changes:
    id: str
    changes: str

    def __init__(self, id: int, changes: ChangesSchema):
        self.id = str(id)
        data = changes.model_dump()
        self.changes = json.dumps(data)

    
    @staticmethod
    def get_all_changes():
        try:
            changes: List[ChangesSchema] = []
            database = RedisDatabase()
            connection = database.get_connection()
            cursor, keys = connection.scan(cursor=0, match="id:*")
            while True:
                for key in keys:
                    data = connection.hgetall(key)
                    change = ChangesSchema(**data)
                    changes.append(change)
                if cursor == 0:
                    break
            database.close_connection()
            return changes
        except Exception as e:
            Log.save(e, __file__, Log.error)

    @staticmethod
    def reset_changes():
        database = RedisDatabase()
        connection = database.get_connection()
        connection.flushdb()
        database.close_connection()

    def register(self) -> bool:
        try:
            database = RedisDatabase()
            connection = database.get_connection()
            connection.hset(f"id:{self.id}", mapping={
                "changes": self.changes
            })
            database.close_connection()
        except Exception as e:
            Log.save(e, __file__, Log.error, console=True)
            return False
        else:
            return True
        
    def get_changes(self) -> dict:
        return self.changes
import json
import redis
import psycopg2
from os import getenv
from typing import List
from dotenv import load_dotenv
from constants import InterfaceType
from database import GKEYS, GTABLES, ChangesSchemaDB
from schemas import ChangeInterfaceSchema, ChangeJsonSchema, ChangeSchema
from system import DetectChanges
from test import constants, DefaultEquipment, DefaultInterface, DefaultOperator


load_dotenv(override=True)

URI = getenv("URI_TEST")
URI_REDIS_TEST = getenv("URI_REDIS_TEST")

class DefaultChangesRedisDB:
    @staticmethod
    def get_changes() -> List[ChangeInterfaceSchema]:
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
        changes = change_controller._get_changes(date=date)
        return changes
    
    @staticmethod
    def clean_table() -> None:
        try:
            database = redis.Redis.from_url(URI_REDIS_TEST)
            cursor, keys = database.scan(cursor=0, match=f"{ChangeJsonSchema.ID.value}:*")
            while True:
                for key in keys:
                    database.delete(key)
                if cursor == 0:
                    break
                cursor, keys = database.scan(cursor=cursor, match=f"{ChangeJsonSchema.ID.value}:*")
            database.close()
        except Exception as e:
            print(e)
    
    @staticmethod
    def new_insert(id: int, changes: ChangeInterfaceSchema) -> bool:
        try:
            DefaultChangesRedisDB.clean_table()
            id = str(id)
            changes = json.dumps(changes.model_dump())
            database = redis.Redis.from_url(URI_REDIS_TEST)
            database.hset(f"{GKEYS.CHANGES.value}:{ChangeJsonSchema.ID.value}:{id}", mapping={
                "changes": changes
            })
            database.close()
        except Exception as e:
            print(e)
            return False
        else:
            return True
        
    @staticmethod
    def get_all_changes() -> List[ChangeInterfaceSchema]:
        try:
            database = redis.Redis.from_url(URI_REDIS_TEST)
            cursor, keys = database.scan(cursor=0, match=f"{GKEYS.CHANGES.value}:{ChangeJsonSchema.ID.value}:*")
            changes: List[ChangeInterfaceSchema] = []
            while True:
                for key in keys:
                    data = database.hgetall(key)
                    data_decoded = {k.decode('utf-8'): v.decode('utf-8') for k, v in data.items()}
                    changes_data = json.loads(data_decoded[ChangeJsonSchema.CHANGES.value])
                    change = ChangeInterfaceSchema(**changes_data)
                    changes.append(change)
                if cursor == 0:
                    break
                cursor, keys = database.scan(cursor=cursor, match=f"{ChangeJsonSchema.ID.value}:*")
            database.close()
            return changes
        except Exception as e:
            print(e)

class DefaultChangesPostgresDB:
    @staticmethod
    def clean_table() -> None:
        """Clean the table of the changes."""
        connection = psycopg2.connect(URI)
        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM {GTABLES.CHANGE.value};")
        connection.commit()
        cursor.close()
        connection.close()
        DefaultInterface.clean_table()
        DefaultEquipment.clean_table()
        DefaultOperator.clean_table()

    @staticmethod
    def get_change(id: int) -> ChangeSchema | None:
        """Get the change with the given ID."""
        connection = psycopg2.connect(URI)
        cursor = connection.cursor()
        cursor.execute(
            f"""SELECT * FROM {GTABLES.CHANGE.value} 
            {ChangesSchemaDB.ID.value} = %s""",
            (  
                id,
            ),
        )
        result = cursor.fetchone()
        if result is None:
            return None
        new_change = ChangeSchema(
            id=result[0],
            newInterface=result[1],
            oldInterface=result[2],
            operator=(result[3] if result[3] != None else None)
        )
        cursor.close()
        connection.close()
        return new_change
    
    @staticmethod
    def new_insert() -> ChangeSchema | None:
        """Create a new change."""
        DefaultChangesPostgresDB.clean_table()
        equipment = DefaultEquipment.new_insert()
        old_interface = DefaultInterface.new_insert(
            clean=False,
            equipment=equipment,
            date=constants.DATE_CONSULT,
            interface_type=InterfaceType.OLD.value,
            ifIndex=constants.IFINDEX
        )
        new_interface = DefaultInterface.new_insert(
            clean=False,
            equipment=equipment,
            date=constants.DATE_CONSULT_TWO,
            interface_type=InterfaceType.NEW.value,
            ifIndex=constants.IFINDEX,
            ifName=constants.IFNAME_TWO
        )
        connection = psycopg2.connect(URI)
        cursor = connection.cursor()
        cursor.execute(
            f"""INSERT INTO {GTABLES.CHANGE.value} (
                {ChangesSchemaDB.NEW_INTERFACE.value}, 
                {ChangesSchemaDB.OLD_INTERFACE.value}
            ) VALUES (%s, %s)
            """,
            (
                new_interface.id,
                old_interface.id,
            ),
        )
        connection.commit()
        cursor.execute(
            f"""SELECT * FROM {GTABLES.CHANGE.value} 
            WHERE {ChangesSchemaDB.NEW_INTERFACE.value} = %s AND 
            {ChangesSchemaDB.OLD_INTERFACE.value} = %s""",
            (  
                new_interface.id, 
                old_interface.id, 
            ),
        )
        result = cursor.fetchone()
        if result is None:
            return None
        new_change = ChangeSchema(
            id=result[0],
            newInterface=result[1],
            oldInterface=result[2],
            operator=(result[3] if result[3] != None else None)
        )
        cursor.close()
        connection.close()
        return new_change
    
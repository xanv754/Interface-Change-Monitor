from typing import List
from database import PostgresDatabase, GTABLES, EquipmentSchemaDB
from schemas import EquipmentSchema
from utils import equipment_to_dict, Log


class Equipment:
    id: int | None
    ip: str | None
    community: str | None
    sysname: str | None

    def __init__(
        self,
        id: int | None = None,
        ip: str | None = None,
        community: str | None = None,
        sysname: str | None = None,
    ):
        self.id = id
        self.ip = ip
        self.community = community
        self.sysname = sysname

    @staticmethod
    def get_all() -> List[EquipmentSchema]:
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(f"""SELECT * FROM {GTABLES.EQUIPMENT.value}""")
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return equipment_to_dict(result)
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return []

    def get_all_by_sysname(self) -> List[EquipmentSchema]:
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""SELECT * FROM {GTABLES.EQUIPMENT.value} 
                WHERE {EquipmentSchemaDB.SYSNAME.value} = %s""",
                (self.sysname,),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return equipment_to_dict(result)
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return []

    def get_by_id(self) -> EquipmentSchema | None:
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""SELECT * FROM {GTABLES.EQUIPMENT.value} 
                WHERE {EquipmentSchemaDB.ID.value} = %s""",
                (self.id,),
            )
            result = cursor.fetchone()
            database.close_connection()
            if not result:
                return None
            equipment = equipment_to_dict([result])
            return equipment[0]
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return None

    def get_by_device(self) -> EquipmentSchema | None:
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""SELECT * FROM {GTABLES.EQUIPMENT.value} 
                WHERE {EquipmentSchemaDB.IP.value} = %s AND 
                {EquipmentSchemaDB.COMMUNITY.value} = %s""",
                (self.ip, self.community),
            )
            result = cursor.fetchone()
            database.close_connection()
            if not result:
                return None
            equipment = equipment_to_dict([result])
            return equipment[0]
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return None

    def update_sysname(self, sysname: str) -> bool:
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            cursor.execute(
                f"""UPDATE {GTABLES.EQUIPMENT.value} 
                SET {EquipmentSchemaDB.SYSNAME.value} = %s 
                WHERE {EquipmentSchemaDB.IP.value} = %s AND
                {EquipmentSchemaDB.COMMUNITY.value} = %s""",
                (sysname, self.ip, self.community),
            )
            connection.commit()
            status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return False
        else:
            if status and status == "UPDATE 1":
                return True
            else:
                return False

    def update_community(self, community: str) -> bool:
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            cursor.execute(
                f"""UPDATE {GTABLES.EQUIPMENT.value} 
                SET {EquipmentSchemaDB.COMMUNITY.value} = %s 
                WHERE {EquipmentSchemaDB.ID.value} = %s""",
                (community, self.id),
            )
            connection.commit()
            status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return False
        else:
            if status and status == "UPDATE 1":
                return True
            else:
                return False

    def delete(self) -> bool:
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            cursor.execute(
                f"""DELETE FROM {GTABLES.EQUIPMENT.value} 
                WHERE {EquipmentSchemaDB.ID.value} = %s""",
                (self.id,),
            )
            connection.commit()
            status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return False
        else:
            if status and status == "DELETE 1":
                return True
            else:
                return False

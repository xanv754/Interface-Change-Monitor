from typing import List
from constants import GTABLES, EquipmentFields
from database import PostgresDatabase
from utils import equipment_to_dict


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
    def get_all() -> List[dict]:
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(f"SELECT * FROM {GTABLES.EQUIPMENT.value}")
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return equipment_to_dict(result)
        except Exception as e:
            print(e)
            return []

    def get_all_by_sysname(self) -> List[dict]:
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"SELECT * FROM {GTABLES.EQUIPMENT.value} WHERE {EquipmentFields.SYSNAME.value} = %s",
                (self.sysname,),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return equipment_to_dict(result)
        except Exception as e:
            print(e)
            return []

    def get_by_id(self) -> List[dict]:
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"SELECT * FROM {GTABLES.EQUIPMENT.value} WHERE {EquipmentFields.ID.value} = %s",
                (self.id,),
            )
            result = cursor.fetchone()
            database.close_connection()
            if not result:
                return []
            return equipment_to_dict([result])
        except Exception as e:
            print(e)
            return []

    def get_by_device(self) -> List[dict]:
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"SELECT * FROM {GTABLES.EQUIPMENT.value} WHERE {EquipmentFields.IP.value} = %s AND {EquipmentFields.COMMUNITY.value} = %s",
                (self.ip, self.community),
            )
            result = cursor.fetchone()
            database.close_connection()
            if not result:
                return []
            return equipment_to_dict([result])
        except Exception as e:
            print(e)
            return []

    def update_sysname(self, sysname: str) -> bool:
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            cursor.execute(
                f"UPDATE {GTABLES.EQUIPMENT.value} SET {EquipmentFields.SYSNAME.value} = %s WHERE {EquipmentFields.ID.value} = %s",
                (sysname, self.id),
            )
            connection.commit()
            status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            print(e)
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
                f"UPDATE {GTABLES.EQUIPMENT.value} SET {EquipmentFields.COMMUNITY.value} = %s WHERE {EquipmentFields.ID.value} = %s",
                (community, self.id),
            )
            connection.commit()
            status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            print(e)
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
                f"DELETE FROM {GTABLES.EQUIPMENT.value} WHERE {EquipmentFields.ID.value} = %s",
                (self.id,),
            )
            connection.commit()
            status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            print(e)
            return False
        else:
            if status and status == "DELETE 1":
                return True
            else:
                return False

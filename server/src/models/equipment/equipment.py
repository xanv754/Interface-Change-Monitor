from typing import List
from constants import GTABLES, EquipmentFields
from utils import PostgresDatabase


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
            equipments: List[dict] = []
            for res in result:
                equipments.append(
                    {
                        EquipmentFields.ID.value: res[0],
                        EquipmentFields.IP.value: res[1],
                        EquipmentFields.COMMUNITY.value: res[2],
                        EquipmentFields.SYSNAME.value: res[3],
                        EquipmentFields.CREATED_AT.value: res[4].strftime("%Y-%m-%d"),
                        EquipmentFields.UPDATED_AT.value: (
                            res[5].strftime("%Y-%m-%d") if res[5] != None else None
                        ),
                    }
                )
            return equipments
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
            equipments: List[dict] = []
            for res in result:
                equipments.append(
                    {
                        EquipmentFields.ID.value: res[0],
                        EquipmentFields.IP.value: res[1],
                        EquipmentFields.COMMUNITY.value: res[2],
                        EquipmentFields.SYSNAME.value: res[3],
                        EquipmentFields.CREATED_AT.value: res[4].strftime("%Y-%m-%d"),
                        EquipmentFields.UPDATED_AT.value: (
                            res[5].strftime("%Y-%m-%d") if res[5] != None else None
                        ),
                    }
                )
            return equipments
        except Exception as e:
            print(e)
            return []

    def get_by_id(self) -> dict | None:
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
                return None
            equipment = {
                EquipmentFields.ID.value: result[0],
                EquipmentFields.IP.value: result[1],
                EquipmentFields.COMMUNITY.value: result[2],
                EquipmentFields.SYSNAME.value: result[3],
                EquipmentFields.CREATED_AT.value: result[4].strftime("%Y-%m-%d"),
                EquipmentFields.UPDATED_AT.value: (
                    result[5].strftime("%Y-%m-%d") if result[5] != None else None
                ),
            }
            return equipment
        except Exception as e:
            print(e)
            return None

    def get_by_device(self) -> dict | None:
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
                return None
            equipment = {
                EquipmentFields.ID.value: result[0],
                EquipmentFields.IP.value: result[1],
                EquipmentFields.COMMUNITY.value: result[2],
                EquipmentFields.SYSNAME.value: result[3],
                EquipmentFields.CREATED_AT.value: result[4].strftime("%Y-%m-%d"),
                EquipmentFields.UPDATED_AT.value: (
                    result[5].strftime("%Y-%m-%d") if result[5] != None else None
                ),
            }
            return equipment
        except Exception as e:
            print(e)
            return None

from typing import List
from constants import GTABLES
from database import PostgresDatabase
from schemas import InterfaceSchema
from utils import interface_to_dict


class Interface:
    id: int
    ifIndex: int
    idEquipment: int
    dateConsult: str

    def __init__(
        self,
        id: int | None = None,
        ifIndex: int | None = None,
        idEquipment: int | None = None,
        dateConsult: str | None = None,
    ):
        self.id = id
        self.ifIndex = ifIndex
        self.idEquipment = idEquipment
        self.dateConsult = dateConsult

    def get_all_by_date(self) -> List[dict]:
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""SELECT * FROM {GTABLES.INTERFACE.value} 
                WHERE {InterfaceSchema.DATE_CONSULT.value} = %s""",
                (self.dateConsult,),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result: return []
            return interface_to_dict(result)
        except Exception as e:
            print(e)
            return []

    def get_by_device_date(self) -> dict | None:
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""SELECT * FROM {GTABLES.INTERFACE.value} 
                WHERE {InterfaceSchema.ID_EQUIPMENT.value} = %s AND 
                {InterfaceSchema.IFINDEX.value} = %s AND 
                {InterfaceSchema.DATE_CONSULT.value} = %s""",
                (self.idEquipment, self.ifIndex, self.dateConsult),
            )
            result = cursor.fetchone()
            database.close_connection()
            if not result: return None
            interface = interface_to_dict([result])
            return interface[0]
        except Exception as e:
            print(e)
            return None

    def get_by_id(self) -> dict | None:
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""SELECT * FROM {GTABLES.INTERFACE.value} 
                WHERE {InterfaceSchema.ID.value} = %s""",
                (self.id,),
            )
            result = cursor.fetchone()
            database.close_connection()
            if not result: return None
            interface = interface_to_dict([result])
            return interface[0]
        except Exception as e:
            print(e)
            return None

    def delete(self) -> bool:
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            cursor.execute(
                f"""DELETE FROM {GTABLES.INTERFACE.value} 
                WHERE {InterfaceSchema.ID.value} = %s""",
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

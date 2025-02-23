import psycopg2
from os import getenv
from dotenv import load_dotenv
from database import GTABLES, EquipmentSchemaDB
from schemas import EquipmentResponseSchema
from test import constants

load_dotenv(override=True)

URI = getenv("URI_TEST")

class DefaultEquipment:
    @staticmethod
    def clean_table() -> None:
        connection = psycopg2.connect(URI)
        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM {GTABLES.EQUIPMENT.value};")
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def new_insert(
        ip: str = constants.IP,
        community: str = constants.COMMUNITY,
        sysname: str = constants.SYSNAME
    ) -> EquipmentResponseSchema | None:
        DefaultEquipment.clean_table()
        connection = psycopg2.connect(URI)
        cursor = connection.cursor()
        cursor.execute(
            f"""INSERT INTO {GTABLES.EQUIPMENT.value} (
                {EquipmentSchemaDB.IP.value}, 
                {EquipmentSchemaDB.COMMUNITY.value}, 
                {EquipmentSchemaDB.SYSNAME.value}
            ) VALUES (%s, %s, %s)
            """,
            (ip, community, sysname),
        )
        connection.commit()
        cursor.execute(
            f"""SELECT * FROM {GTABLES.EQUIPMENT.value} 
            WHERE {EquipmentSchemaDB.IP.value} = %s AND 
            {EquipmentSchemaDB.COMMUNITY.value} = %s""",
            (ip, community),
        )
        result = cursor.fetchone()
        if result is None:
            return None
        equipment = EquipmentResponseSchema(
            id=result[0],
            ip=result[1],
            community=result[2],
            sysname=result[3] if result[3] != None else None,
            createdAt=result[4].strftime("%Y-%m-%d"),
            updatedAt=result[5].strftime("%Y-%m-%d") if result[5] != None else None
        )
        cursor.close()
        connection.close()
        return equipment
    
    @staticmethod
    def select_one_by_id(id: int) -> EquipmentResponseSchema | None:
        connection = psycopg2.connect(URI)
        cursor = connection.cursor()
        cursor.execute(
            f"""SELECT * FROM {GTABLES.EQUIPMENT.value} 
            WHERE {EquipmentSchemaDB.ID.value} = %s""",
            (id,),
        )
        result = cursor.fetchone()
        if result is None:
            return None
        equipment = EquipmentResponseSchema(
            id=result[0],
            ip=result[1],
            community=result[2],
            sysname=result[3] if result[3] != None else None,
            createdAt=result[4].strftime("%Y-%m-%d"),
            updatedAt=result[5].strftime("%Y-%m-%d") if result[5] != None else None
        )
        cursor.close()
        connection.close()
        return equipment
    
    @staticmethod
    def select_one_by_device(ip: str, community: str) -> EquipmentResponseSchema | None:
        connection = psycopg2.connect(URI)
        cursor = connection.cursor()
        cursor.execute(
            f"""SELECT * FROM {GTABLES.EQUIPMENT.value} 
            WHERE {EquipmentSchemaDB.IP.value} = %s AND 
            {EquipmentSchemaDB.COMMUNITY.value} = %s""",
            (ip, community),
        )
        result = cursor.fetchone()
        if result is None:
            return None
        equipment = EquipmentResponseSchema(
            id=result[0],
            ip=result[1],
            community=result[2],
            sysname=result[3] if result[3] != None else None,
            createdAt=result[4].strftime("%Y-%m-%d"),
            updatedAt=result[5].strftime("%Y-%m-%d") if result[5] != None else None
        )
        cursor.close()
        connection.close()
        return equipment
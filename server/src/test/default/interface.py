import psycopg2
from os import getenv
from dotenv import load_dotenv
from database import GTABLES, InterfaceSchemaDB
from schemas import EquipmentSchema, InterfaceSchema
from test import constants, DefaultEquipment

load_dotenv(override=True)

URI = getenv("URI_TEST")

class DefaultInterface:
    @staticmethod
    def clean_table() -> None:
        connection = psycopg2.connect(URI)
        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM {GTABLES.INTERFACE.value};")
        cursor.execute(f"DELETE FROM {GTABLES.EQUIPMENT.value};")
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def new_insert(
        clean: bool = True,
        date: str = constants.DATE_CONSULT,
        equipment: EquipmentSchema | None = None,
        ifIndex: int = constants.IFINDEX,
        interface_type: str = "NEW",
        ifName: str = constants.IFNAME, 
    ) -> InterfaceSchema | None:
        if clean: DefaultInterface.clean_table()
        if equipment is None:
            equipment = DefaultEquipment.new_insert()
            if equipment is None: return None
        connection = psycopg2.connect(URI)
        cursor = connection.cursor()
        cursor.execute(
            f"""INSERT INTO {GTABLES.INTERFACE.value} (
                {InterfaceSchemaDB.IFINDEX.value},
                {InterfaceSchemaDB.ID_EQUIPMENT.value},
                {InterfaceSchemaDB.DATE_CONSULT.value},
                {InterfaceSchemaDB.INTERFACE_TYPE.value},
                {InterfaceSchemaDB.IFNAME.value},
                {InterfaceSchemaDB.IFDESCR.value},
                {InterfaceSchemaDB.IFALIAS.value},
                {InterfaceSchemaDB.IFHIGHSPEED.value},
                {InterfaceSchemaDB.IFOPERSTATUS.value},
                {InterfaceSchemaDB.IFADMINSTATUS.value}
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                ifIndex,
                equipment.id,
                date,
                interface_type,
                ifName,
                "test@ifDescr",
                "test@ifAlias",
                1000,
                "UP",
                "UP",
            ),
        )
        connection.commit()
        cursor.execute(
            f"""SELECT * FROM {GTABLES.INTERFACE.value}
            WHERE {InterfaceSchemaDB.IFINDEX.value} = %s AND
            {InterfaceSchemaDB.ID_EQUIPMENT.value} = %s AND
            {InterfaceSchemaDB.INTERFACE_TYPE.value} = %s""",
            (ifIndex, equipment.id, interface_type),
        )
        result = cursor.fetchone()
        if result is None:
            return None
        interface = InterfaceSchema(
            id=result[0],
            equipment=result[2],
            date=result[3].strftime("%Y-%m-%d"),
            type=result[4],
            ifIndex=result[1],
            ifName=result[5],
            ifDescr=result[6],
            ifAlias=result[7],
            ifHighSpeed=result[8],
            ifOperStatus=result[9],
            ifAdminStatus=result[10],
        )
        cursor.close()
        connection.close()
        return interface

    @staticmethod
    def select_one_by_id(id: int) -> InterfaceSchema | None:
        connection = psycopg2.connect(URI)
        cursor = connection.cursor()
        cursor.execute(
            f"""SELECT * FROM {GTABLES.INTERFACE.value}
            WHERE {InterfaceSchemaDB.ID.value} = %s""",
            (id,),
        )
        result = cursor.fetchone()
        if result is None:
            return None
        interface = InterfaceSchema(
            id=result[0],
            equipment=result[2],
            date=result[3].strftime("%Y-%m-%d"),
            type=result[4],
            ifIndex=result[1],
            ifName=result[5],
            ifDescr=result[6],
            ifAlias=result[7],
            ifHighSpeed=result[8],
            ifOperStatus=result[9],
            ifAdminStatus=result[10],
        )
        cursor.close()
        connection.close()
        return interface

    @staticmethod
    def select_one_by_device_type(ip: str, community: str, ifIndex: int, type: str) -> InterfaceSchema | None:
        equipment = DefaultEquipment.select_one_by_device(ip, community)
        if equipment is None: return None
        connection = psycopg2.connect(URI)
        cursor = connection.cursor()
        cursor.execute(
            f"""SELECT * FROM {GTABLES.INTERFACE.value}
            WHERE {InterfaceSchemaDB.IFINDEX.value} = %s AND
            {InterfaceSchemaDB.ID_EQUIPMENT.value} = %s AND
            {InterfaceSchemaDB.INTERFACE_TYPE.value} = %s""",
            (ifIndex, equipment.id, type),
        )
        result = cursor.fetchone()
        if result is None:
            return None
        interface = InterfaceSchema(
            id=result[0],
            equipment=result[2],
            date=result[3].strftime("%Y-%m-%d"),
            type=result[4],
            ifIndex=result[1],
            ifName=result[5],
            ifDescr=result[6],
            ifAlias=result[7],
            ifHighSpeed=result[8],
            ifOperStatus=result[9],
            ifAdminStatus=result[10],
        )
        cursor.close()
        connection.close()
        return interface

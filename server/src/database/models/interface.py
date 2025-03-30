from os import strerror
from typing import List
from constants.types import InterfaceType
from database.constants.tables import Tables as GTABLES # Global Tables
from database.database import PostgresDatabase
from database.schemas.interface import InterfaceSchemaDB
from schemas.interface import InterfaceSchema
from utils.convert import InterfaceResponse
from utils.log import LogHandler


class InterfaceModel:
    """Model for all queries of the interface table."""

    @staticmethod
    def register(
        ifIndex: int,
        id_equipment: int,
        date_consult: str,
        interface_type: str,
        ifName: str,
        ifDescr: str,
        ifAlias: str,
        ifHighSpeed: int,
        ifOperStatus: str,
        ifAdminStatus: str
    ) -> bool:
        """Register a new interface in the database.

        Parameters
        ----------
        ifIndex : int
            Interface's index.
        id_equipment : int
            Interface's equipment ID.
        date_consult : str
            Interface's date consult.
        interface_type : str
            Interface's type. Options: 'NEW'/'OLD'.
        ifName : str
            Interface's name.
        ifDescr : str
            Interface's description.
        ifAlias : str
            Interface's alias.
        ifHighSpeed : int
            Interface's high speed.
        ifOperStatus : str
            Interface's operational status.
        ifAdminStatus : str
            Interface's administrative status.
        """
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                    INSERT INTO {GTABLES.INTERFACE.value} (
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
                    id_equipment,
                    date_consult,
                    interface_type,
                    ifName,
                    ifDescr,
                    ifAlias,
                    ifHighSpeed,
                    ifOperStatus,
                    ifAdminStatus,
                ),
            )
            connection.commit()
            status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return False
        else:
            if status and status == "INSERT 0 1":
                return True
            else:
                return False

    @staticmethod
    def get_all_by_type(type: str, date: str) -> List[InterfaceSchema]:
        """Get all interfaces filter by type of the interface.

        Parameters
        ----------
        type : str
            Type of the interface.
            - **NEW:** New interface.
            - **OLD:** Old interface.
        date: str
            SNMP's date consult.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                    SELECT *
                    FROM
                        {GTABLES.INTERFACE.value}
                    WHERE
                        {InterfaceSchemaDB.INTERFACE_TYPE.value} = %s AND
                        {InterfaceSchemaDB.DATE_CONSULT.value} = %s
                """,
                (type.upper(), date),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return InterfaceResponse.convert_to_dict(result)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return []

    @staticmethod
    def get_all_by_date_consult(date_consult: str) -> List[InterfaceSchema]:
        """Get all interfaces filter by date of consult of the equipment.

        Parameters
        ----------
        date_consult : str
            SNMP's date consult.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                    SELECT *
                    FROM
                        {GTABLES.INTERFACE.value}
                    WHERE
                        {InterfaceSchemaDB.DATE_CONSULT.value} = %s
                """,
                (date_consult,),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return InterfaceResponse.convert_to_dict(result)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return []

    @staticmethod
    def get_by_equipment_type(ifIndex: int, id_equipment: int, interface_type: str) -> InterfaceSchema | None:
        """Get an interface filter by equipment, ifIndex and type of the interface.

        Parameters
        ----------
        ifIndex : int
            Interface's index.
        id_equipment : int
            Interface's equipment ID.
        type : str
            Type of the interface.
            - **NEW:** New interface.
            - **OLD:** Old interface.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                    SELECT *
                    FROM
                        {GTABLES.INTERFACE.value}
                    WHERE
                        {InterfaceSchemaDB.ID_EQUIPMENT.value} = %s AND
                        {InterfaceSchemaDB.IFINDEX.value} = %s AND
                        {InterfaceSchemaDB.INTERFACE_TYPE.value} = %s
                """,
                (id_equipment, ifIndex, interface_type.upper()),
            )
            result = cursor.fetchone()
            database.close_connection()
            if not result:
                return None
            return InterfaceResponse.convert_to_dict([result])[0]
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return None

    @staticmethod
    def get_by_device_date(ifIndex: int, id_equipment: int, date_consult: str) -> InterfaceSchema | None:
        """Get an interface filter by date of consult of the equipment.

        Parameters
        ----------
        ifIndex : int
            Interface's index.
        if-equipment : int
            Interface's equipment ID.
        date_consult : str
            SNMP's date consult.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                    SELECT *
                    FROM
                        {GTABLES.INTERFACE.value}
                    WHERE
                        {InterfaceSchemaDB.ID_EQUIPMENT.value} = %s AND
                        {InterfaceSchemaDB.IFINDEX.value} = %s AND
                        {InterfaceSchemaDB.DATE_CONSULT.value} = %s
                """,
                (id_equipment, ifIndex, date_consult),
            )
            result = cursor.fetchone()
            database.close_connection()
            if not result:
                return None
            return InterfaceResponse.convert_to_dict([result])[0]
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return None

    @staticmethod
    def get_by_id(id: int) -> InterfaceSchema | None:
        """Get info of the interface by ID.

        Parameters
        ----------
        id : int
            Interface's ID.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                    SELECT *
                    FROM
                        {GTABLES.INTERFACE.value}
                    WHERE
                        {InterfaceSchemaDB.ID.value} = %s
                """,
                (id,),
            )
            result = cursor.fetchone()
            database.close_connection()
            if not result:
                return None
            return InterfaceResponse.convert_to_dict([result])[0]
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return None

    @staticmethod
    def update(
        id: int,
        date_consult: str,
        interface_type: str,
        ifName: str,
        ifDescr: str,
        ifAlias: str,
        ifHighSpeed: int,
        ifOperStatus: str,
        ifAdminStatus: str
    ) -> bool:
        """Update data of an interface.

        Parameters
        ----------
        id : int
            Interface's ID.
        date_consult : str
            Interface's date consult.
        interface_type : str
            Interface's type. Options: 'NEW'/'OLD'.
        ifName : str
            Interface's name.
        ifDescr : str
            Interface's description.
        ifAlias : str
            Interface's alias.
        ifHighSpeed : int
            Interface's high speed.
        ifOperStatus : str
            Interface's operational status.
        ifAdminStatus : str
            Interface's administrative status.
        """
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                    UPDATE
                        {GTABLES.INTERFACE.value}
                    SET
                        {InterfaceSchemaDB.DATE_CONSULT.value} = %s,
                        {InterfaceSchemaDB.IFNAME.value} = %s,
                        {InterfaceSchemaDB.IFDESCR.value} = %s,
                        {InterfaceSchemaDB.IFALIAS.value} = %s,
                        {InterfaceSchemaDB.IFHIGHSPEED.value} = %s,
                        {InterfaceSchemaDB.IFOPERSTATUS.value} = %s,
                        {InterfaceSchemaDB.IFADMINSTATUS.value} = %s
                    WHERE
                        {InterfaceSchemaDB.ID.value} = %s
                """,
                (
                    date_consult,
                    ifName,
                    ifDescr,
                    ifAlias,
                    ifHighSpeed,
                    ifOperStatus.upper(),
                    ifAdminStatus.upper(),
                    id,
                ),
            )
            connection.commit()
            status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return False
        else:
            if status and status == "UPDATE 1":
                return True
            else:
                return False

    @staticmethod
    def update_type(id: int, type: str) -> bool:
        """Update type of the interface.

        Parameters
        ----------
        id : int
            Interface's ID.
        type : str
            New type of the interface.
            - **NEW:** New interface.
            - **OLD:** Old interface.
        """
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                    UPDATE
                        {GTABLES.INTERFACE.value}
                    SET
                        {InterfaceSchemaDB.INTERFACE_TYPE.value} = %s
                    WHERE
                        {InterfaceSchemaDB.ID.value} = %s
                """,
                (type.upper(), id),
            )
            connection.commit()
            status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return False
        else:
            if status and status == "UPDATE 1":
                return True
            else:
                return False

    @staticmethod
    def delete(id: int) -> bool:
        """Delete the interface.

        Parameters
        ----------
        id : int
            Interface's ID.
        """
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                    DELETE FROM
                        {GTABLES.INTERFACE.value}
                    WHERE
                        {InterfaceSchemaDB.ID.value} = %s
                """,
                (id,),
            )
            connection.commit()
            status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return False
        else:
            if status and status == "DELETE 1":
                return True
            else:
                return False

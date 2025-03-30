from typing import List
from psycopg2 import sql
from database.constants.tables import Tables as GTABLES # Global Tables
from database.database import PostgresDatabase
from database.schemas.changes import ChangesSchemaDB
from database.schemas.equipment import EquipmentSchemaDB
from database.schemas.interface import InterfaceSchemaDB
from schemas.change import ChangeInterfaceSchema, RegisterChangeBody
from utils.convert import ChangeResponse
from utils.log import LogHandler


class ChangeModel:
    """Model for all queries of the changes table."""

    @staticmethod
    def register(changes: List[RegisterChangeBody]) -> bool:
        """Register new changes in the database."""
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            with cursor:
                query = sql.SQL(
                    """
                        INSERT INTO {table} ({new_interface}, {old_interface})
                        VALUES (%s, %s)
                    """
                ).format(
                        table=sql.Identifier(GTABLES.CHANGE.value),
                        new_interface=sql.Identifier(ChangesSchemaDB.NEW_INTERFACE.value),
                        old_interface=sql.Identifier(ChangesSchemaDB.OLD_INTERFACE.value),
                    )
                for new_change in changes:
                    cursor.execute(query, (
                        new_change.newInterface,
                        new_change.oldInterface,
                    ))
            connection.commit()
            status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return False
        else:
            if status and "INSERT" in status:
                return True
            else:
                return False

    @staticmethod
    def get_changes() -> List[ChangeInterfaceSchema]:
        """Get list with all changes."""
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                    SELECT
                        c.{ChangesSchemaDB.ID.value} AS id,
                        e.{EquipmentSchemaDB.IP.value} AS ip,
                        e.{EquipmentSchemaDB.COMMUNITY.value} AS community,
                        e.{EquipmentSchemaDB.SYSNAME.value} AS sysname,
                        newInterface.{InterfaceSchemaDB.IFINDEX.value} AS ifIndex,
                        newInterface.{InterfaceSchemaDB.ID.value} as newID,
                        newInterface.{InterfaceSchemaDB.ID_EQUIPMENT.value} AS newEquipment,
                        newInterface.{InterfaceSchemaDB.DATE_CONSULT.value} AS newDate,
                        newInterface.{InterfaceSchemaDB.INTERFACE_TYPE.value} AS newType,
                        newInterface.{InterfaceSchemaDB.IFNAME.value} AS newIfName,
                        newInterface.{InterfaceSchemaDB.IFDESCR.value} AS newIfDescr,
                        newInterface.{InterfaceSchemaDB.IFALIAS.value} AS newIfAlias,
                        newInterface.{InterfaceSchemaDB.IFHIGHSPEED.value} AS newIfHighSpeed,
                        newInterface.{InterfaceSchemaDB.IFOPERSTATUS.value} AS newIfOperStatus,
                        newInterface.{InterfaceSchemaDB.IFADMINSTATUS.value} AS newIfAdminStatus,
                        oldInterface.{InterfaceSchemaDB.ID.value} AS oldID,
                        oldInterface.{InterfaceSchemaDB.ID_EQUIPMENT.value} AS oldEquipment,
                        oldInterface.{InterfaceSchemaDB.DATE_CONSULT.value} AS oldDate,
                        oldInterface.{InterfaceSchemaDB.INTERFACE_TYPE.value} AS oldType,
                        oldInterface.{InterfaceSchemaDB.IFNAME.value} AS oldIfName,
                        oldInterface.{InterfaceSchemaDB.IFDESCR.value} AS oldIfDescr,
                        oldInterface.{InterfaceSchemaDB.IFALIAS.value} AS oldIfAlias,
                        oldInterface.{InterfaceSchemaDB.IFHIGHSPEED.value} AS oldIfHighSpeed,
                        oldInterface.{InterfaceSchemaDB.IFOPERSTATUS.value} AS oldIfOperStatus,
                        oldInterface.{InterfaceSchemaDB.IFADMINSTATUS.value} AS oldIfAdminStatus,
                        c.{ChangesSchemaDB.OPERATOR.value} AS operator
                    FROM
                        {GTABLES.CHANGE.value} c
                    JOIN
                        {GTABLES.INTERFACE.value} newInterface ON c.{ChangesSchemaDB.NEW_INTERFACE.value} = newInterface.{InterfaceSchemaDB.ID.value}
                    JOIN
                        {GTABLES.INTERFACE.value} oldInterface ON c.{ChangesSchemaDB.OLD_INTERFACE.value} = oldInterface.{InterfaceSchemaDB.ID.value}
                    JOIN
                        {GTABLES.EQUIPMENT.value} e ON newInterface.{InterfaceSchemaDB.ID_EQUIPMENT.value} = e.{EquipmentSchemaDB.ID.value}
                """
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return ChangeResponse.convert_to_dict(result)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return []

    @staticmethod
    def reset_changes() -> bool:
        """Reset the all changes."""
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                    DELETE FROM
                        {GTABLES.CHANGE.value}
                """
            )
            connection.commit()
            status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return False
        else:
            if status and "DELETE" in status:
                return True
            else:
                return False

    @staticmethod
    def update_assigned(ids: List[int], assigned: str) -> bool:
        """Update operator of an assigned changes.

        Parameters
        ----------
        ids : List[int]
            List of IDs of the changes.
        assigned : str
            Operator's name.
        """
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            query = sql.SQL(
                """
                    UPDATE
                        {table}
                    SET
                        {operator_column} = %s
                    WHERE
                        {id_column} IN ({ids})
                """
            ).format(
                table=sql.Identifier(GTABLES.CHANGE.value),
                operator_column=sql.Identifier(ChangesSchemaDB.OPERATOR.value),
                id_column=sql.Identifier(ChangesSchemaDB.ID.value),
                ids=sql.SQL(',').join(map(sql.Literal, ids))
            )
            cursor.execute(query, (assigned,))
            connection.commit()
            status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return False
        else:
            if status and "UPDATE" in status:
                return True
            else:
                return False

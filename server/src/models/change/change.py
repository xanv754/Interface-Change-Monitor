from typing import List
from psycopg2 import sql
from database import PostgresDatabase, GTABLES, ChangesSchemaDB, EquipmentSchemaDB, InterfaceSchemaDB
from schemas import ChangeInterfaceSchema
from utils import Log, change_to_dict

class Change:
    assigned: str

    def __init__(self, username: str):
        self.assigned = username

    @staticmethod
    def get_all_changes() -> List[ChangeInterfaceSchema]:
        """Get all changes of the system."""
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
            return change_to_dict(result)
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return []

    @staticmethod
    def reset_changes() -> bool:
        """Reset the all changes of the system."""
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
            Log.save(e, __file__, Log.error, console=True)
            return False
        else:
            if status and "DELETE" in status:
                return True
            else:
                return False

    def update_assigned(self, ids: List[int]) -> bool:
        """Update the operator of the assigned of the changes. \n
        Note: Its necessary declare the username operator in the constructor.
        
        Parameters
        ----------
        ids: List[int]
            List of IDs of the changes.
        """
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            query = sql.SQL("""
                UPDATE 
                    {table}
                SET 
                    {operator_column} = %s
                WHERE 
                    {id_column} IN ({ids})
            """).format(
                table=sql.Identifier(GTABLES.CHANGE.value),
                operator_column=sql.Identifier(ChangesSchemaDB.OPERATOR.value),
                id_column=sql.Identifier(ChangesSchemaDB.ID.value),
                ids=sql.SQL(',').join(map(sql.Literal, ids))
            )
            cursor.execute(query, (self.assigned,))
            connection.commit()
            status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            Log.save(e, __file__, Log.error, console=True)
            return False
        else:
            if status and "UPDATE" in status:
                return True
            else:
                return False
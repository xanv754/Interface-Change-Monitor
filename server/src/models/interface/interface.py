from typing import List
from database import PostgresDatabase, GTABLES, InterfaceSchemaDB
from schemas import InterfaceSchema
from utils import interface_to_dict, Log


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

    @staticmethod
    def get_all_by_type(type: str, date: str) -> List[InterfaceSchema]:
        """Get all interfaces filter by type of the interface. \n
        _Note:_ Its necessary declare the id equipment and the ifIndex of the interface in the constructor.

        Parameters
        ----------
        type : str
            Type of the interface.
            - **NEW:** New/Change interface.
            - **OLD:** Old interface.
        date: str
            Date consult of the interface.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""SELECT * FROM {GTABLES.INTERFACE.value} 
                WHERE {InterfaceSchemaDB.INTERFACE_TYPE.value} = %s AND
                {InterfaceSchemaDB.DATE_CONSULT.value} = %s""",
                (type.upper(), date),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return interface_to_dict(result)
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return []

    def get_all_by_date(self) -> List[InterfaceSchema]:
        """Get all interfaces filter by date of consult of the equipment. \n
        _Note:_ Its necessary declare the date of consult in the constructor.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""SELECT * FROM {GTABLES.INTERFACE.value} 
                WHERE {InterfaceSchemaDB.DATE_CONSULT.value} = %s""",
                (self.dateConsult,),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return interface_to_dict(result)
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return []

    def get_by_device_type(self, type: str) -> InterfaceSchema | None:
        """Get an interface filter by type of the interface. \n
        _Note:_ Its necessary declare the id equipment and the ifIndex of the interface in the constructor.

        Parameters
        ----------
        type : str
            Type of the interface.
            - **NEW:** New/Change interface.
            - **OLD:** Old interface.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""SELECT *
                FROM 
                    {GTABLES.INTERFACE.value} 
                WHERE 
                    {InterfaceSchemaDB.ID_EQUIPMENT.value} = %s AND 
                    {InterfaceSchemaDB.IFINDEX.value} = %s AND
                    {InterfaceSchemaDB.INTERFACE_TYPE.value} = %s
                """,
                (self.idEquipment, self.ifIndex, type.upper()),
            )
            result = cursor.fetchone()
            database.close_connection()
            if not result:
                return None
            interface = interface_to_dict([result])
            return interface[0]
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return None
        
    def get_by_equipment_type(self, type: str) -> InterfaceSchema | None:
        """Get an interface filter by equipment, ifIndex and type of the interface. \n
        _Note:_ Its necessary declare the id equipment and the ifIndex of the interface in the constructor.

        Parameters
        ----------
        type : str
            Type of the interface.
            - **NEW:** New/Change interface.
            - **OLD:** Old interface.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""SELECT * FROM {GTABLES.INTERFACE.value} 
                WHERE {InterfaceSchemaDB.ID_EQUIPMENT.value} = %s AND
                {InterfaceSchemaDB.IFINDEX.value} = %s AND
                {InterfaceSchemaDB.INTERFACE_TYPE.value} = %s""",
                (self.idEquipment, self.ifIndex, type.upper()),
            )
            result = cursor.fetchone()
            database.close_connection()
            if not result:
                return None
            interface = interface_to_dict([result])
            return interface[0]
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return None

    def get_by_device_date(self) -> InterfaceSchema | None:
        """Get an interface filter by date of consult of the equipment. \n
        _Note:_ Its necessary declare the id equipment, the ifIndex of the interface and the date of consult in the constructor.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""SELECT * FROM {GTABLES.INTERFACE.value} 
                WHERE {InterfaceSchemaDB.ID_EQUIPMENT.value} = %s AND 
                {InterfaceSchemaDB.IFINDEX.value} = %s AND 
                {InterfaceSchemaDB.DATE_CONSULT.value} = %s""",
                (self.idEquipment, self.ifIndex, self.dateConsult),
            )
            result = cursor.fetchone()
            database.close_connection()
            if not result:
                return None
            interface = interface_to_dict([result])
            return interface[0]
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return None

    def get_by_id(self) -> InterfaceSchema | None:
        """Get info of the interface by ID. \n
        _Note:_ Its necessary declare the ID interface in the constructor.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""SELECT * FROM {GTABLES.INTERFACE.value} 
                WHERE {InterfaceSchemaDB.ID.value} = %s""",
                (self.id,),
            )
            result = cursor.fetchone()
            database.close_connection()
            if not result:
                return None
            interface = interface_to_dict([result])
            return interface[0]
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return None

    def update_type(self, type: str) -> bool:
        """Update type of the interface. \n
        _Note:_ Its necessary declare the ID interface in the constructor.

        Parameters
        ----------
        type : str
            New type of the interface.
            - **NEW:** New/Change interface.
            - **OLD:** Old interface.
        """
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            cursor.execute(
                f"""UPDATE {GTABLES.INTERFACE.value} 
                SET {InterfaceSchemaDB.INTERFACE_TYPE.value} = %s 
                WHERE {InterfaceSchemaDB.ID.value} = %s""",
                (type.upper(), self.id),
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
        """Delete the interface. \n
        _Note:_ Its necessary declare the ID interface in the constructor.
        """
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            cursor.execute(
                f"""DELETE FROM {GTABLES.INTERFACE.value} 
                WHERE {InterfaceSchemaDB.ID.value} = %s""",
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

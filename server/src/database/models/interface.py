from typing import List
from database.entities.interface import InterfaceEntity
from database.constants.date import TypeDate
from database.utils.database import Database

class InterfaceModel:
    @staticmethod
    def get_interface_by_id(id: int) -> InterfaceEntity | None:
        """Obtain an interface by performing a database query.
        
        Parameters
        ----------
        id : int 
            The id of the interface to be obtained.
        """
        database = Database()
        cur = database.get_cursor()
        cur.execute("SELECT * FROM interface WHERE id = %s", (id,))
        res = cur.fetchone()
        database.close_connection()
        if res:
            data = dict(zip(InterfaceEntity.model_fields.keys(), res))
            interface = InterfaceEntity(**data)
            return interface
        else:
            return None
        
    @staticmethod
    def get_interfaces() -> List[InterfaceEntity]:
        """Obtain a list of all interfaces by performing a database query."""
        database = Database()
        cur = database.get_cursor()
        cur.execute("SELECT * FROM interface")
        res = cur.fetchall()
        database.close_connection()
        if res:
            interfaces: List[InterfaceEntity] = []
            for data in res:
                data = dict(zip(InterfaceEntity.model_fields.keys(), data))
                interface = InterfaceEntity(**data)
                interfaces.append(interface)
            return interfaces
        else:
            return []
        
    @staticmethod
    def get_interfaces_by_equipment(id_equipment: int) -> List[InterfaceEntity]:
        """Obtain a list of all interfaces filter by equipment performing a database query.
        
        Parameters
        ----------
        id_equipment : int
            The id of the equipment.
        """
        database = Database()
        cur = database.get_cursor()
        cur.execute("SELECT * FROM interface WHERE idEquipment = %s", (id_equipment,))
        res = cur.fetchall()
        database.close_connection()
        if res:
            interfaces: List[InterfaceEntity] = []
            for data in res:
                data = dict(zip(InterfaceEntity.model_fields.keys(), data))
                interface = InterfaceEntity(**data)
                interfaces.append(interface)
            return interfaces
        else:
            return []
    
    @staticmethod
    def get_interfaces_by_index(id_equipment: int, if_index: int) -> List[InterfaceEntity]:
        """Obtain a list of all interfaces filter by equipment and index performing a database query.
        
        Parameters
        ----------
        id_equipment : int
            The id of the equipment.
        if_index : int
            The index of the interface.
        """
        database = Database()
        cur = database.get_cursor()
        cur.execute("SELECT * FROM interface WHERE idEquipment = %s AND ifIndex = %s", (id_equipment, if_index))
        res = cur.fetchall()
        database.close_connection()
        if res:
            interfaces: List[InterfaceEntity] = []
            for data in res:
                data = dict(zip(InterfaceEntity.model_fields.keys(), data))
                interface = InterfaceEntity(**data)
                interfaces.append(interface)
            return interfaces
        else:
            return []
        
    @staticmethod
    def get_interfaces_by_date_consult(date_consult: str) -> List[InterfaceEntity]:
        """Obtain a list of all interfaces filter by date consult performing a database query.
        
        Parameters
        ----------
        date_consult : str
            The date of the consult in format YYYY-MM-DD.
        """
        database = Database()
        cur = database.get_cursor()
        cur.execute("SELECT * FROM interface WHERE dateConsult = %s", (date_consult,))
        res = cur.fetchall()
        database.close_connection()
        if res:
            interfaces: List[InterfaceEntity] = []
            for data in res:
                data = dict(zip(InterfaceEntity.model_fields.keys(), data))
                interface = InterfaceEntity(**data)
                interfaces.append(interface)
            return interfaces
        else:
            return []
    
    @staticmethod
    def get_interfaces_today() -> List[InterfaceEntity]:
        """Obtain a list of all interfaces filter by date type TODAY performing a database query."""
        database = Database()
        cur = database.get_cursor()
        cur.execute("SELECT * FROM interface WHERE dateType = %s", (TypeDate.TODAY.value,))
        res = cur.fetchall()
        database.close_connection()
        if res:
            interfaces: List[InterfaceEntity] = []
            for data in res:
                data = dict(zip(InterfaceEntity.model_fields.keys(), data))
                interface = InterfaceEntity(**data)
                interfaces.append(interface)
            return interfaces
        else:
            return []
        
    @staticmethod
    def get_interfaces_yesterday() -> List[InterfaceEntity]:
        """Obtain a list of all interfaces filter by date type YESTERDAY performing a database query."""
        database = Database()
        cur = database.get_cursor()
        cur.execute("SELECT * FROM interface WHERE dateType = %s", (TypeDate.YESTERDAY.value,))
        res = cur.fetchall()
        database.close_connection()
        if res:
            interfaces: List[InterfaceEntity] = []
            for data in res:
                data = dict(zip(InterfaceEntity.model_fields.keys(), data))
                interface = InterfaceEntity(**data)
                interfaces.append(interface)
            return interfaces
        else:
            return []
        
    @staticmethod
    def get_interfaces_old() -> List[InterfaceEntity]:
        """Obtain a list of all interfaces filter by date type OLD performing a database query."""
        database = Database()
        cur = database.get_cursor()
        cur.execute("SELECT * FROM interface WHERE dateType = %s", (TypeDate.OLD.value,))
        res = cur.fetchall()
        database.close_connection()
        if res:
            interfaces: List[InterfaceEntity] = []
            for data in res:
                data = dict(zip(InterfaceEntity.model_fields.keys(), data))
                interface = InterfaceEntity(**data)
                interfaces.append(interface)
            return interfaces
        else:
            return []
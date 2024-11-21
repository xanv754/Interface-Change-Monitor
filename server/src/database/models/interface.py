from typing import List
from database.entities.interface import InterfaceEntity
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
from typing import List
from database.entities.equipment import EquipmentEntity
from database.utils.database import Database

class EquipmentModel:
    @staticmethod
    def get_equipment_by_id(id: int) -> EquipmentEntity | None:
        """Obtain an equipment by performing a database query.
        
        Parameters
        ----------
        id : str 
            The ID of the equipment to be obtained.
        """
        database = Database()
        cur = database.get_cursor()
        cur.execute("SELECT * FROM equipment WHERE id = %s", (id,))
        res = cur.fetchone()
        database.close_connection()
        if res:
            data = dict(zip(EquipmentEntity.model_fields.keys(), res))
            equipment = EquipmentEntity(**data)
            return equipment
        else:
            return None
        
    @staticmethod
    def get_equipments() -> List[EquipmentEntity]:
        """Obtain a list of all equipments by performing a database query."""
        database = Database()
        cur = database.get_cursor()
        cur.execute("SELECT * FROM equipment")
        res = cur.fetchall()
        database.close_connection()
        if res:
            equipments: List[EquipmentEntity] = []
            for data in res:
                data = dict(zip(EquipmentEntity.model_fields.keys(), data))
                equipment = EquipmentEntity(**data)
                equipments.append(equipment)
            return equipments
        else:
            return []
        
    @staticmethod
    def get_equipment_by_ip_and_community(ip: str, community: str) -> EquipmentEntity | None:
        """Obtain an equipment by performing a database query.
        
        Parameters
        ----------
        ip : str 
            The IP of the equipment to be obtained.
        community : str 
            The community of the equipment to be obtained.
        """
        database = Database()
        cur = database.get_cursor()
        cur.execute("SELECT * FROM equipment WHERE ip = %s AND community = %s", (ip, community))
        res = cur.fetchone()
        database.close_connection()
        if res:
            data = dict(zip(EquipmentEntity.model_fields.keys(), res))
            equipment = EquipmentEntity(**data)
            return equipment
        else:
            return None
        
    @staticmethod
    def get_equipment_by_sysname(sysname: str) -> List[EquipmentEntity]:
        """Obtain a list of equipments by performing a database query.
        
        Parameters
        ----------
        sysname : str 
            The sysname of the equipment to be obtained.
        """
        database = Database()
        cur = database.get_cursor()
        cur.execute("SELECT * FROM equipment WHERE sysname = %s", (sysname,))
        res = cur.fetchall()
        database.close_connection()
        if res:
            equipments: List[EquipmentEntity] = []
            for data in res:
                data = dict(zip(EquipmentEntity.model_fields.keys(), data))
                equipment = EquipmentEntity(**data)
                equipments.append(equipment)
            return equipments
        else:
            return []
        
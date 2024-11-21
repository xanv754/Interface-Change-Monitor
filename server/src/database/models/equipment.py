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
        
    @staticmethod
    def insert_equipment(data: dict) -> EquipmentEntity | None:
        """Create an equipment by performing a database query.
        
        Parameters
        ----------
        data: dict
            Dict with the values of the equipment to be created.
        """
        new_equipment = EquipmentEntity(**data)
        database = Database()
        conn = database.get_connection()
        cur = database.get_cursor()
        cur.execute("INSERT INTO equipment (ip, community, sysname) VALUES (%s, %s, %s)", (new_equipment.ip, new_equipment.community, new_equipment.sysname))
        res = cur.statusmessage
        if res == "INSERT 0 1":
            conn.commit()
            database.close_connection()
            return EquipmentModel.get_equipment_by_ip_and_community(new_equipment.ip, new_equipment.community)
        else: 
            database.close_connection()
            return None
        
    @staticmethod
    def insert_equipments(data: List[dict]) -> int:
        """Create a list of equipments by performing a database query.
        
        Parameters
        ----------
        data: List[dict]
            List of dicts with the values of the equipments to be created.

        Returns
        -------
        int: The number of inserted equipments.
        """
        total_inserted = 0
        data = [EquipmentEntity(**equipment) for equipment in data]
        database = Database()
        conn = database.get_connection()
        cur = database.get_cursor()
        for equipment in data:
            cur.execute("INSERT INTO equipment (ip, community, sysname) VALUES (%s, %s, %s)", (equipment.ip, equipment.community, equipment.sysname))
            res = cur.statusmessage
            if res == "INSERT 0 1": total_inserted += 1
        conn.commit()
        database.close_connection()
        return total_inserted
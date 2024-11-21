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
        
        
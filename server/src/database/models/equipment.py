from typing import List
from database.entities.equipment import EquipmentEntity
from database.utils.database import Database

class EquipmentModel:
    @staticmethod
    def get_equipment(id: int) -> EquipmentEntity:
        database = Database()
        cur = database.get_cursor()
        cur.execute("SELECT * FROM equipment WHERE id = %s", (id,))
        res = cur.fetchone()
        data = dict(zip(EquipmentEntity.model_fields.keys(), res))
        equipment = EquipmentEntity(**data)
        return equipment
        
        
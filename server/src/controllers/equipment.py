from models.equipment.postgres import EquipmentPostgres
from models.equipment.model import EquipmentModel
from queries.operator import delete


class EquipmentController:
    def get_by_id(self, id: int) -> dict | None:
        model = EquipmentPostgres()
        response = model.get_equipment(id)
        if response:
            return response.model_dump()
        return None
    
    def get_by_info(self, ip: str, community: str) -> dict | None:
        model = EquipmentPostgres()
        response = model.get_equipment_by_info(ip, community)
        if response:
            return response.model_dump()
        return None
    
    def insert(self, data: EquipmentModel) -> dict | None:
        model = EquipmentPostgres()
        response = model.insert(data)
        if response:
            return response.model_dump()
        return None
    
    def update_community(self, id: int, new_community: str) -> dict | None:
        model = EquipmentPostgres()
        response = model.update_community(id, new_community)
        if response:
            return response.model_dump()
        return None
    
    def update_sysname(self, id: int, new_sysname: str) -> dict | None:
        model = EquipmentPostgres()
        response = model.update_sysname(id, new_sysname)
        if response:
            return response.model_dump()
        return None
    
    def delete(self, id: int) -> dict | None:
        model = EquipmentPostgres()
        response = model.delete(id)
        if response:
            return response.model_dump()
        return None

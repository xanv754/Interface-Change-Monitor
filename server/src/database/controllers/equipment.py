from error import ErrorHandler, ErrorEquipmentHandler, CODEEQUIPMENT
from database.models.equipment import EquipmentModel
from database.entities.equipment import EquipmentField
from database.utils import create
from database.utils.json import equipment_to_json

class EquipmentController:
    def read_equipment_by_id(id: int) -> list | ErrorHandler:
        try:
            equipment = EquipmentModel.get_equipment_by_id(id)
            if not equipment:
                return ErrorEquipmentHandler(CODEEQUIPMENT.ERROR_404_EQUIPMENT_NOT_FOUND)
            else:
                return equipment_to_json([equipment])
        except Exception as e:
            error = ErrorEquipmentHandler(CODEEQUIPMENT.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error
        
    def read_equipments() -> list | ErrorHandler:
        try:
            return equipment_to_json(EquipmentModel.get_equipments())
        except Exception as e:
            error = ErrorEquipmentHandler(CODEEQUIPMENT.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error
        
    def read_equipment_by_ip_and_community(ip: str, community: str) -> list | ErrorHandler:
        try:
            equipment = EquipmentModel.get_equipment_by_ip_and_community(ip, community)
            if not equipment:
                return ErrorEquipmentHandler(CODEEQUIPMENT.ERROR_404_EQUIPMENT_NOT_FOUND)
            else:
                return equipment_to_json([equipment])
        except Exception as e:
            error = ErrorEquipmentHandler(CODEEQUIPMENT.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error
        
    def read_equipment_by_sysname(sysname: str) -> list | ErrorHandler:
        try:
            return equipment_to_json(EquipmentModel.get_equipment_by_sysname(sysname))
        except Exception as e:
            error = ErrorEquipmentHandler(CODEEQUIPMENT.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error
    
    def create_equipment(body: dict) -> list | ErrorHandler:
        try:
            if not EquipmentModel.get_equipment_by_ip_and_community(body[EquipmentField.ip.value], body[EquipmentField.community.value]):
                return EquipmentModel.insert_equipment(body)
            else:
                return ErrorEquipmentHandler(CODEEQUIPMENT.ERROR_409_EQUIPMENT_ALREADY_EXISTS)
        except Exception as e:
            error = ErrorEquipmentHandler(CODEEQUIPMENT.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error
        
    def delete_equipment(id: int) -> bool:
        try:
            if not EquipmentModel.get_equipment_by_id(id):
                return ErrorEquipmentHandler(CODEEQUIPMENT.ERROR_404_EQUIPMENT_NOT_FOUND)
            else:
                return EquipmentModel.delete_equipment(id)
        except Exception as e:
            error = ErrorEquipmentHandler(CODEEQUIPMENT.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error
        
    def update_ip_equipment(id: int, ip: str) -> list | ErrorHandler:
        try:
            equipment = EquipmentModel.get_equipment_by_id(id)
            if not equipment:
                return ErrorEquipmentHandler(CODEEQUIPMENT.ERROR_404_EQUIPMENT_NOT_FOUND)
            else:
                return equipment_to_json([EquipmentModel.update_ip_equipment(id, ip)])
        except Exception as e:
            error = ErrorEquipmentHandler(CODEEQUIPMENT.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error
        
    def update_community_equipment(id: int, community: str) -> list | ErrorHandler:
        try:
            equipment = EquipmentModel.get_equipment_by_id(id)
            if not equipment:
                return ErrorEquipmentHandler(CODEEQUIPMENT.ERROR_404_EQUIPMENT_NOT_FOUND)
            else:
                return equipment_to_json([EquipmentModel.update_community_equipment(id, community)])
        except Exception as e:
            error = ErrorEquipmentHandler(CODEEQUIPMENT.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error
        
    def update_sysname_equipment(id: int, sysname: str) -> list | ErrorHandler:
        try:
            equipment = EquipmentModel.get_equipment_by_id(id)
            if not equipment:
                return ErrorEquipmentHandler(CODEEQUIPMENT.ERROR_404_EQUIPMENT_NOT_FOUND)
            else:
                return equipment_to_json([EquipmentModel.update_sysname_equipment(id, sysname)])
        except Exception as e:
            error = ErrorEquipmentHandler(CODEEQUIPMENT.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error
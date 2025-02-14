from typing import List
from models import Equipment, EquipmentModel
from schemas import EquipmentSchema, EquipmentRegisterBody
from utils import Log

class EquipmentController:
    @staticmethod
    def get_equipment(ip: str, community: str) -> EquipmentSchema | None:
        try:
            model = Equipment(ip=ip, community=community)
            return model.get_by_device()
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return None

    @staticmethod
    def register(body: EquipmentRegisterBody) -> bool:
        try:
            model = EquipmentModel(ip=body.ip, community=body.community)
            return model.register()
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return False

    @staticmethod
    def get_all() -> List[EquipmentSchema]:
        try:
            return Equipment.get_all()
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return []

    @staticmethod
    def update_sysname(ip: str, community: str, sysname: str) -> bool:
        try:
            model = Equipment(ip=ip, community=community)
            return model.update_sysname(sysname)
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return False

    @staticmethod
    def update_community(id_equipment: int, community_new: str) -> bool:
        try:
            model = Equipment(id=id_equipment)
            return model.update_community(community_new)
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return False

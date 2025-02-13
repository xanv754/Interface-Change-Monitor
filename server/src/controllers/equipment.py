from typing import List
from models import Equipment, EquipmentModel
from schemas import EquipmentRegisterBody


class EquipmentController:
    @staticmethod
    def get_equipment(ip: str, community: str) -> dict | None:
        try:
            model = Equipment(ip=ip, community=community)
            return model.get_by_device()
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def register(body: EquipmentRegisterBody) -> bool:
        try:
            model = EquipmentModel(ip=body.ip, community=body.community)
            return model.register()
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def get_all() -> List[dict]:
        try:
            model = Equipment.get_all()
            return model
        except Exception as e:
            print(e)
            return []

    @staticmethod
    def update_sysname(ip: str, community: str, sysname: str) -> bool:
        try:
            model = Equipment(ip=ip, community=community)
            return model.update_sysname(sysname)
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def update_community(id_equipment: int, community_new: str) -> bool:
        try:
            model = Equipment(id=id_equipment)
            return model.update_community(community_new)
        except Exception as e:
            print(e)
            return False

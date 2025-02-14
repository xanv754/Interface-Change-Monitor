from typing import List
from models import Equipment, EquipmentModel
from schemas import EquipmentSchema, EquipmentRegisterBody
from utils import Log

class EquipmentController:
    @staticmethod
    def get_equipment(ip: str, community: str) -> EquipmentSchema | None:
        """Obtain an equipment object with all information of the equipment by your IP and community.
        
        Parameters
        ----------
        ip : str
            IP address of the equipment.
        community : str
            Community of the equipment.
        """
        try:
            model = Equipment(ip=ip, community=community)
            return model.get_by_device()
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return None

    @staticmethod
    def get_all() -> List[EquipmentSchema]:
        """Obtain a list of all equipments of the system."""
        try:
            return Equipment.get_all()
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return []

    @staticmethod
    def register(body: EquipmentRegisterBody) -> bool:
        """Register a new equipment in the system.

        Parameters
        ----------
        body : EquipmentRegisterBody
            Data of the new equipment.
        """
        try:
            model = EquipmentModel(ip=body.ip, community=body.community)
            return model.register()
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return False

    @staticmethod
    def update_sysname(ip: str, community: str, sysname: str) -> bool:
        """Update sysname of the equipment in the system.

        Parameters
        ----------
        ip : str
            IP address of the equipment.
        community : str
            Community of the equipment.
        sysname : str
            New sysname of the equipment.
        """
        try:
            model = Equipment(ip=ip, community=community)
            return model.update_sysname(sysname)
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return False

    @staticmethod
    def update_community(id_equipment: int, community_new: str) -> bool:
        """Update community of the equipment in the system.

        Parameters
        ----------
        id_equipment : int
            ID of the equipment.
        community_new : str
            New community of the equipment.
        """
        try:
            model = Equipment(id=id_equipment)
            return model.update_community(community_new)
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return False

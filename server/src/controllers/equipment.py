from typing import List
from models import Equipment, EquipmentModel
from schemas import EquipmentSchema, EquipmentRegisterBody
from utils import Log

class EquipmentController:
    @staticmethod
    def ensure_equipment(ip: str, community: str, sysname: str) -> EquipmentSchema | None:
        """Checks if a equipment exists, if it does not exist, creates it.

        Parameters
        ----------
        ip : str
            IP equipment.
        community : str
            Community equipment.
        sysname : str
            Sysname equipment.

        Returns
        -------
        EquipmentSchema | None
            The requested equipment.
        """
        try:
            equipment = EquipmentController.get_equipment(ip, community)
            if equipment is None:
                new_equipment = EquipmentController.create_and_register(
                    ip=ip,
                    community=community,
                    sysname=sysname,
                )
                if new_equipment is None: return None
                else: return new_equipment
            return equipment
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return None

    @staticmethod
    def create_and_register(ip: str, community: str, sysname: str) -> EquipmentSchema | None:
        """Create a new equipment and register it in the system.

        Parameters
        ----------
        ip : str
            IP equipment.
        community : str
            Community equipment.
        sysname : str
            Sysname equipment.

        Returns
        -------
        EquipmentSchema
            Equipment registered.
        """
        try:
            new_equipment = EquipmentRegisterBody(
                ip=ip,
                community=community,
                sysname=sysname,
            )
            status = EquipmentController.register(new_equipment)
            if not status:
                raise Exception("Failed to register new equipment.")
            equipment = EquipmentController.get_equipment(ip, community)
            return equipment
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return None

    @staticmethod
    def register(body: EquipmentRegisterBody) -> bool:
        """Register a new equipment in the system.

        Parameters
        ----------
        body : EquipmentRegisterBody
            Data of the new equipment.
        """
        try:
            model = EquipmentModel(ip=body.ip, community=body.community, sysname=body.sysname)
            return model.register()
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return False

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
    def get_equipment_by_id(id_equipment: int) -> EquipmentSchema | None:
        """Obtain an equipment object with all information of the equipment by your ID.
        
        Parameters
        ----------
        id_equipment : int
            ID of the equipment.
        """
        try:
            model = Equipment(id=id_equipment)
            return model.get_by_id()
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
            equipment = EquipmentController.get_equipment(ip, community)
            if equipment is None:
                raise Exception(f"Failed to update sysname ({equipment.sysname}) of equipment (IP: {equipment.ip}, Community: {equipment.community}). Equipment not found.")
            if not EquipmentController.check_same_sysname(equipment, sysname):
                model = Equipment(ip=ip, community=community)
                return model.update_sysname(sysname)
            return True
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
            equipment = EquipmentController.get_equipment_by_id(id_equipment)
            if equipment is None:
                raise Exception("Failed to update community of equipment. Equipment not found.")
            model = Equipment(id=id_equipment)
            return model.update_community(community_new)
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return False

    @staticmethod
    def check_same_sysname(equipment: EquipmentSchema, new_sysname: str) -> bool:
        """Check if the sysname of the equipment is the same as the new one. \n
        Return True if the sysname is the same, False otherwise.

        Parameters
        ----------
        ip : str
            IP equipment.
        community : str
            Community equipment.
        new_sysname : str
            New sysname equipment.
        """
        try:
            if equipment.sysname == new_sysname:
                return True
            return False
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return False
from typing import List
from database.models.equipment import EquipmentModel
from schemas.equipment import EquipmentSchema, RegisterEquipmentBody
from utils.log import LogHandler


class EquipmentController:
    """Controller for all operations of equipment table."""

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
            equipment = EquipmentController.get_equipment_device_without_sysname(ip, community)
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
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
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
            new_equipment = RegisterEquipmentBody(
                ip=ip,
                community=community,
                sysname=sysname,
            )
            status = EquipmentController.register(new_equipment)
            if not status:
                raise Exception("Failed to register new equipment.")
            equipment = EquipmentController.get_equipment_device_without_sysname(ip, community)
            return equipment
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return None

    @staticmethod
    def register(body: RegisterEquipmentBody) -> bool:
        """Register a new equipment in the system.

        Parameters
        ----------
        body : EquipmentRegisterBody
            Data of the new equipment.
        """
        try:
            return EquipmentModel.register(body.ip, body.community, body.sysname)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return False

    @staticmethod
    def get_equipment_device_without_sysname(ip: str, community: str) -> EquipmentSchema | None:
        """Obtain an equipment object with all information of the equipment
        by your IP and community.

        Parameters
        ----------
        ip : str
            IP address of the equipment.
        community : str
            Community of the equipment.
        """
        try:
            return EquipmentModel.get_by_info(ip, community)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return None

    @staticmethod
    def get_equipment_device_with_sysname(ip: str, community: str, sysname: str) -> EquipmentSchema | None:
        """Obtain an equipment object with all information of the equipment
        by your IP, community and sysname.

        Parameters
        ----------
        ip : str
            IP address of the equipment.
        community : str
            Community of the equipment.
        sysname: str
            Sysname of the equipment.
        """
        try:
            return EquipmentModel.get_by_info_sysname(ip, community, sysname)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
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
            return EquipmentModel.get_by_id(id_equipment)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return None

    @staticmethod
    def get_all() -> List[EquipmentSchema]:
        """Obtain a list of all equipments of the system."""
        try:
            return EquipmentModel.get_all()
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
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
            equipment = EquipmentController.get_equipment_device_without_sysname(ip, community)
            if equipment is None:
                raise Exception(f"Failed to update sysname ({sysname}) of equipment (IP: {ip}, Community: {community}). Equipment not found.")
            if not EquipmentController.check_same_sysname(equipment, sysname):
                return EquipmentModel.update_sysname(ip, community, sysname)
            return True
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return False

    @staticmethod
    def update_community(id_equipment: int, new_community: str) -> bool:
        """Update community of the equipment in the system.

        Parameters
        ----------
        id_equipment : int
            ID of the equipment.
        new_community : str
            New community of the equipment.
        """
        try:
            equipment = EquipmentController.get_equipment_by_id(id_equipment)
            if equipment is None:
                raise Exception("Failed to update community of equipment. Equipment not found.")
            return EquipmentModel.update_community(id_equipment, new_community)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
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
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return False

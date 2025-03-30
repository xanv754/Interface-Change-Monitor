from typing import List
from controllers.equipment import EquipmentController
from database.models.interface import InterfaceModel
from schemas.equipment import RegisterEquipmentBody
from schemas.interface import InterfaceSchema, RegisterInterfaceBody
from utils.log import LogHandler
from utils.valid import ValidDataHandler


class InterfaceController:
    """Controller for all operations of interface table."""

    @staticmethod
    def register(body: RegisterInterfaceBody) -> bool:
        """Register a new interface in the system.

        Parameters
        ----------
        body : InterfaceRegisterBody
            Data of the new interface.
        """
        try:
            if not ValidDataHandler.status_type(body.ifAdminStatus): raise Exception("Failed to register new interface. Invalid ifAdminStatus")
            if not ValidDataHandler.status_type(body.ifOperStatus): raise Exception("Failed to register new interface. Invalid ifOperStatus")
            equipment = EquipmentController.ensure_equipment(ip=body.ip, community=body.community, sysname=body.sysname)
            if equipment is None: raise Exception(f"Unregistered interface ({body.ifIndex}). Could not be registered because the equipment (IP: {body.ip}, Community: {body.community}) does not exist.")
            EquipmentController.update_sysname(ip=body.ip, community=body.community, sysname=body.sysname)
            return InterfaceModel.register(
                ifIndex=body.ifIndex,
                id_equipment=equipment.id,
                date_consult=body.dateConsult,
                interface_type=body.interfaceType,
                ifName=body.ifName,
                ifDescr=body.ifDescr,
                ifAlias=body.ifAlias,
                ifHighSpeed=body.ifHighSpeed,
                ifOperStatus=body.ifOperStatus,
                ifAdminStatus=body.ifAdminStatus,
            )
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return False

    @staticmethod
    def get_by_id(id: int) -> InterfaceSchema | None:
        """Obtain an interface object with all information of the interface by your ID.

        Parameters
        ----------
        id : int
            ID of the interface.
        """
        try:
            return InterfaceModel.get_by_id(id=id)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return None

    @staticmethod
    def get_by_equipment_type(ip: str, community: str, ifIndex: int, type: str) -> InterfaceSchema | None:
        """Obtain an interface object with all information of the interface
        by your IP and community equipment, ifIndex and type of the interface.

        Parameters
        ----------
        ip : str
            IP address of the equipment.
        community : str
            Community of the equipment.
        ifIndex : int
            ifIndex of the interface.
        type : str
            Type of the interface.
            - **NEW:** New interface.
            - **OLD:** Old interface.
        """
        try:
            if not ValidDataHandler.interface_type(type):
                raise Exception("Failed to get interface by your device. Invalid interface type.")
            equipment = EquipmentController.get_equipment_device_without_sysname(ip, community)
            if equipment is None:
                raise Exception("Failed to get interface by your device. Equipment not found.")
            return InterfaceModel.get_by_equipment_type(ifIndex, equipment.id, type)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return None

    @staticmethod
    def get_by_id_equipment_type(id_equipment: int, ifIndex: int, type: str) -> InterfaceSchema | None:
        """Obtain an interface object with all information of the interface
        by your IP and community equipment, ifIndex and type of the interface.

        Parameters
        ----------
        id_equipment:
            Equipment's ID.
        ifIndex : int
            ifIndex of the interface.
        type : str
            Type of the interface.
            - **NEW:** New interface.
            - **OLD:** Old interface.
        """
        try:
            if not ValidDataHandler.interface_type(type):
                raise Exception("Failed to get interface by your device. Invalid interface type.")
            if not EquipmentController.get_equipment_by_id(id_equipment):
                raise Exception("Failed to get interface by your device. Equipment not found.")
            return InterfaceModel.get_by_equipment_type(ifIndex, id_equipment, type)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return None

    @staticmethod
    def get_all_by_type(type: str, date: str) -> List[InterfaceSchema]:
        """Get all interfaces filter by type of the interface and date.

        Parameters
        ----------
        type : str
            Type of the interface.
            - **NEW:** New interface.
            - **OLD:** Old interface.
        date: str
            Date consult of the interface.
        """
        try:
            if not ValidDataHandler.interface_type(type):
                raise Exception("Failed to get interfaces by an type interface. Invalid interface type (new/old)")
            return InterfaceModel.get_all_by_type(type, date)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return []

    @staticmethod
    def update(id: int, body: RegisterInterfaceBody) -> bool:
        """Update data of an interface in the system.

        Parameters
        ----------
        id : int
            ID of the interface.
        body : InterfaceRegisterBody
            Data of the interface to update.
        """
        try:
            if not ValidDataHandler.status_type(body.ifAdminStatus):
                raise Exception("Failed to update data interface. Invalid interface type (new/old)")
            if not ValidDataHandler.status_type(body.ifOperStatus):
                raise Exception("Failed to update data interface. Invalid ifOperStatus")
            return InterfaceModel.update(
                id=id,
                date_consult=body.dateConsult,
                interface_type=body.interfaceType,
                ifName=body.ifName,
                ifDescr=body.ifDescr,
                ifAlias=body.ifAlias,
                ifHighSpeed=body.ifHighSpeed,
                ifOperStatus=body.ifOperStatus,
                ifAdminStatus=body.ifAdminStatus,
            )
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return False

    @staticmethod
    def update_type(id: int, type: str) -> bool:
        """Update type of the interface in the system.

        Parameters
        ----------
        id : int
            ID of the interface.
        type : str
            New type of the interface.
            - **NEW:** New interface.
            - **OLD:** Old interface.
        """
        try:
            if not ValidDataHandler.interface_type(type): raise Exception("Failed to update type interface of an interface. Invalid interface type (new/old)")
            if not InterfaceModel.get_by_id(id):
                raise Exception("Failed to update type interface of an interface. Interface not found.")
            return InterfaceModel.update_type(id=id, type=type)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return False

from typing import List
from controllers import EquipmentController
from models import Interface, InterfaceModel
from schemas import InterfaceSchema, InterfaceRegisterBody, EquipmentRegisterBody
from utils import is_valid_interface_type, is_valid_status_type, Log


class InterfaceController:
    @staticmethod
    def register(body: InterfaceRegisterBody) -> bool:
        """Register a new interface in the system.

        Parameters
        ----------
        body : InterfaceRegisterBody
            Data of the new interface.
        """
        try:
            if not is_valid_status_type(body.ifAdminStatus): raise Exception("Unregistered interface. Invalid ifAdminStatus")
            if not is_valid_status_type(body.ifOperStatus): raise Exception("Unregistered interface. Invalid ifOperStatus")
            equipment = EquipmentController.ensure_equipment(ip=body.ip, community=body.community, sysname=body.sysname)
            if equipment is None: raise Exception(f"Unregistered interface ({body.ifIndex}). Could not be registered because the equipment (IP: {body.ip}, Community: {body.community}) does not exist.")
            EquipmentController.update_sysname(ip=body.ip, community=body.community, sysname=body.sysname)
            model = InterfaceModel(
                ifIndex=body.ifIndex,
                idEquipment=equipment.id,
                dateConsult=body.dateConsult,
                ifName=body.ifName,
                ifDescr=body.ifDescr,
                ifAlias=body.ifAlias,
                ifSpeed=body.ifSpeed,
                ifHighSpeed=body.ifHighSpeed,
                ifPhysAddress=body.ifPhysAddress,
                ifType=body.ifType,
                ifOperStatus=body.ifOperStatus,
                ifAdminStatus=body.ifAdminStatus,
                ifPromiscuousMode=body.ifPromiscuousMode,
                ifConnectorPresent=body.ifConnectorPresent,
                ifLastCheck=body.ifLastCheck,
            )
            return model.register()
        except Exception as e:
            Log.save(e, __file__, Log.error)
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
            model = Interface(id=id)
            return model.get_by_id()
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return None

    @staticmethod
    def get_by_device_type(
        ip: str, community: str, ifIndex: int, type: str
    ) -> InterfaceSchema | None:
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
            - **NEW:** New/Change interface.
            - **OLD:** Old interface.
        """
        try:
            if not is_valid_interface_type(type):
                return None
            equipment = EquipmentController.get_equipment(ip, community)
            if equipment is None:
                return None
            model = Interface(idEquipment=equipment.id, ifIndex=ifIndex)
            return model.get_by_device_type(type)
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return None

    @staticmethod
    def get_all_by_type(type: str) -> List[InterfaceSchema]:
        """Get all interfaces filter by type of the interface.

        Parameters
        ----------
        type : str
            Type of the interface.
            - **NEW:** New/Change interface.
            - **OLD:** Old interface.
        """
        try:
            if not is_valid_interface_type(type): raise Exception("Interfaces not found. Invalid interface type (new/old)")
            return Interface.get_all_by_type(type)
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return []
        
    @staticmethod
    def get_by_equipment_type(id_equipment: int, ifIndex: int, type: str) -> InterfaceSchema | None:
        """Get an interface filter by equipment, ifIndex and type of the interface.

        Parameters
        ----------
        id_equipment : int
            ID of the equipment.
        ifIndex : int
            ifIndex of the interface.
        type : str
            Type of the interface.
            - **NEW:** New/Change interface.
            - **OLD:** Old interface.
        """
        try:
            if not is_valid_interface_type(type): raise Exception("Interface not found. Invalid interface type (new/old)")
            model = Interface(idEquipment=id_equipment, ifIndex=ifIndex)
            return model.get_by_equipment_type(type)
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return None

    @staticmethod
    def update(id: int, body: InterfaceRegisterBody) -> bool:
        """Update data of an interface in the system.

        Parameters
        ----------
        id : int
            ID of the interface.
        body : InterfaceRegisterBody
            Data of the interface to update.
        """
        try:
            if not is_valid_status_type(body.ifAdminStatus): raise Exception("Interface not updated. Invalid ifAdminStatus")
            if not is_valid_status_type(body.ifOperStatus): raise Exception("Interface not updated. Invalid ifOperStatus")
            model = InterfaceModel(
                id=id,
                dateConsult=body.dateConsult,
                ifName=body.ifName,
                ifDescr=body.ifDescr,
                ifAlias=body.ifAlias,
                ifSpeed=body.ifSpeed,
                ifHighSpeed=body.ifHighSpeed,
                ifPhysAddress=body.ifPhysAddress,
                ifType=body.ifType,
                ifOperStatus=body.ifOperStatus,
                ifAdminStatus=body.ifAdminStatus,
                ifPromiscuousMode=body.ifPromiscuousMode,
                ifConnectorPresent=body.ifConnectorPresent,
                ifLastCheck=body.ifLastCheck,
            )
            return model.update()
        except Exception as e:
            Log.save(e, __file__, Log.error)
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
            - **NEW:** New/Change interface.
            - **OLD:** Old interface.
        """
        try:
            if not is_valid_interface_type(type): raise Exception("Interface not updated. Invalid interface type (new/old)")
            model = Interface(id=id)
            if not model.get_by_id(): raise Exception("Interface not updated. Interface not found.")
            return model.update_type(type)
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return False

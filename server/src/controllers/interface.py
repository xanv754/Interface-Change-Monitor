from controllers import EquipmentController
from models import Interface, InterfaceModel
from schemas import InterfaceSchema, InterfaceRegisterBody
from utils import is_valid_interface_type, is_valid_status_type, Log


class InterfaceController:
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
    def register(body: InterfaceRegisterBody) -> bool:
        """Register a new interface in the system.

        Parameters
        ----------
        body : InterfaceRegisterBody
            Data of the new interface.
        """
        try:
            if not is_valid_status_type(body.ifAdminStatus):
                return False
            if not is_valid_status_type(body.ifOperStatus):
                return False
            equipment = EquipmentController.get_equipment(body.ip, body.community)
            if equipment is None:
                return False
            if equipment.sysname != body.sysname:
                EquipmentController.update_sysname(
                    body.ip, body.community, body.sysname
                )
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
            if not is_valid_status_type(body.ifAdminStatus):
                return False
            if not is_valid_status_type(body.ifOperStatus):
                return False
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
            if not is_valid_interface_type(type):
                return False
            model = Interface(id=id)
            if not model.get_by_id():
                return False
            return model.update_type(type)
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return False

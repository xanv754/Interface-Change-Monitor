from controllers import EquipmentController
from database import EquipmentSchema
from models import Interface, InterfaceModel
from schemas import InterfaceRegisterBody
from utils import is_valid_interface_type, is_valid_status_type


class InterfaceController:
    @staticmethod
    def get_by_id(id: int) -> dict | None:
        try:
            model = Interface(id=id)
            return model.get_by_id()
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def get_by_device_type(
        ip: str, community: str, ifIndex: int, type: str
    ) -> dict | None:
        try:
            if not is_valid_interface_type(type):
                return None
            equipment = EquipmentController.get_equipment(ip, community)
            if equipment is None:
                return None
            id_equipment = equipment[EquipmentSchema.ID.value]
            model = Interface(idEquipment=id_equipment, ifIndex=ifIndex)
            return model.get_by_device_type(type)
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def register(body: InterfaceRegisterBody) -> bool:
        try:
            if not is_valid_status_type(body.ifAdminStatus):
                return False
            if not is_valid_status_type(body.ifOperStatus):
                return False
            equipment = EquipmentController.get_equipment(body.ip, body.community)
            if equipment is None:
                return False
            id_equipment = equipment[EquipmentSchema.ID.value]
            sysname = equipment[EquipmentSchema.SYSNAME.value]
            if sysname != body.sysname:
                EquipmentController.update_sysname(
                    body.ip, body.community, body.sysname
                )
            model = InterfaceModel(
                ifIndex=body.ifIndex,
                idEquipment=id_equipment,
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
            print(e)
            return False

    @staticmethod
    def update(id: int, body: InterfaceRegisterBody) -> bool:
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
            print(e)
            return False

    @staticmethod
    def update_type(id: int, type: str) -> bool:
        try:
            if not is_valid_interface_type(type):
                return False
            model = Interface(id=id)
            if not model.get_by_id():
                return False
            return model.update_type(type)
        except Exception as e:
            print(e)
            return False

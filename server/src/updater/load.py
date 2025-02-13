from datetime import datetime, timedelta
from constants import InterfaceType
from controllers import InterfaceController
from schemas import InterfaceSchema, InterfaceRegisterBody

DATE = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")


class UpdaterDatabase:
    _instance: "UpdaterDatabase | None" = None
    interface: InterfaceRegisterBody

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, data: list):
        if not len(data) == 16:
            raise Exception("Data not valid")
        new_interface = InterfaceRegisterBody(
            dateConsult=DATE,
            interfaceType=InterfaceType.NEW.value,
            ip=data[0],
            community=data[1],
            sysname=data[2],
            ifIndex=int(data[3]),
            ifName=data[4],
            ifDescr=data[5],
            ifAlias=data[6],
            ifSpeed=int(data[7]),
            ifHighSpeed=int(data[8]),
            ifPhysAddress=data[9],
            ifType=data[10],
            ifOperStatus=data[11],
            ifAdminStatus=data[12],
            ifPromiscuousMode=data[13],
            ifConnectorPresent=data[14],
            ifLastCheck=data[15],
        )
        self.interface = new_interface

    def get_interface(self) -> dict:
        return self.interface

    def update(self) -> None:
        interface_db = self._check_interface_exists()
        if not interface_db:
            InterfaceController.register(self.interface)
            return
        same_interfaces = self._compare_interfaces(interface_db)
        if same_interfaces:
            return
        old_interface_db = InterfaceController.get_by_device_type(
            self.interface.ip,
            self.interface.community,
            self.interface.ifIndex,
            InterfaceType.OLD.value,
        )
        if not old_interface_db:
            InterfaceController.update_type(interface_db.id, InterfaceType.OLD.value)
            InterfaceController.register(self.interface)
            # TODO: add interface to change table
            return
        else:
            InterfaceController.update(
                old_interface_db.id,
                InterfaceRegisterBody(
                    dateConsult=interface_db.date,
                    interfaceType=InterfaceType.OLD.value,
                    ip=self.interface.ip,
                    community=self.interface.community,
                    sysname=self.interface.sysname,
                    ifIndex=self.interface.ifIndex,
                    ifName=interface_db.ifName,
                    ifDescr=interface_db.ifDescr,
                    ifAlias=interface_db.ifAlias,
                    ifSpeed=interface_db.ifSpeed,
                    ifHighSpeed=interface_db.ifHighSpeed,
                    ifPhysAddress=interface_db.ifPhysAddress,
                    ifType=interface_db.ifType,
                    ifOperStatus=interface_db.ifOperStatus,
                    ifAdminStatus=interface_db.ifAdminStatus,
                    ifPromiscuousMode=interface_db.ifPromiscuousMode,
                    ifConnectorPresent=interface_db.ifConnectorPresent,
                    ifLastCheck=interface_db.ifLastCheck
                ),
            )
            InterfaceController.update(interface_db.id, self.interface)
            # TODO: If the interface is not assigned, add interface to change table
            return

    def _check_interface_exists(self) -> InterfaceSchema | None:
        interface = InterfaceController.get_by_device_type(
            ip=self.interface.ip,
            community=self.interface.community,
            ifIndex=self.interface.ifIndex,
            type=InterfaceType.NEW.value,
        )
        return interface

    def _compare_interfaces(self, interface_db: InterfaceSchema) -> bool:
        """Comparte two interfaces to see if they are the same."""
        if self.interface.ifName != interface_db.ifName:
            return False
        if self.interface.ifDescr != interface_db.ifDescr:
            return False
        if self.interface.ifAlias != interface_db.ifAlias:
            return False
        if self.interface.ifHighSpeed != interface_db.ifHighSpeed:
            return False
        if self.interface.ifOperStatus != interface_db.ifOperStatus:
            return False
        if self.interface.ifAdminStatus != interface_db.ifAdminStatus:
            return False
        return True

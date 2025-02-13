from datetime import datetime, timedelta
from constants import InterfaceType
from controllers import InterfaceController
from models import InterfaceRegisterBody
from schemas import InterfaceSchema

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
            InterfaceController.update_type(
                interface_db[InterfaceSchema.ID.value], InterfaceType.OLD.value
            )
            InterfaceController.register(self.interface)
            # TODO: add interface to change table
            return
        else:
            InterfaceController.update(
                old_interface_db[InterfaceSchema.ID.value],
                InterfaceRegisterBody(
                    dateConsult=interface_db[InterfaceSchema.DATE_CONSULT.value],
                    interfaceType=InterfaceType.OLD.value,
                    ip=self.interface.ip,
                    community=self.interface.community,
                    sysname=self.interface.sysname,
                    ifIndex=self.interface.ifIndex,
                    ifName=interface_db[InterfaceSchema.IFNAME.value],
                    ifDescr=interface_db[InterfaceSchema.IFDESCR.value],
                    ifAlias=interface_db[InterfaceSchema.IFALIAS.value],
                    ifSpeed=interface_db[InterfaceSchema.IFSPEED.value],
                    ifHighSpeed=interface_db[InterfaceSchema.IFHIGHSPEED.value],
                    ifPhysAddress=interface_db[InterfaceSchema.IFPHYSADDRESS.value],
                    ifType=interface_db[InterfaceSchema.IFTYPE.value],
                    ifOperStatus=interface_db[InterfaceSchema.IFOPERSTATUS.value],
                    ifAdminStatus=interface_db[InterfaceSchema.IFADMINSTATUS.value],
                    ifPromiscuousMode=interface_db[
                        InterfaceSchema.IFPROMISCUOUSMODE.value
                    ],
                    ifConnectorPresent=interface_db[
                        InterfaceSchema.IFCONNECTORPRESENT.value
                    ],
                    ifLastCheck=interface_db[InterfaceSchema.IFLASTCHECK.value],
                ),
            )
            InterfaceController.update(
                interface_db[InterfaceSchema.ID.value], self.interface
            )
            # TODO: If the interface is not assigned, add interface to change table
            return

    def _check_interface_exists(self) -> dict | None:
        interface = InterfaceController.get_by_device_type(
            ip=self.interface.ip,
            community=self.interface.community,
            ifIndex=self.interface.ifIndex,
            type=InterfaceType.NEW.value,
        )
        return interface

    def _compare_interfaces(self, interface_db: dict) -> bool:
        """Comparte two interfaces to see if they are the same."""
        if self.interface.ifName != interface_db[InterfaceSchema.IFNAME.value]:
            return False
        if self.interface.ifDescr != interface_db[InterfaceSchema.IFDESCR.value]:
            return False
        if self.interface.ifAlias != interface_db[InterfaceSchema.IFALIAS.value]:
            return False
        if (
            self.interface.ifHighSpeed
            != interface_db[InterfaceSchema.IFHIGHSPEED.value]
        ):
            return False
        if (
            self.interface.ifOperStatus
            != interface_db[InterfaceSchema.IFOPERSTATUS.value]
        ):
            return False
        if (
            self.interface.ifAdminStatus
            != interface_db[InterfaceSchema.IFADMINSTATUS.value]
        ):
            return False
        # if self.interface.ifSpeed != interface_db[InterfaceSchema.IFSPEED.value]: return False
        # if self.interface.ifPhysAddress != interface_db[InterfaceSchema.IFPHYSADDRESS.value]: return False
        # if self.interface.ifType != interface_db[InterfaceSchema.IFTYPE.value]: return False
        # if self.interface.ifPromiscuousMode != interface_db[InterfaceSchema.IFPROMISCUOUSMODE.value]: return False
        # if self.interface.ifConnectorPresent != interface_db[InterfaceSchema.IFCONNECTORPRESENT.value]: return False
        # if self.interface.ifLastCheck != interface_db[InterfaceSchema.IFLASTCHECK.value]: return False
        return True

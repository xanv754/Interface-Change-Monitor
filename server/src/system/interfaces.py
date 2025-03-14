from constants import InterfaceType
from controllers import InterfaceController, EquipmentController
from schemas import InterfaceSchema, RegisterInterfaceBody
from utils import Log


class UpdaterInterfaces:
    _instance: "UpdaterInterfaces | None" = None
    interface: RegisterInterfaceBody

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, data: RegisterInterfaceBody):
        try:
            self.interface = data
        except Exception as e:
            Log.save(e, __file__, Log.error, console=True)

    def get_interface(self) -> RegisterInterfaceBody:
        """Get the interface consult to be registered."""
        return self.interface

    def update(self) -> None:
        """Update the consult SNMP of an interface in the database."""
        try:
            interface_db = self._get_interface_exists()
            if not interface_db:
                self._register_new_interface()
                return
            self._update_sysname()
            same_interfaces = self._check_same_interfaces(interface_db=interface_db)
            if not same_interfaces:
                old_interface_db = self._get_old_version_interface()
                if not old_interface_db:
                    self._change_interface_type_from_new_to_old(id_new_interface=interface_db.id)
                    self._register_new_interface()
                    # TODO: add interface to change table
                else:
                    self._move_new_interface_to_old_interface(id_old_interface=old_interface_db.id, new_interface=interface_db)
                    self._load_new_data_to_new_interface(id_new_interface=interface_db.id)
                    # TODO: If the interface is not assigned, add interface to change table
        except Exception as e:
            Log.save(e, __file__, Log.error)

    def _get_interface_exists(self) -> InterfaceSchema | None:
        """Check if the interface exists in the database.
        If the interface exists, return the interface.
        If the interface does not exist, return None.
        """
        interface = InterfaceController.get_by_device_type(
            ip=self.interface.ip,
            community=self.interface.community,
            ifIndex=self.interface.ifIndex,
            type=InterfaceType.NEW.value,
        )
        return interface

    def _check_same_interfaces(self, interface_db: InterfaceSchema) -> bool:
        """Comparte two interfaces to see if they are the same.
        If they are the same, return True.
        """
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

    def _register_new_interface(self) -> None:
        """Register a new interface in the database."""
        try:
            InterfaceController.register(self.interface)
            Log.save("New interface registered", __file__, Log.info)
        except Exception as e:
            Log.save(e, __file__, Log.error)

    def _update_sysname(self) -> None:
        """Update the sysname of the equipment in the database."""
        EquipmentController.update_sysname(
            ip=self.interface.ip,
            community=self.interface.community,
            sysname=self.interface.sysname,
        )
        Log.save(f"Update sysname ({self.interface.sysname}) of equipment (IP: {self.interface.ip}, Community: {self.interface.community})", __file__, Log.info)

    def _get_old_version_interface(self) -> InterfaceSchema | None:
        old_interface_db = InterfaceController.get_by_device_type(
            self.interface.ip,
            self.interface.community,
            self.interface.ifIndex,
            InterfaceType.OLD.value,
        )
        return old_interface_db

    def _change_interface_type_from_new_to_old(self, id_new_interface: int) -> None:
        """Update the type of the interface from new to old."""
        try:
            InterfaceController.update_type(
                id_new_interface, InterfaceType.OLD.value
            )
        except Exception as e:
            Log.save(f"Failed to move new interface to old interface. {e}", __file__, Log.error)

    def _move_new_interface_to_old_interface(self, id_old_interface: int, new_interface: InterfaceSchema) -> None:
        try:
            InterfaceController.update(
                id=id_old_interface,
                body=RegisterInterfaceBody(
                    dateConsult=new_interface.date,
                    interfaceType=InterfaceType.OLD.value,
                    ip=self.interface.ip,
                    community=self.interface.community,
                    sysname=self.interface.sysname,
                    ifIndex=self.interface.ifIndex,
                    ifName=new_interface.ifName,
                    ifDescr=new_interface.ifDescr,
                    ifAlias=new_interface.ifAlias,
                    ifHighSpeed=new_interface.ifHighSpeed,
                    ifOperStatus=new_interface.ifOperStatus,
                    ifAdminStatus=new_interface.ifAdminStatus,
                ),
            )
        except Exception as e:
            Log.save(f"Failed to move new interface to old interface. {e}", __file__, Log.error)

    def _load_new_data_to_new_interface(self, id_new_interface: int) -> None:
        """Load the new data to the new interface."""
        try:
            InterfaceController.update(id=id_new_interface, body=self.interface)
        except Exception as e:
            Log.save(f"Failed to load new data to new interface. {e}", __file__, Log.error)

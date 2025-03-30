from constants.types import InterfaceType
from controllers.interface import InterfaceController
from controllers.equipment import EquipmentController
from schemas.interface import InterfaceSchema, RegisterInterfaceBody
from utils.log import LogHandler


class UpdaterInterfaceHandler:
    """Handler to update data of consulted interfaces in the database."""

    __instance: "UpdaterInterfaceHandler | None" = None
    __interface: RegisterInterfaceBody

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, data: RegisterInterfaceBody):
        self.__interface = data

    def __confirm_existence(self) -> InterfaceSchema | None:
        """Obtained the information about interface if this exists in the database."""
        interface = InterfaceController.get_by_equipment_type(
            ip=self.__interface.ip,
            community=self.__interface.community,
            ifIndex=self.__interface.ifIndex,
            type=InterfaceType.NEW.value,
        )
        return interface

    def __compare_information(self, interface_db: InterfaceSchema) -> bool:
        """Compares if two interfaces are the same"""
        if self.__interface.ifName != interface_db.ifName:
            return False
        if self.__interface.ifDescr != interface_db.ifDescr:
            return False
        if self.__interface.ifAlias != interface_db.ifAlias:
            return False
        if self.__interface.ifHighSpeed != interface_db.ifHighSpeed:
            return False
        if self.__interface.ifOperStatus != interface_db.ifOperStatus:
            return False
        if self.__interface.ifAdminStatus != interface_db.ifAdminStatus:
            return False
        return True

    def __register_new(self) -> None:
        """Register a new interface in the database."""
        try:
            InterfaceController.register(self.__interface)
            LogHandler(content="New interface registered", path=__file__, info=True)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)

    def __update_sysname(self) -> None:
        """Update the sysname of the equipment in the database."""
        EquipmentController.update_sysname(
            ip=self.__interface.ip,
            community=self.__interface.community,
            sysname=self.__interface.sysname,
        )
        LogHandler(content=f"Update sysname ({self.__interface.sysname}) of equipment (IP: {self.__interface.ip}, Community: {self.__interface.community})", path=__file__, info=True)

    def __get_old_version(self) -> InterfaceSchema | None:
        old_interface_db = InterfaceController.get_by_equipment_type(
            self.__interface.ip,
            self.__interface.community,
            self.__interface.ifIndex,
            InterfaceType.OLD.value,
        )
        return old_interface_db

    def __update_type_new_to_old(self, id_stored_interface: int) -> None:
        """Update the type of the interface from new to old."""
        try:
            InterfaceController.update_type(
                id_stored_interface, InterfaceType.OLD.value
            )
        except Exception as e:
            LogHandler(content=f"Failed to move new interface to old interface. {e}", path=__file__, err=True)

    def __transfer_data_new_to_old(self, id_stored_old: int, stored_new: InterfaceSchema) -> None:
        try:
            InterfaceController.update(
                id=id_stored_old,
                body=RegisterInterfaceBody(
                    dateConsult=stored_new.date,
                    interfaceType=InterfaceType.OLD.value,
                    ip=self.__interface.ip,
                    community=self.__interface.community,
                    sysname=self.__interface.sysname,
                    ifIndex=self.__interface.ifIndex,
                    ifName=stored_new.ifName,
                    ifDescr=stored_new.ifDescr,
                    ifAlias=stored_new.ifAlias,
                    ifHighSpeed=stored_new.ifHighSpeed,
                    ifOperStatus=stored_new.ifOperStatus,
                    ifAdminStatus=stored_new.ifAdminStatus,
                ),
            )
        except Exception as e:
            LogHandler(content=f"Failed to move new interface to old interface. {e}", path=__file__, err=True)

    def __update_data_new(self, stored_new: int) -> None:
        """Update the data of type new version interface."""
        try:
            InterfaceController.update(id=stored_new, body=self.__interface)
        except Exception as e:
            LogHandler(content=f"Failed to load new data to new interface. {e}", path=__file__, err=True)

    def get_interface(self) -> RegisterInterfaceBody:
        """Get the interface consult to be registered."""
        return self.__interface

    def update(self) -> None:
        """Update the consult SNMP of an interface in the database."""
        try:
            interface_db = self.__confirm_existence()
            if not interface_db:
                self.__register_new()
                return
            self.__update_sysname()
            same_interfaces = self.__compare_information(interface_db=interface_db)
            if not same_interfaces:
                old_interface_db = self.__get_old_version()
                if not old_interface_db:
                    self.__update_type_new_to_old(id_stored_interface=interface_db.id)
                    self.__register_new()
                    # TODO: add interface to change table
                else:
                    self.__transfer_data_new_to_old(id_stored_old=old_interface_db.id, stored_new=interface_db)
                    self.__update_data_new(stored_new=interface_db.id)
                    # TODO: If the interface is not assigned, add interface to change table
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)

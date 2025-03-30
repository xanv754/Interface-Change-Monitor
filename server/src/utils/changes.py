from typing import List
from datetime import datetime, timedelta
from manager.setting import SettingHandler
from constants.types import InterfaceType
from controllers.interface import InterfaceController
from controllers.change import ChangeController
from schemas.config import SettingSchema
from schemas.interface import InterfaceSchema
from schemas.change import RegisterChangeBody
from utils.log import LogHandler


class ChangeDetector:
    """Change detector between interfaces in the database."""

    __settings: SettingSchema

    def __init__(self):
        settings = SettingHandler()
        self.__settings = settings.get_settings()

    def __create_change_model(self, old_interface: InterfaceSchema, new_interface: InterfaceSchema) -> RegisterChangeBody:
        """Create a new change model."""
        return RegisterChangeBody(
            oldInterface=old_interface.id,
            newInterface=new_interface.id,
        )

    def __get_new_interfaces(self, date: str | None = None) -> List[InterfaceSchema]:
        """Get all interfaces of type new version."""
        if not date: date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        interface_type = InterfaceType.NEW.value
        interfaces = InterfaceController.get_all_by_type(interface_type, date)
        return interfaces

    def __get_old_version_interface(self, new_version: InterfaceSchema) -> InterfaceSchema | None:
        """Get the old version of an interface."""
        old_version: InterfaceSchema | None = InterfaceController.get_by_id_equipment_type(
            id_equipment=new_version.equipment,
            ifIndex=new_version.ifIndex,
            type=InterfaceType.OLD.value
        )
        return old_version

    def __compare_interfaces(
            self,
            old_interface: InterfaceSchema,
            new_interface: InterfaceSchema
        ) -> bool:
        """Compare two interfaces and return True if they are different."""
        if self.__settings.notificationChanges.ifName:
            if old_interface.ifName != new_interface.ifName:
                return True
        if self.__settings.notificationChanges.ifDescr:
            if old_interface.ifDescr != new_interface.ifDescr:
                return True
        if self.__settings.notificationChanges.ifAlias:
            if old_interface.ifAlias != new_interface.ifAlias:
                return True
        if self.__settings.notificationChanges.ifHighSpeed:
            if old_interface.ifHighSpeed != new_interface.ifHighSpeed:
                return True
        if self.__settings.notificationChanges.ifOperStatus:
            if old_interface.ifOperStatus != new_interface.ifOperStatus:
                return True
        if self.__settings.notificationChanges.ifAdminStatus:
            if old_interface.ifAdminStatus != new_interface.ifAdminStatus:
                return True
        return False

    def get_interfaces_with_changes(self, date: str | None = None) -> List[RegisterChangeBody]:
        """Get all a list of changes between interfaces.

        Parameters
        ----------
        date : str
            Day of consultation of the interfaces to detect changes. Default day is yesterday.
        """
        changes: List[RegisterChangeBody] = []
        if date: new_interfaces = self.__get_new_interfaces(date=date)
        else: new_interfaces = self.__get_new_interfaces()
        for new_interface in new_interfaces:
            old_interface = self.__get_old_version_interface(new_interface)
            if old_interface is None: continue
            status_diferrences = self.__compare_interfaces(
                old_interface=old_interface,
                new_interface=new_interface
            )
            if status_diferrences:
                new_change = self.__create_change_model(
                    old_interface=old_interface,
                    new_interface=new_interface
                )
                changes.append(new_change)
        return changes

    def inspect_interfaces(self, date: str | None = None) -> int:
        """Inspects all database interfaces for changes between them.

        Parameters
        ----------
        date: str
            Date of the changes.

        Returns
        -------
        int
            The number of process status.
            - **0:** No changes. Finished correctly.
            - **1:** Changes detected. Finished correctly.
            - **2:** Failed to register new change. Finished with errors.
            - **3:** Failed to detect changes. Load incomplete. Finished with errors.
        """
        try:
            status = 0
            changes = self.get_interfaces_with_changes(date=date)
            ChangeController.delete()
            if changes:
                status = ChangeController.register(changes=changes)
                if status: status = 1
                else: status = 2
            return status
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return 3

from typing import List
from datetime import datetime, timedelta
from core import SystemConfig
from constants import InterfaceType
from controllers import InterfaceController, EquipmentController, SystemController
from schemas import InterfaceResponseSchema, EquipmentResponseSchema, ChangesResponse, OldInterfaceSchema, NewInterfaceSchema
from utils import Log

class DetectChanges:
    """Detect changes between interfaces in the database."""
    _old_interface: InterfaceResponseSchema
    _new_interface: InterfaceResponseSchema
    system: SystemConfig

    def __init__(self, old_interface: InterfaceResponseSchema | None = None, new_interface: InterfaceResponseSchema | None = None):
        self.system = SystemConfig()
        self._old_interface = old_interface
        self._new_interface = new_interface

    def _create_new_change(self, equipment: EquipmentResponseSchema, old_interface: InterfaceResponseSchema, new_interface: InterfaceResponseSchema) -> ChangesResponse:
        """Create a new change."""
        old_change_interface = OldInterfaceSchema(
            id=old_interface.id,
            date=old_interface.date,
            ifName=old_interface.ifName,
            ifDescr=old_interface.ifDescr,
            ifAlias=old_interface.ifAlias,
            ifHighSpeed=old_interface.ifHighSpeed,
            ifOperStatus=old_interface.ifOperStatus,
            ifAdminStatus=old_interface.ifAdminStatus,
        )
        new_change_interface = NewInterfaceSchema(
            id=new_interface.id,
            date=new_interface.date,
            ifName=new_interface.ifName,
            ifDescr=new_interface.ifDescr,
            ifAlias=new_interface.ifAlias,
            ifHighSpeed=new_interface.ifHighSpeed,
            ifOperStatus=new_interface.ifOperStatus,
            ifAdminStatus=new_interface.ifAdminStatus,
        )
        new_change = ChangesResponse(
            id=equipment.id,
            ip=equipment.ip,
            community=equipment.community,
            sysname=equipment.sysname,
            ifIndex=new_interface.ifIndex,
            oldInterface=old_change_interface,
            newInterface=new_change_interface,
            assigned=False
        )
        return new_change

    def _get_equipment(self, id_equipment: int) -> EquipmentResponseSchema | None:
        """Get the equipment."""
        equipment = EquipmentController.get_equipment_by_id(id_equipment)
        return equipment

    def _get_new_interfaces(self, date: str | None = None) -> List[InterfaceResponseSchema]:
        """Get the new interfaces."""
        # if not date: date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        if not date: date = datetime.now().strftime("%Y-%m-%d")
        interface_type = InterfaceType.NEW.value
        interfaces = InterfaceController.get_all_by_type(interface_type, date)
        return interfaces

    def _get_old_version_interface(self, new_interface: InterfaceResponseSchema) -> InterfaceResponseSchema | None:
        """Get the old version of the interface."""
        old_interface_version = InterfaceController.get_by_equipment_type(
            id_equipment=new_interface.equipment,
            ifIndex=new_interface.ifIndex,
            type=InterfaceType.OLD.value
        )
        return old_interface_version

    def _compare_interfaces(
            self,
            old_interface: InterfaceResponseSchema | None = None,
            new_interface: InterfaceResponseSchema | None = None
        ) -> bool:
        """Compare interfaces and return True if they are different."""
        if old_interface is None:
            old_interface = self._old_interface
        if new_interface is None:
            new_interface = self._new_interface
        if self.system.configuration.notificationChanges.ifName:
            if old_interface.ifName != new_interface.ifName:
                return True
        if self.system.configuration.notificationChanges.ifDescr:
            if old_interface.ifDescr != new_interface.ifDescr:
                return True
        if self.system.configuration.notificationChanges.ifAlias:
            if old_interface.ifAlias != new_interface.ifAlias:
                return True
        if self.system.configuration.notificationChanges.ifHighSpeed:
            if old_interface.ifHighSpeed != new_interface.ifHighSpeed:
                return True
        if self.system.configuration.notificationChanges.ifOperStatus:
            if old_interface.ifOperStatus != new_interface.ifOperStatus:
                return True
        if self.system.configuration.notificationChanges.ifAdminStatus:
            if old_interface.ifAdminStatus != new_interface.ifAdminStatus:
                return True
        return False

    def _get_changes(self, date: str | None = None) -> List[ChangesResponse]:
        """Get all changes between interfaces."""

        changes: List[ChangesResponse] = []
        if date: new_interfaces = self._get_new_interfaces(date=date)
        else: new_interfaces = self._get_new_interfaces()
        for new_interface in new_interfaces:
            old_interface = self._get_old_version_interface(new_interface)
            if old_interface is None: continue
            status_diferrences = self._compare_interfaces(
                old_interface=old_interface,
                new_interface=new_interface
            )
            if status_diferrences:
                equipment = self._get_equipment(new_interface.equipment)
                new_change = self._create_new_change(
                    equipment=equipment,
                    old_interface=old_interface,
                    new_interface=new_interface
                )
                changes.append(new_change)
        return changes

    def detect_changes(self, date: str | None = None) -> int:
        """Detect changes between interfaces in the database.

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
            changes = self._get_changes(date=date)
            SystemController.delete_changes()
            if changes:
                for change in changes:
                    status = SystemController.register_change(changes=change)
                    if not status:
                        Log.save(
                            f"Failed to register new change (IP: {change.ip}, Community: {change.community}, Sysname: {change.sysname}, IfIndex: {change.ifIndex})",
                            __file__,
                            Log.error
                        )
                        status = 2
                if status == 0: status = 1
            return status
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return 3

from typing import List
from core import SystemConfig
from constants import InterfaceType
from controllers import InterfaceController, EquipmentController
from schemas import InterfaceSchema, EquipmentSchema, ChangesSchema, OldInterfaceSchema, NewInterfaceSchema

class DetectChanges:
    """Detect changes between interfaces in the database."""
    _old_interface: InterfaceSchema
    _new_interface: InterfaceSchema
    system: SystemConfig

    def __init__(self, old_interface: InterfaceSchema | None = None, new_interface: InterfaceSchema | None = None):
        self.system = SystemConfig()
        self._old_interface = old_interface
        self._new_interface = new_interface

    def _create_new_change(self, equipment: EquipmentSchema, old_interface: InterfaceSchema, new_interface: InterfaceSchema) -> ChangesSchema:
        """Create a new change."""
        old_change_interface = OldInterfaceSchema(
            id=old_interface.id,
            date=old_interface.date,
            ifName=old_interface.ifName,
            ifDescr=old_interface.ifDescr,
            ifAlias=old_interface.ifAlias,
            ifSpeed=old_interface.ifSpeed,
            ifHighSpeed=old_interface.ifHighSpeed,
            ifPhysAddress=old_interface.ifPhysAddress,
            ifType=old_interface.ifType,
            ifOperStatus=old_interface.ifOperStatus,
            ifAdminStatus=old_interface.ifAdminStatus,
            ifPromiscuousMode=old_interface.ifPromiscuousMode,
            ifConnectorPresent=old_interface.ifConnectorPresent,
            ifLastCheck=old_interface.ifLastCheck,
        )
        new_change_interface = NewInterfaceSchema(
            id=new_interface.id,
            date=new_interface.date,
            ifName=new_interface.ifName,
            ifDescr=new_interface.ifDescr,
            ifAlias=new_interface.ifAlias,
            ifSpeed=new_interface.ifSpeed,
            ifHighSpeed=new_interface.ifHighSpeed,
            ifPhysAddress=new_interface.ifPhysAddress,
            ifType=new_interface.ifType,
            ifOperStatus=new_interface.ifOperStatus,
            ifAdminStatus=new_interface.ifAdminStatus,
            ifPromiscuousMode=new_interface.ifPromiscuousMode,
            ifConnectorPresent=new_interface.ifConnectorPresent,
            ifLastCheck=new_interface.ifLastCheck,
        )
        new_change = ChangesSchema(
            ip=equipment.ip,
            community=equipment.community,
            sysname=equipment.sysname,
            ifIndex=new_interface.ifIndex,
            old_interface=old_change_interface,
            new_interface=new_change_interface,
        )
        return new_change
    
    def _get_equipment(self, id_equipment: int) -> EquipmentSchema | None:
        """Get the equipment."""
        equipment = EquipmentController.get_equipment_by_id(id_equipment)
        return equipment

    def _get_new_interfaces(self) -> List[InterfaceSchema]:
        """Get the new interfaces."""
        interface_type = InterfaceType.NEW.value
        interfaces = InterfaceController.get_all_by_type(interface_type)
        return interfaces
    
    def _get_old_version_interface(self, new_interface: InterfaceSchema) -> InterfaceSchema | None:
        """Get the old version of the interface."""
        old_interface_version = InterfaceController.get_by_equipment_type(
            id_equipment=new_interface.equipment,
            ifIndex=new_interface.ifIndex,
            type=InterfaceType.OLD.value
        )
        return old_interface_version

    def _compare_interfaces(
            self, 
            old_interface: InterfaceSchema | None = None, 
            new_interface: InterfaceSchema | None = None
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
        if self.system.configuration.notificationChanges.ifSpeed:
            if old_interface.ifSpeed != new_interface.ifSpeed:
                return True
        if self.system.configuration.notificationChanges.ifHighSpeed:
            if old_interface.ifHighSpeed != new_interface.ifHighSpeed:
                return True
        if self.system.configuration.notificationChanges.ifPhysAddress:
            if old_interface.ifPhysAddress != new_interface.ifPhysAddress:
                return True
        if self.system.configuration.notificationChanges.ifType:
            if old_interface.ifType != new_interface.ifType:
                return True
        if self.system.configuration.notificationChanges.ifOperStatus:
            if old_interface.ifOperStatus != new_interface.ifOperStatus:
                return True
        if self.system.configuration.notificationChanges.ifAdminStatus:
            if old_interface.ifAdminStatus != new_interface.ifAdminStatus:
                return True
        if self.system.configuration.notificationChanges.ifPromiscuousMode:
            if old_interface.ifPromiscuousMode != new_interface.ifPromiscuousMode:
                return True
        if self.system.configuration.notificationChanges.ifConnectorPresent:
            if old_interface.ifConnectorPresent != new_interface.ifConnectorPresent:
                return True
        if self.system.configuration.notificationChanges.ifLastCheck:
            if old_interface.ifLastCheck != new_interface.ifLastCheck:
                return True
        return False

    def get_changes(self) -> List[ChangesSchema]:
        """Get the changes between interfaces."""

        changes: List[ChangesSchema] = []
        new_interfaces = self._get_new_interfaces()
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

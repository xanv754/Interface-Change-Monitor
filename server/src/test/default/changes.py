from typing import List
from constants import InterfaceType
from schemas import ChangesSchema
from system import DetectChanges
from test import constants, DefaultEquipment, DefaultInterface


class DefaultChanges:
    @staticmethod
    def new_insert() -> List[ChangesSchema]:
        date = constants.DATE_CONSULT
        new_equipment = DefaultEquipment.new_insert()
        DefaultInterface.new_insert(
            clean=False,
            date=date,
            equipment=new_equipment,
            interface_type=InterfaceType.OLD.value
        )
        DefaultInterface.new_insert(
            clean=False,
            date=date,
            equipment=new_equipment,
            interface_type=InterfaceType.NEW.value,
            ifName=constants.IFNAME_TWO
        )
        change_controller = DetectChanges()
        changes = change_controller.get_changes(date=date)
        return changes
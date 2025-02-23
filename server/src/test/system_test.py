import unittest
from constants import InterfaceType
from schemas import InterfaceResponseSchema, ChangesResponse
from system import DetectChanges
from test import constants, DefaultInterface, DefaultEquipment


class TestSystem(unittest.TestCase):
    def test_compare_interfaces(self):
        """Test the compare_interfaces method."""

        new_equipment = DefaultEquipment.new_insert()
        old_interface = DefaultInterface.new_insert(
            clean=False,
            equipment=new_equipment,
            interface_type=InterfaceType.OLD.value
        )
        new_interface = DefaultInterface.new_insert(
            clean=False,
            equipment=new_equipment,
            interface_type=InterfaceType.NEW.value,
            ifName=constants.IFNAME_TWO
        )
        change_controller = DetectChanges(old_interface=old_interface, new_interface=new_interface)
        system = change_controller.system
        changes = change_controller._compare_interfaces()
        if system.configuration.notificationChanges.ifName:
            self.assertEqual(changes, True)
        else:
            self.assertEqual(changes, False)

    def test_get_new_interfaces(self):
        """Test the get_new_interfaces method."""
        date = constants.DATE_CONSULT
        new_equipment = DefaultEquipment.new_insert()
        DefaultInterface.new_insert(
            clean=False,
            date=date,
            equipment=new_equipment,
            interface_type=InterfaceType.OLD.value
        )
        new_interface = DefaultInterface.new_insert(
            clean=False,
            date=date,
            equipment=new_equipment,
            interface_type=InterfaceType.NEW.value,
            ifName=constants.IFNAME_TWO
        )
        change_controller = DetectChanges()
        interfaces = change_controller._get_new_interfaces(date=date)
        self.assertEqual(type(interfaces), list)
        self.assertEqual(len(interfaces), 1)
        self.assertEqual(interfaces[0].id, new_interface.id)
        DefaultInterface.clean_table()

    def test_get_old_version_interface(self):
        """Test the get_old_version_interface method."""
        new_equipment = DefaultEquipment.new_insert()
        old_interface = DefaultInterface.new_insert(
            clean=False,
            equipment=new_equipment,
            interface_type=InterfaceType.OLD.value
        )
        new_interface = DefaultInterface.new_insert(
            clean=False,
            equipment=new_equipment,
            interface_type=InterfaceType.NEW.value,
            ifName=constants.IFNAME_TWO
        )
        change_controller = DetectChanges()
        interface = change_controller._get_old_version_interface(new_interface)
        self.assertEqual(type(interface), InterfaceResponseSchema)
        self.assertEqual(interface.id, old_interface.id)
        DefaultInterface.clean_table()

    def test_create_new_change(self):
        """Test the create_new_change method."""
        new_equipment = DefaultEquipment.new_insert()
        old_interface = DefaultInterface.new_insert(
            clean=False,
            equipment=new_equipment,
            interface_type=InterfaceType.OLD.value
        )
        new_interface = DefaultInterface.new_insert(
            clean=False,
            equipment=new_equipment,
            interface_type=InterfaceType.NEW.value,
            ifName=constants.IFNAME_TWO
        )
        change_controller = DetectChanges()
        interface = change_controller._create_new_change(
            equipment=new_equipment,
            old_interface=old_interface,
            new_interface=new_interface
        )
        self.assertEqual(type(interface), ChangesResponse)
        DefaultInterface.clean_table()

    def test_get_changes(self):
        """Test the get_changes method."""
        date = constants.DATE_CONSULT
        new_equipment = DefaultEquipment.new_insert()
        old_interface = DefaultInterface.new_insert(
            clean=False,
            date=date,
            equipment=new_equipment,
            interface_type=InterfaceType.OLD.value
        )
        new_interface = DefaultInterface.new_insert(
            clean=False,
            date=date,
            equipment=new_equipment,
            interface_type=InterfaceType.NEW.value,
            ifName=constants.IFNAME_TWO
        )
        change_controller = DetectChanges()
        changes = change_controller._get_changes(date=date)
        self.assertEqual(type(changes), list)
        self.assertEqual(len(changes), 1)
        self.assertEqual(changes[0].ip, new_equipment.ip)
        self.assertEqual(changes[0].community, new_equipment.community)
        self.assertEqual(changes[0].sysname, new_equipment.sysname)
        self.assertEqual(changes[0].ifIndex, new_interface.ifIndex)
        self.assertEqual(changes[0].oldInterface.id, old_interface.id)
        self.assertEqual(changes[0].newInterface.id, new_interface.id)
        DefaultInterface.clean_table()

    def test_detect_changes(self):
        """Test the detect_changes method."""
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
        status = change_controller.detect_changes(date=date)
        self.assertEqual(status, 1)

if __name__ == "__main__":
    unittest.main()
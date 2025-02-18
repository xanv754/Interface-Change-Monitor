import unittest
from constants import InterfaceType
from schemas import InterfaceSchema, InterfaceRegisterBody
from updater import UpdaterInterfaces, SNMP
from test import constants, DefaultConsults, DefaultInterface, DefaultEquipment, DefaultAssignment


class TestUpdater(unittest.TestCase):
    def test_snmp(self):
        filepath = DefaultConsults.create_consult_file()
        controller = SNMP(filepath=filepath)
        status = controller.get_consults()
        self.assertTrue(status)
        DefaultInterface.clean_table()
        DefaultConsults.delete_consult_file()

    def test_get_interface(self):
        consult = DefaultConsults.consult_new()
        updater = UpdaterInterfaces(consult)
        interface = updater.get_interface()
        self.assertEqual(type(interface), InterfaceRegisterBody)

    def test_get_interface_exists(self):
        equipment_database = DefaultEquipment.new_insert()
        DefaultInterface.new_insert(
            clean=False,
            equipment=equipment_database
        )
        consult = DefaultConsults.consult_new()
        updater = UpdaterInterfaces(consult)
        interface = updater._get_interface_exists()
        self.assertEqual(type(interface), InterfaceSchema)
        self.assertEqual(interface.equipment, equipment_database.id)
        self.assertEqual(interface.ifIndex, constants.IFINDEX)
        DefaultInterface.clean_table()

    def test_check_same_interfaces(self):
        interface_database = DefaultInterface.new_insert()
        consult = DefaultConsults.consult_old()
        updater = UpdaterInterfaces(consult)
        status = updater._check_same_interfaces(interface_database)
        self.assertEqual(status, True)

    def test_update_case_one(self):
        """Case 1: New interface. 

        The consult of the interface does not exist in the database.
        """
        DefaultInterface.clean_table()
        consult = DefaultConsults.consult_old()
        updater = UpdaterInterfaces(consult)
        interface_consult = updater.get_interface()
        updater.update()
        interface_database = DefaultInterface.select_one_by_device_type(
            ip=constants.IP,
            community=constants.COMMUNITY,
            ifIndex=constants.IFINDEX,
            type=InterfaceType.NEW.value,
        )
        self.assertEqual(type(interface_database), InterfaceSchema)
        equipment = DefaultEquipment.select_one_by_id(id=interface_database.equipment)
        self.assertEqual(equipment.ip, interface_consult.ip)
        self.assertEqual(equipment.community, interface_consult.community)
        self.assertEqual(equipment.sysname, interface_consult.sysname)
        self.assertEqual(interface_database.ifIndex, interface_consult.ifIndex)
        DefaultInterface.clean_table()

    def test_updater_case_two(self):
        """Case 2: Consult is the same as the interface in the database.
        
        The interface exists in the database, 
        and the consult returned the same values as the interface in the database.
        """
        interface_database = DefaultInterface.new_insert()
        consult = DefaultConsults.consult_old()
        updater = UpdaterInterfaces(consult)
        interface_consult = updater.get_interface()
        updater.update()
        interface = DefaultInterface.select_one_by_id(id=interface_database.id)
        self.assertEqual(type(interface), InterfaceSchema)
        self.assertEqual(interface.ifIndex, interface_database.ifIndex)
        self.assertEqual(interface.ifIndex, interface_consult.ifIndex)
        self.assertEqual(interface.ifName, interface_database.ifName)
        self.assertEqual(interface.ifName, interface_consult.ifName)
        DefaultInterface.clean_table()

    def test_updater_case_two_special(self):
        """Case 2.1: Consult is the same as the interface in the database, 
        but the sysname is different.
        
        The interface exists in the database, 
        and the consult returned the same values as the interface in the database,
        but the sysname of the equipment of the interface is different.
        """
        interface_database = DefaultInterface.new_insert()
        consult = DefaultConsults.consult_old_with_new_sysname()
        updater = UpdaterInterfaces(consult)
        interface_consult = updater.get_interface()
        updater.update()
        interface = DefaultInterface.select_one_by_id(id=interface_database.id)
        self.assertEqual(type(interface), InterfaceSchema)
        self.assertEqual(interface.ifIndex, interface_database.ifIndex)
        self.assertEqual(interface.ifIndex, interface_consult.ifIndex)
        self.assertEqual(interface.ifName, interface_database.ifName)
        self.assertEqual(interface.ifName, interface_consult.ifName)
        equipment_database = DefaultEquipment.select_one_by_id(id=interface.equipment)
        self.assertEqual(equipment_database.ip, interface_consult.ip)
        self.assertEqual(equipment_database.community, interface_consult.community)
        self.assertEqual(equipment_database.sysname, interface_consult.sysname)
        DefaultInterface.clean_table()

    def test_updater_case_three(self):
        """Case 3: Consult is different from the interface, but does not exist old interface.
        
        The consult of the interface is different from the interface in the database,
        but the interface only exists in one version (new).
        """
        old_interface_database = DefaultInterface.new_insert()
        consult = DefaultConsults.consult_new()
        updater = UpdaterInterfaces(consult)
        interface_consult = updater.get_interface()
        updater.update()
        new_interface_database = DefaultInterface.select_one_by_device_type(
            ip=interface_consult.ip,
            community=interface_consult.community,
            ifIndex=interface_consult.ifIndex,
            type=InterfaceType.NEW.value,
        )
        old_interface_database = DefaultInterface.select_one_by_id(id=old_interface_database.id)
        self.assertEqual(type(new_interface_database), InterfaceSchema)
        self.assertEqual(new_interface_database.ifIndex, interface_consult.ifIndex)
        self.assertEqual(new_interface_database.ifIndex, old_interface_database.ifIndex)
        self.assertEqual(old_interface_database.type, InterfaceType.OLD.value)
        self.assertEqual(new_interface_database.equipment, old_interface_database.equipment)
        DefaultInterface.clean_table()

    def test_updater_case_four(self):
        """Case 4: Consult is different from the interface, and old interface exists.
        
        The consult of the interface is different from the interface in the database,
        and the interface has an old version.
        """
        equipment_database = DefaultEquipment.new_insert()
        old_interface_database = DefaultInterface.new_insert(
            clean=False,
            equipment=equipment_database,
            interface_type=InterfaceType.OLD.value)
        new_interface_database = DefaultInterface.new_insert(
            clean=False,
            equipment=equipment_database,
            interface_type=InterfaceType.NEW.value, 
            date=constants.DATE_CONSULT_TWO
        )
        consult = DefaultConsults.consult_new()
        updater = UpdaterInterfaces(consult)
        interface_consult = updater.get_interface()
        updater.update()
        old_interface_database = DefaultInterface.select_one_by_id(id=old_interface_database.id)
        self.assertEqual(type(old_interface_database), InterfaceSchema)
        self.assertEqual(old_interface_database.equipment, new_interface_database.equipment)
        self.assertEqual(old_interface_database.ifIndex, new_interface_database.ifIndex)
        self.assertEqual(old_interface_database.date, new_interface_database.date)
        self.assertEqual(old_interface_database.type, InterfaceType.OLD.value)
        interface = DefaultInterface.select_one_by_device_type(
            ip=interface_consult.ip,
            community=interface_consult.community,
            ifIndex=interface_consult.ifIndex,
            type=InterfaceType.NEW.value,
        )
        self.assertEqual(type(interface), InterfaceSchema)
        self.assertEqual(interface.equipment, old_interface_database.equipment)
        self.assertEqual(interface.ifIndex, old_interface_database.ifIndex)
        self.assertEqual(interface.type, InterfaceType.NEW.value)
        DefaultInterface.clean_table()

    def test_updater_case_four_special(self):
        """Case 4.1: Consult is different from the interface, and old interface exists and interface has been assigned.
        
        The consult of the interface is different from the interface in the database,
        and the interface has an old version, but that old version has been assigned an operator.
        """
        new_assignment = DefaultAssignment.new_insert()
        consult = DefaultConsults.consult_new()
        updater = UpdaterInterfaces(consult)
        updater.update()
        old_interface_database = DefaultInterface.select_one_by_id(id=new_assignment.old_interface)
        self.assertEqual(type(old_interface_database), InterfaceSchema)
        new_interface_database = DefaultInterface.select_one_by_id(id=new_assignment.new_interface)
        self.assertEqual(type(new_interface_database), InterfaceSchema)
        self.assertEqual(new_interface_database.equipment, old_interface_database.equipment)
        self.assertEqual(new_interface_database.ifIndex, old_interface_database.ifIndex)
        self.assertEqual(new_interface_database.type, InterfaceType.NEW.value)
        self.assertEqual(old_interface_database.type, InterfaceType.OLD.value)
        DefaultAssignment.clean_table()


if __name__ == "__main__":
    unittest.main()

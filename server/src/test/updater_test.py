import unittest
from constants import InterfaceType
from controllers import InterfaceController, OperatorController
from schemas import InterfaceSchema
from updater import UpdaterDatabase
from test import default


class TestUpdater(unittest.TestCase):
    def test_check_interface_exists(self):
        default.register_interface()
        consult = default.create_consult()
        updater = UpdaterDatabase(consult)
        interface = updater._check_interface_exists()
        self.assertEqual(type(interface), InterfaceSchema)
        self.assertEqual(interface.ifIndex, default.IFINDEX)
        default.clean_table_interface()

    def test_compare_interfaces(self):
        default.register_interface()
        consult = default.create_consult()
        updater = UpdaterDatabase(consult)
        other_interface = InterfaceSchema(
            id="0",
            equipment="0",
            date=default.DATE_CONSULT,
            type=InterfaceType.NEW.value,
            ifIndex=default.IFINDEX,
            ifName="test@ifName",
            ifDescr="test@ifDescr",
            ifAlias="test@ifAlias",
            ifSpeed=1000,
            ifHighSpeed=1000,
            ifPhysAddress="test@ifPhysAddress",
            ifType="test@ifType",
            ifOperStatus="UP",
            ifAdminStatus="UP",
            ifPromiscuousMode=False,
            ifConnectorPresent=False,
            ifLastCheck="2022-01-01",
        )
        status = updater._compare_interfaces(other_interface)
        self.assertEqual(status, True)
        other_different_interface = InterfaceSchema(
            id="0",
            equipment="0",
            date=default.DATE_CONSULT,
            type=InterfaceType.NEW.value,
            ifIndex=default.IFINDEX,
            ifName="test@ifName2",
            ifDescr="test@ifDescr2",
            ifAlias="test@ifAlias2",
            ifSpeed=1000,
            ifHighSpeed=1000,
            ifPhysAddress="test@ifPhysAddress",
            ifType="test@ifType",
            ifOperStatus="UP",
            ifAdminStatus="DOWN",
            ifPromiscuousMode=False,
            ifConnectorPresent=False,
            ifLastCheck="2022-01-01",
        )
        status = updater._compare_interfaces(other_different_interface)
        self.assertEqual(status, False)
        default.clean_table_interface()

    def test_updater(self):
        # Case 1: New interface
        default.clean_table_interface()
        consult = default.create_consult()
        updater = UpdaterDatabase(consult)
        updater.update()
        interface = InterfaceController.get_by_device_type(
            ip=default.IP,
            community=default.COMMUNITY,
            ifIndex=default.IFINDEX,
            type=InterfaceType.NEW.value,
        )
        self.assertEqual(type(interface), InterfaceSchema)
        self.assertEqual(interface.ifIndex, default.IFINDEX)
        default.clean_table_interface()

        # Case 2: Consult is the same as the interface in the database
        id_interface = default.register_interface()[1]
        consult = default.create_consult()
        updater = UpdaterDatabase(consult)
        updater.update()
        interface = InterfaceController.get_by_device_type(
            ip=default.IP,
            community=default.COMMUNITY,
            ifIndex=default.IFINDEX,
            type=InterfaceType.NEW.value,
        )
        self.assertEqual(type(interface), InterfaceSchema)
        self.assertEqual(interface.id, id_interface)
        self.assertEqual(interface.ifName, "test@ifName")
        default.clean_table_interface()

        # Case 3: Consult is different from the interface, but does not exist old interface
        id_interface = default.register_interface()[1]
        consult = default.create_consult(one=False)
        updater = UpdaterDatabase(consult)
        updater.update()
        old_interface = InterfaceController.get_by_device_type(
            ip=default.IP,
            community=default.COMMUNITY,
            ifIndex=default.IFINDEX,
            type=InterfaceType.OLD.value,
        )
        self.assertEqual(type(old_interface), InterfaceSchema)
        self.assertEqual(old_interface.id, id_interface)
        self.assertEqual(old_interface.ifName, "test@ifName")
        interface = InterfaceController.get_by_device_type(
            ip=default.IP,
            community=default.COMMUNITY,
            ifIndex=default.IFINDEX,
            type=InterfaceType.NEW.value,
        )
        self.assertEqual(type(interface), InterfaceSchema)
        self.assertEqual(interface.ifIndex, default.IFINDEX)
        self.assertEqual(interface.ifName, "test@ifName2")
        default.clean_table_interface()

        # Case 4: Consult is different from the interface, and old interface exists
        data = default.register_interface(interface_type=InterfaceType.OLD.value)
        id_equipment = data[0]
        id_old_interface = data[1]
        id_new_interface = default.register_interface(
            clean=False, id_equipment=id_equipment
        )[1]
        consult = default.create_consult(one=False)
        updater = UpdaterDatabase(consult)
        updater.update()
        old_interface = InterfaceController.get_by_device_type(
            ip=default.IP,
            community=default.COMMUNITY,
            ifIndex=default.IFINDEX,
            type=InterfaceType.OLD.value,
        )
        self.assertEqual(type(old_interface), InterfaceSchema)
        self.assertEqual(old_interface.id, id_old_interface)
        self.assertEqual(old_interface.ifName, "test@ifName")
        new_interface = InterfaceController.get_by_device_type(
            ip=default.IP,
            community=default.COMMUNITY,
            ifIndex=default.IFINDEX,
            type=InterfaceType.NEW.value,
        )
        self.assertEqual(type(new_interface), InterfaceSchema)
        self.assertEqual(new_interface.id, id_new_interface)
        self.assertEqual(new_interface.ifName, "test@ifName2")
        default.clean_table_interface()

    def test_updater_special_case(self):
        # Case 4: Consult is different from the interface, and old interface exists and interface was assigned
        data = default.register_assignment()
        id_assignment = data[2]
        assignment = OperatorController.get_assignment(id_assignment)
        id_old_interface = assignment.old_interface
        old_interface = InterfaceController.get_by_id(id_old_interface)
        self.assertEqual(type(old_interface), InterfaceSchema)
        self.assertEqual(old_interface.ifName, "test@ifName")
        self.assertEqual(old_interface.type, InterfaceType.OLD.value)
        
        id_new_interface = assignment.new_interface
        new_interface = InterfaceController.get_by_id(id_new_interface)
        self.assertEqual(type(new_interface), InterfaceSchema)
        self.assertEqual(new_interface.ifName, "test@ifName")
        self.assertEqual(new_interface.type, InterfaceType.NEW.value)

        consult = default.create_consult(one=False)
        updater = UpdaterDatabase(consult)
        updater.update()
        old_interface = InterfaceController.get_by_id(id_old_interface)
        self.assertEqual(type(old_interface), InterfaceSchema)
        self.assertEqual(old_interface.ifName, "test@ifName")
        self.assertEqual(old_interface.type, InterfaceType.OLD.value)

        new_interface = InterfaceController.get_by_id(id_new_interface)
        self.assertEqual(type(new_interface), InterfaceSchema)
        self.assertEqual(new_interface.ifName, "test@ifName2")
        self.assertEqual(new_interface.type, InterfaceType.NEW.value)
        default.clean_table_interface()
        default.clean_table_assignment()


if __name__ == "__main__":
    unittest.main()

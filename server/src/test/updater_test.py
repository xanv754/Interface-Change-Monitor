import unittest
from constants import InterfaceType
from controllers import InterfaceController, OperatorController
from database import InterfaceSchema, AssignmentSchema
from updater import UpdaterDatabase
from test import default


class TestUpdater(unittest.TestCase):
    def test_check_interface_exists(self):
        default.register_interface()
        consult = default.create_consult()
        updater = UpdaterDatabase(consult)
        interface = updater._check_interface_exists()
        self.assertEqual(type(interface), dict)
        self.assertEqual(interface[InterfaceSchema.IFINDEX.value], default.IFINDEX)
        default.clean_table_interface()

    def test_compare_interfaces(self):
        default.register_interface()
        consult = default.create_consult()
        updater = UpdaterDatabase(consult)
        other_interface = {
            InterfaceSchema.IFNAME.value: "test@ifName",
            InterfaceSchema.IFDESCR.value: "test@ifDescr",
            InterfaceSchema.IFALIAS.value: "test@ifAlias",
            InterfaceSchema.IFSPEED.value: 1000,
            InterfaceSchema.IFHIGHSPEED.value: 1000,
            InterfaceSchema.IFPHYSADDRESS.value: "test@ifPhysAddress",
            InterfaceSchema.IFTYPE.value: "test@ifType",
            InterfaceSchema.IFOPERSTATUS.value: "UP",
            InterfaceSchema.IFADMINSTATUS.value: "UP",
            InterfaceSchema.IFPROMISCUOUSMODE.value: False,
            InterfaceSchema.IFCONNECTORPRESENT.value: False,
            InterfaceSchema.IFLASTCHECK.value: "2022-01-01",
        }
        status = updater._compare_interfaces(other_interface)
        self.assertEqual(status, True)
        other_different_interface = {
            InterfaceSchema.IFNAME.value: "test@ifName2",
            InterfaceSchema.IFDESCR.value: "test@ifDescr2",
            InterfaceSchema.IFALIAS.value: "test@ifAlias2",
            InterfaceSchema.IFSPEED.value: 1000,
            InterfaceSchema.IFHIGHSPEED.value: 1000,
            InterfaceSchema.IFPHYSADDRESS.value: "test@ifPhysAddress",
            InterfaceSchema.IFTYPE.value: "test@ifType",
            InterfaceSchema.IFOPERSTATUS.value: "UP",
            InterfaceSchema.IFADMINSTATUS.value: "DOWN",
            InterfaceSchema.IFPROMISCUOUSMODE.value: False,
            InterfaceSchema.IFCONNECTORPRESENT.value: False,
            InterfaceSchema.IFLASTCHECK.value: "2022-01-01",
        }
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
        self.assertEqual(type(interface), dict)
        self.assertEqual(interface[InterfaceSchema.IFINDEX.value], default.IFINDEX)
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
        self.assertEqual(type(interface), dict)
        self.assertEqual(interface[InterfaceSchema.ID.value], id_interface)
        self.assertEqual(interface[InterfaceSchema.IFNAME.value], "test@ifName")
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
        self.assertEqual(type(old_interface), dict)
        self.assertEqual(old_interface[InterfaceSchema.ID.value], id_interface)
        self.assertEqual(old_interface[InterfaceSchema.IFNAME.value], "test@ifName")
        interface = InterfaceController.get_by_device_type(
            ip=default.IP,
            community=default.COMMUNITY,
            ifIndex=default.IFINDEX,
            type=InterfaceType.NEW.value,
        )
        self.assertEqual(type(interface), dict)
        self.assertEqual(interface[InterfaceSchema.IFINDEX.value], default.IFINDEX)
        self.assertEqual(interface[InterfaceSchema.IFNAME.value], "test@ifName2")
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
        self.assertEqual(type(old_interface), dict)
        self.assertEqual(old_interface[InterfaceSchema.ID.value], id_old_interface)
        self.assertEqual(old_interface[InterfaceSchema.IFNAME.value], "test@ifName")
        new_interface = InterfaceController.get_by_device_type(
            ip=default.IP,
            community=default.COMMUNITY,
            ifIndex=default.IFINDEX,
            type=InterfaceType.NEW.value,
        )
        self.assertEqual(type(new_interface), dict)
        self.assertEqual(new_interface[InterfaceSchema.ID.value], id_new_interface)
        self.assertEqual(new_interface[InterfaceSchema.IFNAME.value], "test@ifName2")
        default.clean_table_interface()

    def test_updater_special_case(self):
        # Case 4: Consult is different from the interface, and old interface exists and interface was assigned
        data = default.register_assignment()
        id_assignment = data[2]
        assignment = OperatorController.get_assignment(id_assignment)
        id_old_interface = assignment[AssignmentSchema.OLD_INTERFACE.value]
        old_interface = InterfaceController.get_by_id(id_old_interface)
        self.assertEqual(type(old_interface), dict)
        self.assertEqual(old_interface[InterfaceSchema.IFNAME.value], "test@ifName")
        self.assertEqual(
            old_interface[InterfaceSchema.INTERFACE_TYPE.value], InterfaceType.OLD.value
        )
        id_new_interface = assignment[AssignmentSchema.CHANGE_INTERFACE.value]
        new_interface = InterfaceController.get_by_id(id_new_interface)
        self.assertEqual(type(new_interface), dict)
        self.assertEqual(new_interface[InterfaceSchema.IFNAME.value], "test@ifName")
        self.assertEqual(
            new_interface[InterfaceSchema.INTERFACE_TYPE.value], InterfaceType.NEW.value
        )
        consult = default.create_consult(one=False)
        updater = UpdaterDatabase(consult)
        updater.update()
        old_interface = InterfaceController.get_by_id(id_old_interface)
        self.assertEqual(type(old_interface), dict)
        self.assertEqual(old_interface[InterfaceSchema.IFNAME.value], "test@ifName")
        self.assertEqual(
            old_interface[InterfaceSchema.INTERFACE_TYPE.value], InterfaceType.OLD.value
        )
        new_interface = InterfaceController.get_by_id(id_new_interface)
        self.assertEqual(type(new_interface), dict)
        self.assertEqual(new_interface[InterfaceSchema.IFNAME.value], "test@ifName2")
        self.assertEqual(
            new_interface[InterfaceSchema.INTERFACE_TYPE.value], InterfaceType.NEW.value
        )
        default.clean_table_interface()
        default.clean_table_assignment()


if __name__ == "__main__":
    unittest.main()

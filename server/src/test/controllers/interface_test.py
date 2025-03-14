import unittest
import random
from constants import StatusType, InterfaceType
from controllers import InterfaceController
from schemas import InterfaceSchema, RegisterInterfaceBody
from test import constants, DefaultEquipment, DefaultInterface


class TestInterfaceController(unittest.TestCase):
    def test_register(self):
        new_equipment = DefaultEquipment.new_insert()
        new_date_consult =  "2022-" + str(random.randint(1, 12)) + "-" + str(random.randint(1, 28))
        body = RegisterInterfaceBody(
            dateConsult=new_date_consult,
            interfaceType=InterfaceType.NEW.value,
            ip=new_equipment.ip,
            community=new_equipment.community,
            sysname=new_equipment.sysname,
            ifIndex=constants.IFINDEX,
            ifName="eth0",
            ifDescr="eth0",
            ifAlias="eth0",
            ifHighSpeed=1000,
            ifOperStatus=StatusType.UP.value,
            ifAdminStatus=StatusType.UP.value,
        )
        status = InterfaceController.register(body)
        self.assertEqual(status, True)
        interface = DefaultInterface.select_one_by_device_type(
            ip=new_equipment.ip,
            community=new_equipment.community,
            ifIndex=constants.IFINDEX,
            type=InterfaceType.NEW.value,
        )
        self.assertEqual(type(interface), InterfaceSchema)
        self.assertEqual(interface.equipment, new_equipment.id)
        self.assertEqual(interface.ifIndex, constants.IFINDEX)
        self.assertEqual(interface.type, InterfaceType.NEW.value)
        DefaultInterface.clean_table()

    def test_get_by_id(self):
        new_interface = DefaultInterface.new_insert()
        interface = InterfaceController.get_by_id(new_interface.id)
        self.assertEqual(type(interface), InterfaceSchema)
        self.assertEqual(interface.id, new_interface.id)
        DefaultInterface.clean_table()

    def test_get_by_device_type(self):
        new_interface = DefaultInterface.new_insert()
        equipment = DefaultEquipment.select_one_by_id(new_interface.equipment)
        interface = InterfaceController.get_by_device_type(
            ip=equipment.ip,
            community=equipment.community,
            ifIndex=new_interface.ifIndex,
            type=new_interface.type,
        )
        self.assertEqual(type(interface), InterfaceSchema)
        self.assertEqual(interface.id, new_interface.id)
        DefaultInterface.clean_table()

    def test_get_all_by_type(self):
        date = constants.DATE_CONSULT
        new_interface_type = InterfaceType.NEW.value
        new_interface = DefaultInterface.new_insert(
            date=date,
            interface_type=new_interface_type
        )
        interfaces = InterfaceController.get_all_by_type(new_interface_type, date)
        self.assertEqual(type(interfaces), list)
        self.assertNotEqual(len(interfaces), 0)
        self.assertEqual(interfaces[0].id, new_interface.id)
        DefaultInterface.clean_table()

    def test_get_by_equipment_type(self):
        new_interface_type = InterfaceType.NEW.value
        new_interface = DefaultInterface.new_insert(
            interface_type=new_interface_type
        )
        interface = InterfaceController.get_by_equipment_type(
            id_equipment=new_interface.equipment,
            ifIndex=new_interface.ifIndex,
            type=new_interface_type
        )
        self.assertEqual(type(interface), InterfaceSchema)
        self.assertEqual(interface.id, new_interface.id)
        DefaultInterface.clean_table()

    def test_update(self):
        new_interface = DefaultInterface.new_insert()
        new_ifName = "unittest@ifName"
        body = RegisterInterfaceBody(
            dateConsult=constants.DATE_CONSULT_TWO,
            interfaceType=InterfaceType.OLD.value,
            ip=constants.IP,
            community=constants.COMMUNITY,
            sysname=constants.SYSNAME,
            ifIndex=new_interface.ifIndex,
            ifName=new_ifName,
            ifDescr=new_interface.ifDescr,
            ifAlias=new_interface.ifAlias,
            ifHighSpeed=new_interface.ifHighSpeed,
            ifOperStatus=new_interface.ifOperStatus,
            ifAdminStatus=new_interface.ifAdminStatus,
        )
        status = InterfaceController.update(new_interface.id, body)
        self.assertEqual(status, True)
        interface = DefaultInterface.select_one_by_id(new_interface.id)
        self.assertEqual(interface.ifName, new_ifName)
        DefaultInterface.clean_table()

    def test_update_type(self):
        new_interface = DefaultInterface.new_insert()
        new_interface_type = InterfaceType.OLD.value
        status = InterfaceController.update_type(new_interface.id, new_interface_type)
        self.assertEqual(status, True)
        interface = DefaultInterface.select_one_by_id(new_interface.id)
        self.assertEqual(interface.type, new_interface_type)
        DefaultInterface.clean_table()


if __name__ == "__main__":
    unittest.main()

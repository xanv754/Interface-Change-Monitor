import unittest
import random
from constants import StatusType, InterfaceType
from controllers import InterfaceController
from models import InterfaceModel, Interface
from schemas import InterfaceSchema, InterfaceRegisterBody
from test import constants, DefaultEquipment, DefaultInterface


class TestInterfaceModel(unittest.TestCase):
    def test_register(self):
        new_equipment = DefaultEquipment.new_insert()
        new_ifIndex = random.randint(1, 255)
        new_date_consult = "2022-" + str(random.randint(1, 12)) + "-" + str(random.randint(1, 28))
        new_interface_type = InterfaceType.NEW.value
        model = InterfaceModel(
            ifIndex=new_ifIndex,
            idEquipment=new_equipment.id,
            dateConsult=new_date_consult,
            interfaceType=new_interface_type,
            ifName="eth0",
            ifDescr="eth0",
            ifAlias="eth0",
            ifSpeed=1000,
            ifHighSpeed=1000,
            ifPhysAddress="00:00:00:00:00:00",
            ifType="ethernet",
            ifOperStatus=StatusType.UP.value,
            ifAdminStatus=StatusType.UP.value,
            ifPromiscuousMode=False,
            ifConnectorPresent=False,
            ifLastCheck="2022-01-01",
        )
        status = model.register()
        self.assertEqual(status, True)
        new_interface = DefaultInterface.select_one_by_device_type(
            ip=new_equipment.ip,
            community=new_equipment.community,
            ifIndex=new_ifIndex,
            type=new_interface_type
        )
        self.assertEqual(new_interface.equipment, new_equipment.id)
        self.assertEqual(new_interface.ifIndex, new_ifIndex)
        DefaultInterface.clean_table()

    def test_update(self):
        new_interface = DefaultInterface.new_insert()
        new_ifName = "unittest@ifName"
        model = InterfaceModel(
            id=new_interface.id,
            ifIndex=new_interface.ifIndex,
            idEquipment=new_interface.equipment,
            dateConsult=new_interface.date,
            interfaceType=new_interface.type,
            ifName=new_ifName,
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
        status = model.update()
        self.assertEqual(status, True)
        interface = DefaultInterface.select_one_by_id(new_interface.id)
        self.assertEqual(interface.ifName, new_ifName)
        self.assertEqual(interface.type, new_interface.type)
        DefaultInterface.clean_table()

    def test_get_all_by_type(self):
        date = constants.DATE_CONSULT
        new_interface_type = InterfaceType.NEW.value
        new_interface = DefaultInterface.new_insert(
            date=date,
            interface_type=new_interface_type
        )
        model = Interface.get_all_by_type(new_interface_type, date)
        self.assertEqual(type(model), list)
        self.assertNotEqual(len(model), 0)
        self.assertEqual(model[0].id, new_interface.id)
        DefaultInterface.clean_table()

    def test_get_all_by_date(self):
        new_interface = DefaultInterface.new_insert()
        model = Interface(dateConsult=constants.DATE_CONSULT)
        interfaces = model.get_all_by_date()
        self.assertEqual(type(interfaces), list)
        self.assertNotEqual(len(interfaces), 0)
        self.assertEqual(interfaces[0].id, new_interface.id)
        DefaultInterface.clean_table()
    
    def test_get_by_device_type(self):
        new_interface = DefaultInterface.new_insert()
        model = Interface(ifIndex=new_interface.ifIndex, idEquipment=new_interface.equipment)
        interface = model.get_by_device_type(new_interface.type)
        self.assertEqual(type(interface), InterfaceSchema)
        self.assertEqual(interface.id, new_interface.id)
        self.assertEqual(interface.equipment, new_interface.equipment)
        self.assertEqual(interface.ifIndex, new_interface.ifIndex)
        self.assertEqual(interface.type, new_interface.type)
        DefaultInterface.clean_table()

    def test_get_by_equipment_type(self):
        new_interface_type = InterfaceType.NEW.value
        new_interface = DefaultInterface.new_insert(
            interface_type=new_interface_type
        )
        model = Interface(idEquipment=new_interface.equipment, ifIndex=new_interface.ifIndex)
        interface = model.get_by_equipment_type(new_interface_type)
        self.assertEqual(type(interface), InterfaceSchema)
        self.assertEqual(interface.id, new_interface.id)
        DefaultInterface.clean_table()

    def test_get_by_device_date(self):
        new_interface = DefaultInterface.new_insert()
        model = Interface(
            idEquipment=new_interface.equipment,
            ifIndex=new_interface.ifIndex,
            dateConsult=new_interface.date,
        )
        interface = model.get_by_device_date()
        self.assertEqual(type(interface), InterfaceSchema)
        self.assertEqual(interface.equipment, new_interface.equipment)
        self.assertEqual(interface.ifIndex, new_interface.ifIndex)
        self.assertEqual(interface.date, new_interface.date)
        DefaultInterface.clean_table()

    def test_get_by_id(self):
        new_interface = DefaultInterface.new_insert()
        model = Interface(id=new_interface.id)
        interface = model.get_by_id()
        self.assertEqual(type(interface), InterfaceSchema)
        self.assertEqual(interface.id, new_interface.id)
        DefaultInterface.clean_table()

    def test_update_type(self):
        new_interface = DefaultInterface.new_insert()
        new_interface_type = InterfaceType.OLD.value
        model = Interface(id=new_interface.id)
        status = model.update_type(new_interface_type)
        self.assertEqual(status, True)
        interface = DefaultInterface.select_one_by_id(new_interface.id)
        self.assertEqual(interface.type, new_interface_type)
        DefaultInterface.clean_table()

    def test_delete(self):
        new_interface = DefaultInterface.new_insert()
        model = Interface(id=new_interface.id)
        status = model.delete()
        self.assertEqual(status, True)
        self.assertIsNone(
            DefaultInterface.select_one_by_id(new_interface.id)
        )
        DefaultInterface.clean_table()


class TestInterfaceController(unittest.TestCase):
    def test_register(self):
        new_equipment = DefaultEquipment.new_insert()
        new_date_consult =  "2022-" + str(random.randint(1, 12)) + "-" + str(random.randint(1, 28))
        body = InterfaceRegisterBody(
            dateConsult=new_date_consult,
            interfaceType=InterfaceType.NEW.value,
            ip=new_equipment.ip,
            community=new_equipment.community,
            sysname=new_equipment.sysname,
            ifIndex=constants.IFINDEX,
            ifName="eth0",
            ifDescr="eth0",
            ifAlias="eth0",
            ifSpeed=1000,
            ifHighSpeed=1000,
            ifPhysAddress="00:00:00:00:00:00",
            ifType="ethernet",
            ifOperStatus=StatusType.UP.value,
            ifAdminStatus=StatusType.UP.value,
            ifPromiscuousMode=False,
            ifConnectorPresent=False,
            ifLastChange="2022-01-01",
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
        body = InterfaceRegisterBody(
            dateConsult=constants.DATE_CONSULT_TWO,
            interfaceType=InterfaceType.OLD.value,
            ip=constants.IP,
            community=constants.COMMUNITY,
            sysname=constants.SYSNAME,
            ifIndex=new_interface.ifIndex,
            ifName=new_ifName,
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
            ifLastChange=new_interface.ifLastCheck,
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

import unittest
import random
from constants import StatusType, InterfaceType
from controllers import InterfaceController
from models import InterfaceModel, Interface, InterfaceRegisterBody
from schemas import InterfaceSchema
from test import default


class TestInterfaceQuery(unittest.TestCase):
    def test_register(self):
        id_equipment = default.register_equipment()
        model = InterfaceModel(
            ifIndex=random.randint(1, 255),
            idEquipment=id_equipment,
            dateConsult="2022-"
            + str(random.randint(1, 12))
            + "-"
            + str(random.randint(1, 28)),
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
        default.clean_table_interface()

    def test_get_all_by_date(self):
        default.register_interface()
        model = Interface(dateConsult=default.DATE_CONSULT)
        interfaces = model.get_all_by_date()
        self.assertEqual(type(interfaces), list)
        self.assertNotEqual(len(interfaces), 0)
        default.clean_table_interface()

    def test_get_by_device_date(self):
        id_equipment = default.register_interface()[0]
        model = Interface(
            idEquipment=id_equipment,
            ifIndex=default.IFINDEX,
            dateConsult=default.DATE_CONSULT,
        )
        interface = model.get_by_device_date()
        self.assertEqual(type(interface), dict)
        self.assertEqual(interface[InterfaceSchema.IFINDEX.value], default.IFINDEX)
        self.assertEqual(interface[InterfaceSchema.ID_EQUIPMENT.value], id_equipment)
        self.assertEqual(
            interface[InterfaceSchema.DATE_CONSULT.value], default.DATE_CONSULT
        )
        default.clean_table_interface()

    def test_get_by_id(self):
        id_interface = default.register_interface()[1]
        model = Interface(id=id_interface)
        interface = model.get_by_id()
        self.assertEqual(type(interface), dict)
        self.assertEqual(interface[InterfaceSchema.ID.value], id_interface)
        default.clean_table_interface()

    def test_get_by_device_type(self):
        data = default.register_interface()
        id_equipment = data[0]
        id_interface = data[1]
        ifIndex = Interface(id=id_interface).get_by_id()[InterfaceSchema.IFINDEX.value]
        model = Interface(idEquipment=id_equipment, ifIndex=ifIndex)
        interface = model.get_by_device_type(InterfaceType.NEW.value)
        self.assertEqual(type(interface), dict)
        self.assertEqual(interface[InterfaceSchema.ID.value], id_interface)
        default.clean_table_interface()

    def test_update(self):
        data = default.register_interface()
        id_equipment = data[0]
        id_interface = data[1]
        model = InterfaceModel(
            id=id_interface,
            ifIndex=default.IFINDEX,
            idEquipment=id_equipment,
            dateConsult="2025-01-01",
            ifName="test",
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
        status = model.update()
        self.assertEqual(status, True)
        interface = Interface(id=id_interface).get_by_id()
        self.assertEqual(interface[InterfaceSchema.IFNAME.value], "test")
        self.assertEqual(
            interface[InterfaceSchema.INTERFACE_TYPE.value], InterfaceType.NEW.value
        )
        default.clean_table_interface()

    def test_update_type(self):
        id_interface = default.register_interface()[1]
        model = Interface(id=id_interface)
        status = model.update_type(InterfaceType.OLD.value)
        self.assertEqual(status, True)
        interface = Interface(id=id_interface).get_by_id()
        self.assertEqual(
            interface[InterfaceSchema.INTERFACE_TYPE.value], InterfaceType.OLD.value
        )
        default.clean_table_interface()

    def test_delete(self):
        id_equipment = default.register_equipment()
        ifIndex = random.randint(1, 255)
        model = InterfaceModel(
            ifIndex=ifIndex,
            idEquipment=id_equipment,
            dateConsult=default.DATE_CONSULT,
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
        model = Interface(
            ifIndex=ifIndex, idEquipment=id_equipment, dateConsult=default.DATE_CONSULT
        )
        interface = model.get_by_device_date()
        id = interface[InterfaceSchema.ID.value]
        model = Interface(id=id)
        status = model.delete()
        self.assertEqual(status, True)


class TestInterfaceController(unittest.TestCase):
    def test_get_by_id(self):
        id_interface = default.register_interface()[1]
        interface = InterfaceController.get_by_id(id_interface)
        self.assertEqual(type(interface), dict)
        self.assertEqual(interface[InterfaceSchema.ID.value], id_interface)
        default.clean_table_interface()

    def test_get_by_device_type(self):
        id_interface = default.register_interface()[1]
        interface = InterfaceController.get_by_device_type(
            ip=default.IP,
            community=default.COMMUNITY,
            ifIndex=default.IFINDEX,
            type=InterfaceType.NEW.value,
        )
        self.assertEqual(type(interface), dict)
        self.assertEqual(interface[InterfaceSchema.ID.value], id_interface)
        default.clean_table_interface()

    def test_register(self):
        body = InterfaceRegisterBody(
            dateConsult="2022-"
            + str(random.randint(1, 12))
            + "-"
            + str(random.randint(1, 28)),
            interfaceType=InterfaceType.NEW.value,
            ip=default.IP,
            community=default.COMMUNITY,
            sysname=default.SYSNAME,
            ifIndex=default.IFINDEX,
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
        status = InterfaceController.register(body)
        self.assertEqual(status, True)
        interface = InterfaceController.get_by_device_type(
            ip=default.IP,
            community=default.COMMUNITY,
            ifIndex=default.IFINDEX,
            type=InterfaceType.NEW.value,
        )
        self.assertEqual(type(interface), dict)
        self.assertEqual(interface[InterfaceSchema.IFINDEX.value], default.IFINDEX)
        self.assertEqual(
            interface[InterfaceSchema.INTERFACE_TYPE.value], InterfaceType.NEW.value
        )
        default.clean_table_interface()

    def test_update(self):
        id_interface = default.register_interface()[1]
        body = InterfaceRegisterBody(
            dateConsult="2025-"
            + str(random.randint(1, 12))
            + "-"
            + str(random.randint(1, 28)),
            interfaceType=InterfaceType.NEW.value,
            ip=default.IP,
            community=default.COMMUNITY,
            sysname=default.SYSNAME,
            ifIndex=default.IFINDEX,
            ifName="test",
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
        status = InterfaceController.update(id_interface, body)
        self.assertEqual(status, True)
        interface = InterfaceController.get_by_id(id_interface)
        self.assertEqual(interface[InterfaceSchema.ID.value], id_interface)
        self.assertEqual(interface[InterfaceSchema.IFNAME.value], "test")
        self.assertEqual(
            interface[InterfaceSchema.INTERFACE_TYPE.value], InterfaceType.NEW.value
        )
        default.clean_table_interface()

    def test_update_type(self):
        id_interface = default.register_interface()[1]
        status = InterfaceController.update_type(id_interface, InterfaceType.OLD.value)
        self.assertEqual(status, True)
        interface = InterfaceController.get_by_id(id_interface)
        self.assertEqual(interface[InterfaceSchema.ID.value], id_interface)
        self.assertEqual(
            interface[InterfaceSchema.INTERFACE_TYPE.value], InterfaceType.OLD.value
        )
        default.clean_table_interface()


if __name__ == "__main__":
    unittest.main()

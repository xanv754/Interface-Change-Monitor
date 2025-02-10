import unittest
import random
from test import default
from constants import (
    EquipmentFields, 
    InterfaceFields
)
from models import (
    EquipmentModel, 
    Equipment,
    InterfaceModel,
    Interface
)

class TestEquipmentQuery(unittest.TestCase):
    def test_register(self):
        model = EquipmentModel("192.172." + str(random.randint(1, 255)) + "." + str(random.randint(1, 255)), "test" + str(random.randint(1, 255)), default.SYSNAME)
        status = model.register()
        self.assertEqual(status, True)

    def test_get_all(self):
        equipments = Equipment.get_all()
        self.assertEqual(type(equipments), list)
        self.assertNotEqual(len(equipments), 0)

    def test_get_all_by_sysname(self):
        model = Equipment(sysname=default.SYSNAME)
        equipments = model.get_all_by_sysname()
        self.assertEqual(type(equipments), list)
        self.assertNotEqual(len(equipments), 0)

    def test_get_by_id(self):
        model = Equipment(id=default.ID_EQUIPMENT)
        equipment = model.get_by_id()
        self.assertEqual(type(equipment), dict)
        self.assertEqual(equipment[EquipmentFields.ID.value], default.ID_EQUIPMENT)

    def test_get_by_device(self):
        model = Equipment(ip=default.IP, community=default.COMMUNITY)
        equipment = model.get_by_device()
        self.assertEqual(type(equipment), dict)
        self.assertEqual(equipment[EquipmentFields.IP.value], default.IP)
        self.assertEqual(equipment[EquipmentFields.COMMUNITY.value], default.COMMUNITY)

    def test_update_sysname(self):
        model = Equipment(ip=default.IP, community=default.COMMUNITY)
        equipment = model.get_by_device()
        id = equipment[EquipmentFields.ID.value]
        status = model.update_sysname(id, default.SYSNAME)
        self.assertEqual(status, True)

    def test_update_community(self):
        model = Equipment(ip=default.IP, community=default.COMMUNITY)
        equipment = model.get_by_device()
        id = equipment[EquipmentFields.ID.value]
        status = model.update_community(id, default.COMMUNITY)
        self.assertEqual(status, True)

    def test_delete(self):
        model = EquipmentModel("to_delete", "to_delete", "to_delete")
        status = model.register()
        self.assertEqual(status, True)
        model = Equipment(ip="to_delete", community="to_delete")
        equipment = model.get_by_device()
        id = equipment[EquipmentFields.ID.value]
        status = model.delete(id)
        self.assertEqual(status, True)


class TestInterfaceQuery(unittest.TestCase):
    def test_register(self):
        model = InterfaceModel(
            ifIndex=random.randint(1, 255),
            idEquipment=default.ID_EQUIPMENT,
            dateConsult="2022-" + str(random.randint(1, 12)) + "-" + str(random.randint(1, 28)),
            ifName="eth0",
            ifDescr="eth0",
            ifAlias="eth0",
            ifSpeed=1000,
            ifHighSpeed=1000,
            ifPhysAddress="00:00:00:00:00:00",
            ifType="ethernet",
            ifOperStatus="up",
            ifAdminStatus="up",
            ifPromiscuousMode=False,
            ifConnectorPresent=False,
            ifLastCheck="2022-01-01",
        )
        status = model.register()
        self.assertEqual(status, True)

    def test_get_all_by_date(self):
        model = Interface(dateConsult=default.DATE_CONSULT)
        interfaces = model.get_all_by_date()
        self.assertEqual(type(interfaces), list)
        self.assertNotEqual(len(interfaces), 0)

    def test_get_by_device_date(self):
        model = Interface(idEquipment=default.ID_EQUIPMENT, ifIndex=default.IFINDEX, dateConsult=default.DATE_CONSULT)
        interface = model.get_by_device_date()
        self.assertEqual(type(interface), dict)
        self.assertEqual(interface[InterfaceFields.ID.value], default.ID_INTERFACE)

    def test_get_by_id(self):
        model = Interface(id=default.ID_INTERFACE)
        interface = model.get_by_id()
        self.assertEqual(type(interface), dict)
        self.assertEqual(interface[InterfaceFields.ID.value], default.ID_INTERFACE)

    def test_delete(self):
        ifIndex = random.randint(1, 255)
        model = InterfaceModel(
            ifIndex=ifIndex,
            idEquipment=default.ID_EQUIPMENT,
            dateConsult=default.DATE_CONSULT,
            ifName="eth0",
            ifDescr="eth0",
            ifAlias="eth0",
            ifSpeed=1000,
            ifHighSpeed=1000,
            ifPhysAddress="00:00:00:00:00:00",
            ifType="ethernet",
            ifOperStatus="up",
            ifAdminStatus="up",
            ifPromiscuousMode=False,
            ifConnectorPresent=False,
            ifLastCheck="2022-01-01",
        )
        status = model.register()
        self.assertEqual(status, True)
        model = Interface(ifIndex=ifIndex, idEquipment=default.ID_EQUIPMENT, dateConsult=default.DATE_CONSULT)
        interface = model.get_by_device_date()
        id = interface[InterfaceFields.ID.value]
        model = Interface(id=id)
        status = model.delete()
        self.assertEqual(status, True)

if __name__ == '__main__':
    unittest.main()
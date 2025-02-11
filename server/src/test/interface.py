import unittest
import random
from constants import InterfaceFields
from models import InterfaceModel, Interface
from test import default

class TestInterfaceQuery(unittest.TestCase):
    def test_register(self):
        id_equipment = default.default_register_equipment()
        model = InterfaceModel(
            ifIndex=random.randint(1, 255),
            idEquipment=id_equipment,
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
        default.clean_table_interface()

    def test_get_all_by_date(self):
        default.default_register_interface()
        model = Interface(dateConsult=default.DATE_CONSULT)
        interfaces = model.get_all_by_date()
        self.assertEqual(type(interfaces), list)
        self.assertNotEqual(len(interfaces), 0)

    def test_get_by_device_date(self):
        id_equipment = default.default_register_interface()[0]
        model = Interface(
            idEquipment=id_equipment, 
            ifIndex=default.IFINDEX, 
            dateConsult=default.DATE_CONSULT
        )
        interfaces = model.get_by_device_date()
        self.assertEqual(type(interfaces), list)
        self.assertEqual(interfaces[0][InterfaceFields.IFINDEX.value], default.IFINDEX)
        self.assertEqual(interfaces[0][InterfaceFields.ID_EQUIPMENT.value], id_equipment)
        self.assertEqual(interfaces[0][InterfaceFields.DATE_CONSULT.value], default.DATE_CONSULT)

    def test_get_by_id(self):
        id_interface = default.default_register_interface()[1]
        model = Interface(id=id_interface)
        interfaces = model.get_by_id()
        self.assertEqual(type(interfaces), list)
        self.assertEqual(interfaces[0][InterfaceFields.ID.value], id_interface)

    def test_delete(self):
        id_equipment = default.default_register_equipment()
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
            ifOperStatus="up",
            ifAdminStatus="up",
            ifPromiscuousMode=False,
            ifConnectorPresent=False,
            ifLastCheck="2022-01-01",
        )
        status = model.register()
        self.assertEqual(status, True)
        model = Interface(ifIndex=ifIndex, idEquipment=id_equipment, dateConsult=default.DATE_CONSULT)
        interfaces = model.get_by_device_date()
        id = interfaces[0][InterfaceFields.ID.value]
        model = Interface(id=id)
        status = model.delete()
        self.assertEqual(status, True)

if __name__ == '__main__':
    unittest.main()
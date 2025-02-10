import unittest
import random
import psycopg2
from test import default
from constants import (
    EquipmentFields, 
    InterfaceFields,
    OperatorFields
)
from models import (
    EquipmentModel, 
    Equipment,
    InterfaceModel,
    Interface,
    OperatorModel,
    Operator
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
        equipments = model.get_by_id()
        self.assertEqual(type(equipments), list)
        self.assertEqual(equipments[0][EquipmentFields.ID.value], default.ID_EQUIPMENT)

    def test_get_by_device(self):
        model = Equipment(ip=default.IP, community=default.COMMUNITY)
        equipments = model.get_by_device()
        self.assertEqual(type(equipments), list)
        self.assertEqual(equipments[0][EquipmentFields.IP.value], default.IP)
        self.assertEqual(equipments[0][EquipmentFields.COMMUNITY.value], default.COMMUNITY)

    def test_update_sysname(self):
        model = Equipment(ip=default.IP, community=default.COMMUNITY)
        equipments = model.get_by_device()
        id = equipments[0][EquipmentFields.ID.value]
        status = model.update_sysname(id, default.SYSNAME)
        self.assertEqual(status, True)

    def test_update_community(self):
        model = Equipment(ip=default.IP, community=default.COMMUNITY)
        equipments = model.get_by_device()
        id = equipments[0][EquipmentFields.ID.value]
        status = model.update_community(id, default.COMMUNITY)
        self.assertEqual(status, True)

    def test_delete(self):
        model = EquipmentModel("to_delete", "to_delete", "to_delete")
        status = model.register()
        self.assertEqual(status, True)
        model = Equipment(ip="to_delete", community="to_delete")
        equipments = model.get_by_device()
        id = equipments[0][EquipmentFields.ID.value]
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
        interfaces = model.get_by_device_date()
        self.assertEqual(type(interfaces), list)
        self.assertEqual(interfaces[0][InterfaceFields.ID.value], default.ID_INTERFACE)

    def test_get_by_id(self):
        model = Interface(id=default.ID_INTERFACE)
        interfaces = model.get_by_id()
        self.assertEqual(type(interfaces), list)
        self.assertEqual(interfaces[0][InterfaceFields.ID.value], default.ID_INTERFACE)

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
        interfaces = model.get_by_device_date()
        id = interfaces[0][InterfaceFields.ID.value]
        model = Interface(id=id)
        status = model.delete()
        self.assertEqual(status, True)

class TestOperatorQuery(unittest.TestCase):
    def test_register(self):
        model = OperatorModel(
            username=default.USERNAME + str(random.randint(1, 255)),
            name="test",
            lastname="user",
            password="secret123456",
            profile="STANDARD",
            statusaccount="ACTIVE",
        )
        status = model.register()
        self.assertEqual(status, True)

    def test_get_all(self):
        users = Operator.get_all()
        self.assertEqual(type(users), list)
        self.assertNotEqual(len(users), 0)

    def test_get_all_profile_active(self):
        users = Operator.get_all_profile_active("STANDARD")
        self.assertEqual(type(users), list)
        self.assertNotEqual(len(users), 0)
        self.assertEqual(users[0][OperatorFields.PROFILE.value], "STANDARD")
        self.assertEqual(users[0][OperatorFields.STATUS_ACCOUNT.value], "ACTIVE")

    def test_get_all_inactive(self):
        model = OperatorModel(
            username=default.USERNAME + str(random.randint(1, 255)),
            name="test",
            lastname="user",
            password="secret123456",
            profile="STANDARD",
            statusaccount="INACTIVE",
        )
        model.register()
        users = Operator.get_all_inactive()
        self.assertEqual(type(users), list)
        self.assertNotEqual(len(users), 0)
        self.assertEqual(users[0][OperatorFields.STATUS_ACCOUNT.value], "INACTIVE")

    def test_get_all_deleted(self):
        model = OperatorModel(
            username=default.USERNAME + str(random.randint(1, 255)),
            name="test",
            lastname="user",
            password="secret123456",
            profile="STANDARD",
            statusaccount="DELETED",
        )
        model.register()
        users = Operator.get_all_deleted()
        self.assertEqual(type(users), list)
        self.assertNotEqual(len(users), 0)
        self.assertEqual(users[0][OperatorFields.STATUS_ACCOUNT.value], "DELETED")

    def test_get(self):
        model = Operator(username=default.USERNAME)
        users = model.get()
        self.assertEqual(type(users), list)
        self.assertEqual(users[0][OperatorFields.USERNAME.value], default.USERNAME)

    def test_delete(self):
        username = "test_delete"
        model = OperatorModel(
            username=username,
            name="test",
            lastname="user",
            password="secret123456",
            profile="STANDARD",
            statusaccount="DELETED",
        )
        model.register()
        model = Operator(username=username)
        status = model.delete()
        self.assertEqual(status, True)

    def test_update(self):
        model = OperatorModel(
            username=default.USERNAME,
            name="unittest",
            lastname="user",
            password="secret123456",
            profile="STANDARD",
            statusaccount="ACTIVE",
        )
        status = model.update()
        self.assertEqual(status, True)

if __name__ == '__main__':
    unittest.main()
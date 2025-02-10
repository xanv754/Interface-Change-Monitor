import unittest
import random
from constants import EquipmentFields
from models import EquipmentModel, Equipment

IP_RANDOM = "192.172." + str(random.randint(1, 255)) + "." + str(random.randint(1, 255))
COMMUNITY_RANDOM = "test" + str(random.randint(1, 255))
ID = 1
IP = "192.168.1.1"
COMMUNITY = "public"
SYSNAME = "Router1"


class TestEquipmentQuery(unittest.TestCase):
    def test_register(self):
        model = EquipmentModel(IP_RANDOM, COMMUNITY_RANDOM, SYSNAME)
        status = model.register()
        self.assertEqual(status, True)

    def test_get_all(self):
        equipments = Equipment.get_all()
        self.assertEqual(type(equipments), list)
        self.assertNotEqual(len(equipments), 0)

    def test_get_all_by_sysname(self):
        model = Equipment(sysname=SYSNAME)
        equipments = model.get_all_by_sysname()
        self.assertEqual(type(equipments), list)
        self.assertNotEqual(len(equipments), 0)

    def test_get_by_id(self):
        model = Equipment(id=ID)
        equipment = model.get_by_id()
        self.assertEqual(type(equipment), dict)
        self.assertEqual(equipment[EquipmentFields.ID.value], ID)

    def test_get_by_device(self):
        model = Equipment(ip=IP, community=COMMUNITY)
        equipment = model.get_by_device()
        self.assertEqual(type(equipment), dict)
        self.assertEqual(equipment[EquipmentFields.IP.value], IP)
        self.assertEqual(equipment[EquipmentFields.COMMUNITY.value], COMMUNITY)

if __name__ == '__main__':
    unittest.main()
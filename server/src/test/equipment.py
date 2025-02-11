import unittest
import random
from constants import EquipmentFields
from models import EquipmentModel, Equipment
from test import default

class TestEquipmentQuery(unittest.TestCase):
    def test_get_by_id(self):
        id = default.default_register_equipment()
        model = Equipment(id=id)
        equipments = model.get_by_id()
        self.assertEqual(type(equipments), list)
        self.assertEqual(equipments[0][EquipmentFields.ID.value], id)

    def test_get_by_device(self):
        default.default_register_equipment()
        model = Equipment(ip=default.IP, community=default.COMMUNITY)
        equipments = model.get_by_device()
        self.assertEqual(type(equipments), list)
        self.assertEqual(equipments[0][EquipmentFields.IP.value], default.IP)
        self.assertEqual(equipments[0][EquipmentFields.COMMUNITY.value], default.COMMUNITY)

    def test_register(self):
        model = EquipmentModel(
            ip="192.172." + str(random.randint(1, 255)) + "." + str(random.randint(1, 255)), 
            community="test" + str(random.randint(1, 255)), 
            sysname=default.SYSNAME
        )
        status = model.register()
        self.assertEqual(status, True)
        default.clean_table_equipment()

    def test_get_all(self):
        default.default_register_equipment()
        equipments = Equipment.get_all()
        self.assertEqual(type(equipments), list)
        self.assertNotEqual(len(equipments), 0)

    def test_get_all_by_sysname(self):
        default.default_register_equipment()
        model = Equipment(sysname=default.SYSNAME)
        equipments = model.get_all_by_sysname()
        self.assertEqual(type(equipments), list)
        self.assertNotEqual(len(equipments), 0)

    def test_update_sysname(self):
        default.default_register_equipment()
        model = Equipment(ip=default.IP, community=default.COMMUNITY)
        equipments = model.get_by_device()
        id = equipments[0][EquipmentFields.ID.value]
        model = Equipment(id=id)
        status = model.update_sysname(default.SYSNAME)
        self.assertEqual(status, True)

    def test_update_community(self):
        default.default_register_equipment()
        model = Equipment(ip=default.IP, community=default.COMMUNITY)
        equipments = model.get_by_device()
        id = equipments[0][EquipmentFields.ID.value]
        model = Equipment(id=id)
        status = model.update_community(default.COMMUNITY)
        self.assertEqual(status, True)

    def test_delete(self):
        model = EquipmentModel("to_delete", "to_delete", "to_delete")
        status = model.register()
        self.assertEqual(status, True)
        model = Equipment(ip="to_delete", community="to_delete")
        equipments = model.get_by_device()
        id = equipments[0][EquipmentFields.ID.value]
        model = Equipment(id=id)
        status = model.delete()
        self.assertEqual(status, True)


if __name__ == '__main__':
    unittest.main()
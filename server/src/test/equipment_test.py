import unittest
import random
from controllers import EquipmentController
from database import EquipmentSchema
from models import EquipmentModel, Equipment, EquipmentRegisterRequest
from test import default


class TestEquipmentQuery(unittest.TestCase):
    def test_get_by_id(self):
        id = default.register_equipment()
        model = Equipment(id=id)
        equipment = model.get_by_id()
        self.assertEqual(type(equipment), dict)
        self.assertEqual(equipment[EquipmentSchema.ID.value], id)
        default.clean_table_equipment()

    def test_get_by_device(self):
        default.register_equipment()
        model = Equipment(ip=default.IP, community=default.COMMUNITY)
        equipment = model.get_by_device()
        self.assertEqual(type(equipment), dict)
        self.assertEqual(equipment[EquipmentSchema.IP.value], default.IP)
        self.assertEqual(equipment[EquipmentSchema.COMMUNITY.value], default.COMMUNITY)
        default.clean_table_equipment()

    def test_register(self):
        model = EquipmentModel(
            ip="192.172."
            + str(random.randint(1, 255))
            + "."
            + str(random.randint(1, 255)),
            community="test" + str(random.randint(1, 255)),
        )
        status = model.register()
        self.assertEqual(status, True)
        default.clean_table_equipment()

    def test_get_all(self):
        default.register_equipment()
        equipments = Equipment.get_all()
        self.assertEqual(type(equipments), list)
        self.assertNotEqual(len(equipments), 0)
        default.clean_table_equipment()

    def test_get_all_by_sysname(self):
        default.register_equipment()
        model = Equipment(sysname=default.SYSNAME)
        equipments = model.get_all_by_sysname()
        self.assertEqual(type(equipments), list)
        self.assertNotEqual(len(equipments), 0)
        default.clean_table_equipment()

    def test_update_sysname(self):
        default.register_equipment()
        model = Equipment(ip=default.IP, community=default.COMMUNITY)
        status = model.update_sysname(default.SYSNAME)
        self.assertEqual(status, True)
        default.clean_table_equipment()

    def test_update_community(self):
        default.register_equipment()
        model = Equipment(ip=default.IP, community=default.COMMUNITY)
        equipment = model.get_by_device()
        id = equipment[EquipmentSchema.ID.value]
        model = Equipment(id=id)
        status = model.update_community(default.COMMUNITY)
        self.assertEqual(status, True)
        default.clean_table_equipment()

    def test_delete(self):
        model = EquipmentModel("to_delete", "to_delete")
        status = model.register()
        self.assertEqual(status, True)
        model = Equipment(ip="to_delete", community="to_delete")
        equipment = model.get_by_device()
        id = equipment[EquipmentSchema.ID.value]
        model = Equipment(id=id)
        status = model.delete()
        self.assertEqual(status, True)


class TestEquipmentController(unittest.TestCase):
    def test_get_equipment(self):
        default.register_equipment()
        model = EquipmentController.get_equipment(default.IP, default.COMMUNITY)
        self.assertEqual(type(model), dict)
        self.assertEqual(model[EquipmentSchema.IP.value], default.IP)
        self.assertEqual(model[EquipmentSchema.COMMUNITY.value], default.COMMUNITY)
        default.clean_table_equipment()

    def test_register(self):
        model = EquipmentRegisterRequest(
            ip="192.172."
            + str(random.randint(1, 255))
            + "."
            + str(random.randint(1, 255)),
            community="test" + str(random.randint(1, 255)),
        )
        status = EquipmentController.register(model)
        self.assertEqual(status, True)
        default.clean_table_equipment()

    def test_get_all(self):
        default.register_equipment()
        equipments = EquipmentController.get_all()
        self.assertEqual(type(equipments), list)
        self.assertNotEqual(len(equipments), 0)
        default.clean_table_equipment()

    def test_update_sysname(self):
        default.register_equipment()
        status = EquipmentController.update_sysname(
            default.IP, default.COMMUNITY, "test_sysname"
        )
        self.assertEqual(status, True)
        default.clean_table_equipment()

    def test_update_community(self):
        id = default.register_equipment()
        status = EquipmentController.update_community(id, "test_community")
        self.assertEqual(status, True)
        default.clean_table_equipment()


if __name__ == "__main__":
    unittest.main()

import unittest
import random
from controllers import EquipmentController
from models import EquipmentModel, Equipment
from schemas import EquipmentResponseSchema, EquipmentRegisterBody
from test import constants, DefaultEquipment


class TestEquipmentModel(unittest.TestCase):
    def test_register(self):
        DefaultEquipment.clean_table()
        new_ip="192.172." + str(random.randint(1, 255)) + "." + str(random.randint(1, 255))
        new_community="test" + str(random.randint(1, 255))
        model = EquipmentModel(ip=new_ip,community=new_community)
        status = model.register()
        self.assertEqual(status, True)
        new_equipment = DefaultEquipment.select_one_by_device(ip=new_ip, community=new_community)
        self.assertEqual(new_equipment.ip, new_ip)
        self.assertEqual(new_equipment.community, new_community)
        DefaultEquipment.clean_table()

    def test_get_all(self):
        new_equipment = DefaultEquipment.new_insert()
        equipments = Equipment.get_all()
        self.assertEqual(type(equipments), list)
        self.assertNotEqual(len(equipments), 0)
        self.assertEqual(equipments[0].id, new_equipment.id)
        DefaultEquipment.clean_table()

    def test_get_all_by_sysname(self):
        new_equipment = DefaultEquipment.new_insert()
        model = Equipment(sysname=new_equipment.sysname)
        equipments = model.get_all_by_sysname()
        self.assertEqual(type(equipments), list)
        self.assertNotEqual(len(equipments), 0)
        self.assertEqual(equipments[0].id, new_equipment.id)
        DefaultEquipment.clean_table()

    def test_get_by_id(self):
        new_equipment = DefaultEquipment.new_insert()
        model = Equipment(id=new_equipment.id)
        equipment = model.get_by_id()
        self.assertEqual(type(equipment), EquipmentResponseSchema)
        self.assertEqual(equipment.id, new_equipment.id)
        model = Equipment(id="0")
        equipment = model.get_by_id()
        self.assertIsNone(equipment)
        DefaultEquipment.clean_table()

    def test_get_by_device(self):
        new_equipment = DefaultEquipment.new_insert()
        model = Equipment(ip=new_equipment.ip, community=new_equipment.community)
        equipment = model.get_by_ip_community()
        self.assertEqual(type(equipment), EquipmentResponseSchema)
        self.assertEqual(equipment.id, new_equipment.id)
        self.assertEqual(equipment.ip, new_equipment.ip)
        self.assertEqual(equipment.community, new_equipment.community)
        DefaultEquipment.clean_table()

    def test_update_sysname(self):
        equipment = DefaultEquipment.new_insert()
        model = Equipment(ip=equipment.ip, community=equipment.community)
        status = model.update_sysname(sysname=constants.SYSNAME_TWO)
        self.assertEqual(status, True)
        self.assertEqual(
            DefaultEquipment.select_one_by_id(equipment.id).sysname, 
            constants.SYSNAME_TWO
        )
        DefaultEquipment.clean_table()

    def test_update_community(self):
        equipment = DefaultEquipment.new_insert()
        model = Equipment(id=equipment.id)
        status = model.update_community(community=constants.COMMUNITY_TWO)
        self.assertEqual(status, True)
        self.assertEqual(
            DefaultEquipment.select_one_by_id(equipment.id).community, 
            constants.COMMUNITY_TWO
        )
        DefaultEquipment.clean_table()

    def test_delete(self):
        equipment = DefaultEquipment.new_insert()
        model = Equipment(id=equipment.id)
        status = model.delete()
        self.assertEqual(status, True)
        self.assertIsNone(DefaultEquipment.select_one_by_id(equipment.id))
        DefaultEquipment.clean_table()


class TestEquipmentController(unittest.TestCase):
    def test_ensure_equipment(self):
        new_equipment = DefaultEquipment.new_insert()
        equipment = EquipmentController.ensure_equipment(
            ip=new_equipment.ip, 
            community=new_equipment.community, 
            sysname=new_equipment.sysname
        )
        self.assertEqual(type(equipment), EquipmentResponseSchema)
        self.assertEqual(equipment.id, new_equipment.id)
        new_equipment = DefaultEquipment.new_insert(
            ip="0.0.0.0",
            community="unit@test",
            sysname="UnitTest"
        )
        equipment = EquipmentController.ensure_equipment(
            ip=new_equipment.ip, 
            community=new_equipment.community, 
            sysname=new_equipment.sysname
        )
        self.assertEqual(type(equipment), EquipmentResponseSchema)
        self.assertEqual(equipment.ip, new_equipment.ip)
        self.assertEqual(equipment.community, new_equipment.community)
        self.assertEqual(equipment.sysname, new_equipment.sysname)
        DefaultEquipment.clean_table()

    def test_create_and_register(self):
        ip = "0.0.0.0"
        community = "unit@test"
        sysname = "UnitTest"
        equipment = EquipmentController.create_and_register(
            ip=ip, 
            community=community, 
            sysname=sysname
        )
        self.assertEqual(type(equipment), EquipmentResponseSchema)
        self.assertEqual(equipment.ip, ip)
        self.assertEqual(equipment.community, community)
        self.assertEqual(equipment.sysname, sysname)
        DefaultEquipment.clean_table()

    def test_register(self):
        new_ip = "192.172." + str(random.randint(1, 255)) + "." + str(random.randint(1, 255))
        new_community = "test" + str(random.randint(1, 255))
        body = EquipmentRegisterBody(
            ip=new_ip,
            community=new_community
        )
        status = EquipmentController.register(body)
        self.assertEqual(status, True)
        new_equipment = DefaultEquipment.select_one_by_device(ip=new_ip, community=new_community)
        self.assertEqual(new_equipment.ip, new_ip)
        self.assertEqual(new_equipment.community, new_community)
        DefaultEquipment.clean_table()

    def test_get_equipment(self):
        new_equipment = DefaultEquipment.new_insert()
        equipment = EquipmentController.get_equipment_device_without_sysname(ip=new_equipment.ip, community=new_equipment.community)
        self.assertEqual(type(equipment), EquipmentResponseSchema)
        self.assertEqual(equipment.ip, new_equipment.ip)
        self.assertEqual(equipment.community, new_equipment.community)
        DefaultEquipment.clean_table()

    def test_get_equipment_by_id(self):
        new_equipment = DefaultEquipment.new_insert()
        equipment = EquipmentController.get_equipment_by_id(id_equipment=new_equipment.id)
        self.assertEqual(type(equipment), EquipmentResponseSchema)
        self.assertEqual(equipment.id, new_equipment.id)
        DefaultEquipment.clean_table()

    def test_get_all(self):
        new_equipment = DefaultEquipment.new_insert()
        equipments = EquipmentController.get_all()
        self.assertEqual(type(equipments), list)
        self.assertNotEqual(len(equipments), 0)
        self.assertEqual(equipments[0].id, new_equipment.id)
        DefaultEquipment.clean_table()

    def test_update_sysname(self):
        new_equipment = DefaultEquipment.new_insert()
        status = EquipmentController.update_sysname(
            ip=new_equipment.ip,
            community=new_equipment.community,
            sysname=constants.SYSNAME_TWO
        )
        self.assertEqual(status, True)
        self.assertEqual(
            DefaultEquipment.select_one_by_id(new_equipment.id).sysname, 
            constants.SYSNAME_TWO
        )
        DefaultEquipment.clean_table()

    def test_update_community(self):
        new_equipment = DefaultEquipment.new_insert()
        status = EquipmentController.update_community(
            id_equipment=new_equipment.id,
            community_new=constants.COMMUNITY_TWO
        )
        self.assertEqual(status, True)
        self.assertEqual(
            DefaultEquipment.select_one_by_id(new_equipment.id).community, 
            constants.COMMUNITY_TWO
        )
        DefaultEquipment.clean_table()


if __name__ == "__main__":
    unittest.main()

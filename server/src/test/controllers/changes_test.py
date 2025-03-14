import unittest
from typing import List
from constants import InterfaceType
from controllers import ChangeController
from schemas import ChangeInterfaceSchema, RegisterChangeBody
from test import constants, DefaultInterface, DefaultOperator, DefaultEquipment, DefaultChangesPostgresDB
from models import Change, ChangeModel


# class TestChangesController(unittest.TestCase):
#     def test_get_all_changes(self):
#         new_changes = DefaultChangesRedisDB.get_changes()
#         status = DefaultChangesRedisDB.new_insert(id=1, changes=new_changes[0])
#         self.assertEqual(status, True)
#         changes = SystemController.get_all_changes()
#         self.assertEqual(type(changes), list)
#         self.assertEqual(len(changes), 1)
#         self.assertEqual(changes[0].ip, new_changes[0].ip)
#         self.assertEqual(changes[0].community, new_changes[0].community)
#         DefaultChangesRedisDB.clean_table()

#     def test_register_change(self):
#         new_changes = DefaultChangesRedisDB.get_changes()
#         status = SystemController.register_change(id=1, changes=new_changes[0])
#         self.assertEqual(status, True)
#         DefaultChangesRedisDB.clean_table()

class TestChangeController(unittest.TestCase):
    def test_register(self):
        pass

    def test_get_all_changes(self):
        DefaultChangesPostgresDB.new_insert()
        changes = ChangeController.get_all_changes()
        self.assertEqual(type(changes), list)
        self.assertNotEqual(len(changes), 0)
        DefaultChangesPostgresDB.clean_table()

    def test_update_operator(self):
        pass

    def test_delete(self):
        status = ChangeController.delete()
        self.assertEqual(status, True)
        
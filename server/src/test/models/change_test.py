import unittest
from typing import List
from constants import InterfaceType
from database import Change, ChangeModel
from schemas import ChangeInterfaceSchema, RegisterChangeBody
from test import constants, DefaultInterface, DefaultOperator, DefaultEquipment, DefaultChangesPostgresDB


# class TestChangesRedisDB(unittest.TestCase):
#     def test_get_change(self):
#         data_changes = DefaultChangesRedisDB.get_changes()
#         changes = ChangesModelRedis(id=1, changes=data_changes[0])
#         current_change = changes.get_changes()
#         self.assertEqual(type(current_change), str)

#     def test_register_changes(self):
#         changes = DefaultChangesRedisDB.get_changes()
#         self.assertEqual(type(changes), list)
#         self.assertEqual(len(changes), 1)
#         changes = ChangesModelRedis(id=1, changes=changes[0])
#         status = changes.register()
#         self.assertEqual(status, True)
#         DefaultChangesRedisDB.clean_table()

#     def test_get_all_changes(self):
#         new_changes = DefaultChangesRedisDB.get_changes()
#         status = DefaultChangesRedisDB.new_insert(id=1, changes=new_changes[0])
#         self.assertEqual(status, True)
#         changes = ChangesModelRedis.get_all_changes()
#         self.assertEqual(type(changes), list)
#         self.assertEqual(len(changes), 1)
#         self.assertEqual(changes[0].ip, new_changes[0].ip)
#         self.assertEqual(changes[0].community, new_changes[0].community)
#         DefaultChangesRedisDB.clean_table()

#     def test_reset_changes(self):
#         new_changes = DefaultChangesRedisDB.get_changes()
#         status = DefaultChangesRedisDB.new_insert(id=1, changes=new_changes[0])
#         self.assertEqual(status, True)
#         status = ChangesModelRedis.reset_changes()
#         self.assertEqual(status, True)
#         changes = ChangesModelRedis.get_all_changes()
#         self.assertEqual(type(changes), list)
#         self.assertEqual(len(changes), 0)


class TestChangeModelPostgres(unittest.TestCase):
    def test_register(self):
        DefaultChangesPostgresDB.clean_table()
        equipment = DefaultEquipment.new_insert()
        old_interface = DefaultInterface.new_insert(
            clean=False,
            equipment=equipment,
            date=constants.DATE_CONSULT,
            interface_type=InterfaceType.OLD.value,
            ifIndex=constants.IFINDEX
        )
        new_interface = DefaultInterface.new_insert(
            clean=False,
            equipment=equipment,
            date=constants.DATE_CONSULT_TWO,
            interface_type=InterfaceType.NEW.value,
            ifIndex=constants.IFINDEX,
            ifName=constants.IFNAME_TWO
        )
        new_change = RegisterChangeBody(
            oldInterface=old_interface.id,
            newInterface=new_interface.id,
        )
        status = ChangeModel.register(changes=[new_change])
        self.assertEqual(status, True)
        DefaultChangesPostgresDB.clean_table()

    def test_get_all_changes(self):
        new_change = DefaultChangesPostgresDB.new_insert()
        changes: List[ChangeInterfaceSchema] = Change.get_all_changes()
        self.assertEqual(type(changes), list)
        self.assertNotEqual(len(changes), 0)
        self.assertEqual(changes[0].id, new_change.id)
        DefaultChangesPostgresDB.clean_table()

    def test_reset_changes(self):
        status = Change.reset_changes()
        self.assertEqual(status, True)

    def test_update_assigned(self):
        new_change = DefaultChangesPostgresDB.new_insert()
        new_operator = DefaultOperator.new_insert(
            clean=False
        )
        model = Change(new_operator.username)
        status = model.update_assigned(ids=[new_change.id])
        self.assertEqual(status, True)
        DefaultChangesPostgresDB.clean_table()

import unittest
from constants import InterfaceType
from controllers import ChangeController
from schemas import RegisterChangeBody
from test import DefaultInterface, DefaultEquipment, DefaultOperator, DefaultChangesPostgresDB, constants as testConstants


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
        DefaultChangesPostgresDB.clean_table()
        equipment = DefaultEquipment.new_insert()
        old_interface = DefaultInterface.new_insert(
            clean=False,
            equipment=equipment,
            date=testConstants.DATE_CONSULT,
            interface_type=InterfaceType.OLD.value,
            ifIndex=testConstants.IFINDEX
        )
        new_interface = DefaultInterface.new_insert(
            clean=False,
            equipment=equipment,
            date=testConstants.DATE_CONSULT_TWO,
            interface_type=InterfaceType.NEW.value,
            ifIndex=testConstants.IFINDEX,
            ifName=testConstants.IFNAME_TWO
        )
        new_change = RegisterChangeBody(
            oldInterface=old_interface.id,
            newInterface=new_interface.id,
        )
        status = ChangeController.register(changes=[new_change])
        self.assertEqual(status, True)
        DefaultChangesPostgresDB.clean_table()

    def test_get_all_changes(self):
        DefaultChangesPostgresDB.new_insert()
        changes = ChangeController.get_all_changes()
        self.assertEqual(type(changes), list)
        self.assertNotEqual(len(changes), 0)
        DefaultChangesPostgresDB.clean_table()

    def test_update_operator(self):
        new_change = DefaultChangesPostgresDB.new_insert()
        DefaultOperator.new_insert(
            clean=False,
            username=testConstants.USERNAME_ALTERNATIVE
        )
        ids = [new_change.id]
        status = ChangeController.update_operator(ids=ids, operator=testConstants.USERNAME_ALTERNATIVE)
        self.assertEqual(status, True)
        DefaultChangesPostgresDB.clean_table()

    def test_delete(self):
        status = ChangeController.delete()
        self.assertEqual(status, True)
        
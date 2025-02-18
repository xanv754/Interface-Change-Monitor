import unittest
from models import Changes
from test import DefaultChanges

class TestChanges(unittest.TestCase):
    def test_get_change(self):
        data_changes = DefaultChanges.get_changes()
        changes = Changes(id=1, changes=data_changes[0])
        current_change = changes.get_changes()
        self.assertEqual(type(current_change), str)

    def test_register_changes(self):
        DefaultChanges.clean_table()
        changes = DefaultChanges.get_changes()
        self.assertEqual(type(changes), list)
        self.assertEqual(len(changes), 1)
        changes = Changes(id=1, changes=changes[0])
        status = changes.register()
        self.assertEqual(status, True)
        DefaultChanges.clean_table()

    def test_get_all_changes(self):
        DefaultChanges.clean_table()
        new_changes = DefaultChanges.get_changes()
        status = DefaultChanges.new_insert(id=1, changes=new_changes[0])
        self.assertEqual(status, True)
        changes = Changes.get_all_changes()
        self.assertEqual(type(changes), list)
        self.assertEqual(len(changes), 1)
        self.assertEqual(changes[0].ip, new_changes[0].ip)
        self.assertEqual(changes[0].community, new_changes[0].community)
        DefaultChanges.clean_table()

    def test_reset_changes(self):
        DefaultChanges.clean_table()
        new_changes = DefaultChanges.get_changes()
        status = DefaultChanges.new_insert(id=1, changes=new_changes[0])
        self.assertEqual(status, True)
        status = Changes.reset_changes()
        self.assertEqual(status, True)
        changes = Changes.get_all_changes()
        self.assertEqual(type(changes), list)
        self.assertEqual(len(changes), 0)
        


if __name__ == "__main__":  
    unittest.main()
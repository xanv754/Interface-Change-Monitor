import unittest
from models import Changes
from test import DefaultChanges

class TestChanges(unittest.TestCase):
    def test_get_change(self):
        data_changes = DefaultChanges.new_insert()
        changes = Changes(id=1, changes=data_changes[0])
        current_change = changes.get_changes()
        self.assertEqual(type(current_change), dict)

    def test_register_changes(self):
        changes = DefaultChanges.new_insert()
        self.assertEqual(type(changes), list)
        changes = Changes(id=1, changes=changes[0])
        status = changes.register()
        self.assertEqual(status, True)


if __name__ == "__main__":  
    unittest.main()
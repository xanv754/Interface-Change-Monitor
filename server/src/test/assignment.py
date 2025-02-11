import unittest
from test import default
from models import AssignmentModel, Assignment


class TestAssignmentQuery(unittest.TestCase):
    def test_register(self):
        default.register_operator()
        ids = default.register_interface(clean=False)
        id_equipment = ids[0]
        id_interface_one = ids[1]
        id_interface_two = default.register_interface(
            clean=False, id_equipment=id_equipment, date_consult="2024-01-02"
        )[1]
        model = AssignmentModel(
            change_interface=id_interface_one,
            old_interface=id_interface_two,
            operator=default.USERNAME,
            date_assignment=default.DATE_CONSULT,
            status_assignment="PENDING",
            assigned_by=default.USERNAME,
        )
        status = model.register()
        self.assertEqual(status, True)
        default.clean_table_assignment()

    def test_get_all_by_operator(self):
        default.register_assignment()
        model = Assignment(username=default.USERNAME)
        assignments = model.get_all_by_operator()
        self.assertEqual(type(assignments), list)
        self.assertNotEqual(len(assignments), 0)
        default.clean_table_assignment()

    def test_get_all_by_status(self):
        default.register_assignment()
        model = Assignment(username=default.USERNAME)
        assignments = model.get_all_by_status("PENDING")
        self.assertEqual(type(assignments), list)
        self.assertNotEqual(len(assignments), 0)
        default.clean_table_assignment()
    
    def test_update_operator(self):
        id_assignment = default.register_assignment()[2]
        model = Assignment(id=id_assignment)
        default.register_operator(clean=False, username="test")
        status = model.update_operator("test", "unittest")
        self.assertEqual(status, True)
        default.clean_table_assignment()

    def test_update_status(self):
        id_assignment = default.register_assignment()[2]
        model = Assignment(id=id_assignment)
        status = model.update_status("REDISCOVERED")
        self.assertEqual(status, True)
        default.clean_table_assignment()

    def test_delete(self):
        id_assignment = default.register_assignment()[2]
        model = Assignment(id=id_assignment)
        status = model.delete()
        self.assertEqual(status, True)

if __name__ == "__main__":
    unittest.main()

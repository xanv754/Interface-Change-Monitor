import unittest
from constants import StatusAssignmentType, InterfaceType
from controllers import OperatorController
from models import AssignmentModel, Assignment, AssignmentRegisterRequest
from schemas import AssignmentSchema
from test import default


class TestAssignmentModel(unittest.TestCase):
    def test_register(self):
        default.register_operator()
        ids = default.register_interface(clean=False, interface_type=InterfaceType.OLD.value)
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
            status_assignment=StatusAssignmentType.PENDING.value,
            assigned_by=default.USERNAME,
        )
        status = model.register()
        self.assertEqual(status, True)
        default.clean_table_assignment()

    def test_get_all_by_operator(self):
        default.register_assignment()
        model = Assignment(operator=default.USERNAME)
        assignments = model.get_all_by_operator()
        self.assertEqual(type(assignments), list)
        self.assertNotEqual(len(assignments), 0)
        default.clean_table_assignment()

    def test_get_all_by_status(self):
        default.register_assignment()
        model = Assignment(operator=default.USERNAME)
        assignments = model.get_all_by_status(StatusAssignmentType.PENDING.value)
        self.assertEqual(type(assignments), list)
        self.assertNotEqual(len(assignments), 0)
        default.clean_table_assignment()

    def test_get_assignment_by_interface(self):
        default.register_operator()
        ids = default.register_interface(clean=False, interface_type=InterfaceType.OLD.value)
        id_equipment = ids[0]
        id_interface_one = ids[1]
        id_interface_two = default.register_interface(
            clean=False, id_equipment=id_equipment, date_consult="2024-01-02"
        )[1]
        model = AssignmentModel(
            change_interface=id_interface_one,
            old_interface=id_interface_two,
            operator=default.USERNAME,
            date_assignment="2024-01-01",
            status_assignment=StatusAssignmentType.PENDING.value,
            assigned_by=default.USERNAME,
        )
        model.register()
        model = Assignment(
            id_change_interface=id_interface_one,
            id_old_interface=id_interface_two,
            operator=default.USERNAME,
        )
        assignment = model.get_assignment_by_interface()
        self.assertEqual(type(assignment), dict)
        self.assertEqual(assignment[AssignmentSchema.CHANGE_INTERFACE.value], id_interface_one)
        self.assertEqual(assignment[AssignmentSchema.OLD_INTERFACE.value], id_interface_two)
        self.assertEqual(assignment[AssignmentSchema.OPERATOR.value], default.USERNAME)
    
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
        status = model.update_status(StatusAssignmentType.REDISCOVERED.value)
        self.assertEqual(status, True)
        default.clean_table_assignment()

    def test_delete(self):
        id_assignment = default.register_assignment()[2]
        model = Assignment(id=id_assignment)
        status = model.delete()
        self.assertEqual(status, True)


class TestAssignmentController(unittest.TestCase):
    def test_new_assignment(self):
        default.register_operator()
        ids = default.register_interface(clean=False, interface_type=InterfaceType.OLD.value)
        id_equipment = ids[0]
        id_interface_one = ids[1]
        id_interface_two = default.register_interface(
            clean=False, id_equipment=id_equipment, date_consult="2024-01-02"
        )[1]
        body = AssignmentRegisterRequest(
            change_interface=id_interface_two,
            old_interface=id_interface_one,
            operator=default.USERNAME,
            assigned_by="unittest",
        )
        status = OperatorController.new_assignment(body)
        self.assertEqual(status, True)
        status = OperatorController.new_assignment(body)
        self.assertEqual(status, False)
        default.clean_table_assignment()

    def test_get_assignments(self):
        default.register_assignment()
        assignments = OperatorController.get_assignments(default.USERNAME)
        self.assertEqual(type(assignments), list)
        self.assertNotEqual(len(assignments), 0)
        self.assertEqual(assignments[0][AssignmentSchema.OPERATOR.value], default.USERNAME)
        self.assertEqual(assignments[0][AssignmentSchema.STATUS_ASSIGNMENT.value], StatusAssignmentType.PENDING.value)
        default.clean_table_assignment()

    def test_get_all_assignments(self):
        default.register_assignment()
        assignments = OperatorController.get_all_assignments(default.USERNAME)
        self.assertEqual(type(assignments), list)
        self.assertNotEqual(len(assignments), 0)
        self.assertEqual(assignments[0][AssignmentSchema.OPERATOR.value], default.USERNAME)
        default.clean_table_assignment()


if __name__ == "__main__":
    unittest.main()

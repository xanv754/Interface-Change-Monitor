import unittest
from constants import StatusAssignmentType, InterfaceType
from controllers import OperatorController
from models import AssignmentModel, Assignment
from schemas import AssignmentSchema,AssignmentRegisterBody, AssignmentsCountResponse, AssignmentReassignBody
from test import constants, DefaultInterface, DefaultOperator, DefaultEquipment, DefaultAssignment


class TestAssignmentModel(unittest.TestCase):
    def test_register(self):
        new_operator = DefaultOperator.new_insert()
        new_equipment = DefaultEquipment.new_insert()
        new_interface_old_version = DefaultInterface.new_insert(
            clean=False,
            interface_type=InterfaceType.OLD.value,
            equipment=new_equipment
        )
        new_interface_new_version = DefaultInterface.new_insert(
            clean=False,
            equipment=new_equipment,
            date=constants.DATE_CONSULT_TWO,
        )
        model = AssignmentModel(
            change_interface=new_interface_new_version.id,
            old_interface=new_interface_old_version.id,
            operator=new_operator.username,
            date_assignment=constants.DATE_ALTERNATIVE,
            status_assignment=StatusAssignmentType.PENDING.value,
            assigned_by=constants.USERNAME_ALTERNATIVE,
        )
        status = model.register()
        self.assertEqual(status, True)
        new_assignment = DefaultAssignment.select_one_by_data(
            id_change_interface=new_interface_new_version.id,
            id_old_interface=new_interface_old_version.id,
            operator=new_operator.username
        )
        self.assertEqual(type(new_assignment), AssignmentSchema)
        self.assertEqual(new_assignment.new_interface, new_interface_new_version.id)
        self.assertEqual(new_assignment.old_interface, new_interface_old_version.id)
        self.assertEqual(new_assignment.operator, new_operator.username)
        DefaultAssignment.clean_table()

    def test_get_count_all_pending(self):
        DefaultAssignment.new_insert()
        count = Assignment.get_count_all_pending()
        self.assertEqual(count, 1)
        DefaultAssignment.clean_table()

    def test_get_count_all_revised(self):
        DefaultAssignment.new_insert(
            status_assignment=StatusAssignmentType.REDISCOVERED.value
        )
        count = Assignment.get_count_all_revised()
        self.assertEqual(count, 1)
        DefaultAssignment.clean_table()

    def test_get_all_by_status(self):
        new_status_assignment = StatusAssignmentType.REDISCOVERED.value
        new_assignment = DefaultAssignment.new_insert(
            status_assignment=new_status_assignment
        )
        assignments = Assignment.get_all_by_status(new_status_assignment)
        self.assertEqual(type(assignments), list)
        self.assertNotEqual(len(assignments), 0)
        self.assertEqual(assignments[0].id, new_assignment.id)
        self.assertEqual(assignments[0].status, new_status_assignment)
        DefaultAssignment.clean_table()

    def test_get_count_pending_by_operator(self):
        new_operator = DefaultOperator.new_insert()
        DefaultAssignment.new_insert(
            username_operator=new_operator.username,
            status_assignment=StatusAssignmentType.PENDING.value
        )
        model = Assignment(operator=new_operator.username)
        count = model.get_count_pending_by_operator()
        self.assertEqual(count, 1)
        DefaultAssignment.clean_table()

    def test_get_count_revised_by_operator(self):
        new_operator = DefaultOperator.new_insert()
        DefaultAssignment.new_insert(
            username_operator=new_operator.username,
            status_assignment=StatusAssignmentType.REDISCOVERED.value
        )
        model = Assignment(operator=new_operator.username)
        count = model.get_count_revised_by_operator()
        self.assertEqual(count, 1)
        DefaultAssignment.clean_table()

    def test_get_all_status_by_operator(self):
        new_status_assignment = StatusAssignmentType.REDISCOVERED.value
        new_assignment = DefaultAssignment.new_insert(
            status_assignment=new_status_assignment
        )
        model = Assignment(operator=new_assignment.operator)
        assignments = model.get_all_status_by_operator(status=new_status_assignment)
        self.assertEqual(type(assignments), list)
        self.assertNotEqual(len(assignments), 0)
        self.assertEqual(assignments[0].id, new_assignment.id)
        self.assertEqual(assignments[0].status, new_status_assignment)
        DefaultAssignment.clean_table()

    def test_get_all_by_operator(self):
        new_assignment = DefaultAssignment.new_insert()
        model = Assignment(operator=new_assignment.operator)
        assignments = model.get_all_by_operator()
        self.assertEqual(type(assignments), list)
        self.assertNotEqual(len(assignments), 0)
        self.assertEqual(assignments[0].id, new_assignment.id)
        DefaultAssignment.clean_table()

    def test_get_assignment_by_interface(self):
        new_assignment = DefaultAssignment.new_insert()
        model = Assignment(
            id_change_interface=new_assignment.new_interface,
            id_old_interface=new_assignment.old_interface,
            operator=new_assignment.operator,
        )
        assignment = model.get_assignment_by_interface()
        self.assertEqual(type(assignment), AssignmentSchema)
        self.assertEqual(assignment.id, new_assignment.id)
        DefaultAssignment.clean_table()

    def test_get_by_id(self):
        new_assignment = DefaultAssignment.new_insert()
        model = Assignment(id=new_assignment.id)
        assignment = model.get_by_id()
        self.assertEqual(type(assignment), AssignmentSchema)
        self.assertEqual(assignment.id, new_assignment.id)
        DefaultAssignment.clean_table()

    def test_update_operator(self):
        new_assignment = DefaultAssignment.new_insert()
        new_operator = DefaultOperator.new_insert(
            clean=False,
            username=constants.USERNAME_TWO
        )
        model = Assignment(id=new_assignment.id)
        status = model.update_operator(new_operator.username, constants.USERNAME_ALTERNATIVE)
        self.assertEqual(status, True)
        assignment = DefaultAssignment.select_one_by_id(new_assignment.id)
        self.assertEqual(assignment.id, new_assignment.id)
        self.assertEqual(assignment.operator, new_operator.username)
        DefaultAssignment.clean_table()

    def test_update_status(self):
        new_assignment = DefaultAssignment.new_insert()
        new_status_assignment = StatusAssignmentType.REDISCOVERED.value
        model = Assignment(id=new_assignment.id)
        status = model.update_status(new_status_assignment)
        self.assertEqual(status, True)
        assignment = DefaultAssignment.select_one_by_id(new_assignment.id)
        self.assertEqual(assignment.id, new_assignment.id)
        self.assertEqual(assignment.status, new_status_assignment)
        DefaultAssignment.clean_table()

    def test_delete(self):
        new_assignment = DefaultAssignment.new_insert()
        model = Assignment(id=new_assignment.id)
        status = model.delete()
        self.assertEqual(status, True)
        self.assertIsNone(
            DefaultAssignment.select_one_by_id(new_assignment.id)
        )
        DefaultAssignment.clean_table()


class TestAssignmentByOperatorController(unittest.TestCase):
    def test_new_assignment(self):
        new_operator = DefaultOperator.new_insert()
        new_equipment = DefaultEquipment.new_insert()
        new_interface_old_version = DefaultInterface.new_insert(
            clean=False,
            interface_type=InterfaceType.OLD.value,
            equipment=new_equipment
        )
        new_interface_new_version = DefaultInterface.new_insert(
            clean=False,
            equipment=new_equipment,
            date=constants.DATE_CONSULT_TWO,
        )
        body = AssignmentRegisterBody(
            change_interface=new_interface_new_version.id,
            old_interface=new_interface_old_version.id,
            operator=new_operator.username,
            assigned_by=constants.USERNAME_ALTERNATIVE
        )
        status = OperatorController.add_assignment(body)
        self.assertEqual(status, True)
        new_assignment = DefaultAssignment.select_one_by_data(
            id_change_interface=new_interface_new_version.id,
            id_old_interface=new_interface_old_version.id,
            operator=new_operator.username
        )
        self.assertEqual(type(new_assignment), AssignmentSchema)
        self.assertEqual(new_assignment.new_interface, new_interface_new_version.id)
        self.assertEqual(new_assignment.old_interface, new_interface_old_version.id)
        self.assertEqual(new_assignment.operator, new_operator.username)
        DefaultAssignment.clean_table()

    def test_get_assignment_by_id(self):
        new_assignment = DefaultAssignment.new_insert()
        assignment = OperatorController.get_assignment_by_id(new_assignment.id)
        self.assertEqual(type(assignment), AssignmentSchema)
        self.assertEqual(assignment.id, new_assignment.id)
        DefaultAssignment.clean_table()

    def test_get_total_assignments(self):
        DefaultAssignment.new_insert()
        total = OperatorController.get_total_assignments()
        self.assertEqual(type(total), AssignmentsCountResponse)
        self.assertEqual(total.total_pending, 1)
        self.assertEqual(total.total_revised, 0)
        DefaultAssignment.clean_table()

    def test_get_all_assignments_revised(self):
        new_status_assignment = StatusAssignmentType.REDISCOVERED.value
        new_assignment = DefaultAssignment.new_insert(
            status_assignment=new_status_assignment
        )
        assignments = OperatorController.get_all_assignments_revised()
        self.assertEqual(type(assignments), list)
        self.assertNotEqual(len(assignments), 0)
        self.assertEqual(assignments[0].id, new_assignment.id)
        self.assertEqual(assignments[0].operator, new_assignment.operator)
        self.assertEqual(assignments[0].status, new_status_assignment)
        DefaultAssignment.clean_table()

    def test_get_all_assignments_by_operator(self):
        new_status_assignment = StatusAssignmentType.REDISCOVERED.value
        new_assignment = DefaultAssignment.new_insert(
            status_assignment=new_status_assignment
        )
        assignments = OperatorController.get_all_assignments_by_operator(new_assignment.operator)
        self.assertEqual(type(assignments), list)
        self.assertNotEqual(len(assignments), 0)
        self.assertEqual(assignments[0].id, new_assignment.id)
        self.assertEqual(assignments[0].operator, new_assignment.operator)
        self.assertEqual(assignments[0].status, new_status_assignment)
        DefaultAssignment.clean_table()

    def test_get_all_assignments_pending_by_operator(self):
        new_status_assignment = StatusAssignmentType.PENDING.value
        new_assignment = DefaultAssignment.new_insert(
            status_assignment=new_status_assignment
        )
        assignments = OperatorController.get_all_assignments_pending_by_operator(new_assignment.operator)
        self.assertEqual(type(assignments), list)
        self.assertNotEqual(len(assignments), 0)
        self.assertEqual(assignments[0].id, new_assignment.id)
        self.assertEqual(assignments[0].operator, new_assignment.operator)
        self.assertEqual(assignments[0].status, new_status_assignment)
        DefaultAssignment.clean_table()

    def test_get_all_assignments_revised_by_operator(self):
        new_status_assignment = StatusAssignmentType.INSPECTED.value
        new_assignment = DefaultAssignment.new_insert(
            status_assignment=new_status_assignment
        )
        assignments = OperatorController.get_all_assignments_revised_by_operator(new_assignment.operator)
        self.assertEqual(type(assignments), list)
        self.assertNotEqual(len(assignments), 0)
        self.assertEqual(assignments[0].id, new_assignment.id)
        self.assertEqual(assignments[0].operator, new_assignment.operator)
        self.assertEqual(assignments[0].status, new_status_assignment)
        DefaultAssignment.clean_table()

    def test_get_total_assignments_by_operator(self):
        new_status_assignment = StatusAssignmentType.REDISCOVERED.value
        new_assignment = DefaultAssignment.new_insert(
            status_assignment=new_status_assignment
        )
        total = OperatorController.get_total_assignments_by_operator(new_assignment.operator)
        self.assertEqual(type(total), AssignmentsCountResponse)
        self.assertEqual(total.total_pending, 0)
        self.assertEqual(total.total_revised, 1)
        DefaultAssignment.clean_table()

    def test_reassignment(self):
        new_status_assignment = StatusAssignmentType.PENDING.value
        new_assignment = DefaultAssignment.new_insert(
            status_assignment=new_status_assignment
        )
        new_operator = DefaultOperator.new_insert(
            clean=False,
            username=constants.USERNAME_TWO
        )
        body = AssignmentReassignBody(
            id_assignment=new_assignment.id,
            new_operator=new_operator.username,
            assigned_by=constants.USERNAME_ALTERNATIVE
        )
        status = OperatorController.reassignment(body)
        self.assertEqual(status, True)
        assignment = DefaultAssignment.select_one_by_id(new_assignment.id)
        self.assertEqual(assignment.id, new_assignment.id)
        self.assertEqual(assignment.operator, new_operator.username)
        DefaultAssignment.clean_table()

    def test_update_status_assignment(self):
        new_status_assignment = StatusAssignmentType.REDISCOVERED.value
        new_assignment = DefaultAssignment.new_insert()
        status = OperatorController.update_status_assignment(
            id=new_assignment.id,
            status=new_status_assignment
        )
        self.assertEqual(status, True)
        assignment = DefaultAssignment.select_one_by_id(new_assignment.id)
        self.assertEqual(assignment.id, new_assignment.id)
        self.assertEqual(assignment.status, new_status_assignment)
        DefaultAssignment.clean_table()

if __name__ == "__main__":
    unittest.main()

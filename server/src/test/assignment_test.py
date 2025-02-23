import unittest
from constants import StatusAssignmentType, InterfaceType
from controllers import OperatorController
from models import AssignmentModel, Assignment
from schemas import AssignmentResponseSchema, AssignmentInterfaceResponseSchema, AssignmentRegisterBody, StatisticsAssignmentResponse, AssignmentReassignBody, AssignmentUpdateStatus
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
            new_interface=new_interface_new_version.id,
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
        self.assertEqual(type(new_assignment), AssignmentResponseSchema)
        self.assertEqual(new_assignment.newInterface, new_interface_new_version.id)
        self.assertEqual(new_assignment.oldInterface, new_interface_old_version.id)
        self.assertEqual(new_assignment.operator, new_operator.username)
        DefaultAssignment.clean_table()

    def test_get_all_by_operator(self):
        new_assignment = DefaultAssignment.new_insert()
        model = Assignment(operator=new_assignment.operator)
        assignments = model.get_all_assignments_by_operator()
        self.assertEqual(type(assignments), list)
        self.assertNotEqual(len(assignments), 0)
        self.assertEqual(assignments[0].id, new_assignment.id)
        DefaultAssignment.clean_table()

    def test_get_assignment_by_interface(self):
        new_assignment = DefaultAssignment.new_insert()
        model = Assignment(
            id_new_interface=new_assignment.newInterface,
            id_old_interface=new_assignment.oldInterface,
            operator=new_assignment.operator,
        )
        assignment = model.get_assignment_by_interface()
        self.assertEqual(type(assignment), AssignmentResponseSchema)
        self.assertEqual(assignment.id, new_assignment.id)
        DefaultAssignment.clean_table()

    def test_get_by_id_assignment(self):
        new_assignment = DefaultAssignment.new_insert()
        model = Assignment(id=new_assignment.id)
        assignment = model.get_by_id_assignment()
        self.assertEqual(type(assignment), AssignmentResponseSchema)
        self.assertEqual(assignment.id, new_assignment.id)
        DefaultAssignment.clean_table()

    def test_get_by_id_assignment_interfaces(self):
        new_assignment = DefaultAssignment.new_insert()
        model = Assignment(id=new_assignment.id)
        assignment = model.get_info_assignment_by_id()
        self.assertEqual(type(assignment), AssignmentInterfaceResponseSchema)
        self.assertEqual(assignment.idAssignment, new_assignment.id)
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
            newInterface=new_interface_new_version.id,
            oldInterface=new_interface_old_version.id,
            operator=new_operator.username,
            assignedBy=constants.USERNAME_ALTERNATIVE
        )
        status = OperatorController.add_assignment(body)
        self.assertEqual(status, True)
        new_assignment = DefaultAssignment.select_one_by_data(
            id_change_interface=new_interface_new_version.id,
            id_old_interface=new_interface_old_version.id,
            operator=new_operator.username
        )
        self.assertEqual(type(new_assignment), AssignmentResponseSchema)
        self.assertEqual(new_assignment.newInterface, new_interface_new_version.id)
        self.assertEqual(new_assignment.oldInterface, new_interface_old_version.id)
        self.assertEqual(new_assignment.operator, new_operator.username)
        DefaultAssignment.clean_table()

    def test_get_assignment_by_id(self):
        new_assignment = DefaultAssignment.new_insert()
        assignment = OperatorController.get_assignment_by_id(new_assignment.id)
        self.assertEqual(type(assignment), AssignmentResponseSchema)
        self.assertEqual(assignment.id, new_assignment.id)
        DefaultAssignment.clean_table()

    def test_get_all_info_assignment_by_id(self):
        new_assignment = DefaultAssignment.new_insert()
        assignment = OperatorController.get_info_assignment_by_id(new_assignment.id)
        self.assertEqual(type(assignment), AssignmentInterfaceResponseSchema)
        self.assertEqual(assignment.idAssignment, new_assignment.id)
        DefaultAssignment.clean_table()

    def test_get_total_assignments(self):
        DefaultAssignment.new_insert()
        statistics = OperatorController.get_general_statistics_assignments()
        self.assertEqual(type(statistics), list)
        self.assertEqual(len(statistics), 1)
        self.assertEqual(statistics[0].totalPending, 1)
        self.assertEqual(statistics[0].totalRevised, 0)
        DefaultAssignment.clean_table()

    def test_get_total_assignments_by_operator(self):
        new_assignment = DefaultAssignment.new_insert()
        operator = new_assignment.operator
        statistics = OperatorController.get_statistics_assignments_by_operator(operator=operator)
        self.assertEqual(type(statistics), StatisticsAssignmentResponse)
        self.assertEqual(statistics.totalPending, 1)
        self.assertEqual(statistics.totalRevised, 0)
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
            idAssignment=new_assignment.id,
            newOperator=new_operator.username,
            assignedBy=constants.USERNAME_ALTERNATIVE
        )
        status = OperatorController.reassignment(body)
        self.assertEqual(status, True)
        assignment = DefaultAssignment.select_one_by_id(new_assignment.id)
        self.assertEqual(assignment.id, new_assignment.id)
        self.assertEqual(assignment.operator, new_operator.username)
        DefaultAssignment.clean_table()

    def test_update_status_assignment_v2(self):
        new_status_assignment = StatusAssignmentType.REDISCOVERED.value
        new_assignment = DefaultAssignment.new_insert()
        status = OperatorController.update_status_assignment_v2(
            id=new_assignment.id,
            status=new_status_assignment
        )
        self.assertEqual(status, True)
        assignment = DefaultAssignment.select_one_by_id(new_assignment.id)
        self.assertEqual(assignment.id, new_assignment.id)
        self.assertEqual(assignment.status, new_status_assignment)
        DefaultAssignment.clean_table()

    def test_update_status_assignment(self):
        new_status_assignment = StatusAssignmentType.REDISCOVERED.value
        new_assignment = DefaultAssignment.new_insert()
        assignment = AssignmentUpdateStatus(
            id=new_assignment.id,
            newStatus=new_status_assignment
        )
        assignments = [assignment]
        updated = OperatorController.update_status_assignment(data=assignments)
        self.assertEqual(updated, 1)
        assignment = DefaultAssignment.select_one_by_id(new_assignment.id)
        self.assertEqual(assignment.id, new_assignment.id)
        self.assertEqual(assignment.status, new_status_assignment)
        DefaultAssignment.clean_table()

if __name__ == "__main__":
    unittest.main()

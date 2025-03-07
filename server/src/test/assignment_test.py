import unittest
from typing import List
from constants import StatusAssignmentType, InterfaceType
from controllers import OperatorController
from models import AssignmentModel, Assignment
from schemas import AssignmentResponseSchema, AssignmentInterfaceResponseSchema, AssignmentRegisterBody, AssignmentStatisticsResponse, AssignmentReassignBody, AssignmentUpdateStatus
from test import constants, DefaultInterface, DefaultOperator, DefaultEquipment, DefaultAssignment


class TestAssignmentModel(unittest.TestCase):
    def test_register(self):
        first_new_operator = DefaultOperator.new_insert()
        second_new_operator = DefaultOperator.new_insert(
            clean=False,
            username=constants.USERNAME_TWO
        )
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
        assignments: List[AssignmentRegisterBody] = [
            AssignmentRegisterBody(
                newInterface=new_interface_new_version.id,
                oldInterface=new_interface_old_version.id,
                operator=first_new_operator.username,
                assignedBy=constants.USERNAME_ALTERNATIVE
            ),
            AssignmentRegisterBody(
                newInterface=new_interface_new_version.id,
                oldInterface=new_interface_old_version.id,
                operator=second_new_operator.username,
                assignedBy=constants.USERNAME_ALTERNATIVE
            )
        ]
        model = AssignmentModel()
        status = model.register(assignments=assignments)
        self.assertEqual(status, True)
        new_assignment = DefaultAssignment.select_one_by_data(
            id_change_interface=new_interface_new_version.id,
            id_old_interface=new_interface_old_version.id,
            operator=first_new_operator.username
        )
        self.assertEqual(type(new_assignment), AssignmentResponseSchema)
        self.assertEqual(new_assignment.newInterface, new_interface_new_version.id)
        self.assertEqual(new_assignment.oldInterface, new_interface_old_version.id)
        self.assertEqual(new_assignment.operator, first_new_operator.username)
        new_assignment = DefaultAssignment.select_one_by_data(
            id_change_interface=new_interface_new_version.id,
            id_old_interface=new_interface_old_version.id,
            operator=second_new_operator.username
        )
        self.assertEqual(type(new_assignment), AssignmentResponseSchema)
        self.assertEqual(new_assignment.newInterface, new_interface_new_version.id)
        self.assertEqual(new_assignment.oldInterface, new_interface_old_version.id)
        self.assertEqual(new_assignment.operator, second_new_operator.username)
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
        assignment = model.get_assignment_by_id_assignment()
        self.assertEqual(type(assignment), AssignmentResponseSchema)
        self.assertEqual(assignment.id, new_assignment.id)
        DefaultAssignment.clean_table()

    def test_get_by_id_assignment_interfaces(self):
        new_assignment = DefaultAssignment.new_insert()
        model = Assignment(id=new_assignment.id)
        assignment = model.get_info_assignment_by_id_assignment()
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

    def test_update_status_by_ids(self):
        new_equipment = DefaultEquipment.new_insert()
        new_operator = DefaultOperator.new_insert(
            clean=False
        )
        first_old_interface = DefaultInterface.new_insert(
            clean=False,
            equipment=new_equipment,
            interface_type=InterfaceType.OLD.value,
        )
        first_new_interface = DefaultInterface.new_insert(
            clean=False,
            equipment=new_equipment,
            date=constants.DATE_CONSULT_TWO,
        )
        second_old_interface = DefaultInterface.new_insert(
            clean=False,
            equipment=new_equipment,
            interface_type=InterfaceType.OLD.value,
            ifIndex=207
        )
        second_new_interface = DefaultInterface.new_insert(
            clean=False,
            equipment=new_equipment,
            date=constants.DATE_CONSULT_TWO,
            ifIndex=207
        )
        first_assignment = DefaultAssignment.new_insert(
            clean=False,
            equipment=new_equipment,
            operator=new_operator,
            old_interface=first_old_interface,
            new_interface=first_new_interface
        )
        second_assignment = DefaultAssignment.new_insert(
            clean=False,
            equipment=new_equipment,
            operator=new_operator,
            old_interface=second_old_interface,
            new_interface=second_new_interface
        )
        ids = [first_assignment.id, second_assignment.id]
        status = Assignment.update_status_by_ids(ids, StatusAssignmentType.REDISCOVERED.value)
        self.assertEqual(status, True)
        first_assignment = DefaultAssignment.select_one_by_id(id=first_assignment.id)
        self.assertEqual(type(first_assignment), AssignmentResponseSchema)
        self.assertEqual(first_assignment.status, StatusAssignmentType.REDISCOVERED.value)
        second_assignment = DefaultAssignment.select_one_by_id(id=second_assignment.id)
        self.assertEqual(type(second_assignment), AssignmentResponseSchema)
        self.assertEqual(second_assignment.status, StatusAssignmentType.REDISCOVERED.value)
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
        first_new_operator = DefaultOperator.new_insert()
        second_new_operator = DefaultOperator.new_insert(
            clean=False,
            username=constants.USERNAME_TWO
        )
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
        assignments: List[AssignmentRegisterBody] = [
            AssignmentRegisterBody(
                newInterface=new_interface_new_version.id,
                oldInterface=new_interface_old_version.id,
                operator=first_new_operator.username,
                assignedBy=constants.USERNAME_ALTERNATIVE
            ),
            AssignmentRegisterBody(
                newInterface=new_interface_new_version.id,
                oldInterface=new_interface_old_version.id,
                operator=second_new_operator.username,
                assignedBy=constants.USERNAME_ALTERNATIVE
            )
        ]
        status = OperatorController.add_assignment(data=assignments)
        self.assertEqual(status, True)
        new_assignment = DefaultAssignment.select_one_by_data(
            id_change_interface=new_interface_new_version.id,
            id_old_interface=new_interface_old_version.id,
            operator=first_new_operator.username
        )
        self.assertEqual(type(new_assignment), AssignmentResponseSchema)
        self.assertEqual(new_assignment.newInterface, new_interface_new_version.id)
        self.assertEqual(new_assignment.oldInterface, new_interface_old_version.id)
        self.assertEqual(new_assignment.operator, first_new_operator.username)
        new_assignment = DefaultAssignment.select_one_by_data(
            id_change_interface=new_interface_new_version.id,
            id_old_interface=new_interface_old_version.id,
            operator=second_new_operator.username
        )
        self.assertEqual(type(new_assignment), AssignmentResponseSchema)
        self.assertEqual(new_assignment.newInterface, new_interface_new_version.id)
        self.assertEqual(new_assignment.oldInterface, new_interface_old_version.id)
        self.assertEqual(new_assignment.operator, second_new_operator.username)
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
        statistics = OperatorController.get_statistics_assignments_general()
        self.assertEqual(type(statistics), list)
        self.assertEqual(len(statistics), 1)
        self.assertEqual(statistics[0].totalPending, 1)
        self.assertEqual(statistics[0].totalRevised, 0)
        DefaultAssignment.clean_table()

    def test_get_total_assignments_by_operator(self):
        new_assignment = DefaultAssignment.new_insert()
        operator = new_assignment.operator
        statistics = OperatorController.get_statistics_assignments_operator(operator=operator)
        self.assertEqual(type(statistics), AssignmentStatisticsResponse)
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
        status = OperatorController.update_status_assignment(
            id=new_assignment.id,
            status=new_status_assignment
        )
        self.assertEqual(status, True)
        assignment = DefaultAssignment.select_one_by_id(new_assignment.id)
        self.assertEqual(assignment.id, new_assignment.id)
        self.assertEqual(assignment.status, new_status_assignment)
        DefaultAssignment.clean_table()

    def test_update_status_assignments_by_ids(self):
        new_equipment = DefaultEquipment.new_insert()
        new_operator = DefaultOperator.new_insert(
            clean=False
        )
        first_old_interface = DefaultInterface.new_insert(
            clean=False,
            equipment=new_equipment,
            interface_type=InterfaceType.OLD.value,
        )
        first_new_interface = DefaultInterface.new_insert(
            clean=False,
            equipment=new_equipment,
            date=constants.DATE_CONSULT_TWO,
        )
        second_old_interface = DefaultInterface.new_insert(
            clean=False,
            equipment=new_equipment,
            interface_type=InterfaceType.OLD.value,
            ifIndex=207
        )
        second_new_interface = DefaultInterface.new_insert(
            clean=False,
            equipment=new_equipment,
            date=constants.DATE_CONSULT_TWO,
            ifIndex=207
        )
        first_assignment = DefaultAssignment.new_insert(
            clean=False,
            equipment=new_equipment,
            operator=new_operator,
            old_interface=first_old_interface,
            new_interface=first_new_interface
        )
        second_assignment = DefaultAssignment.new_insert(
            clean=False,
            equipment=new_equipment,
            operator=new_operator,
            old_interface=second_old_interface,
            new_interface=second_new_interface
        )
        ids = [
            AssignmentUpdateStatus(idAssignment=first_assignment.id, newStatus=StatusAssignmentType.REDISCOVERED.value),
            AssignmentUpdateStatus(idAssignment=second_assignment.id, newStatus=StatusAssignmentType.REDISCOVERED.value),
        ]
        status = OperatorController.update_status_assignments_by_ids(ids)
        self.assertEqual(status, True)
        DefaultAssignment.clean_table()

if __name__ == "__main__":
    unittest.main()

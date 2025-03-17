import unittest
from typing import List
from constants import StatusAssignmentType, InterfaceType
from controllers import OperatorController
from schemas import AssignmentSchema, AssignmentInterfaceSchema, RegisterAssignmentBody, AssignmentStatisticsSchema, ReassignBody, UpdateStatusAssignmentBody
from test import constants, DefaultInterface, DefaultOperator, DefaultEquipment, DefaultAssignment


class TestAssignmentController(unittest.TestCase):
    def test_add_assignment(self):
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
        new_operator = DefaultOperator.new_insert(
            clean=False,
            username=constants.USERNAME_ALTERNATIVE
        )
        assignments: List[RegisterAssignmentBody] = [
            RegisterAssignmentBody(
                idChange="1",
                newInterface=new_interface_new_version.id,
                oldInterface=new_interface_old_version.id,
                operator=first_new_operator.username,
                assignedBy=constants.USERNAME_ALTERNATIVE
            ),
            RegisterAssignmentBody(
                idChange="2",
                newInterface=new_interface_new_version.id,
                oldInterface=new_interface_old_version.id,
                operator=second_new_operator.username,
                assignedBy=constants.USERNAME_ALTERNATIVE
            )
        ]
        status = OperatorController.add_assignment(body=assignments)
        self.assertEqual(status, True)
        new_assignment = DefaultAssignment.select_one_by_data(
            id_change_interface=new_interface_new_version.id,
            id_old_interface=new_interface_old_version.id,
            operator=first_new_operator.username
        )
        self.assertEqual(type(new_assignment), AssignmentSchema)
        self.assertEqual(new_assignment.newInterface, new_interface_new_version.id)
        self.assertEqual(new_assignment.oldInterface, new_interface_old_version.id)
        self.assertEqual(new_assignment.operator, first_new_operator.username)
        new_assignment = DefaultAssignment.select_one_by_data(
            id_change_interface=new_interface_new_version.id,
            id_old_interface=new_interface_old_version.id,
            operator=second_new_operator.username
        )
        self.assertEqual(type(new_assignment), AssignmentSchema)
        self.assertEqual(new_assignment.newInterface, new_interface_new_version.id)
        self.assertEqual(new_assignment.oldInterface, new_interface_old_version.id)
        self.assertEqual(new_assignment.operator, second_new_operator.username)
        DefaultAssignment.clean_table()

    def test_reassignment(self):
        new_status_assignment = StatusAssignmentType.PENDING.value
        new_assignment = DefaultAssignment.new_insert(
            status_assignment=new_status_assignment
        )
        data = ReassignBody(
            idAssignment=new_assignment.id,
            newOperator=constants.USERNAME,
            assignedBy=constants.USERNAME
        )
        status = OperatorController.reassignment(body=[data])
        self.assertEqual(status, True)
        DefaultAssignment.clean_table()

    def test_get_assignment_by_id(self):
        new_assignment = DefaultAssignment.new_insert()
        assignment = OperatorController.get_assignment_by_id(new_assignment.id)
        self.assertEqual(type(assignment), AssignmentSchema)
        self.assertEqual(assignment.id, new_assignment.id)
        DefaultAssignment.clean_table()

    def test_get_info_assignment_by_id(self):
        new_assignment = DefaultAssignment.new_insert()
        assignment = OperatorController.get_info_assignment_by_id(new_assignment.id)
        self.assertEqual(type(assignment), AssignmentInterfaceSchema)
        self.assertEqual(assignment.idAssignment, new_assignment.id)
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

    def test_get_all_pending_assignments_by_operator(self):
        new_assignment = DefaultAssignment.new_insert()
        assignments = OperatorController.get_all_pending_assignments_by_operator(new_assignment.operator)
        self.assertEqual(type(assignments), list)
        self.assertNotEqual(len(assignments), 0)
        self.assertEqual(assignments[0].idAssignment, new_assignment.id)
        self.assertEqual(assignments[0].statusAssignment, StatusAssignmentType.PENDING.value)
        DefaultAssignment.clean_table()

    def test_get_all_revised_assignments_by_operator(self):
        new_assignment = DefaultAssignment.new_insert(
            status_assignment=StatusAssignmentType.REDISCOVERED.value
        )
        assignments = OperatorController.get_all_revised_assignments_by_operator(new_assignment.operator)
        self.assertEqual(type(assignments), list)
        self.assertNotEqual(len(assignments), 0)
        self.assertEqual(assignments[0].idAssignment, new_assignment.id)
        self.assertEqual(assignments[0].statusAssignment, StatusAssignmentType.REDISCOVERED.value)
        DefaultAssignment.clean_table()

    def test_get_all_revised_assignments_operator_by_month(self):
        new_assignment = DefaultAssignment.new_insert(
            status_assignment=StatusAssignmentType.REDISCOVERED.value
        )
        month = constants.DATE_CONSULT.split("-")[1]
        assignments = OperatorController.get_all_revised_assignments_operator_by_month(month=month)
        self.assertEqual(type(assignments), list)
        self.assertNotEqual(len(assignments), 0)
        self.assertEqual(assignments[0].idAssignment, new_assignment.id)
        self.assertEqual(assignments[0].statusAssignment, StatusAssignmentType.REDISCOVERED.value)
        DefaultAssignment.clean_table()

    def test_get_statistics_assignments_general(self):
        DefaultAssignment.new_insert()
        statistics = OperatorController.get_statistics_assignments_general()
        self.assertEqual(type(statistics), list)
        self.assertEqual(len(statistics), 1)
        self.assertEqual(statistics[0].totalPending, 1)
        self.assertEqual(statistics[0].totalRevised, 0)
        DefaultAssignment.clean_table()

    def test_get_statistics_assignments_general_by_day(self):
        DefaultAssignment.new_insert()
        statistics = OperatorController.get_statistics_assignments_general_by_day(day=constants.DATE_CONSULT)
        self.assertEqual(type(statistics), list)
        self.assertEqual(len(statistics), 1)
        self.assertEqual(statistics[0].totalPending, 1)
        self.assertEqual(statistics[0].totalRevised, 0)
        DefaultAssignment.clean_table()

    def test_get_statistics_assignments_general_by_month(self):
        DefaultAssignment.new_insert()
        month = constants.DATE_CONSULT.split("-")[1]
        statistics = OperatorController.get_statistics_assignments_general_by_month(month=month)
        self.assertEqual(type(statistics), list)
        self.assertEqual(len(statistics), 1)
        self.assertEqual(statistics[0].totalPending, 1)
        self.assertEqual(statistics[0].totalRevised, 0)
        DefaultAssignment.clean_table()

    def test_get_statistics_assignments_operator(self):
        new_assignment = DefaultAssignment.new_insert()
        operator = new_assignment.operator
        statistics = OperatorController.get_statistics_assignments_operator(operator=operator)
        self.assertEqual(type(statistics), AssignmentStatisticsSchema)
        self.assertEqual(statistics.totalPending, 1)
        self.assertEqual(statistics.totalRevised, 0)
        DefaultAssignment.clean_table()

    def test_get_statistics_assignments_operator_by_day(self):
        new_assignment = DefaultAssignment.new_insert()
        operator = new_assignment.operator
        statistics = OperatorController.get_statistics_assignments_operator_by_day(
            operator=operator,
            day=constants.DATE_CONSULT
        )
        self.assertEqual(type(statistics), AssignmentStatisticsSchema)
        self.assertEqual(statistics.totalPending, 1)
        self.assertEqual(statistics.totalRevised, 0)
        DefaultAssignment.clean_table()

    def test_get_statistics_assignments_operator_by_month(self):
        new_assignment = DefaultAssignment.new_insert()
        operator = new_assignment.operator
        statistics = OperatorController.get_statistics_assignments_operator_by_month(
            operator=operator,
            month=constants.DATE_CONSULT.split("-")[1]
        )
        self.assertEqual(type(statistics), AssignmentStatisticsSchema)
        self.assertEqual(statistics.totalPending, 1)
        self.assertEqual(statistics.totalRevised, 0)
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
            UpdateStatusAssignmentBody(idAssignment=first_assignment.id, newStatus=StatusAssignmentType.REDISCOVERED.value),
            UpdateStatusAssignmentBody(idAssignment=second_assignment.id, newStatus=StatusAssignmentType.REDISCOVERED.value),
        ]
        status = OperatorController.update_status_assignments_by_ids(ids)
        self.assertEqual(status, True)
        DefaultAssignment.clean_table()

if __name__ == "__main__":
    unittest.main()

import unittest
from io import StringIO
from constants.types import AssignmentStatusTypes
from database.querys.assignment import AssignmentQuery
from models.assignment import AssignmentModel, AssignmentField, ReassignmentModel, UpdateAssignmentModel
from test import AssignmentDBTest, InterfaceDBTest, UserDBTest


class Query(unittest.TestCase):
    test_database: AssignmentDBTest = AssignmentDBTest()
    test_interface_database: InterfaceDBTest = InterfaceDBTest()
    test_user_database: UserDBTest = UserDBTest()

    def setUp(self) -> None:
        self.test_interface_database.create_table()
        self.test_user_database.create_table()
        self.test_database.create_table()

    def tearDown(self) -> None:
        self.test_database.clean()
        self.test_interface_database.clean()
        self.test_user_database.clean()

    def test_insert(self) -> None:
        """Test of insert assignments."""
        assignment_complete_mock = self.test_database.get_mock()
        assingment_mock = AssignmentModel(
            old_interface_id=assignment_complete_mock.id_old,
            current_interface_id=assignment_complete_mock.id_new,
            username=assignment_complete_mock.username,
            assign_by=assignment_complete_mock.assign_by,
            type_status=assignment_complete_mock.type_status,
            created_at=assignment_complete_mock.created_at,
            updated_at=None
        )
        data = ";".join(str(value) for value in assingment_mock.model_dump(exclude={AssignmentField.CREATED_AT, AssignmentField.UPDATED_AT}).values())
        buffer = StringIO()
        buffer.write(data)
        buffer.seek(0)
        self.setUp()

        query = AssignmentQuery()
        status_operation = query.insert(data=buffer)

        self.tearDown()
        self.assertTrue(status_operation)

    def test_reassign(self) -> None:
        """Test of reassign assignments."""
        assignment_complete_mock = self.test_database.get_mock()
        self.setUp()
        self.test_database.insert(new_assignment=assignment_complete_mock)
        reassignment_mock = ReassignmentModel(
            old_interface_id=assignment_complete_mock.id_old,
            current_interface_id=assignment_complete_mock.id_new,
            old_username=assignment_complete_mock.username,
            new_username="unittest2",
            assign_by=assignment_complete_mock.assign_by,
        )

        query = AssignmentQuery()
        status_operation = query.reassing(data=[reassignment_mock])

        self.tearDown()
        self.assertTrue(status_operation)

    def test_update_status(self) -> None:
        """Test of update assignments."""
        assignment_complete_mock = self.test_database.get_mock()
        self.setUp()
        self.test_database.insert(new_assignment=assignment_complete_mock)

        query = AssignmentQuery()
        status_operation = query.update_status(data=[
            UpdateAssignmentModel(
                old_interface_id=assignment_complete_mock.id_old,
                current_interface_id=assignment_complete_mock.id_new,
                username=assignment_complete_mock.username,
                type_status=AssignmentStatusTypes.REDISCOVERED
            )
        ])

        self.tearDown()
        self.assertTrue(status_operation)

    def test_get_all_by_status(self) -> None:
        """Test of get all assignments by status."""
        assignment_complete_mock = self.test_database.get_mock()
        self.setUp()
        self.test_database.insert(new_assignment=assignment_complete_mock)

        query = AssignmentQuery()
        response = query.get_all_by_status(status=assignment_complete_mock.type_status)

        print(response)

        self.tearDown()
        self.assertFalse(response.empty)
        self.assertEqual(len(response), 1)

    def test_assigned_by_status(self) -> None:
        """Test of get assignments by a status."""
        assignment_complete_mock = self.test_database.get_mock()
        self.setUp()
        self.test_database.insert(new_assignment=assignment_complete_mock)

        query = AssignmentQuery()
        response = query.assigned_by_status(username=assignment_complete_mock.username, status=assignment_complete_mock.type_status)

        print(response)

        self.tearDown()
        self.assertFalse(response.empty)
        self.assertEqual(len(response), 1)

    def test_completed_by_month(self) -> None:
        """Test of get assignments completed by month."""
        assignment_complete_mock = self.test_database.get_mock()
        assignment_complete_mock.type_status = AssignmentStatusTypes.REDISCOVERED
        self.setUp()
        self.test_database.insert(new_assignment=assignment_complete_mock)

        query = AssignmentQuery()
        month = assignment_complete_mock.created_at.split("-")[1]
        response = query.completed_by_month(username=assignment_complete_mock.username, month=month)

        print(response)

        self.tearDown()
        self.assertFalse(response.empty)
        self.assertEqual(len(response), 1)

    def test_get_statistics(self) -> None:
        """Test of get statistics."""
        assignment_complete_mock = self.test_database.get_mock()
        self.setUp()
        self.test_database.insert(new_assignment=assignment_complete_mock)

        query = AssignmentQuery()
        response = query.get_statistics(usernames=[assignment_complete_mock.username])

        print(response)

        self.tearDown()
        self.assertEqual(len(response), 1)

    
if __name__ == "__main__":
    unittest.main()
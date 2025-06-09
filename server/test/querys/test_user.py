import unittest 
from constants.types import RoleTypes, UserStatusTypes
from database.querys.user import UserQuery
from models.user import UserModel
from test import UserDBTest


class Query(unittest.TestCase):
    test_database: UserDBTest = UserDBTest()

    def setUp(self) -> None:
        self.test_database.create_table()

    def tearDown(self) -> None:
        self.test_database.clean()

    def test_insert(self) -> None:
        """Test of insert a user."""
        user_mock = self.test_database.get_mock()
        self.setUp()

        query = UserQuery()
        status_operation = query.insert(new_user=user_mock)

        self.tearDown()
        self.assertTrue(status_operation)

    def test_update(self) -> None:
        """Test of update a user."""
        user_mock = self.test_database.get_mock()
        self.setUp()
        self.test_database.insert(new_user=user_mock)

        user_mock.name = "Unit2"
        user_mock.lastname = "Test2"
        user_mock.status = UserStatusTypes.INACTIVE
        user_mock.role = RoleTypes.SOPORT
        user_mock.is_deleted = True

        query = UserQuery()
        status_operation = query.update(user=user_mock)

        self.tearDown()
        self.assertTrue(status_operation)

    def test_update_password(self) -> None:
        """Test of update password."""
        user_mock = self.test_database.get_mock()
        self.setUp()
        self.test_database.insert(new_user=user_mock)

        user_mock.password = "test2"

        query = UserQuery()
        status_operation = query.update_password(username=user_mock.username, password=user_mock.password)

        self.tearDown()
        self.assertTrue(status_operation)

    def test_delete(self) -> None:
        """Test of delete users."""
        first_user_mock = self.test_database.get_mock()
        second_user_mock = self.test_database.get_mock()
        self.setUp()
        self.test_database.insert(new_user=first_user_mock)
        self.test_database.insert(new_user=second_user_mock)

        query = UserQuery()
        status_operation = query.delete(usernames=[first_user_mock.username, second_user_mock.username])

        self.tearDown()
        self.assertTrue(status_operation)

    def test_get(self) -> None:
        """Test of get a user."""
        user_mock = self.test_database.get_mock()
        self.setUp()
        self.test_database.insert(new_user=user_mock)

        query = UserQuery()
        response = query.get(username=user_mock.username)
        print(response)

        self.tearDown()
        self.assertIsNotNone(response)
        self.assertEqual(response.username, user_mock.username)
        self.assertEqual(response.password, user_mock.password)
        self.assertEqual(response.name, user_mock.name)
        self.assertEqual(response.lastname, user_mock.lastname)
        self.assertEqual(response.status, user_mock.status)
        self.assertEqual(response.role, user_mock.role)

    def test_get_all(self) -> None:
        """Test of get all users."""
        first_user_mock = self.test_database.get_mock()
        second_user_mock = self.test_database.get_mock()
        self.setUp()
        self.test_database.insert(new_user=first_user_mock)
        self.test_database.insert(new_user=second_user_mock)

        query = UserQuery()
        response = query.get_all()

        self.tearDown()
        self.assertIsNotNone(response)
        self.assertEqual(len(response), 2)

    def test_get_users(self) -> None:
        """Test of get users without deleted."""
        first_user_mock = self.test_database.get_mock()
        first_user_mock.status = UserStatusTypes.DELETED
        second_user_mock = self.test_database.get_mock()
        self.setUp()
        self.test_database.insert(new_user=first_user_mock)
        self.test_database.insert(new_user=second_user_mock)

        query = UserQuery()
        response = query.get_users()

        self.tearDown()
        self.assertIsNotNone(response)
        self.assertEqual(len(response), 1)

    def test_get_deleted(self) -> None:
        """Test of get users deleted."""
        first_user_mock = self.test_database.get_mock()
        first_user_mock.status = UserStatusTypes.DELETED
        second_user_mock = self.test_database.get_mock()
        self.setUp()
        self.test_database.insert(new_user=first_user_mock)
        self.test_database.insert(new_user=second_user_mock)

        query = UserQuery()
        response = query.get_deleted()

        self.tearDown()
        self.assertIsNotNone(response)
        self.assertEqual(len(response), 1)

    def test_get_users_by_category(self) -> None:
        """Test of get users by a category."""
        first_user_mock = self.test_database.get_mock()
        self.setUp()
        self.test_database.insert(new_user=first_user_mock)

        query = UserQuery()
        response = query.get_users_by_category(status=UserStatusTypes.ACTIVE, role=RoleTypes.ADMIN)

        self.tearDown()
        self.assertIsNotNone(response)
        self.assertEqual(len(response), 1)
    
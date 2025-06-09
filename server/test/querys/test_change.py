import unittest
from io import StringIO
from datetime import datetime, timedelta
from database.querys.change import ChangeQuery
from models.change import ChangeModel
from models.interface import InterfaceModel
from models.user import UserModel
from test import ChangeDBTest, InterfaceDBTest, UserDBTest


class Query(unittest.TestCase):
    test_database: ChangeDBTest = ChangeDBTest()
    test_interface_database: InterfaceDBTest = InterfaceDBTest()
    test_user_database: UserDBTest = UserDBTest()

    def setUp(self) -> None:
        self.test_interface_database.create_table()
        self.test_user_database.create_table()
        self.test_database.create_table()

    def tearDown(self) -> None:
        self.test_interface_database.clean()
        self.test_user_database.clean()
        self.test_database.clean()

    def test_insert(self) -> None:
        """Test of insert changes."""
        change_complete_mock = self.test_database.get_mock()
        change_mock = ChangeModel(
            current_interface_id=change_complete_mock.id_new,
            old_interface_id=change_complete_mock.id_old,
            assigned=change_complete_mock.username
        )
        data = ";".join(str(value) for value in change_mock.model_dump().values())
        buffer = StringIO()
        buffer.write(data)
        buffer.seek(0)
        self.setUp()

        query = ChangeQuery()
        status_operation = query.insert(data=buffer)

        self.tearDown()
        self.assertTrue(status_operation)

    def test_get_all(self) -> None:
        """Test of get all changes."""
        change_complete_mock = self.test_database.get_mock()
        self.setUp()
        self.test_database.insert(new_change=change_complete_mock)

        query = ChangeQuery()
        response = query.get_all()

        print(response)

        self.tearDown()

        self.assertFalse(response.empty)
        self.assertEqual(len(response), 1)
        

if __name__ == "__main__":
    unittest.main()
import unittest
import random
from constants import OperatorFields
from models import OperatorModel, Operator
from test import default


class TestOperatorQuery(unittest.TestCase):
    def test_register(self):
        model = OperatorModel(
            username=default.USERNAME + str(random.randint(1, 255)),
            name="test",
            lastname="user",
            password="secret123456",
            profile="STANDARD",
            statusaccount="ACTIVE",
        )
        status = model.register()
        self.assertEqual(status, True)
        default.clean_table_operator()

    def test_get_all(self):
        default.register_operator()
        users = Operator.get_all()
        self.assertEqual(type(users), list)
        self.assertNotEqual(len(users), 0)
        default.clean_table_operator()

    def test_get_all_profile_active(self):
        default.register_operator()
        users = Operator.get_all_profile_active("STANDARD")
        self.assertEqual(type(users), list)
        self.assertNotEqual(len(users), 0)
        self.assertEqual(users[0][OperatorFields.PROFILE.value], "STANDARD")
        self.assertEqual(users[0][OperatorFields.STATUS_ACCOUNT.value], "ACTIVE")
        default.clean_table_operator()

    def test_get_all_inactive(self):
        default.register_operator(status_account="INACTIVE")
        users = Operator.get_all_inactive()
        self.assertEqual(type(users), list)
        self.assertNotEqual(len(users), 0)
        self.assertEqual(users[0][OperatorFields.STATUS_ACCOUNT.value], "INACTIVE")
        default.clean_table_operator()

    def test_get_all_deleted(self):
        default.register_operator(status_account="DELETED")
        users = Operator.get_all_deleted()
        self.assertEqual(type(users), list)
        self.assertNotEqual(len(users), 0)
        self.assertEqual(users[0][OperatorFields.STATUS_ACCOUNT.value], "DELETED")
        default.clean_table_operator()

    def test_get(self):
        default.register_operator()
        model = Operator(username=default.USERNAME)
        users = model.get()
        self.assertEqual(type(users), list)
        self.assertEqual(users[0][OperatorFields.USERNAME.value], default.USERNAME)
        default.clean_table_operator()

    def test_delete(self):
        username = "test_delete"
        model = OperatorModel(
            username=username,
            name="test",
            lastname="user",
            password="secret123456",
            profile="STANDARD",
            statusaccount="DELETED",
        )
        model.register()
        model = Operator(username=username)
        status = model.delete()
        self.assertEqual(status, True)

    def test_update(self):
        default.register_operator()
        model = OperatorModel(
            username=default.USERNAME,
            name="unittest",
            lastname="user",
            password="secret123456",
            profile="STANDARD",
            statusaccount="ACTIVE",
        )
        status = model.update()
        self.assertEqual(status, True)
        default.clean_table_operator()


if __name__ == "__main__":
    unittest.main()

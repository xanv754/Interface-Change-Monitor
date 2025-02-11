import unittest
import random
from constants import AccountType, ProfileType
from models import OperatorModel, Operator
from schemas import OperatorSchema
from test import default


class TestOperatorQuery(unittest.TestCase):
    def test_register(self):
        model = OperatorModel(
            username=default.USERNAME + str(random.randint(1, 255)),
            name="test",
            lastname="user",
            password="secret123456",
            profile=ProfileType.STANDARD.value,
            statusaccount=AccountType.ACTIVE.value,
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
        users = Operator.get_all_profile_active(ProfileType.STANDARD.value)
        self.assertEqual(type(users), list)
        self.assertNotEqual(len(users), 0)
        self.assertEqual(users[0][OperatorSchema.PROFILE.value], ProfileType.STANDARD.value)
        self.assertEqual(users[0][OperatorSchema.STATUS_ACCOUNT.value], AccountType.ACTIVE.value)
        default.clean_table_operator()

    def test_get_all_inactive(self):
        default.register_operator(status_account=AccountType.INACTIVE.value)
        users = Operator.get_all_inactive()
        self.assertEqual(type(users), list)
        self.assertNotEqual(len(users), 0)
        self.assertEqual(users[0][OperatorSchema.STATUS_ACCOUNT.value], AccountType.INACTIVE.value)
        default.clean_table_operator()

    def test_get_all_deleted(self):
        default.register_operator(status_account=AccountType.DELETED.value)
        users = Operator.get_all_deleted()
        self.assertEqual(type(users), list)
        self.assertNotEqual(len(users), 0)
        self.assertEqual(users[0][OperatorSchema.STATUS_ACCOUNT.value], AccountType.DELETED.value)
        default.clean_table_operator()

    def test_get(self):
        default.register_operator()
        model = Operator(username=default.USERNAME)
        users = model.get()
        self.assertEqual(type(users), list)
        self.assertEqual(users[0][OperatorSchema.USERNAME.value], default.USERNAME)
        default.clean_table_operator()

    def test_delete(self):
        username = "test_delete"
        model = OperatorModel(
            username=username,
            name="test",
            lastname="user",
            password="secret123456",
            profile=ProfileType.STANDARD.value,
            statusaccount=AccountType.DELETED.value,
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
            profile=ProfileType.STANDARD.value,
            statusaccount=AccountType.ACTIVE.value,
        )
        status = model.update()
        self.assertEqual(status, True)
        default.clean_table_operator()


if __name__ == "__main__":
    unittest.main()

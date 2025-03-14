import unittest
import random
from constants import AccountType, ProfileType
from models import OperatorModel, Operator
from schemas import OperatorSchema
from test import constants, DefaultOperator


class TestOperatorModel(unittest.TestCase):
    def test_register(self):
        new_username = constants.USERNAME + str(random.randint(1, 255))
        model = OperatorModel(
            username=new_username,
            name="unit",
            lastname="test",
            password="secret123456",
            profile=ProfileType.STANDARD.value,
            statusaccount=AccountType.ACTIVE.value,
        )
        status = model.register()
        self.assertEqual(status, True)
        new_operator = DefaultOperator.select_one_by_username(new_username)
        self.assertEqual(type(new_operator), OperatorSchema)
        self.assertEqual(new_operator.username, new_username)
        DefaultOperator.clean_table()

    def test_update(self):
        new_operator = DefaultOperator.new_insert()
        new_lastname = "Unittest2"
        model = OperatorModel(
            username=new_operator.username,
            name=new_operator.name,
            lastname=new_lastname,
            password="deprecated",
            profile=new_operator.profile,
            statusaccount=new_operator.account,
        )
        status = model.update()
        self.assertEqual(status, True)
        new_operator = DefaultOperator.select_one_by_username(new_operator.username)
        self.assertEqual(type(new_operator), OperatorSchema)
        self.assertEqual(new_operator.lastname, new_lastname)
        DefaultOperator.clean_table()

    def test_get_all(self):
        new_operator = DefaultOperator.new_insert()
        users = Operator.get_all()
        self.assertEqual(type(users), list)
        self.assertNotEqual(len(users), 0)
        self.assertEqual(users[0].username, new_operator.username)
        DefaultOperator.clean_table()

    def test_get_all_without_deleted(self):
        username_deleted = "unittest_deleted"
        DefaultOperator.new_insert(
            username=username_deleted,
            status_account=AccountType.DELETED.value
        )
        new_operator = DefaultOperator.new_insert(clean=False)
        users = Operator.get_all_without_deleted()
        self.assertEqual(type(users), list)
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].username, new_operator.username)
        DefaultOperator.clean_table()

    def test_get_all_profile_active(self):
        new_profile_type = ProfileType.STANDARD.value
        new_status_account = AccountType.ACTIVE.value
        new_operator = DefaultOperator.new_insert(
            profile=new_profile_type,
            status_account=new_status_account
        )
        users = Operator.get_all_profile_active(new_profile_type)
        self.assertEqual(type(users), list)
        self.assertNotEqual(len(users), 0)
        self.assertEqual(users[0].username, new_operator.username)
        self.assertEqual(users[0].profile, new_profile_type)
        self.assertEqual(users[0].account, new_status_account)
        DefaultOperator.clean_table()

    def test_get_all_inactive(self):
        new_status_account = AccountType.INACTIVE.value
        new_operator = DefaultOperator.new_insert(
            status_account=new_status_account
        )
        users = Operator.get_all_inactive()
        self.assertEqual(type(users), list)
        self.assertNotEqual(len(users), 0)
        self.assertEqual(users[0].username, new_operator.username)
        self.assertEqual(users[0].account, new_status_account)
        DefaultOperator.clean_table()

    def test_get_all_deleted(self):
        new_status_account = AccountType.DELETED.value
        new_operator = DefaultOperator.new_insert(
            status_account=new_status_account
        )
        users = Operator.get_all_deleted()
        self.assertEqual(type(users), list)
        self.assertNotEqual(len(users), 0)
        self.assertEqual(users[0].username, new_operator.username)
        self.assertEqual(users[0].account, new_status_account)
        DefaultOperator.clean_table()

    def test_get_operator(self):
        new_operator = DefaultOperator.new_insert()
        model = Operator(username=new_operator.username)
        user = model.get()
        self.assertEqual(type(user), OperatorSchema)
        self.assertEqual(user.username, new_operator.username)
        DefaultOperator.clean_table()

    def test_update_password(self):
        new_operator = DefaultOperator.new_insert()
        model = Operator(username=new_operator.username)
        status = model.update_password(constants.PASSWORD_TWO)
        self.assertEqual(status, True)
        new_operator = DefaultOperator.select_one_by_username(new_operator.username)
        self.assertEqual(new_operator.password, constants.PASSWORD_TWO)
        DefaultOperator.clean_table()

    def test_delete(self):
        new_operator = DefaultOperator.new_insert()
        model = Operator(username=new_operator.username)
        status = model.delete()
        self.assertEqual(status, True)
        self.assertIsNone(
            DefaultOperator.select_one_by_username(new_operator.username)
        )
        DefaultOperator.clean_table()
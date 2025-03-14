import unittest
import random
from constants import AccountType, ProfileType
from controllers import OperatorController
from schemas import OperatorSchema, RegisterUserBody, UpdateUserRootBody
from test import constants, DefaultOperator


class TestOperatorController(unittest.TestCase):
    def test_register(self):
        new_username = constants.USERNAME + str(random.randint(1, 255))
        body = RegisterUserBody(
            username=new_username,
            name="unit",
            lastname="test",
            password=constants.PASSWORD,
            profile=ProfileType.STANDARD.value,
        )
        status = OperatorController.register_operator(body)
        self.assertEqual(status, True)
        new_operator = DefaultOperator.select_one_by_username(new_username)
        self.assertEqual(new_operator.username, new_username)
        DefaultOperator.clean_table()
    
    def test_get_operator(self):
        new_operator = DefaultOperator.new_insert()
        operator = OperatorController.get_operator(new_operator.username)
        self.assertEqual(type(operator), OperatorSchema)
        self.assertEqual(operator.username, new_operator.username)
        DefaultOperator.clean_table()

    def test_get_operators(self):
        new_operator = DefaultOperator.new_insert()
        operators = OperatorController.get_operators()
        self.assertEqual(type(operators), list)
        self.assertNotEqual(len(operators), 0)
        self.assertEqual(operators[0].username, new_operator.username)
        DefaultOperator.clean_table()

    def test_get_operators_profile_active(self):
        new_profile_type = ProfileType.STANDARD.value
        new_status_account = AccountType.ACTIVE.value
        new_operator = DefaultOperator.new_insert(
            profile=new_profile_type,
            status_account=new_status_account
        )
        operators = OperatorController.get_operators_profile_active(new_profile_type)
        self.assertEqual(type(operators), list)
        self.assertNotEqual(len(operators), 0)
        self.assertEqual(operators[0].username, new_operator.username)
        self.assertEqual(operators[0].profile, new_profile_type)
        self.assertEqual(operators[0].account, new_status_account)
        DefaultOperator.clean_table()

    def test_update_operator(self):
        new_operator = DefaultOperator.new_insert()
        new_account = AccountType.INACTIVE.value
        body = UpdateUserRootBody(
            username=new_operator.username,
            name=new_operator.name,
            lastname=new_operator.lastname,
            profile=new_operator.profile,
            account=new_account,
        )
        status = OperatorController.update_operator(body)
        self.assertEqual(status, True)
        new_operator = DefaultOperator.select_one_by_username(new_operator.username)
        self.assertEqual(new_operator.account, new_account)
        DefaultOperator.clean_table()

    def test_update_password(self):
        new_operator = DefaultOperator.new_insert()
        status = OperatorController.update_password(new_operator.username, constants.PASSWORD_TWO)
        self.assertEqual(status, True)

    def test_delete_soft_operator(self):
        new_operator = DefaultOperator.new_insert()
        status = OperatorController.delete_soft_operator(new_operator.username)
        self.assertEqual(status, True)
        operator = DefaultOperator.select_one_by_username(new_operator.username)
        self.assertEqual(operator.account, AccountType.DELETED.value)
        DefaultOperator.clean_table()

if __name__ == "__main__":
    unittest.main()

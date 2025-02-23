import unittest
from constants import ProfileType
from core import SecurityCore
from schemas import OperatorResponseSchema
from utils import encrypt
from test import constants, DefaultOperator

class TestSecurity(unittest.TestCase):
    def test_password_hash(self):
        password = constants.PASSWORD
        hashed_password = encrypt.get_password_hash(password)
        self.assertIsNotNone(hashed_password)

    def test_password_verify(self):
        password = constants.PASSWORD
        hashed_password = encrypt.get_password_hash(password)
        self.assertTrue(encrypt.verify_password(password, hashed_password))

    def test_create_access_token(self):
        data = {"sub": constants.USERNAME}
        token = SecurityCore.create_access_token(data)
        self.assertIsNotNone(token)

    def test_authenticate_user(self):
        password = constants.PASSWORD
        hashed_password = encrypt.get_password_hash(password)
        new_operator = DefaultOperator.new_insert(
            password=hashed_password
        )
        user = SecurityCore.authenticate_user(new_operator.username, password)
        self.assertEqual(type(user), OperatorResponseSchema)
        self.assertEqual(user.username, new_operator.username)
        user = SecurityCore.authenticate_user(new_operator.username, "wrong_password")
        self.assertIsNone(user)
        DefaultOperator.clean_table()

    def test_get_access_root(self):
        new_operator = DefaultOperator.new_insert(
            profile = ProfileType.ROOT.value
        )
        token = SecurityCore.create_access_token({"sub": new_operator.username})
        self.assertIsNotNone(token)
        user = SecurityCore.get_access_root(token)
        self.assertEqual(type(user), OperatorResponseSchema)
        self.assertEqual(user.username, new_operator.username)
        new_operator = DefaultOperator.new_insert(
            profile = ProfileType.ADMIN.value
        )
        token = SecurityCore.create_access_token({"sub": new_operator.username})
        user = SecurityCore.get_access_root(token)
        self.assertIsNone(user)
        DefaultOperator.clean_table()

    def test_get_access_admin(self):
        new_operator = DefaultOperator.new_insert(
            profile = ProfileType.ADMIN.value
        )
        token = SecurityCore.create_access_token({"sub": new_operator.username})
        self.assertIsNotNone(token)
        user = SecurityCore.get_access_admin(token)
        self.assertEqual(type(user), OperatorResponseSchema)
        self.assertEqual(user.username, new_operator.username)
        new_operator = DefaultOperator.new_insert(
            profile = ProfileType.STANDARD.value
        )
        token = SecurityCore.create_access_token({"sub": new_operator.username})
        user = SecurityCore.get_access_admin(token)
        self.assertIsNone(user)
        DefaultOperator.clean_table()

    def test_get_access_user(self):
        new_operator = DefaultOperator.new_insert(
            profile = ProfileType.STANDARD.value
        )
        token = SecurityCore.create_access_token({"sub": new_operator.username})
        self.assertIsNotNone(token)
        user = SecurityCore.get_access_user(token)
        self.assertEqual(type(user), OperatorResponseSchema)
        self.assertEqual(user.username, new_operator.username)
        token = "E2oQCViUSHYhD6wy8UepFuX9elAjjK2hRje4HIWWOJZ5eV8Bsa9q1j1ql6I86ItP"
        user = SecurityCore.get_access_user(token)
        self.assertIsNone(user)
        DefaultOperator.clean_table()

if __name__ == '__main__':
    unittest.main()
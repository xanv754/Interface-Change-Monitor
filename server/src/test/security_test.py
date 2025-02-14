import unittest
import asyncio
from core import SecurityCore
from utils import encrypt
from test import default

class TestSecurity(unittest.TestCase):
    def test_password_hash(self):
        password = "123456"
        hashed_password = encrypt.get_password_hash(password)
        self.assertIsNotNone(hashed_password)

    def test_password_verify(self):
        password = "123456"
        hashed_password = encrypt.get_password_hash(password)
        self.assertTrue(encrypt.verify_password(password, hashed_password))

    def test_create_access_token(self):
        data = {"sub": "test"}
        token = SecurityCore.create_access_token(data)
        self.assertIsNotNone(token)

    def test_authenticate_user(self):
        default.register_operator()
        user = SecurityCore.authenticate_user(default.USERNAME, default.PASSWORD)
        self.assertEqual(user.username, default.USERNAME)
        user = SecurityCore.authenticate_user(default.USERNAME, "wrong_password")
        self.assertIsNone(user)
        default.clean_table_operator()

    def test_get_access_user(self):
        default.register_operator()
        token = SecurityCore.create_access_token({"sub": default.USERNAME})
        data = asyncio.run(SecurityCore.get_access_user(token))
        self.assertEqual(data["username"], default.USERNAME)
        token = SecurityCore.create_access_token({"sub": "test"})
        self.assertIsNone(asyncio.run(SecurityCore.get_access_user(token)))
        default.clean_table_operator()

if __name__ == '__main__':
    unittest.main()
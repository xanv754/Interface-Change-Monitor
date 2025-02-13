import unittest
import asyncio
from core import encrypt, SecurityController

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
        token = SecurityController.create_access_token(data)
        print("token ===>", token)
        self.assertIsNotNone(token)

    def test_get_access_user(self):
        token = SecurityController.create_access_token({"sub": "test"})
        data = asyncio.run(SecurityController.get_access_user(token))
        self.assertEqual(data["username"], "test")
        token = SecurityController.create_access_token({"sub": "test2"})
        self.assertRaises(Exception, SecurityController.get_access_user)

if __name__ == '__main__':
    unittest.main()
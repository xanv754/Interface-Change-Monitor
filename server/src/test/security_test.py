import unittest
from core import encrypt

class TestSecurity(unittest.TestCase):
    def test_password_hash(self):
        password = "123456"
        hashed_password = encrypt.get_password_hash(password)
        self.assertIsNotNone(hashed_password)

    def test_password_verify(self):
        password = "123456"
        hashed_password = encrypt.get_password_hash(password)
        self.assertTrue(encrypt.verify_password(password, hashed_password))

if __name__ == '__main__':
    unittest.main()
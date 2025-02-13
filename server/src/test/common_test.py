import unittest
from os import getenv
from dotenv import load_dotenv

load_dotenv(override=True)


class TestCommon(unittest.TestCase):
    def test_env(self):
        uri = getenv("URI")
        self.assertIsNotNone(uri)


if __name__ == "__main__":
    unittest.main()

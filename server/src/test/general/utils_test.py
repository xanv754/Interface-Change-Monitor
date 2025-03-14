import unittest
from os import getenv, getcwd
from dotenv import load_dotenv
from utils import Log

load_dotenv(override=True)


class TestUtils(unittest.TestCase):
    def test_env(self):
        uri = getenv("URI")
        self.assertIsNotNone(uri)

    def test_log(self):
        Log.save("This is a unit test", __file__, Log.info)
        filepath = getcwd().split("src")[0] + "system.log"
        self.assertTrue(filepath.endswith("system.log"))

if __name__ == "__main__":
    unittest.main()

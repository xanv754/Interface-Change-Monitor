import unittest
from os import getenv, getcwd
from dotenv import load_dotenv
from utils import Log

load_dotenv(override=True)


class TestCommon(unittest.TestCase):
    def test_env(self):
        uri = getenv("URI")
        self.assertIsNotNone(uri)

    def test_log(self):
        Log.save("This is a unit test", __file__, Log.info)
        filepath = getcwd().split("src")[0] + "system.log"
        self.assertTrue(filepath.endswith("system.log"))

    def test_impr(self):
        Log.impr("This is a unit test", __file__, Log.info)
        Log.impr("This is a unit test", __file__, Log.error)
        Log.impr("This is a unit test", __file__, Log.warning)
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()

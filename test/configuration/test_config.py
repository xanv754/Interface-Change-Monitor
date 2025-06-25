import unittest
from utils.config import Configuration


class Test(unittest.TestCase):
    def test_environment(self):
        """Test to read environment variables."""
        try:
            configuration = Configuration()
        except:
            self.assertTrue(False)
        else:
            self.assertTrue(configuration.uri_postgres)


if __name__ == '__main__':
    unittest.main()
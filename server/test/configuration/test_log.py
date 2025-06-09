import unittest
from utils.log import log


class Test(unittest.TestCase):
    def test_print_log(self):
        """Test to create a log."""
        try:
            log.info("Unit test log message")
        except:
            self.assertTrue(False)
        else:
            self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
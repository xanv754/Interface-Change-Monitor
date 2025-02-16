import unittest
from core import SystemConfig
from schemas import SystemConfigSchema
from test import configSystem

class TestConfig(unittest.TestCase):
    def test_get_filepath_config(self):
        system_config = SystemConfig()
        filepath = system_config.get_filepath_config()
        self.assertIsNotNone(filepath)

    def test_read_config(self):
        system_config = SystemConfig()
        data = system_config._read_config()
        self.assertIsInstance(data, dict)
        
    def test_create_system_config(self):
        config_default = configSystem.DEFAULT
        system_config = SystemConfig()
        status = system_config._create_system_config(config_default)
        self.assertEqual(status, True)

    def test_get_system_config(self):
        system_config = SystemConfig()
        config = system_config.get_system_config()
        self.assertIsInstance(config, SystemConfigSchema)

if __name__ == "__main__":
    unittest.main()
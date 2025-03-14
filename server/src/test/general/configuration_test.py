import unittest
from os import getcwd
from core import SystemConfig
from schemas import ConfigurationSchema
from test import configSystem

FILEPATH_TEST = getcwd() + "/system.config.test.json"

class TestConfig(unittest.TestCase):
    def test_get_filepath_config(self):
        system_config = SystemConfig(filepath=FILEPATH_TEST)
        filepath = system_config.get_filepath_config()
        self.assertIsNotNone(filepath)

    def test_create_system_config(self):
        system_config = SystemConfig(filepath=FILEPATH_TEST)
        status = system_config._create_system_config()
        self.assertEqual(status, True)

    def test_read_config(self):
        system_config = SystemConfig(filepath=FILEPATH_TEST)
        data = system_config._read_config()
        self.assertIsInstance(data, dict)
        
    def test_get_system_config_to_file(self):
        config_default = configSystem.DEFAULT_DICT
        system_config = SystemConfig(filepath=FILEPATH_TEST)
        status = system_config._get_system_config_to_file(config_default)
        self.assertEqual(status, True)

    def test_get_system_config(self):
        system_config = SystemConfig(filepath=FILEPATH_TEST)
        config = system_config.get_system_config()
        self.assertIsInstance(config, ConfigurationSchema)

    def test_update_config(self):
        config_default = configSystem.DEFAULT_OBJECT
        system_config = SystemConfig(filepath=FILEPATH_TEST)
        status = system_config.update_config(config_default)
        self.assertEqual(status, True)

    def test_reset_config(self):
        system_config = SystemConfig(filepath=FILEPATH_TEST)
        status = system_config.reset_config()
        self.assertEqual(status, True)

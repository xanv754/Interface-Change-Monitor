import unittest
from os import getcwd
from system import SettingHandler
from schemas import SettingSchema
from test import configSystem

FILEPATH_TEST = getcwd() + "/system.config.test.json"

class TestConfig(unittest.TestCase):
    def test_get_filepath_config(self):
        system_config = SettingHandler(filepath=FILEPATH_TEST)
        filepath = system_config.get_filepath()
        self.assertIsNotNone(filepath)

    def test_create_system_config(self):
        system_config = SettingHandler(filepath=FILEPATH_TEST)
        status = system_config.__create_setting_file()
        self.assertEqual(status, True)

    def test_read_config(self):
        system_config = SettingHandler(filepath=FILEPATH_TEST)
        data = system_config.__read_settings()
        self.assertIsInstance(data, dict)

    def test_get_system_config_to_file(self):
        config_default = configSystem.DEFAULT_DICT
        system_config = SettingHandler(filepath=FILEPATH_TEST)
        status = system_config.__create_setting_model(config_default)
        self.assertEqual(status, True)

    def test_get_system_config(self):
        system_config = SettingHandler(filepath=FILEPATH_TEST)
        config = system_config.get_settings()
        self.assertIsInstance(config, SettingSchema)

    def test_update_config(self):
        config_default = configSystem.DEFAULT_OBJECT
        system_config = SettingHandler(filepath=FILEPATH_TEST)
        status = system_config.update_settings(config_default)
        self.assertEqual(status, True)

    def test_reset_config(self):
        system_config = SettingHandler(filepath=FILEPATH_TEST)
        status = system_config.reset_settings()
        self.assertEqual(status, True)

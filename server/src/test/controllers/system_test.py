import unittest
from controllers import SystemController
from schemas import ConfigurationSchema
from test import configSystem


class TestSystemController(unittest.TestCase):
    def test_get_system_config(self):
        system_config = SystemController.get_system_config()
        self.assertIsInstance(system_config, ConfigurationSchema)

    def test_update_config(self):
        config_default = configSystem.DEFAULT_OBJECT
        status = SystemController.update_config(config_default)
        self.assertEqual(status, True)
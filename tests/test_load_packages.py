import unittest

from pathlib import Path
from domain.helpers import load_plugin_module, get_plugin_info
from domain.manager import PluginID


class TestPluginLoadPackages(unittest.TestCase):

    def setUp(self):
        self.source_dir: Path = Path("C:\\Users\\usuario\\Projects\\plugins_arch\\plugins_manager_core\\tests"
                                     "\\test_temp_plugins")

    def test_load_exists_plugin(self):
        expected_value = "test_plugin@1in0in0"
        plugin_path = self.source_dir / expected_value
        module = load_plugin_module(plugin_path)
        plugin_info = get_plugin_info(module)
        plugin_id = PluginID(plugin_info['name'], plugin_info['version'])
        self.assertEqual(str(plugin_id), expected_value)
        self.assertEqual(str(plugin_id.version), "1.0.0")

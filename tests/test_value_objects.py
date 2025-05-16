import unittest
from domain.manager import PluginVersion, PluginID
from domain.exceptions import PluginVersionError


class TestPluginVersion(unittest.TestCase):
    def test_valid_semantic_version(self):
        version = PluginVersion("1.0.0")
        self.assertEqual(version.version, "1.0.0")

    def test_invalid_semantic_version(self):
        with self.assertRaises(PluginVersionError):
            PluginVersion("1.0")

    def test_semantic_version_property(self):
        version = PluginVersion("1.0.0")
        self.assertEqual(version.semantic_version, "1.0.0")


class TestPluginId(unittest.TestCase):
    def test_valid_plugin_id(self):
        plugin_id = PluginID("plugin_name", PluginVersion("1.0.0"))
        self.assertEqual(str(plugin_id), "plugin_name@1me0me0")

    def test_invalid_version_plugin_id(self):
        with self.assertRaises(PluginVersionError):
            _ = PluginID("plugin_name", PluginVersion("1.0"))

    def test_invalid_name_plugin_id(self):
        with self.assertRaises(ValueError):
            _ = PluginID("", PluginVersion("1.0.0"))

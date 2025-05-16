import os
import unittest
from distutils.dir_util import copy_tree
from pathlib import Path

from domain.base_plugin import IPluginConfig, IPluginRuntime, IPluginControl
from domain.exceptions import PluginNotFoundError, PluginAlreadyRegisteredError
from domain.interfaces import IPluginStorage
from domain.manager import PluginConfig, PluginID, PluginVersion, Plugin, PluginManifest, PluginStatus
from infrastructure.storage import FileSystemStorage
from plugins.test_plugin import TestPluginModule


class TestPluginFileStorage(unittest.TestCase):

    def setUp(self):
        self.config = PluginConfig(
            plugins_dir=Path("C:\\Users\\usuario\\Projects\\plugins_arch\\plugins_manager_core\\plugins"),
            temp_dir=Path("C:\\Users\\usuario\\Projects\\plugins_arch\\plugins_manager_core\\tests\\test_temp_plugins"),
            enable_dependency_installation=True
        )
        self.plugin_storage: IPluginStorage = FileSystemStorage(self.config)

        self.plugin = Plugin(
            id=PluginID(
                "test_plugin",
                PluginVersion("1.0.0")
            ),
            manifest=PluginManifest(
                name="test_plugin",
                version="1.0.0",
                category="Input Plugin",
                display_name="Input Plugin",
                labels=["CSV", "Input"],
                description="description data",
                author="Yosvany Márquez Ruiz",
                entry_points={
                    "config_class": {"interface": IPluginConfig, "class": TestPluginModule},
                    "runtime_class": {"interface": IPluginRuntime, "class": TestPluginModule},
                    "control_class": {"interface": IPluginControl, "class": TestPluginModule},
                }
            ),
            status=PluginStatus.ENABLED,
        )

        plugin_id = str(self.plugin.id)
        self.temp_plugin_test = os.path.join(self.config.temp_dir, plugin_id)
        target_folder_plugin = os.path.join(self.config.plugins_dir, plugin_id)
        if not os.path.isdir(target_folder_plugin):
            os.mkdir(target_folder_plugin)
            copy_tree(self.temp_plugin_test, target_folder_plugin)

    def test_list_all_plugin_id(self):
        list_plugins = self.plugin_storage.list_all()
        self.assertEqual(len(list_plugins), 2)

    def test_list_all_installed_plugin_id(self):
        list_plugins = self.plugin_storage.list_all_installed()
        self.assertEqual(len(list_plugins), 2)

    def test_valid_remove_store_plugin(self):
        self.plugin_storage.remove(self.plugin.id)
        list_plugins = self.plugin_storage.list_all()
        self.assertEqual(len(list_plugins), 1)

        self.plugin_storage.store(self.plugin, self.temp_plugin_test)
        list_plugins = self.plugin_storage.list_all()
        self.assertEqual(len(list_plugins), 2)

    def test_invalid_remove_plugin(self):
        plugin_id = PluginID("test_plugin", PluginVersion("2.0.0"))
        with self.assertRaises(PluginNotFoundError):
            self.plugin_storage.remove(plugin_id)

        list_plugins = self.plugin_storage.list_all()
        self.assertEqual(len(list_plugins), 2)

    def test_invalid_store_plugin(self):
        with self.assertRaises(PluginAlreadyRegisteredError):
            self.plugin_storage.store(self.plugin, self.temp_plugin_test)
        list_plugins = self.plugin_storage.list_all()
        self.assertEqual(len(list_plugins), 2)

import unittest
from pathlib import Path

from domain.exceptions import PluginAlreadyRegisteredError
from domain.interfaces import IPluginStorage, IPluginService, IPluginCache
from domain.manager import PluginConfig, PluginID, PluginVersion
from domain.services import PluginService
from infrastructure.cache import InMemoryCache
from infrastructure.storage import FileSystemStorage


class TestPluginService(unittest.TestCase):

    def setUp(self):
        self.base_dir = Path("C:\\Users\\usuario\\Projects\\plugins_arch\\plugins_manager_core\\tests\\tar_files")

        self.config = PluginConfig(
            plugins_dir=Path("C:\\Users\\usuario\\Projects\\plugins_arch\\plugins_manager_core\\plugins"),
            temp_dir=Path("C:\\Users\\usuario\\Projects\\plugins_arch\\plugins_manager_core\\tests\\test_temp_plugins"),
            enable_dependency_installation=True
        )

        self.plugin_storage: IPluginStorage = FileSystemStorage(self.config)
        plugin_cache: IPluginCache = InMemoryCache()
        self.plugin_service: IPluginService = PluginService(self.config, self.plugin_storage, plugin_cache)

    @classmethod
    def setUpClass(cls): ...

    @classmethod
    def tearDownClass(cls): ...

    def test_0_register_plugin_file(self):
        plugin_id = PluginID("test_plugin", PluginVersion("3.0.0"))
        self.plugin_service.unregister_plugin(plugin_id)
        plugin_to_install = self.base_dir / "test_plugin_3.0.0.tar.gz"
        plugin = self.plugin_service.register_plugin(str(plugin_to_install))
        self.assertEqual(self.plugin_storage.exists(plugin.id), True)

    def test_1_register_already_plugin_file(self):
        plugin_id = PluginID("test_plugin", PluginVersion("3.0.0"))
        self.plugin_service.unregister_plugin(plugin_id)

        plugin_to_install = self.base_dir / "test_plugin_3.0.0.tar.gz"
        plugin = self.plugin_service.register_plugin(str(plugin_to_install))
        self.assertEqual(self.plugin_storage.exists(plugin.id), True)

        with self.assertRaises(PluginAlreadyRegisteredError):
            _ = self.plugin_service.register_plugin(str(plugin_to_install))

    def test_2_get_plugin(self):
        plugin_id = PluginID("test_plugin", PluginVersion("3.0.0"))
        plugin = self.plugin_service.get_plugin(plugin_id)
        self.assertIsNotNone(plugin)

    def test_3_list_all_installed_plugin(self):
        list_plugins = self.plugin_service.list_plugins()
        self.assertEqual(len(list_plugins), 2)
        self.assertEqual(self.plugin_service.get_cached_count(), 2)

    def test_4_list_page_installed_plugin(self):
        list_plugins = self.plugin_service.list_plugins(page=1, per_page=1)
        self.assertEqual(len(list_plugins), 1)
        self.assertEqual(self.plugin_service.get_cached_count(), 2)

    def test_5_list_category_page_installed_plugin(self):
        list_plugins = self.plugin_service.list_plugins_by_category("all")
        self.assertEqual(len(list_plugins), 2)
        list_plugins = self.plugin_service.list_plugins_by_category("all", page=1, per_page=1)
        self.assertEqual(len(list_plugins), 1)
        list_plugins = self.plugin_service.list_plugins_by_category("Input Plugin")
        self.assertEqual(len(list_plugins), 1)
        self.assertEqual(self.plugin_service.get_cached_count(), 2)

    def test_6_list_label_page_installed_plugin(self):
        list_plugins = self.plugin_service.list_plugins_by_label("all")
        self.assertEqual(len(list_plugins), 2)
        list_plugins = self.plugin_service.list_plugins_by_label("all", page=1, per_page=1)
        self.assertEqual(len(list_plugins), 1)
        list_plugins = self.plugin_service.list_plugins_by_label("Input")
        self.assertEqual(len(list_plugins), 1)
        list_plugins = self.plugin_service.list_plugins_by_label("CSV")
        self.assertEqual(len(list_plugins), 2)
        self.assertEqual(self.plugin_service.get_cached_count(), 2)

    def test_7_list_author_page_installed_plugin(self):
        list_plugins = self.plugin_service.list_plugins_by_author("all")
        self.assertEqual(len(list_plugins), 2)
        list_plugins = self.plugin_service.list_plugins_by_author("all", page=1, per_page=1)
        self.assertEqual(len(list_plugins), 1)
        list_plugins = self.plugin_service.list_plugins_by_author("Yosvany")
        self.assertEqual(len(list_plugins), 1)
        list_plugins = self.plugin_service.list_plugins_by_author("yosvany")
        self.assertEqual(len(list_plugins), 1)
        list_plugins = self.plugin_service.list_plugins_by_author("Yulia")
        self.assertEqual(len(list_plugins), 0)
        self.assertEqual(self.plugin_service.get_cached_count(), 2)

    def test_8_list_keyword_page_installed_plugin(self):
        list_plugins = self.plugin_service.search_plugins("test_")
        self.assertEqual(len(list_plugins), 2)
        list_plugins = self.plugin_service.search_plugins("test_", page=1, per_page=1)
        self.assertEqual(len(list_plugins), 1)
        list_plugins = self.plugin_service.search_plugins("yosvany")
        self.assertEqual(len(list_plugins), 1)
        list_plugins = self.plugin_service.search_plugins("3.0.0")
        self.assertEqual(len(list_plugins), 1)
        list_plugins = self.plugin_service.search_plugins("2.0.0")
        self.assertEqual(len(list_plugins), 0)
        self.assertEqual(self.plugin_service.get_cached_count(), 2)

    def test_9_list_keyword_page_installed_enabled_plugin(self):
        plugin_id = PluginID("test_plugin", PluginVersion("3.0.0"))
        self.plugin_service.disable_plugin(plugin_id)

        list_plugins = self.plugin_service.search_plugins("test_")
        self.assertEqual(len(list_plugins), 1)

        list_plugins = self.plugin_service.search_plugins("test_", page=1, per_page=1)
        self.assertEqual(len(list_plugins), 1)

        list_plugins = self.plugin_service.search_plugins("yosvany")
        self.assertEqual(len(list_plugins), 1)

        list_plugins = self.plugin_service.search_plugins("3.0.0")
        self.assertEqual(len(list_plugins), 0)

        self.assertEqual(self.plugin_service.get_cached_count(), 2)

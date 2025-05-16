import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from domain.exceptions import PluginRegistrationError, PluginAlreadyRegisteredError, PluginUnregistrationError, \
    PluginUpdateError, PluginError
from domain.helpers import extract_plugin, validate_extracted_plugin, load_plugin_module, get_plugin_info, \
    validate_entry_points, install_dependencies
from domain.interfaces import IPluginService, IPluginStorage, IPluginCache, IPluginObserver, IObserver, Event
from domain.manager import PluginConfig, Plugin, PluginManifest, PluginID, PluginStatus, dto_to_plugin


class PluginService(IPluginService, IPluginObserver):

    def __init__(self, config: PluginConfig, storage: IPluginStorage, cache: IPluginCache):
        super().__init__()
        self.config = config
        self.storage = storage
        self.cache = cache
        self.observers: List[IObserver] = []

    def register_plugin(self, tar_gz_path: str) -> Plugin:
        try:
            plugin = None
            with tempfile.TemporaryDirectory() as tmp_dir:
                extract_plugin(tar_gz_path, tmp_dir)

                plugin_dir = validate_extracted_plugin(tmp_dir)

                # Instalar dependencias
                install_dependencies(plugin_dir)

                # Cargar módulo y validar estructura
                module = load_plugin_module(plugin_dir)
                plugin_info = get_plugin_info(module)
                plugin_id = PluginID(plugin_info['name'], plugin_info['version'])

                # Validar existencia previa
                if self.storage.exists(plugin_id):
                    raise PluginAlreadyRegisteredError(plugin_id)

                # Validar entry points
                _ = validate_entry_points(module, plugin_info)

                plugin_manifest = dto_to_plugin(plugin_info)
                final_path = os.path.join(self.config.plugins_dir, str(plugin_id))
                plugin = Plugin(
                    id=plugin_id,
                    manifest=PluginManifest(**plugin_manifest),
                    status=PluginStatus.ENABLED,
                    installed_at=datetime.now(),
                    installation_path=final_path,
                )
                self.storage.store(plugin, tmp_dir)

                del sys.modules[module.__name__]
                official_plugin = Path(final_path).absolute()
                module = load_plugin_module(official_plugin)
                plugin_info = get_plugin_info(module)
                plugin_id = PluginID(plugin_info['name'], plugin_info['version'])
                plugin_manifest = dto_to_plugin(plugin_info)
                final_path = os.path.join(self.config.plugins_dir, str(plugin_id))
                plugin = Plugin(
                    id=plugin_id,
                    manifest=PluginManifest(**plugin_manifest),
                    status=PluginStatus.ENABLED,
                    installed_at=datetime.now(),
                    installation_path=final_path,
                )
                self.cache.set(str(plugin_id), plugin)

                self.notify_observers(Event.PLUGIN_INSTALLED, plugin)
            return plugin
        except PluginAlreadyRegisteredError:
            raise
        except Exception as e:
            raise PluginRegistrationError(f"Error registering plugin: {e}")

    def unregister_plugin(self, plugin_id: PluginID, exception_not_found=False):
        try:
            if not self.storage.exists(plugin_id):
                if exception_not_found:
                    raise PluginUnregistrationError(f"Plugin {str(plugin_id)} does not exist")
                return

            self.storage.remove(plugin_id)
            self.cache.delete(str(plugin_id))
            self.notify_observers(Event.PLUGIN_UNINSTALLED, plugin_id)
        except Exception as e:
            raise PluginUnregistrationError(f"Error unregistering plugin: {e}")

    def exists(self, plugin_id: PluginID) -> bool:
        return self.storage.exists(plugin_id)

    def update_plugin(self, tar_gz_path: str, plugin_id: PluginID) -> Plugin:
        try:
            self.unregister_plugin(plugin_id)
            plugin = self.register_plugin(tar_gz_path)
            self.notify_observers(Event.PLUGIN_UPDATED, plugin)
            return plugin
        except Exception as e:
            raise PluginUpdateError(f"Error updating plugin: {e}")

    def _load_plugin(self, plugin_id: PluginID) -> Optional[Plugin]:
        try:
            plugin_dir = self.config.plugins_dir / str(plugin_id)
            module = load_plugin_module(plugin_dir)
            plugin_info = get_plugin_info(module)
            plugin_id = PluginID(plugin_info['name'], plugin_info['version'])

            _ = validate_entry_points(module, plugin_info)

            plugin_manifest = dto_to_plugin(plugin_info)
            plugin = Plugin(
                id=plugin_id,
                manifest=PluginManifest(**plugin_manifest),
                status=PluginStatus.ENABLED,
                installed_at=datetime.now(),
                installation_path=str(plugin_dir),
            )
            return plugin
        except PluginError as e:
            return None

    def get_plugin(self, plugin_id: PluginID) -> Optional[Plugin]:
        try:
            str_plugin_key = str(plugin_id)
            plugin = self.cache.get(str_plugin_key)
            if plugin is None:
                plugin = self._load_plugin(plugin_id)
                self.cache.set(str_plugin_key, plugin)
            return plugin
        except PluginError as e:
            return None

    def register_observer(self, observer: IObserver):
        self.observers.append(observer)

    def unregister_observer(self, observer: IObserver):
        self.observers.remove(observer)

    def notify_observers(self, event: str, plugin: Plugin | PluginID):
        for observer in self.observers:
            observer.notify(event, plugin)

    def list_plugins(self, page: int = 1, per_page: int = 10) -> List[Plugin]:
        try:
            results = []
            plugins = self.storage.list_all_installed()
            for plugin_id in plugins:
                key_plugin_id = str(plugin_id)
                if not self.cache.key_exists(key_plugin_id):
                    plugin = self.get_plugin(plugin_id)
                    if plugin:
                        self.cache.set(key_plugin_id, plugin)
                        results.append(plugin)
                else:
                    results.append(self.cache.get(key_plugin_id))

            return results[(page-1)*per_page:page*per_page]
        except Exception as e:
            raise PluginError(f"Error listing plugins: {e}")

    def get_cached_count(self) -> int:
        return self.cache.count(".*")

    def verify_plugin_integrity(self, plugin_id: PluginID) -> bool:
        plugin = self.get_plugin(plugin_id)
        return plugin is not None

    def list_plugins_by_category(self, category: str, page: int = 1, per_page: int = 10) -> List[Plugin]:
        try:
            results = []
            plugins = self.storage.list_all_installed()
            for plugin_id in plugins:
                key_plugin_id = str(plugin_id)
                plugin = self.cache.get(key_plugin_id)
                if not plugin:
                    plugin = self.get_plugin(plugin_id)
                    if plugin:
                        self.cache.set(key_plugin_id, plugin)

                if (category == "all" or plugin.manifest.category == category) and plugin.is_enabled():
                    results.append(plugin)

            return results[(page-1)*per_page:page*per_page]
        except Exception as e:
            raise PluginError(f"Error listing plugins: {e}")

    def list_plugins_by_label(self, label: str, page: int = 1, per_page: int = 10) -> List[Plugin]:
        try:
            results = []
            plugins = self.storage.list_all_installed()
            for plugin_id in plugins:
                key_plugin_id = str(plugin_id)
                plugin = self.cache.get(key_plugin_id)
                if not plugin:
                    plugin = self.get_plugin(plugin_id)
                    if plugin:
                        self.cache.set(key_plugin_id, plugin)

                if (label == "all" or label in plugin.manifest.labels) and plugin.is_enabled():
                    results.append(plugin)

            return results[(page-1)*per_page:page*per_page]
        except Exception as e:
            raise PluginError(f"Error listing plugins: {e}")

    def list_plugins_by_author(self, author: str, page: int = 1, per_page: int = 10) -> List[Plugin]:
        try:
            results = []
            plugins = self.storage.list_all_installed()
            for plugin_id in plugins:
                key_plugin_id = str(plugin_id)
                plugin = self.cache.get(key_plugin_id)
                if not plugin:
                    plugin = self.get_plugin(plugin_id)
                    if plugin:
                        self.cache.set(key_plugin_id, plugin)

                if (author == "all" or author.upper() in plugin.manifest.author.upper()) and plugin.is_enabled():
                    results.append(plugin)

            return results[(page-1)*per_page:page*per_page]
        except Exception as e:
            raise PluginError(f"Error listing plugins: {e}")

    def search_plugins(self, keyword: str, page: int = 1, per_page: int = 10) -> List[Plugin]:
        try:
            results = []
            plugins = self.storage.list_all_installed()
            for plugin_id in plugins:
                key_plugin_id = str(plugin_id)
                plugin = self.cache.get(key_plugin_id)
                if not plugin:
                    plugin = self.get_plugin(plugin_id)
                    if plugin:
                        self.cache.set(key_plugin_id, plugin)

                str_plugin = str(plugin).upper()

                if keyword.upper() in str_plugin and plugin.is_enabled():
                    results.append(plugin)

            return results[(page-1)*per_page:page*per_page]
        except Exception as e:
            raise PluginError(f"Error listing plugins: {e}")

    def enable_plugin(self, plugin_id: PluginID) -> None:
        plugin = self.get_plugin(plugin_id)
        if plugin:
            plugin.enable()
            self.notify_observers(Event.PLUGIN_ENABLED, plugin)

    def disable_plugin(self, plugin_id: PluginID) -> None:
        plugin = self.get_plugin(plugin_id)
        if plugin:
            plugin.disable()
            self.notify_observers(Event.PLUGIN_DISABLED, plugin)

import json
import os
import shutil
from pathlib import Path
from typing import List

from domain.exceptions import PluginAlreadyRegisteredError, PluginStorageRegisterError, PluginNotFoundError, \
    PluginStorageUnregisterError
from domain.helpers import plugin_copy_tree
from domain.interfaces import IPluginStorage
from domain.manager import Plugin, PluginID, PluginConfig


class FileSystemStorage(IPluginStorage):
    _config: PluginConfig = None

    def __init__(self, config: PluginConfig):
        self._plugins_path = config.plugins_dir

    def store(self, plugin: Plugin, from_path: str) -> None:
        str_plugin_id = str(plugin.id)
        plugin_path = str(self._plugins_path)
        target_folder_plugin = os.path.join(plugin_path, str_plugin_id)

        if os.path.exists(target_folder_plugin):
            raise PluginAlreadyRegisteredError(plugin.id)
        try:
            os.makedirs(target_folder_plugin)
            plugin_copy_tree(from_path, target_folder_plugin)

            manifest = plugin.to_dict()
            installed_path = os.path.join(target_folder_plugin, "installed")

            with open(installed_path, "w") as f:
                json.dump(manifest, f)

        except OSError:
            raise PluginStorageRegisterError(plugin.id)

    def remove(self, plugin_id: PluginID) -> None:
        str_plugin_id = str(plugin_id)
        plugin_path = str(self._plugins_path)
        target_folder_plugin = os.path.join(plugin_path, str_plugin_id)
        if not os.path.exists(target_folder_plugin):
            raise PluginNotFoundError(plugin_id)
        try:
            shutil.rmtree(target_folder_plugin)
        except OSError:
            raise PluginStorageUnregisterError(plugin_id)

    def exists(self, plugin_id: PluginID) -> bool:
        plugin_path = Path(self._plugins_path) / str(plugin_id)
        return os.path.exists(plugin_path)

    def list_all(self) -> List[PluginID]:
        plugin_path = str(self._plugins_path)
        with os.scandir(plugin_path) as entries:
            folders = [entry.name for entry in entries if entry.is_dir()]
        result = []
        for folder in folders:

            if "@" not in folder:
                continue

            plugin_name, version = folder.rsplit("@", 1)
            try:
                version = version.replace(plugin_name[-2:], ".")
                plugin_id = PluginID(plugin_name, version)
                result.append(plugin_id)
            except ValueError:
                pass

        return result

    def list_all_installed(self) -> List[PluginID]:
        plugin_path = str(self._plugins_path)
        with os.scandir(plugin_path) as entries:
            folders = [entry.name for entry in entries if entry.is_dir()]
        result = []
        for folder in folders:
            if "@" not in folder:
                continue
            full_path = os.path.join(plugin_path, folder, "installed")
            if os.path.isfile(full_path):
                plugin_name, version = folder.rsplit("@", 1)
                try:
                    version = version.replace(plugin_name[-2:], ".")
                    plugin_id = PluginID(plugin_name, version)
                    result.append(plugin_id)
                except ValueError:
                    pass
        return result

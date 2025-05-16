from domain.interfaces import IPluginService
from domain.manager import PluginID, PluginVersion


class RegisterPluginCommand:
    def __init__(self, service: IPluginService):
        self.service = service

    def execute(self, tar_gz_path: str):
        self.service.register_plugin(tar_gz_path)


class UnregisterPluginCommand:
    def __init__(self, service: IPluginService):
        self.service = service

    def execute(self, name: str, version: str):
        plugin_id = PluginID(name=name, version=PluginVersion(version))
        self.service.unregister_plugin(plugin_id)


class UpdatePluginCommand:
    def __init__(self, service: IPluginService):
        self.service = service

    def execute(self, tar_gz_path: str, name: str, version: str):
        plugin_id = PluginID(name=name, version=PluginVersion(version))
        self.service.update_plugin(tar_gz_path, plugin_id)


class EnablePluginCommand:
    def __init__(self, service: IPluginService):
        self.service = service

    def execute(self, name: str, version: str):
        plugin_id = PluginID(name=name, version=PluginVersion(version))
        self.service.enable_plugin(plugin_id)


class DisablePluginCommand:
    def __init__(self, service: IPluginService):
        self.service = service

    def execute(self, name: str, version: str):
        plugin_id = PluginID(name=name, version=PluginVersion(version))
        self.service.disable_plugin(plugin_id)

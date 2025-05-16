from typing import cast, List

from domain.helpers import SingletonMeta
from domain.interfaces import IPluginService, IPluginObserver, IObserver
from domain.manager import Plugin, PluginID
from ._commands import RegisterPluginCommand, UnregisterPluginCommand, UpdatePluginCommand, EnablePluginCommand, \
    DisablePluginCommand
from ._queries import ListPluginsQuery, ListPluginsByCategoryQuery, ListPluginsByLabelQuery, ListPluginsByAuthorQuery, \
    SearchPluginsQuery, GetPluginQuery, VerifyPluginIntegrityQuery


class ApplicationService(IPluginObserver, IObserver, metaclass=SingletonMeta):

    def __init__(self, plugin_service: IPluginService):
        self.observers: List[IObserver] = []
        self.plugin_service = plugin_service
        self.plugin_observer: IPluginObserver = cast(IPluginObserver, self.plugin_service)
        self.plugin_observer.register_observer(self)

    def register_observer(self, observer: IObserver):
        self.observers.append(observer)

    def unregister_observer(self, observer: IObserver):
        self.observers.remove(observer)

    def notify_observers(self, event: str, plugin: Plugin | PluginID):
        for observer in self.observers:
            observer.notify(event, plugin)

    def notify(self, event: str, plugin: Plugin): ...

    def register_plugin(self, tar_gz_path: str):
        command = RegisterPluginCommand(self.plugin_service)
        command.execute(tar_gz_path)

    def unregister_plugin(self, name: str, version: str):
        command = UnregisterPluginCommand(self.plugin_service)
        command.execute(name, version)

    def update_plugin(self, tar_gz_path: str, name: str, version: str):
        command = UpdatePluginCommand(self.plugin_service)
        command.execute(tar_gz_path, name, version)

    def enable_plugin(self, name: str, version: str):
        command = EnablePluginCommand(self.plugin_service)
        command.execute(name, version)

    def disable_plugin(self, name: str, version: str):
        command = DisablePluginCommand(self.plugin_service)
        command.execute(name, version)

    def list_plugins(self, page: int = 1, per_page: int = 10):
        query = ListPluginsQuery(self.plugin_service)
        return query.execute(page, per_page)

    def list_plugins_by_category(self, category: str, page: int = 1, per_page: int = 10):
        query = ListPluginsByCategoryQuery(self.plugin_service)
        return query.execute(category, page, per_page)

    def list_plugins_by_label(self, label: str, page: int = 1, per_page: int = 10):
        query = ListPluginsByLabelQuery(self.plugin_service)
        return query.execute(label, page, per_page)

    def list_plugins_by_author(self, author: str, page: int = 1, per_page: int = 10):
        query = ListPluginsByAuthorQuery(self.plugin_service)
        return query.execute(author, page, per_page)

    def search_plugins(self, keyword: str, page: int = 1, per_page: int = 10):
        query = SearchPluginsQuery(self.plugin_service)
        return query.execute(keyword, page, per_page)

    def get_plugin(self, name: str, version: str):
        query = GetPluginQuery(self.plugin_service)
        return query.execute(name, version)

    def verify_plugin_integrity(self, name: str, version: str):
        query = VerifyPluginIntegrityQuery(self.plugin_service)
        return query.execute(name, version)

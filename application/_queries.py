from domain.interfaces import IPluginService
from domain.manager import PluginID, PluginVersion


class ListPluginsQuery:
    def __init__(self, service: IPluginService):
        self.service = service

    def execute(self, page: int = 1, per_page: int = 10):
        return self.service.list_plugins(page, per_page)


class ListPluginsByCategoryQuery:
    def __init__(self, service: IPluginService):
        self.service = service

    def execute(self, category: str, page: int = 1, per_page: int = 10):
        return self.service.list_plugins_by_category(category, page, per_page)


class ListPluginsByLabelQuery:
    def __init__(self, service: IPluginService):
        self.service = service

    def execute(self, label: str, page: int = 1, per_page: int = 10):
        return self.service.list_plugins_by_label(label, page, per_page)


class ListPluginsByAuthorQuery:
    def __init__(self, service: IPluginService):
        self.service = service

    def execute(self, author: str, page: int = 1, per_page: int = 10):
        return self.service.list_plugins_by_author(author, page, per_page)


class SearchPluginsQuery:
    def __init__(self, service: IPluginService):
        self.service = service

    def execute(self, keyword: str, page: int = 1, per_page: int = 10):
        return self.service.search_plugins(keyword, page, per_page)


class GetPluginQuery:
    def __init__(self, service: IPluginService):
        self.service = service

    def execute(self, name: str, version: str):
        plugin_id = PluginID(name=name, version=PluginVersion(version))
        return self.service.get_plugin(plugin_id)


class VerifyPluginIntegrityQuery:
    def __init__(self, service: IPluginService):
        self.service = service

    def execute(self, name: str, version: str):
        plugin_id = PluginID(name=name, version=PluginVersion(version))
        return self.service.verify_plugin_integrity(plugin_id)

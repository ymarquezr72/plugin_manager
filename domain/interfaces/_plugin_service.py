from abc import ABC, abstractmethod
from typing import List, Optional

from domain.manager import Plugin, PluginID


class IPluginService(ABC):
    @abstractmethod
    def register_plugin(self, tar_gz_path: str) -> None: ...

    @abstractmethod
    def unregister_plugin(self, plugin_id: PluginID, exception_not_found=False) -> None: ...

    @abstractmethod
    def exists(self, plugin_id: PluginID) -> bool: ...

    @abstractmethod
    def update_plugin(self, tar_gz_path: str, plugin_id: PluginID) -> None: ...

    @abstractmethod
    def get_plugin(self, plugin_id: PluginID) -> Optional[Plugin]: ...

    @abstractmethod
    def list_plugins(self, page: int = 1, per_page: int = 10) -> List[Plugin]: ...

    @abstractmethod
    def get_cached_count(self) -> int: ...

    @abstractmethod
    def verify_plugin_integrity(self, plugin_id: PluginID) -> bool: ...

    @abstractmethod
    def list_plugins_by_category(self, category: str, page: int = 1, per_page: int = 10) -> List[Plugin]: ...

    @abstractmethod
    def list_plugins_by_label(self, label: str, page: int = 1, per_page: int = 10) -> List[Plugin]: ...

    @abstractmethod
    def list_plugins_by_author(self, author: str, page: int = 1, per_page: int = 10) -> List[Plugin]: ...

    @abstractmethod
    def search_plugins(self, keyword: str, page: int = 1, per_page: int = 10) -> List[Plugin]: ...

    @abstractmethod
    def enable_plugin(self, plugin_id: PluginID) -> None: ...

    @abstractmethod
    def disable_plugin(self, plugin_id: PluginID) -> None: ...

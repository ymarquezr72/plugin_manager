from abc import ABC, abstractmethod
from typing import List
from domain.manager import PluginID, Plugin


class IPluginStorage(ABC):

    @abstractmethod
    def store(self, plugin: Plugin, from_path: str) -> None: ...

    @abstractmethod
    def remove(self, plugin_id: PluginID) -> None: ...

    @abstractmethod
    def exists(self, plugin_id: PluginID) -> bool: ...

    @abstractmethod
    def list_all(self) -> List[PluginID]: ...

    @abstractmethod
    def list_all_installed(self) -> List[PluginID]: ...

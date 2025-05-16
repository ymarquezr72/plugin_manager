from abc import ABC, abstractmethod
from typing import Any


class IPluginCache(ABC):
    @abstractmethod
    def set(self, key: str, value: Any) -> None: ...

    @abstractmethod
    def get(self, key: str, default=None) -> Any: ...

    @abstractmethod
    def delete(self, key: str) -> None: ...

    @abstractmethod
    def clear(self) -> None: ...

    @abstractmethod
    def key_exists(self, key: str) -> bool: ...

    @abstractmethod
    def get_keys(self, key_pattern: str) -> list[any]: ...

    @abstractmethod
    def count(self, key_pattern: str) -> int: ...

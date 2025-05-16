import re

from domain.interfaces import IPluginCache


class InMemoryCache(IPluginCache):
    def __init__(self):
        self._cache = {}

    def set(self, key: str, value: any) -> None:
        self._cache[key] = value

    def get(self, key: str, default=None) -> any:
        return self._cache.get(key, default)

    def delete(self, key: str) -> None:
        if key in self._cache:
            del self._cache[key]

    def clear(self) -> None:
        self._cache.clear()
        self._cache = {}

    def key_exists(self, key: str) -> bool:
        return key in self._cache

    def get_keys(self, key_pattern: str) -> list[any]:
        result = []
        for key in self._cache:
            if re.search(key_pattern, key):
                result.append(key)
        result.sort()
        return result

    def count(self, key_pattern: str) -> int:
        return len(self.get_keys(key_pattern))

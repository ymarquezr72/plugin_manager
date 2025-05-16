import unittest

from domain.interfaces import IPluginCache
from infrastructure.cache import InMemoryCache


class TestPluginManifest(unittest.TestCase):

    def setUp(self):
        self.cache: IPluginCache = InMemoryCache()

    def test_cache_get_keys(self):
        self.cache.set("key_001", 10)
        self.cache.set("key_002", 20)
        list_keys = self.cache.get_keys("key_")
        self.assertEqual(list_keys, ["key_001", "key_002"])
        self.cache.delete("key_001")
        list_keys = self.cache.get_keys("key_")
        self.assertEqual(list_keys, ["key_002"])
        self.cache.clear()
        list_keys = self.cache.get_keys("key_")
        self.assertEqual(list_keys, [])

    def test_invalid_cache_get_key(self):
        self.cache.set("key_001", 10)
        value = self.cache.get("key_002")
        self.assertEqual(value, None)
        list_keys = self.cache.get_keys("key_")
        self.assertEqual(list_keys, ["key_001"])

    def test_count_cache(self):
        self.cache.set("key_001", 10)
        value = self.cache.get("key_002")
        self.assertEqual(value, None)
        count = self.cache.count(".*")
        self.assertEqual(count, 1)

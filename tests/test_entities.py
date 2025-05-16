import unittest
from abc import ABC, abstractmethod

from domain.manager import PluginManifest
from domain.exceptions import PluginVersionError


class TestPluginManifest(unittest.TestCase):

    class IPluginInterfaceA(ABC):
        @abstractmethod
        def add(self, data) -> None: ...

    class IPluginInterfaceB(ABC):
        @abstractmethod
        def add(self, data) -> None: ...

    class PluginAManifestInterface(IPluginInterfaceA):
        def add(self, data) -> None: ...

    class PluginBManifestInterface(IPluginInterfaceB):
        def add(self, data) -> None: ...

    def test_valid_plugin_manifest(self):
        plugin_manifest = PluginManifest(
            name="plugin_name",
            version="0.0.1",
            description="description",
            author="author",
            display_name="display_name",
            category="category",
            labels=["label1", "label2"],
            entry_points={
                 "config_class": {
                     "interface": TestPluginManifest.IPluginInterfaceA,
                     "class": TestPluginManifest.PluginAManifestInterface,
                 },
                 "runtime_class": {
                     "interface": TestPluginManifest.IPluginInterfaceB,
                     "class": TestPluginManifest.PluginBManifestInterface
                 },
            }
        )
        self.assertEqual(str(plugin_manifest), "plugin_name (v0.0.1)")

    def test_invalid_plugin_manifest(self):
        with self.assertRaises(TypeError):
            _ = PluginManifest(
                name="plugin_name",
                version="0.0.1",
                description="description",
                author="author",
                # category="categoryA",
                display_name="display_name",
                # labels=["label1", "label2"],
                entry_points={
                    "config_class": {
                        "interface": TestPluginManifest.IPluginInterfaceA,
                        "class": TestPluginManifest.PluginAManifestInterface,
                    },
                    "runtime_class": {
                        "interface": TestPluginManifest.IPluginInterfaceB,
                        "class": TestPluginManifest.PluginBManifestInterface
                    },
                }
            )

    def test_invalid_version_plugin_manifest(self):
        with self.assertRaises(PluginVersionError):
            _ = PluginManifest(
                name="plugin_name",
                version="0.0",
                description="description",
                author="author",
                category="categoryA",
                display_name="display_name",
                # labels=["label1", "label2"],
                entry_points={
                    "config_class": {
                        "interface": TestPluginManifest.IPluginInterfaceA,
                        "class": TestPluginManifest.PluginAManifestInterface,
                    },
                    "runtime_class": {
                        "interface": TestPluginManifest.IPluginInterfaceB,
                        "class": TestPluginManifest.PluginBManifestInterface
                    },
                }
            )

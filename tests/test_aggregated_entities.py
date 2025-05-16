import unittest
from abc import ABC, abstractmethod

from domain.manager import PluginManifest, Plugin, PluginStatus
from domain.exceptions import PluginValidationError, PluginEntrypointError


class TestAggregatedEntities(unittest.TestCase):

    class IPluginInterfaceA(ABC):
        @abstractmethod
        def add(self, data) -> None: ...

        @abstractmethod
        def get_data(self) -> str: ...

    class IPluginInterfaceB(ABC):
        @abstractmethod
        def add(self, data) -> None: ...

    class PluginAManifestInterface(IPluginInterfaceA):

        def __init__(self, prm_valor, arg_parameter=None):
            self.prm_valor = prm_valor
            self.arg_parameter = arg_parameter

        def add(self, data) -> None: ...

        def get_data(self) -> str:
            return f'{self.prm_valor} {self.arg_parameter}'

    class PluginBManifestInterface(IPluginInterfaceB):
        def add(self, data) -> None: ...

    @staticmethod
    def _create_plugin_manifest() -> PluginManifest:
        return PluginManifest(
            name="plugin_name",
            version="0.0.1",
            description="description",
            author="author",
            display_name="display_name",
            category="category",
            labels=["label1", "label2"],
            entry_points={
                 "config_class": {
                     "interface": TestAggregatedEntities.IPluginInterfaceA,
                     "class": TestAggregatedEntities.PluginAManifestInterface,
                 },
                 "runtime_class": {
                     "interface": TestAggregatedEntities.IPluginInterfaceB,
                     "class": TestAggregatedEntities.PluginBManifestInterface
                 },
            }
        )

    def test_valid_aggregated_entities(self):
        plugin_manifest = TestAggregatedEntities._create_plugin_manifest()
        plugin = Plugin(
            plugin_manifest.get_plugin_id(),
            plugin_manifest,
            status=PluginStatus.DISABLED,
            installation_path="plugins"
        )
        last_char = plugin.id.name[-2:]
        expected_value = "plugin_name@0.0.1".replace(".", last_char)
        self.assertEqual(str(plugin.id), expected_value)
        self.assertEqual(plugin.is_enabled(), False)

    def test_valid_aggregated_entities_create_instance(self):
        plugin_manifest = TestAggregatedEntities._create_plugin_manifest()
        plugin = Plugin(
            plugin_manifest.get_plugin_id(),
            plugin_manifest,
            PluginStatus.ENABLED,
            installation_path="plugins"
        )
        instance = plugin.create_instance("config_class", 10, arg_parameter=100)
        result = instance.get_data()
        self.assertEqual(result, "10 100")

    def test_valid_aggregated_invalid_attribute_entities_create_instance(self):
        plugin_manifest = TestAggregatedEntities._create_plugin_manifest()
        plugin = Plugin(
            plugin_manifest.get_plugin_id(),
            plugin_manifest,
            PluginStatus.ENABLED,
            installation_path="plugins"
        )
        with self.assertRaises(AttributeError):
            instance = plugin.create_instance("config_class", 10, arg_parameter=100)
            _ = instance.get_view()

    def test_invalid_aggregated_entities_create_instance(self):
        plugin_manifest = TestAggregatedEntities._create_plugin_manifest()
        plugin = Plugin(
            plugin_manifest.get_plugin_id(),
            plugin_manifest,
            PluginStatus.ENABLED,
            installation_path="plugins"
        )
        with self.assertRaises(PluginEntrypointError):
            _ = plugin.create_instance("any_class", 10, arg_parameter=100)

    def test_invalid_aggregated_entities(self):
        plugin_manifest = TestAggregatedEntities._create_plugin_manifest()
        with self.assertRaises(TypeError):
            _ = Plugin(
                id=plugin_manifest.get_plugin_id(),
                # manifest=plugin_manifest,
                status=PluginStatus.ENABLED,
                installation_path="plugins"
            )

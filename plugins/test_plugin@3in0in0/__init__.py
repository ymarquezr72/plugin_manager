from domain.base_plugin import IPluginConfig, IPluginRuntime, IPluginControl
from .test_plugin_module import TestPluginModule


def get_info():
    return {
        "version": "3.0.0",
        "author": "Osmany Márquez Ruiz",
        "name": "test_plugin",
        "displayName": "CSV Input",
        "category": "Output Plugin",
        "description": "description data",
        "labels": ["CSV", "Output"],
        "entry_points": {
            "config_class": {"interface": IPluginConfig, "class": TestPluginModule},
            "runtime_class": {"interface": IPluginRuntime, "class": TestPluginModule},
            "control_class": {"interface": IPluginControl, "class": TestPluginModule},
        }
    }

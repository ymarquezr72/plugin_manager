from abc import ABC, abstractmethod
from domain.manager import Plugin


class Event:
    PLUGIN_INSTALLED = "plugin_installed"
    PLUGIN_UNINSTALLED = "plugin_uninstalled"
    PLUGIN_ENABLED = "plugin_enabled"
    PLUGIN_DISABLED = "plugin_disabled"
    PLUGIN_UPDATED = "plugin_updated"
    PLUGIN_INTEGRITY_CHECKED = "plugin_integrity_checked"


class IObserver(ABC):
    @abstractmethod
    def notify(self, event: str, plugin: Plugin): ...


class IPluginObserver(ABC):
    @abstractmethod
    def register_observer(self, observer: IObserver): ...

    @abstractmethod
    def unregister_observer(self, observer: IObserver): ...

    @abstractmethod
    def notify_observers(self, event: str, plugin: Plugin): ...

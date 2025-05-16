from dataclasses import dataclass, field
from datetime import datetime
from typing import TypeVar, Optional

from ._core_entities import PluginManifest
from ._value_objects import PluginID, PluginStatus
from domain.exceptions import PluginEntrypointError

T = TypeVar("T")


@dataclass(frozen=True)
class Plugin:
    id: PluginID
    manifest: PluginManifest
    status: PluginStatus
    installed_at: datetime = field(default_factory=datetime.now)
    installation_path: Optional[str] = field(default="")

    _entrypoints_class: dict[str, any] = field(init=False, repr=False, default_factory=dict[str, any])

    def _create_entrypoints_schema(self):
        entrypoints: dict[str, dict[str, T]] = self.manifest.entry_points
        for key, entrypoint in entrypoints.items():
            self._entrypoints_class[key] = entrypoint["class"]

    def __post_init__(self):
        self._create_entrypoints_schema()

    def create_instance(self, entrypoint_name: str, *args, **kwargs) -> T:
        if entrypoint_name not in self._entrypoints_class:
            raise PluginEntrypointError("Invalid entrypoint name")
        class_name = self._entrypoints_class[entrypoint_name]
        return class_name(*args, **kwargs)

    def is_enabled(self):
        return self.status == PluginStatus.ENABLED

    def enable(self):
        object.__setattr__(self, 'status', PluginStatus.ENABLED)

    def disable(self):
        object.__setattr__(self, 'status', PluginStatus.DISABLED)

    def __dict__(self):
        return {
            "id": self.id.to_dict(),
            "manifest": self.manifest.to_dict(),
            "status": self.status,
            "installed_at": self.installed_at.isoformat(),
            "installation_path": self.installation_path,
        }

    def to_dict(self):
        return self.__dict__()

    def __str__(self):
        return str(self.to_dict())

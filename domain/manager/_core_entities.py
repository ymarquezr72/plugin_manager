from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, TypeVar
from semver import Version

from ._value_objects import PluginVersion, PluginID
from domain.exceptions import PluginVersionError

T = TypeVar("T")


def dto_to_plugin(plugin_dto: dict[str, any]):
    return {
        "name": plugin_dto["name"],
        "version": plugin_dto["version"],
        "author": plugin_dto["author"],
        "display_name": plugin_dto["displayName"],
        "category": plugin_dto["category"],
        "description": plugin_dto["description"],
        "entry_points": plugin_dto["entry_points"],
        "labels": plugin_dto.get("labels", []),
    }


def plugin_to_dto(plugin_dto: dict[str, any]):
    return {
        "name": plugin_dto["name"],
        "version": plugin_dto["version"],
        "author": plugin_dto["author"],
        "displayName": plugin_dto["display_name"],
        "category": plugin_dto["category"],
        "description": plugin_dto["description"],
        "entry_points": plugin_dto["entry_points"],
        "labels": plugin_dto.get("labels", []),
    }


@dataclass(frozen=True)
class PluginManifest:
    name: str
    version: str
    author: str
    display_name: str
    category: str
    description: str
    entry_points: dict[str, dict[str, T]]
    labels: Optional[List[str]] = None

    def __post_init__(self):
        if not Version.is_valid(self.version):
            raise PluginVersionError(f"Invalid semantic version: {self.version}")

    def get_plugin_id(self):
        return PluginID(self.name, PluginVersion(self.version))

    def __str__(self):
        return f"{self.name} (v{self.version})"

    def __dict__(self):
        return dict(
            name=self.name,
            version=self.version,
            author=self.author,
            display_name=self.display_name,
            category=self.category,
            description=self.description,
            labels=self.labels,
        )

    def to_dict(self):
        return self.__dict__()


@dataclass(frozen=True)
class PluginConfig:
    plugins_dir: Path = Path("plugins")
    temp_dir: Path = Path("/tmp")
    enable_dependency_installation: bool = True

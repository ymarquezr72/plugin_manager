from dataclasses import dataclass
from enum import Enum
from semver import Version

from domain.exceptions import PluginVersionError


@dataclass(frozen=True)
class PluginStatus:
    ENABLED = "enabled"
    DISABLED = "disabled"


@dataclass(frozen=True)
class PluginVersion:
    version: str

    def __post_init__(self):
        if not Version.is_valid(self.version):
            raise PluginVersionError(f"Invalid semantic version: {self.version}")

    @property
    def semantic_version(self) -> Version:
        return Version.parse(self.version)

    def __hash__(self):
        return self.semantic_version.__hash__()

    def __str__(self):
        return f"{self.version}"


@dataclass(frozen=True)
class PluginID:
    name: str
    version: PluginVersion

    def __post_init__(self):
        if not Version.is_valid(str(self.version)):
            raise ValueError(f"Invalid semantic version: {self.version}")
        if not all([self.name, self.version]):
            raise ValueError("Missing required ID fields")
        if self.name == "":
            raise ValueError("Missing required name field")

    def __hash__(self):
        return hash(f"{self.name}_{self.version}")

    def __str__(self):
        last_char = self.name[-2:]
        return f"{self.name}@{self.version}".replace(".", last_char)

    def __dict__(self):
        return dict(
            name=self.name,
            version=str(self.version)
        )

    def to_dict(self):
        return self.__dict__()


@dataclass
class Pagination:
    page: int
    page_size: int
    total_items: int
    total_pages: int
    items: list

from abc import ABC, abstractmethod


class IPluginLogger(ABC):

    @abstractmethod
    def log(self, level: int, message: object) -> None: ...

    @abstractmethod
    def info(self, message: str, **kwargs) -> None: ...

    @abstractmethod
    def error(self, message: str, **kwargs) -> None: ...

    @abstractmethod
    def warning(self, message: str, **kwargs) -> None: ...

    @abstractmethod
    def critical(self, message: str, **kwargs) -> None: ...

    @abstractmethod
    def debug(self, message: str, **kwargs) -> None: ...

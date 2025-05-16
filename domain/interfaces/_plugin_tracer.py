from abc import ABC, abstractmethod


class IPluginTracer(ABC):

    @abstractmethod
    def trace(self, operation: str, data: dict): ...

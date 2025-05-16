from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')


class IQueueStrategy(ABC, Generic[T]):
    def __init__(self, maxsize=0):
        self._maxsize = maxsize

    @abstractmethod
    def enqueue(self, item: T) -> None:
        pass

    @abstractmethod
    def dequeue(self) -> T:
        pass

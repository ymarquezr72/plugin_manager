from typing import Generic, TypeVar
from ._queue_interface import IQueueStrategy

T = TypeVar('T')


class DataChannel(Generic[T]):
    def __init__(self, strategy: IQueueStrategy[T]):
        self._strategy = strategy

    def enqueue(self, item: T) -> None:
        self._strategy.enqueue(item)

    def dequeue(self) -> T:
        return self._strategy.dequeue()

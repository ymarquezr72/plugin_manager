from queue import Queue

from core.domain import IQueueStrategy


class InMemoryQueue(IQueueStrategy):
    def __init__(self, maxsize=0):
        super().__init__(maxsize)
        self._queue = Queue(maxsize=maxsize)

    def enqueue(self, item):
        self._queue.put(item)  # Bloquea si la cola está llena

    def dequeue(self):
        return self._queue.get()  # Bloquea si la cola está vacía

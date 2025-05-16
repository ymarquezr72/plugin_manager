from threading import Condition

from core.domain import IQueueStrategy


class InMemoryQueueThreadCondition(IQueueStrategy):
    def __init__(self, maxsize):
        super().__init__(maxsize)
        self.maxsize = maxsize
        self.queue = []
        self.condition = Condition()

    def enqueue(self, item):
        with self.condition:
            while len(self.queue) >= self.maxsize:
                self.condition.wait()  # Espera hasta que haya espacio
            self.queue.append(item)
            self.condition.notify_all()  # Notifica a los consumidores

    def dequeue(self):
        with self.condition:
            while not self.queue:
                self.condition.wait()  # Espera hasta que haya elementos
            item = self.queue.pop(0)
            self.condition.notify_all()  # Notifica a los productores
            return item

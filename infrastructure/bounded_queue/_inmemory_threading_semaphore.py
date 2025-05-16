from threading import Semaphore

from plugins.base_plugin.core.domain import IQueueStrategy


class InMemorySemaphoreQueue(IQueueStrategy):
    def __init__(self, maxsize):
        super().__init__(maxsize)
        self.maxsize = maxsize
        self.queue = []
        self.full = Semaphore(maxsize)  # Permite hasta `maxsize` elementos
        self.empty = Semaphore(0)       # Inicialmente vacía

    def enqueue(self, item):
        self.full.acquire()  # Espera si la cola está llena
        self.queue.append(item)
        self.empty.release()  # Notifica que hay elementos disponibles

    def dequeue(self):
        self.empty.acquire()  # Espera si la cola está vacía
        item = self.queue.pop(0)
        self.full.release()   # Libera un espacio en la cola
        return item

from threading import Event

from core.domain import IQueueStrategy


class InMemoryQueueThreadEvent(IQueueStrategy):
    def __init__(self, maxsize):
        super().__init__(maxsize)
        self.maxsize = maxsize
        self.queue = []
        self.full_event = Event()  # Señal para cuando la cola está llena
        self.empty_event = Event()  # Señal para cuando la cola está vacía

    def enqueue(self, item):
        while len(self.queue) >= self.maxsize:
            self.full_event.wait()  # Espera hasta que haya espacio
        self.queue.append(item)
        self.empty_event.clear()  # Reinicia la señal de vacío
        self.full_event.set()     # Indica que la cola está llena

    def dequeue(self):
        while not self.queue:
            self.empty_event.wait()  # Espera hasta que haya elementos
        item = self.queue.pop(0)
        self.full_event.clear()  # Reinicia la señal de lleno
        self.empty_event.set()   # Indica que la cola está vacía
        return item

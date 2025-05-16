from threading import Thread
import logging


class BaseThreadingChannelWorker(Thread):
    def __init__(self, channel):
        super().__init__(daemon=True)
        self.channel = channel
        self.running = True

    def run(self):
        while self.running:
            try:
                self._run()
            except Exception as e:
                logging.error(f"Error en worker de {self.channel}: {str(e)}")

    def _run(self):
        # Ejemplo: Consumir mensajes del canal
        # message = self.channel.dequeue()
        # self.process_message(message)
        pass

    def stop(self):
        self.running = False

    # @staticmethod
    # def process_message(message):
    #     # Lógica de procesamiento común
    #     print(f"Procesando mensaje: {message}")


class MultiChannelManager:
    def __init__(self):
        self.workers = []

    def add_channel(self, channel):
        worker = BaseThreadingChannelWorker(channel)
        self.workers.append(worker)
        worker.start()

    def stop_all(self):
        for worker in self.workers:
            worker.stop()

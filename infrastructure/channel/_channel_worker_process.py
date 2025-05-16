from multiprocessing import Process, Queue as MPQueue
import logging


class BaseProcessChannelWorker(Process):
    def __init__(self, channel):
        super().__init__()
        self.channel = channel
        self.exit_flag = MPQueue()  # Para notificar finalización

    def run(self):
        while True:
            if not self.exit_flag.empty():
                break
            try:
                message = self.channel.dequeue()
                self.process_message(message)
            except Exception as e:
                logging.error(f"Error en proceso {self.name}: {str(e)}")

    def stop(self):
        self.exit_flag.put(True)

    @staticmethod
    def process_message(message):
        # Lógica de procesamiento
        print(f"Procesando mensaje en proceso: {message}")


class MultiProcessManager:
    def __init__(self):
        self.processes = []

    def add_channel(self, channel):
        proc = BaseProcessChannelWorker(channel)
        self.processes.append(proc)
        proc.start()

    def stop_all(self):
        for proc in self.processes:
            proc.stop()
            proc.join()

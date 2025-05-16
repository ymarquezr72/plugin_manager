import logging


class BaseAsyncChannelWorker:
    def __init__(self, channel):
        self.channel = channel

    async def run(self):
        while True:
            try:
                message = await self.channel.dequeue_async()  # Suponiendo un método asíncrono
                await self.process_message(message)
            except Exception as e:
                logging.error(f"Error en worker async: {str(e)}")

    @staticmethod
    async def process_message(message):
        # Procesamiento asíncrono
        print(f"Procesando mensaje async: {message}")

import asyncio

from core.domain import IQueueStrategy


class InMemoryAsyncDataChannel(IQueueStrategy):
    def __init__(self, maxsize=0):
        super().__init__(maxsize)
        self._queue = asyncio.Queue(maxsize)

    async def enqueue(self, item):
        await self._queue.put(item)  # Espera asincrónicamente si está llena

    async def dequeue(self):
        return await self._queue.get()  # Espera asincrónicamente si está vacía

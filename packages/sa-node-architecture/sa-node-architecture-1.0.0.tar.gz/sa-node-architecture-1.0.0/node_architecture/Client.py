import asyncio
import json

from node_architecture.abc import Message


class Client:
    def __init__(self, path: str):
        self._path = path
        self._reader: asyncio.StreamReader | None = None
        self._writer: asyncio.StreamWriter | None = None
        self._loop = asyncio.get_event_loop()

    def connect(self):
        self._reader, self._writer = self._loop.run_until_complete(asyncio.open_unix_connection(self._path))

    async def send(self, message: dict) -> Message:
        self._writer.write(json.dumps(message).encode())
        await self._writer.drain()
        data = await self._reader.read(100)
        data = data.decode()

        return Message.create(self._reader, self._writer, json.loads(data))

    def close(self) -> None:
        self._writer.close()
        self._writer.wait_closed()

    def __call__(self, message: dict) -> Message:
        return self._loop.run_until_complete(self.send(message))

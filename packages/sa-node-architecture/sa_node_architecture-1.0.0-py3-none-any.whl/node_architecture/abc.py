from asyncio import StreamReader, StreamWriter
import json

__all__ = [
    "Message",
]


class Message:
    _reader: StreamReader
    _writer: StreamWriter

    message: dict
    type: str
    args: dict

    @staticmethod
    def create(reader: StreamReader, writer: StreamWriter, response: dict) -> "Message":
        message = Message()
        message._reader = reader
        message._writer = writer
        message.message = response["message"]
        message.type = response["type"]
        message.args = response["args"]
        return message

    async def send(self, message: dict) -> None:
        self._writer.write(json.dumps(message).encode())
        await self._writer.drain()

    def __repr__(self):
        return f'<Message type={self.type} args={self.args} content={self.message}>'

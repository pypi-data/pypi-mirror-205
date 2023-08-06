from abc import abstractmethod

from node_architecture.abc import Message
from asyncio import run


class Receiver:
    async def __call__(self, message, kwargs) -> None:
        await self._handle_message(message, kwargs)

    @abstractmethod
    async def _handle_message(self, message: Message, kwargs) -> None:
        raise NotImplementedError(
            f"Uh oh! You forgot to implement _handle_message in your receiver for {message.type}!"
            "Please implement this method and try again."
        )


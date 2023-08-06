import json
from importlib.util import find_spec, module_from_spec
from importlib.machinery import ModuleSpec
from sys import modules
from asyncio import start_unix_server, StreamReader, StreamWriter, get_event_loop
from types import ModuleType
from signal import signal, SIGINT

from node_architecture.abc import Message


class NodeArchitectureServer:
    def __init__(self, path: str):
        self.server = None
        self._path: str = path
        self._map: dict[str, ...] = {}
        self._extensions: dict[str, ModuleType] = {}

    async def _handle_client(
            self,
            reader: StreamReader,
            writer: StreamWriter
    ) -> None:
        data = await reader.read(1024)
        message = json.loads(data.decode())
        response = Message.create(reader, writer, message)

        await self._map[message["type"]](response, response.args)

    def _load_module_from_spec(self, spec: ModuleSpec, receiver_type: str) -> None:
        module = module_from_spec(spec)

        spec.loader.exec_module(module)

        self._extensions[receiver_type] = module

        setup = getattr(module, "setup")

        self._map[receiver_type] = setup()

    def add_receiver(self, receiver_type: str, file: str) -> None:
        if receiver_type in self._map:
            raise ValueError(f"Receiver type {receiver_type} already exists")

        spec = find_spec(file)
        if spec is None:
            raise FileNotFoundError(f"File {file} not found")

        self._load_module_from_spec(spec, receiver_type)

    def close(self) -> None:
        self.server.close()
        get_event_loop().close()
        exit(0)

    def serve(self):
        self.server = start_unix_server(self._handle_client, self._path)
        get_event_loop().run_until_complete(self.server)
        get_event_loop().run_forever()
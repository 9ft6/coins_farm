import asyncio
import json

import aiohttp
from aiohttp.client_ws import ClientWebSocketResponse

from config import cfg
from core.client import BaseClient
from core.logger import CustomLogger
from core.panel import BasePanel
from db.accounts import Account


class Runner:
    client: BaseClient
    logger: CustomLogger
    panel: BasePanel
    panel_class: BasePanel
    new_accounts: list[Account] = []
    clients: list[BaseClient] = {}
    halt: bool = False

    def __iter__(self):
        return iter(self.clients.values())

    def get_client_by_num(self, num: int) -> BaseClient:
        for c in self:
            if c.num == num:
                return c

    def run(self):
        self.panel = self.panel_class(self)
        asyncio.run(self._run())

    async def _run(self):
        return await asyncio.gather(
            self._run_service(),
            self.logger.run(self),
            self.panel.run(),
        )

    async def _run_service(self):
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(cfg.ws_runner_url()) as ws:
                await ws.send_json({"slug": self.client.get_slug()})

                while True:
                    if self.halt:
                        self.resume()

                    await asyncio.gather(
                        self.start_polling(ws),
                        self.start_cycle(),
                    )

    async def start_cycle(self):
        while not self.halt and (self.new_accounts or self.clients):
            if self.halt:
                break

            for account in self.new_accounts:
                if account.id not in self.clients:
                    client = self.client(len(self.clients), account)
                    client.set_panel(self.panel)
                    self.clients[client.id] = client

            await asyncio.gather(*[c.run() for c in self])

    def pause(self):
        print("stop")
        self.halt = True
        for c in self:
            c.halt = True

    def resume(self):
        print("continue")
        self.halt = False
        for c in self:
            c.halt = False

    async def start_polling(self, ws: ClientWebSocketResponse):
        async for msg in ws:
            match msg.type:
                case aiohttp.WSMsgType.TEXT:
                    await self.handle_message(json.loads(msg.data))

                case  aiohttp.WSMsgType.CLOSED:
                    print("WebSocket connection closed")
                    break
                case aiohttp.WSMsgType.ERROR:
                    print(f"Error: {msg.data}")
                    break

            if self.halt:
                break

    async def handle_message(self, msg: dict):
        print(f"Message from server: {msg}")
        match msg["type"]:
            case "add_accounts":
                print("add accounts")
                self.new_accounts.extend([Account(**i) for i in msg["items"]])
                self.pause()

    def count(self):
        return len(self.clients)

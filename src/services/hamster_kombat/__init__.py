import asyncio

from config import cfg
from services.hamster_kombat.client import HamsterClient
from services.hamster_kombat.logger import logger
from services.hamster_kombat.panel import ConsoleControlPanel


class HamsterDispatcher:
    def run(self):
        asyncio.run(self._run())

    async def _run(self):
        clients = [HamsterClient(n, h) for n, h in cfg.headers.items()]
        tasks = [c.run() for c in clients]
        tasks.append(logger.run(clients))
        tasks.append(ConsoleControlPanel(clients).run())
        await asyncio.gather(*tasks)

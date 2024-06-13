import asyncio

from client import HamsterClient
from config import cfg
from logger import logger
from panel import ConsoleControlPanel


class HamsterDispatcher:
    def run(self):
        asyncio.run(self._run())

    async def _run(self):
        clients = [HamsterClient(n, h) for n, h in cfg.headers.items()]
        tasks = [c.run_pipeline() for c in clients]
        tasks.append(logger.run(clients))
        # tasks.append(ConsoleControlPanel(logger).run())
        await asyncio.gather(*tasks)

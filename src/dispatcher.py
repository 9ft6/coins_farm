import asyncio

from client import HamsterClient
from config import cfg
from logger import logger


class HamsterDispatcher:
    def run(self):
        asyncio.run(self._run())

    async def _run(self):
        clients = [HamsterClient(n, h) for n, h in cfg.headers.items()]
        tasks = [c.run_pipeline() for c in clients]
        tasks.append(logger.run(clients))
        await asyncio.gather(*tasks)

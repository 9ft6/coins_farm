import asyncio

from core.accounts import accounts
from core.client import BaseClient
from core.logger import CustomLogger
from core.panel import BasePanel


class Runner:
    client: BaseClient
    logger: CustomLogger
    panel: BasePanel

    def run(self):
        asyncio.run(self._run())

    async def _run(self):
        tokens = accounts[self.client.slug]
        print(tokens)
        clients = [self.client(n, t) for n, t in enumerate(tokens)]
        tasks = [c.run() for c in clients]
        tasks.append(self.logger.run(clients))
        tasks.append(self.panel(clients).run())
        await asyncio.gather(*tasks)

import asyncio

from core.client import BaseClient
from core.logger import CustomLogger
from core.panel import BasePanel
from clients import accounts


class Runner:
    client: BaseClient
    logger: CustomLogger
    panel: BasePanel

    def run(self):
        asyncio.run(self._run())

    async def _run(self):
        items = await accounts.get_accounts(self.client.slug)
        clients = [self.client(n, a) for n, a in enumerate(items)]
        tasks = [c.run() for c in clients]
        tasks.append(self.logger.run(clients))
        tasks.append(self.panel(clients).run())
        await asyncio.gather(*tasks)

import asyncio
import random

import aiohttp

from config import Headers, cfg
from core.api import BaseAPI
from core.state import BaseState
from services.hamster_kombat.state import State


class BaseClient:
    api: BaseAPI
    api_class: BaseAPI
    id: int
    headers: Headers
    state: BaseState
    state_class: BaseState

    def __init__(self, id: int, headers: Headers):
        self.id = id
        self.headers = headers
        self.state = State()

    def __str__(self):
        return f"{self.id}: {self.api}"

    async def run(self):
        async with aiohttp.ClientSession() as session:
            self.api = self.api_class(session, self)
            await self.before_run()

            while True:
                await self.run_pipeline()

                to_sleep = random.randint(*cfg.sleep_time)
                self.api.debug(f"Going sleep {to_sleep} secs")
                await asyncio.sleep(to_sleep)

    async def before_run(self):
        ...

    async def run_pipeline(self):
        ...

import asyncio
import random

import aiohttp
from fake_useragent import UserAgent

from config import cfg
from core.accounts import accounts
from core.api import BaseAPI
from core.requests import Headers, Request
from core.panel import BasePanel
from core.state import BaseClientConfig, BaseState


class BaseClient:
    slug: str
    api: BaseAPI
    id: int
    headers: Headers
    state: BaseState
    cfg: BaseClientConfig
    panel: BasePanel
    host: str = None
    referer: str
    origin: str
    token: str

    def __init__(self, id: int, token: str):
        self.id = id
        self.token = token
        self.headers = self.start_headers()
        self.state = self.state_class()()
        self.cfg = self.cfg_class()()

    def __str__(self):
        return f"{self.id}: {self.api}"

    def start_headers(self) -> Headers:
        attrs = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Authorization": f"Bearer {self.token}",
            "Connection": "keep-alive",
            "Origin": self.origin,
            "Referer": self.referer,
            "User-Agent": UserAgent().random,
        }
        if self.host:
            attrs["Host"] = self.host
        return Headers(attrs)

    async def run(self):
        async with aiohttp.ClientSession() as session:
            self.api = self.api_class()(session, self)
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

    def api_class(self):
        ...

    def state_class(self):
        ...

    def cfg_class(self):
        ...

    def set_panel(self, panel):
        self.panel = panel

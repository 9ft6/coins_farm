import asyncio
import random

import aiohttp
from fake_useragent import UserAgent

from clients.accounts import accounts
from config import cfg
from core.api import BaseAPI
from core.requests import Headers, Request
from core.panel import BasePanel
from core.state import BaseClientConfig, BaseState
from db.accounts import Account, Tokens


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
    token: str = None
    query: str
    account: Account

    def __init__(self, id: int, account: Account):
        self.id = id
        self.account = account
        self.query = account.query(self.slug)
        self.state = self.state_class()()
        self.cfg = self.cfg_class()()
        self.update_headers()

    def __str__(self):
        return f"{self.id}: {self.api}"

    def update_headers(self) -> Headers:
        self.headers = self.start_headers()

    def start_headers(self) -> Headers:
        attrs = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Origin": self.origin,
            "Referer": self.referer,
            "User-Agent": UserAgent().random,
        }
        if access := self.account.access(self.slug):
            attrs["Authorization"] = f"Bearer {access}"
        if self.host:
            attrs["Host"] = self.host
        return Headers(attrs)

    async def run(self):
        async with aiohttp.ClientSession() as session:
            self.api = self.api_class()(session, self)
            await self.make_auth()
            await self.before_run()
            while True:
                await self.run_pipeline()

                to_sleep = random.randint(*cfg.sleep_time)
                self.api.debug(f"Going sleep {to_sleep} secs")
                await asyncio.sleep(to_sleep)

    async def make_auth(self):
        if self.account.access(self.slug):
            return

        response = await self.api.auth(self.query)
        if response.success:
            tokens = self.get_tokens_from_response(response)
            self.account.set_tokens(self.slug, Tokens(**tokens))
            await accounts.add_tokens(self.account.id, self.slug, tokens)
            self.update_headers()

    def get_tokens_from_response(self, response):
        return response.data["token"]

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

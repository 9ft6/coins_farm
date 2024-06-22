import asyncio
import random

import aiohttp
from fake_useragent import UserAgent

from temp.clients import accounts
from config import cfg
from core.api import BaseAPI
from core.requests import Headers
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
    halt: bool = False
    account: Account

    refresh_lock: bool = False

    def __init__(self, num: int, account: Account):
        self.num = num
        self.id = account.id
        self.account = account
        self.update_headers()
        self.query = account.query(self.slug)
        self.state = self.state_class()()
        self.cfg = self.cfg_class()()

    def __str__(self):
        return f"{self.num} - {self.id}: {self.api}"

    def update_headers(self) -> Headers:
        if not hasattr(self, "headers"):
            self.headers = Headers()
        self.headers.update(self.start_headers())

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
            self.api.info(f"started {self.num} {self.id}")

            await self.make_auth()
            await self.before_run()
            while not self.halt:
                await self.run_pipeline()

                to_sleep = random.randint(*cfg.sleep_time)
                self.api.debug(f"Going sleep {to_sleep} secs")

                slept = 0
                while slept <= to_sleep:
                    await asyncio.sleep(1)
                    slept += 1
                    if self.halt:
                        print(f"{self.num} - {self.id} halted")
                        break

    async def refresh_auth(self):
        if token := self.account.refresh(self.slug):
            if self.refresh_lock:
                print("Waiting Refreshing token")
                while self.refresh_lock:
                    print("already refreshing. wait...")
                    await asyncio.sleep(1)

                return

            print("refreshing token")
            self.refresh_lock = True
            response = await self.api.refresh_auth(token)
            await self.apply_tokens(response.data)
            self.refresh_lock = False
        else:
            await self.make_auth()

    async def make_auth(self):
        if self.account.access(self.slug):
            return

        response = await self.api.auth(self.query)
        if response.success:
            tokens = self.get_tokens_from_response(response)
            await self.apply_tokens(tokens)

    async def apply_tokens(self, tokens):
        print(f'Applying  tokens {tokens}')
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

    @classmethod
    def get_slug(cls):
        return cls.slug

import asyncio

import aiohttp

from db.models import InitData, Tokens, Account
from config import cfg


class Accounts:
    def __init__(self):
        self.base_url = cfg.host_url()

    async def add_init_data(self, game_slug: str, init_data: InitData):
        url = f"{self.base_url}/init_data/{game_slug}"
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=init_data.dict()) as response:
                return await response.json()

    async def add_tokens(self, id: str, slug: str, tokens: Tokens):
        url = f"{self.base_url}/tokens/{slug}/{id}"
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=tokens) as response:
                return await response.json()

    async def get_accounts(self, game_slug: str):
        url = f"{self.base_url}/accounts/{game_slug}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return [Account(**a) for a in await response.json()]

    async def remove_game(self, game_slug: str, user_id: str):
        url = f"{self.base_url}/remove_game/{game_slug}/{user_id}"
        async with aiohttp.ClientSession() as session:
            async with session.delete(url) as response:
                return await response.json()

    async def delete_account(self, user_id: str):
        url = f"{self.base_url}/account/{user_id}"
        async with aiohttp.ClientSession() as session:
            async with session.delete(url) as response:
                return await response.json()


accounts = Accounts()


__all__ = ["accounts"]

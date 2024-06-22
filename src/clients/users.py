import aiohttp

from config import cfg
from db.models import *

from core.logger import SubLogger


logger = SubLogger("users_api")


class Users:
    def __init__(self):
        self.base_url = cfg.host_url()

    async def request(self, method, *args, **kwargs):
        async with aiohttp.ClientSession() as session:
            async with session.request(method, *args, **kwargs) as response:
                try:
                    body = await response.json()
                except:
                    body = await response.text()

                logger.debug(f"[{method}] {args[0]} got {response.status} {body}")
                return body, response.status

    async def get(self, *args, **kwargs):
        return await self.request('GET', *args, **kwargs)

    async def post(self, *args, **kwargs):
        return await self.request('POST', *args, **kwargs)

    async def put(self, *args, **kwargs):
        return await self.request('PUT', *args, **kwargs)

    async def delete(self, *args, **kwargs):
        return await self.request('DELETE', *args, **kwargs)

    async def create_user(self, user: dict):
        user = NewTelegramUser(**user).model_dump()
        body, status = await self.post(f"{self.base_url}/users/", json=user)
        return body

    async def get_user(self, user_id: int):
        body, status = await self.get(f"{self.base_url}/users/{user_id}")
        if isinstance(body, dict):
            return TelegramUser(**body)

    async def update_user(self, user: dict):
        url = f"{self.base_url}/users/{user['id']}"
        body, status = await self.put(url, json=user)
        return body

    async def delete_user(self, user_id: int):
        body, status = await self.delete(f"{self.base_url}/users/{user_id}")
        return body

    async def approve_user(self, user_id: int):
        url = f"{self.base_url}/users/approve/{user_id}"
        body, status = await self.post(url)
        return body

    async def get_users_to_approve(self):
        body, status = await self.get(f"{self.base_url}/users/to_approve/")
        if status == 200:
            return [TelegramUser(**u) for u in body]


users_api = Users()

__all__ = ["users_api"]

from typing import Any

import aiohttp

from config import cfg


class BaseAPIClient:
    logger: Any
    path: str

    def __init__(self):
        self.base_url = f"{cfg.host_url()}{self.path}"

    async def request(self, method, *args, **kwargs):
        async with aiohttp.ClientSession() as session:
            async with session.request(method, *args, **kwargs) as response:
                try:
                    body = await response.json()
                except:
                    body = await response.text()

                self.logger.debug(f"[{method}] {args[0]} got {response.status} {body}")
                return body, response.status

    async def get(self, *args, **kwargs):
        return await self.request('GET', *args, **kwargs)

    async def post(self, *args, **kwargs):
        return await self.request('POST', *args, **kwargs)

    async def put(self, *args, **kwargs):
        return await self.request('PUT', *args, **kwargs)

    async def delete(self, *args, **kwargs):
        return await self.request('DELETE', *args, **kwargs)

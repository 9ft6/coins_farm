from clients.base import BaseAPIClient
from core.logger import SubLogger


logger = SubLogger("runners")


class Runners(BaseAPIClient):
    logger: SubLogger = logger
    path: str = "/runner"

    async def get_stat(self, slug: str):
        url = f"{self.base_url}/{slug}/stat"
        body, status = await self.get(url)
        return body

    async def get_guide(self, slug: str):
        url = f"{self.base_url}/{slug}/guide"
        body, status = await self.get(url)
        return body

    async def put_stat(self, slug: str, data: dict):
        url = f"{self.base_url}/{slug}/stat"
        await self.post(url, json=data)


runners_api = Runners()

__all__ = ["runners_api"]

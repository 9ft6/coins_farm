import aiohttp

from core.logger import LoggerMixin
from core.models import *


class BaseAPI(LoggerMixin):
    session: aiohttp.ClientSession

    def __init__(self, session, client):
        self.session = session
        self.client = client

    def log_id(self):
        return self.client.id

    async def fetch(self, request, *args, **kwargs):
        request = request(self, *args, **kwargs)
        if log_message := request.get_log_message():
            self.info(log_message)

        response = await request.do()

        if not response.success and response.status == 401:
            await self.client.refresh_auth()
            response = await self.fetch(request, *args, **kwargs)

        if response.success:
            return Ok(data=response.data)
        else:
            return Error(error=f"Error: {response.status} {response.error}")


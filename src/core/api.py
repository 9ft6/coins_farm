import aiohttp

from core.logger import LoggerMixin


class BaseAPI(LoggerMixin):
    session: aiohttp.ClientSession

    def __init__(self, session, client):
        self.session = session
        self.client = client

    def log_id(self):
        return self.client.id


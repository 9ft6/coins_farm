import json

import aiohttp
from config import cfg
from core.logger import SubLogger


logger = SubLogger("Socket")


class BotWebSocket:
    def __init__(self):
        self.ws = None

    async def connect(self):
        logger.info("Connected to WebSocket")
        self.session = aiohttp.ClientSession()
        self.ws = await self.session.ws_connect(cfg.ws_bot_url())

    async def disconnect(self):
        if self.ws:
            await self.ws.close()
        if self.session:
            await self.session.close()
        logger.info("Disconnected from WebSocket")

    async def send_and_receive(self, message: dict):
        if self.ws is None or self.ws.closed:
            raise ConnectionError("WebSocket is not connected.")

        logger.info(f"Sent message: {message}")
        while True:
            try:
                await self.ws.send_json(message)
                break
            except Exception as e:
                logger.error(e)

        response = await self.ws.receive()
        logger.info(response)
        if response.type == aiohttp.WSMsgType.TEXT:
            return json.loads(response.data)
        elif response.type == aiohttp.WSMsgType.CLOSED:
            raise ConnectionError("WebSocket connection closed.")
        elif response.type == aiohttp.WSMsgType.ERROR:
            raise ConnectionError(f"WebSocket error: {response.data}")

import asyncio

from bot.bot import FarmBot
from bot.ws import BotWebSocket


class BotApp:
    bot: FarmBot
    ws: BotWebSocket

    def __init__(self):
        self.bot = FarmBot()

    async def run(self):
        return await asyncio.gather(self.bot.serve())


def run_bot():
    asyncio.run(BotApp().run())

import asyncio

from bot.bot import FarmBot
from bot.ws import BotWebSocket


def run_bot():
    asyncio.run(FarmBot().serve())

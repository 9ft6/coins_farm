from aiogram import F
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties

from core.logger import SubLogger
from config import cfg
from bot.ws import BotWebSocket
from bot import utils, common
from bot.users import register_users_handlers
from bot.runners import register_runners_handlers


dispatcher: Dispatcher = Dispatcher()
logger = SubLogger("TGBot")
logger_rn = SubLogger("runner")
static = f"https://github.com/9ft6/coins_farm/blob/main/src/server"


class FarmBot:
    bot: Bot
    ws: BotWebSocket = BotWebSocket()

    def __init__(self):
        self.bot = Bot(
            cfg.bot_token,
            default=DefaultBotProperties(parse_mode='HTML'),
        )
        register_users_handlers(dispatcher)
        register_runners_handlers(dispatcher)

    async def serve(self):
        await self.ws.connect()
        await dispatcher.start_polling(self.bot)

    @staticmethod
    @dispatcher.message(CommandStart())
    @utils.authorize
    async def send_welcome(message: types.Message):
        await common.show_main_menu(message.from_user.id, message)

    @staticmethod
    @dispatcher.callback_query(F.data == "/start")
    @utils.authorize
    async def send_start(query: types.CallbackQuery):
        await query.answer()
        await common.show_main_menu(query.from_user.id, query.message)

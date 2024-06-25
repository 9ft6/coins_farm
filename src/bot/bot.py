from aiogram import F
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties

from config import cfg
from bot import utils, common
from bot.users import register_users_handlers
from bot.runners import register_runners_handlers


def register_base_handlers(dispatcher):
    @dispatcher.message(CommandStart())
    @utils.authorize
    async def send_welcome(message: types.Message):
        await common.show_main_menu(message.from_user.id, message)

    @dispatcher.callback_query(F.data == "/start")
    @utils.authorize
    async def send_start(query: types.CallbackQuery):
        await query.answer()
        await common.show_main_menu(query.from_user.id, query.message)


class FarmBot(Bot):
    def __init__(self):
        props = DefaultBotProperties(parse_mode='HTML')
        super().__init__(cfg.bot_token, default=props)
        self.dispatcher: Dispatcher = Dispatcher()
        register_base_handlers(self.dispatcher)
        register_runners_handlers(self.dispatcher)
        register_users_handlers(self.dispatcher)

    async def serve(self):
        await self.dispatcher.start_polling(self)

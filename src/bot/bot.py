from aiogram import F
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties

from clients.users import users_api
from clients.runners import runners_api
from core.logger import SubLogger
from config import cfg
from bot.ws import BotWebSocket
from bot import keyboards, utils


dispatcher: Dispatcher = Dispatcher()
logger = SubLogger("TGBot")
logger_rn = SubLogger("runner")


class FarmBot:
    bot: Bot
    ws: BotWebSocket = BotWebSocket()

    def __init__(self):
        self.bot = Bot(
            cfg.bot_token,
            default=DefaultBotProperties(parse_mode='HTML'),
        )

    async def serve(self):
        await self.ws.connect()
        return await dispatcher.start_polling(self.bot)

    @staticmethod
    @dispatcher.message(CommandStart())
    @utils.authorize
    async def send_welcome(message: types.Message):
        return await FarmBot.welcome(message)

    @staticmethod
    @dispatcher.callback_query(F.data == "/start")
    @utils.authorize
    async def send_start(query: types.CallbackQuery):
        return await FarmBot.welcome(query.message)

    @staticmethod
    async def welcome(message: types.Message, user_id: int = None):
        user_id = user_id or message.from_user.id
        user = await users_api.get_user(user_id)
        logger.success(f'   welcome - {user=}')

        await message.answer(
            f"Hello! {user}.",
            reply_markup=keyboards.home(user.is_admin())
        )

    @staticmethod
    @dispatcher.callback_query(F.data == 'create_user')
    async def create_user(query: types.CallbackQuery):
        logger.info(f"Create user {query.from_user.id}")
        await users_api.create_user(query.from_user.model_dump())
        return await query.message.answer(
            f"Wait...",
            reply_markup=keyboards.waiting()
        )

    @staticmethod
    @dispatcher.callback_query(F.data == 'check_status')
    @utils.authorize
    async def check_status(query: types.CallbackQuery):
        logger.info(f"Checking status of user {query.from_user.id}")
        return await FarmBot.welcome(query.message, user_id=query.from_user.id)

    @staticmethod
    @dispatcher.callback_query(F.data == 'approve_list')
    @utils.authorize
    @utils.admin_required
    async def approve_list(query: types.CallbackQuery):
        logger.info(f"Asking approve list")
        if users := await users_api.get_users_to_approve():
            return await query.message.answer(
                f"You can ban or approve user.",
                reply_markup=keyboards.users_list(users)
            )

        await query.message.answer(
            "No users to approve. Take a rest.",
            reply_markup=keyboards.home(is_admin=True)
        )

    @staticmethod
    @dispatcher.callback_query(lambda c: c.data.startswith("approve_user_"))
    @utils.authorize
    @utils.admin_required
    async def approve_user(query: types.CallbackQuery):
        user_id = int(query.data.replace("approve_user_", ""))
        result = await users_api.approve_user(user_id)
        logger.info(f"approve user {user_id} {result}")
        return result

    @staticmethod
    @dispatcher.callback_query(lambda c: c.data.startswith("runner_menu_"))
    @utils.authorize
    async def approve_user(query: types.CallbackQuery):
        user = await users_api.get_user(query.from_user.id)
        slug = query.data.replace("runner_menu_", "")
        
        stat_data = await runners_api.get_stat(slug)
        stat_message = '\n'.join([s["state"] for s in stat_data.values()])

        logger_rn.info(f"Getting '{slug}' info")
        await query.message.answer(
            f"Menu of '{slug}\n\n{stat_message}",
            reply_markup=keyboards.runner_menu(slug, user.is_admin())
        )

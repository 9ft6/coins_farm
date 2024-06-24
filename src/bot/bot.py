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


from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


class AttachAccountStates(StatesGroup):
    waiting_for_account_id = State()
    waiting_for_user_id = State()
    slug = State()


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
        return await FarmBot.welcome(message.from_user.id, message)

    @staticmethod
    @dispatcher.callback_query(F.data == "/start")
    @utils.authorize
    async def send_start(query: types.CallbackQuery):
        return await FarmBot.welcome(query.from_user.id, query.message)

    @staticmethod
    async def welcome(user_id: int, message: types.Message):
        user_id = user_id
        user = await users_api.get_user(user_id)
        name = user.username or user.first_name or user.last_name or "username"
        added = user.added_accounts.items()
        items = [f"{s:<20} {len(a)} accounts" for s, a in added]
        accounts = "\n\n".join(items)
        text = (
            "<code>"
            f"Welcome to the farm, {name}!\n"
            f"Your role: {user.role}\n"
            f"Your attached accounts:\n{accounts}"
            "</code>"
        )
        logger.success(text)
        await message.answer(text, reply_markup=keyboards.home(user.is_admin()))

    @staticmethod
    @dispatcher.callback_query(F.data == 'create_user')
    async def create_user(query: types.CallbackQuery):
        logger.info(f"Create user {query.from_user.id}")
        await users_api.create_user(query.from_user.model_dump())
        return await query.message.answer(
            f"Wait...",
            reply_markup=keyboards.waiting(),
        )

    @staticmethod
    @dispatcher.callback_query(F.data == 'check_status')
    @utils.authorize
    async def check_status(query: types.CallbackQuery):
        logger.info(f"Checking status of user {query.from_user.id}")
        return await FarmBot.welcome(query.from_user.id, query.message)

    @staticmethod
    @dispatcher.callback_query(F.data == 'approve_list')
    @utils.authorize
    @utils.admin_required
    async def approve_list(query: types.CallbackQuery):
        logger.info(f"Asking approve list")
        if users := await users_api.get_users_to_approve():
            return await query.message.answer(
                f"You can ban or approve user.",
                reply_markup=keyboards.users_list(users),
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
    @dispatcher.callback_query(
        lambda c: c.data.startswith("runner_attach_account_"))
    @utils.authorize
    @utils.admin_required
    async def attach_account(query: types.CallbackQuery, state: FSMContext):
        slug = query.data.replace("runner_attach_account_", "")
        await state.update_data(slug=slug)
        await query.message.answer("Enter account id to attach")
        await state.set_state(AttachAccountStates.waiting_for_account_id)

    @staticmethod
    @dispatcher.message(AttachAccountStates.waiting_for_account_id)
    async def process_account_id(message: types.Message, state: FSMContext):
        account_id = message.text
        await state.update_data(account_id=account_id)
        await message.answer("Ok. Now enter user_id to attach this account.")
        await state.set_state(AttachAccountStates.waiting_for_user_id)

    @staticmethod
    @dispatcher.message(AttachAccountStates.waiting_for_user_id)
    async def process_user_id(message: types.Message, state: FSMContext):
        msg_user_id = message.from_user.id
        user_id = message.text
        data = await state.get_data()
        account_id = data.get('account_id')
        slug = data.get('slug')
        response = await users_api.attach_account(slug, user_id, account_id)

        await message.answer(f"{account_id=}\n{user_id=}\n{slug=}\n{response=}")

        await state.clear()
        return await FarmBot.show_runner_menu(slug, msg_user_id, message)

    @staticmethod
    @dispatcher.callback_query(
        lambda c: c.data.startswith("runner_add_account_"))
    @utils.authorize
    async def add_account(query: types.CallbackQuery):
        await query.message.answer_photo(
            photo="http://127.0.0.1:8000/static/tg_settings.png",
            caption="Настройки Telegram"
        )

        slug = query.data.replace("runner_add_account_", "")
        result = await runners_api.get_guide(slug)
        return query.message.answer(str(result))

    @staticmethod
    @dispatcher.callback_query(lambda c: c.data.startswith("runner_menu_"))
    @utils.authorize
    async def runner_menu(query: types.CallbackQuery):
        user_id = query.from_user.id
        slug = query.data.replace("runner_menu_", "")
        return await FarmBot.show_runner_menu(slug, user_id, query.message)

    @staticmethod
    async def show_runner_menu(slug: str, user_id: int, message):
        user = await users_api.get_user(user_id)
        stat_data = await runners_api.get_stat(slug)
        if not stat_data:
            return

        if user.is_admin():
            accounts = list(stat_data.values())
        else:
            added = user.added_accounts[slug]
            accounts = [a for a in stat_data.values()
                        if user_id == a["id"]
                        or a["id"] in added]

        stat_message = '\n\n'.join([s["state"] for s in accounts])
        logger_rn.info(f"Getting '{slug}' info")
        await message.answer(
            f"Your {slug} accounts:\n\n{stat_message}",
            reply_markup=keyboards.runner_menu(slug, user.is_admin())
        )

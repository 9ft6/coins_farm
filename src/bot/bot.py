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
static = f"https://github.com/9ft6/coins_farm/blob/main/src/server"

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


base_guide_en = '''
<b>Step 1: Install and configure Telegram</b>

1. Download and install the official Telegram app on your computer. <a href="https://desktop.telegram.org/">Download Telegram for PC</a>.
2. Launch the application and log in.
3. Go to <b>Settings</b> - <b>Advanced Settings</b> - <b>Experimental Features</b>. 
4. Switch on "enable webview inspecting" option.
'''
base_guide = '''
<b>Шаг 1: Установка и настройка Telegram</b>

1. Скачайте и установите официальное приложение Telegram на ваш компьютер. <a href="https://desktop.telegram.org/">Скачать Telegram для ПК</a>.
2. Запустите приложение и авторизуйтесь.
3. Перейдите в раздел <b>Настройки</b> - <b>Продвинутые настройки</b> - <b>Экспериментальные настройки</b>.
4. Включите "enable webview inspecting" что бы необходимые данные можно было увидеть в браузере
'''


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
        await dispatcher.start_polling(self.bot)

    @staticmethod
    @dispatcher.message(CommandStart())
    @utils.authorize
    async def send_welcome(message: types.Message):
        await FarmBot.welcome(message.from_user.id, message)

    @staticmethod
    @dispatcher.callback_query(F.data == "/start")
    @utils.authorize
    async def send_start(query: types.CallbackQuery):
        await FarmBot.welcome(query.from_user.id, query)

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
        markup = keyboards.home(user.is_admin())
        await message.answer(text, reply_markup=markup)

    @staticmethod
    @dispatcher.callback_query(F.data == 'create_user')
    async def create_user(query: types.CallbackQuery):
        logger.info(f"Create user {query.from_user.id}")
        await users_api.create_user(query.from_user.model_dump())
        await query.answer(f"Wait...", reply_markup=keyboards.waiting())

    @staticmethod
    @dispatcher.callback_query(F.data == 'check_status')
    @utils.authorize
    async def check_status(query: types.CallbackQuery):
        logger.info(f"Checking status of user {query.from_user.id}")
        await FarmBot.welcome(query.from_user.id, query)

    @staticmethod
    @dispatcher.callback_query(F.data == 'approve_list')
    @utils.authorize
    @utils.admin_required
    async def approve_list(query: types.CallbackQuery):
        logger.info(f"Asking approve list")
        if users := await users_api.get_users_to_approve():
            return await query.answer(
                f"You can ban or approve user.",
                reply_markup=keyboards.users_list(users),
            )

        await query.answer(
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
        await query.answer(f"approve user {user_id} {result}")

    @staticmethod
    @dispatcher.callback_query(
        lambda c: c.data.startswith("runner_attach_account_"))
    @utils.authorize
    @utils.admin_required
    async def attach_account(query: types.CallbackQuery, state: FSMContext):
        slug = query.data.replace("runner_attach_account_", "")
        await state.update_data(slug=slug)
        await query.answer("Enter account id to attach")
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
        img_url = ("https://github.com/9ft6/coins_farm/blob/"
                   "main/src/server/static/{}?raw=true")
        await query.message.answer_photo(
            photo=img_url.format("tg_settings.png"),
            caption=base_guide
        )

        slug = query.data.replace("runner_add_account_", "")
        await query.message.answer_photo(
            photo=img_url.format("hamster_debugger.png"),
            caption=await runners_api.get_guide(slug)
        )
        await query.answer("Enter account id to add.")

    @staticmethod
    @dispatcher.callback_query(lambda c: c.data.startswith("change_role_"))
    @utils.authorize
    @utils.admin_required
    async def change_role(query: types.CallbackQuery):
        user_id = int(query.data.replace("change_role_", ""))
        su_id = cfg.super_user_id
        if user_id == su_id and su_id != query.from_user.id:
            await query.answer("Ti shto, ahuel? ))")
            user_id = query.from_user.id
        else:
            if user_id == query.from_user.id:
                return await query.answer(
                    "You can't change your own role."
                )
        await users_api.change_role(user_id)
        await FarmBot.show_users_menu(query)

    @staticmethod
    @dispatcher.callback_query(lambda c: c.data.startswith("ban_user_"))
    @utils.authorize
    @utils.admin_required
    async def ban_user(query: types.CallbackQuery):
        user_id = int(query.data.replace("ban_user_", ""))
        su_id = cfg.super_user_id
        if user_id == su_id and su_id != query.from_user.id:
            await query.answer("Ti shto, ahuel? ))")
            user_id = query.from_user.id
        else:
            if user_id == query.from_user.id:
                return await query.answer(
                    "You can't ban yourself, idiot."
                )

        await users_api.ban_unban(user_id)
        await FarmBot.show_users_menu(query)

    @staticmethod
    @dispatcher.callback_query(lambda c: c.data.startswith("user_info_"))
    @utils.authorize
    @utils.admin_required
    async def user_info(query: types.CallbackQuery):
        user_id = int(query.data.replace("user_info_", ""))
        user = await users_api.get_user(user_id)
        lines = [f"{k:<17} : {v}" for k, v in user.model_dump().items()]
        text = "\n".join(lines)
        await query.answer(f"<code>{text}</code>")

    @staticmethod
    @dispatcher.callback_query(F.data == "users_menu")
    @utils.authorize
    @utils.admin_required
    async def users_menu(query: types.CallbackQuery):
        await FarmBot.show_users_menu(query)

    @staticmethod
    async def show_users_menu(query: types.CallbackQuery):
        users = await users_api.get_users()
        await query.answer(
            text=f"Last 50 users:",
            reply_markup=keyboards.user_menu(users),
        )

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
        return await message.answer(
            f"Your {slug} accounts:\n\n{stat_message}",
            reply_markup=keyboards.runner_menu(slug, user.is_admin())
        )

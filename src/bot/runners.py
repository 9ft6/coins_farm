from aiogram import types

from clients.users import users_api
from clients.runners import runners_api
from bot import utils, common

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


def register_runners_handlers(dispatcher):
    @dispatcher.callback_query(
        lambda c: c.data.startswith("runner_attach_account_"))
    @utils.authorize
    @utils.admin_required
    async def attach_account(query: types.CallbackQuery, state: FSMContext):
        await query.answer()
        slug = query.data.replace("runner_attach_account_", "")
        await state.update_data(slug=slug)
        await query.message.answer("Enter account id to attach")
        await state.set_state(AttachAccountStates.waiting_for_account_id)

    @dispatcher.message(AttachAccountStates.waiting_for_account_id)
    async def process_account_id(message: types.Message, state: FSMContext):
        account_id = message.text
        await state.update_data(account_id=account_id)
        await message.answer("Ok. Now enter user_id to attach this account.")
        await state.set_state(AttachAccountStates.waiting_for_user_id)

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
        return await common.show_runner_menu(slug, msg_user_id, message)

    @dispatcher.callback_query(
        lambda c: c.data.startswith("runner_add_account_"))
    @utils.authorize
    async def add_account(query: types.CallbackQuery):
        await query.answer()
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
        await query.message.answer("Enter account id to add.")

    @dispatcher.callback_query(lambda c: c.data.startswith("runner_menu_"))
    @utils.authorize
    async def runner_menu(query: types.CallbackQuery):
        await query.answer()
        user_id = query.from_user.id
        slug = query.data.replace("runner_menu_", "")
        return await common.show_runner_menu(slug, user_id, query.message)

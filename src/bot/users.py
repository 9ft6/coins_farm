from aiogram import F
from aiogram import types

from clients.users import users_api
from core.logger import SubLogger
from config import cfg
from bot import utils, common, keyboards

logger = SubLogger("TGBot")


def register_users_handlers(dispatcher):
    @dispatcher.callback_query(lambda c: c.data.startswith("change_role_"))
    @utils.authorize
    @utils.admin_required
    async def change_role(query: types.CallbackQuery):
        await query.answer()
        user_id = int(query.data.replace("change_role_", ""))
        su_id = cfg.super_user_id
        if user_id == su_id and su_id != query.from_user.id:
            await query.message.answer("Ti shto, ahuel? ))")
            user_id = query.from_user.id
        else:
            if user_id == query.from_user.id:
                return await query.message.answer(
                    "You can't change your own role."
                )
        await users_api.change_role(user_id)
        await common.show_users_menu(query)

    @dispatcher.callback_query(lambda c: c.data.startswith("ban_user_"))
    @utils.authorize
    @utils.admin_required
    async def ban_user(query: types.CallbackQuery):
        await query.answer()
        user_id = int(query.data.replace("ban_user_", ""))
        su_id = cfg.super_user_id
        if user_id == su_id and su_id != query.from_user.id:
            await query.message.answer("Ti shto, ahuel? ))")
            user_id = query.from_user.id
        else:
            if user_id == query.from_user.id:
                return await query.message.answer(
                    "You can't ban yourself, idiot."
                )

        await users_api.ban_unban(user_id)
        await common.show_users_menu(query)

    @dispatcher.callback_query(lambda c: c.data.startswith("user_info_"))
    @utils.authorize
    @utils.admin_required
    async def user_info(query: types.CallbackQuery):
        await query.answer()
        user_id = int(query.data.replace("user_info_", ""))
        user = await users_api.get_user(user_id)
        lines = [f"{k:<17} : {v}" for k, v in user.model_dump().items()]
        text = "\n".join(lines)
        await query.message.answer(f"<code>{text}</code>")

    @dispatcher.callback_query(F.data == "users_menu")
    @utils.authorize
    @utils.admin_required
    async def users_menu(query: types.CallbackQuery):
        await query.answer()
        await common.show_users_menu(query)

    @dispatcher.callback_query(F.data == 'create_user')
    async def create_user(query: types.CallbackQuery):
        logger.info(f"Create user {query.from_user.id}")
        await users_api.create_user(query.from_user.model_dump())
        await query.answer(f"Wait...", reply_markup=keyboards.waiting())

    @dispatcher.callback_query(lambda c: c.data.startswith("approve_user_"))
    @utils.authorize
    @utils.admin_required
    async def approve_user(query: types.CallbackQuery):
        await query.answer()
        user_id = int(query.data.replace("approve_user_", ""))
        result = await users_api.approve_user(user_id)
        logger.info(f"approve user {user_id} {result}")
        await query.message.answer(f"approve user {user_id} {result}")

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

    @dispatcher.callback_query(F.data == 'check_status')
    @utils.authorize
    async def check_status(query: types.CallbackQuery):
        await query.answer("Checking status...")
        logger.info(f"Checking status of user {query.from_user.id}")
        await common.show_main_menu(query.from_user.id, query.message)

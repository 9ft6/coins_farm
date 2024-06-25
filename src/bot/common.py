from aiogram import types

from bot import keyboards
from clients.users import users_api
from clients.runners import runners_api
from core.logger import SubLogger

logger = SubLogger("TGBot")
logger_rn = SubLogger("runner")


async def show_main_menu(user_id: int, message: types.Message):
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


async def show_users_menu(query: types.CallbackQuery):
    users = await users_api.get_users()
    await query.message.answer(
        text=f"Last 50 users:",
        reply_markup=keyboards.user_menu(users),
    )


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

    accounts = sorted(accounts, key=lambda a: a["id"])
    accounts = [f"{i + 1:0>2} {s['state']}" for i, s in enumerate(accounts)]
    stat_message = '\n\n'.join(accounts)
    logger_rn.info(f"Getting '{slug}' info")
    return await message.answer(
        f"Your {slug} accounts:\n\n{stat_message}",
        reply_markup=keyboards.runner_menu(slug, user.is_admin())
    )

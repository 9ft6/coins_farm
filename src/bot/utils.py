import functools

from aiogram import types
from aiogram.types import CallbackQuery

from clients.users import users_api
from bot import keyboards


def admin_required(handler):
    @functools.wraps(handler)
    async def wrapper(query: types.CallbackQuery, *args, **kwargs):
        user_id = query.from_user.id
        user = await users_api.get_user(user_id)

        if not user or not user.is_admin():
            await query.message.answer(
                "Access denied. Admins only.",
                reply_markup=keyboards.start_btn(),
            )
            return

        return await handler(query, *args, **kwargs)

    return wrapper


def authorize(handler):
    """
    decorator to do basic actions to new users
    """
    @functools.wraps(handler)
    async def wrapper(query: CallbackQuery, *args, **kwargs):
        message = query.message if isinstance(query, CallbackQuery) else query
        user_id = query.from_user.id
        if user := await users_api.get_user(user_id):
            if user.need_update_info:
                user_data = message.from_user.model_dump()
                if await users_api.update_user(user_data):
                    user.need_update_info = False

            match user.status:
                case "wait_approve":
                    return await message.answer(
                        f"Wait...",
                        reply_markup=keyboards.waiting(),
                    )
                case "declined":
                    return await message.answer("Go away.")
                case "approved":
                    return await handler(query, *args, **kwargs)
                case _:
                    return await message.answer("Unknown user status.")

        return await message.answer(
            f"If you know what you doing - keep going.",
            reply_markup=keyboards.create_user()
        )

    return wrapper

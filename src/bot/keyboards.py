from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.models import TelegramUser


def start_btn():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text="Start",
        callback_data="/start"
    ))
    return builder.as_markup()


def create_user():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text="Ask to join",
        callback_data="create_user"
    ))
    return builder.as_markup()


def waiting():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text="Check",
        callback_data="check_status"
    ))
    return builder.as_markup()


def home(is_admin: bool):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text="Bloom",
        callback_data="runner_menu_bloom"
    ))
    builder.row(InlineKeyboardButton(
        text="Hamster Kombat",
        callback_data="runner_menu_hamster_kombat"
    ))
    if is_admin:
        builder.row(InlineKeyboardButton(
            text="Approve users",
            callback_data="approve_list"
        ))
    return builder.as_markup()


def users_list(users: list[TelegramUser]):
    builder = InlineKeyboardBuilder()
    for user in users:
        user_state = f"{user.last_name} {user.first_name} {user.id}"
        builder.row(
            InlineKeyboardButton(
                text=f"Approve {user_state}",
                callback_data=f"approve_user_{user.id}"
            ),
            InlineKeyboardButton(
                text=f"Ban {user_state}",
                callback_data=f"ban_user_{user.id}"
            ),
        )
    return builder.as_markup()


def runner_menu(slug: str, is_admin: bool):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text="Add account",
        callback_data=f"runner_add_account_{slug}"
    ))
    builder.row(InlineKeyboardButton(
        text="Change game",
        callback_data=f"/start"
    ))
    builder.row(InlineKeyboardButton(
        text="Delete account",
        callback_data=f"runner_delete_account_{slug}"
    ))
    builder.row(InlineKeyboardButton(
        text="Account Operations",
        callback_data=f"runner_operations_account_{slug}"
    ))
    if is_admin:
        builder.row(InlineKeyboardButton(
            text="Attach Account",
            callback_data=f"runner_attach_account_{slug}"
        ))
        builder.row(InlineKeyboardButton(
            text=f"Stop or Start {slug} runner",
            callback_data=f"runner_stop_start_{slug}"
        ))
    return builder.as_markup()

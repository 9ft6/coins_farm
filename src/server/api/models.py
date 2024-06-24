from typing import Literal

from pydantic import BaseModel


Role = Literal["admin", "user"]
roles: list[Role] = ["admin", "user"]
Status = Literal["approved", "wait_approve", "declined"]
statuses: list[Status] = ["approved", "wait_approve", "declined"]


class TelegramUser(BaseModel):
    id: int
    role: Role
    status: Status
    need_update_info: bool = False
    added_accounts: list = []

    # tg fields
    first_name: str | None = None
    last_name: str | None = None
    language_code: str | None = None
    username: str | None = None
    is_premium: bool | None = None
    is_bot: bool | None = None

    def is_admin(self):
        return self.role == "admin"


class UpdateTelegramUserRequest(BaseModel):
    need_update_info: bool = False
    first_name: str | None = None
    last_name: str | None = None
    language_code: str | None = None
    username: str | None = None
    is_premium: bool | None = None
    is_bot: bool | None = None


class AttachAccountToUserRequest(BaseModel):
    user_id: int
    account_id: int

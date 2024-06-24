import urllib.parse
import json
from typing import Literal

from pydantic import BaseModel, Extra


Role = Literal["admin", "user"]
roles: list[Role] = ["admin", "user"]
Status = Literal["approved", "wait_approve", "declined"]
statuses: list[Status] = ["approved", "wait_approve", "declined"]


class TelegramUser(BaseModel):
    id: int
    role: Role
    status: Status
    need_update_info: bool = False
    added_accounts: dict = {}

    # tg fields
    first_name: str | None = None
    last_name: str | None = None
    language_code: str | None = None
    username: str | None = None
    is_premium: bool | None = None
    is_bot: bool | None = None

    def is_admin(self):
        return self.role == "admin"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ApprovedUser(TelegramUser):
    status: Status = "approved"


class DefaultUser(ApprovedUser):
    need_update_info: bool = True


class NewTelegramUser(TelegramUser):
    status: Status = "wait_approve"
    role: Role = "user"


class Tokens(BaseModel):
    access: str
    refresh: str | None = None

    class Config:
        extra = Extra.ignore


class InitData(BaseModel):
    user_id: int | None = None
    query_id: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    language_code: str | None = None
    allows_write_to_pm: bool | None = None
    auth_date: int | None = None
    hash_value: str | None = None

    data: str | None = None
    tokens: dict[str, str] = {}

    @classmethod
    def from_string(cls, data: str):
        if data:
            return cls(**cls.parse_tg_data(data))

    def get_token_by_slug(self, slug: str):
        return self.tokens.get(slug)

    def add_token_by_slug(self, slug: str, token: str):
        self.tokens[slug] = token

    @staticmethod
    def parse_tg_data(data: str) -> dict:
        parsed_data = urllib.parse.parse_qs(data)
        user_json = parsed_data.get('user', [None])[0]
        result = {"data": data}
        if user_json:
            user_data = json.loads(urllib.parse.unquote(user_json))
            result.update({
                "query_id": parsed_data.get('query_id', [None])[0],
                "user_id": user_data.get('id'),
                "first_name": user_data.get('first_name'),
                "last_name": user_data.get('last_name'),
                "language_code": user_data.get('language_code'),
                "allows_write_to_pm": user_data.get('allows_write_to_pm'),
                "auth_date": int(parsed_data.get('auth_date', [0])[0]),
                "hash_value": parsed_data.get('hash', [None])[0]
            })

        return result


class Account(BaseModel):
    id: int
    init_datas: dict[str, InitData] = {}
    tokens: dict[str, Tokens] = {}

    @staticmethod
    def from_init_data(game: str, data: InitData):
        account = Account(id=data.user_id)
        account.init_datas[game] = data
        return account

    def access(self, slug: str) -> str | None:
        if tokens := self.tokens.get(slug):
            return tokens.access

    def refresh(self, slug: str) -> str | None:
        if tokens := self.tokens.get(slug):
            return tokens.refresh

    def query(self, slug: str) -> str | None:
        if init_data := self.init_datas.get(slug):
            return init_data.data

    def set_init_data(self, slug: str, data: InitData):
        self.init_datas[slug] = data

    def set_tokens(self, slug: str, tokens: Tokens):
        self.tokens[slug] = tokens

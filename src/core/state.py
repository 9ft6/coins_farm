from pydantic import BaseModel

from core.models import Result
from core.models import TgUser


class BaseState(BaseModel):
    data: dict = {}
    user: TgUser | None = None
    user_class: BaseModel

    def set_state(self, result: Result):
        self.data = result.data

    def set_user(self, user: dict):
        self.user = self.user_class(**user)

    def update(self, result: Result | dict):
        if result:
            result = result if isinstance(result, dict) else result.data
            self.data.update(result)

    def username(self):
        if self.user:
            return f"{self.user.name[:7]} {self.user.last_name[:7]}"
        else:
            return "Unknown"


class BaseClientConfig:
    ...

from pydantic import BaseModel

from core.models import Result
from core.models import User


class BaseState(BaseModel):
    data: dict = {}
    user: User | None = None

    def set_state(self, result: Result):
        self.data = result.data

    def set_user(self, user: dict):
        self.user = User(**user)

    def update(self, result: Result):
        self.data.update(result.data)

    def username(self):
        if self.user:
            return f"{self.user.name[:7]} {self.user.last_name[:7]}"
        else:
            return "Unknown"

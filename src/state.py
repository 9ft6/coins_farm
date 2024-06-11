import json

from pydantic import BaseModel

from api import Result
from models import User


class State(BaseModel):
    data: dict = {}
    user: User | None = None

    def set_state(self, result: Result):
        self.data = result.data

    def set_user(self, user: dict):
        self.user = User(**user)

    def update(self, result: Result):
        self.data.update(result.data)

    def need_to_taps(self):
        user = self.data["clickerUser"]
        if user["availableTaps"] == user['maxTaps']:
            return user["availableTaps"]

    def balance(self):
        return self.data.get("clickerUser", {}).get("balanceCoins", "0")

    def taps_count(self):
        if user := self.data.get("clickerUser", {}):
            return f'{user["availableTaps"]}/{user["maxTaps"]}'

        return "0"

    def coins_per_hour(self):
        return self.data.get("clickerUser", {}).get("earnPassivePerHour", "0")

    def username(self):
        if self.user:
            return f"{self.user.name[:7]} {self.user.last_name[:7]}"
        else:
            return "Unknown"

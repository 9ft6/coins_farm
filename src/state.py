import json

from pydantic import BaseModel

from api.models import Result
from models import User


class Statistics:
    stat: dict = {
        "taps": 0,
        "upgrades": 0,
        "upgrades_price": 0,
        "coins_per_hour": 0,
    }
    start_balance: int = 0

    def set_start_balance(self, value):
        self.start_balance = value

    def set_stat(self, name, value):
        if name in self.stat:
            self.stat[name] += value

    def stat_taps(self, value):
        return self.set_stat("tapped", value)

    def stat_upgrades(self, value=1):
        return self.set_stat("upgrades", value)

    def stat_upgrades_price(self, value):
        return self.set_stat("upgrades_price", value)

    def stat_coins_per_hour(self, value):
        return self.set_stat("coins_per_hour", value)


class State(BaseModel, Statistics):
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

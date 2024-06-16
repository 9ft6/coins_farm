from core.state import BaseState, BaseClientConfig


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


class HamsterConfig(BaseClientConfig):
    need_upgrade_depends: bool = True
    auto_upgrade: bool = False
    auto_task: bool = False
    auto_depends: bool = True


class HamsterState(BaseState, Statistics):
    def has_morse(self):
        return not self.data.get("dailyCipher", {}).get("isClaimed")

    def has_combo(self):
        return not self.data.get("dailyCombo", {}).get("isClaimed")

    def user_level(self):
        if user := self.data.get("clickerUser"):
            return user["level"]

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

    def get_upgrades_by_ids(self, ids: list[str]):
        if not ids:
            return []

        upgrades = self.data.get("upgradesForBuy", [])
        return [u for u in upgrades if u["id"] in ids]

from core.state import BaseState, BaseClientConfig
from core.requests import Response
from runners.bloom.models import BloomUser, BaseModel


class Statistics:
    stat: dict = {
        "game_coins": 0,
        "friends_coins": 0,
    }

    def set_start_balance(self, value):
        self.start_balance = value

    def set_stat(self, name, value):
        if name in self.stat:
            self.stat[name] += value

    def stat_game_coins(self, value):
        return self.set_stat("game_coins", value)

    def stat_friends_coins(self, value=1):
        return self.set_stat("friends_coins", value)


class BloomState(BaseState, Statistics):
    user_class: BaseModel = BloomUser
    play_passes: int = 0
    balance: int = 0

    def set_balance(self, play_passes: int, balance: int):
        self.play_passes = play_passes
        self.balance = balance

    def has_pass(self):
        return self.play_passes > 0

    def get_stats(self):
        return (f"claimed friends: + {self.stat['friends_coins']}  "
                f"game: + {self.stat['game_coins']}")


class BloomConfig(BaseClientConfig):
    ...

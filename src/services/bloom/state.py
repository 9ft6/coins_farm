from core.state import BaseState, BaseClientConfig
from core.requests import Response
from services.bloom.models import BloomUser, BaseModel


class BloomState(BaseState):
    user_class: BaseModel = BloomUser
    play_passes: int = 0
    balance: int = 0

    def set_balance(self, play_passes: int, balance: int):
        self.play_passes = play_passes
        self.balance = balance

    def has_pass(self):
        return self.play_passes > 0


class BloomConfig(BaseClientConfig):
    ...

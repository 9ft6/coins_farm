from time import time

from pydantic import Field

from core.requests import PostRequest
from core import utils


class Post(PostRequest):
    base_url: str = "https://api.hamsterkombat.io/clicker"


class AuthPost(PostRequest):
    base_url: str = "https://api.hamsterkombat.io/auth"


class MeRequest(AuthPost):
    path: str = "me-telegram"
    log_message: str = "Get user information"


class SyncRequest(Post):
    path: str = "sync"
    log_message: str = "Synchronizing"


class TapRequest(Post):
    path: str = "tap"
    timestamp: int = Field(default_factory=lambda: int(time()))
    total: int
    count: int

    def get_log_message(self):
        return f"Tap {self.count} times"

    def payload(self):
        return {
            "availableTaps": self.total,
            "timestamp": self.timestamp,
            "count": self.count,
        }


class HasBoostRequest(Post):
    path: str = "boosts-for-buy"
    log_message: str = "Check available boost"


class BuyBoostRequest(Post):
    path: str = "buy-boost"
    timestamp: int = Field(default_factory=lambda: int(time()))
    log_message: str = "Buy boost"

    def payload(self):
        return {
            "boostId": "BoostFullAvailableTaps",
            "timestamp": self.timestamp,
        }


class GetUpgradesRequest(Post):
    path: str = "upgrades-for-buy"
    log_message: str = "Get upgrades list"


class GetTasksRequest(Post):
    path: str = "list-tasks"
    log_message: str = "Get tasks"


class GetConfigRequest(Post):
    path: str = "config"
    log_message: str = "Get config"


class DoTaskRequest(Post):
    path: str = "check-task"
    id: str
    log_message: str = "Do task"

    def payload(self):
        return {"taskId": self.id}


class BuyUpgradeRequest(Post):
    path: str = "buy-upgrade"
    timestamp: int = Field(default_factory=lambda: int(time()))
    upgrade: dict

    def get_log_message(self):
        u = self.upgrade
        price = utils.readable(u['price'])
        cph = utils.readable(u['currentProfitPerHour'])
        ung_info = f"{u['name']} {u['level']} lvl"
        upg_price = f"{price} coins (+ {cph}/h)"
        return f"Buy {ung_info} for {upg_price}"

    def payload(self):
        return {
            "upgradeId": self.upgrade["id"],
            "timestamp": self.timestamp,
        }


class DailyCipherRequest(Post):
    path: str = "claim-daily-cipher"
    phrase: str

    def get_log_message(self):
        return f"Enter Morse passphrase: {self.phrase}"

    def payload(self):
        return {"cipher": self.phrase.upper()}


class DailyComboRequest(Post):
    path: str = "claim-daily-combo"
    log_message: str = "Do combo"


class AuthRequest(AuthPost):
    path: str = "auth-by-telegram-webapp"
    data: str
    log_message: str = "Authenticate..."

    def payload(self):
        return {"initDataRaw": self.data}


__all__ = [
    "MeRequest",
    "AuthRequest",
    "SyncRequest",
    "TapRequest",
    "HasBoostRequest",
    "BuyBoostRequest",
    "GetUpgradesRequest",
    "BuyUpgradeRequest",
    "DailyCipherRequest",
    "GetTasksRequest",
    "DoTaskRequest",
    "GetConfigRequest",
    "DailyComboRequest",
]

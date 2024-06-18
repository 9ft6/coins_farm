from time import time

from pydantic import Field

from core.requests import PostRequest


class Post(PostRequest):
    base_url: str = "https://api.hamsterkombat.io/clicker"


class AuthPost(PostRequest):
    base_url: str = "https://api.hamsterkombat.io/auth"


class MeRequest(AuthPost):
    path: str = "me-telegram"


class SyncRequest(Post):
    path: str = "sync"


class TapRequest(Post):
    path: str = "tap"
    timestamp: int = Field(default_factory=lambda: int(time()))
    total: int
    count: int

    def payload(self):
        return {
            "availableTaps": self.total,
            "timestamp": self.timestamp,
            "count": self.count,
        }


class HasBoostRequest(Post):
    path: str = "boosts-for-buy"


class BuyBoostRequest(Post):
    path: str = "buy-boost"
    timestamp: int = Field(default_factory=lambda: int(time()))

    def payload(self):
        return {
            "boostId": "BoostFullAvailableTaps",
            "timestamp": self.timestamp,
        }


class GetUpgradesRequest(Post):
    path: str = "upgrades-for-buy"


class GetTasksRequest(Post):
    path: str = "list-tasks"


class GetConfigRequest(Post):
    path: str = "config"


class DoTaskRequest(Post):
    path: str = "check-task"
    id: str

    def payload(self):
        return {"taskId": self.id}



class BuyUpgradeRequest(Post):
    path: str = "buy-upgrade"
    timestamp: int = Field(default_factory=lambda: int(time()))
    id: str

    def payload(self):
        return {
            "upgradeId": self.id,
            "timestamp": self.timestamp,
        }


class DailyCipherRequest(Post):
    path: str = "claim-daily-cipher"
    phrase: str

    def payload(self):
        return {"cipher": self.phrase.upper()}


class DailyComboRequest(Post):
    path: str = "claim-daily-combo"


class AuthRequest(AuthPost):
    path: str = "auth-by-telegram-webapp"
    data: str

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

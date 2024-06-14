from time import time

from pydantic import Field

from core.requests import PostRequest, GetRequest


class MeRequest(PostRequest):
    base_url: str = "https://api.hamsterkombat.io/auth"
    path: str = "me-telegram"


class SyncRequest(PostRequest):
    path: str = "sync"


class TapRequest(PostRequest):
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


class HasBoostRequest(PostRequest):
    path: str = "boosts-for-buy"


class BuyBoostRequest(PostRequest):
    path: str = "buy-boost"
    timestamp: int = Field(default_factory=lambda: int(time()))

    def payload(self):
        return {
            "boostId": "BoostFullAvailableTaps",
            "timestamp": self.timestamp,
        }


class GetUpgradesRequest(PostRequest):
    path: str = "upgrades-for-buy"


class GetTasksRequest(PostRequest):
    path: str = "list-tasks"


class GetConfigRequest(PostRequest):
    path: str = "config"


class DoTaskRequest(PostRequest):
    path: str = "check-task"
    id: str

    def payload(self):
        return {"taskId": self.id}



class BuyUpgradeRequest(PostRequest):
    path: str = "buy-upgrade"
    timestamp: int = Field(default_factory=lambda: int(time()))
    id: str

    def payload(self):
        return {
            "upgradeId": self.id,
            "timestamp": self.timestamp,
        }


class DailyCipherRequest(PostRequest):
    path: str = "claim-daily-cipher"
    phrase: str

    def payload(self):
        return {"cipher": self.phrase.upper()}


__all__ = [
    "MeRequest",
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
]

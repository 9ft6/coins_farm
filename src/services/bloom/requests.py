from time import time

from pydantic import Field

from core.requests import PostRequest, Request, GetRequest


class GateWay:
    base_url: str = "https://gateway.blum.codes/v1"


class GameDomain:
    base_url: str = "https://game-domain.blum.codes/api/v1"


class MeRequest(GetRequest, GateWay):
    path: str = "user/me"


class BalanceRequest(GetRequest, GameDomain):
    path: str = "user/balance"


class CheckDailyRequest(PostRequest, GameDomain):
    path: str = "daily-reward?offset=-420"


class StartFarmingRequest(PostRequest, GameDomain):
    path: str = "farming/start"


class ClaimFarmingRequest(PostRequest, GameDomain):
    path: str = "farming/claim"


class CheckFriendRequest(PostRequest, GameDomain):
    path: str = "friends/balance"


class ClaimFriendRequest(PostRequest, GameDomain):
    path: str = "friends/claim"


class PlayGameRequest(PostRequest, GameDomain):
    path: str = "game/play"


class ClaimGameRequest(PostRequest, GameDomain):
    path: str = "game/claim"
    id: str
    points: int = 2000

    def payload(self):
        return {
            "gameId": self.id,
            "points": self.points,
        }


class AuthRequest(PostRequest, GateWay):
    path: str = "auth/provider/PROVIDER_TELEGRAM_MINI_APP"
    query: str

    def payload(self):
        return {
            "query": self.query
        }

__all__ = [
    "MeRequest",
    "BalanceRequest",
    "CheckDailyRequest",
    "StartFarmingRequest",
    "ClaimFarmingRequest",
    "CheckFriendRequest",
    "ClaimFriendRequest",
    "PlayGameRequest",
    "ClaimGameRequest",
    "AuthRequest",
]

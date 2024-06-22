from time import time

from pydantic import Field

from core.requests import PostRequest, Request, GetRequest


class GateWay:
    base_url: str = "https://gateway.blum.codes/v1"


class GameDomain:
    base_url: str = "https://game-domain.blum.codes/api/v1"


class MeRequest(GetRequest, GateWay):
    log_message: str = "Getting user info"
    path: str = "user/me"


class BalanceRequest(GetRequest, GameDomain):
    log_message: str = "Getting balance"
    path: str = "user/balance"


class CheckDailyRequest(PostRequest, GameDomain):
    log_message: str = "Checking daily"
    path: str = "daily-reward?offset=-420"


class StartFarmingRequest(PostRequest, GameDomain):
    log_message: str = "Start Farming"
    path: str = "farming/start"


class ClaimFarmingRequest(PostRequest, GameDomain):
    log_message: str = "Claim farming"
    path: str = "farming/claim"


class CheckFriendRequest(PostRequest, GameDomain):
    log_message: str = "Checking friend"
    path: str = "friends/balance"


class ClaimFriendRequest(PostRequest, GameDomain):
    log_message: str = "Claim friend"
    path: str = "friends/claim"


class PlayGameRequest(PostRequest, GameDomain):
    log_message: str = "Playing game"
    path: str = "game/play"


class ClaimGameRequest(PostRequest, GameDomain):
    log_message: str = "Claiming game"
    path: str = "game/claim"
    id: str
    points: int = 2000

    def payload(self):
        return {
            "gameId": self.id,
            "points": self.points,
        }


class AuthRequest(PostRequest, GateWay):
    log_message: str = "Authenticate..."
    path: str = "auth/provider/PROVIDER_TELEGRAM_MINI_APP"
    query: str

    def payload(self):
        return {"query": self.query}


class RefreshAuthRequest(PostRequest, GateWay):
    log_message: str = "Refreshing token..."
    path: str = "auth/refresh"
    token: str

    def payload(self):
        return {"refresh": self.token}


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
    "RefreshAuthRequest",
]

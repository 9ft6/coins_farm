from core.api import BaseAPI
from services.bloom.requests import *
from services.bloom.logger import logger, CustomLogger


class BloomAPI(BaseAPI):
    logger: CustomLogger = logger

    async def me(self):
        return await self.fetch(MeRequest)

    async def balance(self):
        return await self.fetch(BalanceRequest)

    async def check_daily(self):
        return await self.fetch(CheckDailyRequest)

    async def claim_farming(self):
        return await self.fetch(ClaimFarmingRequest)

    async def start_farming(self):
        return await self.fetch(StartFarmingRequest)

    async def check_friend(self):
        return await self.fetch(CheckFriendRequest)

    async def claim_friend(self):
        return await self.fetch(ClaimFriendRequest)

    async def play_game(self):
        return await self.fetch(PlayGameRequest)

    async def claim_game(self, game_id: str, points: int):
        return await self.fetch(ClaimGameRequest, id=game_id, points=points)

    async def auth(self, query: str):
        return await self.fetch(AuthRequest, query=query)

    async def refresh_auth(self, token: str):
        return await self.fetch(RefreshAuthRequest, token=token)

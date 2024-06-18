from core.api import BaseAPI
from core.models import *
from services.bloom.requests import *
from services.bloom.logger import logger, CustomLogger


class BloomAPI(BaseAPI):
    logger: CustomLogger = logger

    async def me(self):
        self.debug("Getting user info")
        response = await MeRequest(self).do()
        if response.success:
            return Ok(data=response.data)
        else:
            return Error(error=f"Bad status: {response.status}")

    async def balance(self):
        self.debug("Getting balance")
        response = await BalanceRequest(self).do()
        if response.success:
            return Ok(data=response.data)
        else:
            return Error(error=f"Bad status: {response.status}")

    async def check_daily(self):
        self.debug("Checking daily")
        response = await CheckDailyRequest(self).do()
        if response.success:
            return Ok(data=response.data)
        else:
            return Error(error=f"Bad status: {response.status}")

    async def claim_farming(self):
        self.debug("Claim farming")
        response = await ClaimFarmingRequest(self).do()
        if response.success:
            return Ok(data=response.data)
        else:
            return Error(error=f"Bad status: {response.status}")

    async def start_farming(self):
        self.debug("Start Farming")
        response = await StartFarmingRequest(self).do()
        if response.success:
            return Ok(data=response.data)
        else:
            return Error(error=f"Bad status: {response.status}")

    async def check_friend(self):
        self.debug("Checking friend")
        response = await CheckFriendRequest(self).do()
        if response.success:
            return Ok(data=response.data)
        else:
            return Error(error=f"Bad status: {response.status}")

    async def claim_friend(self):
        self.debug("Claim friend")
        response = await ClaimFriendRequest(self).do()
        if response.success:
            return Ok(data=response.data)
        else:
            return Error(error=f"Bad status: {response.status}")

    async def play_game(self):
        self.debug("Playing game")
        response = await PlayGameRequest(self).do()
        if response.success:
            return Ok(data=response.data)
        else:
            return Error(error=f"Bad status: {response.status}")

    async def claim_game(self, game_id: str, points: int):
        self.debug(f"Claiming game {game_id=}")
        response = await ClaimGameRequest(self, id=game_id, points=points).do()
        if response.success:
            return Ok(data=response.data)
        else:
            return Error(error=f"Bad status: {response.status}")

    async def auth(self, query: str):
        self.debug(f"Authenticate...")
        response = await AuthRequest(self, query=query).do()
        if response.success:
            return Ok(data=response.data)
        else:
            return Error(error=f"Bad status: {response.status}")


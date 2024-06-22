from core.models import *
from core.api import BaseAPI
from runners.hamster_kombat.requests import *
from runners.hamster_kombat.logger import logger, CustomLogger


class HamsterAPI(BaseAPI):
    logger: CustomLogger = logger

    async def synchronize(self) -> Result:
        return await self.fetch(SyncRequest)

    async def me(self) -> Result:
        result = await self.fetch(MeRequest)
        result.data = result.data["telegramUser"]
        return result

    async def tap(self, count: int, available: int) -> Result:
        return await self.fetch(TapRequest, count=count, total=available)

    async def get_upgrades(self) -> Result:
        return await self.fetch(GetUpgradesRequest)

    async def buy_upgrade(self, u: dict) -> Result:
        return await self.fetch(BuyUpgradeRequest, upgrade=u)

    async def claim_cipher(self, phrase: str) -> Result:
        return await self.fetch(DailyCipherRequest, phrase=phrase)

    async def has_boost(self) -> Result:
        result = await self.fetch(HasBoostRequest)
        if result.success:
            data = {x["id"]: x for x in result.data["boostsForBuy"]}
            if boosts := data.get("BoostFullAvailableTaps"):
                not_max_level = boosts["level"] < boosts["maxLevel"]
                if not_max_level and boosts["cooldownSeconds"] == 0:
                    return Ok(data=boosts)

        return result

    async def buy_boost(self) -> Result:
        return await self.fetch(BuyBoostRequest)

    async def get_config(self) -> Result:
        return await self.fetch(GetConfigRequest)

    async def get_tasks(self) -> Result:
        return await self.fetch(GetTasksRequest)

    async def do_task(self, task: dict) -> Result:
        return await self.fetch(DoTaskRequest, id=task["id"])

    async def do_combo(self) -> Result:
        return await self.fetch(DailyComboRequest)

    async def auth(self, data: str):
        return await self.fetch(AuthRequest, data=data)

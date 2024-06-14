from core.models import *
from core.api import BaseAPI
from core import utils
from services.hamster_kombat.requests import *
from services.hamster_kombat.logger import logger, CustomLogger


class HamsterAPI(BaseAPI):
    logger: CustomLogger = logger

    async def synchronize(self) -> Result:
        self.debug("Synchronizing")
        response = await SyncRequest(self).do()
        if response.success:
            return Ok(data=response.data)
        else:
            return Error(error=f"Bad status: {response.status}")

    async def me(self) -> Result:
        self.info("Get user information")
        response = await MeRequest(self).do()
        if response.success:
            return Ok(data=response.data["telegramUser"])
        else:
            return Error(error=f"Bad status: {response.status}")

    async def tap(self, count: int, available: int) -> Result:
        self.info(f"Tap {count} times")
        response = await TapRequest(self, count=count, total=available).do()
        if response.success:
            self.client.state.stat_taps(count)
            return Ok(data=response.data)
        else:
            return Error(error=f"Bad status: {response.status}")

    async def get_upgrades(self) -> Result:
        self.debug(f"Get upgrades list")
        response = await GetUpgradesRequest(self).do()
        if response.success:
            return Ok(data=response.data)
        else:
            return Error(error=f"Bad status: {response.status}")

    async def buy_upgrade(self, u: dict) -> Result:
        price = utils.readable(u['price'])
        cph = utils.readable(u['currentProfitPerHour'])
        ung_info = f"{u['name']} {u['level']} lvl"
        upg_price = f"{price} coins (+ {cph}/h)"
        self.info(f"Buy {ung_info} for {upg_price}")
        response = await BuyUpgradeRequest(self, id=u["id"]).do()
        if response.success:
            self.client.state.stat_upgrades()
            self.client.state.stat_upgrades_price(u["price"])
            self.client.state.stat_coins_per_hour(u["profitPerHourDelta"])
            return Ok(data=response.data)
        else:
            return Error(error=f"Bad status: {response}")

    async def claim_cipher(self, phrase: str) -> Result:
        self.info(f"Enter Morse passphrase: {phrase}")
        response = await DailyCipherRequest(self, phrase=phrase).do()
        if response.success:
            return Ok(data=response.data)
        else:
            return Error(error=f"Bad status: {response.status}")

    async def has_boost(self) -> Result:
        self.info(f"Check available boost")
        response = await HasBoostRequest(self).do()
        if response.success:
            data = {x["id"]: x for x in response.data["boostsForBuy"]}
            if boosts := data.get("BoostFullAvailableTaps"):
                self.debug(f"boost: {boosts}")
                not_max_level = boosts["level"] < boosts["maxLevel"]
                if not_max_level and boosts["cooldownSeconds"] == 0:
                    return Ok(data=boosts)

        return Error(error="Cannot get boost with level")

    async def buy_boost(self) -> Result:
        self.info("Buy boost")
        response = await BuyBoostRequest(self).do()
        if response.success:
            return Ok(data=response.data)
        else:
            return Error(error="Cannot get boost with level")

    async def get_config(self) -> Result:
        self.info("Get config")
        response = await GetConfigRequest(self).do()
        if response.success:
            return Ok(data=response.data)
        else:
            return Error(error="Cannot get config")

    async def get_tasks(self) -> Result:
        self.info("Get tasks")
        response = await GetTasksRequest(self).do()
        if response.success:
            return Ok(data=response.data)
        else:
            return Error(error="Cannot get tasks")

    async def do_task(self, task: dict) -> Result:
        self.info("Do task")
        response = await DoTaskRequest(self, id=task["id"]).do()
        if response.success:
            return Ok(data=response.data)
        else:
            return Error(error=f"Cannot do task: {task}")

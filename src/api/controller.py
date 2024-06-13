import aiohttp

import utils
from logger import LoggerMixin
from api.requests import *
from api.models import *


class APIController(LoggerMixin):
    session: aiohttp.ClientSession

    def __init__(self, session, client):
        self.session = session
        self.client = client

    def log_id(self):
        return self.client.id

    async def synchronize(self) -> Result:
        self.debug("Synchronizing")
        request = SyncRequest(self)
        if (response := await request.do()) and response.status < 300:
            return Ok(data=response.data)
        else:
            return Error(error=f"Bad status: {response.status}")

    async def me(self) -> Result:
        self.info("Get user information")
        request = MeRequest(self)
        if (response := await request.do()) and response.status < 300:
            return Ok(data=response.data["telegramUser"])
        else:
            return Error(error=f"Bad status: {response.status}")

    async def tap(self, count: int, available: int) -> Result:
        self.info(f"Tap {count} times")
        request = TapRequest(self, count=count, total=available)
        if (response := await request.do()) and response.status < 300:
            self.client.state.stat_taps(count)
            return Ok(data=response.data)
        else:
            return Error(error=f"Bad status: {response.status}")

    async def get_upgrades(self) -> Result:
        self.debug(f"Get upgrades list")
        request = GetUpgradesRequest(self)
        if (response := await request.do()) and response.status < 300:
            return Ok(data=response.data)
        else:
            return Error(error=f"Bad status: {response.status}")

    async def buy_upgrade(self, u: dict) -> Result:
        price = utils.readable(u['price'])
        cph = utils.readable(u['currentProfitPerHour'])
        ung_info = f"{u['name']} {u['level']} lvl"
        upg_price = f"{price} coins (+ {cph}/h)"
        self.info(f"Buy {ung_info} for {upg_price}")
        request = BuyUpgradeRequest(self, id=u["id"])

        if (response := await request.do()) and response.status < 300:
            self.client.state.stat_upgrades()
            self.client.state.stat_upgrades_price(u["price"])
            self.client.state.stat_coins_per_hour(u["profitPerHourDelta"])
            return Ok(data=response.data)
        else:
            return Error(error=f"Bad status: {response}")

    async def claim_cipher(self, phrase: str) -> Result:
        self.info(f"Enter Morse passphrase: {phrase}")
        request = DailyCipherRequest(self, phrase=phrase)
        if (response := await request.do()) and response.status < 300:
            return Ok(data=response.data)
        else:
            return Error(error=f"Bad status: {response.status}")

    async def has_boost(self) -> Result:
        self.info(f"Check available boost")
        request = HasBoostRequest(self)
        if (response := await request.do()) and response.status < 300:
            data = {x["id"]: x for x in response.data["boostsForBuy"]}
            if boosts := data.get("BoostFullAvailableTaps"):
                self.debug(f"boost: {boosts}")
                not_max_level = boosts["level"] < boosts["maxLevel"]
                if not_max_level and boosts["cooldownSeconds"] == 0:
                    return Ok(data=boosts)

        return Error(error="Cannot get boost with level")

    async def buy_boost(self) -> Result:
        self.info("Buy boost")
        request = BuyBoostRequest(self)
        if (response := await request.do()) and response.status < 300:
            return Ok(data=response.data)
        else:
            return Error(error="Cannot get boost with level")

    async def get_tasks(self) -> Result:
        self.info("Get tasks")
        request = GetTasksRequest(self)
        if (response := await request.do()) and response.status < 300:
            return Ok(data=response.data)
        else:
            return Error(error="Cannot get tasks")

    async def do_task(self, task: dict) -> Result:
        self.info("Do task")
        request = DoTaskRequest(self, id=task["id"])
        if (response := await request.do()) and response.status < 300:
            return Ok(data=response.data)
        else:
            return Error(error=f"Cannot do task: {task}")

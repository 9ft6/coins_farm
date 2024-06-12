import aiohttp

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
        response = await SyncRequest(self).do()
        if response.status < 300:
            return Ok(data=response.data)
        else:
            return Error(error=f"Bad status: {response.status}")

    async def me(self) -> Result:
        self.info("Get user information")
        response = await MeRequest(self).do()
        if response.status < 300:
            return Ok(data=response.data["telegramUser"])
        else:
            return Error(error=f"Bad status: {response.status}")

    async def tap(self, count: int, available: int) -> Result:
        self.info(f"Tap {count} times")
        request = TapRequest(self, count=count, total=available)
        response = await request.do()
        if response.status < 300:
            self.client.state.stat_taps(count)
            return Ok(data=response.data)
        else:
            return Error(error=f"Bad status: {response.status}")

    async def get_upgrades(self) -> Result:
        self.debug(f"Get upgrades list")
        request = GetUpgradesRequest(self)
        response = await request.do()
        if response.status < 300:
            return Ok(data=response.data)
        else:
            return Error(error=f"Bad status: {response.status}")

    async def buy_upgrade(self, upgrade: dict) -> Result:
        self.info(f"Buy {upgrade['id']}")
        print(upgrade)
        request = BuyUpgradeRequest(self, id=upgrade["id"])

        if (response := await request.do()) and response.status < 300:
            self.client.state.stat_upgrades()
            self.client.state.stat_upgrades_price(upgrade["price"])
            self.client.state.stat_coins_per_hour(upgrade["profitPerHourDelta"])
            return Ok(data=response.data)
        else:
            return Error(error=f"Bad status: {response}")

    async def claim_cipher(self, phrase: str) -> Result:
        self.info(f"Enter Morse passphrase: {phrase}")
        request = DailyCipherRequest(self, phrase=phrase)
        response = await request.do()
        if response.status < 300:
            return Ok(data=response.data)
        else:
            return Error(error=f"Bad status: {response.status}")

    async def has_boost(self):
        self.info(f"Check available boost")
        request = HasBoostRequest(self)
        response = await request.do()
        if response.status < 300:
            data = {x["id"]: x for x in response.data["boostsForBuy"]}
            if boosts := data.get("BoostFullAvailableTaps"):
                self.debug(f"boost: {boosts}")
                not_max_level = boosts["level"] < boosts["maxLevel"]
                if not_max_level and boosts["cooldownSeconds"] == 0:
                    return Ok(data=boosts)

        return Error(error="Cannot get boost with level")

    async def buy_boost(self):
        self.info("Buy boost")
        request = BuyBoostRequest(self)
        response = await request.do()
        if response.status < 300:
            return Ok(data=response.data)
        else:
            return Error(error="Cannot get boost with level")

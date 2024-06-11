import asyncio
import random

import aiohttp

from config import Headers, cfg
from state import State
from api import APIController


class HamsterClient:
    id: int
    headers: Headers
    state: State
    api: APIController

    def __init__(self, id: int, headers: Headers):
        self.id = id
        self.headers = headers
        self.state = State()

    def __str__(self):
        balance = int(self.state.balance())
        taps = self.state.taps_count()
        name = self.state.username()
        cph = self.state.coins_per_hour()
        return (f"{self.id:0>2} - {name:^15} {taps:<11}"
                f" coins: {balance:<12} {cph}/h")

    async def run_pipeline(self):
        async with aiohttp.ClientSession() as session:
            self.api = APIController(session, self)

            self.state.set_user((await self.api.me()).data)
            await asyncio.sleep(random.randint(1, 100) / 100)
            self.state.update(await self.api.synchronize())

            if cfg.passphrase:
                await self.api.claim_cipher(cfg.passphrase)
                # self.api.info(f"Passphrase result: {result}")

            while True:
                if taps_count := self.state.need_to_taps():
                    await self.do_taps(taps_count)

                if cfg.upgrade_enable:
                    await self.upgrade()

                to_sleep = random.randint(*cfg.sleep_time)
                self.state.update(await self.api.synchronize())

                self.api.info(f"Going sleep {to_sleep} secs")
                await asyncio.sleep(to_sleep)

    async def do_taps(self, taps: int = 1, only_update: bool = False):
        result = await self.api.tap(taps, taps)
        if result.success:
            self.state.update(result)
            if only_update:
                return

            if (await self.api.has_boost()).success:
                result = await self.api.buy_boost()
                if result.success:
                    self.state.update(result)
                    if taps_count := self.state.need_to_taps():
                        result = await self.api.tap(taps_count, taps_count)
                        if result.success:
                            self.state.update(result)

    async def upgrade(self):
        result = await self.api.get_upgrades()
        if result.success:
            filtered = filter(
                lambda x: (
                    x["isAvailable"]
                    and x["profitPerHour"]
                    and not x["isExpired"]
                    and not x.get("cooldownSeconds", 0)
                    and x["price"] < 1_000_000
                ),
                result.data["upgradesForBuy"],
            )
            upgrades = []
            for upgrade in filtered:
                upgrade["ppp"] = upgrade["price"] / upgrade["profitPerHourDelta"]
                upgrades.append(upgrade)

            balance = self.state.balance()
            total = 0
            money = 0
            upgrades = sorted(upgrades, key=lambda x: x["ppp"], reverse=True)
            for upgrade in list(upgrades)[-4:]:
                if upgrade["price"] <= balance:
                    total += upgrade["profitPerHourDelta"]
                    money += upgrade["price"]
                    balance -= upgrade["price"]
                    result = await self.api.buy_upgrade(upgrade["id"])
                    self.state.update(result)
                    await asyncio.sleep(2)

    def client_line(self):
        return self.headers.__hash__()

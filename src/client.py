import asyncio
import json
import random

import aiohttp

import utils
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
        balance_raw = int(self.state.balance())
        taps = self.state.taps_count()
        name = self.state.username()
        cph = utils.readable(self.state.coins_per_hour())
        cph_improved = utils.readable(self.state.stat["coins_per_hour"])
        coins_raw = balance_raw - self.state.start_balance
        coins = utils.readable(coins_raw)
        prefix = '+' if coins_raw > 0 else ""
        coins = f"({prefix} {coins})"
        upg_count = self.state.stat["upgrades"]
        upg_price = utils.readable(self.state.stat["upgrades_price"])
        upgrades = f"{upg_count} pcs. spent {upg_price} coins."
        balance = utils.readable(balance_raw)
        return (f"{self.id:0>2} {name:^15} {taps:<11} balance: {balance:>8} "
                f"{coins:<8} {cph}/h (+ {cph_improved})\n"
                f"Last logs:                       upgrades bought {upgrades}")

    async def run(self):
        async with aiohttp.ClientSession() as session:
            self.api = APIController(session, self)
            await self.synchronize_all()

            while True:
                await self.run_pipeline()

                to_sleep = random.randint(*cfg.sleep_time)
                self.api.debug(f"Going sleep {to_sleep} secs")
                await asyncio.sleep(to_sleep)

    async def synchronize_all(self):
        tg_user = (await self.api.me()).data
        self.state.set_user(tg_user)
        await asyncio.sleep(random.randint(1, 100) / 100)
        sync_response = await self.api.synchronize()
        balance = sync_response.data["clickerUser"]["balanceCoins"]
        self.state.update(sync_response)
        self.state.set_start_balance(balance)

    async def run_pipeline(self):
        if taps_count := self.state.need_to_taps():
            await self.do_taps(taps_count)

        if cfg.do_tasks:
            await self.do_tasks()

        if cfg.upgrade_depends and self.state.need_upgrade_depends:
            await self.upgrade_depends()
            self.state.set_no_upgrades_depends()

        if cfg.upgrade_enable:
            await self.upgrade()

        self.state.update(await self.api.synchronize())

    async def do_tasks(self):
        result = await self.api.get_tasks()
        if result.success:
            for task in result.data.get("tasks", []):
                if task["isCompleted"]:
                    continue

                await self.api.do_task(task)
                await asyncio.sleep(random.randint(1, 5))

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

    async def upgrade_depends(self):
        result = await self.api.get_upgrades()
        if result.success:
            filtered = filter(
                lambda x: (
                    not x["isExpired"]
                    and x.get("condition")
                    and x["condition"]["_type"] == "ByUpgrade"
                ),
                result.data["upgradesForBuy"],
            )
            if available_upgrades := await self.get_available_upgrades():
                depends = {u["id"]: u for u in filtered}
                print(depends)
                upgrades = {u["id"]: u for u in available_upgrades}
                for _id, depend in depends.items():
                    if upgrade := upgrades.get(_id):
                        for _ in range(upgrade["level"], depend["level"] + 1):
                            # await self.buy_upgrade(upgrade)
                            ...

    async def get_available_upgrades(self, max_price=1_000_000):
        result = await self.api.get_upgrades()
        if result.success:
            filtered = filter(
                lambda x: (
                        x["isAvailable"]
                        and x["profitPerHour"]
                        and not x["isExpired"]
                        and not x.get("cooldownSeconds", 0)
                        and max_price == 0 or x["price"] < max_price
                ),
                result.data["upgradesForBuy"],
            )
            upgrades = []
            for u in filtered:
                pph = u.get("profitPerHourDelta")
                u["ppp"] = u["price"] / pph if pph else 0
                upgrades.append(u)

            return upgrades

    async def upgrade(self):
        if upgrades := await self.get_available_upgrades():
            balance = self.state.balance()
            upgrades = sorted(upgrades, key=lambda x: x["ppp"], reverse=True)
            for upgrade in list(upgrades)[-4:]:
                if upgrade["price"] <= balance:
                    await self.buy_upgrade(upgrade)
                    await asyncio.sleep(2)

    async def buy_upgrade(self, upgrade: dict):
        result = await self.api.buy_upgrade(upgrade)
        if result.success:
            self.state.update(result)
        return result.success

    def client_line(self):
        return self.headers.__hash__()

    async def enter_passphrase(self, passphrase: str):
        return await self.api.claim_cipher(passphrase)
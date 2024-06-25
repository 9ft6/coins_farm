import asyncio
import random

from config import cfg
from core import utils
from core.client import BaseClient
from runners.hamster_kombat.api import HamsterAPI
from runners.hamster_kombat.state import HamsterState, HamsterConfig

static = f"{cfg.host_url()}/static"
hamster_guide_en = '''
<b>Step 2: Obtain parameters from the web version</b>

1. Open the web version of Telegram and log in. <a href="https://web.telegram.org/">Go to Telegram Web</a>.
2. Press <b>Ctrl</b> + <b>Shift</b> + <b>I</b> or <b>F12</b> to open the developer console.
3. Find the line starting with <code>query_id=</code> and copy it.
4. Paste the copied line into the field below, and the account will automatically appear in your account list.
'''
hamster_guide = '''
<b>Шаг 2: Получение параметров из веб-версии</b>

1. Откройте веб-версию Telegram и авторизуйтесь. <a href="https://web.telegram.org/">Перейти в веб-версию Telegram</a> и нажмите play  в Hamster Kombat.
2. Нажмите <b>Ctrl</b> + <b>Shift</b> + <b>I</b> или <b>F12</b>, чтобы открыть консоль разработчика.
3. Найдите строку, начинающуюся с <code>query_id=</code>, и скопируйте её.
4. Вставьте скопированную строку в поле ниже, и аккаунт автоматически добавится в список ваших аккаунтов.
'''


class HamsterClient(BaseClient):
    slug: str = "hamster_kombat"
    api: HamsterAPI
    state: HamsterState
    cfg: HamsterConfig

    host: str = "api.hamsterkombat.io"
    referer: str = "https://hamsterkombat.io/"
    origin: str = "https://hamsterkombat.io"

    def __str__(self):
        # TODO: move that shit to state class
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
        upgrades = f"UPG: {upg_count}/{upg_price}$"
        balance = utils.readable(balance_raw)
        morse_flag = utils.enable_emoji(self.state.has_morse())
        combo_flag = utils.enable_emoji(self.state.has_combo())
        task_flag = utils.enable_emoji(self.cfg.auto_task)
        depends_flag = utils.enable_emoji(self.cfg.auto_depends)
        upgrades_flag = utils.enable_emoji(self.cfg.auto_upgrade)
        is_selected = ">>" if self.num == self.panel.cursor else "  "
        return (
            f"{is_selected}{self.num:0>2} {name:<19} {balance:>8}$ {coins:<8}"
            f" + {cph}/h (+ {cph_improved}) {taps:<11} {upgrades}\n"
            f"  {self.state.user_level() or '':O>2} lvl          "
            f"          {combo_flag} combo {morse_flag} morse {task_flag} "
            f"tasks {upgrades_flag} upgrades: {depends_flag} depends"
        )

    def get_stat(self):
        # TODO: and that shit too
        level = f"{self.state.user_level() or '':O>2} lvl"
        balance_raw = int(self.state.balance())
        balance = utils.readable(balance_raw)
        coins_raw = balance_raw - self.state.start_balance
        coins = utils.readable(coins_raw)
        prefix = '+' if coins_raw > 0 else ""
        coins = f"({prefix} {coins})"
        cph = utils.readable(self.state.coins_per_hour())
        improved = f"(+ {utils.readable(self.state.stat['coins_per_hour'])}"
        taps = self.state.taps_count()
        upg_count = self.state.stat["upgrades"]
        upg_price = utils.readable(self.state.stat["upgrades_price"])
        upgrades = f"UPG: {upg_count}/{upg_price}$"
        morse_flag = utils.enable_emoji(self.state.has_morse())
        combo_flag = utils.enable_emoji(self.state.has_combo())
        task_flag = utils.enable_emoji(self.cfg.auto_task)
        depends_flag = utils.enable_emoji(self.cfg.auto_depends)
        upgrades_flag = utils.enable_emoji(self.cfg.auto_upgrade)
        view = (
            "<code>"
            f"{level} {self.state.username()} {upgrades}\n"
            f"{taps:<11} {balance:>8}$ {coins:<8} + {cph}/h {improved}\n"
            f"{combo_flag} combo {morse_flag} morse {task_flag} "
            f"tasks {upgrades_flag} upgrades: {depends_flag} depends"
            "</code>"
        )
        return view

    @staticmethod
    def get_guide():
        return hamster_guide

    def get_tokens_from_response(self, response):
        return {"access": response.data["authToken"]}

    def api_class(self):
        return HamsterAPI

    def state_class(self):
        return HamsterState

    def cfg_class(self):
        return HamsterConfig

    async def before_run(self):
        await self.synchronize_all()

    async def synchronize_all(self):
        tg_user = (await self.api.me()).data
        self.state.set_user(tg_user)

        upgrades_response = await self.api.get_upgrades()
        self.state.update(upgrades_response)

        sync_response = await self.api.synchronize()
        self.state.update(sync_response)

        self.state.update(await self.api.get_config())

        balance = sync_response.data["clickerUser"]["balanceCoins"]
        self.state.set_start_balance(balance)

    async def run_pipeline(self):
        if taps_count := self.state.need_to_taps():
            await self.do_taps(taps_count)

        if self.cfg.auto_task:
            await self.do_tasks()

        if self.cfg.auto_depends and self.cfg.need_upgrade_depends:
            await self.upgrade_depends()
            self.cfg.need_upgrade_depends = False

        if self.cfg.auto_upgrade:
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
        self.state.stat_taps(taps)
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
        if not result.success:
            return

        available_upgrades = await self.get_available_upgrades()
        if not available_upgrades:
            return

        filtered = filter(
            lambda x: (
                x
                and not x.get("isExpired")
                and x.get("condition")
                and x["condition"]["_type"] == "ByUpgrade"
            ),
            result.data["upgradesForBuy"],
        )
        conditions = [u["condition"] for u in filtered]
        depends = {c["upgradeId"]: c for c in conditions}
        upgrades = {u["id"]: u for u in available_upgrades}

        to_upgrade = {}
        for _id, d in depends.items():
            if u := upgrades.get(_id):
                if (
                    u
                    and u["level"] < d["level"]
                    and u["price"] < 100_000
                    and u["isAvailable"]
                    and not d.get("isExpired")
                ):
                    u["to_level"] = d["level"]
                    to_upgrade[_id] = u

        for _id, u in to_upgrade.items():
            for _ in range(u["level"], u["to_level"] + 1):
                self.api.info(f"Upgrade {_id} {u['level']} -> {u['to_level']}")
                result = await self.buy_upgrade(u)
                if result:
                    u["level"] += 1
                    await asyncio.sleep(0.5)

    async def get_available_upgrades(self, max_price=5_000_000):
        result = await self.api.get_upgrades()
        update = {"dailyCombo": result.data.get("dailyCombo")}
        self.state.update(update)

        if result.success:
            filtered = filter(
                lambda x: (
                    x
                    and x["isAvailable"]
                    and x["profitPerHour"]
                    and not x.get("isExpired")
                    and not x.get("cooldownSeconds", 0)
                    and (max_price == 0 or x["price"] < max_price)
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
        for _ in range(4):
            if upgrades := await self.get_available_upgrades():
                balance = self.state.balance()
                upgrades = sorted(upgrades, key=lambda x: x["ppp"], reverse=True)
                upgrade = list(upgrades)[-1]
                if upgrade["price"] <= balance:
                    await self.buy_upgrade(upgrade)
                    await asyncio.sleep(0.1)

    async def enter_combo(self, combo: list[str]):
        upgrades = self.state.get_upgrades_by_ids(combo)
        tasks = [self.buy_upgrade(u) for u in upgrades]
        await asyncio.gather(*tasks)
        await self.api.do_combo()

    async def buy_upgrade(self, upgrade: dict):
        result = await self.api.buy_upgrade(upgrade)
        if result.success:
            self.state.update(result)
            self.state.stat_upgrades()
            self.state.stat_upgrades_price(upgrade["price"])
            self.state.stat_coins_per_hour(upgrade["profitPerHourDelta"])
        return result.success

    async def enter_passphrase(self, passphrase: str):
        if self.state.data.get('dailyCipher', {}).get('isClaimed'):
            self.api.debug("Cipher is already claimed")
            return

        return await self.api.claim_cipher(passphrase)
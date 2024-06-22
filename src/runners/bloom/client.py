import asyncio
from datetime import datetime as dt
import random

from core.client import BaseClient
from runners.bloom.api import BloomAPI
from runners.bloom.state import BloomState, BloomConfig
from runners.bloom.logger import logger, CustomLogger


class BloomClient(BaseClient):
    logger: CustomLogger = logger
    slug: str = "bloom"
    api: BloomAPI
    state: BloomState
    cfg: BloomConfig

    referer: str = "https://telegram.blum.codes"
    origin: str = "https://telegram.blum.codes"

    def __str__(self):
        st = self.state
        stats = st.get_stats()
        name = st.user and st.user.username or ""
        balance = st.balance
        is_selected = ">>" if self.num == self.panel.cursor else "  "
        return (f"{is_selected}{self.num:0>2} {name:<19} {balance:>5}$ "
                f"{st.play_passes=} {stats}")

    def api_class(self):
        return BloomAPI

    def state_class(self):
        return BloomState

    def cfg_class(self):
        return BloomConfig

    async def before_run(self):
        await self.get_user()

    async def get_user(self):
        self.state.set_user((await self.api.me()).data)

    async def update_balance(self):
        data = (await self.api.balance()).data
        self.state.set_balance(data["playPasses"], data["availableBalance"])
        return data

    async def check_daily(self):
        await self.api.balance()

    async def check_friend(self) -> bool:
        if (response := await self.api.check_friend()) and response.success:
            return response.data["canClaim"]

    async def need_to_farm(self) -> bool:
        balance = await self.update_balance()
        if farming_info := balance.get("farming"):
            diff = farming_info['endTime'] / 1000 - dt.utcnow().timestamp()
            return diff < 0

    async def claim_game(self, game_id: str) -> bool:
        points = random.randint(1400, 2000)
        response = await self.api.claim_game(game_id, points)
        return response.data["message"] == "game session not finished"

    async def run_pipeline(self):
        await self.check_daily()

        if await self.need_to_farm():
            await self.api.claim_farming()
            await self.api.start_farming()

        # if await self.check_friend():
        #     await self.api.claim_friend()

        while self.state.has_pass():
            response = await self.api.play_game()
            game_id = response.data.get("gameId")
            await asyncio.sleep(random.randint(5, 12) / 10)

            while self.claim_game(game_id):
                await asyncio.sleep(random.randint(10, 20) / 10)

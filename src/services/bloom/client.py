import asyncio
from datetime import datetime as dt, timezone
import random

from core.client import BaseClient
from services.bloom.api import BloomAPI
from services.bloom.state import BloomState, BloomConfig


class BloomClient(BaseClient):
    slug: str = "bloom"
    api: BloomAPI
    state: BloomState
    cfg: BloomConfig

    referer: str = "https://telegram.blum.codes"
    origin: str = "https://telegram.blum.codes"

    def __str__(self):
        return f"{self.token}"

    def api_class(self):
        return BloomAPI

    def state_class(self):
        return BloomState

    def cfg_class(self):
        return BloomConfig

    async def before_run(self):
        await self.get_user()
        await self.update_balance()

    async def get_user(self):
        self.state.set_user((await self.api.me()).data)

    async def update_balance(self):
        data = (await self.api.balance()).data
        self.state.set_balance(data["playPasses"], data["availableBalance"])
        return data

    async def check_daily(self):
        await self.api.balance()

    async def check_friend(self) -> bool:
        return (await self.api.check_friend()).data["canClaim"]

    async def need_to_farm(self) -> bool:
        balance = await self.update_balance()
        if farming_info := balance.get("farming"):
            end_time_s = farming_info['endTime'] / 1000.0
            diff = dt.fromtimestamp(end_time_s, timezone.utc) - dt.utcnow()
            return diff.total_seconds() // 3600 < 0

    async def claim_game(self, game_id: str) -> bool:
        response = await self.api.claim_game(game_id, 2000)
        return response.data["message"] == "game session not finished"

    async def run_pipeline(self):
        await self.check_daily()

        if await self.need_to_farm():
            await self.api.claim_farming()
            await self.api.start_farming()

        if await self.check_friend():
            await self.api.claim_friend()

        while self.state.has_pass():
            game_id = (await self.api.play_game()).data.get()
            await asyncio.sleep(random.randint(5, 12) / 10)

            while self.claim_game(game_id):
                await asyncio.sleep(random.randint(10, 20) / 10)

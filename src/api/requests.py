from typing import Any
from http import HTTPMethod

from time import time
import aiohttp
import asyncio
from pydantic import BaseModel, Field


class Response(BaseModel):
    data: Any = None
    status: int
    error: str = None


class BaseRequest(BaseModel):
    url: str | None = None
    base_url: str = "https://api.hamsterkombat.io/clicker"
    path: str
    method: HTTPMethod
    data: str | None = None
    api: Any | None = None

    def __init__(self, api, **kwargs) -> None:
        super().__init__(**kwargs)
        self.api = api
        self.url = f"{self.base_url}/{self.path}"

    async def do(self):
        return await self._make_request()

    async def _make_request(self, attempts=1, **kwargs):
        while attempts:
            pd = self.payload()
            try:
                async with self.api.session.request(
                    self.method,
                    self.url,
                    headers=self.api.client.headers,
                    json=pd,
                    **kwargs
                ) as response:
                    if response.status >= 300:
                        print(f"{self.url}: got a {response.status} "
                              f"response code {await response.read()}")
                        attempts -= 1
                        return await self._make_request(
                            attempts=attempts, **kwargs
                        )
                    try:
                        result = await response.json()
                    except Exception as e:
                        # print(f"Can not decode body JSON: {e}")
                        result = await response.read()

                    # print(f"{self.url}: RESPONSE BODY: {result}")
                    return Response(status=response.status, data=result)
                    # return result, response.status
            except aiohttp.InvalidURL as error:
                print(f"{self.url}: Invalid url: {error}")
                return None
            except aiohttp.ClientPayloadError as error:
                print(f"{self.url}: Malformed payload: {error}")
                return None
            except (
                aiohttp.ClientConnectorError,
                aiohttp.ClientOSError,
                aiohttp.ClientResponseError,
                aiohttp.ServerDisconnectedError,
                asyncio.TimeoutError,
                ValueError,
            ) as error:
                attempts -= 1
                print(f"{self.url}: Got an error {error} during GET request")
                if not attempts:
                    break

                return await self._make_request(attempts=attempts, **kwargs)

        print(f"{self.url}: Exceeded the number of attempts "
              f"to perform {self.method} request")
        return None

    def payload(self):
        ...


class GetRequest(BaseRequest):
    method: HTTPMethod = HTTPMethod.GET


class PostRequest(BaseRequest):
    method: HTTPMethod = HTTPMethod.POST


class MeRequest(PostRequest):
    base_url: str = "https://api.hamsterkombat.io/auth"
    path: str = "me-telegram"


class SyncRequest(PostRequest):
    path: str = "sync"


class TapRequest(PostRequest):
    path: str = "tap"
    timestamp: int = Field(default_factory=lambda: int(time()))
    total: int
    count: int

    def payload(self):
        return {
            "availableTaps": self.total,
            "timestamp": self.timestamp,
            "count": self.count,
        }


class HasBoostRequest(PostRequest):
    path: str = "boosts-for-buy"


class BuyBoostRequest(PostRequest):
    path: str = "buy-boost"
    timestamp: int = Field(default_factory=lambda: int(time()))

    def payload(self):
        return {
            "boostId": "BoostFullAvailableTaps",
            "timestamp": self.timestamp,
        }


class GetUpgradesRequest(PostRequest):
    path: str = "upgrades-for-buy"


class BuyUpgradeRequest(PostRequest):
    path: str = "buy-upgrade"
    timestamp: int = Field(default_factory=lambda: int(time()))
    id: str

    def payload(self):
        return {
            "upgradeId": self.id,
            "timestamp": self.timestamp,
        }

class DailyCipherRequest(PostRequest):
    path: str = "claim-daily-cipher"
    phrase: str

    def payload(self):
        # Should by string word in upper case like {"cipher":"WEB3"}
        return {"cipher": self.phrase.upper()}


__all__ = [
    "BaseRequest",
    "GetRequest",
    "PostRequest",
    "MeRequest",
    "SyncRequest",
    "TapRequest",
    "HasBoostRequest",
    "BuyBoostRequest",
    "GetUpgradesRequest",
    "BuyUpgradeRequest",
    "DailyCipherRequest",
]

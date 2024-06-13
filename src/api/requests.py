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
    success: bool = False


class ErrorResponse(Response):
    def __init__(self, response, error):
        super().__init__(error=error, status=response.status)


class SuccessResponse(Response):
    success: bool = True

    def __init__(self, response, data):
        super().__init__(status=response.status, data=data)


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
        if response := await self._make_request():
            return response
        else:
            return

    def get_kwargs(self):
        return {
            "method": self.method,
            "url": self.url,
            "headers": self.api.client.headers,
            "json": self.payload(),
        }

    async def _make_request(self):
        try:
            async with (self.api.session.request(**self.get_kwargs()) as resp):
                try:
                    body = await resp.json()
                except:
                    body = await resp.read()

                if resp.status >= 300:
                    return self._error(resp, f"got {resp.status} code: {body}")

                return self._success(resp, body)
        except aiohttp.InvalidURL:
            return self._error(resp, f"Invalid url: {self.url}")
        except aiohttp.ClientPayloadError:
            return self._error(resp, f"Malformed payload")
        except (
            aiohttp.ClientConnectorError,
            aiohttp.ClientOSError,
            aiohttp.ClientResponseError,
            aiohttp.ServerDisconnectedError,
            asyncio.TimeoutError,
            ValueError,
        ) as error:

            return self._error(resp, f"Got an error {error}")

    def _success(self, resp, data):
        return SuccessResponse(resp, data)

    def _error(self, resp, error):
        self.api.error(error)
        return ErrorResponse(resp, error)

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


class GetTasksRequest(PostRequest):
    path: str = "list-tasks"


class DoTaskRequest(PostRequest):
    path: str = "check-task"
    id: str

    def payload(self):
        return {"taskId": self.id}



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
    "GetTasksRequest",
    "DoTaskRequest",
]

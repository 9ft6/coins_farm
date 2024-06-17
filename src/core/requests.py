from typing import Any
from http import HTTPMethod

import aiohttp
import asyncio
from pydantic import BaseModel


class Headers(dict):
    _token: str = None

    def __hash__(self):
        return hash(self._token)


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


class Request(BaseModel):
    url: str | None = None
    base_url: str
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
            print(self.get_kwargs())
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


class GetRequest(Request):
    method: HTTPMethod = HTTPMethod.GET


class PostRequest(Request):
    method: HTTPMethod = HTTPMethod.POST


__all__ = [
    "Response",
    "ErrorResponse",
    "SuccessResponse",
    "Request",
    "GetRequest",
    "PostRequest",
]

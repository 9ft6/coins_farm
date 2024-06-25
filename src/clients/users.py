from db.models import *
from clients.base import BaseAPIClient
from core.logger import SubLogger


logger = SubLogger("users_api")


class Users(BaseAPIClient):
    logger: SubLogger = logger
    path: str = "/users"

    async def create_user(self, user: dict):
        user = NewTelegramUser(**user).model_dump()
        body, status = await self.post(f"{self.base_url}/", json=user)
        return body

    async def get_user(self, user_id: int):
        body, status = await self.get(f"{self.base_url}/{user_id}")
        if status == 200:
            return TelegramUser(**body)

    async def get_users(self):
        body, status = await self.get(f"{self.base_url}/")
        if status == 200:
            return [TelegramUser(**u) for u in body]

    async def update_user(self, user: dict):
        url = f"{self.base_url}/{user['id']}"
        body, status = await self.put(url, json=user)
        return body

    async def delete_user(self, user_id: int):
        body, status = await self.delete(f"{self.base_url}/{user_id}")
        return body

    async def approve_user(self, user_id: int):
        url = f"{self.base_url}/approve/{user_id}"
        body, status = await self.post(url)
        return body

    async def change_role(self, user_id: int):
        url = f"{self.base_url}/{user_id}/change_role/"
        body, status = await self.post(url)
        return body

    async def ban_unban(self, user_id: int):
        url = f"{self.base_url}/{user_id}/ban_unban/"
        body, status = await self.post(url)
        return body

    async def get_users_to_approve(self):
        body, status = await self.get(f"{self.base_url}/to_approve/")
        if status == 200:
            return [TelegramUser(**u) for u in body]

    async def attach_account(self, slug: str, user_id: int, account_id: int):
        data = {
            "user_id": user_id,
            "account_id": account_id,
        }
        url = f"{self.base_url}/attach_account/{slug}"
        body, status = await self.post(url, json=data)
        return body


users_api = Users()

__all__ = ["users_api"]

from fastapi import HTTPException, Response

from core.logger import SubLogger
from db.models import TelegramUser
from server.api.models import (
    UpdateTelegramUserRequest,
    AttachAccountToUserRequest,
)

logger = SubLogger("UsersAPI")


def register_users_api(app, Server):
    @app.post("/users/")
    async def create_user(user: TelegramUser):
        try:
            new_user = Server.users.create(user.dict())
            return new_user
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @app.get("/users/{user_id}")
    async def read_user(user_id: int):
        if user := Server.users[user_id]:
            return user
        return Response("User not found", 404)

    @app.put("/users/{user_id}")
    async def update_user(user_id: int, request: UpdateTelegramUserRequest):
        user = Server.users.update(user_id, request.model_dump())
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    @app.delete("/users/{user_id}")
    async def delete_user(user_id: int):
        if not Server.users.delete(user_id):
            raise HTTPException(status_code=404, detail="User not found")
        return {"detail": "User deleted"}

    @app.get("/users/to_approve/")
    async def get_users_to_approve():
        return Server.users.get_users_to_approve()

    @app.post("/users/approve/{user_id}")
    async def approve_user(user_id):
        return Server.users.update(user_id, {"status": "approved"})

    @app.post("/users/attach_account/{slug}")
    async def attach_account(slug: str, body: AttachAccountToUserRequest):
        logger.info(f"Attach account {slug} {body}")

        if body.account_id in Server.accounts.items:
            return Server.users.attach_account(slug, **body.model_dump())
        else:
            return {"detail": "account not found"}

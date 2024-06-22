from fastapi import FastAPI, HTTPException, Response

from core.logger import SubLogger
from db.models import TelegramUser, UpdateTelegramUserRequest
from db import Users

users = Users()
app = FastAPI()
logger = SubLogger("UsersAPI")


def register_users_api(app):
    @app.post("/users/")
    async def create_user(user: TelegramUser):
        try:
            new_user = users.create(user.dict())
            return new_user
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @app.get("/users/{user_id}")
    async def read_user(user_id: int):
        if user := users[user_id]:
            return user
        return Response("User not found", 404)

    @app.put("/users/{user_id}")
    async def update_user(user_id: int, request: UpdateTelegramUserRequest):
        user = users.update(user_id, request.model_dump())
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    @app.delete("/users/{user_id}")
    async def delete_user(user_id: int):
        if not users.delete(user_id):
            raise HTTPException(status_code=404, detail="User not found")
        return {"detail": "User deleted"}

    @app.get("/users/to_approve/")
    async def get_users_to_approve():
        return users.get_users_to_approve()

    @app.post("/users/approve/{user_id}")
    async def approve_user(user_id):
        return users.update(user_id, {"status": "approved"})

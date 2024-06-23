import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from config import cfg
from core import utils
from core.logger import SubLogger
from db import accounts

bot_logger = SubLogger("bot")
rn_logger = SubLogger("runner")

valid_slugs = ["bloom", "hamster_kombat"]
clients = {}
stats = {}  # TODO: use redis
app = FastAPI(debug=True)

from server.api.users import register_users_api  # noqa
from server.api.runners import register_runners_api  # noqa


class Server:
    ws: WebSocket = None

    @staticmethod
    @app.on_event("startup")
    async def on_startup():
        await asyncio.gather(accounts.init())

    @staticmethod
    @app.websocket(cfg.ws_bot_prefix)
    async def bot_endpoint(ws: WebSocket):
        await ws.accept()
        bot_logger.info(f"Connecting to Telegram Bot... {ws.scope}")

        try:
            while True:
                if data := await ws.receive_json():
                    if response := await Server.handle_bot_message(data):
                        await ws.send_json(response)

                await asyncio.sleep(1)

        except WebSocketDisconnect:
            bot_logger.error("client disconnected")
        except Exception as e:
            print(e)
            bot_logger.error(e)

    @staticmethod
    async def handle_bot_message(data: dict):
        bot_logger.debug(f"Received message: {data}")

        match data.get("type"):
            case _:
                return {"error": "unknown message type"}

    @staticmethod
    @app.websocket(cfg.ws_runner_prefix)
    async def runner_endpoint(ws: WebSocket):
        await accounts.init()
        rn_logger.info(f"Connecting to Runner... {ws.scope}")

        await ws.accept()
        slug = None
        try:
            # validate client
            if data := await Server.handshake(ws):
                if slug := data.get("slug"):
                    await Server.start_runner(ws, slug)

                    # wait commands
                    while True:
                        data = await ws.receive_json()
                        rn_logger.success(f"Received message: {data}")
                        await asyncio.sleep(1)

        except WebSocketDisconnect:
            rn_logger.error("client disconnected")
        except Exception as e:
            rn_logger.error(e)
        if slug:
            del clients[slug]

    @staticmethod
    async def handshake(ws: WebSocket):
        data = await ws.receive_json()

        if data["slug"] in valid_slugs:
            clients[data["slug"]] = ws
            ws.data = data
            return data
        else:
            await Server.disconnect(ws, "Invalid slug.")

    @staticmethod
    async def start_runner(ws: WebSocket, slug: str):
        clients[slug] = ws
        items = await accounts.get_accounts_by_slug(slug)
        await Server.send(ws, {"items": items, "type": "add_accounts"})

    @staticmethod
    async def send(ws: WebSocket, data: list | dict | BaseModel):
        await ws.send_json(utils.jsonify(data))

    @staticmethod
    async def disconnect(ws: WebSocket, message: str):
        await ws.send_text(f"{message} Disconnecting.")
        await ws.close()

    @staticmethod
    def get_runner(slug: str):
        return clients[slug]

    @staticmethod
    def set_stat(slug: str, account_id: int, stat: dict):
        if slug not in stats:
            stats[slug] = {account_id: stat}
        else:
            stats[slug][account_id] = stat

    @staticmethod
    def get_stat(slug: str):
        return stats.get(slug)


register_users_api(app, Server)
register_runners_api(app, Server)

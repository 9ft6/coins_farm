from config import cfg
from server.app import app
from server.api.accounts import *


def run_server():
    import asyncio
    import uvicorn
    from db import accounts

    asyncio.run(accounts.init())
    uvicorn.run(app, host=cfg.host, port=cfg.port)

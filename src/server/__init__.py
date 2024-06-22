import uvicorn

from config import cfg
from server.app import app


def run_server():
    uvicorn.run(app, host=cfg.host, port=cfg.port)

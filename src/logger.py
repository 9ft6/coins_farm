from datetime import datetime
from time import monotonic

import asyncio

from config import cfg


class CustomLogger:
    clients: list
    log_lines: list[str] = []
    last_logs: dict[int, str] = {}

    async def run(self, clients):
        self.clients = clients

        while True:
            t0 = monotonic()
            self.clear()
            self.show()
            if (to_sleep := cfg.cui_refresh - (monotonic() - t0)) > 0:
                await asyncio.sleep(to_sleep)

    def clear(self):
        print("\033[H\033[J", end="")

    def show(self):
        for client in self.clients:
            message = self.last_logs.get(client.id, '')
            print(f"{client}\nLast message: {message}\n")

        print()

        for line in self.log_lines[-cfg.cui_last_logs:]:
            print(line)

    def log(self, level, id, message):
        if level != "debug":
            self.last_logs[id] = message

        dt = datetime.now().strftime("%d.%m %H:%M:%S")
        self.log_lines.append(f'[{dt}] [{level:^6}] [{id:0>2}] {message}')


logger = CustomLogger()


class LoggerMixin:
    logger: CustomLogger = logger

    def log_id(self):
        return "default"

    def info(self, message):
        self.logger.log("info", self.log_id(), message)

    def debug(self, message):
        self.logger.log("debug", self.log_id(), message)

    def error(self, message):
        self.logger.log("error", self.log_id(), message)

    def warning(self, message):
        self.logger.log("warning", self.log_id(), message)

import os  # noqa
os.environ[
    "LOGURU_FORMAT"
] = "{time:DD.MM.YY HH:mm:s} [<lvl>{level:^10}</lvl>] <lvl>{message}</lvl>"  # noqa
os.environ["LEVEL"] = "DEBUG"  # noqa

import asyncio
from datetime import datetime
from time import monotonic

from colorama import init as init_colorama, Fore, Style
from loguru import logger

from config import cfg


class SubLogger:
    def __init__(self, name: str, logger: logger = logger):
        self.info = lambda x: logger.info(f"[{name:^8}] {x}")
        self.debug = lambda x: logger.debug(f"[{name:^8}] {x}")
        self.warning = lambda x: logger.warning(f"[{name:^8}] {x}")
        self.error = lambda x: logger.error(f"[{name:^8}] {x}")
        self.success = lambda x: logger.success(f"[{name:^8}] {x}")


init_colorama()


def get_color_by_level(level: str):
    return {
        "error": Fore.LIGHTRED_EX,
        "debug": Fore.LIGHTBLUE_EX,
        "warning": Fore.LIGHTYELLOW_EX,
    }.get(level.lower(), Fore.WHITE)


def get_color_by_id(id: int):
    colors = [
        Fore.GREEN, Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.LIGHTWHITE_EX,
        Fore.LIGHTBLACK_EX, Fore.LIGHTRED_EX, Fore.LIGHTMAGENTA_EX,
        Fore.LIGHTCYAN_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTGREEN_EX,
        Fore.RED, Fore.CYAN, Fore.YELLOW, Fore.WHITE, Fore.BLUE,
    ]
    return colors[id % len(colors)]


class CustomLogger:
    log_lines: list[str] = []
    last_logs: dict[int, list[str]] = {}
    last_screen: str = ""
    panel_line: str = ""
    show_main_screen: bool = True
    halt: bool = False

    async def run(self, runner):
        self.runner = runner
        while True:
            t0 = monotonic()

            if self.show_main_screen:
                self.show()

            if (to_sleep := cfg.cui_refresh - (monotonic() - t0)) > 0:
                await asyncio.sleep(to_sleep)

    def set_show_main(self, value: bool):
        self.show_main_screen = value

    def clear(self):
        if cfg.disable_screen_clear:
            return

        print("\033[H\033[J", end="")

    def show(self):
        lines = []
        if self.panel_line:
            lines.append(self.panel_line)

        for client in self.runner:
            if logs := self.get_last_logs(client.num):
                logs = '\n'.join(logs)
                lines.append(self.get_line(client.num, f"{client}\n{logs}\n"))

        lines.append("")
        lines.extend(self.log_lines[-cfg.cui_last_logs:])

        screen = "\n".join(lines)
        if screen != self.last_screen:
            self.last_screen = screen
            self.clear()
            print(screen)

    def log(self, level, id, message):
        if level != "debug":
            self.add_last_log(id, message)

        dt = datetime.now().strftime("%d.%m %H:%M:%S")
        color = get_color_by_level(level)
        line = self.get_line(id, f'[{id:0>2}] [{dt}] {color} '
                                 f'[{level:^8}] {message}')
        self.log_lines.append(line)

    def set_panel_line(self, line):
        self.panel_line = line

    def get_line(self, id, message):
        return f"{get_color_by_id(id)}{message}{Style.RESET_ALL}"

    def add_last_log(self, id, message):
        if id in self.last_logs:
            if len(self.last_logs[id]) > cfg.cui_show_last_msgs:
                self.last_logs[id].pop(0)

            self.last_logs[id].append(message)
        else:
            self.last_logs[id] = [message]

    def get_last_logs(self, id):
        return self.last_logs.get(id, [])


class LoggerMixin:
    logger: CustomLogger

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

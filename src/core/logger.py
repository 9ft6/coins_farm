import asyncio
from datetime import datetime
from time import monotonic

from colorama import init, Fore, Style

from config import cfg

init()


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
    clients: list
    log_lines: list[str] = []
    last_logs: dict[int, list[str]] = {}
    last_screen: str = ""
    panel_line: str = ""
    show_main_screen: bool = True

    async def run(self, clients):
        self.clients = clients

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

        for client in self.clients:
            if logs := self.get_last_logs(client.id):
                logs = '\n'.join(logs)
                lines.append(self.get_line(client.id, f"{client}\n{logs}\n"))

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

import aioconsole
import asyncio
from functools import wraps

from colorama import Fore, Style
from sshkeyboard import listen_keyboard_manual

from config import cfg
from logger import logger


def input_wrapper(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        logger.set_show_main(False)
        logger.clear()

        result = await f(*args, **kwargs)

        logger.set_show_main(True)
        logger.show()
        return result

    return wrapper


class MultiSelect:
    data: dict[str, list[str]]
    table: list[list[str], list[str], list[str]] = []
    select_count: int
    title: str = ""
    abort: bool = False
    x: int = 0
    y: int = 2
    max_x: int = 0
    max_y: int = 0
    selected: set[str] = set()
    fixed_count: bool = True

    def __init__(self, data: dict[str, list[str]], select_count: int):
        self.data = self.normalize_data(data)
        self.select_count = select_count

    @staticmethod
    def normalize_data(data):
        max_len = max(map(len, data.values()))
        result = {}
        for k, v in data.items():
            if len(v) < max_len:
                v = [*list(sorted(v)), *([""] * (max_len - len(v)))]
            result[k] = v

        return result

    def update(self):
        '''
        Updates table data
        :return:
        '''
        self.table.clear()
        headers = list(self.data.keys())
        cols = [self.data[h] for h in headers]
        self.table.extend([headers, [""] * len(headers)])
        [self.table.append([x for x in i]) for i in zip(*cols)]
        self.max_x = max(self.max_x, len(headers))
        self.max_y = max(self.max_y, len(cols[0]))

    def show(self):
        '''
        Shows table data to select
        :return:
        '''
        logger.clear()
        longest = max([len(str(y)) for x in self.table for y in x])
        lines = [self.title]
        temp = []
        for y, line in enumerate(self.table):
            l = []
            for x, value in enumerate(line):
                is_selected = f'{x}x{y}' in self.selected
                is_cursor = (x, y) == (self.x, self.y)
                marker = Fore.GREEN if is_selected else ""
                value = f"{value:^{longest}}"
                l.append(f'{">>" if is_cursor else "  "}'
                         f'{marker}{value}{Style.RESET_ALL}'
                         f'{"<<" if is_cursor else "  "}')
            temp.append(l)

        lines.extend(["  ".join(l) for l in temp])
        lines.append(f"(Arrows) Move (Space) De/Select (Enter) Finish/Cancel")
        print("\n".join(lines))

    async def input(self, text):
        self.title = text
        self.update()

        self.show()

        while not self.abort:
            await asyncio.sleep(1)

        return self.get_selected()

    def get_selected(self):
        result = []
        for s in self.selected:
            x, y = map(int, s.split("x"))
            result.append(self.table[y][x])
        return result

    def on_press(self, key):
        match key:
            case "left":
                if self.x > 0:
                    self.x -= 1
            case "right":
                self.x += 1
            case "up":
                if self.y > 1:
                    self.y -= 1
            case "down":
                self.y += 1
            case "space":
                string = f"{self.x}x{self.y}"
                if string in self.selected:
                    self.selected.remove(string)
                else:
                    if len(self.selected) < self.select_count:
                        self.selected.add(string)
            case "enter":
                is_full = len(self.selected) == self.select_count
                if not self.fixed_count or is_full:
                    self.abort = True
            case _:
                return

        self.x = self.x if self.x < self.max_x else self.max_x
        self.y = self.y if self.y < self.max_y else self.max_y

        self.show()


class ConsoleControlPanel:
    ms: MultiSelect | None = None

    def __init__(self, clients):
        self.clients = clients
        self.update_logger_line()

    async def run(self):
        await listen_keyboard_manual(
            on_release=self.on_press,
            delay_second_char=0.1,
        )

    async def on_press(self, key):
        match key:
            case "f3":
                combo = await self.ask_combo()
                tasks = [c.enter_combo(combo) for c in self.clients]
                await asyncio.gather(*tasks)
            case "f4":
                passphrase = await self.ask_cipher()
                tasks = [c.enter_passphrase(passphrase) for c in self.clients]
                await asyncio.gather(*tasks)
            case "f5":
                await asyncio.gather(*[c.run_pipeline() for c in self.clients])
            case "f6":
                cfg.do_tasks = not cfg.do_tasks
            case "f7":
                cfg.upgrade_enable = not cfg.upgrade_enable
            case "f8":
                cfg.upgrade_depends = not cfg.upgrade_depends
            case "left" | "right" | "up" | "down" | "space" | "enter":
                print(self.ms)
                if self.ms:
                    self.ms.on_press(key)

        if not self.ms:
            self.update_logger_line()
            logger.show()

    @input_wrapper
    async def ask_cipher(self):
        return await aioconsole.ainput("\n    Enter passphrase: ")

    @input_wrapper
    async def ask_combo(self):
        d = self.clients[0].state.data
        if (c := d.get("clickerConfig")) and (upgrades := c.get("upgrades")):
            data = {}
            for upgrade in upgrades:
                if (section := upgrade.get("section")) not in data:
                    data[section] = [upgrade["id"]]
                else:
                    data[section].append(upgrade["id"])

            self.ms = MultiSelect(data=data, select_count=3)
            selected = await self.ms.input("Select 3 to get combo:")
            self.ms = None
            if len(selected) == 3:
                await asyncio.sleep(0)
                return selected

    def update_logger_line(self):
        if cfg.use_emoji:
            state = lambda s: "🟢" if s else "🔴"
        else:
            state = lambda s: "(+)" if s else "(-)"

        logger.set_panel_line(
            f"Control Panel     "
            f"| Combo (F3) "
            f"| PassPhrase (F4) "
            f"| Sync (F5) "
            f"| {state(cfg.do_tasks)} Tasks (F6) "
            f"| {state(cfg.upgrade_enable)} Upgrades (F7) "
            f"| {state(cfg.upgrade_depends)} Depends (F8) |"
        )

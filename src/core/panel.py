import asyncio
from functools import wraps

from colorama import Fore, Style
from sshkeyboard import listen_keyboard_manual

from services.hamster_kombat.logger import logger


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
    fixed_count: bool

    def __init__(
        self,
        data: dict[str, list[str]],
        select_count: int,
        fixed: bool = True
    ):
        self.data = self.normalize_data(data)
        self.fixed_count = fixed
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


class BasePanel:
    cursor: int = -1
    ms: MultiSelect | None = None

    def __init__(self, clients):
        self.clients = clients
        self.update_logger_line()
        [c.set_panel(self) for c in clients]

    async def run(self):
        await listen_keyboard_manual(
            on_release=self.on_press,
            delay_second_char=0.1,
        )

    def move(self, key):
        match key:
            case "up":
                if self.cursor > - 1:
                    self.cursor -= 1
                else:
                    self.cursor = len(self.clients) - 1
            case "down":
                if self.cursor < len(self.clients):
                    self.cursor += 1
                else:
                    self.cursor = - 1

    def map(self, func, *args, **kwargs):
        return [getattr(c, func)(*args, **kwargs) for c in self.clients]

    async def async_map(self, coro, *args, **kwargs):
        tasks = [getattr(c, coro)(*args, **kwargs) for c in self.clients]
        return await asyncio.gather(*tasks)

    def exec(self, func, *args, **kwargs):
        if self.cursor == -1:
            self.map(func, *args, **kwargs)
        else:
            client = self.clients[self.cursor]
            getattr(client, func)(*args, **kwargs)

    async def async_exec(self, coro, *args, **kwargs):
        if self.cursor == -1:
            await self.async_map(coro, *args, **kwargs)
        else:
            client = self.clients[self.cursor]
            await getattr(client, coro)(*args, **kwargs)

    def switch_cfg_to_clients(self, name):
        if self.cursor == -1:
            for client in self.clients:
                value = getattr(client.cfg, name)
                setattr(client.cfg, name, not value)
        else:
            client = self.clients[self.cursor]
            value = getattr(client.cfg, name)
            setattr(client.cfg, name, not value)

    async def on_press(self, key):
        ...

    def update_logger_line(self):
        ...

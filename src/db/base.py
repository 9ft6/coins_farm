import pickle
from pathlib import Path
from typing import Any

import aiofiles

from config import cfg


class BaseDB:
    items: dict[int, Any]
    inited: bool = False
    item_name: str
    default_dir: Path
    pickle_file: Path

    def __init__(self):
        self.items = {}
        self.default_dir: Path = cfg.data_dir / f"{self.item_name}s"
        self.pickle_file: Path = cfg.data_dir / f"{self.item_name}s.pickle"

    def __setitem__(self, key, value):
        self.items[key] = value

    def __getitem__(self, item):
        try:
            return self.items[item]
        except:
            ...

    def __iter__(self):
        return iter(self.items.values())

    def __str__(self):
        return f"Loaded {len(self.items)} {self.item_name}s"

    def __contains__(self, item):
        return item.id in self.items

    async def init(self):
        if not self.inited:
            await self.load_default()
            await self.load()
            self.inited = True

        print(f"Loaded {len(self.items)} {self.item_name}s")

    async def load_default(self):
        for file in self.default_dir.iterdir():
            if file.is_file():
                await self.process_default(file)

    async def process_default(self, file):
        ...

    async def dump(self):
        if not self.pickle_file.parent.exists():
            self.pickle_file.parent.mkdir(parents=True)

        async with aiofiles.open(self.pickle_file, 'wb') as f:
            await f.write(pickle.dumps(self.items))

    async def load(self):
        try:
            async with aiofiles.open(self.pickle_file, 'rb') as f:
                data = await f.read()
                self.items.update(pickle.loads(data))
                return self.items
        except FileNotFoundError:
            print("No accounts file to load.")
        except EOFError:
            print("Accounts file damaged.")

import pickle

import aiofiles

from config import cfg
from db.models import InitData, Account, Tokens


class Accounts:
    items: dict[int, Account]

    def __init__(self):
        self.items = {}

    def __getitem__(self, item):
        return self.items[item]

    def __iter__(self):
        return iter(self.items.values())

    def __str__(self):
        return f"Loaded {len(self.items)} accounts"

    def __contains__(self, item):
        return item.id in self.items

    async def get_accounts_by_slug(self, slug: str) -> list[Account]:
        return [acc for acc in self if slug in acc.init_datas]

    async def init(self):
        await self.load_default()
        await self.load()
        print(f"Loaded {len(self.items)} accounts")

    async def dump(self):
        if not cfg.accounts_file.parent.exists():
            cfg.accounts_file.parent.mkdir(parents=True)

        async with aiofiles.open(cfg.accounts_file, 'wb') as f:
            await f.write(pickle.dumps(self.items))

    async def load(self):
        try:
            async with aiofiles.open(cfg.accounts_file, 'rb') as f:
                data = await f.read()
                self.items = pickle.loads(data)
                return self.items
        except FileNotFoundError:
            print("No accounts file to load.")
        except EOFError:
            print("Accounts file damaged.")

    async def load_default(self):
        for file in cfg.accounts_dir.iterdir():
            if file.is_file():
                for init_data in self._load_tokens(file):
                    data = InitData.from_string(init_data)
                    await self.add_init_data(file.name, data)

    async def add_init_data(self, slug: str, data: InitData):
        if data.user_id not in self.items:
            self.items[data.user_id] = Account.from_init_data(slug, data)
        else:
            self.items[data.user_id].set_init_data(slug, data)

        await self.dump()

    async def add_tokens(self, user_id: int, slug: str, tokens: Tokens):
        if account := self.items.get(user_id):
            account.set_tokens(slug, tokens)
            await self.dump()

    async def remove_game(self, account: Account, game_id: int):
        # TODO: implement
        await self.dump()

    async def remove(self, account: Account):
        # TODO: implement
        await self.dump()

    def _load_tokens(self, file):
        with file.open() as f:
            lines = [l.strip() for l in f.readlines() if l.strip()]
            return [t for t in lines if t.startswith("query_id=")]

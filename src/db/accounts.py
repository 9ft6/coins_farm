from db.base import BaseDB
from db.models import InitData, Account, Tokens


class Accounts(BaseDB):
    items: dict[int, Account]
    item_name: str = "account"

    async def process_default(self, file):
        for init_data in self._load_tokens(file):
            data = InitData.from_string(init_data)
            await self.add_init_data(file.name, data)

    async def get_accounts_by_slug(self, slug: str) -> list[Account]:
        return [acc for acc in self if slug in acc.init_datas]

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

    def _load_tokens(self, file):
        with file.open() as f:
            lines = [l.strip() for l in f.readlines() if l.strip()]
            return [t for t in lines if t.startswith("query_id=")]

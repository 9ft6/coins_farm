from pathlib import Path

from tinydb import TinyDB, Query
from typing import Any, Dict, List, Optional

from config import cfg
from db.models import *


UserQuery = Query()


class Users:
    db: TinyDB

    item_name: str = "user"
    default_dir: Path
    db_file: Path

    def __init__(self):
        self.default_dir: Path = cfg.data_dir / f"{self.item_name}s"
        self.db = TinyDB(cfg.data_dir / f"{self.item_name}s.db")
        self.items: Dict[int, TelegramUser] = {}
        self.load_default()
        self.load()

    def load_default(self):
        for file in self.default_dir.iterdir():
            if file.is_file():
                self.process_default(file)

    def process_default(self, file):
        user_role = file.name[:-1]
        if user_role in roles:
            for user_id in self._load_users(file):
                user_id = int(user_id) if isinstance(user_id, str) else user_id
                if user_id in self.items:
                    continue

                user = DefaultUser(id=user_id, role=user_role)
                self.items[user_id] = user

    def _load_users(self, file):
        with file.open() as f:
            lines = [l.strip() for l in f.readlines() if l.strip()]
            return [t for t in lines if not t.startswith("#")]

    def load(self):
        records = self.db.all()
        for record in records:
            user = TelegramUser(**record)
            self.items[int(user.id)] = user

    def dump(self):
        self.db.truncate()
        self.db.insert_multiple([u.model_dump() for u in self.items.values()])

    def __setitem__(self, key: int, value: TelegramUser):
        self.items[key] = value
        self.dump()

    def __getitem__(self, key: int) -> Optional[TelegramUser]:
        return self.items.get(int(key))

    def __contains__(self, key: int) -> bool:
        return key in self.items

    def create(self, user_data: Dict[str, Any]) -> TelegramUser:
        user = self.items.get(user_data["id"])
        if user:
            user.status = "wait_approve"
        else:
            user = TelegramUser(**user_data)
            self.items[user.id] = user

        self.dump()
        return user

    def update(self, user_id: int, user_data: Dict[str, Any]) -> TelegramUser:
        if user := self[user_id]:
            for key, value in user_data.items():
                setattr(user, key, value)
            self.items[user_id] = user
            self.dump()
            return user

    def approve_user(self, user_id: int) -> bool:
        return self.set_user_status(user_id, "approved")

    def set_user_status(self, user_id: int, status: str) -> bool:
        if (user := self[user_id]) and status in statuses:
            user.status = status
            self.dump()
            return True
        return False

    def get_users_to_approve(self) -> List[TelegramUser]:
        return [user for user in self.items.values()
                if user.status == "wait_approve"]

    def attach_account(self, slug: str, user_id: int, account_id: int):
        if user := self.items.get(user_id):
            if slug in user.added_accounts:
                user.added_accounts[slug].append(account_id)
            else:
                user.added_accounts[slug] = [account_id]
            self.dump()
            return "Ok"

        return "User not found"


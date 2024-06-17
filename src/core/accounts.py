from config import cfg


class Accounts:
    items: dict[str, list[str]] = {}

    def __init__(self):
        self.load()

    def __iter__(self):
        return iter(self.items.values())

    def __getitem__(self, item):
        return self.items.get(item)

    def __str__(self):
        return f"Loaded {len(self.items)} accounts"

    def load(self):
        for file in cfg.tokens_dir.iterdir():
            if file.is_file():
                if tokens := self._load_tokens(file):
                    self.items[file.name] = tokens

    def _load_tokens(self, file):
        with file.open() as f:
            lines = [l.strip() for l in f.readlines() if l.strip()]
            return [t for t in lines if not t.startswith("#")]


accounts = Accounts()

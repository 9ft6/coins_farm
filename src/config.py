from pathlib import Path
from pydantic_settings import BaseSettings


class MainConfig(BaseSettings):
    class Config:
        env_file = "../env/.env"
        env_file_encoding = 'utf-8'

    tokens_dir: Path = Path("../tokens")
    accounts_file: Path = Path("../data/accounts.pickle")

    # CUI
    cui_last_logs: int = 30  # last logs line count in terminal
    cui_refresh: int = 2  # secs
    use_emoji: bool = True

    # Client
    sleep_time: tuple[int, int] = (100, 200)
    cui_show_last_msgs: int = 5

    # Server
    host: str = "127.0.0.1"
    port: int = 8000

    def host_url(self):
        return f"http://{self.host}:{self.port}"


cfg = MainConfig()

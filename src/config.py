from pathlib import Path
from pydantic_settings import BaseSettings


class MainConfig(BaseSettings):
    class Config:
        env_file = "../env/.env"
        env_file_encoding = 'utf-8'

    data_dir: Path = Path("../data")

    # CUI
    disable_screen_clear: bool = False  # debug option
    cui_last_logs: int = 10  # last logs line count in terminal
    cui_refresh: int = 2  # secs
    cui_show_last_msgs: int = 2
    use_emoji: bool = True

    # Bot
    bot_token: str = None

    # Runner
    sleep_time: tuple[int, int] = (100, 200)

    # Server
    host: str = "127.0.0.1"
    port: int = 8000
    ws_runner_prefix: str = "/ws/runner"
    ws_bot_prefix: str = "/ws/bot"

    def ws_runner_url(self):
        return f"http://{self.host}:{self.port}{self.ws_runner_prefix}"

    def ws_bot_url(self):
        return f"http://{cfg.host}:{cfg.port}{cfg.ws_bot_prefix}"

    def host_url(self):
        return f"http://{self.host}:{self.port}"


cfg = MainConfig()

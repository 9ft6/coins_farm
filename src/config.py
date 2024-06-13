from pathlib import Path
from pydantic_settings import BaseSettings
from fake_useragent import UserAgent


class Headers(dict):
    _token: str = None

    def __init__(self, *args, **kwargs):
        self._token = kwargs.get("Authorization").replace("Bearer ", "")
        super().__init__(*args, **kwargs)

    def __hash__(self):
        return hash(self._token)


class MainConfig(BaseSettings):
    class Config:
        env_file = "../env/.env"
        env_file_encoding = 'utf-8'

    # Hamster Kombat
    upgrade_enable: bool = False
    upgrade_depends: bool = False
    do_tasks: bool = False

    # CUI
    cui_last_logs: int = 30  # last logs line count in terminal
    cui_refresh: int = 2  # secs
    use_emoji: bool = True

    # Client
    sleep_time: tuple[int, int] = (100, 200)
    cui_show_last_msgs: int = 5
    # cycle_timeout: int = 10  # secs

    # common
    tokens_file: Path = Path("../data/tokens")
    headers: dict[int, Headers] | None = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.headers = {n: h for n, h in enumerate(self._generate_headers())}
        if not self.headers:
            print(f"Put headers to data/sessions. check readme")

    def _generate_headers(self) -> set[Headers]:
        '''
        reads tokens file and parses it into a set of unique Headers
        :return:
        '''
        result = set()
        if self.tokens_file.exists():
            with self.tokens_file.open() as f:
                lines = [l.strip() for l in f.readlines() if l.strip()]
                tokens = [t for t in lines if not t.startswith("#")]
                for token in tokens:
                    result.add(Headers(**{
                        "Accept": "*/*",
                        "Accept-Encoding": "gzip, deflate, br, zstd",
                        "Accept-Language": "en-US,en;q=0.9",
                        "Authorization": f"Bearer {token}",
                        "Connection": "keep-alive",
                        "Host": "api.hamsterkombat.io",
                        "Origin": "https://hamsterkombat.io",
                        "Referer": "https://hamsterkombat.io/",
                        "Sec-Fetch-Dest": "empty",
                        "Sec-Fetch-Mode": "cors",
                        "Sec-Fetch-Site": "same-site",
                        "User-Agent": UserAgent().random,
                    }))
        else:
            print("No tokens file found")

        return result


cfg = MainConfig()

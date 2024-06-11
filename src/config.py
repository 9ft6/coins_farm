from pathlib import Path
from pydantic_settings import BaseSettings


class Headers(dict):
    _token: str = None

    def __init__(self, *args, **kwargs):
        self._token = kwargs.get("Authorization").replace("Bearer ", "")
        super().__init__(*args, **kwargs)

    def __hash__(self):
        return hash(self._token)


class MainConfig(BaseSettings):
    headers_file: Path = Path("../data/sessions")
    headers: dict[int, Headers] | None = None
    upgrade_enable: bool = True
    cui_last_logs: int = 30  # last logs line count in terminal
    cui_refresh: int = 2  # secs
    sleep_time: tuple[int, int] = (100, 200)
    passphrase: str = ""
    cui_show_last_msgs: int = 5
    # cycle_timeout: int = 10  # secs

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.headers = {n: h for n, h in enumerate(self._parse_headers())}

    def _parse_headers(self) -> set[Headers]:
        '''
        reads sessions file and parses it into a set of unique Headers
        :return:
        '''
        result = set()
        if self.headers_file.exists():
            with self.headers_file.open() as f:
                chunks = [x.strip() for x in f.read().split("\n\n")]
                chunks = [x.split("\n") for x in chunks if x]
                chunks = [[self._validate_line(y) for y in x] for x in chunks]
                chunks = [[y.split(": ") for y in x if y] for x in chunks]

                allowed = {
                    "Accept",
                    "Accept-Encoding",
                    "Accept-Language",
                    "Authorization",
                    "Connection",
                    # "Content-Length",
                    "Content-Type",
                    "Host",
                    "Origin",
                    "Referer",
                    "Sec-Fetch-Dest",
                    "Sec-Fetch-Mode",
                    "Sec-Fetch-Site",
                    "User-Agent",
                }
                for raw_headers in chunks:
                    headers = {k: v for k, v in raw_headers if k in allowed}
                    result.add(Headers(**headers))

        return result

    def _validate_line(self, l: str):
        l = l.strip()
        conditions = (
            l,
            not l.startswith("#"),
            not l.startswith("POST"),
            not l.startswith("GET"),
        )
        if all(conditions):
            return l


cfg = MainConfig()

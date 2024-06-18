import os  # noqa
os.environ[  # noqa
    "LOGURU_FORMAT"
] = "{time:DD.MM.YY HH:mm:s} [<lvl>{level:^10}</lvl>] <lvl>{message}</lvl>"
os.environ["LEVEL"] = "DEBUG"  # noqa

from loguru import logger  # noqa

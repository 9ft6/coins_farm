from core.runner import Runner
from services.hamster_kombat.client import HamsterClient, BaseClient
from services.hamster_kombat.logger import logger, CustomLogger
from services.hamster_kombat.panel import ConsoleControlPanel, BasePanel


class Hamster(Runner):
    client: BaseClient = HamsterClient
    logger: CustomLogger = logger
    panel: BasePanel = ConsoleControlPanel

from core.runner import Runner
from runners.hamster_kombat.client import HamsterClient, BaseClient
from runners.hamster_kombat.logger import logger, CustomLogger
from runners.hamster_kombat.panel import ConsoleControlPanel, BasePanel


class Hamster(Runner):
    client: BaseClient = HamsterClient
    logger: CustomLogger = logger
    panel_class: BasePanel = ConsoleControlPanel

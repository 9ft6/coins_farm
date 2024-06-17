from core.runner import Runner
from services.bloom.client import BloomClient, BaseClient
from services.bloom.logger import logger, CustomLogger
from services.bloom.panel import ConsoleControlPanel, BasePanel


class Bloom(Runner):
    client: BaseClient = BloomClient
    logger: CustomLogger = logger
    panel: BasePanel = ConsoleControlPanel

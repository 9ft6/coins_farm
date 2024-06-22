from core.runner import Runner
from runners.bloom.client import BloomClient, BaseClient
from runners.bloom.logger import logger, CustomLogger
from runners.bloom.panel import ConsoleControlPanel, BasePanel


class Bloom(Runner):
    client: BaseClient = BloomClient
    logger: CustomLogger = logger
    panel_class: BasePanel = ConsoleControlPanel

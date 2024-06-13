import asyncio

from sshkeyboard import listen_keyboard_manual

from config import cfg
from logger import logger


class ConsoleControlPanel:
    def __init__(self, clients):
        self.clients = clients
        self.update_logger_line()

    async def run(self):
        await listen_keyboard_manual(on_release=self.on_press)

    async def on_press(self, key):
        match key:
            case "f3":
                print('EnterCombo')
            case "f4":
                # To prevent the screen from updating while entering
                # data from the keyboard, we handle this through a
                # logger class that controls stdin and stdout.
                passphrase = await logger.input('Enter passphrase:')
                tasks = [c.enter_passphrase(passphrase) for c in self.clients]
                await asyncio.gather(*tasks)
            case "f5":
                await asyncio.gather(*[c.run_pipeline() for c in self.clients])
            case "f6":
                cfg.do_tasks = not cfg.do_tasks
            case "f7":
                cfg.upgrade_enable = not cfg.upgrade_enable
            case "f8":
                cfg.upgrade_depends = not cfg.upgrade_depends

        self.update_logger_line()
        logger.show()

    def update_logger_line(self):
        if cfg.use_emoji:
            state = lambda s: "🟢" if s else "🔴"
        else:
            state = lambda s: "(+)" if s else "(-)"

        logger.set_panel_line(
            f"Control Panel     "
            f"| Combo (F3) "
            f"| PassPhrase (F4) "
            f"| Sync (F5) "
            f"| {state(cfg.do_tasks)} Tasks (F6) "
            f"| {state(cfg.upgrade_enable)} Upgrades (F7) "
            f"| {state(cfg.upgrade_depends)} Depends (F8) |"
        )

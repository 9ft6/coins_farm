from sshkeyboard import listen_keyboard_manual

from config import cfg


class ConsoleControlPanel:
    def __init__(self, logger):
        self.logger = logger
        self.update_logger_line()

    async def run(self):
        await listen_keyboard_manual(on_release=self.on_press)

    @staticmethod
    def on_press(key):
        match key:
            case "f3":
                print('EnterCombo')
            case "f4":
                print('PassPhrase')
            case "f5":
                print('Sync')
            case "f6":
                print('Tasks')
            case "f7":
                print('Upgrades')
            case "f8":
                print('Depends')

    def update_logger_line(self):
        state = lambda s: "(+)" if s else "(-)"
        self.logger.set_panel_line(
            f"Control Panel     "
            f"|    Combo (F3)   "
            f"| PassPhrase (F4) "
            f"|    Sync (F5)    "
            f"| {state(cfg.upgrade_enable)} Tasks (F6)    "
            f"| {state(cfg.upgrade_enable)} Upgrades (F7) "
            f"| {state(cfg.upgrade_depends)} Depends (F8) "
        )

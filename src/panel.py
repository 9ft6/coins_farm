import platform

from sshkeyboard import listen_keyboard_manual

from config import cfg


class ConsoleControlPanel:
    def __init__(self, logger):
        self.logger = logger
        self.update_logger_line()

    async def run(self):
        await listen_keyboard_manual(on_release=lambda k: self.on_press(k))

    def on_press(self, key):
        match key:
            case "f3":
                print('EnterCombo')
            case "f4":
                print('PassPhrase')
            case "f5":
                print('Sync')
            case "f6":
                cfg.do_tasks = not cfg.do_tasks
            case "f7":
                cfg.upgrade_enable = not cfg.upgrade_enable
            case "f8":
                cfg.upgrade_depends = not cfg.upgrade_depends

        self.update_logger_line()
        self.logger.show()

    def update_logger_line(self):
        if any(platform.win32_ver()):
            state = lambda s: "(+)" if s else "(-)"
        else:
            state = lambda s: "🟢" if s else "🔴"

        self.logger.set_panel_line(
            f"Control Panel     "
            f"| Combo (F3) "
            f"| PassPhrase (F4) "
            f"| Sync (F5) "
            f"| {state(cfg.do_tasks)} Tasks (F6) "
            f"| {state(cfg.upgrade_enable)} Upgrades (F7) "
            f"| {state(cfg.upgrade_depends)} Depends (F8) |"
        )

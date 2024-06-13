import asyncio

try:
    from pynput import keyboard
except:
    keyboard = None

from config import cfg


class ConsoleControlPanel:
    def __init__(self, logger):
        self.logger = logger

    async def run(self):
        self.update_logger_line()
        keyboard.Listener(on_press=self.on_press).start()
        await asyncio.sleep(0.01)

    @staticmethod
    def on_press(key):
        match key:
            case keyboard.Key.f3:
                print('EnterCombo')
            case keyboard.Key.f4:
                print('PassPhrase')
            case keyboard.Key.f5:
                print('Sync')
            case keyboard.Key.f6:
                print('Tasks')
            case keyboard.Key.f7:
                print('Upgrades')
            case keyboard.Key.f8:
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

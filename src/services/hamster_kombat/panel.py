import aioconsole
import asyncio

from config import cfg
from core.panel import MultiSelect, input_wrapper, BasePanel
from services.hamster_kombat.logger import logger


class ConsoleControlPanel(BasePanel):
    async def on_press(self, key):
        match key:
            case "f3":
                combo = await self.ask_combo()
                tasks = [c.enter_combo(combo) for c in self.clients]
                await asyncio.gather(*tasks)
            case "f4":
                passphrase = await self.ask_cipher()
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
            case "left" | "right" | "up" | "down" | "space" | "enter":
                print(self.ms)
                if self.ms:
                    self.ms.on_press(key)

        if not self.ms:
            self.update_logger_line()
            logger.show()

    @input_wrapper
    async def ask_cipher(self):
        return await aioconsole.ainput("\n    Enter passphrase: ")

    @input_wrapper
    async def ask_combo(self):
        d = self.clients[0].state.data
        if (c := d.get("clickerConfig")) and (upgrades := c.get("upgrades")):
            data = {}
            for upgrade in upgrades:
                if (section := upgrade.get("section")) not in data:
                    data[section] = [upgrade["id"]]
                else:
                    data[section].append(upgrade["id"])

            self.ms = MultiSelect(data=data, select_count=3)
            selected = await self.ms.input("Select 3 to get combo:")
            self.ms = None
            if len(selected) == 3:
                await asyncio.sleep(0)
                return selected

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

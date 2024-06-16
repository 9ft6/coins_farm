import aioconsole
import asyncio

from config import cfg
from core import utils
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
                self.switch_cfg_to_clients("auto_task")
            case "f7":
                self.switch_cfg_to_clients("auto_upgrade")
            case "f8":
                self.switch_cfg_to_clients("auto_depends")
            case "left" | "right" | "up" | "down" | "space" | "enter":
                print(self.ms)
                if self.ms:
                    self.ms.on_press(key)

        if not self.ms:
            self.update_logger_line()
            logger.show()

    def switch_cfg_to_clients(self, name):
        for client in self.clients:
            value = getattr(client.cfg, name)
            setattr(client.cfg, name, not value)

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

            self.ms = MultiSelect(data=data, select_count=3, fixed=False)
            selected = await self.ms.input("Select 3 to get combo:")
            self.ms = None
            if len(selected) == 3:
                await asyncio.sleep(0)
            return selected

    def update_logger_line(self):
        logger.set_panel_line(
            f"Control Panel     "
            f"| Combo (F3) "
            f"| PassPhrase (F4) "
            f"| Sync (F5) "
            f"| Tasks (F6) "
            f"| Upgrades (F7) "
            f"| Depends (F8) |"
        )

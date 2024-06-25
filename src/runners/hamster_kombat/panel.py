import aioconsole
import asyncio

from core.panel import MultiSelect, input_wrapper, BasePanel
from runners.hamster_kombat.logger import logger


class ConsoleControlPanel(BasePanel):
    async def on_press(self, key):
        match key:
            case "f3":
                combo = await self.ask_combo()
                await self.async_exec("enter_combo", combo)
            case "f4":
                passphrase = await self.ask_cipher()
                await self.async_exec("enter_passphrase", passphrase)
            case "f5":
                await self.async_exec("run_pipeline")
            case "f6":
                self.switch_cfg_to_clients("auto_task")
            case "f7":
                self.switch_cfg_to_clients("auto_upgrade")
            case "f8":
                self.switch_cfg_to_clients("auto_depends")
            case "left" | "right" | "up" | "down" | "space" | "enter":
                if self.ms:
                    self.ms.on_press(key)
                else:
                    self.move(key)

        if not self.ms:
            self.update_logger_line()
            logger.show()

    @input_wrapper
    async def ask_cipher(self):
        return await aioconsole.ainput("\n    Enter passphrase: ")

    @input_wrapper
    async def ask_combo(self):
        any_client = self.runner.clients[list(self.runner.clients.keys())[0]]
        d = any_client.state.data
        print(d.keys())
        print("clickerConfig upgrades")
        if (c := d.get("clickerConfig")) and (upgrades := c.get("upgradesForBuy")):
            data = {}
            for upgrade in upgrades:
                if (section := upgrade.get("section")) not in data:
                    data[section] = [upgrade["id"]]
                else:
                    data[section].append(upgrade["id"])

            self.ms = MultiSelect(data=data, select_count=3, fixed=False)
            selected = await self.ms.input("Select 3 to get combo:")
            self.ms = None

            return selected

        await asyncio.sleep(0)

    def update_logger_line(self):
        selected = "all" if self.cursor == -1 else f" {self.cursor:0>2}"
        logger.set_panel_line(
            f"Selected: {selected}      "
            f"| Upgrade (F3) "
            f"| PassPhrase (F4) "
            f"| Sync (F5) "
            f"| AutoTasks (F6) "
            f"| AutoUpgrades (F7) "
            f"| AutoDepends (F8) |"
        )

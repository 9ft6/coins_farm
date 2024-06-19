<p align="center">
  <img src="https://github.com/9ft6/hamster_farm/raw/media/pics/cui.png" alt="User Interface">
</p>

<p align="center">
  <img src="https://github.com/9ft6/hamster_farm/raw/media/pics/combo.png" alt="User Interface">
</p>

# HAMSTER KOMBAT

This module is a bot system for automatically claiming shitcoins.
For it to work correctly, the account server must be running.
You can start it by executing `make run-server` (see details on the main page).

## Bot Pipeline

- The bot runs every 2-4 minutes.
- Synchronizes its state.
- If energy is full, it will tap completely.
- If there is an opportunity to buy a boost, it will purchase it and tap.
- If `autodepends` mode is enabled, it will buy dependencies to facilitate card leveling.
- If `autoupgrade` mode is enabled, it will purchase the top profitable card four times in a row.
- If `autotask` mode is enabled, it will attempt to complete all available tasks.
- Then it will go to sleep.

The main purpose of auto mode is to tap automatically with a boost, which works well with `autoupgrade`.

## Console User Interface

In the console, while on the main screen, you can use the up and down keys to select a specific account. Additionally, using the F3-F8 keys, you can start and toggle modes on or off. After activating a mode, press F5 to start the pipeline immediately with new parameters.

- **F3**: Upgrade.
- **F4**: Enter a `PassPhrase`
- **F5**: `Synchronize` and run pipelines.
- **F6**: Toggle `task` execution on and off.
- **F7**: Enable or disable `upgrades`.
- **F8**: Toggle `dependency` upgrades.

Pressing F3 allows you to select (with the space bar) several upgrades and build them by pressing Enter, which enables you to create combos. If no account is selected at the moment, upgrades will be applied to all accounts.

Pressing F4 allows you to enter a Morse phrase. Note that the phrase is not displayed. Simply enter it and press Enter. The phrase will be applied to the selected account. If no account is selected at the moment, it will be applied to all accounts.

## Adding Accounts

1. Open telegram desktop. Go to Settings - Advanced - Experimental settings - Enable webview inspecting
2. Log in to [Telegram Web](https://web.telegram.org/).
3. Press **Shift + Ctrl + I** or **F12** to open the developer console.
4. Select `Session Storage` on the left.
5. Copy the value of `__telegram__initParams`, a string starting with `query_id=`.
6. Paste it into a file in the `accounts/hamster_kombat` directory, with one account per line.

<p align="center">
  <img src="https://github.com/9ft6/hamster_farm/raw/media/pics/hamster_debugger.png" alt="User Interface">
</p>

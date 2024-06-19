# BLOOM

> **Note:** This module is currently under development and is expected to be ready by June 20th. As a result, some information or screenshots may be missing from the documentation. Please stay tuned for updates.


This module is a bot system for automatically claiming shitcoins.
For it to work correctly, the account server must be running.
You can start it by executing `make run-server` (see details on the main page).

## Bot Pipeline
- The bot checks and completes daily tasks.
- Checks and farms if possible.
- Checks and collects friends.
- Plays the game as long as there are game passes available.

## Console User Interface
Under construction

## Adding Accounts

1. Install the "Ignore X-Frame Headers" extension:
   - [Chrome, Opera](https://chrome.google.com/webstore/detail/gleekbfjekiniecknbkamfmkohkpodhe)
   - [Firefox](https://addons.mozilla.org/firefox/addon/ignore-x-frame-options-header/)
2. Open telegram desktop. Go to Settings - Advanced - Experimental settings - Enable webview inspecting
3. Log in to [Telegram Web](https://web.telegram.org/).
4. Press **Shift + Ctrl + I** or **F12** to open the developer console.
5. Select `Session Storage` on the left.
6. Copy the value of `__telegram__initParams`, a string starting with `query_id=`.
7. Paste it into a file in the `accounts/bloom` directory, with one account per line.

<p align="center">
  <img src="https://github.com/9ft6/hamster_farm/raw/media/pics/bloom_debugger.png" alt="debugger">
</p>

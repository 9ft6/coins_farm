
<p align="center">
  <img src="https://github.com/9ft6/hamster_farm/raw/media/pics/cui.png" alt="User Interface">
</p>

**Done:**
- Console interface
- Boost purchase
- Task completion
- Dependency upgrade
- Card mining
- Console control panel
- Console passphrase entering

**Soon:**
- Combo purchases
- Telegram control bot
- Account management
- Status monitoring

---

Due to the popularity of such apps, this project might evolve into a comprehensive platform for farming various games in one place.

---
If you have any questions, feel free to message me on Telegram.

## Overview
This application (bot) is designed to automatically manage multiple Telegram accounts for playing the popular game Hamster Kombat (https://hamsterkombat.io). To generate hourly income around the clock, the game requires user participation every three hours, which is impossible and turns a proud primate into a slave to a rodent. Justice will be restored by the unyielding silicon hand of justice, embodied in my bot.

One of its key strengths is its ability to handle nearly all the necessary manipulations for successful farming. The bot efficiently manages multiple accounts, regardless of whether it's 1, 5, or 100, using asynchronous aiohttp requests.

Here’s how the bot operates: 
- If the power is fully charged, the bot clicks to activate it. 
- Next, it checks if a boost is available for purchase; if so, it buys the boost and clicks again. 
- The bot then completes tasks from the "Earn" section, upgrades all dependencies.
- After that, it identifies the most profitable cards in the "Mining" section, buying 5-6 of them. 
- Finally, it goes into sleep mode for a random period of 2-5 minutes.

Here's the translation into English with Markdown formatting:

---

## Account Management

In the console, the top line is occupied by the control panel, which can be used to manage the configuration.

*Below is a list of commands with a brief description:*

- **F3**: Enter `Combo`. !coming-soon!

- **F4**: Enter a `PassPhrase` to all accounts.

- **F5**: `Synchronize` and run pipelines for all clients.

- **F6**: Toggle `task` execution on and off.*

- **F7**: Enable or disable `upgrades`.*

- **F8**: Toggle `dependency` upgrades.*

* Need restart or wait client waking up.
---

If you need any further modifications or have specific requirements, please let me know!

## Prerequisites
Before you begin, ensure you have met the following requirements:
- Python 3.11 or higher
- Git (optional, for cloning the repository)

## Installation
To set up the project environment and install the necessary dependencies, follow these steps:

1. **Clone the repository (Optional)**:
   If you have git installed, you can clone the repository using:
   ```bash
   git clone https://github.com/9ft6/hamster_farm.git
   cd hamster_farm
   ```
Alternatively, if you have downloaded the project as a zip file, extract it and navigate into the project directory.

2. **Create and activate a virtual environment**: 
   Use make to create a virtual environment and install the required packages:

    ```bash
    make install
    ```
This command sets up a Python virtual environment and installs the dependencies listed in requirements.txt.

# How to Add an Account for Tracking

To add an account for tracking, you need to extract the token from the request headers of the Hamster API. To do this, we will run the game in a browser and use the debugger. To run the game on the computer, we need to replace one file in the game. We will use the method of this guy: [github.com/mudachyo](https://github.com/mudachyo/Hamster-Kombat).. For this, we need the Violentmonkey extension. Below are links to install it for the main browsers:

## Browser Extensions for Debugging:

### Mozilla Firefox:

- **Extension: Violentmonkey**
- **Link:** [Install Violentmonkey for Firefox](https://addons.mozilla.org/en-US/firefox/addon/violentmonkey/)

### Google Chrome:

- **Extension: Violentmonkey**
- **Link:** [Install Violentmonkey for Chrome](https://chrome.google.com/webstore/detail/violentmonkey/jinjaccalgkegednnccohejagnlnfdag)

### Opera:

- **Extension: Violentmonkey**
- **Link:** [Install Violentmonkey for Opera](https://addons.opera.com/en/extensions/details/violentmonkey/)


After installing these extensions, you can start the Game:

1. Go to the link and install the script: [https://github.com/mudachyo/Hamster-Kombat/raw/main/hamster-kombat.user.js](https://github.com/mudachyo/Hamster-Kombat/raw/main/hamster-kombat.user.js).

2. After that, go to [https://web.telegram.org/](https://web.telegram.org/), log in, and start the Hamster Kombat. The game should begin.

3. Press **Shift + Ctrl + I** or **F12** to open the developer console. The screenshot shows where you can find the token you need. It will stop working after a while, and you will need to replace it if the bot stops working.

<p align="center">
  <img src="https://github.com/9ft6/hamster_farm/raw/media/pics/debugger.png" alt="User Interface">
</p>

4. In the root folder of the project, create a folder named `data`.

5. Inside it, create a file named `tokens` (without an extension), and put all the tokens you want to track in it, each on a new line.

6. Then, run the bot.

## Run
To run the farm, use the following command:

```bash
make run
```

This command activates the virtual environment and runs the main.py script located in the src directory.

## TODO
- Telegram bot
- Stat to the bot
- Adding accounts by bot

Done
- Auto tasks
- update accounts management
- Console user interface
- refactor api module 

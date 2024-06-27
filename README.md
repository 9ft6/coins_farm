<p align="center">
  <img src="https://github.com/9ft6/hamster_farm/raw/media/pics/cui.png" alt="User Interface">
</p>
<p align="center">
  <img src="https://github.com/9ft6/hamster_farm/raw/media/pics/bot.png" alt="Bot screenshot">
</p>

## Project Overview

**This project now is developing in private repository. Farm commander is online here [@FarmCommanderBot](https://t.me/FarmCommanderBot), but require approve. If you intrested and want to see sources or work with service please text me in telegram. [@dev9ft6]([https://t.me/FarmCommanderBot](https://t.me/dev9ft6)) **

This project started as an evening coding session over a beer to explore the mechanics of the hyped-up "Hamster Kombat." Now, it's an attempt to create a unified farm for similar projects. To work with it, you need to run the local server and bot modules located in `src/services`. Each module is essentially an API client with logic for auto-leveling, implementing useful functions, and displaying information in the terminal. Currently, there is a Telegram bot that allows users to verify themselves and administrators to approve user participation in the system. The bot supports hot account additions without needing to restart the runners. The system architecture is now microservice-based and includes the following components:

- Runners: Each runner is dedicated to managing a specific game.
- Telegram bot: Manages user registration and verification processes.
- Central FastAPI server: Manages account and user databases, communicates with the bot, and has WebSocket support for communication with the runners.

Implemented:
- [Hamster Kombat](https://github.com/9ft6/hamster_farm/tree/main/src/runners/hamster_kombat/README.md)
- [Bloom](https://github.com/9ft6/hamster_farm/tree/main/src/runners/bloom/README.md)

## Installation and Launch

add bot token to env/.env 
look 

add default user ids to data/users/admins or data/users/users


1. **Clone the repository**:
   If you have Git installed, you can clone the repository using:
   ```bash
   git clone https://github.com/9ft6/hamster_farm.git
   cd hamster_farm
   ```
   
2. **Create and activate a virtual environment**:
   Use make to create a virtual environment and install the required packages:
   ```bash
   make install
   ```
   
3. **Settings**:
   1. add telegram bot token to ```env/.env``` as you can see in ```env/.env.example```
   2. add default user telegram ids to ```data/users/admins``` or ```data/users/users``` files
   3. Create a directory named accounts/ in the root of the project and add files with game slugs (bloom, hamster_kombat). Learn more at game module pages.
   

4. **Run the local account server in one terminal**:
   ```bash
   make run-server
   ```

5. **Run the telegram bot**:
   ```bash
   make run-bot
   ```

6. **Run the local bots in different terminals**:
   ```bash
   make run-bloom
   ```
   or
   ```bash
   make run-hamster
   ```
   It's convenient to use tmux for this. The deployment is currently basic, but we will improve it.

<p align="center">
  <img src="https://github.com/9ft6/hamster_farm/raw/media/pics/cui.png" alt="User Interface">
</p>

## Project Overview

This project started as an evening coding session over a beer to explore the mechanics of the hyped-up "Hamster Kombat." Now, it's an attempt to create a unified farm for similar projects. To work with it, you need to run the local server and bot modules located in `src/services`. Each module is essentially an API client with logic for auto-leveling, implementing useful functions, and displaying information in the terminal. In the coming days, a Telegram bot will be developed to manage the system. It will help quickly add and maintain accounts, as well as monitor statistics and logs.

Implemented:
- [Hamster Kombat](https://github.com/9ft6/hamster_farm/tree/main/src/services/hamster_kombat/README.md)
- [Bloom](https://github.com/9ft6/hamster_farm/tree/main/src/services/bloom/README.md)

## Installation and Launch

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
   
3. **Create the accounts directory**:
   Create a directory named accounts/ in the root of the project and add files

4. **Run the local account server in one terminal**:
   ```bash
   make run-server
   ```

5. **Run the local bots in different terminals**:
   ```bash
   make run-bloom
   ```
   or
   ```bash
   make run-hamster
   ```
   It's convenient to use tmux for this. The deployment is currently basic, but we will improve it.

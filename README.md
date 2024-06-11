
<p align="center">
  <img src="https://github.com/9ft6/hamster_farm/raw/media/pics/cui.png" alt="User Interface">
</p>

## Introduction
This application (bot) is designed to automatically manage multiple Telegram accounts for playing the popular game Hamster Kombat (https://hamsterkombat.io). To generate hourly income around the clock, the game requires user participation every three hours, which is impossible and turns a proud primate into a slave to a rodent. Justice will be restored by the unyielding silicon hand of justice, embodied in my bot.
The bot takes authorized headers from the Telegram web app Hamster Combat, which can easily be obtained from a browser debugger. It doesn't matter if it's 1, 5, or 100 accounts. The bot uses asynchronous aiohttp requests and follows this algorithm: if the power is fully charged, it clicks; then it checks if it can buy a boost, and if available, it buys it and clicks again. After that, it finds the most profitable cards in the mining section, buys 5-6 of them, and goes to sleep for a random 2-5 minutes. The bot was created over a few beers and doesn't aim to be anything super special. Future plans include adding a Telegram bot to track account status and add/update new ones, as well as implementing combo purchases. Stay tuned!

## Using
- to open in browser use
https://github.com/mudachyo/Hamster-Kombat/tree/main?tab=readme-ov-file
- inspect requests in debugger and put in data/sessions config request's raw headers like 
```
POST /auth/me-telegram HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: en-US,en;q=0.9
Authorization: Bearer ...
Connection: keep-alive
Content-Length: 0
Host: api.hamsterkombat.io
Origin: https://hamsterkombat.io
Referer: https://hamsterkombat.io/
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-site
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36
sec-ch-ua: "Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Linux"
```
- if you have more accounts - put to sessions file and separate by new line
- use # char to put comments
- to enter morse passphrase just put in ```cfg.passphrase``` like this ```cfg.passphrase: str = "airdrop"``` and it will be automatically claimed

## TODO
- Claim tasks and earns
- update accounts management
- Telegram bot
- Stat to the bot
- Adding accounts by bot

## Done
- Console user interface
- refactor api module 

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

## TODO
- Claim tasks and earns
- update accounts management
- Telegram bot
- Stat to the bot
- Adding accounts by bot
- man to get token
- man to add token

## Done
- Console user interface
- refactor api module 

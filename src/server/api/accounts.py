from fastapi import HTTPException

from db import accounts
from db.models import InitData, Tokens
from server.app import app
from server.logger import logger


@app.post("/init_data/{game_slug}")
async def add_init_data(game_slug: str, init_data: InitData):
    if init_data.user_id in accounts:
        message = "Already exists. Update init data"
    else:
        message = "Init data added"
    accounts.add_init_data(game_slug, init_data)
    return {"message": message}

@app.post("/tokens/{game_slug}/{user_id}")
async def add_tokens(user_id: str, game_slug: str, tokens: Tokens):
    logger.debug(f"Update tokens for {game_slug}/{user_id}")
    await accounts.add_tokens(int(user_id), game_slug, tokens)


@app.get("/accounts/{game_slug}")
async def get_accounts(game_slug: str):
    result = await accounts.get_accounts_by_slug(game_slug)
    logger.debug(f"Get accounts: {result}")
    return result


@app.delete("/remove_game/{slug}/{user_id}")
async def remove_game(slug: str, user_id: str):
    # TODO: check
    if (account := accounts[user_id]) and slug in account.init_datas:
        del account.init_data[slug]
        await accounts.dump()
        return {"message": "Game removed"}

    raise HTTPException(status_code=404, detail="Game or account not found")


@app.delete("/account/{user_id}")
async def delete_account(user_id: str):
    # TODO: check
    if account := accounts[user_id]:
        accounts.remove(account)
        return {"message": "Account deleted"}

    raise HTTPException(status_code=404, detail="Account not found")

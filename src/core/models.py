from pydantic import BaseModel, Field


class TgUser(BaseModel):
    id: int = Field(..., alias="id")
    name: str = Field(..., alias="firstName")
    is_bot: bool = Field(..., alias="isBot")
    last_name: str = Field(..., alias="lastName")
    lang: str = Field(..., alias="languageCode")


class Result(BaseModel):
    success: bool
    data: dict | None = None
    error: str | None = None


class Ok(Result):
    success: bool = True


class Error(Result):
    success: bool = False


__all__ = [
    "Result",
    "Ok",
    "Error",
    "TgUser",
]

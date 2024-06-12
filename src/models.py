from pydantic import BaseModel, Field


class User(BaseModel):
    id: int = Field(..., alias="id")
    name: str = Field(..., alias="firstName")
    is_bot: bool = Field(..., alias="isBot")
    last_name: str = Field(..., alias="lastName")
    lang: str = Field(..., alias="languageCode")


class Upgrade(BaseModel):
    ...

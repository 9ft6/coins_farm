from pydantic import BaseModel, Extra


class BloomUser(BaseModel):
    id: str
    username: str

    class Config:
        extra = Extra.ignore

    def __init__(self, id: dict, username: str, **kwargs):
        super().__init__(id=str(id["id"]), username=username, **kwargs)

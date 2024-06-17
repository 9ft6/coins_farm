from pydantic import BaseModel


class BloomUser(BaseModel):
    id: str
    username: str

    def __init__(self, id: dict, username: str):
        super().__init__(id=id["id"], username=username)

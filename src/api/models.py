from pydantic import BaseModel


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
]

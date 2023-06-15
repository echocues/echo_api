from pydantic import BaseModel

__all__ = "Token", "TokenData"


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

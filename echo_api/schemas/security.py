from typing import Optional

from pydantic import BaseModel

__all__ = "Token", "TokenData"


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None

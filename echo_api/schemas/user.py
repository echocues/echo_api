from pydantic import BaseModel

__all__ = "User", "UserCreate", "UserLogin"


class User(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str

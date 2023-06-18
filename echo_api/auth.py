from __future__ import annotations

import os
from datetime import datetime, timedelta
from typing import Annotated, Any, Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

# noinspection PyPackageRequirements
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from echo_api import crud, database, schemas

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
SECRET_KEY = os.getenv("SECRET_KEY", default="")
if SECRET_KEY == "":
    raise Exception("SECRET_KEY was not set.")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(
    data: dict[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    db: database.db_depends, token: Annotated[str, Depends(oauth2_scheme)]
) -> database.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await crud.get_user_by_username(db, token_data.username)
    if user is None:
        raise credentials_exception
    return user


user_depends = Annotated[database.User, Depends(get_current_user)]


async def authenticate_user(
    db: AsyncSession, username: str, password: str
) -> database.User | None:
    user = await crud.get_user_by_username(db, username)
    if user and verify_password(password, user.hashed_password):
        return user
    return None

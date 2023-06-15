from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

import echo_api
from echo_api import schemas, database
from echo_api.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
)

auth = APIRouter()


@auth.post("/token", response_model=schemas.Token, tags=["auth"])
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: database.db_depends
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = echo_api.auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")


@auth.get("/me/", response_model=schemas.User, tags=["auth"])
async def read_users_me(current_user: echo_api.auth.user_depends):
    return current_user

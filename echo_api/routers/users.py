from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from echo_api import crud, schemas, database

users = APIRouter()


@users.post("/", response_model=schemas.User, tags=["users", "create"])
async def create_user(user: schemas.UserCreate, db: database.db_depends):
    db_user = await crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=409, detail="Username already registered")

    return await crud.create_user(db=db, user=user)


@users.get("/{user_id}", response_model=schemas.User, tags=["users", "get"])
async def get_user(user_id: int, db: database.db_depends):
    return await crud.get_user(db, user_id)

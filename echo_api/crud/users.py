from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from echo_api import auth, database, schemas


async def get_user(db: AsyncSession, user_id: int) -> database.User | None:
    return await db.scalar(select(database.User).filter(database.User.id == user_id))  # type: ignore


async def get_user_by_username(db: AsyncSession, username: str) -> database.User | None:
    return await db.scalar(  # type: ignore
        select(database.User).filter(database.User.username == username)
    )


async def create_user(db: AsyncSession, user: schemas.UserCreate) -> database.User:
    hashed_password = auth.get_password_hash(user.password)
    db_user = database.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

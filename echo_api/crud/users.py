from echo_api import database, schemas, auth
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

__all__ = "get_user", "get_user_by_username", "get_users", "create_user"


async def get_user(db: AsyncSession, user_id: int):
    return await db.scalar(select(database.User).filter(database.User.id == user_id))


async def get_user_by_username(db: AsyncSession, username: str):
    return await db.scalar(
        select(database.User).filter(database.User.username == username)
    )


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    return await db.scalars(select(database.User).offset(skip).limit(limit))


async def create_user(db: AsyncSession, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = database.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

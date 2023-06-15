from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

__all__ = (
    "SQLALCHEMY_DATABASE_URL",
    "engine",
    "SessionLocal",
    "Base",
    "get_db",
    "db_depends",
)

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


db_depends = Annotated[AsyncSession, Depends(get_db)]

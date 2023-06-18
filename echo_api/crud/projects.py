from __future__ import annotations

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from echo_api import database, schemas


async def get_projects(
    db: AsyncSession, owner_id: int, skip: int = 0, limit: int = 100
) -> Sequence[database.Project]:
    results = await db.scalars(
        select(database.Project)
        .filter(database.Project.owner_id == owner_id)
        .offset(skip)
        .limit(limit)
    )
    return results.all()


async def get_project(db: AsyncSession, project_id: int) -> database.Project | None:
    return await db.scalar(  # type: ignore
        select(database.Project).filter(database.Project.id == project_id)
    )


async def create_project(
    db: AsyncSession, project: schemas.ProjectCreate, user_id: int
) -> database.Project:
    db_project = database.Project(**project.dict(), owner_id=user_id)
    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)
    return db_project

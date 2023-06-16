from sqlalchemy import select

from echo_api import database, schemas
from sqlalchemy.ext.asyncio import AsyncSession

__all__ = "get_projects", "get_project", "create_project"


async def get_projects(db: AsyncSession, owner_id: int, skip: int = 0, limit: int = 100):
    results = await db.scalars(
        select(database.Project).filter(database.Project.owner_id == owner_id).offset(skip).limit(limit)
    )
    return results.all()


async def get_project(db: AsyncSession, project_id: int):
    return await db.scalar(
        select(database.Project).filter(database.Project.id == project_id)
    )


async def create_project(
    db: AsyncSession, project: schemas.ProjectCreate, user_id: int
):
    db_project = database.Project(**project.dict(), owner_id=user_id)
    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)
    return db_project

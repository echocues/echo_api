from typing import Sequence

from fastapi import APIRouter, HTTPException

from echo_api import auth, crud, database, schemas

projects_router: APIRouter = APIRouter()


@projects_router.post("/", response_model=schemas.Project, tags=["projects", "create"])
async def create_project(
    project: schemas.ProjectCreate,
    db: database.db_depends,
    current_user: auth.user_depends,
) -> database.Project:
    return await crud.create_project(db=db, project=project, user_id=current_user.id)


@projects_router.get(
    "/", response_model=list[schemas.Project], tags=["projects", "get"]
)
async def get_projects(
    db: database.db_depends,
    current_user: auth.user_depends,
    skip: int = 0,
    limit: int = 100,
) -> Sequence[database.Project]:
    return await crud.get_projects(db, current_user.id, skip=skip, limit=limit)


@projects_router.get(
    "/{project_id}", response_model=schemas.Project, tags=["projects", "get"]
)
async def get_project(
    project_id: int, db: database.db_depends, current_user: auth.user_depends
) -> database.Project:
    project = await crud.get_project(db, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project does not exist.")
    if current_user.id != project.owner_id:
        raise HTTPException(
            status_code=403, detail="You are not authorized to view this project."
        )
    return project

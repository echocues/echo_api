from fastapi import APIRouter

from echo_api import crud, schemas, database, auth

projects = APIRouter()


@projects.post("/", response_model=schemas.Project, tags=["projects", "create"])
async def create_project(
    project: schemas.ProjectCreate,
    db: database.db_depends,
    current_user: auth.user_depends,
):
    return await crud.create_project(db=db, project=project, user_id=current_user.id)


@projects.get("/{project_id}", response_model=schemas.Project, tags=["projects", "get"])
async def get_project(
    project_id: int, db: database.db_depends, current_user: auth.user_depends
):
    project = await crud.get_project(db, project_id)

    return await crud.get_project(db, project_id)

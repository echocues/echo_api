from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import FileResponse, Response

from echo_api import auth, crud, database, schemas

projects_router: APIRouter = APIRouter()


async def get_project_dep(
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


project_depends = Annotated[database.Project, Depends(get_project_dep)]


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
async def get_project(project: project_depends) -> database.Project:
    return project


@projects_router.get(
    "/file/{project_id}", response_class=FileResponse, tags=["projects", "get"]
)
async def get_project_file(project: project_depends) -> FileResponse:
    return await crud.read_project_file(project.id)


@projects_router.put("/file/{project_id}", tags=["projects", "get"], status_code=204)
async def write_project_file(file: UploadFile, project: project_depends) -> Response:
    await crud.upload_project_file(project.id, file)

    return Response(status_code=204)

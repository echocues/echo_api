from fastapi import APIRouter, HTTPException

from echo_api import crud, database, schemas

users_router: APIRouter = APIRouter()


@users_router.post("/", response_model=schemas.User, tags=["users", "create"])
async def create_user(
    user: schemas.UserCreate, db: database.db_depends
) -> database.User:
    db_user = await crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=409, detail="Username already registered")

    return await crud.create_user(db=db, user=user)


@users_router.get("/{user_id}", response_model=schemas.User, tags=["users", "get"])
async def get_user(user_id: int, db: database.db_depends) -> database.User:
    user = await crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User does not exist.")
    return user

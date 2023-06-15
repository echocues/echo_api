from echo_api import routers, database
from fastapi import FastAPI

tags_metadata = [
    {"name": "users", "description": "Operations with users."},
    {"name": "projects", "description": "Operations with projects."},
    {
        "name": "auth",
        "description": "Authentication and authorization operations. Login logic is here.",
    },
    {"name": "get", "description": "All *get* operations."},
    {"name": "create", "description": "All *create* operations."},
]

# noinspection PyArgumentEqualDefault
app = FastAPI(
    title="EchoCues API",
    version="0.1.0",
    description="API to access the EchoCues database.",
    swagger_ui_parameters={"syntaxHighlight.theme": "monokai"},
    openapi_tags=tags_metadata,
)

app.include_router(routers.users, prefix="/users")
app.include_router(routers.auth, prefix="/auth")
app.include_router(routers.projects, prefix="/projects")


@app.on_event("startup")
async def startup():
    async with database.engine.begin() as conn:
        await conn.run_sync(database.Base.metadata.create_all)

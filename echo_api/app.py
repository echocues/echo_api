from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from echo_api import database, routers

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


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routers.users_router, prefix="/users")
app.include_router(routers.auth_router, prefix="/auth")
app.include_router(routers.projects_router, prefix="/projects")


@app.on_event("startup")
async def startup() -> None:
    logger.info("EchoAPI started.")

    async with database.engine.begin() as conn:
        await conn.run_sync(database.Base.metadata.create_all)

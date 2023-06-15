from pydantic import BaseModel

__all__ = "Project", "ProjectCreate"


class Project(BaseModel):
    id: int
    title: str
    description: str
    owner_id: int

    class Config:
        orm_mode = True


class ProjectCreate(BaseModel):
    title: str
    description: str

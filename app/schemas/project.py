from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)


class ProjectOut(BaseModel):
    id: int
    name: str


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)

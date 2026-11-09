from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from app.models import TaskStatus


# Проекты

class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class ProjectResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


# Задачи

class TaskCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)

    description: str = Field(
        min_length=1,
        max_length=2000
    )

    project_id: int


class TaskResponse(BaseModel):
    id: int
    name: str
    description: str
    project_id: int
    status: TaskStatus
    create_date: datetime
    resolve_date: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

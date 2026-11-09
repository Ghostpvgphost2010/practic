from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime,
    Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base
import enum


class TaskStatus(str, enum.Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    tasks = relationship(
        "Task",
        back_populates="project",
        cascade="all, delete-orphan"
    )


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False
    )

    status = Column(
        Enum(TaskStatus),
        default=TaskStatus.CREATED,
        nullable=False
    )

    create_date = Column(
        DateTime,
        server_default=func.now()
    )

    resolve_date = Column(
        DateTime,
        nullable=True
    )

    project = relationship(
        "Project",
        back_populates="tasks"
    )

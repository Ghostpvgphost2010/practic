from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from datetime import datetime

from app.database import Base, engine, get_db
from app import models, schemas


# Создание таблиц
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Project Manager API",
    description="API для управления проектами и задачами",
    version="1.0.0"
)


# --------------------------------
# СОЗДАНИЕ ПРОЕКТА
# --------------------------------

@app.post("/projects/", response_model=schemas.ProjectResponse)
def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db)
):
    db_project = models.Project(
        name=project.name
    )

    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    return db_project


# --------------------------------
# ПОЛУЧЕНИЕ СПИСКА ПРОЕКТОВ
# --------------------------------

@app.get("/projects/", response_model=list[schemas.ProjectResponse])
def get_projects(
    db: Session = Depends(get_db)
):
    projects = db.query(models.Project).all()

    return projects


# --------------------------------
# СОЗДАНИЕ ЗАДАЧИ В ПРОЕКТЕ
# --------------------------------

@app.post("/projects/{project_id}/tasks/",
          response_model=schemas.TaskResponse)
def create_task(
    project_id: int,
    task: schemas.TaskCreate,
    db: Session = Depends(get_db)
):
    project = db.query(models.Project).filter(
        models.Project.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    if task.project_id != project_id:
        raise HTTPException(
            status_code=400,
            detail="Project ID mismatch"
        )

    db_task = models.Task(
        name=task.name,
        description=task.description,
        project_id=project_id,
        status=models.TaskStatus.CREATED
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


# --------------------------------
# ПОЛУЧЕНИЕ ЗАДАЧИ
# --------------------------------

@app.get("/tasks/{task_id}",
         response_model=schemas.TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task

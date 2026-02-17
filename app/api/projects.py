from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.database import get_db
from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectOut, ProjectCreate

router = APIRouter(tags=["projects"])


@router.post("/", response_model=ProjectOut)
def create_project(
        project: ProjectCreate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    new_project = Project(name=project.name, owner_id=current_user.id)

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project


@router.get("/", response_model=list[ProjectOut])
def get_projects(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    projects = db.query(Project).filter(Project.owner_id == current_user.id).all()
    return projects


@router.get("/{project_id}", response_model=ProjectOut)
def get_project(
        project_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    project = (db.query(Project)
               .filter(Project.id == project_id, Project.owner_id == current_user.id)
               .first())
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project

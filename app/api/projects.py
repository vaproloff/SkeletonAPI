from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.database import get_db
from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectOut, ProjectUpdate

router = APIRouter(prefix="/projects", tags=["projects"])


def _get_owned_project(db: Session, user_id: int, project_id: int) -> Project | None:
    return db.query(Project).filter(Project.id == project_id, Project.owner_id == user_id).first()


@router.post("", response_model=ProjectOut)
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


@router.get("", response_model=list[ProjectOut])
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
    project = _get_owned_project(db, current_user.id, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project


@router.patch("/{project_id}", response_model=ProjectOut)
def update_project(
        project_id: int,
        project_in: ProjectUpdate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    project = _get_owned_project(db, current_user.id, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project_in.name is not None:
        project.name = project_in.name

    project.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(project)

    return project


@router.delete("/{project_id}", status_code=204)
def delete_project(
        project_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    project = _get_owned_project(db, current_user.id, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(project)
    db.commit()

    return Response(status_code=204)

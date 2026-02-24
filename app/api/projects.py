from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectOut, ProjectUpdate
from app.services import project_service

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("", response_model=ProjectOut)
def create_project(
        project_in: ProjectCreate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    return project_service.create_project(db, current_user, project_in)


@router.get("", response_model=list[ProjectOut])
def get_projects(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    return project_service.get_projects(db, current_user)


@router.get("/{project_id}", response_model=ProjectOut)
def get_project(
        project_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    project = project_service.get_project(db, current_user, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    return project


@router.patch("/{project_id}", response_model=ProjectOut)
def update_project(
        project_id: int,
        project_in: ProjectUpdate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    project = project_service.update_project(db, current_user, project_id, project_in)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    return project


@router.delete("/{project_id}", status_code=204)
def delete_project(
        project_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    deleted = project_service.delete_project(db, current_user, project_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Project not found")

    return Response(status_code=204)

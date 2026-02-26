from fastapi import APIRouter, Depends, Query
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
        limit: int = Query(default=20, ge=1, le=100),
        offset: int = Query(default=0, ge=0),
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    return project_service.get_projects(db, current_user, limit=limit, offset=offset)


@router.get("/{project_id}", response_model=ProjectOut)
def get_project(
        project_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    return project_service.get_project(db, current_user, project_id)


@router.patch("/{project_id}", response_model=ProjectOut)
def update_project(
        project_id: int,
        project_in: ProjectUpdate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    return project_service.update_project(db, current_user, project_id, project_in)


@router.delete("/{project_id}", status_code=204)
def delete_project(
        project_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    project_service.delete_project(db, current_user, project_id)

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.user import User
from app.repositories import project_repo
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.services.exceptions import NotFoundError


def create_project(db: Session, user: User, data: ProjectCreate) -> Project:
    project = project_repo.create(db, user.id, data.name)

    db.commit()
    db.refresh(project)

    return project


def get_projects(db: Session, user: User, *, limit: int, offset: int) -> list[Project]:
    return project_repo.list_by_owner(db, user.id, limit, offset)


def get_project(db: Session, user: User, project_id: int) -> Project:
    project = project_repo.get_owned_by_id(db, user.id, project_id)
    if project is None:
        raise NotFoundError("Project not found")

    return project


def update_project(db: Session, user: User, project_id: int, data: ProjectUpdate) -> Project:
    project = project_repo.get_owned_by_id(db, user.id, project_id)
    if project is None:
        raise NotFoundError("Project not found")

    if data.name is not None:
        project.name = data.name
        project.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(project)

    return project


def delete_project(db: Session, user: User, project_id: int) -> None:
    project = project_repo.get_owned_by_id(db, user.id, project_id)
    if project is None:
        raise NotFoundError("Project not found")

    project_repo.delete(db, project)
    db.commit()

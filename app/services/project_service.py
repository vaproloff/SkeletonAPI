from datetime import datetime, timezone

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.services.exceptions import NotFoundError


def _get_owned_project(db: Session, user_id: int, project_id: int) -> Project | None:
    return db.query(Project).filter(Project.id == project_id, Project.owner_id == user_id).first()


def create_project(db: Session, user: User, data: ProjectCreate) -> Project:
    project = Project(name=data.name, owner_id=user.id)

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


def get_projects(db: Session, user: User, *, limit: int, offset: int) -> list[Project]:
    return (db.query(Project)
            .filter(Project.owner_id == user.id)
            .order_by(desc(Project.id))
            .limit(limit)
            .offset(offset)
            .all()
            )


def get_project(db: Session, user: User, project_id: int) -> Project:
    project = _get_owned_project(db, user.id, project_id)
    if project is None:
        raise NotFoundError("Project not found")

    return project


def update_project(db: Session, user: User, project_id: int, data: ProjectUpdate) -> Project:
    project = _get_owned_project(db, user.id, project_id)
    if project is None:
        raise NotFoundError("Project not found")

    if data.name is not None:
        project.name = data.name
        project.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(project)

    return project


def delete_project(db: Session, user: User, project_id: int) -> None:
    project = _get_owned_project(db, user.id, project_id)
    if project is None:
        raise NotFoundError("Project not found")

    db.delete(project)
    db.commit()

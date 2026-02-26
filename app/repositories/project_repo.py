from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.project import Project


def get_owned_by_id(db: Session, owner_id: int, project_id: int) -> Project | None:
    return (db.query(Project)
            .filter(Project.id == project_id, Project.owner_id == owner_id)
            .first()
            )


def list_by_owner(db: Session, owner_id: int, limit: int, offset: int) -> list[Project]:
    return (db.query(Project)
            .filter(Project.owner_id == owner_id)
            .order_by(desc(Project.id))
            .limit(limit)
            .offset(offset)
            .all()
            )


def create(db: Session, owner_id: int, name: str) -> Project:
    project = Project(name=name, owner_id=owner_id)
    db.add(project)
    return project


def delete(db: Session, project: Project) -> None:
    db.delete(project)

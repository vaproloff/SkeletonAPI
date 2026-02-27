import pytest

from app.core.security import hash_password
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.schemas.user import UserCreate
from app.services import auth_service, project_service
from app.services.exceptions import AlreadyExistsError, NotFoundError


def test_get_unknown_project(db_session):
    user = User(email="test@test.com", hashed_password=hash_password("secret"))
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    with pytest.raises(NotFoundError):
        project_service.get_project(db_session, user, 123)


def test_duplicate_user_register(db_session):
    user = User(email="dup@test.com", hashed_password=hash_password("secret"))
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    with pytest.raises(AlreadyExistsError):
        auth_service.register_user(db_session, UserCreate(email="dup@test.com", password="secret2"))


def test_update_project_updates_timestamp(db_session):
    user = User(email="update@test.com", hashed_password=hash_password("secret"))
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    project = project_service.create_project(db_session, user, ProjectCreate(name="Test Project"))
    old_updated_at = project.updated_at
    updated_project = project_service.update_project(db_session, user, project.id,
                                                     ProjectUpdate(name="Test Project v.2"))
    assert updated_project.name == "Test Project v.2"
    assert updated_project.updated_at > old_updated_at

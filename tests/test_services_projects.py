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


def test_duplicate_user_registration(db_session):
    user = User(email="dup@test.com", hashed_password=hash_password("secret"))
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    with pytest.raises(AlreadyExistsError):
        auth_service.register_user(db_session, UserCreate(email="dup@test.com", password="secret2"))

    user = auth_service.register_user(db_session,
                                      UserCreate(email="no_dup@test.com", password="secret"))
    assert user is not None


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


def test_create_project_duplicate(db_session):
    user = User(email="test@test.com", hashed_password=hash_password("secret"))
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    project_service.create_project(db_session, user, ProjectCreate(name="Project 1"))

    with pytest.raises(AlreadyExistsError):
        project_service.create_project(db_session, user, ProjectCreate(name="Project 1"))

    project2 = project_service.create_project(db_session, user, ProjectCreate(name="Project 2"))
    assert project2.name == "Project 2"


def test_create_project_duplicate_with_another_owner(db_session):
    user1 = auth_service.register_user(db_session, UserCreate(email="1@test.com", password="s"))
    project1 = project_service.create_project(db_session, user1, ProjectCreate(name="Project"))

    user2 = auth_service.register_user(db_session, UserCreate(email="2@test.com", password="s"))
    project2 = project_service.create_project(db_session, user2, ProjectCreate(name="Project"))

    assert project1.owner_id == user1.id
    assert project2.owner_id == user2.id
    assert project1.name == project2.name

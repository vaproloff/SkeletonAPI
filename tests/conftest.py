import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from app.database import Base, get_db
from app.main import app

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql://app:app@localhost:5432/app_test",
)

engine_test = create_engine(TEST_DATABASE_URL)
SessionLocalTest = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


@pytest.fixture(scope="session", autouse=True)
def create_test_schema():
    Base.metadata.drop_all(bind=engine_test)
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)


@pytest.fixture()
def db_session():
    """
    Изоляция: каждый тест в транзакции, в конце rollback.
    """
    connection = engine_test.connect()
    transaction = connection.begin()
    session = SessionLocalTest(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture()
def client(db_session):
    """
    Подменяем get_db на тестовую сессию.
    """

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

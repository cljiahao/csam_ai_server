import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app import app
from db.base import Base
from db.session import get_db

from core.directory import directory

SQLALCHEMY_DATABASE_URL = f"sqlite:///{directory.base_dir}/tests/test_db.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(engine)  # Create the tables.

@pytest.fixture(scope="session", autouse=True)
def cleanup_database(request):
    """Cleanup the test database after tests have run."""

    def remove_test_db():
        # Ensure that connections and sessions are closed
        Base.metadata.drop_all(bind=engine)
        engine.dispose()

        # Remove the test database file
        if os.path.exists(SQLALCHEMY_DATABASE_URL.replace("sqlite:///", "")):
            os.remove(SQLALCHEMY_DATABASE_URL.replace("sqlite:///", ""))

    request.addfinalizer(remove_test_db)

@pytest.fixture(scope="function")
def db_session(request):
    """Create a new database session with a rollback at the end of the test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSession(bind=connection)

    def teardown():
        session.close()
        transaction.rollback()
        connection.close()

    request.addfinalizer(teardown)
    yield session


@pytest.fixture(scope="function")
def test_client(db_session:Session):
    """Create a test client that uses the override_get_db fixture to return a session."""

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client

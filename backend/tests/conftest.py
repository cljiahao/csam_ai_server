import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from src.app import start_application
from src.core.directory import directory
from src.db.base import Base
from src.db.session import get_db

# SQLite database URL for testing
SQLITE_DATABASE_URL = f"sqlite:///{directory.base_dir}/tests/test_db.db"

# Create a SQLAlchemy engine
engine = create_engine(
    SQLITE_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Create a sessionmaker to manage sessions
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def mock_create_tables():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Test")


@pytest.fixture(autouse=True)
def app(monkeypatch):
    monkeypatch.setattr("src.app.create_tables", mock_create_tables)
    _app = start_application()
    yield _app


@pytest.fixture(scope="session", autouse=True)
def cleanup_database(request):
    """Cleanup the test database after tests have run."""
    Base.metadata.drop_all(bind=engine)

    def remove_test_db():
        # Ensure that connections and sessions are closed
        engine.dispose()

        # Remove the test database file
        if os.path.exists(SQLITE_DATABASE_URL.replace("sqlite:///", "")):
            os.remove(SQLITE_DATABASE_URL.replace("sqlite:///", ""))

    request.addfinalizer(remove_test_db)


@pytest.fixture(scope="function")
def db_session(request):
    """Create a new database session with a rollback at the end of the test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    def teardown():
        session.close()
        transaction.rollback()
        connection.close()

    request.addfinalizer(teardown)
    yield session


@pytest.fixture(scope="function")
def test_client(db_session, app):
    """Create a test client that uses the override_get_db fixture to return a session."""

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
